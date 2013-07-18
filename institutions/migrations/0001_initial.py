# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Institution'
        db.create_table(u'institutions_institution', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fid', self.gf('django.db.models.fields.IntegerField')()),
            ('org', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'institutions', ['Institution'])

        # Adding unique constraint on 'Institution', fields ['fid', 'username']
        db.create_unique(u'institutions_institution', ['fid', 'username'])


    def backwards(self, orm):
        # Removing unique constraint on 'Institution', fields ['fid', 'username']
        db.delete_unique(u'institutions_institution', ['fid', 'username'])

        # Deleting model 'Institution'
        db.delete_table(u'institutions_institution')


    models = {
        u'institutions.institution': {
            'Meta': {'unique_together': "(('fid', 'username'),)", 'object_name': 'Institution'},
            'fid': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'org': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['institutions']