import requests
import json
import time
import os
import random

BASE_URL = "http://localhost:5000/v1"
BASE_PATH = os.path.dirname(__file__)

my_user = {
        "email": "alexander@example.com",
        "first_name": "Alexander",
        "last_name": "Gutierrez",
        "profile_id": "",
        "status": "Guitarrista",
        "music_styles": ["Jazz", "Funk", "Rock", "Son"],
        "principal_instrument": "Guitarra",
        "bio": "Esta es mi bio hermosa uwu",
        "region": "Metropolitana de Santiago",
        "password": "12345678",
        "token": ""
    }
from datetime import datetime, timedelta
timedelta(minutes=3)


class RandomUsersGenerator:
    _first_names_file = f"{BASE_PATH}/data/first_names.all.txt"
    _last_names_file = f"{BASE_PATH}/data/last_names.all.txt"

    _instruments = ["Acordeón", "Armónica", "Arpa", "Bajo", "Batería", "Bodhrán", "Castañuelas",
                    "Cajón", "Charango", "Clarinete", "Contrabajo", "Cuatro", "Voz", "Guitarra", "Piano"]
    _regions = ["Aisén del G. Carlos Ibáñez del Campo", "Antofagasta",
                "Arica y Parinacota", "Atacama", "Biobío", "Coquimbo", "La Araucanía",
                "Libertador General Bernardo O'Higgins", "Los Lagos", "Los Ríos",
                "Magallanes y de la Antártica Chilena", "Maule", "Metropolitana de Santiago",
                "Ñuble", "Tarapacá", "Valparaíso"]

    def __init__(self):
        with open(self._first_names_file, 'r', errors='ignore', encoding='utf8') as f:
            self._first_names = f.read().strip().split('\n')
        f.close()
        with open(self._last_names_file, 'r', errors='ignore', encoding='utf8') as f:
            self._last_names = f.read().strip().split('\n')
        f.close()

    def _get_rfn(self):
        return self._first_names[random.randint(0, len(self._first_names)-1)]

    def _get_rln(self):
        return self._last_names[random.randint(0, len(self._last_names)-1)]

    def generate_random_user(self):
        fn = self._get_rfn()
        ln = self._get_rln()
        email = f"{fn[0]}.{ln}@example.com"
        return {
            "first_name": fn,
            "last_name": ln,
            "email": email,
            "status": "test status",
            "music_styles": ["Jazz", "Funk", "Rock", "Son"],
            "principal_instrument": self._instruments[random.randint(0, len(self._instruments)-1)],
            "region": self._regions[random.randint(0, len(self._regions)-1)],
            "bio": ("Bio de prueba para el testeo de la aplicación."
                    "esta bio no es más que un texto al azar que"
                    "ocupe éste espacio por motivos de test."),
            "password": "1234"
        }

    def generate_random_users(self, number):
        for _ in range(number):
            yield self.generate_random_user()


headers = {
    'Content-Type': 'application/json',
    'Authorization': ''
}


def register_user(user):
    res = requests.post(
        f"{BASE_URL}/auth/signup",
        headers=headers,
        data=json.dumps({
            "email": user['email'],
            "first_name": user['first_name'],
            "last_name": user['last_name'],
            "password": user['password']
        })
    )
    return res


def register_profile(user, profile_id, token):
    res = requests.put(
        f"{BASE_URL}/profiles/{profile_id}",
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        },
        json={
            'music_styles': user['music_styles'],
            'principal_instrument': user['principal_instrument'],
            'status': user['status']
        }
    )


def login_user(user):
    res = requests.post(
        f"{BASE_URL}/auth/login",
        headers=headers,
        data=json.dumps({
            "email": user['email'],
            "password": user['password']
        })
    )
    headers['Authorization'] = f"Bearer {res.json()['token']}"
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
    done = 0
    err = 0
    print("Cargando Random user generator...", end=" ")
    rug = RandomUsersGenerator()
    print("Listo.")

    print("Registrando usuario principal...")
    res = register_user(my_user)
    my_user['profile_id'] = res.json()['profile_id']
    my_user['token'] = res.json()['token']
    print("Listo.")

    print("Registrando perfil... ", end=" ")
    register_profile(my_user, my_user['profile_id'], my_user['token'])
    print("Listo.")

    print("Registrando usuarios...")
    for user in rug.generate_random_users(200):
        print(f"Registrando {user['first_name']} {user['last_name']} {user['email']}...", end=" ")
        res = register_user(user)
        j = res.json()
        if res.status_code == 200:
            token = j['token']
            p_id = j['profile_id']
            register_profile(user, p_id, token)
            done += 1
            print("Listo.")

        else:
            err += 1
            print(f"Error: {res.status_code} {j['message']}")

    t = int(time.time()-start_time)
    print(f"Time: {t//60} minutes and {t%60} seconds")
    print(f"Se registraron {done} usuarios")
    print(f"{err} usuarios dieron error y no fueron regiastrados")
