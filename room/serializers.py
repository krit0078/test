from rest_framework import serializers
from room import models

class EdTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EdTask
        fields = ('id','description','timestamp','status')

class EdResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EdResource
        fields = ('id','description','timestamp','status')

class EdLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EdLevel
        fields = ('id','prefix','title')

class EdSubLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EdLevel
        fields = ('id','prefix','title')

class EdCourseSerializer(serializers.ModelSerializer):
    catagory_name = serializers.CharField(source='catagory.title', read_only=True)

    class Meta:
        model = models.EdCourse
        fields = ('id','course_name','description','catagory','catagory_name','cover_pic','uid','timestamp','status')

class EdEnrolmentSerialiezer(serializers.ModelSerializer):
    class Meta:
        model = models.EdEnrolment
        fields = ('id','status')

class EdPathSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.EdPath
        fields = ('id','catagory','task','member','status','timestamp')

class EdSubTaskSerializer(serializers.ModelSerializer):
    teacher_fname=serializers.CharField(source='teacher.firstname',read_only=True)
    teacher_lname=serializers.CharField(source='teacher.lastname',read_only=True)

    class Meta:
        model = models.EdSubTask
        fields = ('id','description','timestamp','status','teacher_fname','teacher_lname')

class EdUserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EdUserType
        fields = ('id','prefix','title')