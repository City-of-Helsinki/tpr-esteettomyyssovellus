from django.contrib.auth.models import User, Group
from django.http.response import HttpResponse
from psycopg2.extensions import JSON
from rest_framework import status, viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from . serializers import *
import psycopg2
from rest_framework.response import Response
import urllib.parse as urlparse
from urllib.parse import parse_qs
from drf_multiple_model.viewsets import ObjectMultipleModelAPIViewSet
from rest_framework.decorators import action
import json

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
    filter_fields = ('servicepoint', 'form',)


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
    pagination_class = None
    filter_fields = ("ext_servicepoint_id",)

    @action(detail=True, methods=['POST'], url_path='update_address')
    def update_address(self, request, *args, **kwargs):
        try:
            request_data = request.data
            servicepoint = self.get_object()
            servicepoint.address_street_name = request_data["address_street_name"]
            servicepoint.address_no = request_data["address_no"]
            servicepoint.address_city = request_data["address_city"]
            servicepoint.modified_by = request_data["modified_by"]
            servicepoint.modified = request_data["modified"]
            servicepoint.save()
            return Response({'status': 'address updated'})
        except:
            return Response("Updating failed", status=status.HTTP_400_BAD_REQUEST)


class ArSystemViewSet(viewsets.ModelViewSet):
    """

    """
    queryset = ArSystem.objects.all()
    serializer_class = ArSystemSerializer
    filter_fields = ("system_id",)
    pagination_class = None
    # permission_classes = [permissions.IsAuthenticated]


class ArSystemFormViewSet(viewsets.ModelViewSet):
    """

    """
    queryset = ArSystemForm.objects.all()
    serializer_class = ArSystemFormSerializer

    permission_classes = [permissions.IsAuthenticated]


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


class ArXQuestionAnswerPhotoTxtViewSet(viewsets.ModelViewSet):
    queryset = ArXQuestionAnswerPhotoTxt.objects.all()
    serializer_class = ArXQuestionAnswerPhotoTxtSerializer

    filter_fields = ('answer_photo_id',)
    pagination_class = None


class ArXQuestionAnswerPhotoViewSet(viewsets.ModelViewSet):
    queryset = ArXQuestionAnswerPhoto.objects.all()
    serializer_class = ArXQuestionAnswerPhotoSerializer

    filter_fields = ('log',)
    pagination_class = None


class ArXQuestionAnswerCommentViewSet(viewsets.ModelViewSet):
    queryset = ArXQuestionAnswerComment.objects.all()
    serializer_class = ArXQuestionAnswerCommentSerializer

    filter_fields = ('log',)
    pagination_class = None


class ArXQuestionAnswerLocationViewSet(viewsets.ModelViewSet):
    queryset = ArXQuestionAnswerLocation.objects.all()
    serializer_class = ArXQuestionAnswerLocationSerializer

    filter_fields = ('log',)
    pagination_class = None


