from django.shortcuts import render, redirect, HttpResponse
from srsapp.EmailBackEnd import EmailBackEnd
from django.contrib.auth import logout, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from srsapp.models import CustomUser, Course, Subjects, Student
from django.contrib.auth import get_user_model
from django.http import JsonResponse
import logging
import random
from django.shortcuts import get_object_or_404
from datetime import datetime

from srsapp.forms import UserRegistrationForm

User = get_user_model()


def BASE(request):
    return render(request, "base.html")


def SIGNUP(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            
            # Check if email exists in Student model
            student_exists = Student.objects.filter(email=email).exists()
            if student_exists:
                messages.error(request, "This email is registered as a student. Students cannot create staff accounts.")
                return redirect("signup")
            
            # Check if email already exists as a user
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "This email is already registered.")
                return redirect("signup")
            
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            messages.success(request, "Your Account Has Been Created Successfully!")
            return redirect("login")
    else:
        form = UserRegistrationForm()

    context = {
        "form": form,
    }
    return render(request, "signup.html", context)


@login_required(login_url="/")
def DASHBOARD(request):
    course_count = Course.objects.all().count
    sub_count = Subjects.objects.all().count
    student_count = Student.objects.all().count
    context = {
        "course_count": course_count,
        "sub_count": sub_count,
        "student_count": student_count,
    }
    return render(request, "dashboard.html", context)


def LOGIN(request):
    return render(request, "login.html")


def doLogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        # Check if email exists in Student model
        student_exists = Student.objects.filter(email=email).exists()
        if student_exists:
            messages.error(request, "Students cannot login through this panel. Please use the student portal.")
            return redirect("login")
        
        user = EmailBackEnd.authenticate(
            request,
            username=email,
            password=password,
        )
        if user != None:
            if user.is_staff:
                login(request, user)
                return redirect("dashboard")
            else:
                messages.error(request, "You are not authorized to access this panel")
                return redirect("login")
        else:
            messages.error(request, "Email or Password is not valid")
            return redirect("login")
    else:
        messages.error(request, "Email or Password is not valid")
        return redirect("login")


@login_required(login_url="/")
def doLogout(request):
    logout(request)
    return redirect("login")


@login_required(login_url="/")
def PROFILE(request):
    user = CustomUser.objects.get(id=request.user.id)
    context = {
        "user": user,
    }
    return render(request, "profile.html", context)


@login_required(login_url="/")
def PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get("profile_pic")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name

            if password != None and password != "":
                customuser.set_password(password)
            if profile_pic != None and profile_pic != "":
                customuser.profile_pic = profile_pic
            customuser.save()
            messages.success(request, "Your profile has been updated successfully")
            return redirect("profile")

        except:
            messages.error(request, "Your profile updation has been failed")
    return render(request, "profile.html")


@login_required(login_url="/")
def CHANGE_PASSWORD(request):
    context = {}
    ch = User.objects.filter(id=request.user.id)

    if len(ch) > 0:
        data = User.objects.get(id=request.user.id)
        context["data"]= data
    if request.method == "POST":
        current = request.POST["cpwd"]
        new_pas = request.POST["npwd"]
        user = User.objects.get(id=request.user.id)
        un = user.username
        check = user.check_password(current)
        if check == True:
            user.set_password(new_pas)
            user.save()
            messages.success(request, "Password Change  Succeesfully!!!")
            user = User.objects.get(username=un)
            login(request, user)
        else:
            messages.success(request, "Current Password wrong!!!")
            return redirect("change_password")
    return render(request, "change-password.html")


@login_required(login_url="/")
def ADD_COURSES(request):
    if request.method == "POST":
        coursesn = request.POST.get("courseshortname")
        coursefn = request.POST.get("coursefullname")
        courses = Course(courseshortname=coursesn, coursefullname=coursefn)
        courses.save()
        messages.success(request, "Course Added Succeesfully!!!")
        return redirect("add_courses")
    return render(request, "add-courses.html")


@login_required(login_url="/")
def MANAGE_COURSES(request):
    courses = Course.objects.all()
    context = {
        "courses": courses,
    }
    return render(request, "manage_course.html", context)


