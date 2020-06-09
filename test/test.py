import requests
import json
import time

BASE_URL = "http://localhost:5000/v1"

EMAIL = "alexander@musicom.com"
FIRST_NAME = "Alexander"
LAST_NAME = "Gutierrez"
PASSWORD = "1234"
headers = {
    'Content-Type': 'application/json',
    'Authorization': ''
}

t = time.time()
# Signup
res = requests.post(
    f"{BASE_URL}/auth/signup",
    headers=headers,
    data=json.dumps({
        "email": EMAIL,
        "first_name": FIRST_NAME,
        "last_name": LAST_NAME,
        "password": PASSWORD
    })
)
if res.status_code == 400:
    res = requests.post(
        f"{BASE_URL}/auth/login",
        headers=headers,
        data=json.dumps({
            "email": EMAIL,
            "password": PASSWORD
        })
    )

headers['Authorization'] = "Bearer "+res.json()['token']
profile_id = res.json()['profile_id']
print(res.json())

# profile
# res = requests.put(
#     f"{BASE_URL}/profile/t",
#     headers=headers,
#     data=json.dumps({
#         "status": "test 1"
#     })
# )
# print(res.json())

# list
res = requests.get(f"{BASE_URL}/userProfiles?profile_id="+profile_id, headers=headers)
print(res.json())

print(time.time()-t)
