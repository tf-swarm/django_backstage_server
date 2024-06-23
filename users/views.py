from django.shortcuts import render
import json
import math
import time
from django.http import JsonResponse
from login.models import SpManager,SpRole,SpPermission
from login.token_util import decode_token
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password
# Create your views here.
'''
获取所有管理员
查询条件统一规范
 '''
def getAllUsers(request):
    # 获取请求头的数据 request.META.get('HTTP_KEY')  KEY必须是大写的
    # 获取用户信息
    user = decode_token(request.META.get('HTTP_AUTHORIZATION'))
    # 用户检验
    list = SpManager.objects.filter(mag_name=user[0])
    if len(list) > 0:
        query = request.GET.get('query')
        pagenum = int(request.GET.get('pagenum'))
        pagesize = int(request.GET.get('pagesize'))
        if query == '':
            managers = SpManager.objects.all()
        else:
            managers = SpManager.objects.filter(mag_name__contains=query)
        #总数total
        total = len(managers)
        #防止查询大于本身数据的页数
        if pagenum > math.ceil(total/pagesize):
            pagenum = 1
        pagtor = Paginator(managers,pagesize).page(pagenum)
        # print(ptr)
        retManagers = []
        for manager in pagtor:
            role = SpRole.objects.filter(role_id=manager.role_id)
            if(len(role)==0):
                if manager.role_id == 0:
                    role_name = '超级管理员'
                else:
                    role_name = '普通用户'
            else:
                role_name = role[0].role_name
            retManagers.append({
                'id': manager.mg_id,
                'role_name': role_name,
                'username': manager.mag_name,
                'create_time': manager.mg_time,
                'mobile': manager.mg_mobile,
                'email': manager.mg_email,
                'mg_state': manager.mg_state == 1
            })
        resultData = {}
        resultData['total'] = total
        resultData['pagenum'] = pagenum
        resultData['users'] = retManagers
        return JsonResponse({
                    'data': resultData,
                    'meta': {
                        'msg': '查找成功',
                        'status': 200,
                    }
        })
    else:
        return JsonResponse({
            'meta': {
                'msg': '无权限访问',
                'status': 404,
            }
        })


'''
创建管理员
 '''
@csrf_exempt
def createManager(request):
    # 获取请求头的数据 request.META.get('HTTP_KEY')  KEY必须是大写的
    # 获取用户信息
    user = decode_token(request.META.get('HTTP_AUTHORIZATION'))
    # 用户检验
    list = SpManager.objects.filter(mag_name=user[0])
    if len(list)>0:
        recive_data = json.loads(request.body.decode('utf-8'))
        username = recive_data['username']
        #判断是否存在同名
        if len(SpManager.objects.filter(mag_name=username))> 0:
            return JsonResponse({
                'meta': {
                    'msg': '用户名已存在',
                    'status': 404,
                }
            })
        else:
            password = recive_data['password']
            password = make_password(password)
            email = recive_data['email']
            mobile = recive_data['mobile']
            mg_time = int(time.time())
            manager = SpManager.objects.create(
                mag_name=username,
                mg_pwd=password,
                mg_email=email,
                mg_mobile=mobile,
                mg_time=mg_time,
                role_id=-1,
                mg_state=1
            )
            return JsonResponse({
                "data": {
                    "id": manager.mg_id,
                    "username": manager.mag_name,
                    "mobile": manager.mg_mobile,
                    "email": manager.mg_email,
                    "role_id": manager.role_id,
                    "create_time": manager.mg_time
			    },
                "meta": {
                    "msg": "用户创建成功",
                    "status": 201
                }
            })
    else:
        return JsonResponse({
            'meta': {
                'msg': '无权限访问',
                'status': 404,
            }
        })


'''
更新用户状态
'''
@csrf_exempt
def updateActiveManager(request, mg_id, state):
    # 获取请求头的数据 request.META.get('HTTP_KEY')  KEY必须是大写的
    # 获取用户信息
    user = decode_token(request.META.get('HTTP_AUTHORIZATION'))
    # 用户检验
    list = SpManager.objects.filter(mag_name=user[0])
    if len(list) > 0:
        manager = SpManager.objects.get(mg_id=mg_id)
        if manager.role_id != 0:
            if state == 'true':
                manager.mg_state = 1
            else:
                manager.mg_state = 0
            manager.save()
            return JsonResponse({
                "data": {
                    "id": manager.mg_id,
                    "username": manager.mag_name,
                    "mobile": manager.mg_mobile,
                    "email": manager.mg_email,
                    "rid": manager.role_id,
                    "mg_state": manager.mg_state
                },
                "meta": {
                    "msg": "设置状态成功",
                    "status": 200
                }
            })
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
'''
GET:根据id查询用户
PUT:更新用户
DELETE:删除用户
'''
@csrf_exempt
def updateManager(request,mg_id):
    if request.method == 'GET':
        manager = SpManager.objects.get(mg_id=mg_id)
        return JsonResponse({
            "data": {
                "id": manager.mg_id,
                "username": manager.mag_name,
                "mobile": manager.mg_mobile,
                "email": manager.mg_email,
                "role_id": manager.role_id,
            },
            "meta": {
                "msg": "查询成功",
                "status": 200
            }
        })
    elif request.method == 'PUT':
        recive_data = json.loads(request.body.decode('utf-8'))
        email = recive_data['email']
        mobile = recive_data['mobile']
        manager = SpManager.objects.get(mg_id=mg_id)
        manager.mg_mobile = mobile
        manager.mg_email = email
        manager.save()
        return JsonResponse({
            "data": {
                "id": manager.mg_id,
                "username": manager.mag_name,
                "mobile": manager.mg_mobile,
                "email": manager.mg_email,
                "role_id": manager.role_id,
            },
            "meta": {
                "msg": "更新成功",
                "status": 200
            }
        })
    elif request.method == 'DELETE':
        manager = SpManager.objects.get(mg_id=mg_id)
        manager.delete()
        return JsonResponse({
            "data": None,
            "meta": {
                "msg": "删除成功",
                "status": 200
            }
        })



