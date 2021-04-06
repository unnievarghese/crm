from django.db import models
from datetime import date

class Courses(models.Model):
    course_name=models.CharField(max_length=50,unique=True)
    course_duration=models.CharField(max_length=50)

    def __str__(self):
        return self.course_name

class Batch(models.Model):
    batch_code=models.CharField(max_length=50,unique=True)
    course=models.ForeignKey(Courses,on_delete=models.CASCADE)
    batch_date=models.DateField()
    course_fee=models.CharField(max_length=50)
    action={
        ('Yet to beign','Yet to beign'),
        ('Ongoing','Ongoing'),
        ('completed','completed')
    }
    batch_status=models.CharField(max_length=120,choices=action)

    def __str__(self):
        return self.batch_code

class Enquiry(models.Model):
    enquiryid=models.CharField(primary_key=True,max_length=100)
    studentname=models.CharField(max_length=150)
    address=models.TextField()
    qualification=models.CharField(max_length=50)
    collegename=models.CharField(max_length=100)
    course=models.ForeignKey(Courses,on_delete=models.CASCADE)
    batch=models.ForeignKey(Batch,on_delete=models.CASCADE)
    contact=models.IntegerField()
    email=models.EmailField(unique=True)
    enquirydate=models.DateField(default=date.today())
    followup_date=models.DateField()
    action={
        ('call_back','call_back'),
        ('Admitted','Admitted'),
        ('Cancel','Cancel')
    }
    status=models.CharField(max_length=20,choices=action)

    def __str__(self):
        return str(self.enquiryid)

class Admission(models.Model):
    admission_no=models.CharField(max_length=50,unique=True)
    enquiryid=models.CharField(max_length=50)
    coursefee=models.IntegerField()
    batch_code=models.ForeignKey(Batch,on_delete=models.CASCADE)
    date=models.DateField(default=date.today())

    def __str__(self):
        return self.admission_no

class Payment(models.Model):
    admission_no=models.CharField(max_length=50)
    amount=models.IntegerField()
    payment_date=models.DateField(default=date.today())
    enquiryid=models.CharField(max_length=50)

    def __str__(self):
        return self.amount
