from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import Post, Comment, Reply, PostImage, PostParagraph
from Profile.models import UserProfile
from .forms import CommentForm, ReplyForm
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def post(request):
    user_profile = UserProfile.objects.get(user=request.user)
    posts = Post.objects.all()
    paginator = Paginator(posts, 4)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'user_profile': user_profile}
    return render(request, 'Blog/post.html', context)


@login_required(login_url='login')
def comment(request, post_id):
    user_profile = UserProfile.objects.get(user=request.user)
    post = Post.objects.get(id=post_id)
    comments = post.comment_set.all()
    post_images = PostImage.objects.filter(post=post)
    post_paragraphs = PostParagraph.objects.filter(post=post)

    content_list = []
    for post_image in post_images:
        content_list.append([post_image.image_url, post_image.order])

    for post_paragraph in post_paragraphs:
        content_list.append([post_paragraph.paragraph, post_paragraph.order])

    content_list.sort(key=lambda content: content[1])
    contents = list(map(lambda content: content[0], content_list))

    context = {'post': post, 'contents': contents,
               'comments': comments,
               'user_profile': user_profile}
    return render(request, 'Blog/comment.html', context)


@login_required(login_url='login')
def createComment(request, post_id):
    user_profile = UserProfile.objects.get(user=request.user)
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comm = form.data['comment']
            user = request.user
            new_comment = Comment.objects.create(
                user=user, post=post, comment=comm)
            return redirect('comment', post_id)
    else:
        form = CommentForm()

    context = {'post': post, 'CommentForm': form, 'user_profile': user_profile}
    return render(request, 'Blog/comment-form.html', context)


@login_required(login_url='login')
def editComment(request, comment_id):
    user_profile = UserProfile.objects.get(user=request.user)
    comment = Comment.objects.get(id=comment_id)
    post_id = comment.post.id
    post = Post.objects.get(id=post_id)
    form = CommentForm(initial={'comment': comment.comment})
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            edited_comm = form.data['comment']
            comment.comment = edited_comm
            comment.save()
            return redirect('comment', post_id)

    context = {'post': post, 'commentForm': form, 'user_profile': user_profile}
    return render(request, 'Blog/comment-form.html', context)


@login_required(login_url='login')
def deleteComment(request, comment_id):
    user_profile = UserProfile.objects.get(user=request.user)
    comment = Comment.objects.get(id=comment_id)
    post_id = comment.post.id
    if request.method == 'POST':
        comment.delete()
        return redirect('comment', post_id)

    context = {'comment': comment.comment,
               'post_id': post_id, 'user_profile': user_profile}
    return render(request, 'Blog/delete-comment.html', context)


@login_required(login_url='login')
def reply(request, comment_id):
    user_profile = UserProfile.objects.get(user=request.user)
    comment = Comment.objects.get(id=comment_id)
    replies = comment.reply_set.all()
    context = {'comment': comment, 'replies': replies,
               'user_profile': user_profile}
    return render(request, 'Blog/reply.html', context)


@login_required(login_url='login')
def createReply(request, comment_id):
    user_profile = UserProfile.objects.get(user=request.user)
    comment = Comment.objects.get(id=comment_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.data['reply']
            user = request.user
            new_reply = Reply.objects.create(
                comment=comment, user=user, reply=reply)
            return redirect('reply', comment.id)
    else:
        form = ReplyForm()

    context = {'comment': comment, 'replyForm': form,
               'user_profile': user_profile}
    return render(request, 'Blog/create-reply.html', context)


@login_required(login_url='login')
def editReply(request, reply_id):
    user_profile = UserProfile.objects.get(user=request.user)
    reply = Reply.objects.get(id=reply_id)
    comment_id = reply.comment.id
    comment = Comment.objects.get(id=comment_id)
    form = ReplyForm(initial={'reply': reply.reply})
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            edited_reply = form.data['reply']
            reply.reply = edited_reply
            reply.save()
            return redirect('reply', comment_id)

    context = {'comment': comment, 'replyForm': form, 'user_profile': user_profile}
    return render(request, 'Blog/create-reply.html', context)


@login_required(login_url='login')
def deleteReply(request, reply_id):
    user_profile = UserProfile.objects.get(user=request.user)
    reply = Reply.objects.get(id=reply_id)
    comment_id = reply.comment.id

    if request.method == 'POST':
        reply.delete()
        return redirect('reply', comment_id)

    context = {'reply': reply.reply,
               'comment_id': comment_id, 'user_profile': user_profile}
    return render(request, 'Blog/delete-reply.html', context)