@login_required(login_url="/")
def DELETE_COURSES(request, id):
    courses = Course.objects.get(id=id)
    courses.delete()
    messages.success(request, "Record Delete Succeesfully!!!")

    return redirect("manage_courses")


@login_required(login_url="/")
def UPDATE_COURSES(request, id):
    courses = Course.objects.get(id=id)

    context = {
        "courses": courses,
    }

    return render(request, "update_course.html", context)


@login_required(login_url="/")
def UPDATE_COURSES_DETAILS(request):
    if request.method == "POST":
        c_id = request.POST.get("course_id")
        courseshortname = request.POST.get("courseshortname")
        coursefullname = request.POST.get("coursefullname")
        course = Course.objects.get(id=c_id)
        course.courseshortname = courseshortname
        course.coursefullname = coursefullname
        course.save()
        messages.success(request, "Your course detail has been updated successfully")
        return redirect("manage_courses")
    return render(request, "update_course.html")


@login_required(login_url="/")
def ADD_SUBJECT(request):
    course = Course.objects.all()
    if request.method == "POST":
        course_id = request.POST.get("course_id")
        subject1 = request.POST.get("subject1")
        subject2 = request.POST.get("subject2")
        subject3 = request.POST.get("subject3")
        subject4 = request.POST.get("subject4")
        subject5 = request.POST.get("subject5")
        cid = Course.objects.get(id=course_id)
        subjects = Subjects(
            course_id=cid,
            subject1=subject1,
            subject2=subject2,
            subject3=subject3,
            subject4=subject4,
            subject5=subject5,
        )
        subjects.save()
        messages.success(request, "Subject Added Succeesfully!!!")
        return redirect("add_subject")
    context = {"course": course}
    return render(request, "add-subject.html", context)


@login_required(login_url="/")
def MANAGE_SUBJECT(request):
    subjects = Subjects.objects.all()
    context = {
        "subjects": subjects,
    }
    return render(request, "manage_subject.html", context)


@login_required(login_url="/")
def DELETE_SUBJECT(request, id):
    subjects = Subjects.objects.get(id=id)
    subjects.delete()
    messages.success(request, "Record Delete Succeesfully!!!")

    return redirect("manage_subject")


@login_required(login_url="/")
def UPDATE_SUBJECTS(request, id):
    subject = Subjects.objects.get(id=id)
    course = Course.objects.all()
    context = {
        "subject": subject,
        "course": course,
    }
    return render(request, "update_subject.html", context)


@login_required(login_url="/")
def UPDATE_SUBJECTS_DETAILS(request):
    if request.method == "POST":
        subject_id = request.POST.get("subject_id")
        course_id = request.POST.get("course_id")
        subject1 = request.POST.get("subject1")
        subject2 = request.POST.get("subject2")
        subject3 = request.POST.get("subject3")
        subject4 = request.POST.get("subject4")
        subject5 = request.POST.get("subject5")

        subject = Subjects.objects.get(id=subject_id)
        cid = Course.objects.get(id=course_id)

        subject.course_id = cid
        subject.subject1 = subject1
        subject.subject2 = subject2
        subject.subject3 = subject3
        subject.subject4 = subject4
        subject.subject5 = subject5
        subject.save()
        messages.success(request, "Subject Updated Successfully!!!")
        return redirect("manage_subject")
    return redirect("manage_subject")


