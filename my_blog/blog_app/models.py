from django.db import models
from django.utils import timezone 
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
# defining our post model
class PublishManager(models.Manager):
    def get_queryset(self):
        return super(PublishManager, self).get_queryset().filter(status='published')
    
    
class Post(models.Model):
    STATUS_CHOICES= (
        ('draft', 'draft'),
        ('published', 'published'),
    )
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date = "publish")
    author = models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    
    objects = models.Manager()
    published = PublishManager()
    
    def get_absolute_url(self):
        return reverse('blog_app:post_detail', args =[self.publish.year, self.publish.month, self.publish.day, self.slug])
    
    class Meta:
        ordering = ('-publish',)
    def __str__(self):
        return self.title
    
    
