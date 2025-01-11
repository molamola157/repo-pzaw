from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from datetime import datetime
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from .forms import CustomAuthenticationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Post, Vote

def post_list(rekwest):
    posts = Post.objects.all().order_by('-created_at')
    return render(rekwest, 'polls/post_list.html', {'posts': posts})

def post_detail(rekwest, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(rekwest, 'polls/post_detail.html', {'post': post})

from django.utils.timezone import now  
from django.http import HttpResponse, HttpResponseBadRequest
from .models import Post

def post_new(rekwest):
    if rekwest.method == "POST":
        content = rekwest.POST.get("content", "").strip()
        tytul = rekwest.POST.get("contenttytul", "").strip()
        

    
        if not tytul:
            return HttpResponseBadRequest("Daj tytuł!")
        if len(tytul) > 50:
            return HttpResponseBadRequest("Tytuł nie może przekraczać 50 znaków")
        if not content:
            return HttpResponseBadRequest("Wsadź coś do posta!")
        if len(content) < 5:
            return HttpResponseBadRequest("Treść posta musi mieć co najmniej 5 znaków")
        if len(content) > 1000:
            return HttpResponseBadRequest("Treść posta nie może przekraczać 1000 znaków")

        post = Post.objects.create(
            title=tytul,
            content=content,
            created_at=now(),
            user=rekwest.user  
        )


        return redirect("post_detail", post_id=post.id)

    return render(rekwest, "polls/post_new.html")

def register(rekwest):
    if rekwest.method == 'POST':
        form = CustomUserCreationForm(rekwest.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(rekwest, 'polls/register.html', {'form': form})


def user_login(rekwest):
    if rekwest.method == 'POST':
        form = CustomAuthenticationForm(rekwest.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(rekwest, username=username, password=password)
            if user is not None:
                login(rekwest, user)
                return redirect('post_list')  
            else:
                form.add_error(None, 'a')
        else:
            print(form.errors)
            print("kurde")
           
    else:
        form = CustomAuthenticationForm()
    return render(rekwest, 'polls/login.html', {'form': form})

@csrf_exempt
def post_reaction(rekwest, post_id, action):
    if not rekwest.user.is_authenticated:
        return JsonResponse({'error': 'Musisz być zalogowany, aby głosować'}, status=403)

    post = get_object_or_404(Post, pk=post_id)

    if post.voters.filter(username=rekwest.user.username).exists():
        return JsonResponse({'error': 'Już głosowałeś na ten post'}, status=400)

    if action == 'like':
        post.likes += 1
    elif action == 'dislike':
        post.dislikes += 1
    else:
        return JsonResponse({'error': 'nie'}, status=400)

    post.voters.add(rekwest.user)

    post.save()

    return JsonResponse({'likes': post.likes, 'dislikes': post.dislikes})
