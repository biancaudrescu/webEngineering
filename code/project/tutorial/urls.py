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
from airports import views

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

    url(r'^web/airports/$', views.airports, name='airports'),
    url(r'^web/carriers/$', views.carriers, name='carriers'),
    url(r'^web/carriers/comments/$', views.carriersComm, name='carriersComm'),
    url(r'^web/carriers/rankings/$', views.carriersRankings, name='carriersRankings'),
    url(r'^web/statistics/$', views.statistics, name='statistics'),
    url(r'^web/statistics/post$', views.statisticsPost, name='statisticsPost'),
    url(r'^web/statistics/flights/$', views.statisticsMinutes, name='statisticsMinutes'),
    url(r'^web/statistics/delays/$', views.statisticsDelays, name='statisticsDelays'),
    url(r'^web/statistics/delete/$', views.statisticsDelete, name='statisticsDelete'),
    url(r'^web/statistics/description/$', views.statisticsDescription, name='statisticsDescription')

]

