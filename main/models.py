from django.db import models

# Create your models here.

class Staff(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    sex = models.CharField(max_length=255)
    phone = models.IntegerField()
    email = models.EmailField()
    degree = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    job = models.CharField(max_length=255)

    def serialize(self):
        return {
            "first_name" : self.first_name,
            "last_name" : self.last_name,
            "sex" : self.sex,
            "phone" : self.phone,
            "email" : self.email,
            "specialization" : self.specialization,
            "department" : self.department,
            "job" : self.job,
        }

class Module(models.Model):
    code = models.CharField(max_length=10)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    tutors = models.ManyToManyField(Staff, blank=True, related_name="module")

    def serialize(self):
        return {
            "code" : self.code,
            "title" : self.title,
            "description" : self.description,
            "tutors" : [tutor.serialize() for tutor in self.tutors],
        }

class Programme(models.Model):
    code = models.CharField(max_length=10)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    modules = models.ManyToManyField(Module, blank=True, related_name="programme")
    fee = models.DecimalField(max_digits=10, decimal_places=2)

    def serialize(self):
        return {
            "code" : self.code,
            "title" : self.title,
            "description" : self.description,
            "modules" : [module.serialize() for module in self.modules],
            "fee" : self.fee
        }

class DiscountsAndScholarship(models.Model):
    code = models.CharField(max_length=10)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    percent = models.IntegerField()

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
    hasOffer = models.BooleanField(default=True)
    DiscountOrScholarship = models.ManyToManyField(DiscountsAndScholarship, blank=True, related_name="discounts")
    date = models.DateTimeField(auto_now=True)

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
            "programme_applied" : [programme.serialize() for programme in self.programme_application],
            "hasOffer" : self.hasOffer,
            "discountOrScholarship" : [item.serialize() for item in self.DiscountOrScholarship],
            "date" : self.date
        }

class StudentInvoice(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="student_invoice")
    academic_year = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    finance_hold = models.DecimalField(max_digits=10, decimal_places=2)
    date_issued = models.DateField(auto_now=True)

class StudentPayments(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="payments")
    invoices = models.ManyToManyField(StudentInvoice, blank=False, related_name="invoice")
    percent = models.IntegerField()
    academic_year = models.CharField(max_length=255)
    date_updated = models.DateTimeField(auto_now=True)

class EnrolledStudent(models.Model):
    studentID = models.CharField(max_length=10)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="course")
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name="students")
    academic_year = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    mode = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)
    
class StudentService(models.Model):
    enrolled_student = models.ForeignKey(EnrolledStudent, on_delete=models.CASCADE, related_name="services")
    visa_application_date = models.DateField(auto_now=True)
    visa_status = models.CharField(max_length=255)
    visa_exp_date = models.DateField(auto_now=False)
    inCountry = models.BooleanField(default=True)
    
class StudentAcademics(models.Model):
    enrolled_student = models.ForeignKey(EnrolledStudent, on_delete=models.CASCADE, related_name="academics")
    academic_module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="modules")
    module_score = models.CharField(max_length=255)
    academic_hold = models.CharField(max_length=255)
    academic_year = models.CharField(max_length=255)
    academic_term = models.CharField(max_length=255)