'''
获取角色列表
'''
def getRoles(request):
    # 获取请求头的数据 request.META.get('HTTP_KEY')  KEY必须是大写的
    # 获取用户信息
    user = decode_token(request.META.get('HTTP_AUTHORIZATION'))
    # 用户检验
    list = SpManager.objects.filter(mag_name=user[0])
    if len(list) > 0:
        roles = SpRole.objects.all()
        permissions = SpPermission.objects.all()
        permissionKeys = {}
        # ps_id怎么key permission作为value 存入字典中
        for permission in permissions:
            permissionKeys[permission.ps_id] = permission
        rolesResults = []
        for role in roles:
            permissionIds = role.ps_ids.split(',')
            rolesResult = {
                'id': role.role_id,
                'roleName': role.role_name,
                'roleDesc': role.role_desc,
                'children': [],
            }
            rolesResult['children'] = getPermissionsResult(permissionKeys,permissionIds)
            rolesResults.append(rolesResult)
            print(rolesResult)

        return JsonResponse({
            'data': rolesResults,
            'meta': {
                'msg': '登陆成功',
                'status': 200,
            }
        }, safe=False)
    else:
        return JsonResponse({
            'meta': {
                'msg': '获取成功',
                'status': 404,
            }
        })


def getPermissionsResult(permissionKeys,permissionIds):
    permissionsResult = {}
    # permissionIds中有权限时
    # permissionIds分割为列表时，空字符串会分割成含字符的列表
    if len(permissionIds) > 1:
        # 处理一级菜单
        for permissionId in permissionIds:
            if int(permissionId) in permissionKeys.keys():
                permission = permissionKeys[int(permissionId)]
                if permission.ps_level == '0':
                    permissionsResult[permission.ps_id] = {
                        'id': permission.ps_id,
                        'authName': permission.ps_name,
                        'path': None,
                        'children': []
                    }

        # 临时存储二级返回结果
        tmpResult = {}
        # 处理二级菜单
        for permissionId in permissionIds:
            if int(permissionId) in permissionKeys.keys():
                permission = permissionKeys[int(permissionId)]
                if permission.ps_level == '1':
                    parentPermissionResult = permissionsResult[permission.ps_pid]
                    if parentPermissionResult:
                        tmpResult[permission.ps_id] = {
                            'id': permission.ps_id,
                            'authName': permission.ps_name,
                            'path': None,
                            'children': [],
                        }
                        parentPermissionResult['children'].append(tmpResult[permission.ps_id])
        # 处理三级菜单
        for permissionId in permissionIds:
            if int(permissionId) in permissionKeys.keys():
                permission = permissionKeys[int(permissionId)]
                if permission.ps_level == '2':
                    parentPermissionResult = tmpResult[permission.ps_pid]
                    if parentPermissionResult:
                        parentPermissionResult['children'].append({
                            'id': permission.ps_id,
                            'authName': permission.ps_name,
                            'path': None,
                        })
    # permissionsResult.values()为dict_values类型
    # 必须转为列表
    return list(permissionsResult.values())


'''
分配用户角色
'''
@csrf_exempt
def setRole(request, mg_id):
    # 接收json请求参数
    receive_data = json.loads(request.body.decode('utf-8'))
    manager = SpManager.objects.get(mg_id=mg_id)
    role_id = receive_data['rid']
    if manager.role_id != 0:
        manager.role_id = role_id
        manager.save()
        return JsonResponse(
            {
                "data": {
                    "id": manager.mg_id,
                    "rid": role_id,
                    "username": manager.mag_name,
                    "mobile": manager.mg_mobile,
                    "email": manager.mg_email,
                },
                "meta": {
                    "msg": "设置角色成功",
                    "status": 200
                }
            }
        )
    else:
        return JsonResponse({
            "meta": {
                "msg": "设置角色失败",
                "status": 404
            }
        })
