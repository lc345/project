from typing import Any
from django.contrib import admin
from django import forms

from django.contrib import messages
from interview.models import Candidate
from datetime import datetime

from MonitorTypes.models import MonitorTypes
from MonitorTypes.models import Resume
from django.utils.html import format_html


# Register your models here.

class MonitorTypeAdmin(admin.ModelAdmin):
    exclude = ('creator', )
    list_display = ('monitor_type', 'description', 'creator')

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        obj.creator = request.user
        return super().save_model(request, obj, form, change)

def enter_interview_process(modeladmin, request, queryset):
    candidate_names = ""
    for resume in queryset:
        candidate = Candidate()
        # 把 obj 对象中的所有属性拷贝到 candidate 对象中:
        candidate.__dict__.update(resume.__dict__)
        candidate.created_date = datetime.now()
        candidate.modified_date = datetime.now()
        candidate_names = candidate.username + "," + candidate_names
        candidate.creator = request.user.username
        candidate.save()
    messages.add_message(request, messages.INFO, '%s 已成功录入系统' % (candidate_names) )

enter_interview_process.short_description = u'录入系统'


class ResumeAdmin(admin.ModelAdmin):

    actions = (enter_interview_process,)

    def image_tag(self, obj):              
        if obj.picture:
            return format_html('<img src="{}" style="width:100px;height:80px;"/>'.format(obj.picture.url))
        return ""
    image_tag.allow_tags = True
    image_tag.short_description = 'Image'

    list_display = ('username', 'applicant', 'city', 'apply_position', 'bachelor_school', 'master_school', 'major','created_date')

    readonly_fields = ('applicant', 'created_date', 'modified_date',)

    fieldsets = (
        (None, {'fields': (
            "applicant", ("username", "city", "phone"),
            ("email", "apply_position", "born_address", "gender", ), ("picture", "attachment",),
            ("bachelor_school", "master_school"), ("major", "degree"), ('created_date', 'modified_date'),
            "candidate_introduction", "work_experience","project_experience",)}),
    )

    def save_model(self, request, obj, form, change):
        obj.applicant = request.user
        super().save_model(request, obj, form, change)


# Register your models here.
admin.site.register(MonitorTypes, MonitorTypeAdmin)
admin.site.register(Resume, ResumeAdmin)