from django.shortcuts import render

# Create your views here.
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Person, Relatives, Imp
from django.db.models import Max

@csrf_exempt
def post(request):
    data = json.load(request)
    return JsonResponse(data=data)

@csrf_exempt
def imports(request):
    if request.method == "POST":
        data = json.loads(request.body)
        otv = checkPersones(data['citizens'])
        if otv:
            return JsonResponse({'data':{'import_id':str(otv)}}, status = 201)
        else:
            return HttpResponse(status = 400)

    return HttpResponse(status = 501)

@csrf_exempt
def patchImp(request, imp, cit):
    if request.method == "PATCH":
        data = json.loads(request.body)
        return HttpResponse(str(imp) + str(cit), status = 201)
    return HttpResponse(status = 201)

def checkPersones(personesMap):
    personesList = []
    ids = set()
    relativeList = []

    #imp_id = Imp.objects.all().aggregate(Max('import_id'))['import_id__max']
    imp = Imp(num = len(personesMap))
    imp.save()

    for i in personesMap:
        if i['citizen_id'] in ids:
            deleteImport(imp.import_id)
            return None
        ids.add(i['citizen_id'])

    for i in personesMap:

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

    for i in range(len(personesMap)):

        personesList[i].save()
        for j in personesMap[i]['relatives']:
            if j not in ids:
                deleteImport(imp.import_id)
                return None
            Relatives(
                import_id = imp,
                citizen_id = personesMap[i]['citizen_id'],
                relative_id = j,
                person_id = personesList[i]
            ).save()
    return imp.import_id

def deleteImport(import_id):
    Relatives.objects.filter(import_id=import_id).delete()
    Person.objects.filter(import_id=import_id).delete()
    Imp.objects.filter(import_id=import_id).delete()

def parseDate(s):
    #TODO Проверка даты на сегоддяшнюю дату + Check spelling
    #if len(s) != 11:
    #    return None
    m = s.split('.')
    if len(m) != 3:
        return None
    return '-'.join(m[::-1])