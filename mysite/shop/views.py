from django.shortcuts import render

# Create your views here.
import json
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Person, Relatives, Imp, forChange
from .MyError import MyError
from .Birthdays import Birthdays
from .TownYearsPerc import TownYearsPerc
from django.db import transaction, DataError, Error
from django import FieldError
import datetime
import numpy as np

@csrf_exempt
def post(request):

    """
    It is the mirror
    :param request: http request
    :return: http response
    """

    data = json.load(request)
    return JsonResponse(data=data)

@csrf_exempt
def importsR(request):

    """
    Handler for the first request in SfYBS(ship for yandex backend school)
    :param request: http request
    :return: http response
    """

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

    """
    Handler for the second request in SfYBS(ship for yandex backend school)
    :param request: http request
    :param imp: number of import_id of the person
    :param cit: number of citizen_id of the person
    :return: http response
    """

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

    """
    Handler for the third request in SfYBS(ship for yandex backend school)
    :param request: http request
    :param imp: number of import_id of the persons
    :return: http response
    """

    if request.method == "GET":
        perss, err = getImport(imp)
        if not err:
            return JsonResponse(perss.as_json(),status = perss.numError)
        return JsonResponse(dict( data = perss), status = 200)
    return HttpResponse(status = 501)

@csrf_exempt
def birthdayR(request, imp):


    """
    Handler for the fourth request in SfYBS(ship for yandex backend school)
    :param request: http request
    :param imp: number of import_id of the persons
    :return: http response
    """

    if request.method == "GET":
        otv, err = getBirthdays(imp)
        if not err:
            return JsonResponse(otv.as_json(),status = otv.numError)
        return JsonResponse(dict( data = otv), status = 200)
    return HttpResponse(status = 501)

@csrf_exempt
def townBirthdayR(request, imp):

    """
    Handler for the fiveth request in SfYBS(ship for yandex backend school)
    :param request: http request
    :param imp: number of import_id of the persons
    :return: http response
    """

    if request.method == "GET":
        otv, err = townBirtdays(imp)
        if not err:
            return JsonResponse(otv.as_json(),status = otv.numError)
        return JsonResponse(dict( data = otv), status = 200)
    return HttpResponse(status = 501)

def townBirtdays(imp):

    """
    Function help fiveth handler
    :param imp: number of import_id
    :return:
        good exodus: list percentiles | TRUE
        bad exodus: MyError with mail, that persons not found | FALSE
    """

    pers = Person.objects.filter(import_id = imp)
    if not len(pers):
        return MyError('cannot find persons with this import_id', 404), False



    TYP = TownYearsPerc()

    for per in pers:
        TYP.add(per.town,per.getAge)

    return TYP.export(), True

def getBirthdays(imp):

    """
    Function help fourth handler
    :param imp: number of import_id
    :return:
        good exodus: dictionary with month, citizen_id's and counts | TRUE
        bad exodus: MyError with mail, that persons not found | FALSE
    """

    rels = Relatives.objects.filter(import_id = imp)
    if not len(rels):
        return MyError('cannot find persons with this import_id', 404), False

    DRs = Birthdays()

    for i in rels:
        DRs.add(str(i.person_id.birth_date.month), str(i.relative_id))

    return DRs.generate(), True

def getImport(imp):

    """
    Function help third handler
    :param imp: number of import_id
    :return:
        good exodus: list of persons in dict, which is rady for JSON | TRUE
        bad exodus: MyError with mail, that persons not found | FALSE
    """

    perss = Person.objects.filter(import_id = imp)
    if not len(perss):
        return MyError('cannot find persones with this import_id', 404), False

    otv = []
    for i in perss:
        otv.append(i.as_json(getRelatives(i.id)))
    return otv, True

def changeProfile(data, pers):

    """
    Function help second handler
    :param data: dictionary with new changing fields
    :param pers: Person(Model) old data
    :return:
        good exodus: person's dictionary
        bad exodus: MyError with mail of error
    """

    for i in data:
        if i == 'citizen_id':
            return MyError("field citizen_id cannot be rewritten")

        if i not in forChange:
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

    """
    function for adding and deleting relatives
    :param pers: Person(Model) old Data
    :param futRel: set of future relatives
    :return:
        good exodus: Person(Model) review data
        bad exodus: MyError with mail of error
    """

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

    """
    function for geting set of id relatives of person with perId
    :param perId: person_id
    :return: set with relatives
    """

    rel = Relatives.objects.filter(person_id = perId) #.values('citizen_id')
    ids = set()
    for i in rel:
        ids.add(i.relative_id)
    #return set(rel['citizen_id'])
    return ids

def getPerson(imp, cit):

    """

    :param imp: import_id of person
    :param cit: citizen_id of person
    :return:
        good exodus: Person(Model)
        bad exodus: MyError with mail of error
    """

    try:
        pers = Person.objects.filter(import_id = imp , citizen_id = cit)
    except:
        return MyError("DB error")
    if len(pers):
        return pers[0]
    return MyError("cannot find person i_id/c_id: " + str(imp) + "/" + str(cit))

#@transaction.atomic
def checkPersones(personesMap):

    """
    Function help first handler
    :param personesMap: list of new persons
    :return: import Imp(Model)
        if error return MyError
    """

    if not len(personesMap):
        return MyError("persones list is empty")

    personesList = []
    ids = set()

    #imp_id = Imp.objects.all().aggregate(Max('import_id'))['import_id__max']
    imp = Imp(num = len(personesMap))
    imp.save()

    try:
        with transaction.atomic():

            for i in personesMap:
                if checkKeys(i):
                    deleteImport(imp.import_id)
                    return checkKeys(i)
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

    except DataError:
        deleteImport(imp.import_id)
        #do_stuff()
        return MyError("Error")

    except Error:
        deleteImport(imp.import_id)
        #do_stuff()
        return MyError("Erro3r")

    return imp

def deleteImport(import_id):

    """
    Delete all objects with import_id
    :param import_id:
    :return: None
    """

    Relatives.objects.filter(import_id=import_id).delete()
    Person.objects.filter(import_id=import_id).delete()
    Imp.objects.filter(import_id=import_id).delete()

def parseDate(s):

    """
    Function validate s
    :param s: string like DD.MM.YYYY
    :return:
        good exodus: string like YYYY-MM-DD
        bad exodus: None
    """


    #if len(s) != 11:
    #    return None
    m = s.split('.')
    if len(m) != 3:
        return None
    date = datetime.date.today()
    try:
        if date.year < int(m[2]):
            return None
        if date.year == int(m[2]):
            if date.month < int(m[1]):
                return None
            if date.month == int(m[1]):
                if date.day < int(m[0]):
                    return None
    except:
        return None

    return '-'.join(m[::-1])

def checkKeys(di):

    """
    function for checking fields in dictionary
    :param di: dictionary for checking
    :return:
            good exodus: None
            bad exodus: MyError
    """

    if 'town' not in di or 'street' not in di or 'building' not in di or 'appartement' not in di or 'name' not in di or 'birth_date' not in di or 'gender' not in di or 'relatives' not in di or 'citizen_id' not in di:
        return MyError("problem with name of fields")
    return None