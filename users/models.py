from django.db import models
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_img = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
    display_name = models.CharField(max_length=50)
    info = models.TextField()

    def __str__(self):
        return self.user.username