from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail


# Create your views here.
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "post/detail.html"
def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) # 3 posts in each page 
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
        
    return render(request,'post/list.html', {'posts': posts})

def  post_detail(request,year,month,day,post):
    post =get_object_or_404(Post, slug=post,
                            status='published',
                            publish__year = year,
                            publish__month=month,
                            publish__day = day)
    return render(request, 'post/detail.html', {'post':post})
# handling forms in views
def post_share(request, post_id):
    # retrieve post by id 
    post = get_object_or_404(Post, id=post_id, status ='published')
    sent = False 
    if request.method == "POST":
        # form was submitted 
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # forms fields passed validation 
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url()) # helps you include link to the post in the email 
            subject = f"{cd['name']} recommends you read"\
                f" {post.title}"
            message = f"Read{post.title} at {post_url}\n\n"\
                f"{cd['name']}\'s comments:{cd['comments']}"
            # send email
            send_mail(subject,message, 'ngagadancan2003@gmail.com', {cd['to']})
            
            sent = True
        else:
            form = EmailPostForm()
        return render(request, 'post/share.html', { 'post': post, 'form': form , sent: sent })