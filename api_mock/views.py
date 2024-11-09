from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random

@csrf_exempt

def MockResponse(request):

    i = round(random.randrange(99999),0)

    if i % 5 != 0:
        data = {
            "success":"True",
            "message":"Success",
            "estimated_data":{"class":str(random.randrange(10)) , "confidence":str(random.randrange(10000)/10000) }
        }
    else:
        data = {
            "success":"False",
            "message":"E" + str(i),
            "estimated_data":{}
        }
    return JsonResponse(data)
