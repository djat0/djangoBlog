from django.shortcuts import render, redirect
from .models import UserProfile
from .forms import UserForm, UserProfileForm, EditUserForm, ResetPassForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def register(request):
    if request.user.is_authenticated:
        return redirect('post')
    if request.method == 'POST':
        form1 = UserForm(request.POST or None)
        form2 = UserProfileForm(request.POST or None, request.FILES or None)
        print('forms not filled')
        if form1.is_valid():
            print('form 1 valid')
        if form2.is_valid():
            print('form 2 is valid')
        else:
            print(form2.errors)
        if form1.is_valid():
            print('both forms are valid')
            user = form1.save()
            UserProfile = form2.save(commit=False)
            UserProfile.user = user
            UserProfile.save()
            messages.success(request, 'Account successfully created')
            return redirect('login')
    context = {'form1': UserForm, 'form2': UserProfileForm}
    return render(request, 'Profile/register.html', context)


def userLogin(request):
    if request.user.is_authenticated:
        return redirect('post')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('post')
        else:
            messages.info(request, 'username and password did not match')

    return render(request, 'Profile/login.html')


def userLogout(request):
    logout(request)
    return redirect('login')


def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = {'user_profile': user_profile}
    return render(request, 'Profile/profile.html', context)


def editProfile(request):
    user = request.user
    if request.method == 'POST':
        form = EditUserForm(request.POST)
        if form.is_valid():
            user.username = form.data['username']
            user.first_name = form.data['first_name']
            user.last_name = form.data['last_name']
            user.email = form.data['email']
            user.save()
            return redirect('profile')
    else:
        form = EditUserForm(initial={'username': user.username, 'first_name': user.first_name,
                            'last_name': user.last_name, 'email': user.email})

    context = {'form': form}
    return render(request, 'Profile/edit-profile.html', context)


def resetPassword(request):
    user = request.user
    if request.method == 'POST':
        form = ResetPassForm(request.POST)
        if form.is_valid():
            if user.check_password(form.data['old_password']) != True:
                messages.info(request, 'incorrect password')
            else:
                if form.data['new_password'] != form.data['confirm_password']:
                    messages.info(
                        request, 'new password and confirm passwordd did not match')
                else:
                    user.set_password(form.data['new_password'])
                    messages.info(request, 'password changed successfully')
                    return redirect('profile')
    else:
        form = ResetPassForm()

    context = {'form': form}
    return render(request, 'Profile/reset-password.html', context)
