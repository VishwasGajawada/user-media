from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import (TemplateView,ListView)
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from userapp.models import Post,UserProfile,Comment
from userapp.forms import UserCreationForm,UserProfileForm,PostForm,UserUpdateForm,CommentForm,PostUpdateForm
# Create your views here.
class IndexView(ListView):
    context_object_name = 'posts'
    model = Post
    template_name = "userapp/index.html"

    def get_queryset(self):
        queryset = self.model.objects.all().order_by('-created')
        return queryset

def signup(request):
    user_form = UserCreationForm()
    profile_form = UserProfileForm()
    context = {'user_form': user_form, 'profile_form': profile_form}
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST,request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('/')

    return render(request,'userapp/signup.html',context)

@login_required(login_url='login')
def profile(request,pk=1):
    # user = request.user
    user = User.objects.get(id = pk)
    prof = UserProfile.objects.filter(user=user)[0]
    posts = Post.objects.filter(user = user)
    context ={'profile':prof,'posts':posts,'post_author':user}
    return render(request,'userapp/profile.html',context)

@login_required(login_url='login')
def update_profile(request):
    user = request.user
    uform = UserUpdateForm(instance = user)
    pform = UserProfileForm(instance = user.profile)
    context = {'user_form':uform , 'profile_form':pform}
    if request.method == 'POST':
        uform = UserUpdateForm(request.POST,instance = user)
        pform = UserProfileForm(request.POST,request.FILES,instance = user.profile)
        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()
            # usr = uform.save()
            # pro = pform.save(commit=False)
            # pro.user = usr
            # pro.save()
            # return redirect('index')
            return redirect('profile',pk=user.id)

    return render(request,'userapp/update_profile.html',context)

@login_required(login_url='login')
def add_post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('index')

    context = {'form':form}
    return render(request,'userapp/add_post.html',context)


@login_required(login_url='login')
def post_detail(request,pk):
    post = Post.objects.get(id = pk)
    post_form = PostUpdateForm(instance=post)
    comments = Comment.objects.filter(post = post).order_by('-time_commented')
    comment_form = CommentForm()
    context = {'post_form':post_form, 'comment_form':comment_form,'post':post,'old_comments':comments}

    # post_update
    if request.method == 'POST':
        post_form = PostUpdateForm(request.POST,instance = post)
        if post_form.is_valid():
            post_form.save()
            return redirect('post_detail',pk)
    
    return render(request,'userapp/post_detail.html',context)

@login_required(login_url='login')
def delete_post(request,pk):
    post = Post.objects.get(id = pk)
    # post = get_object_or_404(Post,pk = pk)
    if (request.user != post.user) or post is None:
        return redirect('index')
    user = post.user
    post.delete()
    return redirect('profile',pk=user.id)

@login_required(login_url='login')
def make_comment(request,pk):
    post = Post.objects.get(id = pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail',pk = pk)
    return redirect('post_detail',pk = pk)

@login_required(login_url='login')
def delete_comment(request,pk):
    comment = Comment.objects.get(id = pk)
    post = comment.post
    if request.user!=comment.user:
        return redirect('post_detail',pk=comment.post.id)
    comment.delete()
    return redirect('post_detail',pk=comment.post.id)


