from django.shortcuts import render
from django.http import HttpResponse
from .models import Ai_analysis_log
from .forms import PathForm
import re
import urllib.parse
import datetime 
import requests
import json

def index(request):
    pathform = PathForm()
    context = {
        'pathform':pathform ,
        'explanation':'(例) /image/d03f1d36ca69348c51aa/c413eac329e1c0d03/test.jpg'
    }
    return render(request,'ai_analysis/index.html', context)
    
def create(request):

    image_path = request.POST.get('PathForm')
    # url = 'http://example.com'
    url = 'http://localhost:8000/api_mock/'

    session = requests.session()    

    headers = {'Content-Type':'application/json'}

    data = {
        "image_path": image_path
    }

    json_data = json.dumps(data)

    response_data = session.post(url,data=json_data,headers=headers)
    r = json.loads(response_data.text)
 
    success = r['success']
    message = r['message']
    if success == 'True' :
        cls = r['estimated_data']['class']
        confidence = r['estimated_data']['confidence']
    else:
        cls = None
        confidence = None

    pathform = PathForm()
    dt_now = datetime.datetime.now() + datetime.timedelta(hours=9)
    ai_analysis_log =  Ai_analysis_log()
    ai_analysis_log.image_path = image_path
    ai_analysis_log.success = success
    ai_analysis_log.message = message
    ai_analysis_log.cls = cls
    ai_analysis_log.confidence = confidence
    ai_analysis_log.request_timestamp = dt_now
    ai_analysis_log.response_timestamp = dt_now
    
    ai_analysis_log.save()

    context = {
        'pathform':pathform ,
        'explanation':'(例) /image/d03f1d36ca69348c51aa/c413eac329e1c0d03/test.jpg' ,       
        'ai_analysis_log': ai_analysis_log
    }
    return render(request,'ai_analysis/index.html', context)

