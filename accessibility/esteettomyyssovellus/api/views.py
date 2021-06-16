from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from . serializers import *
from . models import ArEntrance, ArForm, ArXQuestion
import psycopg2
from rest_framework.response import Response

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


class InfoTextViewSet(viewsets.ViewSet):

    def list(self, request):
        try:

            ps_connection = psycopg2.connect(user="ar_dev",
                                            password="ar_dev",
                                            host="10.158.123.184",
                                            port="5432",
                                            database="hki")

            cursor = ps_connection.cursor()

            # call stored procedure
            cursor.callproc('arp_store_other_sentences', [1, "fi"])
            result = cursor.fetchall()
            for row in result:
                print(row)
            
            return Response(result)

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connecting to PostgreSQL", error)

        finally:
            # closing database connection.
            if ps_connection:
                cursor.close()
                ps_connection.close()
                print("PostgreSQL connection is closed")




class ArXQuestionAnswerPhotoViewSet(viewsets.ModelViewSet):
    """
    
    """
    queryset = ArXQuestionAnswerPhoto.objects.all()
    serializer_class = ArXQuestionAnswerPhotoSerializer
    