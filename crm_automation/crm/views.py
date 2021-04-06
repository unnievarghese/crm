from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from crm.forms import councilor_creationform,siginform,course_creation_form,batch_creation_form,enquiry_creation_form,\
    admission_creation_form,payment_form
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
from crm.models import *
from django.db.models import Q

class signin(TemplateView):
    context={}
    template_name = 'crm/signin.html'
    form_class=siginform

    def get(self, request, *args, **kwargs):
        self.context['form']=self.form_class
        self.context['user']=str(request.user)
        return render(request,self.template_name,self.context)
    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            pwd=form.cleaned_data.get('password')
            user=authenticate(request,username=username,password=pwd)
            if user:
                login(request,user)
                return redirect('home')
            return redirect('signin')

class signout(TemplateView):

    def get(self, request, *args, **kwargs):
        logout(self.request)
        return redirect('signin')

class councillor_creation(PermissionRequiredMixin, TemplateView):

    permission_required = 'user.view_user'

    context = {}
    template_name = "crm/councilor_creation.html"
    form_class = councilor_creationform

    def get(self, request, *args, **kwargs):
        self.context['form'] = self.form_class
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'crm/centreheadpage.html')
        return redirect('councilorcreation')

class course_creation(PermissionRequiredMixin,TemplateView):

    permission_required = 'courses.view_courses'

    context={}
    template_name = 'crm/course_add.html'
    form_class=course_creation_form

    def get(self, request, *args, **kwargs):
        form=self.form_class
        course_obj=Courses.objects.all()
        self.context['courses']=course_obj
        self.context['form']=form
        return render(request,self.template_name,self.context)

    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('createcourse')

class homepage(LoginRequiredMixin,TemplateView):

    login_url = '/crm/signin'
    context={}
    template_name = 'crm/base.html'

    def get(self, request, *args, **kwargs):
        name=str(request.user)
        self.context['name']=name
        return render(request, self.template_name,self.context)
    def post(self, request, *args, **kwargs):
        search_value=request.POST.get('search')
        print(search_value)
        admission_obj=Admission.objects.filter(admission_no=search_value)
        if len(admission_obj)!=0:
            for admisssion in admission_obj:
                search_value=admisssion.enquiryid
        enquiry_obj=Enquiry.objects.filter(Q(enquiryid=search_value) | Q(studentname=search_value))

        self.context['results']=enquiry_obj
        return render(request,'crm/search.html',self.context)

class batch_creation(PermissionRequiredMixin,TemplateView):

    permission_required = 'batch.view_batch'

    context={}
    template_name ='crm/batch_add.html'
    form_class=batch_creation_form

    def get(self, request, *args, **kwargs):
        form=self.form_class
        self.context['form']=form
        return render(request,self.template_name,self.context)
    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('batch')
        self.context['form']=form
        return render(request,self.template_name,self.context)

class enquiry_creation(LoginRequiredMixin,TemplateView):
    login_url = '/crm/signin'
    context={}
    template_name = 'crm/enquiry_add.html'
    form_class=enquiry_creation_form
    model=Enquiry
    def get(self, request, *args, **kwargs):
        enquiry_obj = self.model.objects.last()
        if enquiry_obj:
            last_enquiry_id = enquiry_obj.enquiryid
            lst = int(last_enquiry_id.split('-')[1]) + 1
            enquiry_id = 'Enquiry-' + str(lst)
        else:
            enquiry_id = 'Enquiry-1'
        form=self.form_class
        self.context['form']=form(initial={'enquiryid':enquiry_id})
        return render(request,self.template_name,self.context)

    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        self.context['form']=form
        return render(request,self.template_name,self.context)

class admission_creation(LoginRequiredMixin,TemplateView):
    login_url = '/crm/signin'
    context={}
    template_name = 'crm/admission_creation.html'
    form_class=admission_creation_form

    def get(self, request, *args, **kwargs):
        admission_obj = Admission.objects.last()
        if admission_obj:
            last_admission_no = admission_obj.admission_no
            lst = int(last_admission_no.split('-')[1]) + 1
            admission_no = 'admission-' + str(lst)
        else:
            admission_no = 'admission-1'
        enquiry_id=kwargs.get('id')
        form=self.form_class
        self.context['form']=form(initial={'enquiryid':enquiry_id,'admission_no':admission_no})
        return render(request,self.template_name,self.context)
    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            form.save()
            enquiry_id=kwargs.get('id')
            enquiry_obj=Enquiry.objects.get(enquiryid=enquiry_id)
            enquiry_obj.status='Admitted'
            enquiry_obj.save()
            return redirect('home')
        else:
            self.context['form']=form
            return render(request,self.template_name,self.context)

class paymentdetails(LoginRequiredMixin,TemplateView):
    login_url = '/crm/signin'
    template_name = 'crm/paymentdetails.html'
    model=Payment
    context={}

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)

    def post(self, request, *args, **kwargs):
        admissiion_no=request.POST.get('admission no')
        payment_objs=self.model.objects.filter(admission_no=admissiion_no)

        if len(payment_objs)==0:
            if 'payment_objs' in self.context:
                del self.context['payment_objs']
            self.context['admission_no']=admissiion_no
            self.context['nopayments']='No payments made'
            return render(request,self.template_name,self.context)
        else:
            if 'nopayments' in self.context:
                del self.context['nopayments']
            sum=0
            for payment in payment_objs:
                sum+=payment.amount
            total_fee=Admission.objects.get(admission_no=admissiion_no).coursefee
            balance_fee=int(total_fee)-sum
            self.context['balance']=balance_fee
            self.context['total']=sum
            self.context['admission_no']=admissiion_no
            self.context['payment_objs']=payment_objs
            return render(request,self.template_name,self.context)

class makepayment(LoginRequiredMixin,TemplateView):
    login_url = '/crm/signin'
    template_name = 'crm/payment.html'
    form_class=payment_form
    context={}

    def get(self, request, *args, **kwargs):
        admission_no=kwargs.get('id')
        enquiry_obj=Admission.objects.get(admission_no=admission_no)
        form=self.form_class
        self.context['form']=form(initial={'admission_no':admission_no,'enquiryid':enquiry_obj.enquiryid})
        return render(request,self.template_name,self.context)
    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

class enquirylist(LoginRequiredMixin,TemplateView):
    login_url = '/crm/signin'
    context={}
    template_name = 'crm/enquiry_list.html'
    model=Enquiry

    def get(self, request, *args, **kwargs):
        enquires=self.model.objects.all()
        self.context['enquires']=enquires
        return render(request,self.template_name,self.context)

class admissionlist(LoginRequiredMixin,TemplateView):
    login_url = '/crm/signin'
    context={}
    template_name = 'crm/admission_list.html'
    model=Admission

    def get(self, request, *args, **kwargs):
        admissions=self.model.objects.all()
        self.context['admissions']=admissions
        return render(request,self.template_name,self.context)

class batch_list(LoginRequiredMixin,TemplateView):
    login_url = '/crm/signin'
    template_name ='crm/batch_list.html'
    context={}
    model=Batch

    def get(self, request, *args, **kwargs):
        batches=self.model.objects.all()
        self.context['batches']=batches
        return render(request,self.template_name,self.context)
