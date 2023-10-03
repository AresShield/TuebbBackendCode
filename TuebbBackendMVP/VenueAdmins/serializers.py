from rest_framework import serializers
from .models import Menu, MenuItem, AdvancedVenueProfile, Photo
from userAuth.models import VenueProfile


# serializer for menu items
class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ["id", "name", "description", "price"]

    def create(self, validated_data):
        item = MenuItem.objects.create(**validated_data)
        profile = VenueProfile.objects.get(govern_user=self.context['request'].user)
        menu = Menu.objects.get(owner=profile)
        menu.items.add(item)
        menu.save()
        return item


# serializer for menu as a whole
class MenuSerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = ["id", "items"]

    def validate(self, attrs):

        instance = self.instance
        if self.context["request"].data.get("delete_menu_items"):

            for it in self.context["request"].data.get("delete_menu_items"):
                if MenuItem.objects.get(pk=int(it)) not in instance.items.all():
                    raise serializers.ValidationError({"delete_menu_items": "No permission to do this!"})

            return attrs
        raise serializers.ValidationError({"delete_menu_items": "No valid arguments!"})

    def update(self, instance, validated_data):
        if self.context["request"].data.get("delete_menu_items"):
            for item in self.context["request"].data.get("delete_menu_items"):
                item_obj = MenuItem.objects.get(id=item)
                instance.items.remove(item_obj)
                item_obj.delete()
        return instance


# serializer for images
class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ["file"]

# serializer for full venue profiles
# note: only one image can be uploaded at a time
class AdvancedProfileVenueSerializer(serializers.ModelSerializer):
    images = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = AdvancedVenueProfile
        fields = ["address", "opening_hours", "description", "contact", "images", "entry_fee"]

    def validate(self, attrs):
        if self.context["request"].data.get("delete_photos"):
            instance = self.instance
            for photo in self.context["request"].data.get("delete_photos"):
                if Photo.objects.get(pk=int(photo)) not in instance.images.all():
                    raise serializers.ValidationError({"delete_photos": "No permission to do this!"})
        """ if self.context["request"].data.get("upload_images"):
             for file in self.context["request"].data.get("upload_images"):
                 print(file)
                 #if file.split(".")[-1] not in ["jpg", "png", "jpeg", "JPG", "PNG", "JPEG"]:
                     #raise serializers.ValidationError({"Uploaded photos": "File type not supported!"})
         """
        return attrs


    def update(self, instance, validated_data):
        if self.context["request"].data.get("delete_photos"):
            for photo in self.context["request"].data.get("delete_photos"):
                photo_obj = Photo.objects.get(pk=photo)
                instance.images.remove(photo_obj)
                photo_obj.delete()

        if self.context["request"].data.get("upload_image"):
            photo = Photo.objects.create(file=self.context["request"].data.get("upload_image"))
            instance.images.add(photo)

        instance.address=validated_data.get("address")
        instance.opening_hours=validated_data.get("opening_hours")
        instance.description=validated_data.get("description")
        instance.contact=validated_data.get("contact")
        instance.entry_fee=validated_data.get("entry_fee")

        instance.save()
        return instance
