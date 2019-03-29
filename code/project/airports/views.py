# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseBadRequest, HttpResponseRedirect

from statistics import mean, median, stdev

# Create your views here.
from django.shortcuts import render
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_csv import renderers as r
from django.core.exceptions import ObjectDoesNotExist

from airports.forms import *
from airports.models import Airport, Carrier, Statistics, StatisticsGroup, Flights, NumDelays, CarrierComment
from airports.serializers import AirportSerializer, CarrierSerializer, StatisticsGroupSerializer, CarrierCommentSerializer



#Biancas shit
def airports(request):
    return render(request, "../templates/airports.html", {})

def carriers(request):
    return render(request, "../templates/carriers.html", {})


def carriersRankings(request):
    return render(request, "../templates/carriersrankings.html", {})


def carriersComm(request):
    return render(request, "../templates/carrierscomm.html", {})

def statistics(request):
    if request.method=='GET':
        return render(request, "../templates/statistics.html", {})





def statisticsPost(request):
    if request.method == 'POST':
        charForm1 = CharForm(request.POST)


        formFlights= FlightsForm(request.POST)
        formMin =minDelayForm(request.POST)
        formNum = numDelayForm(request.POST)
        if formNum.is_valid() and formFlights.is_valid() and formMin.is_valid() and charForm1.is_valid():
            num = dict(formNum.cleaned_data)
            min = dict(formMin.cleaned_data)
            fli = dict(formFlights.cleaned_data)
            identity = dict(charForm1.cleaned_data)
            air = identity["airport_id"]
            car = identity["carrier_id"]
            tim = identity["time_id"]
            print(air, car, tim)
            stat = dict({"minutes_del": min, "num_del": num, "flights": fli})
            statGroup = dict({"airport": air, "carrier": car, "statistics": stat, "time": tim})

            stat = StatisticsGroupSerializer(data=statGroup)

            if not stat.is_valid():
                return HttpResponseRedirect("./")

            stat.save()

    else:
        charForm1 = CharForm()

        formFlights = FlightsForm()
        formMin= minDelayForm()
        formNum = numDelayForm()

    return render(request, "../templates/post.html", {'forma': charForm1,'form1':formFlights,'form2':formMin,'form3':formNum})


def statisticsDelete(request):
    if request.method == 'POST':
        charForm1 = CharForm(request.POST)

        if  charForm1.is_valid():

            identity = dict(charForm1.cleaned_data)
            air = identity["airport_id"]
            car = identity["carrier_id"]
            tim = identity["time_id"]
            try:
                obj = StatisticsGroup.objects.get(airport=air,carrier=car,time=tim)
                obj.delete()
            except:
                return HttpResponseRedirect('./')

            return  HttpResponseRedirect('./')

        return HttpResponseRedirect('./')

    else:
        charForm1 = CharForm()

        formFlights = FlightsForm()
        formMin= minDelayForm()
        formNum = numDelayForm()

    return render(request, "../templates/delete.html", {'forma': charForm1,'form1':formFlights,'form2':formMin,'form3':formNum})



def statisticsMinutes(request):
    return render(request, "../templates/statisticsminutes.html", {})


def statisticsDelays(request):
    return render(request, "../templates/statisticsdelays.html", {})


def statisticsDescription(request):
    return render(request, "../templates/statisticsdescription.html", {})


#Jakobs shit
class ListAirports(APIView):
    
    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES) + (r.CSVRenderer,)

    def get(self, request, format=None):
        res_data = AirportSerializer(Airport.objects.all(),many=True).data
        for airport in res_data:
            airport["link"] = request.path+airport["code"]
        return Response(res_data)

class RIAirportView(APIView):

    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES) + (r.CSVRenderer,)

    def get(self, request, airport_id, format=None):
        airport = AirportSerializer(Airport.objects.get(code=airport_id)).data
        airport["link"] = request.path
        return Response(airport)

class ListCarriers(APIView):
    

    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES) + (r.CSVRenderer,)

    def get(self, request, format=None):

        airport = request.GET.get("airport","")
        if airport != "":
            stats = StatisticsGroup.objects.filter(airport=airport)
            if len(stats) == 0:
                return HttpResponseBadRequest("Please specify a proper airport.")
            carrier_codes = stats.values_list('carrier',flat=True).distinct()
            carriers = []
            for code in carrier_codes:
                carriers.append(CarrierSerializer(Carrier.objects.get(code=code)).data)
            for carrier in carriers:
                carrier["link"] = request.path+carrier["code"]
            return Response(carriers)

        res_data = CarrierSerializer(Carrier.objects.all(), many=True).data
        for carrier in res_data:
            carrier["link"] = request.path+carrier["code"]
        return Response(res_data)

