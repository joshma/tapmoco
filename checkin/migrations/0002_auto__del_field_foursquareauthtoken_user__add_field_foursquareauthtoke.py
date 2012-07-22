# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'FoursquareAuthToken.user'
        db.delete_column('checkin_foursquareauthtoken', 'user_id')

        # Adding field 'FoursquareAuthToken.username'
        db.add_column('checkin_foursquareauthtoken', 'username',
                      self.gf('django.db.models.fields.CharField')(default='me@joshma.com', max_length=100),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'FoursquareAuthToken.user'
        raise RuntimeError("Cannot reverse this migration. 'FoursquareAuthToken.user' and its values cannot be restored.")
        # Deleting field 'FoursquareAuthToken.username'
        db.delete_column('checkin_foursquareauthtoken', 'username')


    models = {
        'checkin.foursquareauthtoken': {
            'Meta': {'object_name': 'FoursquareAuthToken'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['checkin']