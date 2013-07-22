# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Account', fields ['institution', 'account_number']
        db.create_unique(u'finance_account', ['institution_id', 'account_number'])

        # Adding unique constraint on 'Transaction', fields ['account', 'transaction_id']
        db.create_unique(u'finance_transaction', ['account_id', 'transaction_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Transaction', fields ['account', 'transaction_id']
        db.delete_unique(u'finance_transaction', ['account_id', 'transaction_id'])

        # Removing unique constraint on 'Account', fields ['institution', 'account_number']
        db.delete_unique(u'finance_account', ['institution_id', 'account_number'])


    models = {
        u'finance.account': {
            'Meta': {'unique_together': "(('institution', 'account_number'),)", 'object_name': 'Account'},
            'account_number': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'balance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '2'}),
            'broker_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
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
            'Meta': {'unique_together': "(('account', 'transaction_id'),)", 'object_name': 'Transaction'},
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
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        }
    }

    complete_apps = ['finance']
