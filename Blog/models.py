from django.db import models
import uuid
from django.contrib.auth.models import User


def get_thumbnail_filepath(self, filename):
    return f"post-thumbnail/{self.id}/thumbnail.png"


def get_default_thumbnail():
    return "post-thumbnail/default/default-thumbnail.png"


def get_post_image_filepath(self, filename):
    return f"post-image/{self.post.id}/{self.order}.png"


class Post(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    title = models.CharField(max_length=100, null=False, blank=False)
    headline = models.TextField(null=False, blank=False)
    thumbnail = models.ImageField(
        upload_to=get_thumbnail_filepath,
        null=True,
        blank=True,
        default=get_default_thumbnail,
    )
    datetime_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.title, self.datetime_posted)

    @property
    def thumbnail_url(self):
        try:
            image = self.thumbnail.url
        except:
            image = None
        return image


class PostImage(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(
        null=True, blank=True, upload_to=get_post_image_filepath)
    order = models.IntegerField()

    @property
    def image_url(self):
        try:
            image = self.image.url
        except:
            image = ""
        return image


class PostParagraph(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    paragraph = models.TextField(null=False, blank=True)
    order = models.IntegerField()


class Comment(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500, null=False, blank=False)
    datetime_posted = models.DateTimeField(auto_now_add=True)


class Reply(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.TextField(max_length=500, null=False, blank=False)
    datetime_replied = models.DateTimeField(auto_now_add=True)
