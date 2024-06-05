from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Courses(models.Model):
    course_code = models.CharField(max_length=255, null=True)
    course_sn = models.CharField(max_length=100, null=True)
    course_fn = models.CharField(max_length=255, null=True)
    posting_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.course_code

class Rooms(models.Model):
    seater = models.CharField(max_length=100, null=True)
    room_no = models.CharField(max_length=100, null=True)
    fees = models.CharField(max_length=255, null=True)
    posting_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.seater

class States(models.Model):
    statename = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.statename

class Userregistration(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    regNo = models.IntegerField(null=True)
    gender = models.CharField(max_length=50, null=True)
    contactNo = models.CharField(max_length=15, null=True)
    image = models.FileField(max_length=200, null=True)
    regDate = models.DateField(null=True)
    updationDate = models.DateTimeField(auto_now_add=True)

class Registration(models.Model):
    rooms = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    foodstatus = models.CharField(max_length=100, null=True)
    stayfrom = models.CharField(max_length=50, null=True)
    duration = models.CharField(max_length=50, null=True)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    userreg = models.ForeignKey(Userregistration, on_delete=models.CASCADE)
    egycontactno = models.CharField(max_length=15, null=True)
    guardianName = models.CharField(max_length=250, null=True)
    guardianRelation = models.CharField(max_length=250, null=True)
    guardianContactno = models.CharField(max_length=15, null=True)
    corresAddress = models.CharField(max_length=350, null=True)
    corresCIty = models.CharField(max_length=100, null=True)
    corresState = models.CharField(max_length=100, null=True)
    corresPincode = models.CharField(max_length=50, null=True)
    pmntAddress = models.CharField(max_length=350, null=True)
    pmntCity = models.CharField(max_length=100, null=True)
    pmnatetState = models.CharField(max_length=100, null=True)
    pmntPincode = models.CharField(max_length=50, null=True)
    postingDate = models.DateField(null=True)
    updationDate = models.DateField(null=True)



