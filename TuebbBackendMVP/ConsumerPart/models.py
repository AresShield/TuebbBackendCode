from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class ConsumerUser(models.Model):

    GENDER = [
        ("F", "Female"),
        ("M", "Male"),
        ("N", "Non-binary"),
        ("O", "Other")
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="consumer_account")
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER, blank=True, null=True)


    def __str__(self):
        return f"Consumer account of {self.user.email}"
