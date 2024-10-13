# 启动异步任务celery：DJANGO_SETTINGS_MODULE=settings.base celery -A SecurityMonitoringAnalysis worker --loglevel=info

# flower启动命令：DJANGO_SETTINGS_MODULE=settings.base celery -A SecurityMonitoringAnalysis flower --broker=redis://@localhost:6379/0

# 宝塔： 查看状态：/etc/init.d/bt status  查看进程的端口：netstat -tnlp |grep 32514 #32514为第一条命令返回的Bt-Panel服务对应的pid  重启服务宝塔会更改登录链接，在终端输入 bt 14 找到新的链接登录即可