# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Institution'
        db.create_table(u'finance_institution', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fid', self.gf('django.db.models.fields.IntegerField')()),
            ('org', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'finance', ['Institution'])

        # Adding unique constraint on 'Institution', fields ['fid', 'username']
        db.create_unique(u'finance_institution', ['fid', 'username'])

        # Adding model 'Account'
        db.create_table(u'finance_account', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('institution', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['finance.Institution'])),
            ('account_number', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('routing_number', self.gf('django.db.models.fields.CharField')(max_length=9, blank=True)),
            ('balance', self.gf('django.db.models.fields.DecimalField')(max_digits=15, decimal_places=2)),
            ('broker_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'finance', ['Account'])

        # Adding model 'Transaction'
        db.create_table(u'finance_transaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['finance.Account'])),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=15, decimal_places=2)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('mcc', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('memo', self.gf('django.db.models.fields.TextField')()),
            ('payee', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('sic', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('transaction_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'finance', ['Transaction'])


    def backwards(self, orm):
        # Removing unique constraint on 'Institution', fields ['fid', 'username']
        db.delete_unique(u'finance_institution', ['fid', 'username'])

        # Deleting model 'Institution'
        db.delete_table(u'finance_institution')

        # Deleting model 'Account'
        db.delete_table(u'finance_account')

        # Deleting model 'Transaction'
        db.delete_table(u'finance_transaction')


    models = {
        u'finance.account': {
            'Meta': {'object_name': 'Account'},
            'account_number': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'balance': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '2'}),
            'broker_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['finance.Institution']"}),
            'routing_number': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'})
        },
        u'finance.institution': {
            'Meta': {'unique_together': "(('fid', 'username'),)", 'object_name': 'Institution'},
            'fid': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'org': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'finance.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['finance.Account']"}),
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '2'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mcc': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'memo': ('django.db.models.fields.TextField', [], {}),
            'payee': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sic': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'transaction_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['finance']