from email import message
from django.shortcuts import render, HttpResponseRedirect
from . forms import SignUpForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from . models import Post

# home view
def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts})

#about
def about(request):
    return render(request, 'blog/about.html')

#contact
def contact(request):
    return render(request, 'blog/contact.html')
    
#dashboard
def dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        if user.is_superuser == True:
            posts = Post.objects.all()
        else:
            posts= Post.objects.filter(uname= user)
    
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request, 'blog/dashboard.html',{'posts': posts, 'full_name': full_name, 'groups': gps})
    else:
        return HttpResponseRedirect('/login/')

#logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

#signup
def user_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
           form.save() 
           messages.success(request, 'registration success!!')
           return HttpResponseRedirect('/login/')
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})

#login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = LoginForm(request=request, data=request.POST)
            if fm.is_valid():
                nm = fm.cleaned_data['username']
                psw = fm.cleaned_data['password']
                user = authenticate(username=nm, password=psw)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'User Login Successfully!!')
                    return HttpResponseRedirect('/dashboard/')
                else:
                    messages.error(request, 'wrong user enter correct one')
                    fm = LoginForm()
                    return render(request, 'blog/login.html', {'form': fm})
        else:
            fm = LoginForm()
        return render(request, 'blog/login.html', {'form': fm})
    else:
        return HttpResponseRedirect('/dashboard/')

#add new post
def add_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                name = request.user
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                add_pst = Post(uname= name, title= title, desc= desc)
                add_pst.save() 
                messages.success(request, 'post added successfully!!!')
                return HttpResponseRedirect('/dashboard/')
                form = PostForm()
        else:
            form = PostForm()
        return render(request, 'blog/addpost.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')    

#update post
def update_post(request,id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = Post.objects.get(pk= id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
                messages.success(request, 'updated successfull!!')
                return HttpResponseRedirect('/dashboard/')
        else:
            pi = Post.objects.get(pk= id)
            form = PostForm(instance=pi)
        return render(request, 'blog/updatepost.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')

#update post
def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = Post.objects.get(pk= id)
            pi.delete()
            messages.success(request, 'post deleted successfully!!!')
            return HttpResponseRedirect('/dashboard/')
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')

