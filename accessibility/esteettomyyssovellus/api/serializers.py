from django.contrib.auth.models import User, Group
from django.db import models
from . models import *
from rest_framework import serializers
# from . models import Form

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class ArEntranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArEntrance
        fields = '__all__'

    
class ArFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArForm
        fields = '__all__'


class ArXQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArXQuestion
        fields = '__all__'



class ArXQuestionBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArXQuestionBlock
        fields = '__all__'


class ArServicepointSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArServicepoint
        fields = '__all__'
