from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User #追加

class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    #tags = models.ManyToManyField(Tag, blank=True)
    created_date = models.DateTimeField(auto_now_add=True) #default=timezone.now
    published_date = models.DateTimeField(blank=True, null=True)
    views = models.PositiveIntegerField(default=0) #閲覧数
    
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']
    
    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

class ContentImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    content_image = models.ImageField(upload_to='post_content_images/')
