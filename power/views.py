from django.shortcuts import render
import json
from django.http import JsonResponse
from login.models import SpManager,SpPermissionApi,SpPermission,SpRole
from login.token_util import decode_token
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
'''
 获取全部权限
 list 类型
 tree 类型
'''
def getAllRights(request,type1):
    # 获取请求头的数据 request.META.get('HTTP_KEY')  KEY必须是大写的
    # 获取用户信息
    user = decode_token(request.META.get('HTTP_AUTHORIZATION'))
    # 用户检验
    managers = SpManager.objects.filter(mag_name=user[0])
    if len(managers) > 0:
        permissionApis = SpPermissionApi.objects.all()
        if type1 == 'list':
            result = []
            for permissionApi in permissionApis:
                result.append({
                    'id': permissionApi.ps_id,
                    'authName': permissionApi.ps.ps_name,
                    'pid': permissionApi.ps.ps_pid,
                    'level': permissionApi.ps.ps_level,
                    'path': permissionApi.ps_api_path
                })
            return JsonResponse({
                'data': result,
                'meta': {
                    'msg': '获取权限列表成功',
                    'status': 200
                }
            })
        else:
            keyCategories = {}
            # 显示一级
            permissionsResult = {}
            # 处理一级菜单
            for permissionApi in permissionApis:
                # 以ps_id 为key 以permisssionApi为value存储为字典keyCategories
                keyCategories[permissionApi.ps_id] = permissionApi

                if permissionApi.ps.ps_level == '0':
                    permissionsResult[permissionApi.ps_id] = {
                        'id': permissionApi.ps_id,
                        'authName': permissionApi.ps.ps_name,
                        'path': permissionApi.ps_api_path,
                        'pid': permissionApi.ps.ps_pid,
                        'children': []
                    }
            # 临时存储二级返回结果
            tmpResult = {}
            # 处理二级菜单
            for permissionApi in permissionApis:
                if permissionApi.ps.ps_level == '1':
                    # 当二级菜单的父级菜单不存在时，就不添加
                    if permissionApi.ps.ps_pid not in permissionsResult.keys():
                        continue
                    parentPermissionResult = permissionsResult[permissionApi.ps.ps_pid]
                    if parentPermissionResult:
                        tmpResult[permissionApi.ps_id] = {
                            "id": permissionApi.ps_id,
                            "authName": permissionApi.ps.ps_name,
                            "path": permissionApi.ps_api_path,
                            "pid": permissionApi.ps.ps_pid,
                            "children": []
                        }
                        parentPermissionResult['children'].append(tmpResult[permissionApi.ps_id])
            # print(permissionsResult)
            # 处理三级菜单
            for permissionApi in permissionApis:
                if permissionApi.ps.ps_level == '2':
                    # 当二级菜单的父级菜单不存在时，就不添加
                    if permissionApi.ps.ps_pid not in tmpResult.keys():
                        continue
                    parentPermissionResult = tmpResult[permissionApi.ps.ps_pid]
                    if parentPermissionResult:
                        parentPermissionResult['children'].append({
                            "id": permissionApi.ps_id,
                            "authName": permissionApi.ps.ps_name,
                            "path": permissionApi.ps_api_path,
                            "pid": str(permissionApi.ps.ps_pid) + "," +
                                   str(keyCategories[permissionApi.ps.ps_pid].ps.ps_pid)
                        })
            return JsonResponse({
                'data': list(permissionsResult.values()),
                'meta': {
                  'msg': '获取权限列表成功',
                  'status': 200
                }
            }, safe=False)
    else:
        return JsonResponse({
            'meta': {
                'msg': '无权限访问',
                'status': 404,
            }
        })
