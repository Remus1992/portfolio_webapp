from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


def user_image_uh(instance, filename):
    return "users/{}/profile_image/{}".format(instance.username, filename)


class User(AbstractUser):
    phone_number = models.CharField(max_length=50)
    profile_bio = models.TextField(max_length=300, blank=True, null=True)
    image = models.ImageField(upload_to=user_image_uh, blank=True, null=True)


class Album(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="photo_albums")
    title = models.CharField(max_length=50, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    album_details = models.TextField()
    alt_text = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            number = 0
            slug_title = slugify(self.title)
            checking = True
            while checking:
                results = Album.objects.filter(slug=slug_title)
                if results.exists():
                    slug_title = slugify(self.title) + '_' + str(number + 1)
                    number += 1
                else:
                    checking = False
                self.slug = slug_title
        super().save(args, kwargs)


def photo_image_uh(instance, filename):
    return 'photography/{}/{}'.format(instance.album, filename)


class Photo(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="photos")
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="photo_album")
    title = models.CharField(max_length=50, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    image = models.ImageField(upload_to=photo_image_uh, blank=True, null=True)
    alt_text = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    image_details = models.TextField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            number = 0
            slug_title = slugify(self.title)
            checking = True
            while checking:
                results = Photo.objects.filter(slug=slug_title)
                if results.exists():
                    slug_title = slugify(self.title) + '_' + str(number + 1)
                    number += 1
                else:
                    checking = False
                self.slug = slug_title
        super().save(args, kwargs)


class Website(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="websites")
    title = models.CharField(max_length=50, blank=True, null=True)
    link = models.CharField(max_length=50, blank=True, null=True)
    website_details = models.TextField()
    slug = models.SlugField(blank=True, null=True, unique=True)
    alt_text = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    youtube = models.CharField(max_length=255, blank=True, null=True)
    image_details = models.TextField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            number = 0
            slug_title = slugify(self.title)
            checking = True
            while checking:
                results = Website.objects.filter(slug=slug_title)
                if results.exists():
                    slug_title = slugify(self.title) + '_' + str(number + 1)
                    number += 1
                else:
                    checking = False
                self.slug = slug_title
        super().save(args, kwargs)

