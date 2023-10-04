import requests
from requests.auth import HTTPBasicAuth
from userAuth import User


class VenueProfile():
    def __init__(self):
        self.user = User()

    def add_team_member(self, email):
        r = requests.patch('http://127.0.0.1:8000/venue_admin/change_team_members/', auth=self.user.get_auth(), json={
            "add_team_member": email
            })
        return r.json()

    def remove_team_member(self, email):
        r = requests.patch('http://127.0.0.1:8000/venue_admin/change_team_members/', auth=self.user.get_auth(), json={
            "remove_team_member": email
        })
        return r.json()


venue = VenueProfile()
print(venue.add_team_member("example@email.de"))
print(venue.remove_team_member("example@email.de"))
