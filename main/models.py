from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Staff(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_details")
    sex = models.CharField(max_length=255)
    phone = models.IntegerField()
    degree = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    job = models.CharField(max_length=255)
    it_department_access = models.BooleanField(default=False)
    student_office_department_access = models.BooleanField(default=False)
    student_visa_access = models.BooleanField(default=False)
    student_finance_access = models.BooleanField(default=False)
    student_admission_access = models.BooleanField(default=False)
    director_access = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def serialize(self):
        return {
            "first_name" : self.user.first_name,
            "last_name" : self.user.last_name,
            "sex" : self.sex,
            "phone" : self.phone,
            "email" : self.user.email,
            "specialization" : self.specialization,
            "department" : self.department,
            "job" : self.job,
        }

class Module(models.Model):
    code = models.CharField(max_length=10)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    tutors = models.ManyToManyField(Staff, blank=True, related_name="module")

    def __str__(self):
        return self.title

    def serialize(self):
        return {
            "code" : self.code,
            "title" : self.title,
            "description" : self.description,
            "tutors" : [tutor.id for tutor in self.tutors.all()],
        }

class Programme(models.Model):
    code = models.CharField(max_length=10)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    modules = models.ManyToManyField(Module, blank=True, related_name="programme")
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def serialize(self):
        return {
            "code" : self.code,
            "title" : self.title,
            "description" : self.description,
            "modules" : [module.code for module in self.modules.all()],
            "fee" : self.fee
        }

class DiscountsAndScholarship(models.Model):
    code = models.CharField(max_length=10)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    percent = models.IntegerField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def serialize(self):
            return {
                "code" : self.code,
                "title" : self.title,
                "description" : self.description,
                "percent" : self.percent
            }    

class Student(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    sex = models.CharField(max_length=255)
    phone = models.IntegerField()
    email = models.EmailField()
    country = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    isInternationalStudent = models.BooleanField(default=False)
    programme_application = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name="programmed_applied")
    hasOffer = models.BooleanField(default=False)
    DiscountOrScholarship = models.ManyToManyField(DiscountsAndScholarship, blank=True, related_name="discounts")
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def serialize(self):
        return {
            "first_name" : self.first_name,
            "last_name" : self.last_name,
            "sex" : self.sex,
            "phone" : self.phone,
            "email" : self.email,
            "country" : self.country,
            "address" : self.address,
            "isInternationalStudent" : self.isInternationalStudent,
            "programme_applied" : self.programme_application.code,
            "hasOffer" : self.hasOffer,
            "discountOrScholarship" : [item.code for item in self.DiscountOrScholarship.all()],
            "date" : self.date
        }

class StudentInvoice(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="student_invoice")
    academic_year = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    finance_hold = models.DecimalField(max_digits=10, decimal_places=2)
    date_issued = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.student.first_name} {self.student.last_name}'

class StudentPayments(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="payments")
    invoices = models.ManyToManyField(StudentInvoice, blank=False, related_name="invoice")
    percent = models.IntegerField()
    academic_year = models.CharField(max_length=255)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.student.first_name} {self.student.last_name}'

class EnrolledStudent(models.Model):
    studentID = models.CharField(max_length=10)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="course")
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name="students")
    academic_year = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    mode = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.student.first_name} {self.student.last_name}'
    
class StudentService(models.Model):
    enrolled_student = models.ForeignKey(EnrolledStudent, on_delete=models.CASCADE, related_name="services")
    visa_application_date = models.DateField(auto_now=True)
    visa_status = models.CharField(max_length=255)
    visa_exp_date = models.DateField(auto_now=False)
    inCountry = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.enrolled_student.student.first_name} {self.enrolled_student.student.last_name}'
    
class StudentAcademics(models.Model):
    enrolled_student = models.ForeignKey(EnrolledStudent, on_delete=models.CASCADE, related_name="academics")
    academic_module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="modules")
    module_score = models.CharField(max_length=255)
    academic_hold = models.CharField(max_length=255)
    academic_year = models.CharField(max_length=255)
    academic_term = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.enrolled_student.student.first_name} {self.enrolled_student.student.last_name}'

class Event(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="event_creator")
    desc = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.creator.username} {self.desc}'