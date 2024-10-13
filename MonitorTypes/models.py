from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

from interview.models import DEGREE_TYPE

TypeName = [
    (0, "人脸"),
    (1, "手势"),
    (2, "温度"),
    (3, "窗户"),
    (4, "门"),
]

# Create your models here.

class MonitorTypes(models.Model):
    monitor_type = models.SmallIntegerField(blank=False, choices=TypeName, verbose_name="监控类型")
    description = models.TextField(max_length=1024, verbose_name="描述")
    creator = models.ForeignKey(User, verbose_name="创建人", null=True, on_delete=models.SET_NULL)
    created_date = models.DateTimeField(verbose_name="创建日期", default=datetime.now)
    modified_date = models.DateTimeField(verbose_name="修改时间", default=datetime.now)


class Resume(models.Model):
    # Translators: 简历实体的翻译
    username = models.CharField(max_length=135, verbose_name="姓名")
    applicant = models.ForeignKey(User, verbose_name="申请人", null=True, on_delete=models.SET_NULL)
    city = models.CharField(max_length=135, verbose_name="城市")
    phone = models.CharField(max_length=135,  verbose_name="手机号码")
    email = models.EmailField(max_length=135, blank=True, verbose_name="邮箱")
    apply_position = models.CharField(max_length=135, blank=True, verbose_name="应聘职位")
    born_address = models.CharField(max_length=135, blank=True, verbose_name="生源地")
    gender = models.CharField(max_length=135, blank=True, verbose_name="性别")
    picture = models.ImageField(upload_to='images/', blank=True, verbose_name="个人照片") 
    attachment = models.FileField(upload_to='file/', blank=True, verbose_name="简历附件")

    # 学校与学历信息
    bachelor_school = models.CharField(max_length=135, blank=True, verbose_name="本科学校")
    master_school = models.CharField(max_length=135, blank=True, verbose_name="研究生学校")
    doctor_school = models.CharField(max_length=135, blank=True, verbose_name="博士生学校")
    major = models.CharField(max_length=135, blank=True, verbose_name="专业")
    degree = models.CharField(max_length=135, choices=DEGREE_TYPE, blank=True, verbose_name="学历")
    created_date = models.DateTimeField(verbose_name="创建日期", default=datetime.now)
    modified_date = models.DateTimeField(verbose_name="修改日期", auto_now=True)

    # 候选人自我介绍，工作经历，项目经历
    candidate_introduction = models.TextField(max_length=1024, blank=True, verbose_name="自我介绍")
    work_experience = models.TextField(max_length=1024, blank=True, verbose_name="工作经历")
    project_experience = models.TextField(max_length=1024, blank=True, verbose_name="项目经历")

    class Meta:
        verbose_name = "信息"
        verbose_name_plural = "用户个人信息"
    
    def __str__(self):
        return self.username