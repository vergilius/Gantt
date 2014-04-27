# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Task.parent_task'
        db.alter_column(u'domain_task', 'parent_task_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domain.Task'], null=True))

        # Changing field 'Task.developer'
        db.alter_column(u'domain_task', 'developer_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Task.parent_task'
        raise RuntimeError("Cannot reverse this migration. 'Task.parent_task' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Task.parent_task'
        db.alter_column(u'domain_task', 'parent_task_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domain.Task']))

        # User chose to not deal with backwards NULL issues for 'Task.developer'
        raise RuntimeError("Cannot reverse this migration. 'Task.developer' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Task.developer'
        db.alter_column(u'domain_task', 'developer_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'domain.assignment': {
            'Meta': {'unique_together': "(('user', 'team'),)", 'object_name': 'Assignment'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domain.Team']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'domain.project': {
            'Meta': {'object_name': 'Project'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domain.Team']"}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'through': u"orm['domain.ProjectAssignment']", 'symmetrical': 'False'})
        },
        u'domain.projectassignment': {
            'Meta': {'unique_together': "(('user', 'project'),)", 'object_name': 'ProjectAssignment'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domain.Project']"}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'domain.task': {
            'Meta': {'object_name': 'Task'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'developer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'due_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent_task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domain.Task']", 'null': 'True', 'blank': 'True'}),
            'priority': ('django.db.models.fields.IntegerField', [], {}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domain.Project']"}),
            'realization': ('django.db.models.fields.IntegerField', [], {}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'domain.team': {
            'Meta': {'object_name': 'Team'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'through': u"orm['domain.Assignment']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['domain']