from stark.service.stark import site, ModelStark,get_datetime_text
from .models import *
from web.views.userinfo import UserInfoHandler
from web.views.school import SchoolHandler
from web.views.depart import DepartmentHandler
from web.views.course import CourseHandler
from web.views.class_list import ClassListHandler
from web.views.my_customer import MyCustomerHandler
from web.views.public_customer import PublicCustomerHandler
from web.views.all_customer import All_Cusotmer
from web.views.courserecord import CourseRecordConfig
from web.views.student import StudentConfig
from web.views.studyrecord import StudyConfig
from web.views.consultrecord import ConsultConfig

#用户
site.register(UserInfo,UserInfoHandler)

#学校
site.register(School,SchoolHandler)

#部门
site.register(Department,DepartmentHandler)

#课程
site.register(Course,CourseHandler)

#班级
site.register(ClassList, ClassListHandler)

#我的客户
site.register(Customer,MyCustomerHandler,'mycustomer')

#公共客户
site.register(Customer,PublicCustomerHandler,'public')

#所有客户
site.register(Customer,All_Cusotmer )

#客户跟进
site.register(ConsultRecord, ConsultConfig)

#学生
site.register(Student, StudentConfig)

#上课记录
site.register(CourseRecord, CourseRecordConfig)

#学生上课成绩、签到记录
site.register(StudyRecord, StudyConfig)

#客户状态表
site.register(CustomerDistrbute)
