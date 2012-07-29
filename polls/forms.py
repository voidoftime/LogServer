#coding=utf8

from django import forms

predefinedPeriods=(('CurrentDay','Сегодня'),('Yesterday','Вчера'),('LastWeek','Неделя'),('LastMonth','Месяц'))

class FilterForm(forms.Form):
    predefinedPeriod = forms.ChoiceField(widget=forms.RadioSelect, choices=predefinedPeriods,label='')
    beginDate=forms.DateField(widget=forms.DateTimeInput)
    endDate=forms.DateField()