@login_required(login_url="/")
def REGISTER_STUDENTS(request):
    course = Course.objects.all()
    if request.method == "POST":
        course_id = request.POST.get("course_id")
        subjects_id = request.POST.get("subjects_id")
        roll_number = random.randint(100000000, 999999999)
        session = request.POST.get("session")
        fname = request.POST.get("fname")
        mname = request.POST.get("mname")
        lname = request.POST.get("lname")
        gender = request.POST.get("gender")
        gname = request.POST.get("gname")
        ocp = request.POST.get("ocp")
        income = request.POST.get("income")
        category = request.POST.get("category")
        ph = request.POST.get("ph")
        nation = request.POST.get("nation")
        mobno = request.POST.get("mobno")
        email = request.POST.get("email")
        country = request.POST.get("country")
        state = request.POST.get("state")
        city = request.POST.get("city")
        padd = request.POST.get("padd")
        cadd = request.POST.get("cadd")
        class1 = request.POST.get("class1")
        board1 = request.POST.get("board1")

        roll1 = request.POST.get("roll1")
        pyear1 = request.POST.get("pyear1")
        class2 = request.POST.get("class2")
        board2 = request.POST.get("board2")
        roll2 = request.POST.get("roll2")
        pyear2 = request.POST.get("pyear2")

        sub1 = request.POST.get("sub1")
        marks1 = request.POST.get("marks1")
        fmarks1 = request.POST.get("fmarks1")
        sub2 = request.POST.get("sub2")
        marks2 = request.POST.get("marks2")
        fmarks2 = request.POST.get("fmarks2")
        cid = Course.objects.get(id=course_id)
        sid = Subjects.objects.get(id=subjects_id)
        stu = Student(
            created_by=request.user,
            course_id=cid,
            subjects_id=sid,
            roll_number=roll_number,
            session=session,
            fname=fname,
            mname=mname,
            lname=lname,
            gender=gender,
            gname=gname,
            ocp=ocp,
            income=income,
            category=category,
            ph=ph,
            mobno=mobno,
            nation=nation,
            email=email,
            country=country,
            state=state,
            city=city,
            padd=padd,
            cadd=cadd,
            class1=class1,
            board1=board1,
            roll1=roll1,
            pyear1=pyear1,
            class2=class2,
            board2=board2,
            roll2=roll2,
            pyear2=pyear2,
            sub1=sub1,
            marks1=marks1,
            fmarks1=fmarks1,
            sub2=sub2,
            marks2=marks2,
            fmarks2=fmarks2,
        )
        stu.save()
        messages.success(request, "Student registered Succeesfully!!!")
        return redirect("reg_students")
    context = {"course": course}
    return render(request, "reg-students.html", context)


@login_required(login_url="/")
def get_subjects(request):
    if request.method == "GET":
        c_id = request.GET.get("c_id")
        sub = Subjects.objects.filter(course_id=c_id)
        subject_options = ""
        for subject in sub:
            subject_options += f'<option value="{subject.id}">{subject.subject1}+{subject.subject2}+{subject.subject3}+{subject.subject4}+{subject.subject5}</option>'
        return JsonResponse({"subject_options": subject_options})


@login_required(login_url="/")
def MANAGE_STUDENTS(request):
    if request.user.is_superuser:
        stu = Student.objects.all()
    else:
        stu = Student.objects.filter(created_by=request.user)

    context = {
        "stu": stu,
    }
    return render(request, "manage_students.html", context)


@login_required(login_url="/")
def delete_Students(request, id):
    try:
        stu = get_object_or_404(Student, id=id)
        if not request.user.is_superuser and stu.created_by != request.user:
            messages.error(request, "You are not authorized to delete this student.")
            return redirect("manage_students")
        stu.delete()
        messages.success(request, "Record Deleted Successfully!!!")
    except Student.DoesNotExist:
        messages.error(request, "Student does not exist.")
    return redirect("manage_students")


@login_required(login_url="/")
def UPDATE_STUDENTS(request, id):
    course = Course.objects.all()
    student = Student.objects.get(id=id)

    if not request.user.is_superuser and student.created_by != request.user:
        messages.error(request, "You are not authorized to update this student.")
        return redirect("manage_students")

    context = {
        "student": student,
        "course": course,
    }

    return render(request, "update_student.html", context)


