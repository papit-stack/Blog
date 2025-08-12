from django.contrib import admin
from .models import Category,Blog
# Register your models here.
admin.site.register(Category)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('blog_title', 'author', 'created_at', 'updated_at','is_published')
    prepopulated_fields = {'slug': ('blog_title',)}
admin.site.register(Blog,BlogAdmin)