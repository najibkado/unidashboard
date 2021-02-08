from django.contrib import admin
from .models import Staff, Module, Programme, DiscountsAndScholarship, Student, StudentInvoice, StudentPayments, EnrolledStudent, StudentService, StudentAcademics, Event

# Register your models here.

admin.site.register(Staff)
admin.site.register(Module)
admin.site.register(Programme)
admin.site.register(DiscountsAndScholarship)
admin.site.register(Student)
admin.site.register(StudentInvoice)
admin.site.register(StudentPayments)
admin.site.register(EnrolledStudent)
admin.site.register(StudentService)
admin.site.register(StudentAcademics)
admin.site.register(Event)