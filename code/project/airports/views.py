# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
import json
import csv
import statistics
import re

# Create your views here.
from rest_framework.renderers import JSONRenderer
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_csv import renderers as r
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from airports.models import Airport, Carrier, Statistics, StatisticsGroup, Flights, NumDelays, CarrierComment
from airports.serializers import AirportSerializer, CarrierSerializer, StatisticsGroupSerializer, CarrierCommentSerializer


class ListAirports(APIView):
    """
    get:

    List all airports in the US.

    example output:
    [
    {
        "code": "ATL",
        "name": "Atlanta, GA: Hartsfield-Jackson Atlanta International"
    },
    {
        "code": "BOS",
        "name": "Boston, MA: Logan International"
    },
    .
    .
    .
    ]
    """
    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES) + (r.CSVRenderer,)

    def get(self, request, format=None):
        res_data = AirportSerializer(Airport.objects.all(),many=True).data
        for airport in res_data:
            airport["link"] = "localhost:8000/airports/"+airport["code"]
        return Response(res_data)

class RIAirportView(APIView):

    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES) + (r.CSVRenderer,)

    def get(self, request, airport_id, format=None):
        airport = AirportSerializer(Airport.objects.get(code=airport_id)).data
        airport["link"] = "localhost:8000/airports/"+airport["code"]
        return Response(airport)

class ListCarriers(APIView):
    """
    get:
        List all carriers in the US.

        example output:
        [
        {
            "code": "AA",
            "name": "American Airlines Inc."
        },
        {
            "code": "AS",
            "name": "Alaska Airlines Inc."
        }   
        ]
    """

    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES) + (r.CSVRenderer,)

    def get(self, request, format=None):
        res_data = CarrierSerializer(Carrier.objects.all(), many=True).data
        for carrier in res_data:
            carrier["link"] = "localhost:8000/carriers/"+carrier["code"]
        return Response(res_data)

class RICarrierView(APIView):

    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES) + (r.CSVRenderer,)

    def get(self, request, carrier_id, format=None):
        carrier = CarrierSerializer(Carrier.objects.get(code=carrier_id)).data
        carrier["link"] = "localhost:8000/carriers/"+carrier["code"]
        return Response(carrier)

class ListCarriersOfAirport(APIView):
    """
    get:

    List all carriers for a specific airport.

    input format - .../airports/<airport_code>/carriers/

    example input - .../airports/ATL/carriers/

    example output:
    [
    {
        "code": "B6",
        "name": "JetBlue Airways"
    },
    {
        "code": "CO",
        "name": "Continental Air Lines Inc."
    },
    .
    .
    .
    ]
    """
    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES) + (r.CSVRenderer,)

    def get(self, request, airport_id, format=None):
        stats = StatisticsGroup.objects.filter(airport=airport_id)
        carrier_codes = stats.values_list('carrier',flat=True).distinct()
        list = []
        for code in carrier_codes:
            list.append(CarrierSerializer(Carrier.objects.get(code=code)).data)
        return Response(list)

