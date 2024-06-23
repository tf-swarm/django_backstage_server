from django.shortcuts import render
import datetime
import time
import json
import math
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from goods.models import SpCategory,SpAttribute,SpGoods,SpGoodsPics,SpGoodsAttr,SpGoodsCats
from django.http import JsonResponse
# Create your views here.

'''
GET:查询全部商品
POST:添加商品
'''
@csrf_exempt
def getAllGoods(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        pagenum = int(request.GET.get('pagenum'))
        pagesize = int(request.GET.get('pagesize'))
        if query == '':
            Allgoods = SpGoods.objects.all()
        else:
            Allgoods = SpGoods.objects.filter(goods_name__contains=query,is_del=0)
        #总数
        total = len(Allgoods)
        # 防止查询大于本身数据的页数
        if pagenum > math.ceil(total / pagesize):
            pagenum = 1
        pagtor = Paginator(Allgoods, pagesize).page(pagenum)
        resGoods = []
        for goods in pagtor:
            resGoods.append({
                "goods_id": goods.goods_id,
                "goods_name": goods.goods_name,
                "goods_price": goods.goods_price,
                "goods_number": goods.goods_number,
                "goods_weight": goods.goods_weight,
                "goods_state": goods.goods_state,
                "add_time": goods.add_time,
                "upd_time": goods.upd_time,
                "hot_mumber": goods.hot_mumber,
                "is_promote": goods.is_promote == 1
            })
        resultData = {}
        resultData['total'] = total
        resultData['pagenum'] = pagenum
        resultData['goods'] = resGoods
        return JsonResponse({
            'data': resultData,
            'meta': {
                'msg': '获取成功',
                'status': 200,
            }
        })
    #  商品的添加
    elif request.method == 'POST':
        receive_data = json.loads(request.body.decode('utf-8'))
        try:
            # 获取分类三层的id
            goods_cat = receive_data['goods_cat'].split(',')
            goods = SpGoods.objects.create(
                goods_name=receive_data['goods_name'],
                goods_introduce=receive_data['goods_introduce'],
                goods_number=receive_data['goods_number'],
                goods_price=float(receive_data['goods_price']),
                goods_weight=float(receive_data['goods_weight']),
                is_del=0,
                cat_id=goods_cat[2],
                add_time=int(time.time()),
                upd_time=int(time.time()),
                cat_one_id=goods_cat[0],
                cat_two_id=goods_cat[1],
                cat_three_id=goods_cat[2],
                hot_mumber=0,
                is_promote=0,
                goods_state=0
            )
            # print(goods.goods_id)
            # 存储商品对应的分类
            for cat in goods_cat:
                if len(SpGoodsCats.objects.filter(cat_id=int(cat))) == 0:
                    category = SpCategory.objects.get(cat_id=int(cat))
                    SpGoodsCats.objects.create(
                        cat_id=category.cat_id,
                        parent_id=category.cat_pid,
                        cat_name=category.cat_name,
                        is_show=1,
                        cat_sort=0,
                        data_flag=1,
                        create_time=int(time.time())
                    )
            # print(goods_cat)
            # 存储商品对应的图片
            if len(receive_data['pics'])>0:
                pics = receive_data['pics'][0]['pic']
                SpGoodsPics.objects.create(
                    goods_id = goods.goods_id,
                    img=pics,
                    is_temp=0,
                )
                # print(pics)

            # 存储商品对应的参数
            for attr in receive_data['attrs']:
                SpGoodsAttr.objects.create(
                    goods_id=goods.goods_id,
                    attr_id=attr['attr_id'],
                    attr_value=attr['attr_value'],
                    add_price=0,
                )
            # print(receive_data['attrs'])
            return JsonResponse({
                "data": None,
                "meta": {
                    "msg": "创建商品成功",
                    "status": 201
                }
            })
        except:
            return JsonResponse({
                "data": None,
                "meta": {
                    "msg": "创建商品失败",
                    "status": 404
                }
            })

# 暂存图片
@csrf_exempt
def upload(request):
    if request.method == 'POST':
        # 获取图片
        img = request.FILES.get('file')
        # 存取图片
        pic = SpGoodsPics()
        pic.img = img
        pic.is_temp = 1
        pic.save()
        return JsonResponse({
            "data": {
                "tmp_path": str(pic.img),
            },
            "meta": {
                "msg": "上传成功",
                "status": 200
            }
        })

'''
DELETE：删除商品，图片'''
@csrf_exempt
def goodsManage(request,goods_id):
    goods = SpGoods.objects.get(goods_id=goods_id)
    if request.method == 'DELETE':
        goods.is_del = 1
        goods.save()
        # goods.delete()
        # 删除商品相关的参数、图片
        SpGoodsAttr.objects.filter(goods_id = goods_id).delete()
        SpGoodsPics.objects.filter(goods_id__isnull=True).delete()
        SpGoodsPics.objects.filter(goods_id = goods_id).delete()
        return JsonResponse({
            "data": None,
            "meta": {
                "msg": "删除成功",
                "status": 200
            }
        })



'''
GET请求根据id查询参数
PUT请求编辑参数
DELETE请求删除删除
'''
@csrf_exempt
def attrManage(request,cat_id,attr_id):
    attr = SpAttribute.objects.get(attr_id=attr_id)
    if request.method == 'GET':
        return JsonResponse({
            "data": {
                "attr_id": attr.attr_id,
                "attr_name": attr.attr_name,
                "cat_id": attr.cat_id,
                "attr_sel": attr.attr_sel,
                "attr_write": attr.attr_write,
                "attr_vals": attr.attr_vals
            },
            "meta": {
                "msg": "获取成功",
                "status": 200
            }
        })
    elif request.method == 'PUT':
        receive_data = json.loads(request.body.decode('utf-8'))
        attr.attr_name = receive_data['attr_name']
        if 'attr_vals' in receive_data.keys():
            attr.attr_vals = receive_data['attr_vals']
        attr.save()
        return JsonResponse({
            "data": {
                "attr_id": attr.attr_id,
                "attr_name": attr.attr_name,
                "cat_id": attr.cat_id,
                "attr_sel": attr.attr_sel,
                "attr_write": attr.attr_write,
                "attr_vals": attr.attr_vals
            },
            "meta": {
                "msg": "更新成功",
                "status": 200
            }
        })
    else:
        attr.delete()
        return JsonResponse({
            "data": None,
            "meta": {
                "msg": "删除成功",
                "status": 200
            }
        })

'''
GET参数列表查询
POST 添加参数
'''
@csrf_exempt
def getAttributes(request,cat_id):
    if request.method == 'GET':
        sel = request.GET.get('sel')
        # 多条件查询
        attributes = SpAttribute.objects.filter(cat_id=cat_id,attr_sel=sel)
        # 返回列表字典数据
        attrResult = []
        for attr in attributes:
            attrResult.append({
                "attr_id": attr.attr_id,
                "attr_name": attr.attr_name,
                "cat_id": attr.cat_id,
                "attr_sel": attr.attr_sel,
                "attr_write": attr.attr_write,
                "attr_vals": attr.attr_vals
            })
        return JsonResponse({
            "data": attrResult,
            "meta": {
                "msg": "获取成功",
                "status": 200
            }
        },safe=False)
    elif request.method == 'POST':
        # 获取post请求参数
        receive_data = json.loads(request.body.decode('utf-8'))
        name = receive_data['attr_name']
        sel = receive_data['attr_sel']
        # 保存参数
        attr = SpAttribute()
        attr.attr_name = name
        attr.attr_sel = sel
        attr.cat_id = cat_id
        attr.attr_write = 'manual'
        attr.save()
        return JsonResponse({
            "data": {
                "attr_id": attr.attr_id,
                "attr_name": attr.attr_name,
                "cat_id": attr.cat_id,
                "attr_sel": attr.attr_sel,
                "attr_write": attr.attr_write,
                "attr_vals": attr.attr_vals
            },
            "meta": {
                "msg": "创建成功",
                "status": 201
            }
        })

'''
根据商品分类id查询相关信息
根据商品分类id更新数据
根据商品分类id删除数据
'''
@csrf_exempt
def catManage(request, id):
    cat = SpCategory.objects.get(cat_id=id)
    if request.method == 'GET':
        return JsonResponse({
            "data": {
                "cat_id": cat.cat_id,
                "cat_name": cat.cat_name,
                "cat_pid": cat.cat_pid,
                "cat_level": cat.cat_level
            },
            "meta": {
                "msg": "获取成功",
                "status": 200
            }
        })
    elif request.method == 'PUT':
        cat_name = json.loads(request.body.decode('utf-8'))['cat_name']
        cat.cat_name = cat_name
        cat.save()
        return JsonResponse({
            "data": {
                "cat_id": cat.cat_id,
                "cat_name": cat.cat_name,
                "cat_pid": cat.cat_pid,
                "cat_level": cat.cat_level
            },
            "meta": {
                "msg": "更新成功",
                "status": 200
            }
        })
    else:
        cat.delete()
        return JsonResponse({
            "data": None,
            "meta": {
                "msg": "删除成功",
                "status": 200
            }
        })
'''
获取全部参数
get 请求带参数的
get 请求不带参数的
'''
@csrf_exempt
def getAllCategories(request):
    if request.method == 'GET':
        # 获取请求参数
        print(datetime.datetime.now())
        ty = int(request.GET.get('type',default=3))
        pagenum = int(request.GET.get('pagenum',default=-1))
        pagesize = int(request.GET.get('pagesize',default=-1))
        # 获取所有category数据
        categories = SpCategory.objects.all()
        # 字典存取categories
        keyCategories = {}
        for category in categories:
            keyCategories[category.cat_id] = category
        result = list(getTreeResult(keyCategories,categories,ty).values())
        if pagenum == -1:
            return JsonResponse({
                'data': result,
                'meta': {
                    'msg': '获取成功',
                    'status': 200
                }
            }, safe=False)
        total = len(result)
        result = result[(pagenum-1)*pagesize:((pagenum-1)*pagesize)+pagesize]
        print(datetime.datetime.now())
        return JsonResponse({
            'data': {
                'result': result,
                'total': total,
                'pagenum': pagenum,
                'pagesize': pagesize
            },
            'meta': {
                'msg': '获取成功',
                'status': 200
            }
        }, safe=False)
    else:
        #获取post请求参数
        receive_data = json.loads(request.body.decode('utf-8'))
        cat_level = receive_data['cat_level']
        cat_name = receive_data['cat_name']
        cat_pid = receive_data['cat_pid']
        #添加分类
        cat = SpCategory()
        cat.cat_level = cat_level
        cat.cat_name = cat_name
        cat.cat_pid = cat_pid
        cat.cat_deleted = 0
        cat.save()
        return JsonResponse({
            "meta": {
                "msg": "创建成功",
                "status": 201
            }
        })
'''
返回参数字典
'''
def getTreeResult(keyCategories,categories,ty):
    #显示一级
    result = {}
    #处理一级
    for cat in categories:
        # 判断是否被删除
        if isDelete(keyCategories,cat):
            continue
        if cat.cat_pid == 0:
            result[cat.cat_id] = {
                'cat_id': cat.cat_id,
                'cat_name':cat.cat_name,
                'cat_pid': cat.cat_pid,
                'cat_level':cat.cat_level,
                'cat_deleted': cat.cat_deleted == 1,
                'children': []
            }
    # 临时存储二级返回结果
    tmpResult = {}
    # 处理二级菜单
    for cat in categories:
        # 判断是否被删除, 当父级不存在时也视为被删除
        if isDelete(keyCategories, cat):
            continue
        if cat.cat_level == 1 and cat.cat_level < ty:
            parentResult = result[cat.cat_pid]
            tmpResult[cat.cat_id] = {
                'cat_id': cat.cat_id,
                'cat_name':cat.cat_name,
                'cat_pid': cat.cat_pid,
                'cat_level':cat.cat_level,
                'cat_deleted': cat.cat_deleted == 1,
                'children': []
            }
            parentResult['children'].append(tmpResult[cat.cat_id])
    # print(result)
    #处理三级菜单
    for cat in categories:
        # 判断是否被删除,
        if isDelete(keyCategories, cat):
            continue
        if cat.cat_level == 2 and cat.cat_level < ty:
            if cat.cat_pid not in tmpResult.keys():
                continue
            parentResult = tmpResult[cat.cat_pid]
            if parentResult:
                parentResult['children'].append({
                    'cat_id': cat.cat_id,
                    'cat_name': cat.cat_name,
                    'cat_pid': cat.cat_pid,
                    'cat_level': cat.cat_level,
                    'cat_deleted': cat.cat_deleted == 1,
                })
    # print(result)
    return result
'''
判断参数是否被删除
'''
def isDelete(keyCategories,cat):
    if cat.cat_pid == 0:
        return  cat.cat_deleted
    elif cat.cat_deleted:
        return True
    else:
        if cat.cat_pid not in keyCategories.keys():
            return True
        return isDelete(keyCategories,keyCategories[cat.cat_pid])