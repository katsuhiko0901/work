from django.shortcuts import render
from .models import Ai_analysis_log
# 2024/11/10 K.Matsuura UPD START
# from .forms import PathForm
import os
from .forms import UploadFileForm
from django.utils.crypto import get_random_string
# >>>--- 2024/11/10 K.Matsuura UPD END
import datetime 
import requests
import json

def index(request):
    # 2024/11/10 K.Matsuura UPD START --->>>
    # pathform = PathForm()
    uploadfileform = UploadFileForm()
    # >>>--- 2024/11/10 K.Matsuura UPD END
    context = {
        # 2024/11/10 K.Matsuura UPD START --->>>
        # 'pathform':pathform ,
        # 'explanation':'(例) /image/d03f1d36ca69348c51aa/c413eac329e1c0d03/test.jpg'
        'uploadfileform' : uploadfileform
        # >>>--- 2024/11/10 K.Matsuura UPD END
    }
    return render(request,'ai_analysis/index.html', context)
    
def create(request):

    # 2024/11/10 K.Matsuura UPD START --->>>
    # image_path = request.POST.get('PathForm')
    #
    # url = 'http://example.com' # 本番用
    # url = 'http://localhost:8000/api_mock/'
    #
    # session = requests.session()    
    #
    # headers = {'Content-Type':'application/json'}
    #
    # data = {
    #    "image_path": image_path
    # }
    # 
    #     json_data = json.dumps(data)
    # 
    #     err = 0
    #     try:
    #         response_data = session.post(url,data=json_data,headers=headers)
    #         r = json.loads(response_data.text)
    #     
    #         success = r['success']
    #         message = r['message']
    #         if success == 'True' :
    #             cls = r['estimated_data']['class']
    #             confidence = r['estimated_data']['confidence']
    #         else:
    #            cls = None
    #            confidence = None
    #             err = 1 
    #    except Exception:
    #        success = False
    #        message = 'Unexpected errors occuered'
    #         cls = None
    #        confidence = None
    #        err = 1
    
    ai_analysis_log =  Ai_analysis_log()

    # 正常終了以外はこの内容を画面表示（err = 1の場合はログ保存対象外とする）
    image_path = ''
    success = False
    message = 'Unexpected errors occuered'
    cls = None
    confidence = None
    err = 1

    if request.method == 'POST' :

        uploadfileform = UploadFileForm(request.POST , request.FILES)

        if uploadfileform.is_valid() :
            # アップロードするフォルダを作成
            save_dir = get_random_string(20) 
            os.mkdir('img/' + save_dir)
            save_dir2 = get_random_string(17) 
            os.mkdir('img/' + save_dir + '/' + save_dir2)
            image_path = 'img/' + save_dir + '/' + save_dir2 + '/' + request.FILES['file'].name
            handle_uploaded_file(request.FILES['file'] , image_path)            

            # url = 'http://example.com' # 本番用
            url = 'http://localhost:8000/api_mock/'

            session = requests.session()    

            headers = {'Content-Type':'application/json'}

            data = {
                "image_path": image_path
            }
            print(data)
            json_data = json.dumps(data)

            try:
                response_data = session.post(url,data=json_data,headers=headers)
                r = json.loads(response_data.text)
            
                success = r['success']
                message = r['message']
                if success == 'True' :
                    cls = r['estimated_data']['class']
                    confidence = r['estimated_data']['confidence']
                    err = 0
            except Exception:
                pass
        else:
            uploadfileform = UploadFileForm()
    else:
        uploadfileform = UploadFileForm()
    # >>>--- 2024/11/10 K.Matsuura UPD END   

    # 2024/11/10 K.Matsuura DEL START --->>>    
    # pathform = PathForm()
    # >>>--- 2024/11/10 K.Matsuura DEL END    
    dt_now = datetime.datetime.now() + datetime.timedelta(hours=9)
    ai_analysis_log.image_path = image_path
    ai_analysis_log.success = success
    ai_analysis_log.message = message
    ai_analysis_log.cls = cls
    ai_analysis_log.confidence = confidence
    ai_analysis_log.request_timestamp = dt_now
    ai_analysis_log.response_timestamp = dt_now
    
    if err == 0:
        ai_analysis_log.save()

    context = {
        # 2024/11/10 K.Matsuura UPD START --->>>
        # 'pathform':pathform ,
        # 'explanation':'(例) /image/d03f1d36ca69348c51aa/c413eac329e1c0d03/test.jpg' ,       
        'uploadfileform' : uploadfileform,
        # >>>--- 2024/11/10 K.Matsuura UPD END
        'ai_analysis_log': ai_analysis_log
    }
    return render(request,'ai_analysis/index.html', context)

# 2024/11/10 K.Matsuura ADD START --->>>
def handle_uploaded_file(file_obj, upload_path) :
    with open(upload_path, 'wb+') as destination:
        for chunk in file_obj.chunks() :
            destination.write(chunk)
# >>>--- 2024/11/10 K.Matsuura ADD END    
