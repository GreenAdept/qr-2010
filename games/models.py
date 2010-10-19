from django.db import models
from django.contrib.auth.models import User
from qr import local_settings

import datetime

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
    created_by = models.OneToOneField(User)
    created = models.DateTimeField()
    template_directory = models.FilePathField(path=GAME_TEMPLATE_DIR, recursive=True, blank=True,)
    
    class Meta:
        db_table = 'game'
        get_latest_by = "created"

class Location(models.Model):
    QR_code = models.FileField(upload_to='qr_codes')
    location = models.CharField(max_length=45)
    clue = models.TextField(blank=True)
    created = models.DateTimeField()
    visible = models.DateTimeField()
    expires = models.DateTimeField()
    gameID = models.ForeignKey('Game')
