from aifc import Error
from django.contrib.auth.models import User, Group
from django.http.response import HttpResponse
from psycopg2.extensions import JSON
from rest_framework import status, viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from esteettomyyssovellus.settings import API_TOKEN
from .serializers import *
import psycopg2
from rest_framework.response import Response
import urllib.parse as urlparse
from urllib.parse import parse_qs
from drf_multiple_model.viewsets import ObjectMultipleModelAPIViewSet
from rest_framework.decorators import action
import json
from esteettomyyssovellus.settings import (
    DB_HOST,
    DB_PASSWORD,
    DB_PORT,
    DB_USER,
    DB,
    DEBUG,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        if not DEBUG and (
            "HTTP_AUTHORIZATION" not in request.META
            or request.META["HTTP_AUTHORIZATION"] != API_TOKEN
        ):
            return HttpResponse(
                "Token authentication failed.", status=status.HTTP_403_FORBIDDEN
            )
        return super().list(request, *args, **kwargs)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def list(self, request, *args, **kwargs):
        if not DEBUG and (
            "HTTP_AUTHORIZATION" not in request.META
            or request.META["HTTP_AUTHORIZATION"] != API_TOKEN
        ):
            return HttpResponse(
                "Token authentication failed.", status=status.HTTP_403_FORBIDDEN
            )
        return super().list(request, *args, **kwargs)


class ArEntranceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ArEntrances to be viewed or edited.
    """

    queryset = ArEntrance.objects.all()
    serializer_class = ArEntranceSerializer
    # permission_classes = [permissions.IsAuthenticated]
    filter_fields = (
        "servicepoint",
        "form",
    )

    def list(self, request, *args, **kwargs):
        if not DEBUG and (
            "HTTP_AUTHORIZATION" not in request.META
            or request.META["HTTP_AUTHORIZATION"] != API_TOKEN
        ):
            return HttpResponse(
                "Token authentication failed.", status=status.HTTP_403_FORBIDDEN
            )
        return super().list(request, *args, **kwargs)


class ArFormViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar_form.
    """

    queryset = ArForm.objects.all()
    serializer_class = ArFormSerializer

    def list(self, request, *args, **kwargs):
        if not DEBUG and (
            "HTTP_AUTHORIZATION" not in request.META
            or request.META["HTTP_AUTHORIZATION"] != API_TOKEN
        ):
            return HttpResponse(
                "Token authentication failed.", status=status.HTTP_403_FORBIDDEN
            )
        return super().list(request, *args, **kwargs)


class ArXQuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar_x_question.
    """

    queryset = ArXQuestion.objects.all()
    serializer_class = ArXQuestionSerializer

    # In order to filter form_id with URL type for example:
    # http://localhost:8000/api/ArXQuestions/?form_id=1
    filter_fields = ("form_id",)

    def list(self, request, *args, **kwargs):
        if not DEBUG and (
            "HTTP_AUTHORIZATION" not in request.META
            or request.META["HTTP_AUTHORIZATION"] != API_TOKEN
        ):
            return HttpResponse(
                "Token authentication failed.", status=status.HTTP_403_FORBIDDEN
            )
        return super().list(request, *args, **kwargs)


class ArXQuestionBlockViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar_x_question_block.
    """

    queryset = ArXQuestionBlock.objects.all()
    serializer_class = ArXQuestionBlockSerializer

    def list(self, request, *args, **kwargs):
        if not DEBUG and (
            "HTTP_AUTHORIZATION" not in request.META
            or request.META["HTTP_AUTHORIZATION"] != API_TOKEN
        ):
            return HttpResponse(
                "Token authentication failed.", status=status.HTTP_403_FORBIDDEN
            )
        return super().list(request, *args, **kwargs)


class ArServicepointViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar_servicepoint.
    """

    queryset = ArServicepoint.objects.all()
    serializer_class = ArServicepointSerializer
    pagination_class = None
    filter_fields = ("ext_servicepoint_id",)

    def list(self, request, *args, **kwargs):
        if not DEBUG and (
            "HTTP_AUTHORIZATION" not in request.META
            or request.META["HTTP_AUTHORIZATION"] != API_TOKEN
        ):
            return HttpResponse(
                "Token authentication failed.", status=status.HTTP_403_FORBIDDEN
            )
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=["POST"], url_path="update_address")
    def update_address(self, request, *args, **kwargs):
        if not DEBUG and (
            "HTTP_AUTHORIZATION" not in request.META
            or request.META["HTTP_AUTHORIZATION"] != API_TOKEN
        ):
            return HttpResponse(
                "Token authentication failed.", status=status.HTTP_403_FORBIDDEN
            )
        try:
            request_data = request.data
            servicepoint = self.get_object()
            servicepoint.address_street_name = request_data["address_street_name"]
            servicepoint.address_no = request_data["address_no"]
            servicepoint.address_city = request_data["address_city"]
            servicepoint.modified_by = request_data["modified_by"]
            servicepoint.modified = request_data["modified"]
            servicepoint.save()
            return Response({"status": "address updated"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response("Updating failed", status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["POST"], url_path="update_accessibility_contacts")
    def update_accessibility_contacts(self, request, *args, **kwargs):
        if not DEBUG and (
            "HTTP_AUTHORIZATION" not in request.META
            or request.META["HTTP_AUTHORIZATION"] != API_TOKEN
        ):
            return HttpResponse(
                "Token authentication failed.", status=status.HTTP_403_FORBIDDEN
            )
        try:
            request_data = request.data
            servicepoint = self.get_object()
            servicepoint.accessibility_phone = request_data["accessibility_phone"]
            servicepoint.accessibility_email = request_data["accessibility_email"]
            servicepoint.accessibility_www = request_data["accessibility_www"]
            servicepoint.modified_by = request_data["modified_by"]
            servicepoint.modified = request_data["modified"]
            servicepoint.save()
            return Response(
                {"status": "accessibility information updated"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response("Updating failed", status=status.HTTP_400_BAD_REQUEST)


class ArSystemViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar_system.
    """

    queryset = ArSystem.objects.all()
    serializer_class = ArSystemSerializer
    filter_fields = ("system_id",)
    pagination_class = None

    def list(self, request, *args, **kwargs):
        if not DEBUG and (
            "HTTP_AUTHORIZATION" not in request.META
            or request.META["HTTP_AUTHORIZATION"] != API_TOKEN
        ):
            return HttpResponse(
                "Token authentication failed.", status=status.HTTP_403_FORBIDDEN
            )
        return super().list(request, *args, **kwargs)


class ArExternalServicepointViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar_external_servicepoint.
    """

    queryset = ArExternalServicepoint.objects.all()
    serializer_class = ArExternalServicepointSerializer
    filter_fields = (
        "servicepoint_id",
        "system_id",
    )
    pagination_class = None

    def list(self, request, *args, **kwargs):
        if not DEBUG and (
            "HTTP_AUTHORIZATION" not in request.META
            or request.META["HTTP_AUTHORIZATION"] != API_TOKEN
        ):
            return HttpResponse(
                "Token authentication failed.", status=status.HTTP_403_FORBIDDEN
            )
        return super().list(request, *args, **kwargs)


class ArSystemFormViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar_system_form.
    """

    queryset = ArSystemForm.objects.all()
    serializer_class = ArSystemFormSerializer
    pagination_class = None

    def list(self, request, *args, **kwargs):
        if not DEBUG and (
            "HTTP_AUTHORIZATION" not in request.META
            or request.META["HTTP_AUTHORIZATION"] != API_TOKEN
        ):
            return HttpResponse(
                "Token authentication failed.", status=status.HTTP_403_FORBIDDEN
            )
        return super().list(request, *args, **kwargs)


class ArFormLanguageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar_form_language.
    """

    queryset = ArFormLanguage.objects.all()
    serializer_class = ArFormLanguageSerializer

    def list(self, request, *args, **kwargs):
        if not DEBUG and (
            "HTTP_AUTHORIZATION" not in request.META
            or request.META["HTTP_AUTHORIZATION"] != API_TOKEN
        ):
            return HttpResponse(
                "Token authentication failed.", status=status.HTTP_403_FORBIDDEN
            )
        return super().list(request, *args, **kwargs)


class ArXQuestionLanguageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar_x_question_language.
    """

    queryset = ArXQuestionLanguage.objects.all()
    serializer_class = ArXQuestionLanguageSerializer

    def list(self, request, *args, **kwargs):
        if not DEBUG and (
            "HTTP_AUTHORIZATION" not in request.META
            or request.META["HTTP_AUTHORIZATION"] != API_TOKEN
        ):
            return HttpResponse(
                "Token authentication failed.", status=status.HTTP_403_FORBIDDEN
            )
        return super().list(request, *args, **kwargs)


class ArXStoredSentenceLangViewSet(viewsets.ViewSet):
    """
    Endpoint for ar_x_stored_sentence_lang table.
    Use with entrance_id parameter.
    http://localhost:8000/api/ArXStoredSentenceLangs/?entrance_id=1&form_submitted=Y
    """

    def list(self, request):
        if not DEBUG and (
            "HTTP_AUTHORIZATION" not in request.META
            or request.META["HTTP_AUTHORIZATION"] != API_TOKEN
        ):
            return HttpResponse(
                "Token authentication failed.", status=status.HTTP_403_FORBIDDEN
            )
        try:
            ps_connection = psycopg2.connect(
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT,
                database=DB,
            )

            cursor = ps_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            # Get url parameters from request
            parsed = urlparse.urlparse(self.request.get_raw_uri())

            # Check if entrance_id parameter is given,
            # if no parameter is given return an empty api enpoint
            try:
                entrance_id = parse_qs(parsed.query)["entrance_id"]
            except:
                entrance_id = "0"

            form_submitted = parse_qs(parsed.query)["form_submitted"]

            if form_submitted[0] == "Y":
                cursor.execute(
                    "SELECT * FROM ar_dev.ar_x_stored_sentence_lang WHERE entrance_id=%s AND form_submitted='Y' ORDER BY sentence_order_text",
                    entrance_id,
                )
            if form_submitted[0] == "D":
                cursor.execute(
                    "SELECT * FROM ar_dev.ar_x_stored_sentence_lang WHERE entrance_id=%s AND form_submitted='D' ORDER BY sentence_order_text",
                    entrance_id,
                )

            result = cursor.fetchall()
            return Response(result)
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)

        finally:
            # closing database connection.
            if ps_connection:
                cursor.close()
                ps_connection.close()
                print("PostgreSQL connection is closed")


class ArBackendQuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar_backend_question.
    """

    queryset = ArBackendQuestion.objects.all()
    serializer_class = ArBackendQuestionSerializer

    # In order to filter form_id with URL type for example:
    # http://localhost:8000/api/ArXQuestions/?form_id=1
    filter_fields = ("form_id", "question_id")
    pagination_class = None

    def list(self, request, *args, **kwargs):
        if not DEBUG and (
            "HTTP_AUTHORIZATION" not in request.META
            or request.META["HTTP_AUTHORIZATION"] != API_TOKEN
        ):
            return HttpResponse(
                "Token authentication failed.", status=status.HTTP_403_FORBIDDEN
            )
        return super().list(request, *args, **kwargs)


class ArBackendQuestionBlockViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar_backend_question_block.
    """

    queryset = ArBackendQuestionBlock.objects.all()
    serializer_class = ArBackendQuestionBlockSerializer

    # In order to filter form_id with URL type for example:
    # http://localhost:8000/api/ArXQuestions/?form_id=1
    filter_fields = ("form_id",)
    pagination_class = None

    def list(self, request, *args, **kwargs):
        if not DEBUG and (
            "HTTP_AUTHORIZATION" not in request.META
            or request.META["HTTP_AUTHORIZATION"] != API_TOKEN
        ):
            return HttpResponse(
                "Token authentication failed.", status=status.HTTP_403_FORBIDDEN
            )
        return super().list(request, *args, **kwargs)


class ArBackendQuestionChoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar_backend_question_choice.
    """

    queryset = ArBackendQuestionChoice.objects.all()
    serializer_class = ArBackendQuestionChoiceSerializer

    # In order to filter form_id with URL type for example:
    # http://localhost:8000/api/ArXQuestions/?form_id=1
    filter_fields = ("form_id",)
    pagination_class = None

    def list(self, request, *args, **kwargs):
        if not DEBUG and (
            "HTTP_AUTHORIZATION" not in request.META
            or request.META["HTTP_AUTHORIZATION"] != API_TOKEN
        ):
            return HttpResponse(
                "Token authentication failed.", status=status.HTTP_403_FORBIDDEN
            )
        return super().list(request, *args, **kwargs)


class ArBackendEntranceFieldViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar_backend_entrance.
    """

    queryset = ArBackendEntranceField.objects.all()
    serializer_class = ArBackendEntranceFieldSerializer

    # In order to filter form_id with URL type for example:
    # http://localhost:8000/api/ArXQuestions/?form_id=1
    filter_fields = ("entrance_id", "log_id")
    pagination_class = None

    def list(self, request, *args, **kwargs):
        if not DEBUG and (
            "HTTP_AUTHORIZATION" not in request.META
            or request.META["HTTP_AUTHORIZATION"] != API_TOKEN
        ):
            return HttpResponse(
                "Token authentication failed.", status=status.HTTP_403_FORBIDDEN
            )
        return super().list(request, *args, **kwargs)


class ArBackendEntranceAnswerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar_backend_entrance.
    """

    queryset = ArBackendEntranceAnswer.objects.all()
    serializer_class = ArBackendEntranceAnswerSerializer

    # In order to filter form_id with URL type for example:
    # http://localhost:8000/api/ArXQuestions/?form_id=1
    filter_fields = ("entrance_id", "log_id")
    pagination_class = None

    def list(self, request, *args, **kwargs):
        if not DEBUG and (
            "HTTP_AUTHORIZATION" not in request.META
            or request.META["HTTP_AUTHORIZATION"] != API_TOKEN
        ):
            return HttpResponse(
                "Token authentication failed.", status=status.HTTP_403_FORBIDDEN
            )
        return super().list(request, *args, **kwargs)


class ArXAdditionalinfoViewSet(ObjectMultipleModelAPIViewSet):
    """
    API endpoint for ar_x_additional_info.
    """

    search_fields = ["log", "question"]
    querylist = [
        {
            "queryset": ArXQuestionAnswerComment.objects.all(),
            "serializer_class": ArXQuestionAnswerCommentSerializer,
            "label": "comment",
        },
        {
            "queryset": ArXQuestionAnswerLocation.objects.all(),
            "serializer_class": ArXQuestionAnswerLocationSerializer,
            "label": "location",
        },
        {
            "queryset": ArXQuestionAnswerPhoto.objects.all(),
            "serializer_class": ArXQuestionAnswerPhotoSerializer,
            "label": "photo",
        },
    ]
    pagination_class = None

    def list(self, request, *args, **kwargs):
        if not DEBUG and (
            "HTTP_AUTHORIZATION" not in request.META
            or request.META["HTTP_AUTHORIZATION"] != API_TOKEN
        ):
            return HttpResponse(
                "Token authentication failed.", status=status.HTTP_403_FORBIDDEN
            )
        return super().list(request, *args, **kwargs)


# class ArXQuestionAnswerPhotoTxtViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint for ar_x_question_answer_photo_text.
#     """

#     queryset = ArXQuestionAnswerPhotoTxt.objects.all()
#     serializer_class = ArXQuestionAnswerPhotoTxtSerializer

#     filter_fields = ("answer_photo_id",)
#     pagination_class = None


# class ArXQuestionAnswerPhotoViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint for ar_x_questtion_answer_photo.
#     """

#     queryset = ArXQuestionAnswerPhoto.objects.all()
#     serializer_class = ArXQuestionAnswerPhotoSerializer

#     filter_fields = ("log",)
#     pagination_class = None


# class ArXQuestionAnswerCommentViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint for ar_x_question_answer_comment.
#     """

#     queryset = ArXQuestionAnswerComment.objects.all()
#     serializer_class = ArXQuestionAnswerCommentSerializer

#     filter_fields = ("log",)
#     pagination_class = None


# class ArXQuestionAnswerLocationViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint for ar_x_question_answer_location.
#     """

#     queryset = ArXQuestionAnswerLocation.objects.all()
#     serializer_class = ArXQuestionAnswerLocationSerializer

#     filter_fields = ("log",)
#     pagination_class = None


class ArXAnswerLogViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar_x_answer_log.
    """

    queryset = ArXAnswerLog.objects.all()
    serializer_class = ArXAnswerLogSerializer
    pagination_class = None
    filter_fields = ("entrance",)

    def list(self, request, *args, **kwargs):
        if not DEBUG and (
            "HTTP_AUTHORIZATION" not in request.META
            or request.META["HTTP_AUTHORIZATION"] != API_TOKEN
        ):
            return HttpResponse(
                "Token authentication failed.", status=status.HTTP_403_FORBIDDEN
            )
        return super().list(request, *args, **kwargs)

    # Function for creating a new answer log so that the request returns the log_id
    def create(self, request, *args, **kwargs):
        if not DEBUG and (
            "HTTP_AUTHORIZATION" not in request.META
            or request.META["HTTP_AUTHORIZATION"] != API_TOKEN
        ):
            return HttpResponse(
                "Token authentication failed.", status=status.HTTP_403_FORBIDDEN
            )
        serializer = ArXAnswerLogSerializer(data=request.data)
        if serializer.is_valid():
            log = serializer.save()
            log_id = log.log_id
            return Response(log_id, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArXQuestionAnswerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar_x_question_answer.
    """

    queryset = ArXQuestionAnswer.objects.all()
    serializer_class = ArXQuestionAnswerSerializer
    pagination_class = None
    filter_fields = ("log",)

    def list(self, request, *args, **kwargs):
        if not DEBUG and (
            "HTTP_AUTHORIZATION" not in request.META
            or request.META["HTTP_AUTHORIZATION"] != API_TOKEN
        ):
            return HttpResponse(
                "Token authentication failed.", status=status.HTTP_403_FORBIDDEN
            )
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if not DEBUG and (
            "HTTP_AUTHORIZATION" not in request.META
            or request.META["HTTP_AUTHORIZATION"] != API_TOKEN
        ):
            return HttpResponse(
                "Token authentication failed.", status=status.HTTP_403_FORBIDDEN
            )
        data = []
        try:
            log_id = request.data["log"]
            data = request.data["data"]
        except:
            print("corrupted data")
        filtered_data = set(data)
        try:
            ps_connection = psycopg2.connect(
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT,
                database=DB,
            )

            cursor = ps_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            for item in filtered_data:
                cursor.execute(
                    "INSERT INTO ar_dev.ar_x_question_answer VALUES (%s, %s)",
                    (log_id, item),
                )
                ps_connection.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully into mobile table")

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while inserting to database", error)
            return Response(
                "Error while inserting to database" + error,
                status=status.HTTP_400_BAD_REQUEST,
            )

        finally:
            # closing database connection.
            if ps_connection:
                cursor.close()
                ps_connection.close()
                print("PostgreSQL connection is closed")
                return Response(
                    "Items added to the database", status=status.HTTP_201_CREATED
                )


class ArXQuestionBlockAnswerFieldViewSet(viewsets.ModelViewSet):
    """
    API endpoint for
    """

    queryset = ArXQuestionBlockAnswerField.objects.all()
    serializer_class = ArXQuestionBlockAnswerFieldSerializer
    pagination_class = None
    filter_fields = ("log_id",)

    def list(self, request, *args, **kwargs):
        if not DEBUG and (
            "HTTP_AUTHORIZATION" not in request.META
            or request.META["HTTP_AUTHORIZATION"] != API_TOKEN
        ):
            return HttpResponse(
                "Token authentication failed.", status=status.HTTP_403_FORBIDDEN
            )
        return super().list(request, *args, **kwargs)


class ChopAddressView(APIView):
    """
    API endpoint for chopping the address at ptv_chop_address.
    """

    def get(self, request, format=None):
        if not DEBUG and (
            "HTTP_AUTHORIZATION" not in request.META
            or request.META["HTTP_AUTHORIZATION"] != API_TOKEN
        ):
            return HttpResponse(
                "Token authentication failed.", status=status.HTTP_403_FORBIDDEN
            )
        # Placeholder endpoint for get request
        return Response(
            """Get called for a funcion call that requires
                        parameters and a post"""
        )

    def post(self, request, format=None):
        if not DEBUG and (
            "HTTP_AUTHORIZATION" not in request.META
            or request.META["HTTP_AUTHORIZATION"] != API_TOKEN
        ):
            return HttpResponse(
                "Token authentication failed.", status=status.HTTP_403_FORBIDDEN
            )
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
            ps_connection = psycopg2.connect(
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT,
                database=DB,
            )

            cursor = ps_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            # Call the psql function that chops the address
            cursor.execute(
                "SELECT ar_dev.ptv_chop_address(%s, %s)", (address, post_office)
            )

            # Get the returned values
            return_cursor = cursor.fetchall()

            # The psql function returns a string of type
            # "('address',1,Helsinki)". Strip the data
            # and turn it into a List

            # First strip the "(" and ")"
            print(return_cursor[0]["ptv_chop_address"])
            return_string = return_cursor[0]["ptv_chop_address"][1:][:-1]
            # Split by commas
            return_strings = return_string.split(",")
            # Strip the additional quotes from the address
            if return_strings[0][0] == '"':
                return_strings[0] = return_strings[0][1:][:-1]

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while using database function", error)
            return Response(
                "Error while using database function",
                status=status.HTTP_400_BAD_REQUEST,
            )
        finally:
            # closing database connection.
            if ps_connection:
                cursor.close()
                ps_connection.close()
                print("PostgreSQL connection is closed")
                return Response(return_strings, status=status.HTTP_201_CREATED)


