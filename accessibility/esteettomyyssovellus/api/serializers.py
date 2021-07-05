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


class ArSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArSystem
        fields = '__all__'


class ArSystemFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArSystemForm
        fields = '__all__'


class ArXQuestionAnswerPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArXQuestionAnswerPhoto
        fields = '__all__'


class ArFormLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArFormLanguage
        fields = '__all__'

# class ArBackendCopyableEntranceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ArBackendCopyableEntrance
#         fields = '__all__'


class ArXQuestionLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArXQuestionLanguage
        fields = '__all__'


# class ArXStoredSentenceLangSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ArXStoredSentenceLang
#         fields = '__all__'


class ArBackendQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArBackendQuestion
        fields = '__all__'


class ArBackendQuestionBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArBackendQuestionBlock
        fields = '__all__'


class ArBackendQuestionChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArBackendQuestionChoice
        fields = '__all__'
