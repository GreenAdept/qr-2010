# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Location.polymorphic_ctype'
        db.add_column('games_location', 'polymorphic_ctype', self.gf('django.db.models.fields.related.ForeignKey')(related_name='polymorphic_location_set', null=True, to=orm['contenttypes.ContentType']), keep_default=False)

        # Adding field 'Game.polymorphic_ctype'
        db.add_column('game', 'polymorphic_ctype', self.gf('django.db.models.fields.related.ForeignKey')(related_name='polymorphic_game_set', null=True, to=orm['contenttypes.ContentType']), keep_default=False)

        # Adding field 'Player.polymorphic_ctype'
        db.add_column('games_player', 'polymorphic_ctype', self.gf('django.db.models.fields.related.ForeignKey')(related_name='polymorphic_player_set', null=True, to=orm['contenttypes.ContentType']), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Location.polymorphic_ctype'
        db.delete_column('games_location', 'polymorphic_ctype_id')

        # Deleting field 'Game.polymorphic_ctype'
        db.delete_column('game', 'polymorphic_ctype_id')

        # Deleting field 'Player.polymorphic_ctype'
        db.delete_column('games_player', 'polymorphic_ctype_id')


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
            'center_latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6'}),
            'center_longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
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
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'expires': ('django.db.models.fields.DateTimeField', [], {}),
            'gameID': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['games.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'polymorphic_location_set'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'visible': ('django.db.models.fields.DateTimeField', [], {})
        },
        'games.player': {
            'Meta': {'object_name': 'Player'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['games.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'polymorphic_player_set'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['games']
