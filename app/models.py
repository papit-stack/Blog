from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.text import slugify

# Create your models here.
class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_id=models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
class Category(models.Model):
    category_title=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.category_title

class Blog(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    slug=models.SlugField(unique=True, blank=True)
    blog_title=models.CharField(max_length=100)
    blog_short_description=models.TextField(max_length=700)
    blog_description=models.TextField(max_length=2000)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_published=models.BooleanField(default=False)
    image=models.ImageField(upload_to='blog_images/',blank=True,null=True)
    def save(self, *args, **kwargs):
        self.is_published = self.status == 'published'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.blog_title
