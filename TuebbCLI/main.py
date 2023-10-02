import requests
from requests.auth import HTTPBasicAuth
from userAuth import User


run_loop = True

user = User()
print(f"Already signed in: {user.signedin}")

command_list = ["login"]

# Sign up and sign in process
while not user.signedin:
    l_s = input("Login(1) or Sign up(2)?")
    if l_s == "1":
        email = input("email:").strip()
        password = input("password:").strip()
        log = user.login(email, password)
        print(f"Login successful: {log}")

    elif l_s == "2":
        email = input("email:").strip()
        password = input("password:").strip()
        password2 = input("repeat the password:").strip()
        first_name = input("First name:").strip()
        last_name = input("Last name:").strip()
        obj = {
            "email":email,
            "password":password,
            "password2": password2,
            "first_name": first_name,
            "last_name": last_name
        }
        signup_p = user.sign_up(obj)
        print(f"Sign up successful: {signup_p}")
