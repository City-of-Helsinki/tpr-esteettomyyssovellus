from django.contrib.auth.models import User, Group
from . models import ArEntrance
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


# class FormSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Form
#         fields = ['form_id']


class ArEntranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArEntrance
        fields = '__all__'