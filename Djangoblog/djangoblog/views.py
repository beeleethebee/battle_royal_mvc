from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import Article, Comment, User
from .forms import CommentForm
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView
)
# Create your views here.
def home(request):
    return render(request, 'landing/homepage.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=user_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

class ArticleListView(ListView):
    model = Article
    queryset = Article.objects.all
    template_name = "djangoblog/article_list.html"
    context_object_name = "articles"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ["title", "content", "image"]
    template_name = "djangoblog/article_form.html"
    success_url = reverse_lazy('articles_list')
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.slug = slugify(form.cleaned_data['title'])
        obj.save()
        return super().form_valid(form)

class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    fields = ["title", "content", "image"]
    context_object_name = "article"
    template_name = "djangoblog/article_form.html"
    success_url = reverse_lazy('articles_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        update = True
        context['update'] = update
        return context
    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)

class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    context_object_name = "article"
    success_url = reverse_lazy('articles_list')
    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)

class ArticleDetailView(DetailView):
    model = Article
    template_name = "djangoblog/article_detail.html"

    def get_context_data(self, **kwargs):
        article = get_object_or_404(Article, pk=self.kwargs["pk"])
        context = super().get_context_data(**kwargs)
        context['article'] = article
        context['form'] = CommentForm()
        context['comments'] = article.comment_set.all()
        return context

    def post(self, request, *args, **kwargs):
        commentForm = CommentForm(request.POST)
        article = get_object_or_404(Article, pk=self.kwargs["pk"])
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context['article'] = Article.objects.filter(id=self.kwargs['pk'])[0]
        context['comments'] = article.comment_set.all()
        context['form'] = commentForm

        if commentForm.is_valid() and request.user.is_authenticated:
            comment = Comment.objects.create(
                content = commentForm.cleaned_data['content'], article=article, author=request.user
            )
            context['form'] = CommentForm()

        return self.render_to_response(context=context)


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    context_object_name = "comment"
    template_name = 'djangoblog/article_confirm_delete.html'
    def get_success_url(self):
            return reverse_lazy('article_detail', kwargs={'pk': self.kwargs['article_pk']})
