import requests


def get_questions():
    url = "http://127.0.0.1:8000/get_questions/"
    params = {"questions_num": 1}
    headers = {"Accept": "application/json"}

    response = requests.post(url, params=params, headers=headers)

    if response.status_code == 200:
        result = response.json()
        print(result)
    else:
        print(f"Ошибка {response.status_code}: {response.text}")


if __name__ == "__main__":
    get_questions()
