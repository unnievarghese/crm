from django.urls import path
from crm.views import councillor_creation,signin,course_creation,homepage,signout,batch_creation,enquiry_creation,\
    admission_creation,paymentdetails,makepayment,enquirylist,admissionlist,batch_list

urlpatterns = [
    path('councillorcreation',councillor_creation.as_view(),name='councilorcreation'),
    path('signin',signin.as_view(),name='signin'),
    path('createcourse',course_creation.as_view(),name='createcourse'),
    path('signout',signout.as_view(),name='signout'),
    path('batchcreation',batch_creation.as_view(),name='batch'),
    path('enquirycreation',enquiry_creation.as_view(),name='enquiry'),
    path('admission/<str:id>',admission_creation.as_view(),name='admission'),
    path('paymentdetails',paymentdetails.as_view(),name='paymentdetails'),
    path('makepayment/<str:id>',makepayment.as_view(),name='payment'),
    path('home',homepage.as_view(),name='home'),
    path('enquiry_list',enquirylist.as_view(),name='enquirylist'),
    path('admission_list',admissionlist.as_view(),name='admissionlist'),
    path('batch_list',batch_list.as_view(),name='batchlist'),

]
