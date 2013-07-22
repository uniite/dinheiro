# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Account.name'
        db.add_column(u'finance_account', 'name',
                      self.gf('django.db.models.fields.CharField')(default='Unknown', max_length=50),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Account.name'
        db.delete_column(u'finance_account', 'name')


    models = {
        u'finance.account': {
            'Meta': {'unique_together': "(('institution', 'account_number'),)", 'object_name': 'Account'},
            'account_number': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'balance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '2'}),
            'broker_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['finance.Institution']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'routing_number': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'})
        },
        u'finance.institution': {
            'Meta': {'unique_together': "(('fid', 'username'),)", 'object_name': 'Institution'},
            'fid': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '255'}),
            'org': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'finance.transaction': {
            'Meta': {'ordering': "['-date']", 'unique_together': "(('account', 'transaction_id'),)", 'object_name': 'Transaction'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['finance.Account']"}),
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '2'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mcc': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'memo': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'payee': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sic': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'transaction_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        }
    }

    complete_apps = ['finance']