class RICarrierView(APIView):

    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES) + (r.CSVRenderer,)

    def get(self, request, carrier_id, format=None):
        carrier = CarrierSerializer(Carrier.objects.get(code=carrier_id)).data
        carrier["link"] = request.path
        return Response(carrier)

class AllStatistics(APIView):
    

    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES) + (r.CSVRenderer,)

    def get(self, request, airport_code, format=None):
        carrier_code = request.GET.get('c_code','')
        if airport_code == '' or carrier_code == '':
            return HttpResponseBadRequest("Please specify an airport and carrier code")
        month_year = request.GET.get('month_year','all')
        stats = StatisticsGroup.objects.filter(airport=airport_code,carrier=carrier_code)
        if len(stats) == 0:
            return Response(list())
        if month_year == 'all':
            res_data = StatisticsGroupSerializer(stats,many=True).data
            for stat in res_data:
                stat["link"] = request.path+"?c_code="+stat["carrier"]+"&month_year="+stat["time"]
            return Response(res_data)
        stats = stats.filter(time=month_year)
        if len(stats) == 0:
            return Response(list())
        stats = StatisticsGroupSerializer(stats,many=True).data
        stats[0]["link"] = request.path+"?c_code="+stats[0]["carrier"]+"&month_year="+stats[0]["time"]
        return Response(stats)

    def post(self, request, airport_code, format=None):
        stat_data = request.data
        stat = StatisticsGroupSerializer(data=stat_data,many=True)
        
        if stat.is_valid():
            print(stat.save())
            return Response()

        return HttpResponseBadRequest("Please give a proper statistics dictionary that doesn't already exist.")


    def put(self, request, airport_code, format=None):
        try:
            stat_data = request.data[0]
        except:
            return HttpResponseBadRequest("Please give a proper dictionary enclosed in square brackets.")
        airport = stat_data["airport"]
        carrier = stat_data["carrier"]
        month_year = stat_data["time"]

        stats = StatisticsGroupSerializer(data=request.data, many=True)
        stats2 = StatisticsGroup.objects.filter(airport=airport, carrier=carrier, time=month_year)
        stats2_data = StatisticsGroupSerializer(stats2,many=True)
        if len(stats2) == 1:
            stats2.first().delete()
        
        if not stats.is_valid():
            stats2=StatisticsGroupSerializer(data=stats2_data,many=True)
            stats2.is_valid()
            stats2.save()
            return HttpResponseBadRequest("Please give a proper statistics dictionary")
        stats.save()

        return Response()

    def delete(self, request, airport_code, format=None):
        carrier_code = request.GET.get('c_code', '')
        month_year = request.GET.get('month_year', 'all')
        if airport_code == '' or carrier_code == '':
            return HttpResponseBadRequest("Please specify an airport and carrier code")
        stats = StatisticsGroup.objects.filter(airport=airport_code, carrier=carrier_code)
        if len(stats) == 0:
            return HttpResponseBadRequest("No statistics found for given airport and carrier, please check that you're giving proper airport and carrier codes.")
        if month_year == 'all':
            stats.delete()
            return Response()
        stats = stats.filter(time=month_year)
        if len(stats) == 0:
            return HttpResponseBadRequest("No statistics found for given time for this airport and carrier.")
        stats.delete()
        return Response()

class FlightsStatistics(APIView):

    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES) + (r.CSVRenderer,)

    def get(self, request, airport_code, format=None):
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
                "link": request.path+"?c_code="+carrier_code+"&month_year="+stat["time_id"]
            })
        return Response(list)

class DelayStatistics(APIView):

    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES) + (r.CSVRenderer,)

    def get(self, request, airport_code, format=None):
        carrier_code = request.GET.get('c_code', '')
        if airport_code == '' or carrier_code == '':
            return HttpResponseBadRequest("Please specify an airport and carrier code")
        month_year = request.GET.get('month_year', 'all')
        reason = request.GET.get('reason', 'all')

        if airport_code != "ALL":
            stats = StatisticsGroup.objects.filter(airport=airport_code, carrier=carrier_code)
        else:
            stats = StatisticsGroup.objects.filter(carrier=carrier_code)

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
                    "link": request.path+"?c_code="+carrier_code+"&month_year="+stat["time_id"]

                })
            else:
                num_del.pop('_state')
                list.append({
                    "delays": num_del,
                    "time": stat["time_id"],
                    "link": request.path+"?c_code="+carrier_code+"&month_year="+stat["time_id"]

                })
        return Response(list)

