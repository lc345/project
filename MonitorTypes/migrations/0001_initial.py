# Generated by Django 3.0.3 on 2024-07-24 05:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MonitorTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monitor_type', models.SmallIntegerField(choices=[(0, '人脸'), (1, '手势'), (2, '温度'), (3, '窗户'), (4, '门')], verbose_name='监控类型')),
                ('description', models.TextField(max_length=1024, verbose_name='描述')),
                ('created_date', models.DateTimeField(verbose_name='创建日期')),
                ('modified_date', models.DateTimeField(verbose_name='修改时间')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='创建人')),
            ],
        ),
    ]
