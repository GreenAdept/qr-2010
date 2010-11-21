
from django.db import models
from django.contrib.auth.models import User
from django import forms

from qr import local_settings


GAME_TYPES = (
              ('TH', 'Treasure Hunt'),
              ('QU', 'Questline'),
              )
GAME_TEMPLATE_DIR = local_settings.LOCAL_ROOT_DIR + 'game_template_dir/'

# Create your models here.

class Game(models.Model):
    game_type = models.CharField(max_length=2, choices=GAME_TYPES)
    is_public = models.BooleanField()
    city = models.CharField(max_length=45)
    center_latitude = models.DecimalField(max_digits=10, decimal_places=6)
    center_longitude = models.DecimalField(max_digits=10, decimal_places=6)
    created_by = models.ForeignKey(User)
    created = models.DateTimeField()
    template_directory = models.FilePathField(path=GAME_TEMPLATE_DIR, recursive=True, blank=True,)

    class Meta:
        db_table = 'game'
        get_latest_by = "created"

class Location(models.Model):
    QR_code = models.FileField(upload_to='qr_codes')
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    clue = models.TextField(blank=True)
    created = models.DateTimeField()
    visible = models.DateTimeField()
    expires = models.DateTimeField()
    gameID = models.ForeignKey(Game)

class Player(models.Model):
    game = models.ForeignKey(Game)
    user = models.ForeignKey(User)
    visited_locations = models.ManyToManyField(Location)

class PartialGameForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = ('game_type', 'is_public', 'city')
        
        
