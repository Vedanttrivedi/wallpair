from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from  . models import Post
from .forms import PostForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def home(request):
	dic={
		'user':Post.objects.all()
	}
	return render(request,'blog/home.html',dic)

class PostListView(ListView):
	model  = Post
	template_name='blog/home.html'
	context_object_name = 'user'
	ordering = ['-date_posted']
	paginate_by = 3

class PostDetailView(DetailView):
	model = Post
	#it looks for template in below order
	# <app>/<model>_<type of view>.html

class PostCreateView(LoginRequiredMixin,CreateView):
	model = Post
	fields = ['title','content']
	success_url = '/'

	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
	model  = Post
	fields = ['title','content']

	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user==post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	model= Post
	success_url= '/'
	template_name = 'blog/post_delete.html'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class UserPostListView(ListView):
	model = Post
	template_name = 'blog/poster.html'
	context_object_name = 'posts'
	paginate_by = 3

	def get_queryset(self):
		user = get_object_or_404(User,username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')

def timepass(request):
	return redirect('blog-home')


def about(request):
	return render(request,'blog/about.html',{'user':User.objects.filter(username='vedant').first()})


def myroute(request):
	return HttpResponse('<h3>django</h3>')

def tandc(request):
    return render(request,'blog/tandc.html')
    
def team(request):
    return render(request,'blog/team.html')