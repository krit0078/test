from django.db import models
from django.utils import timezone


class EdUserType(models.Model):
    prefix=models.CharField(max_length=95,blank=True,null=True)
    title=models.CharField(max_length=95,blank=True,null=True)

    class Meta:
        managed = True
        db_table = 'ed_user_type'

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

class EdMember(models.Model):
    password = models.CharField(max_length=45)
    firstname = models.CharField(max_length=100,blank=True,null=True)
    lastname = models.CharField(max_length=100,blank=True,null=True)
    email = models.CharField(max_length=225,db_index=True)
    picture = models.CharField(max_length=512, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    ed_user_type=models.ForeignKey(EdUserType, models.DO_NOTHING,blank=True,null=True)
    ed_sub_level=models.ForeignKey(EdSubLevel,models.DO_NOTHING,blank=True,null=True)

    class Meta:
        managed = True
        db_table = 'ed_member'

class EdCourse(models.Model):
    course_name = models.CharField(max_length=45)
    teacher = models.ForeignKey(EdMember, models.DO_NOTHING, blank=True, null=True, related_name="teacher")
    description = models.TextField(blank=True, null=True)
    catagory = models.ForeignKey(EdSubLevel, models.DO_NOTHING, blank=True, null=True)
    cover_pic = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=45, blank=True, null=True)
    uid = models.CharField(max_length=45, blank=True, null=True)  # Field name made lowercase.
    student = models.ForeignKey(EdMember, models.DO_NOTHING, blank=True, null=True,related_name="student")

    class Meta:
        managed = True
        db_table = 'ed_course'

class EdEnrolment(models.Model):
    date = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    course = models.ForeignKey(EdCourse, models.DO_NOTHING)
    member = models.ForeignKey(EdMember, models.DO_NOTHING,related_name='member')

    class Meta:
        managed = True
        db_table = 'ed_enrolment'

class EdLog(models.Model):
    ip=models.CharField(max_length=50)
    device=models.CharField(max_length=200,null=True)
    location=models.TextField(null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    ed_member = models.ForeignKey(EdMember, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'ed_log'
