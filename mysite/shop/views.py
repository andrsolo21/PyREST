from django.shortcuts import render

# Create your views here.
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
#from shop.shop.models import serialize, Person
from .func import serialize


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
        for i in data['citizens']:
            per = serialize(i)
            per.save()

        return HttpResponse(str(len(data['citizens'])))
    if request.method == "GET":
        return HttpResponse('get')

    return HttpResponse('none')
    #return JsonResponse(form_data)и