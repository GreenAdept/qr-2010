
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, IntegrityError
from django.contrib.auth.models import User
from django import forms


from polymorphic import PolymorphicModel

from qr import local_settings
from qr.games import utils
from qr.thirdparty.uuidfield import UUIDField

GAME_TYPES = (
              ('TH', 'Treasure Hunt'),
              ('QU', 'Questline'),
              )
GAME_TEMPLATE_DIR = local_settings.LOCAL_ROOT_DIR + 'game_template_dir/'

class Game(PolymorphicModel):
    game_type = models.CharField(max_length=2, choices=GAME_TYPES)
    is_public = models.BooleanField(default='')
    city = models.CharField(max_length=45, default='')
    center_latitude = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    center_longitude = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    created_by = models.ForeignKey(User)
    created = models.DateTimeField(default='2010-01-01')
    template_directory = models.FilePathField(path=GAME_TEMPLATE_DIR, recursive=True, blank=True,)
    
    class Meta:
        db_table = 'game'
        get_latest_by = "created"
    
class Location(PolymorphicModel):
    QR_code = models.FileField(upload_to='qr_codes')
    latitude = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    clue = models.TextField(blank=True)
    created = models.DateTimeField(default='2010-01-01')
    visible = models.DateTimeField(default='2010-01-01')
    expires = models.DateTimeField(default='2010-01-01')
    gameID = models.ForeignKey(Game)
    uuid = UUIDField(auto=True)

class Player(PolymorphicModel):
    game = models.ForeignKey(Game)
    user = models.ForeignKey(User)

class PartialGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('game_type', 'is_public', 'city')

class TreasureHuntGame(Game):
    ordered_locations = models.CommaSeparatedIntegerField(max_length=200)
    
    def save(self, *args, **kwargs):
        # game_type is always TH
        if self.game_type == '':
            self.game_type = GAME_TYPES[0][0]
        elif self.game_type != GAME_TYPES[0][0]:
            raise IntegrityError('TH game_type must always be TH')
        super(TreasureHuntGame, self).save(*args, **kwargs)

class TreasureHuntPlayer(Player):
    highest_visited = models.ForeignKey(Location, related_name='hunt_player', null=True)
    
    def save(self, *args, **kwargs):
        if self.highest_visited is not None:
            # make sure the highest_visited field refers to a location
            # that is part of the correct game
            try:
                self.game.location_set.get(pk=self.highest_visited.id)
            except ObjectDoesNotExist:
                raise IntegrityError('highest_visited must be a Location of the correct Game')
        super(TreasureHuntPlayer, self).save(*args, **kwargs)

def location_save(sender, **kwargs):
    ''' Called after a location gets saved.
        Check if the location is for a TreasureHuntGame,
        and if so then make sure the game's ordered_locations
        includes the location.
    '''
    # only need to update when a new location is added
    # (assuming locations are never moved to a new game
    # after they are created)
    if kwargs['created']:
        loc = kwargs['instance']
        game = loc.gameID
        if isinstance(game, TreasureHuntGame):
            game_locs = utils.csv_to_list(game.ordered_locations)
            if loc.id not in game_locs:
                game.ordered_locations += str(loc.id) + ','
                game.save()

from django.db.models.signals import post_save
post_save.connect(location_save, sender=Location)



class UserProfile(models.Model):
    user = models.OneToOneField(User)
    firstname = models.CharField(max_length=50, blank=True)
    lastname = models.CharField(max_length=50, blank=True)
    photo = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True)
    birthday = models.DateField(blank=True, null=True) 
    bio = models.TextField(blank=True)
 
 
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
