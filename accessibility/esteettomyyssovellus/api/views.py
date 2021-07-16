from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from . serializers import *
import psycopg2
from rest_framework.response import Response
import urllib.parse as urlparse
from urllib.parse import parse_qs
from drf_multiple_model.viewsets import ObjectMultipleModelAPIViewSet

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class ArEntranceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ArEntrances to be viewed or edited.
    """
    queryset = ArEntrance.objects.all()
    serializer_class = ArEntranceSerializer
    # permission_classes = [permissions.IsAuthenticated]
    filter_fields = ('servicepoint',)


class ArFormViewSet(viewsets.ModelViewSet):
    """
    API endpoint for forms.
    """
    queryset = ArForm.objects.all()
    serializer_class = ArFormSerializer


class ArXQuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for forms.
    """
    queryset = ArXQuestion.objects.all()
    serializer_class = ArXQuestionSerializer

    # In order to filter form_id with URL type for example:
    # http://localhost:8000/api/ArXQuestions/?form_id=1
    filter_fields = ('form_id',)


class ArXQuestionBlockViewSet(viewsets.ModelViewSet):
    """
    API endpoint for forms.
    """
    queryset = ArXQuestionBlock.objects.all()
    serializer_class = ArXQuestionBlockSerializer


class ArServicepointViewSet(viewsets.ModelViewSet):
    """

    """
    queryset = ArServicepoint.objects.all()
    serializer_class = ArServicepointSerializer


class ArSystemViewSet(viewsets.ModelViewSet):
    """

    """
    queryset = ArSystem.objects.all()
    serializer_class = ArSystemSerializer

    permission_classes = [permissions.IsAuthenticated]


class ArSystemFormViewSet(viewsets.ModelViewSet):
    """

    """
    queryset = ArSystemForm.objects.all()
    serializer_class = ArSystemFormSerializer

    permission_classes = [permissions.IsAuthenticated]

#
#
#   EXAMPLE ON HOW TO ACCESS DATA IN THE DATABASE
#   WITHOUT USING DJANGO ORM!
#
#
# class InfoTextViewSet(viewsets.ViewSet):

#     def list(self, request):
#         try:

#             ps_connection = psycopg2.connect(user="ar_dev",
#                                             password="ar_dev",
#                                             host="10.158.123.184",
#                                             port="5432",
#                                             database="hki")

#             cursor = ps_connection.cursor(
#                   cursor_factory=psycopg2.extras.RealDictCursor)

#             # call stored procedure
#             cursor.execute("""SELECT * FROM ar_dev.ar_backend_question;""")
#             result = cursor.fetchall()
#             return Response(result)

#         except (Exception, psycopg2.DatabaseError) as error:
#             print("Error while connecting to PostgreSQL", error)

#         finally:
#             # closing database connection.
#             if ps_connection:
#                 cursor.close()
#                 ps_connection.close()
#                 print("PostgreSQL connection is closed")


class ArXQuestionAnswerPhotoViewSet(viewsets.ModelViewSet):
    """

    """
    queryset = ArXQuestionAnswerPhoto.objects.all()
    serializer_class = ArXQuestionAnswerPhotoSerializer


# class ArBackendCopyableEntranceViewSet(viewsets.ModelViewSet):
#     queryset = ArBackendCopyableEntrance.objects.all()
#     serializer_class = ArBackendCopyableEntranceSerializer


class ArFormLanguageViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = ArFormLanguage.objects.all()
    serializer_class = ArFormLanguageSerializer


class ArXQuestionLanguageViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = ArXQuestionLanguage.objects.all()
    serializer_class = ArXQuestionLanguageSerializer


