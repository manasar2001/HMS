from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, logout, authenticate
from datetime import date
from django.db.models import Max


# Create your views here.

def index(request):
    regno = 1001 if Userregistration.objects.count() == 0 else Userregistration.objects.aggregate(max=Max('regNo'))[
                                                                   "max"] + 1
    error = ""
    if request.method == 'POST':

        fn = request.POST['firstName']
        ln = request.POST['lastName']
        gen = request.POST['gender']
        cno = request.POST['contactNo']
        e = request.POST['email']
        pas = request.POST['password']
        im = request.FILES['image']

        try:
            user = User.objects.create_user(username=e, password=pas, first_name=fn, last_name=ln)
            Userregistration.objects.create(users=user, regNo=regno, gender=gen, contactNo=cno, image=im,
                                            regDate=date.today())
            error = "no"
        except:
            error = "yes"
    return render(request, 'index.html', locals())


def user_login(request):
    error = ""
    if request.method == 'POST':
        e = request.POST['email']
        p = request.POST['pwd']
        user = authenticate(username=e, password=p)
        try:
            if user:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    return render(request, 'user_login.html', locals())


def user_home(request):

    return render(request, 'user_home.html')


def book_Hostel(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    rooms = Rooms.objects.all()
    course = Courses.objects.all()
    user = User.objects.get(id=request.user.id)
    userreg = Userregistration.objects.get(users=user)
    regcount = Registration.objects.filter(userreg=userreg).count()

    if request.method == "POST":
        rid = request.POST['rooms']
        roomid = Rooms.objects.get(id=rid)
        cid = request.POST['course']
        courseid = Courses.objects.get(id=cid)

        foodstatus = request.POST['foodstatus']
        stayfrom = request.POST['stayfrom']
        duration = request.POST['duration']
        egycontactno = request.POST['egycontactno']
        guardianName = request.POST['guardianName']
        guardianRelation = request.POST['guardianRelation']
        guardianContactno = request.POST['guardianContactno']
        corresAddress = request.POST['corresAddress']
        corresCIty = request.POST['corresCIty']
        corresState = request.POST['corresState']
        corresPincode = request.POST['corresPincode']
        pmntAddress = request.POST['pmntAddress']
        pmntCity = request.POST['pmntCity']
        pmnatetState = request.POST['pmnatetState']
        pmntPincode = request.POST['pmntPincode']

        try:
            Registration.objects.create(rooms=roomid, course=courseid, userreg=userreg, foodstatus=foodstatus,
                                        stayfrom=stayfrom, duration=duration, egycontactno=egycontactno,
                                        guardianName=guardianName,
                                        guardianRelation=guardianRelation, guardianContactno=guardianContactno,
                                        corresAddress=corresAddress,
                                        corresCIty=corresCIty, corresState=corresState, corresPincode=corresPincode,
                                        pmntAddress=pmntAddress,
                                        pmntCity=pmntCity, pmnatetState=pmnatetState, pmntPincode=pmntPincode, postingDate=date.today(), updationDate=date.today())
            error = "no"
        except:
            error = "yes"
    return render(request, 'book_Hostel.html', locals())


def room_Details(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user = request.user
    userreg = Userregistration.objects.get(users=user)
    roomdata = Registration.objects.filter(userreg=userreg)
    return render(request, 'room_Details.html', locals())

def delete_RoomDtls(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    roomdata = Registration.objects.get(id=pid)
    roomdata.delete()
    return redirect('room_Details')


def view_RoomDtls(request, pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    roomdata = Registration.objects.get(id=pid)
    totalroomcost = int(roomdata.duration) * int(roomdata.rooms.fees)
    totalfoodcost = int(roomdata.duration) * 2000
    totalcost = totalroomcost + totalfoodcost

    return render(request, 'view_RoomDtls.html', locals())


def my_Profile(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user = User.objects.get(id=request.user.id)
    data = Userregistration.objects.get(users=user)
    return render(request, 'my_Profile.html', locals())


def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user = User.objects.get(id=request.user.id)
    userdata = Userregistration.objects.get(users=user)

    error = ""
    if request.method == "POST":
        rno = request.POST['regNo']
        fname = request.POST['firstName']
        lname = request.POST['lastName']
        gen = request.POST['gender']
        cno = request.POST['contactNo']


        userdata.regNo = rno
        userdata.users.first_name = fname
        userdata.users.last_name = lname
        userdata.gender = gen
        userdata.contactNo = cno

        try:
            userdata.save()
            userdata.users.save()
            error = "no"
        except:
            error = "yes"

        try:
            image = request.FILES['image']
            userdata.image = image
            userdata.save()
        except:
            pass
    return render(request, 'edit_profile.html', locals())


def change_UserPassword(request):
    if not request.user.is_authenticated:
        return redirect('index')
    error = ""
    user = request.user
    if request.method == "POST":
        o = request.POST['old']
        n = request.POST['new']
        try:
            u = User.objects.get(id=request.user.id)
            if user.check_password(o):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = 'not'
        except:
            error = "yes"
    return render(request, 'change_UserPassword.html', locals())


def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    return render(request, 'admin_login.html', locals())


def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    allstudent = Registration.objects.all().count()
    allrms = Rooms.objects.all().count()
    allcourse = Courses.objects.all().count()

    return render(request, 'admin_home.html', locals())


def add_Course(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method == "POST":
        cod = request.POST['course_code']
        csn = request.POST['course_sn']
        cfn = request.POST['course_fn']
        try:
            Courses.objects.create(course_code=cod, course_sn=csn, course_fn=cfn)
            error = "no"
        except:
            error = "yes"
    return render(request, 'add_Course.html', locals())


def manage_Course(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    course = Courses.objects.all()
    return render(request, 'manage_Course.html', locals())


def edit_Course(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    course = Courses.objects.get(id=pid)
    if request.method == "POST":
        cod = request.POST['course_code']
        csn = request.POST['course_sn']
        cfn = request.POST['course_fn']

        course.course_code = cod
        course.course_sn = csn
        course.course_fn = cfn

        try:
            course.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'edit_Course.html', locals())


def delete_Course(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    course = Courses.objects.get(id=pid)
    course.delete()
    return redirect('manage_Course')


def add_Room(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method == "POST":
        st = request.POST['seater']
        rno = request.POST['room_no']
        fee = request.POST['fees']
        try:
            Rooms.objects.create(seater=st, room_no=rno, fees=fee)
            error = "no"
        except:
            error = "yes"
    return render(request, 'add_Room.html', locals())


def manage_Room(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    room = Rooms.objects.all()
    return render(request, 'manage_Room.html', locals())


def edit_Room(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    room = Rooms.objects.get(id=pid)
    if request.method == "POST":
        st = request.POST['seater']
        rno = request.POST['room_no']
        fee = request.POST['fees']

        room.seater = st
        room.room_no = rno
        room.fees = fee

        try:
            room.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'edit_Room.html', locals())


def delete_Room(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    room = Rooms.objects.get(id=pid)
    room.delete()
    return redirect('manage_Room')


def student_Registration(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    rooms = Rooms.objects.all()
    course = Courses.objects.all()
    regno = 1001 if Userregistration.objects.count() == 0 else Userregistration.objects.aggregate(max=Max('regNo'))[
                                                                   "max"] + 1
    if request.method == 'POST':
        rid = request.POST['rooms']
        roomid = Rooms.objects.get(id=rid)
        cid = request.POST['course']
        courseid = Courses.objects.get(id=cid)

        foodstatus = request.POST['foodstatus']
        stayfrom = request.POST['stayfrom']
        duration = request.POST['duration']

        fn = request.POST['firstName']
        ln = request.POST['lastName']
        gen = request.POST['gender']
        cno = request.POST['contactNo']
        e = request.POST['email']
        pas = request.POST['password']
        img = request.FILES['image']
        egycontactno = request.POST['egycontactno']
        guardianName = request.POST['guardianName']
        guardianRelation = request.POST['guardianRelation']
        guardianContactno = request.POST['guardianContactno']
        corresAddress = request.POST['corresAddress']
        corresCIty = request.POST['corresCIty']
        corresState = request.POST['corresState']
        corresPincode = request.POST['corresPincode']
        pmntAddress = request.POST['pmntAddress']
        pmntCity = request.POST['pmntCity']
        pmnatetState = request.POST['pmnatetState']
        pmntPincode = request.POST['pmntPincode']

        try:
            user = User.objects.create_user(username=e, password=pas, first_name=fn, last_name=ln)
            userreg = Userregistration.objects.create(users=user, regNo=regno, gender=gen, contactNo=cno, image=img, regDate=date.today())
            Registration.objects.create(rooms=roomid, course=courseid, userreg=userreg, foodstatus=foodstatus,
                                        stayfrom=stayfrom, duration=duration, egycontactno=egycontactno,
                                        guardianName=guardianName,
                                        guardianRelation=guardianRelation, guardianContactno=guardianContactno,
                                        corresAddress=corresAddress,
                                        corresCIty=corresCIty, corresState=corresState, corresPincode=corresPincode,
                                        pmntAddress=pmntAddress,
                                        pmntCity=pmntCity, pmnatetState=pmnatetState, pmntPincode=pmntPincode, postingDate=date.today(), updationDate=date.today())
            error = "no"
        except:
            error = "yes"
    return render(request, 'student_Registration.html', locals())


def manage_student(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    stdata = Registration.objects.all()
    return render(request, 'manage_student.html', locals())

def view_RegistrationDtls(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    roomdata = Registration.objects.get(id=pid)
    totalroomcost = int(roomdata.duration) * int(roomdata.rooms.fees)
    totalfoodcost = int(roomdata.duration) * 2000
    totalcost = totalroomcost + totalfoodcost
    return render(request, 'view_RegistrationDtls.html', locals())


def changePassword(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    user = request.user
    if request.method == "POST":
        o = request.POST['oldpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if user.check_password(o):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = 'not'
        except:
            error = "yes"
    return render(request, 'changePassword.html', locals())

def delete_StudentReg(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    roomdata = Registration.objects.get(id=pid)
    roomdata.delete()
    roomdata.userreg.delete()
    roomdata.userreg.users.delete()
    return redirect('manage_student')


def Logout(request):
    logout(request)
    return redirect('index')
