from django.shortcuts import render
import math
import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from orders.models import SpOrder,SpReport1
from django.core.paginator import Paginator
from django.http import JsonResponse
# Create your views here.

'''
获取所有订单
'''
def getAllOrder(request):
    query = request.GET.get('query')
    pagenum = int(request.GET.get('pagenum'))
    pagesize = int(request.GET.get('pagesize'))
    if query == '':
        orders = SpOrder.objects.all()
    else:
        orders = SpOrder.objects.filter(order_number__contains=query)
    # 总数total
    total = len(orders)
    # 防止查询大于本身数据的页数
    if pagenum > math.ceil(total / pagesize):
        pagenum = 1
    pagtor = Paginator(orders, pagesize).page(pagenum)
    list_orders = []
    for order in pagtor:
        list_orders.append({
            "order_id": order.order_id,
            "user_id": order.user_id,
            "order_number": order.order_number,
            "order_price": order.order_price,
            "order_pay": order.order_pay,
            "is_send": order.is_send,
            "trade_no": order.trade_no,
            "order_fapiao_title": order.order_fapiao_title,
            "order_fapiao_company": order.order_fapiao_company,
            "order_fapiao_content": order.order_fapiao_content,
            "consignee_addr": order.consignee_addr,
            "pay_status": order.pay_status,
            "create_time": order.create_time,
            "update_time": order.update_time
        })
    resultData = {}
    resultData['total'] = total
    resultData['pagenum'] = pagenum
    resultData['pagesize'] = pagesize
    resultData['goods'] = list_orders
    return JsonResponse({
        'data': resultData,
        'meta': {
            'msg': '获取成功',
            'status': 200,
        }
    })

'''测试物流的'''
def getkuaidi(request,id):
    return JsonResponse({
        "data": [
            {
                "time": "2018-05-10 09:39:00",
                "ftime": "2018-05-10 09:39:00",
                "context": "已签收,感谢使用顺丰,期待再次为您服务",
                "location": ""
            },
            {
                "time": "2018-05-10 08:23:00",
                "ftime": "2018-05-10 08:23:00",
                "context": "[北京市]北京海淀育新小区营业点派件员 顺丰速运 95338正在为您派件",
                "location": ""
            },
            {
                "time": "2018-05-10 07:32:00",
                "ftime": "2018-05-10 07:32:00",
                "context": "快件到达 [北京海淀育新小区营业点]",
                "location": ""
            },
            {
                "time": "2018-05-10 02:03:00",
                "ftime": "2018-05-10 02:03:00",
                "context": "快件在[北京顺义集散中心]已装车,准备发往 [北京海淀育新小区营业点]",
                "location": ""
            },
            {
                "time": "2018-05-09 23:05:00",
                "ftime": "2018-05-09 23:05:00",
                "context": "快件到达 [北京顺义集散中心]",
                "location": ""
            },
            {
                "time": "2018-05-09 21:21:00",
                "ftime": "2018-05-09 21:21:00",
                "context": "快件在[北京宝胜营业点]已装车,准备发往 [北京顺义集散中心]",
                "location": ""
            },
            {
                "time": "2018-05-09 13:07:00",
                "ftime": "2018-05-09 13:07:00",
                "context": "顺丰速运 已收取快件",
                "location": ""
            },
            {
                "time": "2018-05-09 12:25:03",
                "ftime": "2018-05-09 12:25:03",
                "context": "卖家发货",
                "location": ""
            },
            {
                "time": "2018-05-09 12:22:24",
                "ftime": "2018-05-09 12:22:24",
                "context": "您的订单将由HLA（北京海淀区清河中街店）门店安排发货。",
                "location": ""
            },
            {
                "time": "2018-05-08 21:36:04",
                "ftime": "2018-05-08 21:36:04",
                "context": "商品已经下单",
                "location": ""
            }
        ],
        "meta": {"status": 200, "message": "获取物流信息成功！"}
    })

'''
统计
'''
def statis(request,report_num):
    if report_num == '1':
        reports = SpReport1.objects.all()
        result = reportOne(reports)
        # print(result)
        return JsonResponse({
            'data':result,
            'meta':{
                'status': 200,
                'msg': '获取报表成功'
            }
        })
def reportOne(reports):
    result = {}
    #存储区域名称
    areaKeys = {}
    areaVal = {}
    for report in reports:
        areaKeys[report.rp1_area] = 1
    # 去除重复的地区
    areaVal['data'] = list(areaKeys.keys())
    result['legend'] = areaVal
    series = []
    rp1_users = {}
    for report in reports:
        if report.rp1_area not in rp1_users.keys():
            # 空列表不能直接append
            rp1_users[report.rp1_area] = []+[report.rp1_user_count]
        else:
           rp1_users[report.rp1_area].append(report.rp1_user_count)

    for area in rp1_users.keys():
        dict_series = {}
        dict_series['data'] = rp1_users[area]
        dict_series['name'] = area
        dict_series['stack'] = '总量'
        dict_series['type'] = 'line'
        dict_series['areaStyle'] = {'normal': {}}
        if series == None:
            # 空列表不能直接append
            series + [dict_series]
        else:
            series.append(dict_series)
    result['series'] = series
    # x轴为时间
    dateKeys = {}
    dateVal = {}
    for report in reports:
        # 日期时间转字符串
        dateKeys[report.rp1_date.strftime('%Y-%m-%d')] = 1
    # print(dateKeys)
    dateVal['data'] = list(dateKeys.keys())
    # print(dateVal)
    #列表字典存储
    result['xAxis'] = []+[dateVal]
    # y轴为值
    result['yAxis'] = [{'type': 'values'}]
    return result