class ArXStoredSentenceLangViewSet(viewsets.ViewSet):
    """
    Endpoint for ar_x_stored_sentence_lang table.
    Use with entrance_id parameter.
    http://localhost:8000/api/ArXStoredSentenceLangs/?entrance_id=1
    """
    def list(self, request):
        try:
            # TODO: Move to constants
            ps_connection = psycopg2.connect(user="ar_dev",
                                             password="ar_dev",
                                             host="10.158.123.184",
                                             port="5432",
                                             database="hki")

            cursor = ps_connection.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor)

            # Get url parameters from request
            parsed = urlparse.urlparse(self.request.get_raw_uri())

            # Check if entrance_id parameter is given,
            # if no parameter is given return an empty api enpoint
            try:
                entrance_id = parse_qs(parsed.query)['entrance_id']
            except:
                entrance_id = "0"

            cursor.execute("""SELECT * FROM ar_dev.ar_x_stored_sentence_lang
                            WHERE entrance_id=%s
                            ORDER BY sentence_order_text""",
                            entrance_id)
            result = cursor.fetchall()
            return Response(result)

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connecting to PostgreSQL", error)

        finally:
            # closing database connection.
            if ps_connection:
                cursor.close()
                ps_connection.close()
                print("PostgreSQL connection is closed")


class ArBackendQuestionViewSet(viewsets.ModelViewSet):
    queryset = ArBackendQuestion.objects.all()
    serializer_class = ArBackendQuestionSerializer

    # In order to filter form_id with URL type for example:
    # http://localhost:8000/api/ArXQuestions/?form_id=1
    filter_fields = ('form_id', 'question_id')
    pagination_class = None


class ArBackendQuestionBlockViewSet(viewsets.ModelViewSet):
    queryset = ArBackendQuestionBlock.objects.all()
    serializer_class = ArBackendQuestionBlockSerializer

    # In order to filter form_id with URL type for example:
    # http://localhost:8000/api/ArXQuestions/?form_id=1
    filter_fields = ('form_id',)
    pagination_class = None


class ArBackendQuestionChoiceViewSet(viewsets.ModelViewSet):
    queryset = ArBackendQuestionChoice.objects.all()
    serializer_class = ArBackendQuestionChoiceSerializer

    # In order to filter form_id with URL type for example:
    # http://localhost:8000/api/ArXQuestions/?form_id=1
    filter_fields = ('form_id',)
    pagination_class = None


class ArBackendEntranceAnswerViewSet(viewsets.ModelViewSet):
    queryset = ArBackendEntranceAnswer.objects.all()
    serializer_class = ArBackendEntranceAnswerSerializer

    # In order to filter form_id with URL type for example:
    # http://localhost:8000/api/ArXQuestions/?form_id=1
    filter_fields = ('entrance_id', 'log_id')
    pagination_class = None


class ArXAdditionalinfoViewSet(ObjectMultipleModelAPIViewSet):

    search_fields = ["log", "question"]
    querylist = [
        {'queryset': ArXQuestionAnswerComment.objects.all(), 'serializer_class': ArXQuestionAnswerCommentSerializer, 'label': "comment"},
        {'queryset': ArXQuestionAnswerLocation.objects.all(), 'serializer_class': ArXQuestionAnswerLocationSerializer, 'label': "location"},
        {'queryset': ArXQuestionAnswerPhoto.objects.all(), 'serializer_class': ArXQuestionAnswerPhotoSerializer, 'label': "photo"}
    ]
    pagination_class = None


class ArXQuestionAnswerPhotoTxtVieSet(viewsets.ModelViewSet):
    queryset = ArXQuestionAnswerPhotoTxt.objects.all()
    serializer_class = ArXQuestionAnswerPhotoTxtSerializer

    filter_fields = ('answer_photo_id',)
    pagination_class = None


class ArXQuestionAnswerPhotoVieSet(viewsets.ModelViewSet):
    queryset = ArXQuestionAnswerPhoto.objects.all()
    serializer_class = ArXQuestionAnswerPhotoSerializer

    filter_fields = ('log',)
    pagination_class = None


class ArXQuestionAnswerCommentVieSet(viewsets.ModelViewSet):
    queryset = ArXQuestionAnswerComment.objects.all()
    serializer_class = ArXQuestionAnswerCommentSerializer

    filter_fields = ('log',)
    pagination_class = None


class ArXQuestionAnswerLocationVieSet(viewsets.ModelViewSet):
    queryset = ArXQuestionAnswerLocation.objects.all()
    serializer_class = ArXQuestionAnswerLocationSerializer

    filter_fields = ('log',)
    pagination_class = None