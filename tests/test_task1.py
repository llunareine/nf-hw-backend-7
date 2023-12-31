import requests


def test_get_signup():
    response = requests.get("http://localhost:8000/signup")
    assert "email" in response.text
    assert "text" in response.text
    assert "password" in response.text


def test_post_signup_invalid():
    data = {"email": ""}
    response = requests.post("http://localhost:8000/signup", data=data)
    assert response.status_code == 422


def test_post_signup_valid():
    data = {
        "email": "test@test.com",
        "full_name": "Aibek Azamatov",
        "password": "123"
    }

    photo_file = open("/home/llunareine/nFactorial/new-hw-backend-6/tests/cat.jpeg", "rb")
    files = {"photo": photo_file}

    response = requests.post(
        "http://localhost:8000/signup",
        data=data,
        files=files,
        allow_redirects=False
    )
    assert response.status_code == 303
    assert "/login" in response.headers.get("location")
