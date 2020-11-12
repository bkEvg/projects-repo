from django.shortcuts import render
from .models import Post
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin




class PostListView(generic.ListView):
	model = Post
	context_object_name = 'posts'
	template_name = 'blog/home.html'
	ordering = ['-date_posted']


class PostDetailView(generic.DetailView):
	model = Post
	context_object_name = 'post'


class PostCreateView(generic.CreateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class PostUpdateView(generic.UpdateView):
	model = Post
	fields = ['title', 'content']
	success_url = '/'


def about(request):
	return render(request, 'blog/about.html', {'title': 'About'})

