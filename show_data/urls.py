from django.conf.urls import url
from show_data import views
from django.urls import path, re_path

app_name = 'show_data'
urlpatterns = [
    # 通过url函数设置url路由配置项
    # 使用re_path利用正则严格匹配开头和结尾
    # path('index/', views.index, name='index'),  # 建立/index和视图index之间的关系 必须要求有/
    # path('index2/', views.index2, name='index2'),  # 建立/index和视图index之间的关系 必须要求有/
    path('bar/', views.ChartView.as_view(), name='query'),  # 建立/index和视图index之间的关系 必须要求有/
    path('', views.IndexView.as_view(), name='index'),
    re_path(r'^query/', views.query, name='query'),
    # re_path(r'^query/', views.query, name='query'),
]
