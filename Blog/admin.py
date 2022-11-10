from django.contrib import admin
from .models import Post, Comment, Reply, PostParagraph, PostImage


class PostImageInline(admin.StackedInline):
    model = PostImage
    fk_name = 'post'
    extra = 1


class PostParagraphInline(admin.StackedInline):
    model = PostParagraph
    fk_name = 'post'
    extra = 1


class PostImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'image')


class PostParagraphAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'paragraph')


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'headline', 'datetime_posted')
    inlines = [PostImageInline, PostParagraphInline]


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'post_id', 'comment', 'datetime_posted')


class ReplyAdmin(admin.ModelAdmin):
    list_display = ('comment_id', 'user_id', 'reply', 'datetime_replied')


admin.site.register(Post, PostAdmin)
admin.site.register(PostImage, PostImageAdmin)
admin.site.register(PostParagraph, PostParagraphAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reply, ReplyAdmin)
