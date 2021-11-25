"""esteettomyyssovellus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from rest_framework import routers
from . api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'ArEntrances', views.ArEntranceViewSet)
router.register(r'ArForms', views.ArFormViewSet)
router.register(r'ArXQuestions', views.ArXQuestionViewSet)
router.register(r'ArXQuestionBlocks', views.ArXQuestionBlockViewSet)
router.register(r'ArServicepoints', views.ArServicepointViewSet)
router.register(r'ArSystems', views.ArSystemViewSet)
router.register(r'ArSystemForms', views.ArSystemFormViewSet)
router.register(r'ArXQuestionAnswerPhotos',
                views.ArXQuestionAnswerPhotoViewSet)
router.register(r'ArFormLanguages', views.ArFormLanguageViewSet)
router.register(r'ArXQuestionLanguages', views.ArXQuestionLanguageViewSet)
router.register(r'ArXStoredSentenceLangs', views.ArXStoredSentenceLangViewSet,
                basename='storedsentencelang')
router.register(r'ArBackendQuestions', views.ArBackendQuestionViewSet)
router.register(r'ArBackendQuestionBlocks',
                views.ArBackendQuestionBlockViewSet)
router.register(r'ArBackendQuestionChoice',
                views.ArBackendQuestionChoiceViewSet)
router.register(r'ArBackendEntranceAnswer',
                views.ArBackendEntranceAnswerViewSet)
router.register(r'ArXAdditionalinfo', views.ArXAdditionalinfoViewSet,
                basename="additionalinfo")
router.register(r'ArXQuestionAnswerComment',
                views.ArXQuestionAnswerCommentViewSet)
router.register(r'ArXQuestionAnswerLocation',
                views.ArXQuestionAnswerLocationViewSet)
router.register(r'ArXQuestionAnswerPhoto',
                views.ArXQuestionAnswerPhotoViewSet)
router.register(r'ArXQuestionAnswerPhotoTxt',
                views.ArXQuestionAnswerPhotoTxtViewSet)
router.register(r'ArXAnswerLog',
                views.ArXAnswerLogViewSet)
router.register(r'ArXQuestionAnswer',
                views.ArXQuestionAnswerViewSet)
router.register(r'ArExternalServicepoint',
                views.ArExternalServicepointViewSet)
router.register(r'ArBackendEntrance',
                views.ArBackendEntranceViewset)
router.register(r'ArBackendServicepoint',
                views.ArBackendServicepointViewset)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls',
                              namespace='rest_framework')),
]

# Add endpoint for the ptv_chop_address psql function.
urlpatterns += [
    path('api/ChopAddress/', views.ChopAddressView.as_view()),
    path('api/GenerateSentences/', views.GenerateSentencesView.as_view())
]

# Public APIs
urlpatterns += [
     # SYSTEM DATA
     path('api/v1/accessibility/variables/',
         views.ArRest01AccessVariableView.as_view()),
     path('api/v1/accessibility/viewpoints/',
         views.ArRest01AccessViewpointView.as_view()),
     path('api/v1/accessibility/requirements/',
         views.ArRest01RequirementView.as_view()),

     # CLIENT DATA
     path('api/v1/servicepoints/<uuid:systemId>/<str:servicePointId>/',
         views.ArRest01ServicepointView),
     path('api/v1/servicepoints/<uuid:systemId>/<str:servicePointId>/sentences/',
         views.ArRest01SentenceView),
     path('api/v1/servicepoints/<uuid:systemId>/<str:servicePointId>/entrances/<int:entranceId>/sentences/',
         views.ArRest01EntranceSentenceView),

     # CLIENT DATA, MASSIVE QUERIES
     path('api/v1/servicepoints/<uuid:systemId>/', views.ArSystemServicepointsView),
     path('api/v1/servicepoints/<uuid:systemId>/entrances/', views.ArSystemEntrancesView),
     path('api/v1/accessibility/servicepoints/<uuid:systemId>/sentences/', views.ArSystemSentencesView),


     # servicePointId is str because it can be both uuid or int
     path('api/v1/servicepoints/<uuid:systemId>/<str:servicePointId>/entrances/',
         views.ArRest01EntranceView),

     # TODO: no primary_key doesn't work for now
     #path('api/v1/servicepoints/<uuid:systemId>/<str:servicePointId>/shortages/',
     #     views.ArRest01ShortageView),
]
