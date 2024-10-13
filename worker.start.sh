# 启动 SecurityMonitoringAnalysis 这个 package 的时候，会运行 __init__.py
# __init__.py 里面初始化了 django 的配置
DJANGO_SETTINGS_MODULE=settings.base celery -A SecurityMonitoringAnalysis worker -l INFO

