import requests
from requests.auth import HTTPBasicAuth


# handle user auth and more
class User:
    def __init__(self):
        self.signedin = False
        self.email = None
        self.password = None
        with open("TuebbCLI/auth.txt", "r") as f:
            data = f.readlines()
            if len(data)>1:
                self.email = data[0].strip()
                self.password = data[1].strip()
                self.signedin = True

    def save_to_file(self):
        with open("TuebbCLI/auth.txt", "w+") as f:
            f.write(self.email + "\n")
            f.write(self.password + "\n")
        return True

    def sign_in(self, email, password):
        r = requests.post('http://127.0.0.1:8000/auth/login/', auth=HTTPBasicAuth(email, password))
        # print(r.json()["Status"])
        if r.json().get("Status"):
            if r.json()["Status"] == "Valid User!":
                self.email = email
                self.password = password
                return True
        return False

    def get_auth(self):
        return HTTPBasicAuth(self.email, self.password)

    def login(self, email, password):
        signin = self.sign_in(email, password)
        if signin:
            if self.save_to_file():
                self.signedin = True
                return True
        return False

    def sign_up(self, obj):
        r = requests.post('http://127.0.0.1:8000/auth/register/', json=obj)
        if r.status_code==201:
            self.email = obj["email"]
            self.password = obj["password"]
            self.save_to_file()
            self.signedin = True
            return True
        return False
