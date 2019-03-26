from stark.service.stark import site, ModelStark,get_datetime_text
from django.urls import path
from web.models import *
from django.utils.safestring import mark_safe
from django.shortcuts import HttpResponse, redirect, render
from django.db.models import Q
import datetime
from django.http import JsonResponse
class StudentConfig(ModelStark):
    def score_view(self, request, sid):
        if request.is_ajax():

            print(request.GET)

            sid = request.GET.get("sid")
            cid = request.GET.get("cid")

            study_record_list = StudyRecord.objects.filter(student=sid, course_record__class_obj=cid)

            data_list = []

            for study_record in study_record_list:
                day_num = study_record.course_record.day_num
                data_list.append(["day%s" % day_num, study_record.score])
            print(data_list)
            return JsonResponse(data_list, safe=False)


        else:
            student = Student.objects.filter(id=sid).first()
            class_list = student.class_list.all()

            return render(request, "score_view.html", locals())

    def extra_url(self):
        temp = []
        temp.append(path("score_view/<int:sid>", self.score_view))
        return temp

    def score_show(self, obj=None, header=False):
        if header:
            return "查看成绩"
        return mark_safe("<a href='/stark/web/student/score_view/%s'>查看成绩</a>" % obj.id)

    list_display = ["customer", "class_list", score_show]
    list_display_links = ["customer"]