@login_required(login_url="/")
def UPDATE_STUDENTS_DETAILS(request):
    if request.method == "POST":
        s_id = request.POST.get("student_id")
        session = request.POST.get("session")
        fname = request.POST.get("fname")
        mname = request.POST.get("mname")
        lname = request.POST.get("lname")
        gender = request.POST.get("gender")
        gname = request.POST.get("gname")
        ocp = request.POST.get("ocp")
        income = request.POST.get("income")
        category = request.POST.get("category")
        ph = request.POST.get("ph")
        nation = request.POST.get("nation")
        mobno = request.POST.get("mobno")
        email = request.POST.get("email")
        country = request.POST.get("country")
        state = request.POST.get("state")
        city = request.POST.get("city")
        padd = request.POST.get("padd")
        cadd = request.POST.get("cadd")
        class1 = request.POST.get("class1")
        board1 = request.POST.get("board1")
        roll1 = request.POST.get("roll1")
        pyear1 = request.POST.get("pyear1")
        class2 = request.POST.get("class2")
        board2 = request.POST.get("board2")
        roll2 = request.POST.get("roll2")
        pyear2 = request.POST.get("pyear2")
        sub1 = request.POST.get("sub1")
        marks1 = request.POST.get("marks1")
        fmarks1 = request.POST.get("fmarks1")
        sub2 = request.POST.get("sub2")
        marks2 = request.POST.get("marks2")
        fmarks2 = request.POST.get("fmarks2")
        fmarks2 = request.POST.get("fmarks2")
        stu = Student.objects.get(id=s_id)

        if not request.user.is_superuser and stu.created_by != request.user:
            messages.error(request, "You are not authorized to update this student.")
            return redirect("manage_students")

        stu.session = session
        stu.fname = fname
        stu.mname = mname
        stu.lname = lname
        stu.gender = gender
        stu.gname = gname
        stu.ocp = ocp
        stu.income = income
        stu.category = category
        stu.ph = ph
        stu.nation = nation
        stu.mobno = mobno
        stu.email = email
        stu.country = country
        stu.state = state
        stu.city = city
        stu.padd = padd
        stu.cadd = cadd
        stu.class1 = class1
        stu.board1 = board1
        stu.roll1 = roll1
        stu.pyear1 = pyear1
        stu.class2 = class2
        stu.board2 = board2
        stu.roll2 = roll2
        stu.pyear2 = pyear2
        stu.sub1 = sub1
        stu.marks1 = marks1
        stu.fmarks1 = fmarks1
        stu.sub2 = sub2
        stu.marks2 = marks2
        stu.fmarks2 = fmarks2
        stu.save()
        messages.success(request, "Your student detail has been updated successfully")
        return redirect("manage_students")
    return render(request, "update_student.html")


@login_required(login_url="/")
def VIEW_STUDENT(request, id):
    student = get_object_or_404(Student, id=id)
    # Check permissions if not superuser?
    # Current requirement implies teachers can view their students.
    # Admin sees all.
    # Assuming VIEW permissions follow MANAGE permissions logic (creator only or admin)
    if not request.user.is_superuser and student.created_by != request.user:
        messages.error(request, "You are not authorized to view this student.")
        return redirect("manage_students")

    return render(request, "student_detail.html", {"student": student})


@login_required(login_url="/")
def VIEW_COURSE(request, id):
    course = get_object_or_404(Course, id=id)
    return render(request, "course_detail.html", {"course": course})


@login_required(login_url="/")
def VIEW_SUBJECT(request, id):
    subject = get_object_or_404(Subjects, id=id)
    return render(request, "subject_detail.html", {"subject": subject})


def data_between_dates(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    stu = []

    if start_date and end_date:
        # Validate the date inputs
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            return render(
                request,
                "data_between_dates.html",
                {"stu": stu, "error_message": "Invalid date format"},
            )

        # Filter visitors between the given date range
        stu = Student.objects.filter(created_at__range=(start_date, end_date))

    return render(
        request,
        "data_between_dates.html",
        {"stu": stu, "start_date": start_date, "end_date": end_date},
    )


@login_required(login_url="/")
def Search_Students(request):
    if request.method == "GET":
        query = request.GET.get("query", "")
        if query:
            # Filter records where Roll Number or Mobile Number contains the query
            stu = Student.objects.filter(
                roll_number__icontains=query
            ) | Student.objects.filter(mobno__icontains=query)

            if not request.user.is_superuser:
                stu = stu.filter(created_by=request.user)

            messages.success(request, "Search against " + query)
            return render(request, "search-students.html", {"stu": stu, "query": query})
        else:
            print("No Record Found")
            return render(request, "search-students.html", {})
