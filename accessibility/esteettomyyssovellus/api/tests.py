import hashlib
import inspect
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers
from rest_framework.test import APIClient

from . import serializers as app_serializers
from . import views
from .renderers import CustomXmlRenderer


class UpgradeCompatibilityTests(SimpleTestCase):
    """Exercise upgrade-sensitive behavior without querying any database."""

    def test_model_serializers_initialize(self):
        checked = 0
        for name, serializer in inspect.getmembers(
            app_serializers, inspect.isclass
        ):
            if (
                serializer.__module__ == app_serializers.__name__
                and issubclass(serializer, serializers.ModelSerializer)
            ):
                with self.subTest(serializer=name):
                    self.assertTrue(serializer().fields)
                checked += 1
        self.assertGreater(checked, 0)

    def test_viewset_filters_are_preserved(self):
        checked = 0
        for name, view in inspect.getmembers(views, inspect.isclass):
            if view.__module__ != views.__name__ or not hasattr(
                view, "queryset"
            ):
                continue
            with self.subTest(view=name):
                self.assertFalse(
                    hasattr(view, "filter_fields"),
                    "Use filterset_fields; filter_fields is unsupported.",
                )
                if not hasattr(view, "filterset_fields"):
                    continue
                filterset = DjangoFilterBackend().get_filterset_class(
                    view(), view.queryset
                )
                self.assertIsNotNone(filterset)
                self.assertEqual(
                    set(filterset.base_filters), set(view.filterset_fields)
                )
                checked += 1
        self.assertGreater(checked, 0)

    @patch.object(views, "DEBUG", False)
    @patch.object(views, "API_TOKEN", "upgrade-test-token")
    def test_token_header_allows_valid_and_rejects_missing_or_invalid(self):
        client = APIClient()
        path = "/api/users/"
        self.assertEqual(client.options(path).status_code, 403)
        self.assertEqual(
            client.options(path, HTTP_AUTHORIZATION="invalid").status_code, 403
        )
        token = hashlib.sha256(views.API_TOKEN.encode("ascii")).hexdigest()
        self.assertEqual(
            client.options(path, HTTP_AUTHORIZATION=token).status_code, 200
        )

    def test_api_root_and_cors(self):
        response = APIClient().get(
            "/api/",
            HTTP_ORIGIN="https://asiointi.hel.fi",
            HTTP_ACCEPT="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data)
        self.assertEqual(
            response.headers["access-control-allow-origin"],
            "https://asiointi.hel.fi",
        )

    def test_custom_xml_renderer(self):
        xml = CustomXmlRenderer().render(
            {"names": ["ö & <test>"], "enabled": True}
        )
        if isinstance(xml, bytes):
            xml = xml.decode("utf-8")
        self.assertIn("&amp;", xml)
        self.assertIn("&lt;test&gt;", xml)
        self.assertIn("true", xml)

    def test_pdf_views_render_with_application_templates_and_stylesheet(self):
        request = RequestFactory().get("/api/pdfview/upgrade-test/")
        context = {
            "language_code": "fi",
            "link": "http://testserver/upgrade-test/",
            "logos": [],
            "data": [
                {
                    "row_format": "MAIN_TITLE",
                    "plain_text": "Esteettömyys – upgrade test",
                },
                {
                    "row_format": "ROW",
                    "plain_text": "Entrance",
                    "bold_text": "Accessible",
                },
            ],
        }
        for view_class in (views.PdfView, views.PdfDownloadView):
            with self.subTest(view=view_class.__name__):
                view = view_class()
                view.setup(request)
                view.object_list = []
                response = view.render_to_response(context)
                response.render()
                self.assertEqual(
                    response.headers["Content-Type"], "application/pdf"
                )
                self.assertTrue(response.content.startswith(b"%PDF-"))
