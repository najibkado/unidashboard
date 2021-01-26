from django.urls import path, include
from main.views import staff, index, module, programme, discount, student, invoice, payment, enroll, academic, service

urlpatterns = [
    path('', index.index, name="index"),
    path('api/staff', staff.StaffsApiView.as_view()),
    path('api/staff/<int:id>', staff.StaffApiView.as_view()),
    path('api/module', module.ModulesApiView.as_view()),
    path('api/module/<int:id>', module.ModuleApiView.as_view()),
    path('api/programme', programme.ProgrammesApiView.as_view()),
    path('api/programme/<int:id>', programme.ProgrammeApiView.as_view()),
    path('api/discountandscholarship', discount.DiscountsAndScholarshipsApiView.as_view()),
    path('api/discountandscholarship/<int:id>', discount.DiscountsAndScholarshipApiView.as_view()),
    path('api/student', student.StudentsApiView.as_view()),
    path('api/student/<int:id>', student.StudentApiView.as_view()),
    path('api/invoice', invoice.InvoicesApiView.as_view()),
    path('api/invoice/<int:id>', invoice.InvoiceApiView.as_view()),
    path('api/payment', payment.PaymentsApiView.as_view()),
    path('api/payment/<int:id>', payment.PaymentApiView.as_view()),
    path('api/enroll', enroll.EnrolledStudentsApiView.as_view()),
    path('api/enroll/<int:id>', enroll.EnrolledStudentApiView.as_view()),
    path('api/academics', academic.StudentsAcademicsApiView.as_view()),
    path('api/academics/<int:id>', academic.StudentAcademicsApiView.as_view()),
    path('api/services', service.StudentServicesApiView.as_view()),
    path('api/services/<int:id>', service.StudentServiceApiView.as_view())

]
