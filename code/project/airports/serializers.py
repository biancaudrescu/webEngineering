from rest_framework import serializers

from airports.models import Airport, Carrier, Statistics, Flights, NumDelays, MinutesDelayed, StatisticsGroup, Time, CarrierComment


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ('code', 'name')


class CarrierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrier
        fields = ('code', 'name')


class CarrierCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarrierComment
        fields = ('carrier', 'comment')


class TimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Time
        fields = ('label', 'year', 'month',)


class FlightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flights
        exclude = ('id',)


class NumDelaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = NumDelays
        exclude = ('id',)


class MinutesDelayedSerializer(serializers.ModelSerializer):
    class Meta:
        model = MinutesDelayed
        exclude = ('id',)


class StatisticsSerializer(serializers.ModelSerializer):
    minutes_del = MinutesDelayedSerializer()
    num_del = NumDelaysSerializer()
    flights = FlightsSerializer()

    class Meta:
        model = Statistics
        fields = ('minutes_del', 'num_del', 'flights')

    def create(self, validated_data):
        flights = FlightsSerializer().create(validated_data.pop("flights"))
        num_del = NumDelaysSerializer().create(validated_data.pop("num_del"))
        minutes_del = MinutesDelayedSerializer().create(validated_data.pop("minutes_del"))
        stats = Statistics()
        stats.flights = flights
        stats.minutes_del = minutes_del
        stats.num_del = num_del
        stats.save()
        return stats


class StatisticsGroupSerializer(serializers.ModelSerializer):

    statistics = StatisticsSerializer()

    class Meta:
        model = StatisticsGroup
        fields = ('airport', 'carrier', 'statistics', 'time')

    def create(self, validated_data):

        stats = StatisticsGroup()
        stats.airport = validated_data["airport"]
        stats.carrier = validated_data["carrier"]
        stats.time = validated_data["time"]
        stats.statistics = StatisticsSerializer().create(validated_data.pop("statistics"))
        stats.save()
        return stats
