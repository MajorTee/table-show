# coding=utf-8
from typing import List

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
import json
from random import randrange
from rest_framework.views import APIView

from pyecharts.charts import Bar
from pyecharts import options as opts
from show_data.models import DataInfo

from pyecharts.faker import Faker
from pyecharts.charts import Line

# Create your views here.

# def my_render(request, template_path, context_dict):
#     template = loader.get_template(template_path)
#     res_html = template.render(context_dict)
#     return HttpResponse(res_html)


# 1.定义视图函数，HttpRequest
# 2.进行url配置，建立url地址和视图的对应关系
# http://127.0.0.1:8000/index
# def index(request):
#     '''
#     # 和M T进行交互
#     # return HttpResponse('测试')
#
#     # 使用模板文件
#     # 1.加载文件
#     template = loader.get_template('show_data/index.html')
#     # 2.定义模板上下文
#     # context = RequestContext(request, {})
#     context = {}  # 2.1 改写
#     # 3.模板渲染：产生标准html
#     res_html = template.render(context)
#     # 4.返回浏览器
#     return HttpResponse(res_html)
#     '''
#
#     # 重构
#     # return my_render(request, 'show_data/index.html', {})
#
#     # 官方render
#     return render(request, 'show_data/index.html', {'content': 'hello hello', 'list': list(range(1, 5))})


# def relation(request):
#     if request.method == 'POST':
#         sku_id = request.POST.get('goods_id')
#         global algor
#         algor = request.POST.get('algor')
#         objects_filter = DataInfo.objects.filter(goodsID=goods_id).values()
#         if not objects_filter.exists():
#             hit_yes = False
#         else:
#             hit_yes = True
#             sale_data = objects_filter[0]
#
#             sku_data = str_to_list(sale_data['sku_id'])
#
#             global flgb_data
#             flgb_data = str_to_list(sale_data['FLGB_data'])
#
#     return render(request, 'show_data/relation_show.html', {'hit': hit_yes, 'sku_id': sku_id, 'algor': algor})


real_data = ''
flgb_data = ''
lgb_data = ''
xgb_data = ''
fxgb_data = ''
lr_data = ''
flr_data = ''
svm_data = ''
algor_data = ''
all_data = {}
algor = ''


def query(request):
    if request.method == 'POST':
        sku_id = request.POST.get('sku_id')
        global algor
        algor = request.POST.get('algor')
        objects_filter = DataInfo.objects.filter(skuID=sku_id).values()

        if not objects_filter.exists():
            hit_yes = False
        else:
            hit_yes = True
            sale_data = objects_filter[0]

            global real_data
            real_data = str_to_list(sale_data['real_data'])

            global flgb_data
            flgb_data = str_to_list(sale_data['FLGB_data'])
            global lgb_data
            lgb_data = str_to_list(sale_data['LGB_data'])
            global fxgb_data
            fxgb_data = str_to_list(sale_data['FXGB_data'])
            global flr_data
            flr_data = str_to_list(sale_data['FLR_data'])
            global xgb_data
            xgb_data = str_to_list(sale_data['XGB_data'])
            global lr_data
            lr_data = str_to_list(sale_data['LR_data'])
            global svm_data
            svm_data = str_to_list(sale_data['SVM_data'])

            global algor_data
            if algor == "LSSFOA-LightGBM":
                algor_data = flgb_data
            elif algor == "FOA-XGB":
                algor_data = fxgb_data
            elif algor == "FOA-LR":
                algor_data = flr_data
            elif algor == "LightGBM":
                algor_data = lgb_data
            elif algor == "XGB":
                algor_data = xgb_data
            elif algor == "LR":
                algor_data = lr_data
            elif algor == "SVM":
                algor_data = svm_data
            elif algor == "all":
                global all_data
                all_data = sale_data
                algor = "对比数据"
            else:
                algor_data = ''

        return render(request, 'show_data/table_show.html', {'hit': hit_yes, 'sku_id': sku_id, 'algor': algor})

    # return redirect(request, 'show_data/query.html')


def response_as_json(data):
    json_str = json.dumps(data)
    response = HttpResponse(
        json_str,
        content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def json_response(data, code=200):
    data = {
        "code": code,
        "msg": "success",
        "data": data,
    }
    return response_as_json(data)


def json_error(error_string="error", code=500, **kwargs):
    data = {
        "code": code,
        "msg": error_string,
        "data": {}
    }
    data.update(kwargs)
    return response_as_json(data)


JsonResponse = json_response
JsonError = json_error


def str_to_list(word: str) -> List:
    word_split = word.split(",")
    for i in range(5):
        word_split[i] = ('%.2f' % float(word_split[i]))
    return word_split


def line_base() -> Line:
    c = (
        Line()
            .add_xaxis(["week1", "week2", "week3", "week4", "week5"])
            .add_yaxis("预测数据", algor_data)
            .add_yaxis("真实数据", real_data)
            .set_global_opts(title_opts=opts.TitleOpts(title=""))
            .dump_options_with_quotes()
    )

    return c


# 使用柱状图展示所有数据对比结果
def bar_base() -> Bar:
    c = (
        Bar()
            .add_xaxis(["week1", "week2", "week3", "week4", "week5"])
            .add_yaxis("real", real_data)
            .add_yaxis("LSSFOA-LightGBM", flgb_data)
            .add_yaxis("LightGBM", lgb_data)
            .add_yaxis("LR", flr_data)
            .set_global_opts(title_opts=opts.TitleOpts())
            .dump_options_with_quotes()
    )
    return c


class ChartView(APIView):
    def get(self, request, *args, **kwargs):
        if algor != '对比数据':
            return JsonResponse(json.loads(line_base()))
        else:
            return JsonResponse(json.loads(bar_base()))


class IndexView(APIView):
    def get(self, request, *args, **kwargs):
        return HttpResponse(content=open("./templates/show_data/query.html", encoding='UTF-8').read())


