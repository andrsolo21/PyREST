from django.shortcuts import render

# Create your views here.
import json
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Person, Relatives, Imp
from .MyError import MyError
from .Birthdays import Birthdays
from django.db.models import Max

@csrf_exempt
def post(request):
    data = json.load(request)
    return JsonResponse(data=data)

@csrf_exempt
def importsR(request):
    if request.method == "POST":
        data = json.loads(request.body)
        otv = checkPersones(data['citizens'])
        if not otv.isError():
            return JsonResponse({'data':{'import_id':str(otv.import_id)}}, status = 201)
        else:
            return JsonResponse(otv.as_json() ,status = otv.numError)

    return HttpResponse(status = 401)

@csrf_exempt
def patchImpR(request, imp, cit):
    if request.method == "PATCH":
        pers = getPerson(imp, cit)
        if not pers:
            return JsonResponse(MyError("person not found").as_json(),status = 403)

        data = json.loads(request.body)

        pers = changeProfile(data, pers)

        if pers.isError():
            return JsonResponse(pers.as_json(),status = pers.numError)

        return JsonResponse(dict( data = pers.as_json(getRelatives(pers.id))), status = 200)

    return HttpResponse(status = 501)

@csrf_exempt
def getImportR(request, imp):
    if request.method == "GET":
        perss, err = getImport(imp)
        if not err:
            return JsonResponse(perss.as_json(),status = perss.numError)
        return JsonResponse(dict( data = perss), status = 200)
    return HttpResponse(status = 501)

@csrf_exempt
def birthdayR(request, imp):
    if request.method == "GET":
        otv, err = getBirthdays(imp)
        if not err:
            return JsonResponse(otv.as_json(),status = otv.numError)
        return JsonResponse(dict( data = otv), status = 200)
    return HttpResponse(status = 501)

def getBirthdays(imp):
    rels = Relatives.objects.filter(import_id = imp)
    if not len(rels):
        return MyError('cannot find persones with this import_id', 404), False

    DRs = Birthdays()

    for i in rels:
        DRs.add(str(i.person_id.birth_date.month), str(i.relative_id))

    return DRs.generate(), True


def getImport(imp):
    perss = Person.objects.filter(import_id = imp)
    if not len(perss):
        return MyError('cannot find persones with this import_id', 404), False

    otv = []
    for i in perss:
        otv.append(i.as_json(getRelatives(i.id)))
    return otv, True

def changeProfile(data, pers):
    for i in data:
        if i == 'citizen_id':
            return MyError("field citizen_id cannot be rewritten")

        if i not in Person.forChange:
            return MyError("field " + str(i) + " does not exist")

        if i == 'town':
            pers.town = data['town']

        if i == 'street':
            pers.street = data['street']

        if i == 'building':
            pers.building = data['building']

        if i == 'appartement':
            pers.appartement = data['appartement']

        if i == 'name':
            pers.name = data['name']

        if i == 'gender':
            pers.gender = data['gender']

        if i == 'birth_date':
            date = parseDate(data['birth_date'])
            if not date:
                return MyError('cannot parse date')
            else:
                pers.birth_date = date



    if 'relatives' in data:
        pers = workWithRelatives(pers, set(data['relatives']))
        if pers.isError():
            return pers
    pers.save()
    return pers

def workWithRelatives(pers, futRel):
    """function for adding and deleting relatives"""
    lastRel = getRelatives(pers.id)

    toDel = lastRel - futRel
    toAdd = futRel - lastRel

    #return MyError("-".join(list(toDel)) + " * " + "+".join(list(toAdd)))

    for i in toDel:
        Relatives.objects.filter(import_id = pers.import_id, relative_id = pers.citizen_id, citizen_id = i).delete()
        Relatives.objects.filter(import_id = pers.import_id, relative_id = i, citizen_id = pers.citizen_id).delete()

    for i in toAdd:
        pers2 = getPerson(pers.import_id, i)
        if not pers2:
            return MyError("cannot find person i_id/c_id: " + str(pers.import_id) + "/" + str(i), 404)

        Relatives(
            import_id = pers.import_id,
            citizen_id = pers.citizen_id,
            relative_id = i,
            person_id = pers,
        ).save()

        Relatives(
            import_id = pers.import_id,
            citizen_id = i,
            relative_id = pers.citizen_id,
            person_id = pers2,
        ).save()
    return pers

def getRelatives(perId):
    """function for geting set of id relatives of person with perId"""
    rel = Relatives.objects.filter(person_id = perId) #.values('citizen_id')
    ids = set()
    for i in rel:
        ids.add(i.relative_id)
    #return set(rel['citizen_id'])
    return ids

def getPerson(imp, cit):
    """"""
    try:
        pers = Person.objects.filter(import_id = imp , citizen_id = cit)
    except:
        return MyError("DB error")
    if len(pers):
        return pers[0]
    return MyError("cannot find person i_id/c_id: " + str(imp) + "/" + str(cit))

def checkPersones(personesMap):
    personesList = []
    ids = set()

    #imp_id = Imp.objects.all().aggregate(Max('import_id'))['import_id__max']
    imp = Imp(num = len(personesMap))
    imp.save()

    for i in personesMap:
        if i['citizen_id'] in ids:
            deleteImport(imp.import_id)
            return MyError("citizen_id " + str(i) + "is duplicated")
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
                return MyError("person " + str(imp.import_id) + "/" +  str(personesMap[i]['citizen_id']) + " (imp/cit) has nonexistent relative: " + str(j))
            Relatives(
                import_id = imp,
                citizen_id = personesMap[i]['citizen_id'],
                relative_id = j,
                person_id = personesList[i]
            ).save()
    return imp

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