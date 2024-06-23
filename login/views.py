import json
from django.shortcuts import render,render_to_response
from django.http import JsonResponse
from login.models import SpManager,SpRole,SpPermissionApi
from login.token_util import decode_token,encode_token
from django.views.decorators.csrf import csrf_exempt
from operator import itemgetter
from django.contrib.auth.hashers import check_password
# Create your views here.
@csrf_exempt
def login_check(request):
    '''登陆校验视图'''
    # request.POST 保存的是post方式提交的参数 QueryDict
    # 表单形式提交request.POST接收
    # json数据形式提交request.body接收
    recive_data = json.loads(request.body.decode('utf-8'))
    username = recive_data['username']
    password = recive_data['password']
    print(username," ",password)
    list = SpManager.objects.filter(mag_name=username)
    if len(list) > 0 and check_password(password, list[0].mg_pwd):
        manager = list[0]
        if manager.mg_state != 1:
            return JsonResponse({
                'meta': {
                    'msg': '用户未激活',
                    'status': 500,
                }
            })
        return JsonResponse({
            'data': {
                'id': manager.mg_id,
                'rid': manager.role_id,
                'username': manager.mag_name,
                'mobile': manager.mg_mobile,
                'email': manager.mg_email,
                'token': encode_token(manager.mag_name, password)
            },
            'meta': {
                'msg': '登陆成功',
                'status': 200,
            }
        })
    else:
        return JsonResponse({
             'meta': {
                'msg': '登陆失败',
                'status': 404,
            }
        })
def get_menu(request):
    # 获取请求头的数据 request.META.get('HTTP_KEY')  KEY必须是大写的
    #获取用户信息
    user = decode_token(request.META.get('HTTP_AUTHORIZATION'))
    #用户检验
    list = SpManager.objects.filter(mag_name=user[0])
    if len(list) > 0:
        permissionApis = SpPermissionApi.objects.all()
        rid = list[0].role_id
        if rid == 0:
            result = authFn(rid, None, permissionApis)
            return JsonResponse({
                'data': result,
                'meta': {
                    'msg': '登陆成功',
                    'status': 200,
                }
            }, safe=False)
        else:
            role = SpRole.objects.filter(role_id=rid)
            if len(role)!=0:
                rolePermissions = role[0].ps_ids.split(',')
                keyRolePermissions = {}
                for rolePermission in rolePermissions:
                    keyRolePermissions[int(rolePermission)] = True
                result = authFn(rid, keyRolePermissions, permissionApis)
                return JsonResponse({
                    'data': result,
                    'meta': {
                        'msg': '登陆成功',
                        'status': 200,
                    }
                }, safe=False)
            else:
                return JsonResponse({
                    'meta': {
                        'msg': '无权限访问',
                        'status': 404,
                    }
                })

    else:
        return JsonResponse({
            'meta': {
                'msg': '无权限访问',
                'status': 404,
            }
        })
#处理菜单
def authFn(rid,keyRolePermissions,permissionApis):
    rootPermissionsResult = {}
    #处理一级菜单
    for permissionApi in permissionApis:
        if permissionApi.ps.ps_level == '0':
            if rid != 0:
                if permissionApi.ps_id not in keyRolePermissions.keys():
                    continue
            rootPermissionsResult[permissionApi.ps_id] = {
                'id': permissionApi.ps_id,
                'authName': permissionApi.ps.ps_name,
                'path': permissionApi.ps_api_path,
                'children': [],
                'order': permissionApi.ps_api_order
            }

    #处理二级菜单
    for permissionApi in permissionApis:
        if permissionApi.ps.ps_level == '1':
            if rid != 0:
                if permissionApi.ps_id not in keyRolePermissions.keys():
                        continue
            parentPermissionResult = rootPermissionsResult[permissionApi.ps.ps_pid]
            if parentPermissionResult:
                parentPermissionResult['children'].append({
                    'id': permissionApi.ps_id,
                    'authName': permissionApi.ps.ps_name,
                    'path': permissionApi.ps_api_path,
                    'children': [],
                    'order': permissionApi.ps_api_order
                })
    # 排序
    result = rootPermissionsResult.values()
    result = sorted(result,key=itemgetter('order'))
    return result


def index(request):
    return render_to_response("html/login.html")