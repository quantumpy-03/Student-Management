from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    profile_pic = models.ImageField(upload_to="media/profile_pic")


class Course(models.Model):
    courseshortname = models.CharField(max_length=250, default="")
    coursefullname = models.CharField(max_length=250, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.coursefullname + (self.courseshortname)


class Subjects(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    subject1 = models.CharField(max_length=250, default="")
    subject2 = models.CharField(max_length=250, default="")
    subject3 = models.CharField(max_length=250, default="")
    subject4 = models.CharField(max_length=250, default="")
    subject5 = models.CharField(max_length=250, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class Student(models.Model):
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True
    )
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    subjects_id = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    roll_number = models.IntegerField(default=0)
    session = models.CharField(max_length=250, default="")
    fname = models.CharField(max_length=250, default="")
    mname = models.CharField(max_length=250, default="")
    lname = models.CharField(max_length=250, default="")
    gender = models.CharField(max_length=250, default="")
    gname = models.CharField(max_length=250, default="")
    ocp = models.CharField(max_length=250, default="")
    income = models.CharField(max_length=250, default="")
    category = models.CharField(max_length=250, default="")
    ph = models.CharField(max_length=250, default="")
    nation = models.CharField(max_length=250, default="")
    mobno = models.CharField(max_length=250, default="")
    email = models.EmailField(max_length=100)
    country = models.CharField(max_length=250, default="")
    state = models.CharField(max_length=250, default="")
    city = models.CharField(max_length=250, default="")
    padd = models.TextField(blank=True, default=0)
    cadd = models.TextField(blank=True, default=0)
    class1 = models.CharField(max_length=250, default="")
    board1 = models.CharField(max_length=250, default="")
    roll1 = models.CharField(max_length=250, default="")
    pyear1 = models.CharField(max_length=250, default="")
    class2 = models.CharField(max_length=250, default="")
    board2 = models.CharField(max_length=250, default="")
    roll2 = models.CharField(max_length=250, default="")
    pyear2 = models.CharField(max_length=250, default="")
    sub1 = models.CharField(max_length=250, default="")
    marks1 = models.IntegerField()
    fmarks1 = models.IntegerField()
    sub2 = models.CharField(max_length=250, default="")
    marks2 = models.IntegerField()
    fmarks2 = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.fname
