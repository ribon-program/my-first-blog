from django.contrib import admin
from .models import Post, Comment, ContentImage, Category

class CategoryAdmin(admin.ModelAdmin):
    list_display=('id','title')
    list_display_links=('id','title')

class CommentAdmin(admin.ModelAdmin):
    list_display=('id','author','user','post')
    list_display_links=('id','author')


class ContentImageInline(admin.TabularInline):
    model = ContentImage
    extra = 1

class PostAdmin(admin.ModelAdmin):
    list_display=('id','title','user')
    list_display_links=('id','title')
    inlines = [
        ContentImageInline,
    ]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
#admin.site.register(Tag)