class AllStatistics(APIView):
    """
    get:
        List full statistics for a specific airport, carrier and time.

        example input: .../statistics/?a_code=ATL&c_code=AA?month_year=2003/6

        example output:
        [
        {
            "airport": "ATL",
            "carrier": "AA",
            "statistics": {
                "minutes_del": {
                    "late_aircraft": 1269,
                    "weather": 1722,
                    "carrier": 1367,
                    "security": 139,
                    "total": 8314,
                    "nat_avi_sys": 3817
                },
                "num_del": {
                    "weather": 28,
                    "security": 2,
                    "late_aircraft": 18,
                    "nat_avi_sys": 105,
                    "carrier": 34
                },
                "flights": {
                    "cancelled": 5,
                    "on_time": 561,
                    "total": 752,
                    "delayed": 186,
                    "diverted": 0
                }
            },
            "time": "2003/6"
        }
        ]

    post:
        Insert new statistics. 
        
        Body is the same as the example output for GET.

    put:
        Modify statistics. Body is the same as in POST.

    delete:
        Delete a statistics entry. Url is the same as in the GET method.

    """

    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES) + (r.CSVRenderer,)

    def get(self, request, format=None):
        airport_code = request.GET.get('a_code','')
        carrier_code = request.GET.get('c_code','')
        if airport_code == '' or carrier_code == '':
            return HttpResponseBadRequest("Please specify an airport and carrier code")
        month_year = request.GET.get('month_year','all')
        stats = StatisticsGroup.objects.filter(airport=airport_code,carrier=carrier_code)
        if month_year == 'all':
            res_data = StatisticsGroupSerializer(stats,many=True).data
            for stat in res_data:
                stat["link"] = "localhost:8000/statistics/?a_code="+stat["airport"]+"&c_code="+stat["carrier"]+"&month_year="+stat["time"]
            return Response(res_data)
        stats = stats.filter(time=month_year)
        stats = StatisticsGroupSerializer(stats,many=True).data
        stats[0]["link"] = "localhost:8000/statistics/?a_code="+stats[0]["airport"]+"&c_code="+stats[0]["carrier"]+"&month_year="+stats[0]["time"]
        return Response(stats)

    def post(self, request, format=None):
        stat_data = request.data
        stat = StatisticsGroupSerializer(data=stat_data,many=True)

        try:
            stat.is_valid()
            stat.save()
        except:
            return HttpResponseBadRequest("Please give a proper statistics dictionary")

        return Response()

    def put(self, request, format=None):
        stat_data = request.data[0]
        airport = stat_data["airport"]
        carrier = stat_data["carrier"]
        month_year = stat_data["time"]

        stats = StatisticsGroupSerializer(data=request.data, many=True)
        try:
            stats.is_valid()
        except:
            return HttpResponseBadRequest("Please give a proper statistics dictionary")
        stats2 = StatisticsGroup.objects.filter(airport=airport, carrier=carrier, time=month_year)
        if len(stats2) == 1:
            stats2.first().delete()
        stats.save()

        return Response()

    def delete(self, request, format=None):
        airport_code = request.GET.get('a_code', '')
        carrier_code = request.GET.get('c_code', '')
        month_year = request.GET.get('month_year', 'all')
        if airport_code == '' or carrier_code == '':
            return HttpResponseBadRequest("Please specify an airport and carrier code")
        stats = StatisticsGroup.objects.filter(airport=airport_code, carrier=carrier_code)
        if month_year == 'all':
            stats.delete()
            return Response()
        stats.filter(time=month_year).delete()
        return Response()

class FlightsStatistics(APIView):

    """
    get:

    Return statistics specific to flights.

    example input - .../statistics/flights/?a_code=ATL&c_code=AA&month_year=2003/6

    example output:
    [
    {
        "cancelled": 5,
        "delayed": 186,
        "on_time": 561,
        "time": "2003/6"
    }
    ]
    """

    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES) + (r.CSVRenderer,)

    def get(self, request, format=None):
        airport_code = request.GET.get('a_code', '')
        carrier_code = request.GET.get('c_code', '')
        month_year = request.GET.get('month_year', 'all')
        if airport_code == '' or carrier_code == '':
            return HttpResponseBadRequest("Please specify an airport and carrier code")
        stats = StatisticsGroup.objects.filter(airport=airport_code, carrier=carrier_code)
        if month_year != 'all':
            stats = stats.filter(time=month_year)
        stats = stats.values()
        list = []
        for stat in stats:
            stati = Statistics.objects.get(id=stat["statistics_id"]).__dict__
            flights = Flights.objects.get(id=stati["flights_id"]).__dict__
            list.append({
                "on_time": flights["on_time"],
                "delayed": flights["delayed"],
                "cancelled": flights["cancelled"],
                "time": stat["time_id"],
                "link": "localhost:8000/statistics/flights/?a_code="+airport_code+"&c_code="+carrier_code+"&month_year="+stat["time_id"]
            })
        return Response(list)