class ArXAnswerLogViewSet(viewsets.ModelViewSet):
    queryset = ArXAnswerLog.objects.all()
    serializer_class = ArXAnswerLogSerializer
    pagination_class = None
    filter_fields = ("entrance",)

    # Function for creating a new answer log so that the request returns the log_id
    def create(self, request, *args, **kwargs):
        serializer = ArXAnswerLogSerializer(data=request.data)
        if serializer.is_valid():
            log = serializer.save()
            log_id = log.log_id
            return Response(log_id, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class ArXQuestionAnswerViewSet(viewsets.ModelViewSet):
    queryset = ArXQuestionAnswer.objects.all()
    serializer_class = ArXQuestionAnswerSerializer
    pagination_class = None
    filter_fields = ("log",)

    def create(self, request, *args, **kwargs):
        data = []
        try:
            log_id = request.data["log"]
            data = request.data["data"]
        except:
            print("corrupted data")
        filtered_data = set(data)
        try:
                            # TODO: Move to constants
            ps_connection = psycopg2.connect(user="ar_dev",
                                             password="ar_dev",
                                             host="10.158.123.184",
                                             port="5432",
                                             database="hki")

            cursor = ps_connection.cursor(
                    cursor_factory=psycopg2.extras.RealDictCursor)

            for item in filtered_data:
                cursor.execute("INSERT INTO ar_dev.ar_x_question_answer VALUES (%s, %s)",
                               (log_id, item))
                ps_connection.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully into mobile table")

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while inserting to database", error)
            return Response("Error while inserting to database" + error,
                            status=status.HTTP_400_BAD_REQUEST)

        finally:
            # closing database connection.
            if ps_connection:
                cursor.close()
                ps_connection.close()
                print("PostgreSQL connection is closed")
                return Response("Items added to the database",
                                status=status.HTTP_201_CREATED)


class ChopAddressView(APIView):
    def get(self, request, format=None):
        # Placeholder endpoint for get request
        return Response("""Get called for a funcion call that requires
                        parameters and a post""")

    def post(self, request, format=None):
        # Post request to call the ptv_chop_address function in the psql
        # database
        address = ""
        post_office = ""

        #
        try:
            address = request.data["address"]
            post_office = request.data["postOffice"]
        except:
            print("Address data missing")


        try:
                            # TODO: Move to constants
            ps_connection = psycopg2.connect(user="ar_dev",
                                             password="ar_dev",
                                             host="10.158.123.184",
                                             port="5432",
                                             database="hki")

            cursor = ps_connection.cursor(
                    cursor_factory=psycopg2.extras.RealDictCursor)

            # Call the psql function that chops the address
            cursor.execute("SELECT ar_dev.ptv_chop_address(%s, %s)",
                           (address, post_office))

            # Get the returned values
            return_cursor = cursor.fetchall()

            # The psql function returns a string of type
            # "('address',1,Helsinki)". Strip the data
            # and turn it into a List

            # First strip the "(" and ")"
            print(return_cursor[0]["ptv_chop_address"])
            return_string = return_cursor[0]["ptv_chop_address"][1:][:-1]
            # Split by commas
            return_strings = return_string.split(',')
            # Strip the additional quotes from the address
            if return_strings[0][0] == '"':
                return_strings[0] = return_strings[0][1:][:-1]

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while using database function", error)
            return Response("Error while using database function",
                            status=status.HTTP_400_BAD_REQUEST)
        finally:
            # closing database connection.
            if ps_connection:
                cursor.close()
                ps_connection.close()
                print("PostgreSQL connection is closed")
                return Response(return_strings, status=status.HTTP_201_CREATED)


class GenerateSentencesView(APIView):
    def get(self, request, format=None):
        # Placeholder endpoint for get request
        return Response("""Get called for a funcion call that requires
                        parameters and a post""")

    def post(self, request, format=None):
        # Post request to call the arp_store_sentences function in the psql
        # database

        entrance_id = -1
        #
        try:
            entrance_id = request.data["entrance_id"]
        except:
            print("Address data missing")


        if entrance_id > 0:
            try:
                                # TODO: Move to constants
                ps_connection = psycopg2.connect(user="ar_dev",
                                                 password="ar_dev",
                                                 host="10.158.123.184",
                                                 port="5432",
                                                 database="hki")

                cursor = ps_connection.cursor(
                        cursor_factory=psycopg2.extras.RealDictCursor)

                # Call the psql function that chops the address
                cursor.execute("SELECT ar_dev.arp_store_sentences(%s)",
                               [entrance_id])
                ps_connection.commit()

            except (Exception, psycopg2.DatabaseError) as error:
                print("Error while using database function arp_store_sentences", error)
                return Response("Error while using database function",
                                status=status.HTTP_400_BAD_REQUEST)
            finally:
                # closing database connection.
                if ps_connection:
                    cursor.close()
                    ps_connection.close()
                    print("PostgreSQL connection is closed")
                    return Response("Sentences created",
                                    status=status.HTTP_201_CREATED)
        else:
            return Response("Entrance_id missing. No function called.",
                            status=status.HTTP_400_BAD_REQUEST)


class ArRest01AccessVariableView(APIView):

    def get(self, request, format=JSON):
        try:
            data = ArRest01AccessVariable.objects.all()
            modified_data = []
            for item in data:
                modified_data.append({
                    "variableId": item.variable_id,
                    "variableName": item.variable_name,
                    "values": item.values_data.split(',')
                })
            return HttpResponse([json.dumps(modified_data, ensure_ascii=False)],
                                status=status.HTTP_200_OK)
        except:
            return Response("Error occured",
                            status=status.HTTP_400_BAD_REQUEST)



class ArRest01AccessViewpointView(APIView):

    def get(self, request, format=JSON):
        try:
            data = ArRest01AccessViewpoint.objects.all()
            modified_data = []
            for item in data:
                modified_data.append({
                    "viewpointId": item.viewpoint_id,
                    "names": [
                        {
                            "language": "fi",
                            "value": item.name_fi,
                        },
                                            {
                            "language": "sv",
                            "value": item.name_sv,
                        },                    {
                            "language": "en",
                            "value": item.name_en,
                        }
                    ],
                    "values": item.values_data.split(','),
                    "viewPointOrderText": item.viewpoint_order
                })
            return HttpResponse([json.dumps(modified_data, ensure_ascii=False)],
                                status=status.HTTP_200_OK)
        except:
            return Response("Error occured",
                            status=status.HTTP_400_BAD_REQUEST)



class ArRest01RequirementView(APIView):

    def get(self, request, format=JSON):
        try:
            data = ArRest01Requirement.objects.all()
            modified_data = []
            for item in data:
                modified_data.append({
                    "requirementId": item.requirement_id,
                    "requirementText": item.requirement_text,
                    "isIndoorRequirement": item.is_indoor_requirement,
                    "evaluationZone": item.evaluation_zone
                })
            return HttpResponse([json.dumps(modified_data, ensure_ascii=False)],
                                status=status.HTTP_200_OK)
        except:
            return Response("Error occured",
                            status=status.HTTP_400_BAD_REQUEST)


def ArRest01ServicepointView(request, systemId, servicePointId):

    try:
        # TODO: external_servicepoint_id or servicepoint_id
        data = ArRest01Servicepoint.objects.filter(system_id=systemId, external_servicepoint_id=servicePointId)
        item = data[0]
        integer_map = map(int, item.entrances.split(','))
        modified_data = {
            "systemId": str(item.system_id),
            "servicePointId": item.external_servicepoint_id,
            "name": item.servicepoint_name,
            "addressStreetName": item.address_street_name,
            "addressNo": item.address_no,
            "addressCity": item.address_city,
            "locEasting": item.loc_easting,
            "locNorthing": item.loc_northing,
            "accessibilityPhone": item.accessibility_phone,
            "accessibilityEmail": item.accessibility_email,
            "accessibilityWww": item.accessibility_www,
            "created": item.created.strftime("%Y-%m-%dT%H:%M:%S"),
            "modified": item.modified.strftime("%Y-%m-%dT%H:%M:%S"),
            "entrances": list(integer_map)
        }
        return HttpResponse([json.dumps(modified_data, ensure_ascii=False)],
                            status=status.HTTP_200_OK)
    except:
        return Response("Error occured",
                        status=status.HTTP_400_BAD_REQUEST)


def ArRest01EntranceView(request, systemId, servicePointId):

    try:
        data = ArRest01Entrance.objects.filter(system_id=systemId, external_servicepoint_id=servicePointId)
        modified_data = []
        for item in data:
            entrance = {
                "systemId": str(item.system_id),
                "servicePointId": item.external_servicepoint_id,
                "entranceId": item.entrance_id,
                "isMainEntrance": item.is_main_entrance == 'Y',
                "names": [],
                "locEasting": item.loc_easting,
                "locNorthing": item.loc_northing,
                "photoUrl": item.photo_url,
                "streetviewUrl": item.streetview_url,
                # 2014-11-14T09:10:58
                "created": item.created.strftime("%Y-%m-%dT%H:%M:%S"),
                "modified": item.modified.strftime("%Y-%m-%dT%H:%M:%S"),
                "sentencesCreated": item.sentences_created.strftime("%Y-%m-%dT%H:%M:%S"),
                "sentencesModified": item.sentences_modified.strftime("%Y-%m-%dT%H:%M:%S")
            }
            if item.name_fi:
                entrance["names"].append({"language": "fi", "value": item.name_fi})
            if item.name_sv:
                entrance["names"].append({"language": "sv", "value": item.name_sv})
            if item.name_en:
                entrance["names"].append({"language": "en", "value": item.name_en})

            modified_data.append(entrance)
        return HttpResponse([json.dumps(modified_data, ensure_ascii=False)],
                            status=status.HTTP_200_OK)
    except:
        return Response("Error occured",
                        status=status.HTTP_400_BAD_REQUEST)


def ArRest01SentenceView(request, systemId, servicePointId):

    try:
        data = ArRest01Sentence.objects.filter(system_id=systemId, external_servicepoint_id=servicePointId)
        modified_data = []
        for item in data:
            sentence = {
                "systemId": str(item.system_id),
                "servicePointId": item.external_servicepoint_id,
                "entranceId": item.entrance_id,
                "sentenceGroups": [],
                "sentences": [],
                "sentenceOrderText": item.sentence_order_text
            }
            if item.sentence_group_fi:
                sentence["sentenceGroups"].append({"language": "fi", "value": str(item.sentence_group_fi)})
            if item.sentence_group_sv:
                sentence["sentenceGroups"].append({"language": "sv", "value": item.sentence_group_sv})
            if item.sentence_group_en:
                sentence["sentenceGroups"].append({"language": "en", "value": item.sentence_group_en})

            if item.sentence_fi:
                sentence["sentences"].append({"language": "fi", "value": item.sentence_fi})
            if item.sentence_sv:
                sentence["sentences"].append({"language": "sv", "value": item.sentence_sv})
            if item.sentence_en:
                sentence["sentences"].append({"language": "en", "value": item.sentence_en})

            modified_data.append(sentence)
        return HttpResponse([json.dumps(modified_data, ensure_ascii=False)],
                            status=status.HTTP_200_OK)
    except:
        return Response("Error occured",
                        status=status.HTTP_400_BAD_REQUEST)


def ArRest01EntranceSentenceView(request, systemId, servicePointId, entranceId):

    try:
        data = ArRest01Sentence.objects.filter(system_id=systemId, external_servicepoint_id=servicePointId,
                                               entrance_id=entranceId)
        modified_data = []
        for item in data:
            sentence = {
                "systemId": str(item.system_id),
                "servicePointId": item.external_servicepoint_id,
                "entranceId": item.entrance_id,
                "sentenceGroups": [],
                "sentences": [],
                "sentenceOrderText": item.sentence_order_text
            }
            if item.sentence_group_fi:
                sentence["sentenceGroups"].append({"language": "fi", "value": str(item.sentence_group_fi)})
            if item.sentence_group_sv:
                sentence["sentenceGroups"].append({"language": "sv", "value": item.sentence_group_sv})
            if item.sentence_group_en:
                sentence["sentenceGroups"].append({"language": "en", "value": item.sentence_group_en})

            if item.sentence_fi:
                sentence["sentences"].append({"language": "fi", "value": item.sentence_fi})
            if item.sentence_sv:
                sentence["sentences"].append({"language": "sv", "value": item.sentence_sv})
            if item.sentence_en:
                sentence["sentences"].append({"language": "en", "value": item.sentence_en})

            modified_data.append(sentence)
        return HttpResponse([json.dumps(modified_data, ensure_ascii=False)],
                            status=status.HTTP_200_OK)
    except:
        return Response("Error occured",
                        status=status.HTTP_400_BAD_REQUEST)


