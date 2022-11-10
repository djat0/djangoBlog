from django.urls import path
from . import views

urlpatterns = [
    path('', views.post, name='post'),
    path('comment/<str:post_id>', views.comment, name='comment'),
    path('create-comment/<str:post_id>',
         views.createComment, name='create-comment'),
    path('edit-comment/<str:comment_id>',
         views.editComment, name='edit-comment'),
    path('delete-comment/<str:comment_id>',
         views.deleteComment, name='delete-comment'),
    path('reply/<str:comment_id>', views.reply, name='reply'),
    path('create-reply/<str:comment_id>',
         views.createReply, name='create-reply'),
    path('edit-reply/<str:reply_id>', views.editReply, name='edit-reply'),
    path('delete-reply/<str:reply_id>', views.deleteReply, name='delete-reply'),
]
