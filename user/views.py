from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from user.forms import SignUpForm, SignInForm


def logout_view(request):
    """logout view"""

    try:
        logout(request)
    except:
        raise Exception("unable to logout")
    else:
        return redirect("/")


def redirect_view(request):
    """redirects user depending on user's privileges"""

    if(request.user.is_authenticated):
        if(request.user.is_teacher):
            return redirect("/quiz/create-quiz/")
        else:
            return redirect(f"/quiz/{request.user.pk}/")
    else:
        return redirect("/signin/")


def sign_up(request):
    """both student's and teacher's sign up view using builtin model form"""

    if request.user.is_authenticated:
        return redirect("/")
    context = {'form': SignUpForm}
    return render(request, 'signin/sign_up.html', context)


def sign_in(request):
    """both student's and teacher's sign in view using builtin model form"""

    if request.user.is_authenticated:
        return redirect("/")
    context = {'form': SignInForm}
    return render(request, 'signin/sign_in.html', context)


def teacher_sign_up(request):
    """sign up post request validation view"""

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            print(request.POST)
            teacher = form.save(commit=False)
            teacher.is_teacher = True
            teacher.save()
        else:
            return JsonResponse({"error": "details are invalid"}, safe=False)
    return redirect("/")


def teacher_sign_in(request):
    """sign in post request validation view"""

    if request.method == 'POST':
        form = SignInForm(data=request.POST)
        user = None
        print(request.POST)
        if form.is_valid():
            try:
                user = authenticate(request, username=request.POST.get(
                    'username'), password=request.POST.get('password'))
            except:
                return JsonResponse({"error": "user not found"}, safe=False)
            if user is not None and user.is_teacher:
                try:
                    login(request, user)
                    return redirect("/quiz/create-quiz/")
                except:
                    return JsonResponse({"error": "unable to login"}, safe=False)
            else:
                return JsonResponse({"error": "user not found"}, safe=False)
        else:
            return JsonResponse({"error": "details are invalid"}, safe=False)
    return redirect("/")


def student_sign_up(request):
    """student sign up post request validation view"""

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            print(request.POST)
            form.save()
        else:
            return JsonResponse({"error": "details are invalid"}, safe=False)
    return redirect("/")


def student_sign_in(request):
    """student sign in post request validation view"""

    if request.method == 'POST':
        form = SignInForm(data=request.POST)
        user = None
        print(request.POST)
        if form.is_valid():
            try:
                user = authenticate(request, username=request.POST.get(
                    'username'), password=request.POST.get('password'))
            except:
                raise Exception("unablr to authenticate")
            if user is not None and not user.is_teacher:
                try:
                    login(request, user)
                    return redirect("/quiz/"+str(user.pk)+"/")
                except:
                    raise Exception("unable to login")
            else:
                return JsonResponse({"error": "user not found"}, safe=False)
        else:
            return JsonResponse({"error": "details are invalid"}, safe=False)
    return redirect("/")