class DelayStatistics(APIView):

    """
    get:

    Return statistics specific to all or carrier delays. Reason can be 'carrier' or 'all'.

    example input - .../statistics/flights/?a_code=ATL&c_code=AA&month_year=2003/6

    example output:

    [
    {
        "delays": {
            "nat_avi_sys": 105,
            "late_aircraft": 18,
            "weather": 28,
            "carrier": 34,
            "security": 2,
            "id": 203
        },
        "time": "2003/6"
    }
    ]

    example input - .../statistics/flights/?a_code=ATL&c_code=AA&month_year=2003/6&reason=carrier

    example output:

    [
    {
        "late_airport": 18,
        "carrier": 34,
        "time": "2003/6"
    }
    ]
    """

    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES) + (r.CSVRenderer,)

    def get(self, request, format=None):
        airport_code = request.GET.get('a_code', '')
        carrier_code = request.GET.get('c_code', '')
        if airport_code == '' or carrier_code == '':
            return HttpResponseBadRequest("Please specify an airport and carrier code")
        month_year = request.GET.get('month_year', 'all')
        reason = request.GET.get('reason', 'all')

        stats = StatisticsGroup.objects.filter(airport=airport_code, carrier=carrier_code)
        if month_year != 'all':
            stats = stats.filter(time=month_year)
        stats = stats.values()
        list = []
        for stat in stats:
            stati = Statistics.objects.get(id=stat["statistics_id"]).__dict__
            num_del = NumDelays.objects.get(id=stati["num_del_id"]).__dict__
            if reason == "carrier":
                list.append({
                    "carrier": num_del["carrier"],
                    "late_airport": num_del["late_aircraft"],
                    "time": stat["time_id"],
                    "link": "localhost:8000/statistics/delays/?a_code="+airport_code+"&c_code="+carrier_code+"&month_year="+stat["time_id"]

                })
            else:
                num_del.pop('_state')
                list.append({
                    "delays": num_del,
                    "time": stat["time_id"],
                    "link": "localhost:8000/statistics/delays/?a_code="+airport_code+"&c_code="+carrier_code+"&month_year="+stat["time_id"]

                })
        return Response(list)

class FancyStatistics(APIView):
    """
    get:

    List mean, median, standard deviation for all carrier related flight delays between two airports for a specific carrier or all carriers.

    example input - http://localhost:8000/statistics/description/?from=ATL&to=BOS

    example output:

    {
    "late_aircraft": {
        "std": 148.34847906813897,
        "avg": 87.72222222222223,
        "median": 17.5
    },
    "carrier": {
        "std": 122.17404279152811,
        "avg": 69.44444444444444,
        "median": 26.5
    }
    }

    example input - http://localhost:8000/statistics/description/?from=ATL&to=BOS&carrier=AA
    example output:

    {
    "late_aircraft": {
        "std": 19.79898987322333,
        "avg": 32,
        "median": 32
    },
    "carrier": {
        "std": 24.748737341529164,
        "avg": 51.5,
        "median": 51.5
    }
    }
    """
    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES) + (r.CSVRenderer,)

    def get(self, request, format=None):
        from_a = request.GET.get('from', '')
        to_a = request.GET.get('to', '')
        carrier = request.GET.get('carrier', 'all')
        if from_a == '' or to_a == '':
            return HttpResponseBadRequest("Please specify a 'from' airport and a 'to' airport")
        from_stats = []
        to_stats = []
        if carrier == 'all':
            from_stats = StatisticsGroupSerializer(StatisticsGroup.objects.filter(airport=from_a),many=True).data
            to_stats = StatisticsGroupSerializer(StatisticsGroup.objects.filter(airport=to_a),many=True).data
        else:
            from_stats = StatisticsGroupSerializer(StatisticsGroup.objects.filter(airport=from_a,carrier=carrier), many=True).data
            to_stats = StatisticsGroupSerializer(StatisticsGroup.objects.filter(airport=to_a,carrier=carrier), many=True).data
        carrier_delays = []
        late_air_delays = []
        for stat in from_stats:
            carrier_delays.append(stat['statistics']['num_del']['carrier'])
            late_air_delays.append(stat['statistics']['num_del']['late_aircraft'])
        for stat in to_stats:
            carrier_delays.append(stat['statistics']['num_del']['carrier'])
            late_air_delays.append(stat['statistics']['num_del']['late_aircraft'])

        carrier_delays.sort()
        late_air_delays.sort()

        description = {
            "carrier": {
                "avg": statistics.mean(carrier_delays),
                "median": statistics.median(carrier_delays),
                "std": statistics.stdev(carrier_delays)
            },
            "late_aircraft": {
                "avg": statistics.mean(late_air_delays),
                "median": statistics.median(late_air_delays),
                "std": statistics.stdev(late_air_delays)
            },
            "link": "localhost:8000/statistics/description/?from="+from_a+"&to="+to_a+"&carrier="+carrier
        }

        return Response(description)

