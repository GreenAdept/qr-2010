# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

import uuid
from qr.games.models import Location
from MySQLdb import OperationalError

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Location.uuid'
        db.add_column('games_location', 'uuid', self.gf('qr.thirdparty.uuidfield.fields.UUIDField')(default='ff', max_length=32, unique=False, blank=True), keep_default=False)
        
        # hacks added by Doug to assign a UUID to existing locations
        # (note that the line above was also changed from unique=True to unique=False)
        try:
            locs = Location.objects.all()
            for loc in locs:
                loc.uuid = uuid.uuid4().hex
                loc.save()
        except OperationalError:
            # this will occur during South's dry run of this migration;
            # that's fine, we only need to change the UUID's when we actually
            # apply the migration
            pass
        db.create_index('games_location', ['uuid'], unique=True)


    def backwards(self, orm):
        
        # Deleting field 'Location.uuid'
        db.delete_column('games_location', 'uuid')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'games.game': {
            'Meta': {'object_name': 'Game', 'db_table': "'game'"},
            'center_latitude': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '6'}),
            'center_longitude': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '6'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '45'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': "'2010-01-01'"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'game_type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'polymorphic_game_set'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'template_directory': ('django.db.models.fields.FilePathField', [], {'path': "'c:/documents and settings/doug/bitnami djangostack projects/game_template_dir/'", 'max_length': '100', 'recursive': 'True', 'blank': 'True'})
        },
        'games.location': {
            'Meta': {'object_name': 'Location'},
            'QR_code': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'clue': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': "'2010-01-01'"}),
            'expires': ('django.db.models.fields.DateTimeField', [], {'default': "'2010-01-01'"}),
            'gameID': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['games.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '6'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '6'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'polymorphic_location_set'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'uuid': ('qr.thirdparty.uuidfield.fields.UUIDField', [], {'max_length': '32', 'unique': 'True', 'blank': 'True'}),
            'visible': ('django.db.models.fields.DateTimeField', [], {'default': "'2010-01-01'"})
        },
        'games.player': {
            'Meta': {'object_name': 'Player'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['games.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'polymorphic_player_set'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'games.treasurehuntgame': {
            'Meta': {'object_name': 'TreasureHuntGame', '_ormbases': ['games.Game']},
            'game_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['games.Game']", 'unique': 'True', 'primary_key': 'True'}),
            'ordered_locations': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '200'})
        },
        'games.treasurehuntplayer': {
            'Meta': {'object_name': 'TreasureHuntPlayer', '_ormbases': ['games.Player']},
            'highest_visited': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'hunt_player'", 'null': 'True', 'to': "orm['games.Location']"}),
            'player_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['games.Player']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['games']
