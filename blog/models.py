from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import	reverse

# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset()\
            .filter(status = 'published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length = 10,
                            choices = STATUS_CHOICES, default = 'draft')
    objects = models.Manager()
    published = PublishedManager()

    def get_absolute_url(self):
        return reverse("post_details",
                    args=[self.publish.year,
                          self.publish.month,
                          self.publish.day,
                          self.slug])

    class Meta:
        ordering = ('-publish',)
        def __str__ (self):
            return self.title 

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comments by {} on {}'.format(self.name, self.post)    

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    message = models.TextField()
    date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("date",)

    def __str__(self):
        return "Message by {self.name} and email is {self.email}"    