class Rankings(APIView):
        """
        retrieve:

            Get rankings of carriers based on query parameters.

            example input - .../carriers/rankings/?mdc=1&ndla=1

            example output - 

            [
                {
                    "carrier": "EV",
                    "min_del_carrier": 0,
                    "num_del_late_air": 0
                },
                {
                    "carrier": "RU",
                    "min_del_carrier": 2,
                    "num_del_late_air": 1
                },
                {
                    "carrier": "HP",
                    "min_del_carrier": 3,
                    "num_del_late_air": 2
                },
                .
                .
                .
            ]
        """
        def get(self, request, format=None):
            min_del_carrier = request.GET.get("mdc","0")
            min_del_late_air = request.GET.get("mdla","0")
            num_del_carrier = request.GET.get("ndc","0")
            num_del_late_air = request.GET.get("ndla","0")

            carriers = CarrierSerializer(Carrier.objects.all(),many=True).data
            stats = StatisticsGroupSerializer(StatisticsGroup.objects.all(),many=True).data
            output = []
            for x in carriers:
                x_out = dict({"carrier": x["code"], "num": 0})
                output.append(x_out)

            for stat in stats:
                code = stat["carrier"]
                i = -1
                for idx in range(len(output)):
                    if output[idx]["carrier"] == code:
                        output[idx]["num"] += 1
                        i = idx
                        
                if i != -1:
                    if min_del_carrier == "1":
                        if "min_del_carrier" in output:
                            output[i]["min_del_carrier"] += stat["statistics"]["minutes_del"]["carrier"]
                        else:
                            output[i]["min_del_carrier"] = stat["statistics"]["minutes_del"]["carrier"]
                    if min_del_late_air == "1":
                        if "min_del_late_air" in output:
                            output[i]["min_del_late_air"] += stat["statistics"]["minutes_del"]["late_aircraft"]
                        else:
                            output[i]["min_del_late_air"] = stat["statistics"]["minutes_del"]["late_aircraft"]
                    if num_del_carrier == "1":
                        if "num_del_carrier" in output:
                            output[i]["num_del_carrier"] += stat["statistics"]["num_del"]["carrier"]
                        else:
                            output[i]["num_del_carrier"] = stat["statistics"]["num_del"]["carrier"]
                    if num_del_late_air == "1":
                        if "num_del_late_air" in output:
                            output[i]["num_del_late_air"] += stat["statistics"]["num_del"]["late_aircraft"]
                        else:
                            output[i]["num_del_late_air"] = stat["statistics"]["num_del"]["late_aircraft"]

            idx = 0
            while idx < len(output):
                if output[idx]["num"] == 0:
                    del output[idx]
                else:
                    idx += 1
            
            if min_del_carrier == "1":
                output.sort(key=(lambda a : a["min_del_carrier"]/a["num"]))
                for i in range(len(output)):
                    output[i]["min_del_carrier"] = i
            if min_del_late_air == "1":
                output.sort(key=(lambda a : a["min_del_late_air"]/a["num"]))
                for i in range(len(output)):
                    output[i]["min_del_late_air"] = i
            if num_del_carrier == "1":
                output.sort(key=(lambda a : a["num_del_carrier"]/a["num"]))
                for i in range(len(output)):
                    output[i]["num_del_carrier"] = i
            if num_del_late_air == "1":
                output.sort(key=(lambda a : a["num_del_late_air"]/a["num"]))
                for i in range(len(output)):
                    output[i]["num_del_late_air"] = i

            for i in range(len(output)):
                output[i].pop("num", None)
            
            output.append({"link": "localhost:8000/carriers/rankings/?mdc="+min_del_carrier+"&mdla="+min_del_late_air+"&ndc="+num_del_carrier+"&ndla="+num_del_late_air})
            return Response(output)

