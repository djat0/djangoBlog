from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from PIL import Image


def get_avatar_filepath(self, filename):
    return f"avatars/{self.user.username}-{str(self.user.pk)}/avatar.png"


def get_default_avatar():
    return "avatars/default/default-user.png"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to=get_avatar_filepath,
        null=True,
        blank=True,
        default=get_default_avatar,
    )

    def __str__(self):
        return self.user.username

    @property
    def get_fullname(self):
        return f"{self.user.last_name} {self.user.first_name}"

    def save(self):
        super().save()
        img = Image.open(self.avatar.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)
