from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import redirect, render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from shortener.forms import RegisterForm
from shortener.models import Users


def index(request):
    # print(request.user.pay_plan.name)
    user = Users.objects.filter(username="admin").first()
    email = user.email if user else "Anonymous User!"
    print(email)
    print(request.user.is_authenticated)
    if request.user.is_authenticated is False:
        email = "Anonymous User!"
    print(email)
    return render(request, "base.html", {"welcome_msg": f"Hello {email}"})


def redirect_test(request):
    print("Go Redirect")
    return redirect("index")

# test4d

@csrf_exempt
def get_user(request, user_id):
    print(user_id)
    if request.method == "GET":
        abc = request.GET.get("abc")
        xyz = request.GET.get("xyz")
        user = Users.objects.filter(pk=user_id).first()
        return render(request, "base.html", {"user":user, "params":[abc, xyz]})
    elif request.method == "POST":
        username = request.GET.get("username")
        if username:
            user = Users.objects.filter(pk=user_id).update(username=username)
        return JsonResponse(dict(status=201,msg="You just reached with Post Method!"), safe=False)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        msg = "올 바르지 않은 데이터 입니다."
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            msg = "회원 가입 완료"
        return render(request, "register.html", {"form" : form, "msg" : msg})
    else:
        form = RegisterForm()
        return render(request, "register.html", {"form" : form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request.POST)
        msg = "가입되어 있지 않거나 로그인 정보가 잘못 되었습니다."
        if form.is_valid():
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                msg = "로그인 성공 (variable) user: AbstarctBaseUser"
                login(request, user)
        return render(request, "login.html", {"form":form, "msg":msg})
    else:
        form = AuthenticationForm()
        return render(request, "login.html", {"form":form})


def logout_view(request):
    logout(request)
    return redirect("index")