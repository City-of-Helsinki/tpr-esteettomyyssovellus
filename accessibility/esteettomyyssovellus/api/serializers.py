from django.contrib.auth.models import User, Group
from django.db.models import fields
from .models import *
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class ArEntranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArEntrance
        fields = [
            "entrance_id",
            "created",
            "created_by",
            "modified",
            "modified_by",
            "is_main_entrance",
            "servicepoint",
            "form",
        ]


class ArFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArForm
        fields = "__all__"


class ArXQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArXQuestion
        fields = "__all__"


class ArXQuestionBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArXQuestionBlock
        fields = "__all__"


class ArServicepointSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArServicepoint
        fields = [
            "servicepoint_id",
            "business_id",
            "organisation_code",
            "system_id_old",
            "servicepoint_name",
            "ext_servicepoint_id",
            "created",
            "created_by",
            "modified",
            "modified_by",
            "address_street_name",
            "address_no",
            "address_city",
            "is_searchable",
            "organisation_id",
            "system",
            "loc_easting",
            "loc_northing",
            "location_id",
        ]


class ArSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArSystem
        fields = "__all__"


class ArSystemFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArSystemForm
        fields = "__all__"


# class ArXQuestionAnswerPhotoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ArXQuestionAnswerPhoto
#         fields = "__all__"


class ArFormLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArFormLanguage
        fields = "__all__"


# class ArBackendCopyableEntranceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ArBackendCopyableEntrance
#         fields = '__all__'


class ArXQuestionLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArXQuestionLanguage
        fields = "__all__"


# class ArXStoredSentenceLangSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ArXStoredSentenceLang
#         fields = '__all__'


class ArBackendQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArBackendQuestion
        fields = "__all__"


class ArBackendQuestionBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArBackendQuestionBlock
        fields = "__all__"


class ArBackendQuestionChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArBackendQuestionChoice
        fields = "__all__"


class ArBackendEntranceAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArBackendEntranceAnswer
        fields = "__all__"


# class ArXQuestionAnswerCommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ArXQuestionAnswerComment
#         fields = "__all__"


# class ArXQuestionAnswerLocationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ArXQuestionAnswerLocation
#         fields = "__all__"


# class ArXQuestionAnswerPhotoTxtSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ArXQuestionAnswerPhotoTxt
#         fields = "__all__"


class ArXAnswerLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArXAnswerLog
        fields = "__all__"


class ArXQuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArXQuestionAnswer
        fields = "__all__"


class ArExternalServicepointSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArExternalServicepoint
        fields = "__all__"


class ArBackendEntranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArBackendEntrance
        fields = "__all__"


class ArBackendServicepointSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArBackendServicepoint
        fields = "__all__"


class ArBackendExternalServicepointSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArBackendExternalServicepoint
        fields = "__all__"


class ArBackendQuestionBlockFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArBackendQuestionBlockField
        fields = "__all__"


class ArXQuestionBlockAnswerFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArXQuestionBlockAnswerField
        fields = "__all__"


class ArBackendEntranceFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArBackendEntranceField
        fields = "__all__"


class ArBackendEntranceChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArBackendEntranceChoice
        fields = "__all__"


class ArBackendEntrancePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArBackendEntrancePlace
        fields = "__all__"


class ArBackendEntranceSentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArBackendEntranceSentence
        fields = "__all__"


class ArBackendPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArBackendPlace
        fields = "__all__"


class ArXPlaceAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArXPlaceAnswer
        fields = "__all__"


class ArXPlaceAnswerBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArXPlaceAnswerBox
        fields = "__all__"


class ArXPlaceAnswerBoxTxtSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArXPlaceAnswerBoxTxt
        fields = "__all__"


class ArXQuestionBlockAnswerCmtSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArXQuestionBlockAnswerCmt
        fields = "__all__"


class ArXQuestionBlockAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArXQuestionBlockAnswer
        fields = "__all__"


class ArBackendCopyableEntranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArBackendCopyableEntrance
        fields = "__all__"


class ArBackendDeadPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArBackendDeadPhoto
        fields = "__all__"


class ArXQuestionBlockAnswerTxtSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArXQuestionBlockAnswerTxt
        fields = "__all__"


class ArBackendFormGuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArBackendFormGuide
        fields = "__all__"


class ArBackendEntranceSentenceGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArBackendEntranceSentenceGroup
        fields = "__all__"