class GenerateSentencesView(APIView):
    """
    API endpoint for creating sentences at arp_store_sentences.
    """

    def get(self, request, format=None):
        if not DEBUG and (
            "HTTP_AUTHORIZATION" not in request.META
            or request.META["HTTP_AUTHORIZATION"] != API_TOKEN
        ):
            return HttpResponse(
                "Token authentication failed.", status=status.HTTP_403_FORBIDDEN
            )
        # Placeholder endpoint for get request
        return Response(
            """Get called for a funcion call that requires
                        parameters and a post"""
        )

    def post(self, request, format=None):
        # Post request to call the arp_store_sentences function in the psql
        # database
        if not DEBUG and (
            "HTTP_AUTHORIZATION" not in request.META
            or request.META["HTTP_AUTHORIZATION"] != API_TOKEN
        ):
            return HttpResponse(
                "Token authentication failed.", status=status.HTTP_403_FORBIDDEN
            )

        entrance_id = -1
        form_submitted = "D"
        #
        try:
            entrance_id = request.data["entrance_id"]
            form_submitted = request.data["form_submitted"]
        except:
            print("Address data missing")

        if entrance_id > 0:
            try:
                ps_connection = psycopg2.connect(
                    user=DB_USER,
                    password=DB_PASSWORD,
                    host=DB_HOST,
                    port=DB_PORT,
                    database=DB,
                )

                cursor = ps_connection.cursor(
                    cursor_factory=psycopg2.extras.RealDictCursor
                )

                # Call the psql function that creates the sentences
                cursor.execute(
                    "SELECT ar_dev.arp_store_sentences(%s, %s)",
                    (entrance_id, form_submitted),
                )
                ps_connection.commit()

            except (Exception, psycopg2.Error) as error:
                print("Error while using database function arp_store_sentences", error)
                return Response(
                    "Error while using database function",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            finally:
                # closing database connection.
                if ps_connection:
                    cursor.close()
                    ps_connection.close()
                    print("PostgreSQL connection is closed")
                    return Response("Sentences created", status=status.HTTP_201_CREATED)
        else:
            return HttpResponse("Error occured", status=status.HTTP_400_BAD_REQUEST)


class ArRest01AccessVariableView(APIView):
    """
    API endpoint for ar_rest01_access_variable.
    """

    def get(self, request, format=JSON):
        try:
            data = ArRest01AccessVariable.objects.all()
            modified_data = []
            for item in data:
                modified_data.append(
                    {
                        "variableId": item.variable_id,
                        "variableName": item.variable_name,
                        "values": item.values_data.split(","),
                    }
                )
            return HttpResponse(
                [json.dumps(modified_data, ensure_ascii=False)],
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            return HttpResponse(
                "Error occured: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArRest01AccessViewpointView(APIView):
    """
    API endpoint for ar_rest01_access_viewpoint.
    """

    def get(self, request, format=JSON):
        try:
            data = ArRest01AccessViewpoint.objects.all()
            modified_data = []
            for item in data:
                modified_data.append(
                    {
                        "viewpointId": int(item.viewpoint_id),
                        "names": [
                            {
                                "language": "fi",
                                "value": item.name_fi,
                            },
                            {
                                "language": "sv",
                                "value": item.name_sv,
                            },
                            {
                                "language": "en",
                                "value": item.name_en,
                            },
                        ],
                        "values": item.values_data.split(","),
                        "viewPointOrderText": item.viewpoint_order,
                    }
                )
            return HttpResponse(
                [json.dumps(modified_data, ensure_ascii=False)],
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            return HttpResponse(
                "Error occured: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArRest01RequirementView(APIView):
    """
    API endpoint for ar_rest01_requirement.
    """

    def get(self, request, format=JSON):
        try:
            data = ArRest01Requirement.objects.all()
            modified_data = []
            for item in data:
                modified_data.append(
                    {
                        "requirementId": item.requirement_id,
                        "requirementText": item.requirement_text,
                        "isIndoorRequirement": item.is_indoor_requirement,
                        "evaluationZone": item.evaluation_zone,
                    }
                )
            return HttpResponse(
                [json.dumps(modified_data, ensure_ascii=False)],
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            return HttpResponse(
                "Error occured: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArRest01ServicepointView(APIView):
    def get(self, request, systemId=None, servicePointId=None, format=None):
        try:
            # TODO: external_servicepoint_id or servicepoint_id
            data = ArRest01Servicepoint.objects.filter(
                system_id=systemId, external_servicepoint_id=servicePointId
            )
            item = data[0]
            integer_map = map(int, item.entrances.split(","))
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
                "entrances": list(integer_map),
            }
            return HttpResponse(
                [json.dumps(modified_data, ensure_ascii=False)],
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            return HttpResponse(
                "Error occured: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArRest01EntranceView(APIView):
    def get(self, request, systemId=None, servicePointId=None, format=None):
        try:
            data = ArRest01Entrance.objects.filter(
                system_id=systemId, external_servicepoint_id=servicePointId
            )
            modified_data = []
            for item in data:
                entrance = {
                    "systemId": str(item.system_id),
                    "servicePointId": item.external_servicepoint_id,
                    "entranceId": item.entrance_id,
                    "isMainEntrance": item.is_main_entrance == "Y",
                    "names": [],
                    "locEasting": item.loc_easting,
                    "locNorthing": item.loc_northing,
                    "photoUrl": item.photo_url,
                    "streetviewUrl": item.streetview_url,
                    # 2014-11-14T09:10:58
                    "created": item.created.strftime("%Y-%m-%dT%H:%M:%S"),
                    "modified": item.modified.strftime("%Y-%m-%dT%H:%M:%S"),
                    "sentencesCreated": item.sentences_created.strftime(
                        "%Y-%m-%dT%H:%M:%S"
                    ),
                    "sentencesModified": item.sentences_modified.strftime(
                        "%Y-%m-%dT%H:%M:%S"
                    ),
                }
                if item.name_fi:
                    entrance["names"].append({"language": "fi", "value": item.name_fi})
                if item.name_sv:
                    entrance["names"].append({"language": "sv", "value": item.name_sv})
                if item.name_en:
                    entrance["names"].append({"language": "en", "value": item.name_en})

                modified_data.append(entrance)
            return HttpResponse(
                [json.dumps(modified_data, ensure_ascii=False)],
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            return HttpResponse(
                "Error occured: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


# def ArRest01EntranceView(request, systemId, servicePointId):


#     try:
#         data = ArRest01Entrance.objects.filter(system_id=systemId, external_servicepoint_id=servicePointId)
#         modified_data = []
#         for item in data:
#             entrance = {
#                 "systemId": str(item.system_id),
#                 "servicePointId": item.external_servicepoint_id,
#                 "entranceId": item.entrance_id,
#                 "isMainEntrance": item.is_main_entrance == 'Y',
#                 "names": [],
#                 "locEasting": item.loc_easting,
#                 "locNorthing": item.loc_northing,
#                 "photoUrl": item.photo_url,
#                 "streetviewUrl": item.streetview_url,
#                 # 2014-11-14T09:10:58
#                 "created": item.created.strftime("%Y-%m-%dT%H:%M:%S"),
#                 "modified": item.modified.strftime("%Y-%m-%dT%H:%M:%S"),
#                 "sentencesCreated": item.sentences_created.strftime("%Y-%m-%dT%H:%M:%S"),
#                 "sentencesModified": item.sentences_modified.strftime("%Y-%m-%dT%H:%M:%S")
#             }
#             if item.name_fi:
#                 entrance["names"].append({"language": "fi", "value": item.name_fi})
#             if item.name_sv:
#                 entrance["names"].append({"language": "sv", "value": item.name_sv})
#             if item.name_en:
#                 entrance["names"].append({"language": "en", "value": item.name_en})

#             modified_data.append(entrance)
#         return HttpResponse([json.dumps(modified_data, ensure_ascii=False)],
#                             status=status.HTTP_200_OK)
#     except Exception as error:
#         return HttpResponse("Error occured: " + str(error),
#                         status=status.HTTP_400_BAD_REQUEST)


class ArRest01SentenceView(APIView):
    def get(self, request, systemId=None, servicePointId=None, format=None):
        try:
            data = ArRest01Sentence.objects.filter(
                system_id=systemId, external_servicepoint_id=servicePointId
            )
            modified_data = []
            for item in data:
                sentence = {
                    "systemId": str(item.system_id),
                    "servicePointId": item.external_servicepoint_id,
                    "entranceId": item.entrance_id,
                    "sentenceGroups": [],
                    "sentences": [],
                    "sentenceOrderText": item.sentence_order_text,
                }
                if item.sentence_group_fi:
                    sentence["sentenceGroups"].append(
                        {"language": "fi", "value": str(item.sentence_group_fi)}
                    )
                if item.sentence_group_sv:
                    sentence["sentenceGroups"].append(
                        {"language": "sv", "value": item.sentence_group_sv}
                    )
                if item.sentence_group_en:
                    sentence["sentenceGroups"].append(
                        {"language": "en", "value": item.sentence_group_en}
                    )

                if item.sentence_fi:
                    sentence["sentences"].append(
                        {"language": "fi", "value": item.sentence_fi}
                    )
                if item.sentence_sv:
                    sentence["sentences"].append(
                        {"language": "sv", "value": item.sentence_sv}
                    )
                if item.sentence_en:
                    sentence["sentences"].append(
                        {"language": "en", "value": item.sentence_en}
                    )

                modified_data.append(sentence)
            return HttpResponse(
                [json.dumps(modified_data, ensure_ascii=False)],
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            return HttpResponse(
                "Error occured: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArRest01EntranceSentenceView(APIView):
    def get(
        self, request, systemId=None, servicePointId=None, entranceId=None, format=None
    ):
        try:
            data = ArRest01Sentence.objects.filter(
                system_id=systemId,
                external_servicepoint_id=servicePointId,
                entrance_id=entranceId,
            )
            modified_data = []
            for item in data:
                sentence = {
                    "systemId": str(item.system_id),
                    "servicePointId": item.external_servicepoint_id,
                    "entranceId": item.entrance_id,
                    "sentenceGroups": [],
                    "sentences": [],
                    "sentenceOrderText": item.sentence_order_text,
                }
                if item.sentence_group_fi:
                    sentence["sentenceGroups"].append(
                        {"language": "fi", "value": str(item.sentence_group_fi)}
                    )
                if item.sentence_group_sv:
                    sentence["sentenceGroups"].append(
                        {"language": "sv", "value": item.sentence_group_sv}
                    )
                if item.sentence_group_en:
                    sentence["sentenceGroups"].append(
                        {"language": "en", "value": item.sentence_group_en}
                    )

                if item.sentence_fi:
                    sentence["sentences"].append(
                        {"language": "fi", "value": item.sentence_fi}
                    )
                if item.sentence_sv:
                    sentence["sentences"].append(
                        {"language": "sv", "value": item.sentence_sv}
                    )
                if item.sentence_en:
                    sentence["sentences"].append(
                        {"language": "en", "value": item.sentence_en}
                    )

                modified_data.append(sentence)
            return HttpResponse(
                [json.dumps(modified_data, ensure_ascii=False)],
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            return HttpResponse(
                "Error occured: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArRest01ShortageView(APIView):
    def get(
        self, request, systemId=None, servicePointId=None, viewPointId=None, format=None
    ):
        try:
            if viewPointId != None:
                data = ArRest01Shortage.objects.filter(
                    system_id=systemId,
                    servicepoint_id=servicePointId,
                    viewpoint_id=viewPointId,
                )
            elif servicePointId != None:
                data = ArRest01Shortage.objects.filter(
                    system_id=systemId, servicepoint_id=servicePointId
                )
            else:
                data = ArRest01Shortage.objects.filter(system_id=systemId)
            if len(data) > 0:
                modified_data = []
                for item in data:
                    shortage = {
                        "systemId": str(item.system_id),
                        "servicePointId": item.external_servicepoint_id,
                        "viewpointId": item.viewpoint_id,
                        "shortages": [],
                    }
                    if item.shortage_fi:
                        shortage["shortages"].append(
                            {"language": "fi", "value": item.shortage_fi}
                        )
                    if item.shortage_sv:
                        shortage["shortages"].append(
                            {"language": "sv", "value": item.shortage_sv}
                        )
                    if item.shortage_en:
                        shortage["shortages"].append(
                            {"language": "en", "value": item.shortage_en}
                        )

                    modified_data.append(shortage)
                return HttpResponse(
                    [json.dumps(modified_data, ensure_ascii=False)],
                    status=status.HTTP_200_OK,
                )
        except Exception as error:
            return HttpResponse(
                "Error occured: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArSystemServicepointsView(APIView):
    def get(self, request, systemId=None, format=None):
        try:
            # TODO: external_servicepoint_id or servicepoint_id
            data = ArRest01Servicepoint.objects.filter(system_id=systemId)

            modified_data = []
            for item in data:
                integer_map = map(int, item.entrances.split(","))
                modified_data.append(
                    {
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
                        "entrances": list(integer_map),
                    }
                )
            return HttpResponse(
                [json.dumps(modified_data, ensure_ascii=False)],
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            return HttpResponse(
                "Error occured: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArSystemEntrancesView(APIView):
    def get(self, request, systemId=None, format=None):
        try:
            data = ArRest01Entrance.objects.filter(system_id=systemId)
            modified_data = []
            for item in data:
                entrance = {
                    "systemId": str(item.system_id),
                    "servicePointId": item.external_servicepoint_id,
                    "entranceId": item.entrance_id,
                    "isMainEntrance": item.is_main_entrance == "Y",
                    "names": [],
                    "locEasting": item.loc_easting,
                    "locNorthing": item.loc_northing,
                    "photoUrl": item.photo_url,
                    "streetviewUrl": item.streetview_url,
                    "created": item.created.strftime("%Y-%m-%dT%H:%M:%S"),
                    "modified": item.modified.strftime("%Y-%m-%dT%H:%M:%S"),
                    "sentencesCreated": item.sentences_created.strftime(
                        "%Y-%m-%dT%H:%M:%S"
                    ),
                    "sentencesModified": item.sentences_modified.strftime(
                        "%Y-%m-%dT%H:%M:%S"
                    ),
                }
                if item.name_fi:
                    entrance["names"].append({"language": "fi", "value": item.name_fi})
                if item.name_sv:
                    entrance["names"].append({"language": "sv", "value": item.name_sv})
                if item.name_en:
                    entrance["names"].append({"language": "en", "value": item.name_en})

                modified_data.append(entrance)
            return HttpResponse(
                [json.dumps(modified_data, ensure_ascii=False)],
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            return HttpResponse(str(error), status=status.HTTP_400_BAD_REQUEST)


class ArSystemSentencesView(APIView):
    def get(self, request, systemId=None, format=None):
        try:
            data = ArRest01Sentence.objects.filter(system_id=systemId)
            modified_data = []
            for item in data:
                sentence = {
                    "systemId": str(item.system_id),
                    "servicePointId": item.external_servicepoint_id,
                    "entranceId": item.entrance_id,
                    "sentenceGroups": [],
                    "sentences": [],
                    "sentenceOrderText": item.sentence_order_text,
                }
                if item.sentence_group_fi:
                    sentence["sentenceGroups"].append(
                        {"language": "fi", "value": str(item.sentence_group_fi)}
                    )
                if item.sentence_group_sv:
                    sentence["sentenceGroups"].append(
                        {"language": "sv", "value": item.sentence_group_sv}
                    )
                if item.sentence_group_en:
                    sentence["sentenceGroups"].append(
                        {"language": "en", "value": item.sentence_group_en}
                    )

                if item.sentence_fi:
                    sentence["sentences"].append(
                        {"language": "fi", "value": item.sentence_fi}
                    )
                if item.sentence_sv:
                    sentence["sentences"].append(
                        {"language": "sv", "value": item.sentence_sv}
                    )
                if item.sentence_en:
                    sentence["sentences"].append(
                        {"language": "en", "value": item.sentence_en}
                    )

                modified_data.append(sentence)
            return HttpResponse(
                [json.dumps(modified_data, ensure_ascii=False)],
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            return HttpResponse(
                "Error occured: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArRest01ServicepointAccessibilityViewset(APIView):
    def get(
        self, request, systemId=None, servicePointId=None, entranceId=None, format=None
    ):
        try:
            if servicePointId != None:
                data = ArRest01ServicepointAccessibility.objects.filter(
                    system_id=systemId, servicepoint_id=servicePointId
                )
            else:
                data = ArRest01ServicepointAccessibility.objects.filter(
                    system_id=systemId
                )
            modified_data = []
            for item in data:
                property = {
                    "systemId": str(item.system_id),
                    "servicePointId": item.servicepoint_id,
                    "variableId": item.variable_id,
                    "variableName": item.variable_name,
                    "value": item.rest_value,
                }
                modified_data.append(property)
            return HttpResponse(
                [json.dumps(modified_data, ensure_ascii=False)],
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            return HttpResponse(
                "Error occured: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArRest01EntranceAccessibilityViewset(APIView):
    def get(
        self, request, systemId=None, servicePointId=None, entranceId=None, format=None
    ):
        try:
            if entranceId != None:
                data = ArRest01EntranceAccessibility.objects.filter(
                    system_id=systemId,
                    servicepoint_id=servicePointId,
                    entrance_id=entranceId,
                )
            elif servicePointId != None:
                data = ArRest01EntranceAccessibility.objects.filter(
                    system_id=systemId, servicepoint_id=servicePointId
                )
            else:
                data = ArRest01EntranceAccessibility.objects.filter(
                    system_id=systemId,
                )
            modified_data = []
            for item in data:
                property = {
                    "systemId": str(item.system_id),
                    "servicePointId": item.servicepoint_id,
                    "entranceId": item.entrance_id,
                    "variableId": item.variable_id,
                    "variableName": item.variable_name,
                    "value": item.rest_value,
                }
                modified_data.append(property)
            return HttpResponse(
                [json.dumps(modified_data, ensure_ascii=False)],
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            return HttpResponse(
                "Error occured: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArRest01SummaryViewset(APIView):
    def get(
        self,
        request,
        systemId=None,
        servicePointId=None,
        entranceId=None,
        viewPointId=None,
        format=None,
    ):
        try:
            if viewPointId != None:
                data = ArRest01Summary.objects.filter(
                    system_id=systemId,
                    servicepoint_id=servicePointId,
                    viewpoint_id=viewPointId,
                )
            elif servicePointId != None:
                data = ArRest01Summary.objects.filter(
                    system_id=systemId, servicepoint_id=servicePointId
                )
            else:
                data = ArRest01Summary.objects.filter(
                    system_id=systemId,
                )
            modified_data = []
            for item in data:
                property = {
                    "systemId": str(item.system_id),
                    "servicePointId": item.servicepoint_id,
                    "viewpointId": item.viewpoint_id,
                    "isAccessible": item.is_accessible,
                    "shortageCount": item.shortage_count,
                }
                modified_data.append(property)
            return HttpResponse(
                [json.dumps(modified_data, ensure_ascii=False)],
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            return HttpResponse(
                "Error occured: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArRest01ReportshortageViewset(APIView):
    def get(
        self,
        request,
        systemId=None,
        servicePointId=None,
        entranceId=None,
        viewPointId=None,
        format=None,
    ):
        try:
            if servicePointId != None:
                data = ArRest01Reportshortage.objects.filter(
                    system_id=systemId, servicepoint_id=servicePointId
                )
            else:
                data = ArRest01Reportshortage.objects.filter(
                    system_id=systemId,
                )
            modified_data = []
            for item in data:
                property = {
                    "systemId": str(item.system_id),
                    "servicePointId": item.servicepoint_id,
                    "viewpointId": item.viewpoint_id,
                    "isIndoorServicepoint": item.is_indoor_servicepoint == "Y",
                    "evaluationZone": item.evaluation_zone,
                    "easyToFix": item.easy_to_fix,
                    "requirementId": item.requirement_id,
                    "requirementText": item.requirement_text,
                    "explanationWhyNot": item.explanation_why_not,
                    "shortages": [],
                }
                if item.shortage_fi:
                    property["shortages"].append(
                        {"language": "fi", "value": item.shortage_fi}
                    )
                if item.shortage_sv:
                    property["shortages"].append(
                        {"language": "sv", "value": item.shortage_sv}
                    )
                if item.shortage_en:
                    property["shortages"].append(
                        {"language": "en", "value": item.shortage_en}
                    )

                modified_data.append(property)
            return HttpResponse(
                [json.dumps(modified_data, ensure_ascii=False)],
                status=status.HTTP_200_OK,
            )

        except Exception as error:
            return HttpResponse(
                "Error occured: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArRest01ReportsummaryViewset(APIView):
    def get(
        self,
        request,
        systemId=None,
        servicePointId=None,
        entranceId=None,
        viewPointId=None,
        format=None,
    ):
        try:
            if servicePointId != None:
                data = ArRest01Reportsummary.objects.filter(
                    system_id=systemId, servicepoint_id=servicePointId
                )
            else:
                data = ArRest01Reportsummary.objects.filter(
                    system_id=systemId,
                )
            modified_data = []
            for item in data:
                property = {
                    "systemId": str(item.system_id),
                    "servicePointId": item.servicepoint_id,
                    "isAccessible": item.is_accessible,
                    "shortageCount": item.shortage_count,
                    "shortageCountEasyToFix": item.shortage_count_easy_to_fix,
                    "wheelIsAccessible": item.wheel_is_accessible,
                    "wheelShortageCount": item.wheel_shortage_count,
                    "wheelShortageCountOutside": item.wheel_shortage_count_outside,
                    "wheelShortageCountEntrance": item.wheel_shortage_count_entrance,
                    "wheelShortageCountInside": item.wheel_shortage_count_inside,
                    "visualIsAccessible": item.visual_is_accessible,
                    "visualShortageCount": item.visual_shortage_count,
                    "visualShortageCountEasyToFix": item.visual_shortage_count_easy_to_fix,
                    "visualShortageCountOutside": item.visual_shortage_count_outside,
                    "visualShortageCountEntrance": item.visual_shortage_count_entrance,
                    "visualShortageCountInside": item.visual_shortage_count_inside,
                    "hearingIsAccessible": item.hearing_is_accessible,
                    "toiletIsAccessible": item.toilet_is_accessible,
                }

                modified_data.append(property)
            return HttpResponse(
                [json.dumps(modified_data, ensure_ascii=False)],
                status=status.HTTP_200_OK,
            )

        except Exception as error:
            return HttpResponse(
                "Error occured: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArBackendEntranceViewset(viewsets.ModelViewSet):
    """
    API endpoint for ar backend entrance.
    """

    queryset = ArBackendEntrance.objects.all()
    serializer_class = ArBackendEntranceSerializer
    pagination_class = None
    filter_fields = ("entrance_id",)

    def list(self, request, *args, **kwargs):
        if not DEBUG and (
            "HTTP_AUTHORIZATION" not in request.META
            or request.META["HTTP_AUTHORIZATION"] != API_TOKEN
        ):
            return HttpResponse(
                "Token authentication failed.", status=status.HTTP_403_FORBIDDEN
            )
        return super().list(request, *args, **kwargs)


class ArBackendServicepointViewset(viewsets.ModelViewSet):
    """
    API endpoint for ar backend entrance.
    """

    queryset = ArBackendServicepoint.objects.all()
    serializer_class = ArBackendServicepointSerializer
    pagination_class = None
    filter_fields = ("servicepoint_id",)

    def list(self, request, *args, **kwargs):
        if not DEBUG and (
            "HTTP_AUTHORIZATION" not in request.META
            or request.META["HTTP_AUTHORIZATION"] != API_TOKEN
        ):
            return HttpResponse(
                "Token authentication failed.", status=status.HTTP_403_FORBIDDEN
            )
        return super().list(request, *args, **kwargs)


class ArBackendQuestionBlockFieldViewset(viewsets.ModelViewSet):
    """ """

    queryset = ArBackendQuestionBlockField.objects.all()
    serializer_class = ArBackendQuestionBlockFieldSerializer
    pagination_class = None
    filter_fields = ("question_block_id",)

    def list(self, request, *args, **kwargs):
        if not DEBUG and (
            "HTTP_AUTHORIZATION" not in request.META
            or request.META["HTTP_AUTHORIZATION"] != API_TOKEN
        ):
            return HttpResponse(
                "Token authentication failed.", status=status.HTTP_403_FORBIDDEN
            )
        return super().list(request, *args, **kwargs)
