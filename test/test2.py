import requests
import json
import time

BASE_URL = "http://localhost:5000/v1"

users = [
    {
        "email": "alexander.pjzz@gmail.com",
        "first_name": "Alexander",
        "last_name": "Gutierrez",
        "profile_id": "",
        "password": "1234",
        "token": ""
    },
    {
        "email": "jorge@example.com",
        "first_name": "Jorge",
        "last_name": "Gonzalez",
        "profile_id": "",
        "password": "12345678",
        "token": ""
    },
    {
        "email": "andres@example.com",
        "first_name": "Andres",
        "last_name": "Deza",
        "profile_id": "",
        "password": "12345678",
        "token": ""
    },
    {
        "email": "camila@example.com",
        "first_name": "Camila",
        "last_name": "Araneda",
        "profile_id": "",
        "password": "12345678",
        "token": ""
    }
]

headers = {
    'Content-Type': 'application/json',
    'Authorization': ''
}


def register_user(email, first_name, last_name, password):
    res = requests.post(
        f"{BASE_URL}/auth/signup",
        headers=headers,
        data=json.dumps({
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "password": password
        })
    )
    return res


def login_user(user):
    res = requests.post(
        f"{BASE_URL}/auth/login",
        headers=headers,
        data=json.dumps({
            "email": user['email'],
            "password": user['password']
        })
    )
    return res


def list_profiles(user):
    res = requests.get(
        f"{BASE_URL}/userProfiles?profile_id=" + user['profile_id'],
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {user["token"]}'
        }
    )
    print(res.json())
    print(len(res.json()['users']))
    return res


if __name__ == '__main__':

    start_time = time.time()
    for user in users:
        res = register_user(
            user['email'],
            user['first_name'],
            user['last_name'],
            user['password']
        )
        if res.status_code == 400:
            res = login_user(user)
        print(res.json())
        user['profile_id'] = res.json()['profile_id']
        user['token'] = res.json()['token']

    list_profiles(users[0])
    print(f"Time: {time.time()-start_time}")
