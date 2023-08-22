from django.shortcuts import render
from django.views.generic import (ListView, DetailView, UpdateView,
                                  CreateView, DeleteView)
from datetime import datetime
# Create your views here.
from .models import Post
from django.views import View
from .forms import NewsForm
from django.core.paginator import Paginator

from .filters import PostFilter # импортируем недавно написанный фильтр

class NewsList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = ['-posted']
    paginate_by = 2
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['value1'] = None

        return context
    
class Search(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(
            self.request.GET,
            queryset=self.get_queryset()
        )
        return context
      
class NewsView(View):
    def get(self, request):
        news = Post.objects.order_by('-posted')

        paginator = Paginator(news, 1)

        news = paginator.get_page(request.GET.get('page', 1))

        data = {
            'news': news,
        }
        return render(request, 'post_detail.html', data)


class PostDetail(DetailView):
    template_name = 'post_detail.html'
    queryset = Post.objects.all()


class PostCreate(CreateView):
    template_name = 'post_create.html'
    form_class = NewsForm
    success_url = '/news'


class PostEdit(UpdateView):
    template_name = 'post_create.html'
    form_class = NewsForm
    success_url = '/news'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDelete(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news'
