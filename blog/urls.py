from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from blog.views import SearchPostView, ListView #CommentFormView

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('users/<int:pk>/', views.users_detail, name='users_detail'), #ユーザページ
    #path('<int:pk>', views.PostList.as_view(), name='post_list'),
    path('<int:pk>', views.post_list, name='post_list'), #ページネーション 
    path('signup/', views.signup, name='signup'), #ユーザー登録
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    #path('post/<int:pk>/', views.CommentListView.as_view(), name='post_comments'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('post/<pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<pk>/remove/', views.post_remove, name='post_remove'),
    path('post/<str:category>/', views.post_category, name='post_category'), # 追加
    #path('post/<int:pk>/comment/', CommentFormView.as_view(), name='comment_form'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    #path('post/<int:pk>/comments/<int:comment_pk>', views.post_comments, name='post_comments'), #コメントページ
    #path('comment/<int:pk>/', CommentFormView.as_view(), name='comment_form'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    path('category/', views.CategoryList.as_view(), name='category_list'),
    path('category/create', views.CreateCategory.as_view(), name='create_category'),
    path('category/update/<int:pk>', views.UpdateCategory.as_view(), name='update_category'),
    path('category/delete/<int:pk>', views.DeleteCategory.as_view(), name='delete_category'),
    path('search/', SearchPostView.as_view(), name='search_result'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
]