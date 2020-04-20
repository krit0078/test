# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils import timezone

class TbCatagory(models.Model):
    prefix = models.CharField(max_length=45)
    title = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'ed_catagory'

class TbMember(models.Model):
    username = models.CharField(max_length=45,db_index=True)
    password = models.CharField(max_length=45)
    fullname = models.CharField(max_length=80)
    description = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=45,db_index=True)
    picture = models.CharField(max_length=512, blank=True, null=True)
    member_type = models.CharField(max_length=10)

    class Meta:
        managed = True
        db_table = 'ed_member'

class TbLog(models.Model):
    ip=models.CharField(max_length=50)
    device=models.CharField(max_length=200,null=True)
    location=models.TextField(null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    tb_member = models.ForeignKey(TbMember, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'ed_log'