from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from taggit.models import Tag
from django.http import HttpRequest
from main_app.models import Disease

def get_list_of_symptoms():
    symptoms = list(Tag.objects.all())
    s = []
    for i in range(1, len(symptoms), 2):
        s.append([symptoms[i - 1], symptoms[i]])
    return s


class MainView(View):
    def get(self, request, *args, **kwargs):
        s = get_list_of_symptoms()
        return render(
            request,
            template_name='index.html',
            context={
                'symptoms': s
            }
        )


class SearchView(View):
    def get(self, request, *args, **kwargs):
        symptoms = []
        try:
            for i in request.GET:
                symptoms.append(Tag.objects.get(slug=i))
        except:
            return redirect('main_app:index')
        if len(symptoms) == 0:
            return redirect('main_app:index')
        diseases = Disease.objects.all()
        result = {}
        for disease in diseases:
            cnt = 0
            for symp in symptoms:
                if symp in disease.symptoms.all():
                    cnt += 1
            if cnt > 0 and cnt >= (len(symptoms) + 1) // 2:
                result[disease] = (-cnt, len(disease.symptoms.all()))

        print(sorted(result.keys(), key=lambda x: result[x]))
        return render(request,
                      template_name='search.html',
                      context={
                          'symptoms': get_list_of_symptoms(),
                          'result': sorted(result.keys(), key=lambda x: result[x])[:9],
                          'symptoms_str': 'Заболевания с симптомами: ' + ', '.join(request.GET).capitalize()
                      })

class AllDiseasesView(View):
    def get(self, request, *args, **kwargs):
        diseases = list(Disease.objects.all())
        print(diseases)
        return render(request,
                      template_name='search.html',
                      context={
                          'symptoms': get_list_of_symptoms(),
                          'result': diseases,
                          'symptoms_str': 'Все заболевания'
                      })
