from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.posts_list, name='fetch_all_posts'),
    path('posts/<slug:slug>/', views.post_detail, name='fetch_single_post'),
    path('bookmarks/', views.user_bookmarks, name='user_bookmarks'),
    path('bookmarks/post/<int:post_id>/', views.user_bookmarks, name='bookmark_post'),
    path('bookmarks/<int:bookmark_id>/', views.manage_bookmark, name='manage_bookmark'),

    # path('post/<int:post_id>/', views.fetch_single_post, name='post'),
    # path('comment/<int:post_id>/', views.create_comment, name='comment'),
    # path('comment/<int:comment_id>/edit/', views.update_comment, name='update_comment'),
    # path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),

]

