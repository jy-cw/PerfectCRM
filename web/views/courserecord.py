#!/usr/bin/env python
#coding=utf-8
from stark.service.stark import site, ModelStark,get_datetime_text
from django.urls import path
from web.models import *
from django.utils.safestring import mark_safe
from django.shortcuts import HttpResponse, redirect, render
from django.db.models import Q
import datetime
from django.http import JsonResponse

class CourseRecordConfig(ModelStark):
    def score(self, request, course_record_id):
        if request.method == "POST":
            print(request.POST)

            data = {}
            for key, value in request.POST.items():

                if key == "csrfmiddlewaretoken": continue

                field, id = key.rsplit("_", 1)

                if id in data:
                    data[id][field] = value
                else:
                    data[id] = {field: value}  # data  {4:{"score":90}}

            print("data", data)

            for pk, update_data in data.items():
                StudyRecord.objects.filter(id=id).update(**update_data)

            return redirect(request.path)


        else:
            study_record_list = StudyRecord.objects.filter(course_record=course_record_id)
            score_choices = StudyRecord.score_choices
            return render(request, "score.html", locals())

    def extra_url(self):

        temp = []
        temp.append(path("record_score/<int:course_record_id>", self.score))
        return temp

    def record(self, obj=None, header=False):
        if header:
            return "学习记录"
        return mark_safe("<a href='/stark/web/studyrecord/?course_record=%s'>记录</a>" % obj.id)

    def record_score(self, obj=None, header=False):
        if header:
            return "录入成绩"
        return mark_safe("<a href='record_score/%s'>录入成绩</a>" % obj.id)

    list_display = ["class_obj", "day_num", "teacher", record, record_score]

    def patch_studyrecord(self, request, queryset):
        print(queryset)
        temp = []
        for course_record in queryset:
            # 与course_record关联的班级对应所有学生
            student_list = Student.objects.filter(class_list__id=course_record.class_obj.id)
            for student in student_list:
                obj = StudyRecord(student=student, course_record=course_record)
                temp.append(obj)
        StudyRecord.objects.bulk_create(temp)

    patch_studyrecord.text= "批量生成学习记录"
    actions = [patch_studyrecord, ]