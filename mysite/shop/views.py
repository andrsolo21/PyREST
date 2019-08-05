from django.shortcuts import render

# Create your views here.
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Person, Relatives, Imp
from django.db.models import Max

def hello(request):
    return HttpResponse('Hello, World')

def hello2(request):
    return HttpResponse('Hello2, World')

@csrf_exempt
def post(request):
    data = json.load(request)
    return JsonResponse(data=data)

@csrf_exempt
def imports(request):
    data = json.loads(request.body)
    if request.method == "POST":
        #for i in data['citizens']:
            #per = serialize(i)
            #per.save()
        checkPersones(data['citizens'])

        return HttpResponse(str(len(data['citizens'])))
    if request.method == "GET":
        return HttpResponse('get')

    return HttpResponse('none')
    #return JsonResponse(form_data)

def checkPersones(personesMap):
    personesList = []
    ids = set()
    imp_id = Imp.objects.all().aggregate(Max('import_id'))['import_id__max']
    imp = Imp(num = len(personesMap), import_id = imp_id + 1)
    imp.save()


    for i in personesMap:
        if i['citizen_id'] in ids:
            return None
        pers = Person(
            citizen_id = i['citizen_id'],
            import_id = imp,
            town = i['town'],
            street = i['street'],
            building = i['building'],
            appartement = i['appartement'],
            name = i['name'],
            birth_date = parseDate(i['birth_date']),
            gender = i['gender']
        )
        personesList.append(pers)
    for i in personesList:
        i.save()

def parseDate(s):
    #TODO Проверка даты на сегоддяшнюю дату + Check spelling
    #if len(s) != 11:
    #    return None
    m = s.split('.')
    if len(m) != 3:
        return None
    return '-'.join(m[::-1])