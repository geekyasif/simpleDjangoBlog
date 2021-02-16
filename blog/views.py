from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Post , Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm, ContactForm
from django.core.mail import send_mail


# Create your views here.
def home(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 10) #10 post in each page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)    
    context = {
         'page_obj' : page_obj
        }
    return render(request, "home/home.html", context)


def post_details(request, year, month, day, post):
    post = get_object_or_404(Post,
                            publish__year=year,
                            publish__month=month,
                            publish__day= day,
                            slug=post,
                            status='published',
                            )
    #list of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data = request.POST)
        if comment_form.is_valid():
            #create a comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)

            #assign the current post to the comment
            new_comment.post = post
            #save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    context = {
        'post' : post,
        'comment_form' : comment_form,
        'new_comment' : new_comment,
        'comments' : comments,
    }                        
    return render(request, 'blog/post_details.html',context)                    

def post_share(request, post_id):
    #retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        #form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():

            #form fields passed validation
            cd = form.cleaned_data
            #.... send email
            
            post_url = request.build_absolute_uri(post.get_absolute_url())
            
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title,post_url, cd['name'], cd['comments'])
            
            send_mail(subject, message, 'mdasif08737@gmail.com',[cd['to']])
            send = True
    else:
        form = EmailPostForm()

    context= {
        'post':post,
        'form':form,
        'sent': sent,
    }    
    return render(request, 'blog/post_share.html',context)                    


def contact(request):
    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            new_contact = contact_form.save(commit=False)
            new_contact.save()
            return redirect('contact')       
    else:
        contact_form = ContactForm()
    context = {
        'contact_form' : contact_form
    }
    return render(request, 'home/contact.html', context)
    