class CommentView(APIView):

        """
        get: 

        Get list of comments for one or all carriers.

        example input - .../carriers/comments/?carrier=AA

        example output -

        [
            {
                "id": 1,
                "carrier_id": "AA",
                "comment": "Great carrier!"
            },
            {
                "id": 2,
                "carrier_id": "AA",
                "comment": "Wow this carrier changed my life!"
            },
            .
            .
            .
        ]
        """

        renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES) + (r.CSVRenderer,)

        def get(self, request, format=None):
            carrier = request.GET.get("carrier", "all")
            if carrier == "all":
                comments = CarrierComment.objects.all().values()
                for comment in comments:
                    comment["link"] = "localhost:8000/comments/?id="+str(comment["id"])
                return Response(comments)

            try:
                car = Carrier.objects.get(code=carrier)
            except ObjectDoesNotExist:
                return HttpResponseBadRequest("Carrier doesn't exist")
            
            comments = CarrierComment.objects.filter(carrier=carrier).values()
            for comment in comments:
                comment["link"] = "localhost:8000/comments/?id="+str(comment["id"])
            return Response(comments)
        

        """
        post: 

        Post a new comment

        example input - .../carriers/comments/

        [{
            "carrier": "AA",
            "comment": "Just take my money!"
        }]

        """
        @swagger_auto_schema(request_body=CarrierCommentSerializer)
        def post(self, request, format=None):
            data = request.data[0]
            comment = CarrierCommentSerializer(data=data)
            try:
                comment.is_valid()
                comment.save()
            except:
                return HttpResponseBadRequest("Please give a proper comment dictionary")
            return Response()

        """
        put:

        Create or modify a comment based on an id.

        example input - .../carriers/comments/

        [{
            "id": 2
            "carrier": "AA",
            "comment": "Just take my money!"
        }]
        """
        @swagger_auto_schema(request_body=CarrierCommentSerializer)
        def put(self, request, format=None):
            data = request.data[0]
            comment = CarrierComment.objects.filter(id=data["id"])
            if len(comment) != 0:
                comment.delete()
            
            new_comment = CarrierCommentSerializer(data=data)
            try:
                new_comment.is_valid()
                new_comment.save()
            except:
                return HttpResponseBadRequest("Please give a proper comment dictionary")
            return Response()

        """
        delete:

        Delete an existing comment.

        example input - .../carriers/comments/?id=2
        """
        def delete(self, request, format=None):
            id = request.GET.get("id","")
            try:
                comment = CarrierComment.objects.get(id=id)
                comment.delete()
            except ObjectDoesNotExist:
                return HttpResponseBadRequest("Please give a proper comment id")
            
            return Response()
            

