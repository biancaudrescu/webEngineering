"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin


from airports import views
from rest_framework.documentation import include_docs_urls
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Airports API",
      default_version='v1',
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^airports/$', views.ListAirports.as_view()),
    url(r'^airports/(?P<airport_id>[\w]+)/$',views.RIAirportView.as_view()),

    url(r'^carriers/$', views.ListCarriers.as_view()),
    url(r'^carriers/(?P<carrier_id>[\w]+)/$',views.RICarrierView.as_view()),

    url(r'^airports/(?P<airport_code>[\w]+)/statistics/$', views.AllStatistics.as_view()),
    url(r'^airports/(?P<airport_code>[\w]+)/statistics/flights/$', views.FlightsStatistics.as_view()),
    url(r'^airports/(?P<airport_code>[\w]+)/statistics/delays/$', views.DelayStatistics.as_view()),
    url(r'^airports/(?P<from_a>[\w]+)/statistics/description/$', views.FancyStatistics.as_view()),

    url(r'^rankings/$',views.Rankings.as_view()),
    url(r'^comments/$', views.CommentView.as_view()),
    
    url(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

