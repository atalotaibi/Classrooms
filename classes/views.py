from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Classroom, Student
from .forms import ClassroomForm, SignupForm, SigninForm, StudentForm
from django.contrib.auth import login, authenticate, logout

def classroom_list(request):
	classrooms = Classroom.objects.all()
	context = {
		"classrooms": classrooms,
	}
	return render(request, 'classroom_list.html', context)


def classroom_detail(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)
	students = classroom.students.all().order_by('name','-exam_grade')
	context = {
		"classroom": classroom,
		"students": students,
	}
	return render(request, 'classroom_detail.html', context)


def classroom_create(request):
	if request.user.is_anonymous:
		return redirect('signin')

	form = ClassroomForm()
	if request.method == "POST":
		form = ClassroomForm(request.POST, request.FILES or None)
		if form.is_valid():
			classroom = form.save(commit=False)
			classroom.teacher = request.user
			form.save()
			messages.success(request, "Successfully Created!")
			return redirect('classroom-list')
	context = {
	"form": form,
	}
	return render(request, 'create_classroom.html', context)


def classroom_update(request, classroom_id):
	if request.user.is_anonymous:
		messages.warning(request, "You have no permission")
		return redirect('classroom-detail',classroom_id)

	classroom = Classroom.objects.get(id=classroom_id)
	if not (request.user.is_staff or request.user == classroom.teacher):
		messages.warning(request, "You have no permission")
		return redirect('classroom-detail',classroom_id)
    	
	
	form = ClassroomForm(instance=classroom)
	if request.method == "POST":
		form = ClassroomForm(request.POST, request.FILES or None, instance=classroom)
		if form.is_valid():
			form.save()
			messages.success(request, "Successfully Edited!")
			return redirect('classroom-list')
	context = {
	"form": form,
	"classroom": classroom,
	}
	return render(request, 'update_classroom.html', context)


def classroom_delete(request, classroom_id):
	if request.user.is_anonymous:
		messages.warning(request, "You have no permission")
		return redirect('classroom-detail',classroom_id)

	classroom = Classroom.objects.get(id=classroom_id)
	if not (request.user.is_staff or request.user == classroom.teacher):
		messages.warning(request, "You have no permission")
		return redirect('classroom-detail',classroom_id)

	classroom.delete()
	messages.success(request, "Successfully Deleted!")
	return redirect('classroom-list')

def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            uesr_obj = form.save(commit=False)
            uesr_obj.set_password(uesr_obj.password)
            uesr_obj.save()
            login(request, uesr_obj)
            return redirect('classroom-list')
    context = {
        "form":form,
    }
    
    return render(request, 'signup.html', context)

def signin(request):
    form = SigninForm()
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            my_username = form.cleaned_data['username']
            my_password = form.cleaned_data['password']
            uesr_obj = authenticate(username=my_username, password=my_password)
            if uesr_obj is not None:
                login(request, uesr_obj)
                return redirect('classroom-list')
    context = {
        "form":form,
    }
    return render(request, 'signin.html', context)

def signout(request):
    logout(request)
    return redirect('signin')

def add_student(request, classroom_id):
	if request.user.is_anonymous:
		messages.warning(request, "You have no permission")
		return redirect('classroom-detail',classroom_id)
	
	classroom = Classroom.objects.get(id=classroom_id)
	if not (request.user.is_staff or request.user == classroom.teacher):
		messages.warning(request, "You have no permission")
		return redirect('classroom-detail',classroom_id)
	
	form = StudentForm()
	if request.method == "POST":
		form = StudentForm(request.POST)
		if form.is_valid():
			student = form.save(commit=False)
			student.classroom = classroom
			student.save()
			return redirect('classroom-detail', classroom_id)
	context = {
        "form":form,
        "classroom": classroom,
    }
	return render(request, 'add_student.html', context)

def student_update(request, student_id):
	student = Student.objects.get(id=student_id)
	if request.user.is_anonymous:
		messages.warning(request, "You have no permission")
		return redirect('classroom-detail', student.classroom.id)
	
	if not (request.user.is_staff or request.user == student.classroom.teacher):
		messages.warning(request, "You have no permission")
		return redirect('classroom-detail', student.classroom.id)

	form = StudentForm(instance=student)
	if request.method == "POST":
		form = StudentForm(request.POST, request.FILES or None, instance=student)
		if form.is_valid():
			form.save()
			messages.success(request, "Successfully Edited!")
			return redirect('classroom-list')
	context = {
	"form": form,
	"student": student,
	}
	return render(request, 'update_student.html', context)


def student_delete(request, student_id):
	if request.user.is_anonymous:
		messages.warning(request, "You have no permission")
		return redirect('classroom-detail', student.classroom.id)
	student = Student.objects.get(id=student_id)
	
	if not (request.user.is_staff or request.user == student.classroom.teacher):
		messages.warning(request, "You have no permission")
		return redirect('classroom-detail', student.classroom.id)

	Student.objects.get(id=student_id).delete()
	messages.success(request, "Successfully Deleted!")
	return redirect('classroom-list')
