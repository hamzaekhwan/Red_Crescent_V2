

from polls.models import *
from rest_framework.views import *
from rest_framework.decorators import *
from rest_framework.response import *

from .models import *

from django.contrib.auth import get_user_model
from .serializers import *

import requests
from django.core.files.base import ContentFile
import base64,shortuuid

def send_sms(message,phone):
    params = {
                        "job_name": "marksJob",
                        "user_name": "sarchoms1",
                        "password": "Sarc@12345678",
                        "msg": message,
                        "sender":"SARC-Homs",
                        "to" : phone}

    url = "https://bms.syriatel.sy/API/SendSMS.aspx?"
    response = requests.post(url,params=params,verify=False)


def convert_base64(code64,name1,name2):    
       
            s = shortuuid.ShortUUID(alphabet="0123456789abcdef")
            otp = s.random(length=5)
            var=code64.split('/')[1]
            image_name =  otp+  '.'+var.split(';')[0]

            extension = image_name.split('.')[1].lower()

            image_name = '{}_{}.{}'.format( name1 , name2, extension)

            imgStr = code64.split(';base64')

            new_image = ContentFile(base64.b64decode(imgStr[1]), name=image_name)

            return new_image