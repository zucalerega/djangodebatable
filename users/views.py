from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm, ReportForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from .models import Profile, Report, Follow
from users import views as user_views
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from posts.models import Post
from django.urls import reverse
from chat.models import Rating
# Create your views here.
def home_view(request):
    return render(request, 'users/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect("/profileChange/")
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form':form})

@login_required
def dynamic_lookup_view(request, username):
    obj = get_object_or_404(Profile, user=User.objects.filter(username=username)[0])
    follow = len(Follow.objects.filter(follower=request.user, following=User.objects.get(username=username)))
    obj.respecting = len(Follow.objects.filter(follower=User.objects.get(username=username)))
    obj.respectedBy = len(Follow.objects.filter(following=User.objects.get(username=username)))
    obj.save()
    ratings = Rating.objects.filter(recipient=str(username))
    posts = Post.objects.filter(author=User.objects.get(username=username)).order_by('-date_posted')
    context = {"object": obj, "follow": follow, "totalratings": len(Rating.objects.filter(recipient=str(username))), "ratings": ratings, "posts": posts}
    return render(request, "users/profile.html", context)

def profile_list_view(request):
	queryset = Profile.objects.all()
	context = {
		"object_list": queryset
	}
	return render(request, "users/profile.html", context)

@login_required
def profileChange(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Update success')
            return redirect('users:profile', request.user)
    else:
        u_form=UserUpdateForm(instance = request.user)
        p_form=ProfileUpdateForm(instance = request.user.profile)
    context={
        'u_form':u_form,
        'p_form':p_form,

    }
    return render(request, 'users/profileChange.html', context)

@login_required
def report_view(request, username):
    obj = Report.objects.create(offender=username, reporter=request.user.username)
    form = ReportForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()

        form = ReportForm()
        messages.success(request, f'User Reported')

        return redirect('users:profile', username)
    context = {
    'form': form
    }

    return render(request, "users/report.html", context)

def follow_view(request, username):
    if len(Follow.objects.filter(follower=request.user, following=User.objects.get(username=username))) == 0:
        follow = Follow.objects.create(follower=request.user, following=User.objects.get(username=username))
    else:
        Follow.objects.get(follower=request.user, following=User.objects.get(username=username)).delete()
    return redirect('users:profile', username)
