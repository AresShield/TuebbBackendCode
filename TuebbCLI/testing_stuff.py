import requests
from requests.auth import HTTPBasicAuth
from userAuth import User


user = User()

email = "example@email.de"
password = "Password123!?"
password2 = "Password123!?"
first_name = "Andrew"
last_name = "Carnegie"

obj = {
    "email":email,
    "password":password,
    "password2": password2,
    "first_name": first_name,
    "last_name": last_name
}
user.sign_up(obj)
