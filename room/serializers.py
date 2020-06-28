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