'''
GET ： 根据id查询角色
PUT ： 根据id编辑角色
DELETE ： 根据id删除角色
'''
@csrf_exempt
def getRoleById(request,rid):
    role = SpRole.objects.get(role_id=rid)
    if request.method == 'GET':
        return JsonResponse({
            'data': {
                "roleId": role.role_id,
                "roleName": role.role_name,
                "roleDesc": role.role_desc,
                "rolePermissionDesc": role.ps_ca
            },
            'meta': {
                "msg": "获取成功",
                "status": 200
            }
        })
    elif request.method == 'PUT':
        # 获取请求参数
        recive_data = json.loads(request.body.decode('utf-8'))
        role_desc = recive_data['roleDesc']
        role_name = recive_data['roleName']
        # 修改角色信息
        role.role_desc = role_desc
        role.role_name = role_name
        role.save()
        return JsonResponse({
            "data": {
                "roleId": role.role_id,
                "roleName": role_name,
                "roleDesc": role_desc
            },
            "meta": {
                "msg": "编辑成功",
                "status": 200
            }
        })
    else:
        role.delete()
        return JsonResponse({
            "data": None,
            "meta": {
                "msg": "删除成功",
                "status": 200
            }
        })
@csrf_exempt
# 删除角色特定权限
def deleteRoleRight(request,role_id,right_id):
    role = SpRole.objects.get(role_id=role_id)
    ps_ids = role.ps_ids.split(',')
    new_ps_ids = []
    # 存储新的权限
    for ps_id in ps_ids:
        if int(right_id) == int(ps_id):
            continue
        new_ps_ids.append(ps_id)
    # 将权限列表转成用逗号隔开的字符串
    new_ps_ids_string = ','.join(new_ps_ids)
    role.ps_ids = new_ps_ids_string
    # 更新数据库
    role.save()
    # 返回当前角色最新的权限数据
    permissions = SpPermission.objects.all()
    permissionKeys = {}
    # ps_id怎么key permission作为value 存入字典中
    for permission in permissions:
        permissionKeys[permission.ps_id] = permission
    # data中调用获取该角色权限的函数
    return JsonResponse({
        "data":getPermissionsResult(permissionKeys,new_ps_ids),
        "meta": {
            "msg": "取消权限成功",
            "status": 200
        }
    },safe=False)

'''
对角色进行授权
    rights权限是以逗号分割的字符串参数
'''
@csrf_exempt
def updateRoleRight(request,role_id):
    # 获取请求参数
    recive_data = json.loads(request.body.decode('utf-8'))
    is_str = recive_data['rids']
    role = SpRole.objects.get(role_id=role_id)
    role.ps_ids = is_str
    role.save()
    return JsonResponse({
        "data": None,
        "meta": {
            "msg": "更新成功",
            "status": 200
        }
    })

'''
获取角色列表
添加角色
'''
@csrf_exempt
def getRoles(request):
    # 获取请求头的数据 request.META.get('HTTP_KEY')  KEY必须是大写的
    # 获取用户信息
    user = decode_token(request.META.get('HTTP_AUTHORIZATION'))
    # 用户检验
    list = SpManager.objects.filter(mag_name=user[0])
    if len(list) > 0:
        # get请求 获取全部角色信息
        if request.method == 'GET':
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

            return JsonResponse({
                'data': rolesResults,
                'meta': {
                    'msg': '获取成功',
                    'status': 200,
                }
            }, safe=False)
        else:
            # post 请求
            # 实现角色的添加
            recive_data = json.loads(request.body.decode('utf-8'))
            role_desc = recive_data['roleDesc']
            role_name = recive_data['roleName']
            role = SpRole()
            role.role_name = role_name
            role.role_desc = role_desc
            role.save()
            return JsonResponse({
                "data": {
                    "roleId": role.role_id,
                    "roleName": role_name,
                    "roleDesc": role_desc
                },
                "meta": {
                    "msg": "创建成功",
                    "status": 201
                }
             })
    else:
        return JsonResponse({
            'meta': {
                'msg': '权限不足',
                'status': 404,
            }
        })

# 获取ids中的权限
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
                    # 当二级菜单的父级菜单不存在时，就不添加
                    if permission.ps_pid not in permissionsResult.keys():
                        continue
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
                    # 当三级菜单的父级菜单不存在时，不添加
                    if permission.ps_pid not in tmpResult.keys():
                        continue
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