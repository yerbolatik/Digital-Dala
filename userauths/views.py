from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View
from django.template.loader import render_to_string

from userauths.forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from userauths.models import Profile, User
from core.models import Post


def RegisterView(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already registered!")
        return redirect("core:index")

    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        full_name = form.cleaned_data.get("full_name")
        phone = form.cleaned_data.get("phone")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")

        user = authenticate(email=email, password=password)
        login(request, user)

        profile = Profile.objects.get(user=request.user)
        profile.full_name = full_name
        profile.phone = phone
        profile.save()

        messages.success(
            request, f"Hi! {full_name}! Your account was created successfully.")
        return redirect("core:index")

    context = {
        "form": form
    }
    return render(request, "userauths/sign_up.html", context)


def LoginView(request):

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You are logged In!")
                return redirect("core:index")
            else:
                messages.error(request, "Username or password does not match")
                return redirect("userauths:sign-up")
        except:
            messages.error(request, "Username does not exist")
            return redirect("userauths:sign-up")

    return HttpResponseRedirect("/")


def LogoutView(request):
    logout(request)
    messages.success(request, "You are logged out!")
    return redirect("userauths:sign-up")


@login_required
def my_profile(request):
    profile = request.user.profile
    posts = Post.objects.filter(active=True, user=request.user).order_by("-id")

    followers = profile.followers.all()
    followings = profile.followings.all()

    context = {
        "profile": profile,
        "posts": posts,
        "followers": followers,
        "followings": followings,
    }
    return render(request, "userauths/my_profile.html", context)


class EditProfileView(View):
    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        form = ProfileUpdateForm(instance=profile)
        return render(request, 'userauths/edit_profile.html', {'form': form})

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('userauths:my_profile')
        return render(request, 'userauths/edit_profile.html', {'form': form})
