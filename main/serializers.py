from rest_framework import serializers
from .models import Staff, Module, Programme, DiscountsAndScholarship, Student, StudentInvoice, StudentPayments, EnrolledStudent, StudentService, StudentAcademics

class StaffSerializerClass(serializers.ModelSerializer):
    class Meta():
        model = Staff
        fields = [
            'id', 
            'first_name',
            'last_name',
            'sex',
            'phone',
            'email',
            'specialization',
            'department',
            'job'
        ]

class ModuleSerializerClass(serializers.ModelSerializer):
    class Meta():
        model = Module
        fields = [
            'id',
            'code',
            'title',
            'description',
            'tutors'
        ]

class ProgrammeSerializerClass(serializers.ModelSerializer):
    class Meta():
        model = Programme
        fields = [
            'id',
            'code',
            'title',
            'description',
            'modules',
            'fee'
        ]

class DiscountsAndScholarshipSerializerClass(serializers.ModelSerializer):
    class Meta():
        model = DiscountsAndScholarship
        fields = [
            'id',
            'code',
            'title',
            'description',
            'percent',
        ]

class StudentSerializerClass(serializers.ModelSerializer):
    class Meta():
        model = Student
        fields = [
            'id',
            'first_name',
            'last_name',
            'sex',
            'phone',
            'email',
            'country',
            'address',
            'isInternationalStudent',
            'programme_application',
            'hasOffer',
            'DiscountOrScholarship'
        ]

class StudentInvoiceSerializerClass(serializers.ModelSerializer):
    class Meta():
        model = StudentInvoice
        fields = [
            'id',
            'student',
            'academic_year',
            'amount',
            'balance',
            'finance_hold',
            'date_issued'
        ]

class StudentPaymentsSerializerClass(serializers.ModelSerializer):
    class Meta():
        model = StudentPayments
        fields = [
            'id',
            'student',
            'invoices',
            'percent',
            'academic_year',
            'date_updated'
        ]

class EnrolledStudentSerializerClass(serializers.ModelSerializer):
    class Meta():
        model = EnrolledStudent
        fields = [
            'id',
            'studentID',
            'student',
            'programme',
            'academic_year',
            'status',
            'mode',
            'date'
        ]

class StudentServiceSerializerClass(serializers.ModelSerializer):
    class Meta():
        model = StudentService
        fields = [
            'id',
            'enrolled_student',
            'visa_application_date',
            'visa_status',
            'visa_exp_date',
            'inCountry'
        ]

class StudentAcademicsSerializerClass(serializers.ModelSerializer):
    class Meta():
        model = StudentAcademics
        fields = [
            'id',
            'enrolled_student',
            'academic_module',
            'module_score',
            'academic_hold',
            'academic_year',
            'academic_term'
        ]
