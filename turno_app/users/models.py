from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):

    ASESOR='ASESOR'
    ADMIN='ADMIN'
    CLIENT='CLIENT'
    ROLES = (
        (ASESOR, 'Asesor'),
        (ADMIN, 'Administrador'),
        (CLIENT, 'Cliente')
    )

    # Proxy user atuh    
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    website = models.URLField(max_length = 200,blank=True)
    biography = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20,blank=True)
    picture = models.ImageField(
        upload_to='users/pictures', 
        blank=True,
        null=True
    )
    rol = models.CharField(max_length=100, choices=ROLES, default=CLIENT)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


def __str__(self):
    return self.user.username
