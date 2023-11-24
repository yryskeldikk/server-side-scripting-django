from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse

from .forms import RegisterForm, LoginForm, ProfileEditForm, PasswordEditForm


def register_user(request):
    if request.method == "GET":
        form = RegisterForm()
        return render(request, "accounts/register.html", {"form": form})
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:login")
        else:
            return render(request, "accounts/register.html", {"form": form})
    return HttpResponseNotAllowed(["GET", "POST"])


def login_user(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "accounts/login.html", {"form": form})
    if request.method == "POST":
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("accounts:profile-view")
        else:
            return render(request, "accounts/login.html", {"form": form})
    return HttpResponseNotAllowed(["GET", "POST"])


def logout_user(request):
    if request.method == "GET":
        logout(request)
        return redirect("accounts:login")
    return HttpResponseNotAllowed(["GET"])


def profile_view(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse("UNAUTHORIZED", status=401)

    if request.method == "GET":
        profile_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        return JsonResponse(profile_data)
    return HttpResponseNotAllowed(["GET"])


def profile_edit(request):
    user = request.user

    if not user.is_authenticated:
        return HttpResponse("UNAUTHORIZED", status=401)

    if request.method == "POST":
        form = ProfileEditForm(data=request.POST, instance=user)
        password_form = PasswordEditForm(user, data=request.POST)

        if form.is_valid():
            if request.POST.get("password1"):
                if password_form.is_valid():
                    password_form.save()
                else:
                    return render(
                        request,
                        "accounts/profile.html",
                        {"form": form, "password_form": password_form},
                    )
            user = form.save()
            update_session_auth_hash(request, user)
            login(request, user)
            return redirect("accounts:profile-view")
        else:
            return render(
                request,
                "accounts/profile.html",
                {"form": form, "password_form": password_form},
            )

    if request.method == "GET":
        form = ProfileEditForm(instance=user)
        password_form = PasswordEditForm(user=user)
        return render(
            request,
            "accounts/profile.html",
            {"form": form, "password_form": password_form},
        )
    return HttpResponseNotAllowed(["GET", "POST"])
