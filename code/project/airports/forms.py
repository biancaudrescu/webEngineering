from django import forms
from .models import MinutesDelayed,Airport,Carrier,StatisticsGroup,Time,NumDelays,Flights
class AirportForm(forms.ModelForm):

        class Meta:
              model=Airport

              fields=('code','name')



class CarrierForm(forms.ModelForm):

        class Meta:
              model=Carrier

              fields=('code','name')




class TimeForm(forms.ModelForm):

        class Meta:
              model=Time

              fields=('year','month','label')



class StatForm(forms.ModelForm):

        class Meta:
              model=StatisticsGroup

              fields=('airport','carrier','time')




class minDelayForm(forms.ModelForm):

        class Meta:
              model=MinutesDelayed

              fields=('carrier','weather','total','late_aircraft','security','nat_avi_sys')


class numDelayForm(forms.ModelForm):

        class Meta:
              model=NumDelays

              fields=('carrier','weather','late_aircraft','security','nat_avi_sys')




class FlightsForm(forms.ModelForm):

        class Meta:
              model=Flights

              fields=('cancelled','on_time','total','delayed','diverted')

class CharForm(forms.Form):
        airport_id = forms.CharField(label="airport_id",max_length=3)
        carrier_id = forms.CharField(label="carrier_id",max_length=3)
        time_id = forms.CharField(label="time_id",max_length=7)
