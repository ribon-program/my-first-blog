from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone
from .models import Post, Comment, Category
from .forms import PostForm, CommentForm, CategoryForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm #ユーザー登録
from django.contrib.auth import authenticate, login #登録後自動ログイン
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger #ページネーション
from django.contrib.auth.models import User #ユーザーページ
from django.views.generic import UpdateView, ListView, DeleteView, DetailView
from django.views.generic.edit import CreateView, FormView #Formview メール送付
from django.urls import reverse_lazy
from django.db.models import  Count, Q #検索
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.views import generic

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(posts, 5)
    p = request.GET.get('p')
    posts = paginator.get_page(p)
    post_views = Post.objects.order_by('-views')[:10] #閲覧数
    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'post_views': post_views,
    }) #閲覧数post_views        

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    queryset = post.comments.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 5)
    
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    post.views += 1 #閲覧数
    post.save() #閲覧数
    return render(request, 'blog/post_detail.html', {'post': post, 'queryset': queryset})

#def paginate_queryset(request, queryset, count):

    #paginator = Paginator(queryset, count)
    #page = request.GET.get('page')
    #try:
        #page_obj = paginator.page(page)
    #except PageNotAnInteger:
        #page_obj = paginator.page(1)
    #except EmptyPage:
        #page_obj = paginator.page(paginator.num_pages)
    #return page_obj
    
#def comment_list(request):
    #comment_list = post.comments.object.all()
    #page_obj = paginate_queryset(request, comment_list, 1)
    #context = {
        #'comment_list': page_obj.object_list,
        #'page_obj': page_obj,
    #}
    #eturn render(request, 'app/post_detail.html', context)


#class PostCommentListView(ListView):
    #model = Comment
    #context_object_name = 'comments'
    #template_name = 'blog/post_detail.html'
    #paginate_by = 5

    #def get_context_data(self, **kwargs):
        #kwargs['post'] = self.post
        #return super().get_context_data(**kwargs)

    #def get_queryset(self):
        #self.post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        #queryset = self.post.comments.order_by('created_at')
        #return queryset

    #def post_detail(request, pk):
        #post = get_object_or_404(Post, pk=pk)
        #post.views += 1 #閲覧数
        #post.save() #閲覧数
        #return render(request, 'blog/post_detail.html', {'post': post})



@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES) #request.FILESでファイル添付
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user #post.author -> post.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post) #request.FILESでファイル添付
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user #追加
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

#class CommentFormView(ListView):
    #model = Comment
    #template_name = 'blog/post_detail.html'
    #paginate_by = 5


#class CommentFormView(CreateView):
    #model = Comment
    #form_class = CommentForm
    #paginate_by = 5

    #def form_valid(self, form):
        #comment = form.save(commit=False)
        #post_pk = self.kwargs['pk']
        #comment.post = get_object_or_404(Post, pk=post_pk)
        #comment.save()
        #return redirect('post_detail', pk=post_pk)

    #def get_context_data(self, **kwargs):
        #context = super().get_context_data(**kwargs)
        #post_pk = self.kwargs['pk']
        #context['post'] = get_object_or_404(Post, pk=post_pk)
        #return context
    
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            input_username = form.cleaned_data['username']
            input_password = form.cleaned_data['password1']
            new_user = authenticate(username=input_username, password=input_password)
            if new_user is not None:
                login(request, new_user)
                return redirect('/', pk=new_user.pk)
    else:
        form = UserCreationForm()
    return render(request, 'blog/signup.html', {'form': form})

def users_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    posts = user.post_set.all().order_by('-created_at')
    return render(request, 'blog/users_detail.html', {'user': user})

#追加
class CategoryList(ListView):
    model = Category
    template_name = 'blog/category.html'
    

class CreateCategory(CreateView):
	model = Category
	template_name = 'blog/category_create.html'
	form_class = CategoryForm
	success_url = reverse_lazy('category_list')

class UpdateCategory(UpdateView):
    model = Category
    template_name = 'blog/category_update.html'
    form_class = CategoryForm
    success_url = reverse_lazy('category_list')

class DeleteCategory(DeleteView):
    model = Category
    template_name = 'blog/category_delete.html'
    success_url = reverse_lazy('category_list')

#カテゴリー結果投稿一覧表示
def index(request):
    post = Post.objects.order_by('title')
    return render(request, 'post/index.html', {'post': post})

def post_category(request, category):
    # titleがURLの文字列と一致するCategoryインスタンスを取得
    category = Category.objects.get(title=category)
    # 取得したCategoryに属するPost一覧を取得
    posts = Post.objects.filter(category=category).order_by('-published_date') #.order_by()で日付降順
    paginator = Paginator(posts, 5)
    p = request.GET.get('p')
    posts = paginator.get_page(p)
    return render(request, 'blog/post_category.html', {'posts': posts, 'category': category})

#検索
class SearchPostView(ListView):
    template_name = "blog/search_result.html"
    model = Post
    paginate_by = 5

    #Serch
    def get_queryset(self):
        query = self.request.GET.get('q', None)
        lookups = (
            Q(title__icontains=query) |
            Q(text__icontains=query)
        )
        if query is not None:
            qs = super().get_queryset().filter(lookups).distinct().order_by('-published_date') #.order_by()で日付降順
            return qs
        qs = super().get_queryset()
        return qs
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context


class PasswordChange(PasswordChangeView):
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'register/password_change.html'

class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'register/password_change_done.html'


#パスワード変更用URLの送付ページ
class PasswordReset(PasswordResetView):
    subject_template_name = 'register/mail_template/password_reset/subject.txt'
    email_template_name = 'register/mail_template/password_reset/message.txt'
    template_name = 'register/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('password_reset_done')


#パスワード変更用URLを送りましたページ
class PasswordResetDone(PasswordResetDoneView):
    template_name = 'register/password_reset_done.html'


#新パスワード入力ページ
class PasswordResetConfirm(PasswordResetConfirmView):
    form_class = MySetPasswordForm
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'register/password_reset_confirm.html'

#新パスワード設定しましたページ
class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'register/password_reset_complete.html'
