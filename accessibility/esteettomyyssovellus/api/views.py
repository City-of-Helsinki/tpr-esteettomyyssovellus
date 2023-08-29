from django.contrib.auth.models import User, Group
from django.http import QueryDict
from django.http.response import HttpResponse
from psycopg2.extensions import JSON
from rest_framework import status, viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from esteettomyyssovellus.settings import (
    PUBLIC_AZURE_CONTAINER,
    AZURE_URL,
    PDF_BASE_URL,
)
import uuid
from azure.storage.blob import ContentSettings
from .serializers import *
import psycopg2
from rest_framework.response import Response
import urllib.parse as urlparse
from urllib.parse import parse_qs
from rest_framework.decorators import action
import json
from esteettomyyssovellus.settings import (
    DB_HOST,
    DB_PASSWORD,
    DB_PORT,
    DB_USER,
    DB,
    DEBUG,
    SEARCH_PATH,
    API_TOKEN,
)
import hashlib
from rest_framework import permissions
from .storage import create_blob_client
import base64
from urllib.parse import urlparse, parse_qs
from dateutil import parser
from datetime import datetime
from django.shortcuts import redirect
from rest_framework.renderers import JSONRenderer
from esteettomyyssovellus.api.renderers import CustomXmlRenderer

# pdf imports
from django.conf import settings as conf_settings
from django.utils import timezone
from django.views.generic import ListView
from django_weasyprint import WeasyTemplateResponseMixin

class TokenPermission(permissions.BasePermission):
    edit_methods = "__all__"

    def has_permission(self, request, view):
        if not DEBUG and (
            "HTTP_AUTHORIZATION" not in request.META
            or request.META["HTTP_AUTHORIZATION"]
            != hashlib.sha256(API_TOKEN.encode("ascii")).hexdigest()
        ):
            return False
        return True


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [
        TokenPermission,
    ]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [
        TokenPermission,
    ]


class ArEntranceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ArEntrances to be viewed or edited.
    """

    queryset = ArEntrance.objects.all()
    serializer_class = ArEntranceSerializer
    permission_classes = [
        TokenPermission,
    ]
    filter_fields = (
        "servicepoint",
        "form",
    )

    @action(detail=True, methods=["POST"], url_path="delete_entrance_data")
    def delete_entrance_data(self, request, *args, **kwargs):
        # Post request to call the arp_delete_place_from_answer function in the psql database
        entrance_id = ""

        try:
            entrance = self.get_object()
            entrance_id = entrance.entrance_id
        except:
            print("Required data missing")
            return Response(
                "Error while getting entrance. Entrance_id not in database.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            ps_connection = psycopg2.connect(
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT,
                database=DB,
                options="-c search_path={}".format(SEARCH_PATH),
            )

            cursor = ps_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            # Call the psql function that chops the address
            cursor.execute("SELECT arp_delete_entrance_data(%s)", [entrance_id])

            # Get the returned values
            result = cursor.fetchall()
            ps_connection.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while using database function", error)
            result = str(error)
            return Response(
                "Error while using database function %s",
                error,
                status=status.HTTP_400_BAD_REQUEST,
            )
        finally:
            # closing database connection.
            if ps_connection:
                cursor.close()
                ps_connection.close()
                print("PostgreSQL connection is closed")
            return HttpResponse(
                [
                    json.dumps(
                        {
                            "status": result,
                            "deleted_entrance_id": entrance_id,
                        }
                    )
                ],
                status=201,
            )

    @action(detail=True, methods=["POST"], url_path="delete_entrance")
    def delete_entrance(self, request, *args, **kwargs):
        # Post request to call the arp_delete_place_from_answer function in the psql database
        entrance_id = ""

        try:
            entrance = self.get_object()
            entrance_id = entrance.entrance_id
        except:
            print("Required data missing")
            return Response(
                "Error while getting entrance. Entrance_id not in database.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            ps_connection = psycopg2.connect(
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT,
                database=DB,
                options="-c search_path={}".format(SEARCH_PATH),
            )

            cursor = ps_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            # Call the psql function that chops the address
            cursor.execute("SELECT arp_delete_entrance_data(%s)", [entrance_id])

            # Get the returned values
            result = cursor.fetchall()
            ps_connection.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while using database function", error)
            result = str(error)
            return Response(
                "Error while using database function %s",
                error,
                status=status.HTTP_400_BAD_REQUEST,
            )
        finally:
            # closing database connection.
            if ps_connection:
                cursor.close()
                ps_connection.close()
                print("PostgreSQL connection is closed")
            # Delete the entrance entry from the database.
            entrance.delete()
            # Return response
            return HttpResponse(
                [
                    json.dumps(
                        {
                            "status": result,
                            "deleted_entrance_id": entrance_id,
                        }
                    )
                ],
                status=201,
            )


class ArFormViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar_form.
    """

    queryset = ArForm.objects.all()
    serializer_class = ArFormSerializer
    permission_classes = [
        TokenPermission,
    ]


class ArXQuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar_x_question.
    """

    queryset = ArXQuestion.objects.all()
    serializer_class = ArXQuestionSerializer

    # In order to filter form_id with URL type for example:
    # http://localhost:8000/api/ArXQuestions/?form_id=1
    filter_fields = ("form_id",)
    permission_classes = [
        TokenPermission,
    ]


class ArXQuestionBlockViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar_x_question_block.
    """

    queryset = ArXQuestionBlock.objects.all()
    serializer_class = ArXQuestionBlockSerializer
    permission_classes = [
        TokenPermission,
    ]


class ArServicepointViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar_servicepoint.
    """

    queryset = ArServicepoint.objects.all()
    serializer_class = ArServicepointSerializer
    pagination_class = None
    filter_fields = ("servicepoint_id",)
    permission_classes = [
        TokenPermission,
    ]

    @action(detail=True, methods=["POST"], url_path="update_address")
    def update_address(self, request, *args, **kwargs):
        try:
            request_data = request.data
            servicepoint = self.get_object()
            servicepoint.address_street_name = request_data["address_street_name"]
            servicepoint.address_no = request_data["address_no"]
            servicepoint.address_city = request_data["address_city"]
            servicepoint.loc_easting = request_data["loc_easting"]
            servicepoint.loc_northing = request_data["loc_northing"]
            servicepoint.modified_by = request_data["modified_by"]
            servicepoint.modified = request_data["modified"]
            servicepoint.save()
            return Response({"status": "address updated"}, status=status.HTTP_200_OK)
        except Exception as e:
            return HttpResponse("Updating failed", status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=True, methods=["POST"], url_path="update_accessibility_contacts")
    # def update_accessibility_contacts(self, request, *args, **kwargs):
    #     try:
    #         request_data = request.data
    #         servicepoint = self.get_object()
    #         servicepoint.accessibility_phone = request_data["accessibility_phone"]
    #         servicepoint.accessibility_email = request_data["accessibility_email"]
    #         servicepoint.accessibility_www = request_data["accessibility_www"]
    #         servicepoint.modified_by = request_data["modified_by"]
    #         servicepoint.modified = request_data["modified"]
    #         servicepoint.save()
    #         return Response(
    #             {"status": "accessibility information updated"},
    #             status=status.HTTP_200_OK,
    #         )
    #     except Exception as e:
    #         return HttpResponse("Updating failed", status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["POST"], url_path="update_external")
    def update_external(self, request, *args, **kwargs):
        try:
            request_data = request.data
            servicepoint = self.get_object()
            servicepoint.servicepoint_name = request_data["servicepoint_name"]
            servicepoint.ext_servicepoint_id = request_data["ext_servicepoint_id"]
            servicepoint.modified_by = request_data["modified_by"]
            servicepoint.modified = request_data["modified"]
            servicepoint.is_searchable = "Y"
            servicepoint.save()
            return Response({"status": "external servicepoint id updated"}, status=status.HTTP_200_OK)
        except Exception as e:
            return HttpResponse("Updating failed", status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=True, methods=["POST"], url_path="set_searchable")
    # def set_searchable(self, request, *args, **kwargs):
    #     try:
    #         servicepoint = self.get_object()
    #         servicepoint.is_searchable = "Y"
    #         servicepoint.save()
    #         return Response(
    #             {"status": "servicepoint set searchable."},
    #             status=status.HTTP_200_OK,
    #         )
    #     except Exception as e:
    #         return HttpResponse("Updating failed", status=status.HTTP_400_BAD_REQUEST)


class ArSystemViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar_system.
    """

    queryset = ArSystem.objects.all()
    serializer_class = ArSystemSerializer
    filter_fields = (
        "system_id",
        "name",
    )
    pagination_class = None
    permission_classes = [
        TokenPermission,
    ]


class ArExternalServicepointViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar_external_servicepoint.
    """

    queryset = ArExternalServicepoint.objects.all()
    serializer_class = ArExternalServicepointSerializer
    filter_fields = (
        "servicepoint_id",
        "system_id",
        "external_servicepoint_id",
    )
    pagination_class = None
    permission_classes = [
        TokenPermission,
    ]


class ArSystemFormViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar_system_form.
    """

    queryset = ArSystemForm.objects.all()
    serializer_class = ArSystemFormSerializer
    pagination_class = None
    permission_classes = [
        TokenPermission,
    ]


class ArFormLanguageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar_form_language.
    """

    queryset = ArFormLanguage.objects.all()
    serializer_class = ArFormLanguageSerializer
    permission_classes = [
        TokenPermission,
    ]


class ArXQuestionLanguageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar_x_question_language.
    """

    queryset = ArXQuestionLanguage.objects.all()
    serializer_class = ArXQuestionLanguageSerializer
    permission_classes = [
        TokenPermission,
    ]


class ArXStoredSentenceLangViewSet(viewsets.ViewSet):
    """
    Endpoint for ar_x_stored_sentence_lang table.
    Use with entrance_id parameter.
    http://localhost:8000/api/ArXStoredSentenceLangs/?entrance_id=1&form_submitted=Y
    """

    permission_classes = [
        TokenPermission,
    ]

    def list(self, request):
        try:
            ps_connection = psycopg2.connect(
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT,
                database=DB,
                options="-c search_path={}".format(SEARCH_PATH),
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
                    "SELECT * FROM ar_x_stored_sentence_lang WHERE entrance_id=%s AND form_submitted='Y' ORDER BY sentence_order_text",
                    entrance_id,
                )
            if form_submitted[0] == "D":
                cursor.execute(
                    "SELECT * FROM ar_x_stored_sentence_lang WHERE entrance_id=%s AND form_submitted='D' ORDER BY sentence_order_text",
                    entrance_id,
                )

            result = cursor.fetchall()
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
            result = {"error": error}
        finally:
            # closing database connection.
            if ps_connection:
                cursor.close()
                ps_connection.close()
                print("PostgreSQL connection is closed")
            return Response(result)


class ArBackendQuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar_backend_question.
    """

    queryset = ArBackendQuestion.objects.all()
    serializer_class = ArBackendQuestionSerializer

    # In order to filter form_id with URL type for example:
    # http://localhost:8000/api/ArXQuestions/?form_id=1
    filter_fields = (
        "form_id",
        "question_id",
        "language_id",
        "question_block_id",
    )
    pagination_class = None
    permission_classes = [
        TokenPermission,
    ]


class ArBackendQuestionBlockViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar_backend_question_block.
    """

    queryset = ArBackendQuestionBlock.objects.all()
    serializer_class = ArBackendQuestionBlockSerializer

    # In order to filter form_id with URL type for example:
    # http://localhost:8000/api/ArXQuestions/?form_id=1
    filter_fields = (
        "form_id",
        "language_id",
        "question_block_id",
    )
    pagination_class = None
    permission_classes = [
        TokenPermission,
    ]


class ArBackendQuestionChoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar_backend_question_choice.
    """

    queryset = ArBackendQuestionChoice.objects.all()
    serializer_class = ArBackendQuestionChoiceSerializer

    # In order to filter form_id with URL type for example:
    # http://localhost:8000/api/ArXQuestions/?form_id=1
    filter_fields = (
        "form_id",
        "language_id",
        "question_block_id",
        "question_id",
        "question_choice_id",
    )
    pagination_class = None
    permission_classes = [
        TokenPermission,
    ]


class ArBackendEntranceFieldViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar_backend_entrance.
    """

    queryset = ArBackendEntranceField.objects.all()
    serializer_class = ArBackendEntranceFieldSerializer

    # In order to filter form_id with URL type for example:
    # http://localhost:8000/api/ArXQuestions/?form_id=1
    filter_fields = (
        "log_id",
        "entrance_id",
        "question_block_id",
        "question_block_field_id",
        "form_submitted",
    )
    pagination_class = None
    permission_classes = [
        TokenPermission,
    ]


class ArBackendEntranceAnswerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar_backend_entrance.
    """

    queryset = ArBackendEntranceAnswer.objects.all()
    serializer_class = ArBackendEntranceAnswerSerializer

    # In order to filter form_id with URL type for example:
    # http://localhost:8000/api/ArXQuestions/?form_id=1
    filter_fields = (
        "entrance_id",
        "log_id",
        "form_submitted",
        "question_block_id",
        "question_id",
        "question_choice_id",
    )
    pagination_class = None
    permission_classes = [
        TokenPermission,
    ]


class ArBackendFormViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar_backend_form.
    """

    queryset = ArBackendForm.objects.all()
    serializer_class = ArBackendFormSerializer
    pagination_class = None
    filter_fields = ("form_id",)
    permission_classes = [
        TokenPermission,
    ]


class ArBackendFormGuideViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar_backend_form_guide.
    """

    queryset = ArBackendFormGuide.objects.all()
    serializer_class = ArBackendFormGuideSerializer
    pagination_class = None
    filter_fields = ("form_id",)
    permission_classes = [
        TokenPermission,
    ]


# class ArXAdditionalinfoViewSet(ObjectMultipleModelAPIViewSet):
#     """
#     API endpoint for ar_x_additional_info.
#     """

