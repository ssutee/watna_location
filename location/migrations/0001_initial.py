# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Picture'
        db.create_table('location_picture', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(max_length=500, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, blank=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='pictures', null=True, to=orm['location.Location'])),
        ))
        db.send_create_signal('location', ['Picture'])

        # Adding model 'Skill'
        db.create_table('location_skill', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200, db_index=True)),
        ))
        db.send_create_signal('location', ['Skill'])

        # Adding model 'Profile'
        db.create_table('location_profile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('map_type', self.gf('django.db.models.fields.CharField')(default='ROADMAP', max_length=10)),
            ('sorting', self.gf('django.db.models.fields.CharField')(default='entry', max_length=10)),
            ('display', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('other_skills', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('location', ['Profile'])

        # Adding M2M table for field skills on 'Profile'
        db.create_table('location_profile_skills', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('profile', models.ForeignKey(orm['location.profile'], null=False)),
            ('skill', models.ForeignKey(orm['location.skill'], null=False))
        ))
        db.create_unique('location_profile_skills', ['profile_id', 'skill_id'])

        # Adding model 'Status'
        db.create_table('location_status', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200, db_index=True)),
        ))
        db.send_create_signal('location', ['Status'])

        # Adding model 'Location'
        db.create_table('location_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('place_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('organization', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('relation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['location.Relation'], null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(related_name='locations', null=True, to=orm['location.Status'])),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('address', self.gf('django.db.models.fields.TextField')()),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('country', self.gf('django_countries.fields.CountryField')(default='TH', max_length=2)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('additional_info', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hide_email', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hide_phone_number', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hide_address', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('location', ['Location'])

        # Adding M2M table for field activities on 'Location'
        db.create_table('location_location_activities', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('location', models.ForeignKey(orm['location.location'], null=False)),
            ('activity', models.ForeignKey(orm['location.activity'], null=False))
        ))
        db.create_unique('location_location_activities', ['location_id', 'activity_id'])

        # Adding model 'Relation'
        db.create_table('location_relation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200, db_index=True)),
        ))
        db.send_create_signal('location', ['Relation'])

        # Adding model 'Activity'
        db.create_table('location_activity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200, db_index=True)),
            ('priority', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('color', self.gf('location.models.ColorModelField')(default='#FF776B', max_length=7)),
        ))
        db.send_create_signal('location', ['Activity'])


    def backwards(self, orm):
        # Deleting model 'Picture'
        db.delete_table('location_picture')

        # Deleting model 'Skill'
        db.delete_table('location_skill')

        # Deleting model 'Profile'
        db.delete_table('location_profile')

        # Removing M2M table for field skills on 'Profile'
        db.delete_table('location_profile_skills')

        # Deleting model 'Status'
        db.delete_table('location_status')

        # Deleting model 'Location'
        db.delete_table('location_location')

        # Removing M2M table for field activities on 'Location'
        db.delete_table('location_location_activities')

        # Deleting model 'Relation'
        db.delete_table('location_relation')

        # Deleting model 'Activity'
        db.delete_table('location_activity')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'location.activity': {
            'Meta': {'object_name': 'Activity'},
            'color': ('location.models.ColorModelField', [], {'default': "'#FF776B'", 'max_length': '7'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'location.location': {
            'Meta': {'object_name': 'Location'},
            'activities': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'locations'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['location.Activity']"}),
            'additional_info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.TextField', [], {}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'country': ('django_countries.fields.CountryField', [], {'default': "'TH'", 'max_length': '2'}),
            'hide_address': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hide_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hide_phone_number': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'organization': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'place_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'relation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['location.Relation']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'locations'", 'null': 'True', 'to': "orm['location.Status']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        },
        'location.picture': {
            'Meta': {'object_name': 'Picture'},
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pictures'", 'null': 'True', 'to': "orm['location.Location']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        'location.profile': {
            'Meta': {'object_name': 'Profile'},
            'display': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map_type': ('django.db.models.fields.CharField', [], {'default': "'ROADMAP'", 'max_length': '10'}),
            'other_skills': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'profiles'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['location.Skill']"}),
            'sorting': ('django.db.models.fields.CharField', [], {'default': "'entry'", 'max_length': '10'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'location.relation': {
            'Meta': {'object_name': 'Relation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'})
        },
        'location.skill': {
            'Meta': {'object_name': 'Skill'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'})
        },
        'location.status': {
            'Meta': {'object_name': 'Status'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'})
        }
    }

    complete_apps = ['location']