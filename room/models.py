# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils import timezone

class EdUserType(models.Model):
    prefix=models.CharField(max_length=95,blank=True,null=True)
    title=models.CharField(max_length=95,blank=True,null=True)

    class Meta:
        managed = True
        db_table = 'ed_user_type'

class EdMember(models.Model):
    password = models.CharField(max_length=45)
    firstname = models.CharField(max_length=100,blank=True,null=True)
    lastname = models.CharField(max_length=100,blank=True,null=True)
    email = models.CharField(max_length=225,db_index=True)
    picture = models.CharField(max_length=512, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    ed_user_type=models.ForeignKey(EdUserType, models.DO_NOTHING,blank=True,null=True)

    class Meta:
        managed = True
        db_table = 'ed_member'

class EdLog(models.Model):
    ip=models.CharField(max_length=50)
    device=models.CharField(max_length=200,null=True)
    location=models.TextField(null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    ed_member = models.ForeignKey(EdMember, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'ed_log'

class EdLevel(models.Model):
    prefix=models.CharField(max_length=95,blank=True,null=True)
    title=models.CharField(max_length=95,blank=True,null=True)

    class Meta:
        managed = True
        db_table = 'ed_level'

class EdSubLevel(models.Model):
    prefix=models.CharField(max_length=95,blank=True,null=True)
    title=models.CharField(max_length=95,blank=True,null=True)
    ed_level=models.ForeignKey(EdLevel, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'ed_sub_level'