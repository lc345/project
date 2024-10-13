from django.urls import path
from MonitorTypes import views

urlpatterns = [
    # 监控列表
    path("monitorlist/", views.monitorlist, name="monitorlist"),
    # 详情
    path("monitor/<int:monitor_id>/", views.detail, name="monitor"),
    path('resume/add/', views.ResumeCreateView.as_view(), name='resume-add'),
    path('resume/<int:pk>/', views.ResumeDetailView.as_view(), name='resume-detail'),
]
