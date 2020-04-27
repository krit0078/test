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
    picture = models.CharField(max_length=512,default='/uploads/0/img/user.png', blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    user_type=models.ForeignKey(EdUserType, models.DO_NOTHING,blank=True,null=True, related_name='user_type')
    catagory=models.ForeignKey(EdSubLevel,models.DO_NOTHING,blank=True,null=True)

    class Meta:
        managed = True
        db_table = 'ed_member'

class EdCourse(models.Model):
    course_name = models.CharField(max_length=45)
    teacher = models.ForeignKey(EdMember, models.DO_NOTHING, blank=True, null=True, related_name="teacher")
    description = models.TextField(blank=True, null=True)
    catagory = models.ForeignKey(EdSubLevel, models.DO_NOTHING, blank=True, null=True, related_name="catagory")
    cover_pic = models.TextField(blank=True, null=True, default='/uploads/0/cover/cover1.png')
    status = models.CharField(max_length=45,default='ACTIVE', blank=True, null=True)
    uid = models.CharField(max_length=45, blank=True, null=True)  # Field name made lowercase.
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'ed_course'

class EdEnrolment(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    course = models.ForeignKey(EdCourse, models.DO_NOTHING)
    member = models.ForeignKey(EdMember, models.DO_NOTHING,related_name='member')

    class Meta:
        managed = True
        db_table = 'ed_enrolment'

class EdPost(models.Model):
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=45,default='ACTIVE', blank=True, null=True)
    member = models.ForeignKey(EdMember, models.DO_NOTHING, blank=True, null=True)
    course = models.ForeignKey(EdCourse, models.DO_NOTHING,blank=True, null=True,related_name="course")

    class Meta:
        managed = True
        db_table = 'ed_post'

class EdPostFile(models.Model):
    file_name=models.CharField(max_length=250)
    file_link=models.TextField(blank=True, null=True)
    file_type=models.TextField(blank=True, null=True)
    status = models.CharField(max_length=45,default='ACTIVE', blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    post=models.ForeignKey(EdPost, models.DO_NOTHING, blank=True, null=True,related_name='post')

    class Meta:
        managed = True
        db_table = 'ed_post_file'

class EdReply(models.Model):
    description = models.TextField(blank=True, null=True)
    member = models.ForeignKey(EdMember, models.DO_NOTHING, blank=True, null=True)
    status = models.CharField(max_length=45,default='ACTIVE', blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    post=models.ForeignKey(EdPost, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ed_reply'

class EdTask(models.Model):
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=45,default='ACTIVE', blank=True, null=True)
    teacher = models.ForeignKey(EdMember, models.DO_NOTHING, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    course = models.ForeignKey(EdCourse, models.DO_NOTHING,blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ed_task'

class EdTaskFile(models.Model):
    file_name=models.CharField(max_length=250)
    file_link=models.TextField(blank=True, null=True)
    file_type=models.TextField(blank=True, null=True)
    status = models.CharField(max_length=45,default='ACTIVE', blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    task=models.ForeignKey(EdTask, models.DO_NOTHING, blank=True, null=True,related_name='task')

    class Meta:
        managed = True
        db_table = 'ed_task_file'

class EdTaskOpengraph(models.Model):
    title = models.CharField(max_length=512, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    url=models.TextField(blank=True, null=True)
    image=models.TextField(blank=True, null=True)
    task=models.ForeignKey(EdTask, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ed_task_opengraph'

class EdTurnedIn(models.Model):
    description = models.TextField(blank=True, null=True)
    score = models.IntegerField(blank=True, default=0)
    status = models.CharField(max_length=45,default='TURNEDIN', blank=True, null=True)
    member = models.ForeignKey(EdMember, models.DO_NOTHING, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    task=models.ForeignKey(EdTask, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ed_turnedin'


class EdLive(models.Model):
    url=models.TextField(blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    platform = models.CharField(max_length=70, blank=True, null=True)
    status = models.CharField(max_length=45,default='ACTIVE', blank=True, null=True)
    teacher = models.ForeignKey(EdMember, models.DO_NOTHING, blank=True, null=True)
    course = models.ForeignKey(EdCourse, models.DO_NOTHING,blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'ed_live'

class EdResource(models.Model):
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=45,default='ACTIVE', blank=True, null=True)
    teacher = models.ForeignKey(EdMember, models.DO_NOTHING, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    task=models.ForeignKey(EdTask, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ed_resource'

class EdResourceFile(models.Model):
    file_name=models.CharField(max_length=250)
    file_link=models.TextField(blank=True, null=True)
    file_type=models.TextField(blank=True, null=True)
    status = models.CharField(max_length=45,default='ACTIVE', blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    resource=models.ForeignKey(EdResource, models.DO_NOTHING, blank=True, null=True,related_name='resource')

    class Meta:
        managed = True
        db_table = 'ed_resource_file'

class EdResourceOpengraph(models.Model):
    title = models.CharField(max_length=512, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    url=models.TextField(blank=True, null=True)
    image=models.TextField(blank=True, null=True)
    resource=models.ForeignKey(EdResource, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ed_resource_opengraph'

class EdSocial(models.Model):
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=45,default='ACTIVE', blank=True, null=True)
    teacher = models.ForeignKey(EdMember, models.DO_NOTHING, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    task=models.ForeignKey(EdTask, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ed_social'

class EdSocialFile(models.Model):
    file_name=models.CharField(max_length=250)
    file_link=models.TextField(blank=True, null=True)
    file_type=models.TextField(blank=True, null=True)
    status = models.CharField(max_length=45,default='ACTIVE', blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    social=models.ForeignKey(EdSocial, models.DO_NOTHING, blank=True, null=True,related_name='social')

    class Meta:
        managed = True
        db_table = 'ed_social_file'

class EdSocialOpengraph(models.Model):
    title = models.CharField(max_length=512, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    url=models.TextField(blank=True, null=True)
    image=models.TextField(blank=True, null=True)
    social=models.ForeignKey(EdSocial, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ed_social_opengraph'

class EdLog(models.Model):
    ip=models.CharField(max_length=50)
    device=models.CharField(max_length=200,null=True)
    location=models.TextField(null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    ed_member = models.ForeignKey(EdMember, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'ed_log'
