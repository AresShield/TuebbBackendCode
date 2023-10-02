import requests
from requests.auth import HTTPBasicAuth
from userAuth import User


class Menu():
    def __init__(self):
        self.user = User()

    def get_menu_(self):
        r = requests.get('http://127.0.0.1:8000/venue_admin/menu/', auth=self.user.get_auth())
        """if r.json().get("Status"):
            if r.json()["Status"] == "Valid User!":
                self.email = email
                self.password = password
                return True
        return False"""
        print("Current menu:")
        for item in r.json()["items"]:
            print(item)

    def add_item(self, name, description, price):
        obj = {
            "name":name,
            "description":description,
            "price":price
        }
        r = requests.post('http://127.0.0.1:8000/venue_admin/menu_item/', auth=self.user.get_auth(), json=obj)
        #print(r.json())

    def change_item(self, name, description, price, id):
        obj = {
            "name": name,
            "description": description,
            "price": price
        }
        r = requests.put(f'http://127.0.0.1:8000/venue_admin/menu_item/{id}/', auth=self.user.get_auth(), json=obj)
        #print(r.json())

    def delete_item(self, ids):
        obj = {
            "delete_menu_items": ids
        }
        r = requests.patch('http://127.0.0.1:8000/venue_admin/menu/', auth=self.user.get_auth(), json=obj)
        #print(r.json())


menu = Menu()
"""menu.add_item(name="ExampleDrink", description="That one is really good!", price=12.23)
menu.get_menu_()
menu.change_item(name="ExampleDrink", description="That one is really good!", price=15.23, id=1)
menu.get_menu_()"""
menu.get_menu_()
menu.delete_item(ids=[1,2])
menu.get_menu_()