class FancyStatistics(APIView):
    
    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES) + (r.CSVRenderer,)

    def get(self, request, from_a, format=None):
        to_a = request.GET.get('to', '')
        carrier = request.GET.get('carrier', 'all')
        if from_a == '' or to_a == '':
            return HttpResponseBadRequest("Please specify a 'to' airport as a query parameter.")

        from_stats = StatisticsGroup.objects.filter(airport=from_a)
        to_stats = StatisticsGroup.objects.filter(airport=to_a)
        if len(from_stats) == 0:
            return HttpResponseBadRequest("Outgoing airport doesn't exist or has no statistics.")
        if len(to_stats) == 0:
            return HttpResponseBadRequest("Destination airport doesn't exist or has no statistics.")
        
        if carrier != 'all':
            from_stats = from_stats.filter(carrier=carrier)
            to_stats = to_stats.filter(carrier=carrier)
            if len(from_stats) == 0 and len(to_stats) == 0:
                return HttpResponseBadRequest("Specified carrier has no statistics or doesn't exit.")

        from_stats = StatisticsGroupSerializer(from_stats,many=True).data
        to_stats = StatisticsGroupSerializer(to_stats,many=True).data

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
                "avg": mean(carrier_delays),
                "median": median(carrier_delays),
                "std": stdev(carrier_delays)
            },
            "late_aircraft": {
                "avg": mean(late_air_delays),
                "median": median(late_air_delays),
                "std": stdev(late_air_delays)
            },
            "link": request.path+"?to="+to_a+"&carrier="+carrier
        }

        return Response(description)

class Rankings(APIView):

    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES) + (r.CSVRenderer,)

    def get(self, request, format=None):
        min_del_carrier = request.GET.get("mdc","0")
        min_del_late_air = request.GET.get("mdla","0")
        num_del_carrier = request.GET.get("ndc","0")
        num_del_late_air = request.GET.get("ndla","0")

        if min_del_carrier == "0" and min_del_late_air == "0" and num_del_carrier == "0" and num_del_late_air == "0":
            return HttpResponseBadRequest("Please specify at least one ranking criterion in the query parameters (mdc=1, mdla=1, ndc=1 or ndla=1).")
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
        
        output.append({"link": request.path+"?mdc="+min_del_carrier+"&mdla="+min_del_late_air+"&ndc="+num_del_carrier+"&ndla="+num_del_late_air})
        return Response(output)

class CommentView(APIView):

    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES) + (r.CSVRenderer,)

    def get(self, request, format=None):
        carrier = request.GET.get("carrier", "all")
        comment_id = request.GET.get("id", "")
        if comment_id != "":
            try:
                comment = CarrierComment.objects.get(id=comment_id)
                comment = CarrierCommentSerializer(comment).data
                comment["link"] = request.path+"?id="+comment_id
                return Response(comment)
            except:
                return HttpResponseBadRequest("Comment does not exist.")
        if carrier == "all":
            comments = CarrierComment.objects.all().values()
            links = []
            for comment in comments:
                links.append(request.path+"?id="+str(comment["id"]))
            comments = CarrierCommentSerializer(CarrierComment.objects.all(),many=True).data
            for i in range(len(comments)):
                comments[i]["link"] = links[i]
            return Response(comments)

        try:
            car = Carrier.objects.get(code=carrier)
        except ObjectDoesNotExist:
            return HttpResponseBadRequest("Carrier doesn't exist")
        
        comments = CarrierComment.objects.filter(carrier=carrier).values()
        for comment in comments:
            comment["link"] = request.path+"?id="+str(comment["id"])
            comment["carrier"] = comment["carrier_id"]
            del comment["carrier_id"]
        return Response(comments)
    
    def post(self, request, format=None):
        data = request.data[0]
        comment = CarrierCommentSerializer(data=data)
        
        if comment.is_valid():
            comment.save()
            return Response()

        return HttpResponseBadRequest("Please give a proper comment dictionary")

    def put(self, request, format=None):
        try:
            data = request.data[0]
            new_comment = CarrierCommentSerializer(data=data)
            if not new_comment.is_valid():
                return HttpResponseBadRequest("Request body is inadequate, read the documentation.")
        except:
            return HttpResponseBadRequest("Request body is inadequate, read the documentation.")
        id = request.GET.get("id","")
        try:
            comment = CarrierComment.objects.filter(id=id)
        except:
            return Response("Please specify a proper id. Must be an int.")
        if len(comment) != 0:
            comment_data = CarrierCommentSerializer(comment[0])
            comment.delete()
        
        if new_comment.is_valid():
            new_comment.save()
            return Response()

        comment = CarrierCommentSerializer(comment_data)
        comment.is_valid()
        comment.save()
        return HttpResponseBadRequest("Please give a proper comment dictionary")

    def delete(self, request, format=None):
        id = request.GET.get("id","")
        try:
            comment = CarrierComment.objects.get(id=int(id))
            comment.delete()
        except:
            return HttpResponseBadRequest("Please give a proper comment id")
        
        return Response()
        

