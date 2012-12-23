# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Location'
        db.create_table('location_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('place_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('contact_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('address', self.gf('django.db.models.fields.TextField')()),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('fax_number', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('additional_info', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('location', ['Location'])

        # Adding M2M table for field activities on 'Location'
        db.create_table('location_location_activities', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('location', models.ForeignKey(orm['location.location'], null=False)),
            ('activity', models.ForeignKey(orm['location.activity'], null=False))
        ))
        db.create_unique('location_location_activities', ['location_id', 'activity_id'])

        # Adding model 'Activity'
        db.create_table('location_activity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200, db_index=True)),
        ))
        db.send_create_signal('location', ['Activity'])


    def backwards(self, orm):
        # Deleting model 'Location'
        db.delete_table('location_location')

        # Removing M2M table for field activities on 'Location'
        db.delete_table('location_location_activities')

        # Deleting model 'Activity'
        db.delete_table('location_activity')


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
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
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