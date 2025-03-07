import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from PIL import Image
from io import BytesIO
import uvicorn
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
import base64

load_dotenv()
genai_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

app = FastAPI(title="Gemini API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TextRequest(BaseModel):
    text: str
    system_prompt: Optional[str] = "You are a helpful assistant."


class ImageRequest(BaseModel):
    image: str  # Base64 encoded image data


@app.post("/api/text")
async def process_text(request: TextRequest):
    try:
        # Create a chat session with the system prompt
        sys_instruct = request.system_prompt

        response = genai_client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction=sys_instruct),
            contents=[request.text]
        )

        return {
            "response": response.text,
            "success": True
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing text: {str(e)}")


@app.post("/api/analyze-food")
async def analyze_food(request: ImageRequest):
    # try:
    # Decode base64 image
    try:
        # Try to decode with base64 header
        if ',' in request.image:
            _, image_data = request.image.split(',', 1)
        else:
            image_data = request.image

        img_bytes = base64.b64decode(image_data)
        img = Image.open(BytesIO(img_bytes))
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Invalid base64 image: {str(e)}")

    system_prompt = "You are the best nutritionist in the world."

    prompt = """
    This is a picture of some food. 
    Please analyze the food nutrients, calculate each element with potential calories count and calculate the total calories.
    You should provide a short description of the food and the total calories count in the form of a JSON object with the following format.
    { "calories": 0 , "descriptions": "A short description of the food." }
    """

    # Generate content using the vision model
    response = genai_client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json",
            response_schema=genai.types.Schema(
                type=genai.types.Type.OBJECT,
                properties={
                    "descriptions": genai.types.Schema(
                        type=genai.types.Type.STRING,
                    ),
                    "calories": genai.types.Schema(
                        type=genai.types.Type.NUMBER,
                    ),
                },
            ),
        ),
        contents=[img, prompt]
    )

    result = json.loads(response.text)

    return result

    # except Exception as e:
    #     print(e)
    #     raise HTTPException(
    #         status_code=500, detail=f"Error analyzing food image: {str(e)}")


@app.get("/")
async def root():
    return {"message": "Welcome to the Gemini API. Use /api/text for text generation and /api/analyze-food for food calorie estimation."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
