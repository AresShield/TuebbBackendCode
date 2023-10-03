import requests
from requests.auth import HTTPBasicAuth
from userAuth import User
from PIL import Image as ImageFile
from tkinter.filedialog import askopenfilename
import tempfile

class AdvancedVenueProfile():
    def __init__(self):
        self.user = User()

    def get_profile(self):
        r = requests.get('http://127.0.0.1:8000/venue_admin/adv_profile/', auth=self.user.get_auth())
        return r.json()

    def change_profile(self, address=None, opening_hours=None, description=None,
                       contact=None, entry_fee=None):

        data = self.get_profile()
        if address: data["address"] = address
        if opening_hours: data["opening_hours"] = opening_hours
        if description: data["description"] = description
        if contact: data["contact"] = contact
        if entry_fee: data["entry_fee"] = entry_fee
        r = requests.put('http://127.0.0.1:8000/venue_admin/adv_profile/', data, auth=self.user.get_auth())


    def add_picture(self):

        data = self.get_profile()

        image = ImageFile.open(askopenfilename())
        image_file = tempfile.NamedTemporaryFile(suffix='.png')
        image.save(image_file, 'png')

        with open(image_file.name, 'rb') as image:
            files = {
                "upload_image": image
            }
            r = requests.put('http://127.0.0.1:8000/venue_admin/adv_profile/', data, auth=self.user.get_auth(), files=files)
            print(r.json())

    def delete_picture(self, ids):
        data = self.get_profile()

        data["delete_photos"] = ids

        r = requests.put('http://127.0.0.1:8000/venue_admin/adv_profile/', data, auth=self.user.get_auth())


adv_profile = AdvancedVenueProfile()
#print(adv_profile.get_profile())
"""adv_profile.change_profile(address="Another Adress!")
adv_profile.get_profile()"""
#adv_profile.add_picture()
#adv_profile.get_profile()
adv_profile.delete_picture([3,])
print(adv_profile.get_profile())
