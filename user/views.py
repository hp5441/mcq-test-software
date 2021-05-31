from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from user.forms import SignUpForm, SignInForm


def logout_view(request):
    try:
        logout(request)
    except:
        raise Exception("unable to logout")
    else:
        return redirect("/")


def redirect_view(request):
    if(request.user.is_authenticated):
        if(request.user.is_teacher):
            return redirect("/quiz/quiz-create/")
        else:
            return redirect(f"/quiz/{request.user.pk}/")
    else:
        return redirect("/signin/")


def sign_up(request):
    if request.user.is_authenticated:
        return redirect("/")
    context = {'form': SignUpForm}
    return render(request, 'signin/sign_up.html', context)


def sign_in(request):
    if request.user.is_authenticated:
        return redirect("/")
    context = {'form': SignInForm}
    return render(request, 'signin/sign_in.html', context)


def teacher_sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            print(request.POST)
            teacher = form.save(commit=False)
            teacher.is_teacher = True
            teacher.save()
            return HttpResponse("thanks")


def teacher_sign_in(request):
    if request.method == 'POST':
        form = SignInForm(data=request.POST)
        print(request.POST)
        if form.is_valid():
            user = authenticate(request, username=request.POST.get(
                'username'), password=request.POST.get('password'))
            if user is not None:
                try:
                    login(request, user)
                    return redirect("/quiz/create-quiz/")
                except:
                    raise Exception("unable to login")
            else:
                raise Exception("user not found")


def student_sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            print(request.POST)
            form.save()
            return HttpResponse("thanks")


def student_sign_in(request):
    if request.method == 'POST':
        form = SignInForm(data=request.POST)
        print(request.POST)
        if form.is_valid():
            user = authenticate(request, username=request.POST.get(
                'username'), password=request.POST.get('password'))
            if user is not None:
                try:
                    login(request, user)
                    return redirect("/quiz/"+str(user.pk)+"/")
                except:
                    raise Exception("unable to login")
            else:
                raise Exception("user not found")
