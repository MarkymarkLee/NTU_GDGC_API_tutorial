import requests
import base64


def test_main():
    url = "http://127.0.0.1:8000"
    response = requests.get(url)

    print(response.json())

    assert response.status_code == 200


def test_text_generation():
    url = "http://127.0.0.1:8000/api/text"
    data = {
        "text": "I am feeling happy today."
    }
    response = requests.post(url, json=data)

    print(response.json())

    assert response.status_code == 200


def test_food_analysis():
    url = "http://127.0.0.1:8000/api/analyze-food"

    # Open the image and encode it to base64

    image_path = "salad.jpg"
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    data = {
        "image": encoded_image
    }
    response = requests.post(url, json=data)

    print(response.json())

    assert response.status_code == 200


if __name__ == "__main__":
    # test_main()
    # test_text_generation()
    test_food_analysis()
