# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django_countries.fields import Country


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Location.country'
        db.add_column('location_location', 'country',
                      self.gf('django_countries.fields.CountryField')(default=Country(code=u'TH'), max_length=2),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Location.country'
        db.delete_column('location_location', 'country')


    models = {
        'location.activity': {
            'Meta': {'object_name': 'Activity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'})
        },
        'location.location': {
            'Meta': {'object_name': 'Location'},
            'activities': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'locations'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['location.Activity']"}),
            'additional_info': ('django.db.models.fields.TextField', [], {}),
            'address': ('django.db.models.fields.TextField', [], {}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'country': ('django_countries.fields.CountryField', [], {'default': "Country(code=u'TH')", 'max_length': '2'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'fax_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'place_name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['location']