#     search_fields = ["log", "question"]
#     querylist = [
#         {
#             "queryset": ArXQuestionAnswerComment.objects.all(),
#             "serializer_class": ArXQuestionAnswerCommentSerializer,
#             "label": "comment",
#         },
#         {
#             "queryset": ArXQuestionAnswerLocation.objects.all(),
#             "serializer_class": ArXQuestionAnswerLocationSerializer,
#             "label": "location",
#         },
#         {
#             "queryset": ArXQuestionAnswerPhoto.objects.all(),
#             "serializer_class": ArXQuestionAnswerPhotoSerializer,
#             "label": "photo",
#         },
#     ]
#     pagination_class = None
#     permission_classes = [
#         TokenPermission,
#     ]


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
    permission_classes = [
        TokenPermission,
    ]

    # Function for creating a new answer log so that the request returns the log_id
    def create(self, request, *args, **kwargs):
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
    permission_classes = [
        TokenPermission,
    ]

    def create(self, request, *args, **kwargs):
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
                options="-c search_path={}".format(SEARCH_PATH),
            )

            cursor = ps_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            for item in filtered_data:
                cursor.execute(
                    "INSERT INTO ar_x_question_answer VALUES (%s, %s)",
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
    permission_classes = [
        TokenPermission,
    ]


class ChopAddressView(APIView):
    """
    API endpoint for chopping the address at ptv_chop_address.
    """

    permission_classes = [
        TokenPermission,
    ]

    def get(self, request, format=None):
        # Placeholder endpoint for get request
        return Response(
            """Get called for a function call that requires parameters and a post"""
        )

    def post(self, request, format=None):
        # Post request to call the ptv_chop_address function in the psql database
        address = ""
        post_office = ""

        try:
            address = request.data["address"]
            post_office = request.data["postOffice"]
        except:
            return HttpResponse("Address data missing", status=status.HTTP_400_BAD_REQUEST)

        try:
            ps_connection = psycopg2.connect(
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT,
                database=DB,
                options="-c search_path={}".format(SEARCH_PATH),
            )

            cursor = ps_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            # Call the psql function that chops the address
            cursor.execute("SELECT ptv_chop_address(%s, %s)", (address, post_office))

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

    permission_classes = [
        TokenPermission,
    ]

    def get(self, request, format=None):
        # Placeholder endpoint for get request
        return Response(
            """Get called for a function call that requires parameters and a post"""
        )

    def post(self, request, format=None):
        # Post request to call the arp_store_sentences function in the psql database
        entrance_id = -1
        form_submitted = "D"

        try:
            entrance_id = request.data["entrance_id"]
            form_submitted = request.data["form_submitted"]
        except:
            return HttpResponse("Entrance id or form submitted data missing", status=status.HTTP_400_BAD_REQUEST)

        if entrance_id > 0:
            try:
                ps_connection = psycopg2.connect(
                    user=DB_USER,
                    password=DB_PASSWORD,
                    host=DB_HOST,
                    port=DB_PORT,
                    database=DB,
                    options="-c search_path={}".format(SEARCH_PATH),
                )

                cursor = ps_connection.cursor(
                    cursor_factory=psycopg2.extras.RealDictCursor
                )

                # Call the psql function that creates the sentences
                cursor.execute(
                    "SELECT arp_store_sentences(%s, %s)",
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
                    return HttpResponse("Sentences created", status=status.HTTP_201_CREATED)
        else:
            return HttpResponse("Error occurred", status=status.HTTP_400_BAD_REQUEST)


class DisplayEntranceWithMapView(APIView):
    """
    API endpoint for getting value of tf2_display_entrance_with_map for log id.
    """

    permission_classes = [
        TokenPermission,
    ]

    def get(self, request, format=None):
        # Placeholder endpoint for get request
        return Response(
            """Get called for a function call that requires parameters and a post"""
        )

    def post(self, request, format=None):
        # Post request to call the tf2_display_entrance_with_map function in the psql database
        log_id = -1

        try:
            log_id = request.data["logId"]
        except:
            return HttpResponse("Log id data missing", status=status.HTTP_400_BAD_REQUEST)

        if log_id > 0:
            result_string = ""

            try:
                ps_connection = psycopg2.connect(
                    user=DB_USER,
                    password=DB_PASSWORD,
                    host=DB_HOST,
                    port=DB_PORT,
                    database=DB,
                    options="-c search_path={}".format(SEARCH_PATH),
                )

                cursor = ps_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

                # Call the psql function that gets the display entrance with map value
                cursor.execute("SELECT tf2_display_entrance_with_map(%s)", (log_id,))

                # Get the returned values
                return_cursor = cursor.fetchall()
                print("return_cursor " + str(return_cursor))
                result_string = return_cursor[0]["tf2_display_entrance_with_map"]

            except (Exception, psycopg2.Error) as error:
                print("Error while using database function tf2_display_entrance_with_map", error)
                return HttpResponse(
                    "Error while using database function",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            finally:
                # closing database connection.
                if ps_connection:
                    cursor.close()
                    ps_connection.close()
                    print("PostgreSQL connection is closed")
                    return HttpResponse(result_string, status=status.HTTP_200_OK)
        else:
            return HttpResponse("Error occurred", status=status.HTTP_400_BAD_REQUEST)


class ArRest01AccessVariableView(APIView):
    """
    API endpoint for ar_rest01_access_variable.
    """

    renderer_classes = (JSONRenderer,CustomXmlRenderer,)

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
            # return HttpResponse(
            #     [json.dumps(modified_data, ensure_ascii=False)],
            #     content_type="application/json; charset=utf-8",
            #     status=status.HTTP_200_OK,
            # )
            # HttpResponse(json_string, content_type='application/json; charset=utf-8')
            return Response(modified_data)
        except Exception as error:
            return HttpResponse(
                "Error occurred: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArRest01AccessViewpointView(APIView):
    """
    API endpoint for ar_rest01_access_viewpoint.
    """

    renderer_classes = (JSONRenderer,CustomXmlRenderer,)

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
            # return HttpResponse(
            #     [json.dumps(modified_data, ensure_ascii=False)],
            #     content_type="application/json; charset=utf-8",
            #     status=status.HTTP_200_OK,
            # )
            return Response(modified_data)
        except Exception as error:
            return HttpResponse(
                "Error occurred: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArRest01RequirementView(APIView):
    """
    API endpoint for ar_rest01_requirement.
    """

    renderer_classes = (JSONRenderer,CustomXmlRenderer,)

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
            # return HttpResponse(
            #     [json.dumps(modified_data, ensure_ascii=False)],
            #     content_type="application/json; charset=utf-8",
            #     status=status.HTTP_200_OK,
            # )
            return Response(modified_data)
        except Exception as error:
            return HttpResponse(
                "Error occurred: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArRest01PlaceView(APIView):
    """
    API endpoint for ar_rest01_place.
    """

    renderer_classes = (JSONRenderer,CustomXmlRenderer,)

    def get(self, request, format=JSON):
        try:
            data = ArRest01Place.objects.all().order_by('place_order')
            modified_data = []
            for item in data:
                place = {
                    "placeId": item.place_id,
                    "names": [],
                    "descriptions": [],
                    "placeOrderText": item.place_order,
                }

                if item.name_fi:
                    place["names"].append({ "language": "fi", "value": item.name_fi })
                if item.name_sv:
                    place["names"].append({ "language": "sv", "value": item.name_sv })
                if item.name_en:
                    place["names"].append({ "language": "en", "value": item.name_en })

                if item.description_fi:
                    place["descriptions"].append({ "language": "fi", "value": item.description_fi })
                if item.description_sv:
                    place["descriptions"].append({ "language": "sv", "value": item.description_sv })
                if item.description_en:
                    place["descriptions"].append({ "language": "en", "value": item.description_en })

                modified_data.append(place)

            return Response(modified_data)
        except Exception as error:
            return HttpResponse(
                "Error occurred: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArRest01QuestionnaireView(APIView):
    """
    API endpoint for ar_rest01_questionnaire.
    """

    renderer_classes = (JSONRenderer,CustomXmlRenderer,)

    def get(self, request, format=JSON):
        try:
            data = ArRest01Questionnaire.objects.all()
            modified_data = []
            for item in data:
                questionnaire = {
                    "id": item.id,
                    "orderText": item.order_text,
                    "structureCode": item.structure_code,
                    "color": item.color,
                    "contents": [],
                }

                if item.contents_fi:
                    questionnaire["contents"].append({ "language": "fi", "value": item.contents_fi })
                if item.contents_sv:
                    questionnaire["contents"].append({ "language": "sv", "value": item.contents_sv })
                if item.contents_en:
                    questionnaire["contents"].append({ "language": "en", "value": item.contents_en })

                modified_data.append(questionnaire)

            return Response(modified_data)
        except Exception as error:
            return HttpResponse(
                "Error occurred: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArRest01FormView(APIView):
    """
    API endpoint for ar_rest01_form.
    """

    renderer_classes = (JSONRenderer,CustomXmlRenderer,)

    def get(self, request, format=JSON):
        try:
            data = ArRest01Form.objects.all().order_by("form_id")
            modified_data = []
            for item in data:
                form = {
                    "formId": item.form_id,
                    "titles": [],
                    "descriptions": [],
                }

                if item.title_fi:
                    form["titles"].append({ "language": "fi", "value": item.title_fi })
                if item.title_sv:
                    form["titles"].append({ "language": "sv", "value": item.title_sv })
                if item.title_en:
                    form["titles"].append({ "language": "en", "value": item.title_en })

                if item.description_fi:
                    form["descriptions"].append({ "language": "fi", "value": item.description_fi })
                if item.description_sv:
                    form["descriptions"].append({ "language": "sv", "value": item.description_sv })
                if item.description_en:
                    form["descriptions"].append({ "language": "en", "value": item.description_en })

                modified_data.append(form)

            return Response(modified_data)
        except Exception as error:
            return HttpResponse(
                "Error occurred: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArRest01QuestionBlockView(APIView):
    """
    API endpoint for ar_rest01_question_block.
    """

    renderer_classes = (JSONRenderer,CustomXmlRenderer,)

    def get(self, request, format=JSON):
        try:
            data = ArRest01QuestionBlock.objects.all().order_by("question_block_order_text")
            modified_data = []
            for item in data:
                question_block = {
                    "questionBlockId": item.question_block_id,
                    "formId": item.form_id,
                    "questionBlockCode": item.question_block_code,
                    "questionBlocks": [],
                    "questionBlockOrderText": item.question_block_order_text,
                    "descriptions": [],
                    "photoUrl": item.photo_url,
                    "photoTexts": [],
                }

                if item.question_block_text_fi:
                    question_block["questionBlocks"].append({ "language": "fi", "value": item.question_block_text_fi })
                if item.question_block_text_sv:
                    question_block["questionBlocks"].append({ "language": "sv", "value": item.question_block_text_sv })
                if item.question_block_text_en:
                    question_block["questionBlocks"].append({ "language": "en", "value": item.question_block_text_en })

                if item.description_fi:
                    question_block["descriptions"].append({ "language": "fi", "value": item.description_fi })
                if item.description_sv:
                    question_block["descriptions"].append({ "language": "sv", "value": item.description_sv })
                if item.description_en:
                    question_block["descriptions"].append({ "language": "en", "value": item.description_en })

                if item.photo_text_fi:
                    question_block["photoTexts"].append({ "language": "fi", "value": item.photo_text_fi })
                if item.photo_text_sv:
                    question_block["photoTexts"].append({ "language": "sv", "value": item.photo_text_sv })
                if item.photo_text_en:
                    question_block["photoTexts"].append({ "language": "en", "value": item.photo_text_en })

                modified_data.append(question_block)

            return Response(modified_data)
        except Exception as error:
            return HttpResponse(
                "Error occurred: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArRest01QuestionView(APIView):
    """
    API endpoint for ar_rest01_question.
    """

    renderer_classes = (JSONRenderer,CustomXmlRenderer,)

    def get(self, request, format=JSON):
        try:
            data = ArRest01Question.objects.all().order_by("question_order_text")
            modified_data = []
            for item in data:
                question = {
                    "questionId": item.question_id,
                    "formId": item.form_id,
                    "questionBlockId": item.question_block_id,
                    "questionCode": item.question_code,
                    "questions": [],
                    "questionOrderText": item.question_order_text,
                    "descriptions": [],
                    "photoUrl": item.photo_url,
                    "photoTexts": [],
                }

                if item.question_text_fi:
                    question["questions"].append({ "language": "fi", "value": item.question_text_fi })
                if item.question_text_sv:
                    question["questions"].append({ "language": "sv", "value": item.question_text_sv })
                if item.question_text_en:
                    question["questions"].append({ "language": "en", "value": item.question_text_en })

                if item.description_fi:
                    question["descriptions"].append({ "language": "fi", "value": item.description_fi })
                if item.description_sv:
                    question["descriptions"].append({ "language": "sv", "value": item.description_sv })
                if item.description_en:
                    question["descriptions"].append({ "language": "en", "value": item.description_en })

                if item.photo_text_fi:
                    question["photoTexts"].append({ "language": "fi", "value": item.photo_text_fi })
                if item.photo_text_sv:
                    question["photoTexts"].append({ "language": "sv", "value": item.photo_text_sv })
                if item.photo_text_en:
                    question["photoTexts"].append({ "language": "en", "value": item.photo_text_en })

                modified_data.append(question)

            return Response(modified_data)
        except Exception as error:
            return HttpResponse(
                "Error occurred: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArRest01ChoiceView(APIView):
    """
    API endpoint for ar_rest01_choice.
    """

    renderer_classes = (JSONRenderer,CustomXmlRenderer,)

    def get(self, request, format=JSON):
        try:
            data = ArRest01Choice.objects.all().order_by("choice_order_text")
            modified_data = []
            for item in data:
                choice = {
                    "choiceId": item.choice_id,
                    "formId": item.form_id,
                    "questionBlockId": item.question_block_id,
                    "questionId": item.question_id,
                    "choices": [],
                    "choiceOrderText": item.choice_order_text,
                }

                if item.choice_text_fi:
                    choice["choices"].append({ "language": "fi", "value": item.choice_text_fi })
                if item.choice_text_sv:
                    choice["choices"].append({ "language": "sv", "value": item.choice_text_sv })
                if item.choice_text_en:
                    choice["choices"].append({ "language": "en", "value": item.choice_text_en })

                modified_data.append(choice)

            return Response(modified_data)
        except Exception as error:
            return HttpResponse(
                "Error occurred: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArRest01ServicepointView(APIView):
    renderer_classes = (JSONRenderer,CustomXmlRenderer,)

    http_method_names = [
        "delete",
        "get",
    ]

    def get(self, request, systemId=None, servicePointId=None, targetId=None, format=None):
        if servicePointId == "entrances":
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
                        "photoSource": item.photo_source_text,
                        "photoTexts": [],
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

                    if item.photo_text_fi:
                        entrance["photoTexts"].append({"language": "fi", "value": item.photo_text_fi})
                    if item.photo_text_sv:
                        entrance["photoTexts"].append({"language": "sv", "value": item.photo_text_sv})
                    if item.photo_text_en:
                        entrance["photoTexts"].append({"language": "en", "value": item.photo_text_en})

                    modified_data.append(entrance)
                # return HttpResponse(
                #     [json.dumps(modified_data, ensure_ascii=False)],
                #     content_type="application/json; charset=utf-8",
                #     status=status.HTTP_200_OK,
                # )
                return Response(modified_data)
            except Exception as error:
                return HttpResponse(
                    "Error occurred: " + str(error), status=status.HTTP_400_BAD_REQUEST
                )

        try:
            if targetId != None:
                data = ArRest01Servicepoint.objects.filter(
                    system_id=systemId, external_servicepoint_id=targetId
                )
            else:
                data = ArRest01Servicepoint.objects.filter(
                    system_id=systemId, external_servicepoint_id=servicePointId
                )

            if len(data) > 0:
                item = data[0]
                integer_map = map(int, item.entrances.split(","))

                modified_data = {
                    "systemId": str(item.system_id),
                }

                if targetId != None:
                    modified_data.update({
                        "targetId": item.external_servicepoint_id,
                    })
                else:
                    modified_data.update({
                        "servicePointId": item.external_servicepoint_id,
                    })

                modified_data.update({
                    "name": item.servicepoint_name,
                    "addressStreetName": item.address_street_name,
                    "addressNo": item.address_no,
                    "addressCity": item.address_city,
                    "locEasting": item.loc_easting,
                    "locNorthing": item.loc_northing,
                    "accessibilityPhone": item.accessibility_phone,
                    "accessibilityEmail": item.accessibility_email,
                    "accessibilityWww": item.accessibility_www,
                    "contactPersons": [],
                    "created": item.created.strftime("%Y-%m-%dT%H:%M:%S"),
                    "modified": item.modified.strftime("%Y-%m-%dT%H:%M:%S"),
                })

                if targetId == None:
                    modified_data.update({
                        "entrances": list(integer_map),
                    })

                if item.contact_person_fi:
                    modified_data["contactPersons"].append({ "language": "fi", "value": item.contact_person_fi })
                if item.contact_person_sv:
                    modified_data["contactPersons"].append({ "language": "sv", "value": item.contact_person_sv })
                if item.contact_person_en:
                    modified_data["contactPersons"].append({ "language": "en", "value": item.contact_person_en })

                # return HttpResponse(
                #     [json.dumps(modified_data, ensure_ascii=False)],
                #     content_type="application/json; charset=utf-8",
                #     status=status.HTTP_200_OK,
                # )
                return Response(modified_data)
            else:
                return HttpResponse([])
        except Exception as error:
            return HttpResponse(
                "Error occurred: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, systemId, servicePointId, format=None):
        systems = ArSystem.objects.all()
        is_in_systems = False
        for system in systems:
            if system.system_id == systemId:
                is_in_systems = True
        if not is_in_systems:
            return HttpResponse(
                "System not in AR.", status=status.HTTP_401_UNAUTHORIZED
            )

        URL = request.build_absolute_uri()
        parsed_url = urlparse(URL)
        query = parse_qs(parsed_url.query)
        keys = ["user", "validUntil", "checksum"]
        for key in keys:
            if key not in query:
                return HttpResponse(
                    "Required query parameter missing.",
                    status=status.HTTP_400_BAD_REQUEST,
                )

        user = str(query["user"][0])
        validUntil = query["validUntil"][0]
        valid_until = parser.parse(validUntil)
        now = datetime.now()
        if valid_until < now:
            return HttpResponse(
                "The request is no longer valid.", status=status.HTTP_401_UNAUTHORIZED
            )

        # TODO: Check the user??

        validUntil = str(validUntil)
        checksum = str(query["checksum"][0])
        system = ArSystem.objects.get(system_id=systemId)
        checksum_secret = getattr(system, "checksum_secret")
        # concatenation order: checksumSecret + systemId +  servicePointId + user + validUntil
        checksum_string = (
            str(checksum_secret)
            + str(systemId)
            + str(servicePointId)
            + user
            + validUntil
        )

        # TODO: If used often create function for checking checksum
        if checksum.lower() != hashlib.sha256(checksum_string.encode("ascii")).hexdigest().lower():
            return HttpResponse(
                "Checksums did not match. ", status=status.HTTP_401_UNAUTHORIZED
            )

        # Call arp_delete_entrance_data to all entrances of the servicepoint

        servicepoint = ArServicepoint.objects.get(ext_servicepoint_id=servicePointId)
        entrances = ArEntrance.objects.filter(
            servicepoint_id=servicepoint.servicepoint_id
        )
        for entrance in entrances:
            # Call arp_delete_entrance_data
            entrance_id = entrance.entrance_id
            try:
                ps_connection = psycopg2.connect(
                    user=DB_USER,
                    password=DB_PASSWORD,
                    host=DB_HOST,
                    port=DB_PORT,
                    database=DB,
                    options="-c search_path={}".format(SEARCH_PATH),
                )

                cursor = ps_connection.cursor(
                    cursor_factory=psycopg2.extras.RealDictCursor
                )

                # Call the psql function that chops the address
                cursor.execute("SELECT arp_delete_entrance_data(%s)", [entrance_id])

                # Get the returned values
                result = cursor.fetchall()
                ps_connection.commit()

            except (Exception, psycopg2.DatabaseError) as error:
                print("Error while using database function", error)
                result = str(error)
                return HttpResponse(
                    "Error deleting data using arp_delete_entrance_data" + str(error),
                    status=status.HTTP_400_BAD_REQUEST,
                )
            finally:
                # closing database connection.
                if ps_connection:
                    cursor.close()
                    ps_connection.close()
                print("PostgreSQL connection is closed")
            # If the entrance is not main entrance, delete entrance from the database.
            if entrance.is_main_entrance == "N":
                # delete entrance
                entrance.delete()

        servicepoint.is_searchable = "N"
        servicepoint.save()

        return HttpResponse(
            "Servicepoint deleted successfully.", status=status.HTTP_200_OK
        )


class ArRest01EntranceView(APIView):
    renderer_classes = (JSONRenderer,CustomXmlRenderer,)

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
                    "photoSource": item.photo_source_text,
                    "photoTexts": [],
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

                if item.photo_text_fi:
                    entrance["photoTexts"].append({"language": "fi", "value": item.photo_text_fi})
                if item.photo_text_sv:
                    entrance["photoTexts"].append({"language": "sv", "value": item.photo_text_sv})
                if item.photo_text_en:
                    entrance["photoTexts"].append({"language": "en", "value": item.photo_text_en})

                modified_data.append(entrance)
            # return HttpResponse(
            #     [json.dumps(modified_data, ensure_ascii=False)],
            #     content_type="application/json; charset=utf-8",
            #     status=status.HTTP_200_OK,
            # )
            return Response(modified_data)
        except Exception as error:
            return HttpResponse(
                "Error occurred: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArRest01AddExternalReferenceView(APIView):
    def post(self, request, systemId, servicePointId):
        # {
        # "ServicePointId":"338de29b-a5e5-47a9-a79f-80cb6c3a303b",
        # "SystemId":"ab6e2755-19a2-45b4-b5cd-484098b6c511",
        # "User":"user@tpr.fi",
        # "ValidUntil":"2018-01-30T18:08:01",
        # "Checksum":"C6FC721604E5F093B19071DD8903C5643B6BDE0EF1C8D62CBE869A7416BF9551"
        #  }
        try:
            systems = ArSystem.objects.all()
            is_in_systems = False
            for system in systems:
                if system.system_id == systemId:
                    is_in_systems = True
            if not is_in_systems:
                return HttpResponse(
                    "System not in AR.", status=status.HTTP_401_UNAUTHORIZED
                )

            data = request.data
            keys = ["ServicePointId", "SystemId", "User", "ValidUntil", "Checksum"]
            for key in keys:
                if key not in data:
                    return HttpResponse(
                        "Data does not contain required keys.",
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            external_servicepoint_id = data["ServicePointId"]
            external_system_id = data["SystemId"]
            user = data["User"]
            checksum = data["Checksum"]
            validUntil = data["ValidUntil"]

            valid_until = parser.parse(validUntil)
            now = datetime.now()
            if valid_until < now:
                return HttpResponse(
                    "The request is no longer valid.", status=status.HTTP_401_UNAUTHORIZED
                )

            internalSystem = ArSystem.objects.get(system_id = systemId)
            internalServicepoint = ArExternalServicepoint.objects.get(system = internalSystem, external_servicepoint_id = servicePointId)
            externalSystem = ArSystem.objects.get(system_id = external_system_id)
            servicepoint = ArServicepoint.objects.get(servicepoint_id = internalServicepoint.servicepoint_id)

            checksum_secret = getattr(internalSystem, "checksum_secret")
            # concatenation order: checksumSecret + systemId +  servicePointId + user + validUntil + external systemId + external servicepointId
            checksum_string = (
                str(checksum_secret)
                + str(systemId)
                + str(servicePointId)
                + str(user)
                + str(validUntil)
                + str(external_system_id)
                + str(external_servicepoint_id)
            )

            if checksum.lower() != hashlib.sha256(checksum_string.encode("ascii")).hexdigest().lower():
                return HttpResponse(
                    "Checksums did not match.",
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # Don't update the external servicepoint if it already exists, so that created and created_by values are preserved
            externalServicepointExists = ArExternalServicepoint.objects.filter(
                external_servicepoint_id = external_servicepoint_id,
                system = externalSystem,
                servicepoint = servicepoint
            ).exists()
            if externalServicepointExists:
                return HttpResponse("External servicepoint already exists.", status=status.HTTP_200_OK)

            # Insert a new external servicepoint
            ArExternalServicepoint.objects.create(
                external_servicepoint_id = external_servicepoint_id,
                system = externalSystem,
                servicepoint = servicepoint,
                created = now,
                created_by = user
            )

            return HttpResponse("External servicepoint added.", status=status.HTTP_200_OK)
        except Exception as error:
            return HttpResponse("Error occurred: " + str(error), status=status.HTTP_400_BAD_REQUEST)


class ArRest01SentenceView(APIView):
    renderer_classes = (JSONRenderer,CustomXmlRenderer,)

    def get(self, request, systemId=None, servicePointId=None, targetId=None, format=None):
        try:
            if targetId != None:
                data = ArRest01Sentence.objects.filter(
                    system_id=systemId, external_servicepoint_id=targetId
                )
            else:
                data = ArRest01Sentence.objects.filter(
                    system_id=systemId, external_servicepoint_id=servicePointId
                )

            modified_data = []
            for item in data:
                sentence = {
                    "systemId": str(item.system_id),
                }

                if targetId != None:
                    sentence.update({
                        "targetId": item.external_servicepoint_id,
                    })
                else:
                    sentence.update({
                        "servicePointId": item.external_servicepoint_id,
                        "entranceId": item.entrance_id,
                    })

                sentence.update({
                    "sentenceGroups": [],
                    "sentences": [],
                    "sentenceOrderText": item.sentence_order_text,
                })

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

            # return HttpResponse(
            #     [json.dumps(modified_data, ensure_ascii=False)],
            #     content_type="application/json; charset=utf-8",
            #     status=status.HTTP_200_OK,
            # )
            return Response(modified_data)
        except Exception as error:
            return HttpResponse(
                "Error occurred: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArRest01EntranceSentenceView(APIView):
    renderer_classes = (JSONRenderer,CustomXmlRenderer,)

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
            # return HttpResponse(
            #     [json.dumps(modified_data, ensure_ascii=False)],
            #     content_type="application/json; charset=utf-8",
            #     status=status.HTTP_200_OK,
            # )
            return Response(modified_data)
        except Exception as error:
            return HttpResponse(
                "Error occurred: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArRest01ShortageView(APIView):
    renderer_classes = (JSONRenderer,CustomXmlRenderer,)

    def get(
        self, request, systemId=None, servicePointId=None, targetId=None, viewPointId=None, format=None
    ):
        try:
            if targetId != None and viewPointId != None:
                data = ArRest01Shortage.objects.filter(
                    system_id=systemId,
                    external_servicepoint_id=targetId,
                    viewpoint_id=viewPointId,
                )
            elif viewPointId != None:
                data = ArRest01Shortage.objects.filter(
                    system_id=systemId,
                    external_servicepoint_id=servicePointId,
                    viewpoint_id=viewPointId,
                )
            elif targetId != None:
                data = ArRest01Shortage.objects.filter(
                    system_id=systemId, external_servicepoint_id=targetId
                )
            elif servicePointId != None:
                data = ArRest01Shortage.objects.filter(
                    system_id=systemId, external_servicepoint_id=servicePointId
                )
            else:
                data = ArRest01Shortage.objects.filter(system_id=systemId)

            if len(data) > 0:
                modified_data = []
                for item in data:
                    shortage = {
                        "systemId": str(item.system_id),
                    }

                    if targetId != None or "/targets/" in request.path:
                        shortage.update({
                            "targetId": item.external_servicepoint_id,
                        })
                    else:
                        shortage.update({
                            "servicePointId": item.external_servicepoint_id,
                        })

                    shortage.update({
                        "viewpointId": item.viewpoint_id,
                        "requirementId": item.requirement_id,
                        "shortages": [],
                    })

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

                # return HttpResponse(
                #     [json.dumps(modified_data, ensure_ascii=False)],
                #     content_type="application/json; charset=utf-8",
                #     status=status.HTTP_200_OK,
                # )
                return Response(modified_data)
        except Exception as error:
            return HttpResponse(
                "Error occurred: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArSystemServicepointsView(APIView):
    renderer_classes = (JSONRenderer,CustomXmlRenderer,)

    def get(self, request, systemId=None, format=None):
        try:
            # TODO: external_servicepoint_id or servicepoint_id
            data = ArRest01Servicepoint.objects.filter(system_id=systemId)

            modified_data = []
            for item in data:
                integer_map = map(int, item.entrances.split(","))
                servicepoint = {
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
                    "contactPersons": [],
                    "created": item.created.strftime("%Y-%m-%dT%H:%M:%S"),
                    "modified": item.modified.strftime("%Y-%m-%dT%H:%M:%S"),
                    "entrances": list(integer_map),
                }

                if item.contact_person_fi:
                    servicepoint["contactPersons"].append({ "language": "fi", "value": item.contact_person_fi })
                if item.contact_person_sv:
                    servicepoint["contactPersons"].append({ "language": "sv", "value": item.contact_person_sv })
                if item.contact_person_en:
                    servicepoint["contactPersons"].append({ "language": "en", "value": item.contact_person_en })

                modified_data.append(servicepoint)

            # return HttpResponse(
            #     [json.dumps(modified_data, ensure_ascii=False)],
            #     content_type="application/json; charset=utf-8",
            #     status=status.HTTP_200_OK,
            # )
            return Response(modified_data)
        except Exception as error:
            return HttpResponse(
                "Error occurred: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArSystemEntrancesView(APIView):
    renderer_classes = (JSONRenderer,CustomXmlRenderer,)

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
                    "photoSource": item.photo_source_text,
                    "photoTexts": [],
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

                if item.photo_text_fi:
                    entrance["photoTexts"].append({"language": "fi", "value": item.photo_text_fi})
                if item.photo_text_sv:
                    entrance["photoTexts"].append({"language": "sv", "value": item.photo_text_sv})
                if item.photo_text_en:
                    entrance["photoTexts"].append({"language": "en", "value": item.photo_text_en})

                modified_data.append(entrance)
            # return HttpResponse(
            #     [json.dumps(modified_data, ensure_ascii=False)],
            #     content_type="application/json; charset=utf-8",
            #     status=status.HTTP_200_OK,
            # )
            return Response(modified_data)
        except Exception as error:
            return HttpResponse(
                "Error occurred: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArSystemSentencesView(APIView):
    renderer_classes = (JSONRenderer,CustomXmlRenderer,)

    def get(self, request, systemId=None, format=None):
        try:
            data = ArRest01Sentence.objects.filter(system_id=systemId)
            modified_data = []
            for item in data:
                sentence = {
                    "systemId": str(item.system_id),
                }

                if "/targets/" in request.path:
                    sentence.update({
                        "targetId": item.external_servicepoint_id,
                    })
                else:
                    sentence.update({
                        "servicePointId": item.external_servicepoint_id,
                        "entranceId": item.entrance_id,
                    })

                sentence.update({
                    "sentenceGroups": [],
                    "sentences": [],
                    "sentenceOrderText": item.sentence_order_text,
                })

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

            # return HttpResponse(
            #     [json.dumps(modified_data, ensure_ascii=False)],
            #     content_type="application/json; charset=utf-8",
            #     status=status.HTTP_200_OK,
            # )
            return Response(modified_data)
        except Exception as error:
            return HttpResponse(
                "Error occurred: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArRest01ServicepointAccessibilityViewSet(APIView):
    renderer_classes = (JSONRenderer,CustomXmlRenderer,)

    def get(
        self, request, systemId=None, servicePointId=None, targetId=None, entranceId=None, format=None
    ):
        try:
            if targetId != None:
                data = ArRest01ServicepointAccessibility.objects.filter(
                    system_id=systemId, external_servicepoint_id=targetId
                )
            elif servicePointId != None:
                data = ArRest01ServicepointAccessibility.objects.filter(
                    system_id=systemId, external_servicepoint_id=servicePointId
                )
            else:
                data = ArRest01ServicepointAccessibility.objects.filter(
                    system_id=systemId
                )

            modified_data = []
            for item in data:
                property = {
                    "systemId": str(item.system_id),
                }

                if targetId != None or "/targets/" in request.path:
                    property.update({
                        "targetId": item.external_servicepoint_id,
                    })
                else:
                    property.update({
                        "servicePointId": item.external_servicepoint_id,
                    })

                property.update({
                    "variableId": item.variable_id,
                    "variableName": item.variable_name,
                    "value": item.rest_value,
                })

                modified_data.append(property)

            # return HttpResponse(
            #     [json.dumps(modified_data, ensure_ascii=False)],
            #     content_type="application/json; charset=utf-8",
            #     status=status.HTTP_200_OK,
            # )
            return Response(modified_data)
        except Exception as error:
            return HttpResponse(
                "Error occurred: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArRest01EntranceAccessibilityViewSet(APIView):
    renderer_classes = (JSONRenderer,CustomXmlRenderer,)

    def get(
        self, request, systemId=None, servicePointId=None, entranceId=None, format=None
    ):
        try:
            if entranceId != None:
                data = ArRest01EntranceAccessibility.objects.filter(
                    system_id=systemId,
                    external_servicepoint_id=servicePointId,
                    entrance_id=entranceId,
                )
            elif servicePointId != None:
                data = ArRest01EntranceAccessibility.objects.filter(
                    system_id=systemId, external_servicepoint_id=servicePointId
                )
            else:
                data = ArRest01EntranceAccessibility.objects.filter(
                    system_id=systemId,
                )
            modified_data = []
            for item in data:
                property = {
                    "systemId": str(item.system_id),
                    "servicePointId": item.external_servicepoint_id,
                    "entranceId": item.entrance_id,
                    "variableId": item.variable_id,
                    "variableName": item.variable_name,
                    "value": item.rest_value,
                }
                modified_data.append(property)
            # return HttpResponse(
            #     [json.dumps(modified_data, ensure_ascii=False)],
            #     content_type="application/json; charset=utf-8",
            #     status=status.HTTP_200_OK,
            # )
            return Response(modified_data)
        except Exception as error:
            return HttpResponse(
                "Error occurred: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArRest01EntranceChoiceViewSet(APIView):
    renderer_classes = (JSONRenderer,CustomXmlRenderer,)

    def get(
        self, request, systemId=None, servicePointId=None, targetId=None, entranceId=None, format=None
    ):
        try:
            if targetId != None and entranceId != None:
                data = ArRest01EntranceChoice.objects.filter(
                    system_id=systemId,
                    external_servicepoint_id=targetId,
                    entrance_id=entranceId,
                ).order_by('question_order_text')
            elif entranceId != None:
                data = ArRest01EntranceChoice.objects.filter(
                    system_id=systemId,
                    external_servicepoint_id=servicePointId,
                    entrance_id=entranceId,
                ).order_by('question_order_text')
            elif targetId != None:
                data = ArRest01EntranceChoice.objects.filter(
                    system_id=systemId, external_servicepoint_id=targetId
                ).order_by('question_order_text')
            elif servicePointId != None:
                data = ArRest01EntranceChoice.objects.filter(
                    system_id=systemId, external_servicepoint_id=servicePointId
                ).order_by('question_order_text')
            else:
                data = ArRest01EntranceChoice.objects.filter(
                    system_id=systemId,
                ).order_by('question_order_text')

            modified_data = []
            for item in data:
                choice = {
                    "systemId": str(item.system_id),
                }

                if targetId != None or "/targets/" in request.path:
                    choice.update({
                        "targetId": item.external_servicepoint_id,
                    })
                else:
                    choice.update({
                        "servicePointId": item.external_servicepoint_id,
                        "entranceId": item.entrance_id,
                    })

                choice.update({
                    "questionId": item.question_id,
                    "questionOrderText": item.question_order_text,
                    "choiceId": item.question_choice_id,
                    "choices": [],
                })

                if item.question_choice_text_fi:
                    choice["choices"].append({ "language": "fi", "value": item.question_choice_text_fi })
                if item.question_choice_text_sv:
                    choice["choices"].append({ "language": "sv", "value": item.question_choice_text_sv })
                if item.question_choice_text_en:
                    choice["choices"].append({ "language": "en", "value": item.question_choice_text_en })

                modified_data.append(choice)

            return Response(modified_data)
        except Exception as error:
            return HttpResponse(
                "Error occurred: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArRest01EntrancePlaceViewSet(APIView):
    renderer_classes = (JSONRenderer,CustomXmlRenderer,)

    def get(
        self, request, systemId=None, servicePointId=None, targetId=None, entranceId=None, format=None
    ):
        try:
            if targetId != None and entranceId != None:
                data = ArRest01EntrancePlace.objects.filter(
                    system_id=systemId,
                    external_servicepoint_id=targetId,
                    entrance_id=entranceId,
                ).order_by('place_order_text')
            elif entranceId != None:
                data = ArRest01EntrancePlace.objects.filter(
                    system_id=systemId,
                    external_servicepoint_id=servicePointId,
                    entrance_id=entranceId,
                ).order_by('place_order_text')
            elif targetId != None:
                data = ArRest01EntrancePlace.objects.filter(
                    system_id=systemId, external_servicepoint_id=targetId
                ).order_by('place_order_text')
            elif servicePointId != None:
                data = ArRest01EntrancePlace.objects.filter(
                    system_id=systemId, external_servicepoint_id=servicePointId
                ).order_by('place_order_text')
            else:
                data = ArRest01EntrancePlace.objects.filter(
                    system_id=systemId,
                ).order_by('place_order_text')

            modified_data = []
            for item in data:
                place = {
                    "systemId": str(item.system_id),
                }

                if targetId != None or "/targets/" in request.path:
                    place.update({
                        "targetId": item.external_servicepoint_id,
                    })
                else:
                    place.update({
                        "servicePointId": item.external_servicepoint_id,
                        "entranceId": item.entrance_id,
                    })

                place.update({
                    "headings": [],
                    "sentenceGroups": [],
                    "placeId": item.place_id,
                    "place": [],
                    "placeOrderText": item.place_order_text,
                    "locEasting": item.loc_easting,
                    "locNorthing": item.loc_northing,
                    "locationTexts": [],
                    "photoUrl": item.photo_url,
                    "photoSource": item.photo_source_text,
                    "photoTexts": [],
                })

                if item.heading_fi:
                    place["headings"].append({ "language": "fi", "value": item.heading_fi })
                if item.heading_sv:
                    place["headings"].append({ "language": "sv", "value": item.heading_sv })
                if item.heading_en:
                    place["headings"].append({ "language": "en", "value": item.heading_en })

                if item.sentence_group_fi:
                    place["sentenceGroups"].append({ "language": "fi", "value": item.sentence_group_fi })
                if item.sentence_group_sv:
                    place["sentenceGroups"].append({ "language": "sv", "value": item.sentence_group_sv })
                if item.sentence_group_en:
                    place["sentenceGroups"].append({ "language": "en", "value": item.sentence_group_en })

                if item.place_name_fi:
                    place["place"].append({ "language": "fi", "value": item.place_name_fi })
                if item.place_name_sv:
                    place["place"].append({ "language": "sv", "value": item.place_name_sv })
                if item.place_name_en:
                    place["place"].append({ "language": "en", "value": item.place_name_en })

                if item.location_text_fi:
                    place["locationTexts"].append({ "language": "fi", "value": item.location_text_fi })
                if item.location_text_sv:
                    place["locationTexts"].append({ "language": "sv", "value": item.location_text_sv })
                if item.location_text_en:
                    place["locationTexts"].append({ "language": "en", "value": item.location_text_en })

                if item.photo_text_fi:
                    place["photoTexts"].append({ "language": "fi", "value": item.photo_text_fi })
                if item.photo_text_sv:
                    place["photoTexts"].append({ "language": "sv", "value": item.photo_text_sv })
                if item.photo_text_en:
                    place["photoTexts"].append({ "language": "en", "value": item.photo_text_en })

                modified_data.append(place)

            return Response(modified_data)
        except Exception as error:
            return HttpResponse(
                "Error occurred: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArRest01SummaryViewSet(APIView):
    renderer_classes = (JSONRenderer,CustomXmlRenderer,)

    def get(
        self,
        request,
        systemId=None,
        servicePointId=None,
        targetId=None,
        entranceId=None,
        viewPointId=None,
        format=None,
    ):
        try:
            if targetId != None and viewPointId != None:
                data = ArRest01Summary.objects.filter(
                    system_id=systemId,
                    external_servicepoint_id=targetId,
                    viewpoint_id=viewPointId,
                )
            elif viewPointId != None:
                data = ArRest01Summary.objects.filter(
                    system_id=systemId,
                    external_servicepoint_id=servicePointId,
                    viewpoint_id=viewPointId,
                )
            elif targetId != None:
                data = ArRest01Summary.objects.filter(
                    system_id=systemId, external_servicepoint_id=targetId
                )
            elif servicePointId != None:
                data = ArRest01Summary.objects.filter(
                    system_id=systemId, external_servicepoint_id=servicePointId
                )
            else:
                data = ArRest01Summary.objects.filter(
                    system_id=systemId,
                )

            modified_data = []
            for item in data:
                property = {
                    "systemId": str(item.system_id),
                }

                if targetId != None or "/targets/" in request.path:
                    property.update({
                        "targetId": item.external_servicepoint_id,
                    })
                else:
                    property.update({
                        "servicePointId": item.external_servicepoint_id,
                    })

                property.update({
                    "viewpointId": item.viewpoint_id,
                    "isAccessible": item.is_accessible,
                    "shortageCount": item.shortage_count,
                })

                modified_data.append(property)

            # return HttpResponse(
            #     [json.dumps(modified_data, ensure_ascii=False)],
            #     content_type="application/json; charset=utf-8",
            #     status=status.HTTP_200_OK,
            # )
            return Response(modified_data)
        except Exception as error:
            return HttpResponse(
                "Error occurred: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArRest01ReportshortageViewSet(APIView):
    renderer_classes = (JSONRenderer,CustomXmlRenderer,)

    def get(
        self,
        request,
        systemId=None,
        servicePointId=None,
        targetId=None,
        entranceId=None,
        viewPointId=None,
        format=None,
    ):
        try:
            if targetId != None:
                data = ArRest01Reportshortage.objects.filter(
                    system_id=systemId, external_servicepoint_id=targetId
                )
            elif servicePointId != None:
                data = ArRest01Reportshortage.objects.filter(
                    system_id=systemId, external_servicepoint_id=servicePointId
                )
            else:
                data = ArRest01Reportshortage.objects.filter(
                    system_id=systemId,
                )

            modified_data = []
            for item in data:
                property = {
                    "systemId": str(item.system_id),
                }

                if targetId != None or "/targets/" in request.path:
                    property.update({
                        "targetId": item.external_servicepoint_id,
                    })
                else:
                    property.update({
                        "servicePointId": item.external_servicepoint_id,
                    })

                property.update({
                    "viewpointId": item.viewpoint_id,
                    "isIndoorServicepoint": item.is_indoor_servicepoint == "Y",
                    "evaluationZone": item.evaluation_zone,
                    "easyToFix": item.easy_to_fix == "Y",
                    "requirementId": item.requirement_id,
                    "requirementText": item.requirement_text,
                    "explanationWhyNot": item.explanation_why_not,
                    "shortages": [],
                })

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

            # return HttpResponse(
            #     [json.dumps(modified_data, ensure_ascii=False)],
            #     content_type="application/json; charset=utf-8",
            #     status=status.HTTP_200_OK,
            # )
            return Response(modified_data)

        except Exception as error:
            return HttpResponse(
                "Error occurred: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArRest01ReportsummaryViewSet(APIView):
    renderer_classes = (JSONRenderer,CustomXmlRenderer,)

    def get(
        self,
        request,
        systemId=None,
        servicePointId=None,
        targetId=None,
        entranceId=None,
        viewPointId=None,
        format=None,
    ):
        try:
            if targetId != None:
                data = ArRest01Reportsummary.objects.filter(
                    system_id=systemId, external_servicepoint_id=targetId
                )
            elif servicePointId != None:
                data = ArRest01Reportsummary.objects.filter(
                    system_id=systemId, external_servicepoint_id=servicePointId
                )
            else:
                data = ArRest01Reportsummary.objects.filter(
                    system_id=systemId,
                )

            modified_data = []
            for item in data:
                property = {
                    "systemId": str(item.system_id),
                }

                if targetId != None or "/targets/" in request.path:
                    property.update({
                        "targetId": item.external_servicepoint_id,
                    })
                else:
                    property.update({
                        "servicePointId": item.external_servicepoint_id,
                    })

                property.update({
                    "isAccessible": item.is_accessible,
                    "shortageCount": item.shortage_count,
                    "shortageCountEasyToFix": item.shortage_count_easy_to_fix,
                    "wheelIsAccessible": item.wheel_is_accessible,
                    "wheelShortageCount": item.wheel_shortage_count,
                    "wheelShortageCountEasyToFix": item.wheel_shortage_count_easy_to_fix,
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
                })

                modified_data.append(property)

            # return HttpResponse(
            #     [json.dumps(modified_data, ensure_ascii=False)],
            #     content_type="application/json; charset=utf-8",
            #     status=status.HTTP_200_OK,
            # )
            return Response(modified_data)

        except Exception as error:
            return HttpResponse(
                "Error occurred: " + str(error), status=status.HTTP_400_BAD_REQUEST
            )


class ArBackendEntranceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar backend entrance.
    """

    queryset = ArBackendEntrance.objects.all()
    serializer_class = ArBackendEntranceSerializer
    pagination_class = None
    filter_fields = ("entrance_id", "log_id", "servicepoint_id", "form_submitted")
    permission_classes = [
        TokenPermission,
    ]


class ArBackendServicepointViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar backend servicepoint.
    """

    queryset = ArBackendServicepoint.objects.all()
    serializer_class = ArBackendServicepointSerializer
    pagination_class = None
    filter_fields = (
        "servicepoint_id",
        "log_id",
        "main_entrance_id",
        "form_submitted",
    )
    permission_classes = [
        TokenPermission,
    ]


class ArBackendExternalServicepointViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ar backend external servicepoint.
    """

    queryset = ArBackendExternalServicepoint.objects.all()
    serializer_class = ArBackendExternalServicepointSerializer
    pagination_class = None
    filter_fields = (
        "external_servicepoint_id",
    )
    permission_classes = [
        TokenPermission,
    ]


class ArBackendQuestionBlockFieldViewSet(viewsets.ModelViewSet):
    """ """

    queryset = ArBackendQuestionBlockField.objects.all()
    serializer_class = ArBackendQuestionBlockFieldSerializer
    pagination_class = None
    filter_fields = (
        "question_block_id",
        "form_id",
        "language_id",
        "question_block_field_id",
    )
    permission_classes = [
        TokenPermission,
    ]


class ArBackendEntranceChoiceViewSet(viewsets.ModelViewSet):
    queryset = ArBackendEntranceChoice.objects.all()
    serializer_class = ArBackendEntranceChoiceSerializer
    pagination_class = None
    filter_fields = (
        "entrance_id",
        "log_id",
        "language_id",
        "sentence_group_id",
        "question_block_id",
        "question_id",
        "question_choice_id",
        "form_submitted",
    )
    permission_classes = [
        TokenPermission,
    ]


class ArBackendEntrancePlaceViewSet(viewsets.ModelViewSet):
    queryset = ArBackendEntrancePlace.objects.all()
    serializer_class = ArBackendEntrancePlaceSerializer
    pagination_class = None
    filter_fields = (
        "log_id",
        "entrance_id",
        "question_block_id",
        "place_id",
        "box_id",
        "form_submitted",
    )
    permission_classes = [
        TokenPermission,
    ]


class ArBackendEntranceSentenceViewSet(viewsets.ModelViewSet):
    queryset = ArBackendEntranceSentence.objects.all()
    serializer_class = ArBackendEntranceSentenceSerializer
    pagination_class = None
    filter_fields = (
        "entrance_id",
        "form_submitted",
        "log_id",
        "language_id",
        "sentence_group_id",
        "sentence_id",
        "parent_sentence_id",
    )
    permission_classes = [
        TokenPermission,
    ]


class ArBackendPlaceViewSet(viewsets.ModelViewSet):
    queryset = ArBackendPlace.objects.all()
    serializer_class = ArBackendPlaceSerializer
    pagination_class = None
    permission_classes = [
        TokenPermission,
    ]
    filter_fields = (
        "place_id",
        "language_id",
    )


class ArBackendCopyableEntranceViewSet(viewsets.ModelViewSet):
    queryset = ArBackendCopyableEntrance.objects.all()
    serializer_class = ArBackendCopyableEntranceSerializer
    pagination_class = None
    filter_fields = (
        "entrance_id",
    )
    permission_classes = [
        TokenPermission,
    ]


class ArBackendEntranceSentenceGroupViewSet(viewsets.ModelViewSet):
    queryset = ArBackendEntranceSentenceGroup.objects.all()
    serializer_class = ArBackendEntranceSentenceGroupSerializer
    pagination_class = None
    filter_fields = (
        "servicepoint_id",
        "entrance_id",
    )
    permission_classes = [
        TokenPermission,
    ]


class ArXPlaceAnswerViewSet(viewsets.ModelViewSet):
    queryset = ArXPlaceAnswer.objects.all()
    serializer_class = ArXPlaceAnswerSerializer
    pagination_class = None
    permission_classes = [
        TokenPermission,
    ]


class ArXPlaceAnswerBoxViewSet(viewsets.ModelViewSet):
    queryset = ArXPlaceAnswerBox.objects.all()
    serializer_class = ArXPlaceAnswerBoxSerializer
    pagination_class = None
    permission_classes = [
        TokenPermission,
    ]

    @action(detail=True, methods=["DELETE"], url_path="delete_box_txts")
    def delete_box_txts(self, request, *args, **kwargs):
        try:
            answer_box = self.get_object()
            box_id = getattr(answer_box, "box_id")
            if box_id == None:
                return Response(
                    "Deletion failed.",
                    status=status.HTTP_400_BAD_REQUEST,
                )

            instances = ArXPlaceAnswerBoxTxt.objects.filter(box_id=box_id)
            instances.delete()
            return Response(
                "ArXPlaceAnswerBoxTxt with box_id=" + str(box_id) + " deleted.",
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            return HttpResponse("Deletion failed.", status=status.HTTP_400_BAD_REQUEST)


class ArXPlaceAnswerBoxTxtViewSet(viewsets.ModelViewSet):
    queryset = ArXPlaceAnswerBoxTxt.objects.all()
    serializer_class = ArXPlaceAnswerBoxTxtSerializer
    pagination_class = None
    permission_classes = [
        TokenPermission,
    ]

    def delete(self, request, *args, **kwargs):
        if request.method == "DELETE":
            params = QueryDict(request.params)
            box_id = request.POST.get("box_id", None)
            if box_id == None:
                return Response(
                    params,
                    status=status.HTTP_400_BAD_REQUEST,
                )

            instances = ArXPlaceAnswerBoxTxt.objects.filter(box_id=box_id)
            instances.delete()
            return Response(
                "ArXPlaceAnswerBoxTxt with box_id=" + box_id + " deleted.",
                status=status.HTTP_204_NO_CONTENT,
            )


class ArXQuestionBlockAnswerCmtViewSet(viewsets.ModelViewSet):
    queryset = ArXQuestionBlockAnswerCmt.objects.all()
    serializer_class = ArXQuestionBlockAnswerCmtSerializer
    pagination_class = None
    filter_fields = (
        "question_block_id",
    )
    permission_classes = [
        TokenPermission,
    ]

    def get_queryset(self):
        if self.request.method == "GET":
            queryset = ArXQuestionBlockAnswerCmt.objects.all()
            entrance_id = self.request.GET.get("entrance_id", None)
            form_submitted = self.request.GET.get("form_submitted", None)
            if entrance_id is not None:
                if form_submitted is not None:
                    logs = ArXAnswerLog.objects.all().filter(entrance_id=entrance_id, form_submitted=form_submitted)
                else:
                    logs = ArXAnswerLog.objects.all().filter(entrance_id=entrance_id)
                log_ids = [log.log_id for log in logs]
                queryset = queryset.filter(log_id__in=log_ids)
            return queryset


class ArXQuestionBlockAnswerViewSet(viewsets.ModelViewSet):
    queryset = ArXQuestionBlockAnswer.objects.all()
    serializer_class = ArXQuestionBlockAnswerSerializer
    pagination_class = None
    permission_classes = [
        TokenPermission,
    ]


class ArXQuestionBlockAnswerTxtViewSet(viewsets.ModelViewSet):
    queryset = ArXQuestionBlockAnswerTxt.objects.all()
    serializer_class = ArXQuestionBlockAnswerTxtSerializer
    pagination_class = None
    permission_classes = [
        TokenPermission,
    ]


class AzureUploader(APIView):
    permission_classes = [
        TokenPermission,
    ]

    def post(self, request, servicepoint_id=None):
        try:
            # file = request.FILES["file"]
            encoded_file = request.data["file"].split(",")[1]
            file = base64.b64decode(encoded_file)
            file_upload_name = str(uuid.uuid4()) + ".jpg"
            blob_service_client = create_blob_client(servicepoint_id, file_upload_name)
            my_content_settings = ContentSettings(
                content_type="image/jpg",
                content_encoding=None,
                content_language=None,
                content_disposition=None,
                cache_control=None,
                content_md5=None,
            )
            blob_service_client.upload_blob(file, content_settings=my_content_settings)
            url = (
                AZURE_URL
                + PUBLIC_AZURE_CONTAINER
                + "/"
                + servicepoint_id
                + "/"
                + file_upload_name
            )
            return HttpResponse(
                [
                    json.dumps(
                        {
                            "status": "success",
                            "uploaded_file_name": file_upload_name,
                            "url": url,
                        }
                    )
                ],
                status=201,
            )
        except Exception as e:
            return HttpResponse(e)

    def delete(self, request, servicepoint_id=None, format=None):
        try:
            file_name = request.data["image_name"]
            blob_service_client = create_blob_client(servicepoint_id, file_name)
            blob_service_client.delete_blob()
            return HttpResponse(
                [
                    json.dumps(
                        {
                            "status": "success",
                            "deleted_file_name": file_name,
                        }
                    )
                ],
                status=201,
            )
        except Exception as e:
            return HttpResponse(e)


class ArpDeletePlaceFromAnswer(APIView):
    """
    API endpoint for arp_delete_place_from_answer(v_log_id_in integer, v_place_id_in integer)
    """

    permission_classes = [
        TokenPermission,
    ]

    def get(self, request, format=None):
        # Placeholder endpoint for get request
        return Response(
            """Get called for a function call that requires parameters and a post"""
        )

    def delete(self, request, format=None):
        # Post request to call the arp_delete_place_from_answer function in the psql database
        log_id = ""
        place_id = ""

        try:
            log_id = int(request.data["log_id"])
            place_id = int(request.data["place_id"])
        except:
            print("Required data missing")
            return Response(
                "Error while using database function",
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            ps_connection = psycopg2.connect(
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT,
                database=DB,
                options="-c search_path={}".format(SEARCH_PATH),
            )

            cursor = ps_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            # Call the psql function that chops the address
            cursor.execute(
                "SELECT arp_delete_place_from_answer(%s, %s)", (log_id, place_id)
            )

            # Get the returned values
            result = cursor.fetchall()
            ps_connection.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while using database function", error)
            return Response(
                "Error while using database function %s",
                error,
                status=status.HTTP_400_BAD_REQUEST,
            )
        finally:
            # closing database connection.
            if ps_connection:
                cursor.close()
                ps_connection.close()
                print("PostgreSQL connection is closed")
            return HttpResponse(
                [
                    json.dumps(
                        {
                            "status": result,
                            "deleted_place_id": place_id,
                            "deleted_log_id": log_id,
                        }
                    )
                ],
                status=201,
            )


class PdfReportView(ListView):
    template_name = "pdf.html"
    queryset = ArBackendPdf.objects.none()
    serializer_class = ArBackendPdfSerializer
    pagination_class = None
    permission_classes = [
        TokenPermission,
    ]

    def get_context_data(self, **kwargs):
        # Get the target id from the url path
        # Target id examples:
        #   tpr:5304
        #   ptv:7b5f2481-a80f-4773-8a95-bb7a43fc7a21
        targetId = self.kwargs["target_id"]

        # Get any specified query string values
        purposeCode = self.request.GET.get("purpose", "LAST_QUESTION_ANSWER")
        date = self.request.GET.get("date", None)
        languageId = self.request.GET.get("language", "1")

        # Translate the language id to a code
        languageCode = ""
        if languageId == "1":
            languageCode = "fi"
        elif languageId == "2":
            languageCode = "sv"
        elif languageId == "3":
            languageCode = "en"
        elif languageId == "fi":
            languageId = "1"
            languageCode = "fi"
        elif languageId == "sv":
            languageId = "2"
            languageCode = "sv"
        elif languageId == "en":
            languageId = "3"
            languageCode = "en"

        # Get the internal servicepoint id corresponding to the target id
        backendExternalServicepoint = ArBackendExternalServicepoint.objects.get(external_servicepoint_id = targetId)
        servicepointId = backendExternalServicepoint.servicepoint_id
        logIds = None

        # Get the logos to show in the footer, with the format 'helsinki+avi+okm'
        logo = backendExternalServicepoint.logo

        if purposeCode == "ARCHIVED_QUESTION_ANSWER" and date != None:
            # Get the logs ids for the specified date
            try:
                ps_connection = psycopg2.connect(
                    user=DB_USER,
                    password=DB_PASSWORD,
                    host=DB_HOST,
                    port=DB_PORT,
                    database=DB,
                    options="-c search_path={}".format(SEARCH_PATH),
                )

                cursor = ps_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

                # Call the psql function that gets the log ids
                cursor.execute("SELECT tf2_servicepoint_logids_before_date(%s, %s)", [servicepointId, date])

                # Get the returned values
                result = cursor.fetchall()
                print("result " + str(result))
                result_string = result[0]["tf2_servicepoint_logids_before_date"]
                logIds = result_string.split(",")

            except (Exception, psycopg2.Error) as error:
                print("Error while using database function tf2_servicepoint_logids_before_date", error)
            finally:
                # Close the database connection
                if ps_connection:
                    cursor.close()
                    ps_connection.close()
                    print("PostgreSQL connection is closed")

        # Get the full url to display as a link
        link = self.request.build_absolute_uri(PDF_BASE_URL + "api/pdfview/" + str(targetId) + "/?purpose=" + str(purposeCode) + "&date=" + str(date) + "&language=" + str(languageId))

        # Make an array of the logo images to display in the footer, using the static base url
        logoBase = self.request.build_absolute_uri(PDF_BASE_URL + "static/img/")
        logos = []
        if logo != None:
            logos = logo.split("+")
            logos = map(lambda item: item + "_" + languageCode + ".png", logos)

        # Store the data for the pdf template
        context = super().get_context_data(**kwargs)
        context["purpose"] = purposeCode
        context["target"] = targetId
        context["date"] = date
        context["link"] = link
        context["language_code"] = languageCode
        context["logo_base"] = logoBase
        context["logos"] = logos

        if logIds != None:
            context["data"] = ArBackendPdf.objects.filter(purpose_code = purposeCode, language_id = languageId, servicepoint_id = servicepointId, log_id__in = logIds)
        else:
            context["data"] = ArBackendPdf.objects.filter(purpose_code = purposeCode, language_id = languageId, servicepoint_id = servicepointId)

        return context


class PdfView(WeasyTemplateResponseMixin, PdfReportView):
    # The stylesheet is stored in accessibility/static/css
    pdf_stylesheets = [
        conf_settings.STATIC_ROOT + "css/pdf.css",
    ]


class PdfDownloadView(WeasyTemplateResponseMixin, PdfReportView):
    # Dynamically generate filename
    def get_pdf_filename(self):
        return "esteettömyys-{at}.pdf".format(
            at=timezone.now().strftime("%Y%m%d-%H%M"),
        )

    pdf_stylesheets = [
        conf_settings.STATIC_ROOT + "css/pdf.css",
    ]
