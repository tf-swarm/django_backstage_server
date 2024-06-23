from django.shortcuts import render,render_to_response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import UserInfo

# Create your views here.
def hello(request):
    return JsonResponse({
        'result': 200,
        'msg': '连接成功'
    })
def registerPage(request):
    return render_to_response("html/register.html")

