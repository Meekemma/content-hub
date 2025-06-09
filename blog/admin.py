from django.contrib import admin
from .models import Category, Topic, Post, Comment,Bookmark


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'author', 'category', 'status', 'is_published', 'published_at', 'created_at'
    )
    list_filter = ('status', 'is_published', 'category', 'topics', 'created_at', 'published_at')
    search_fields = ('title', 'content', 'meta_title', 'meta_description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('topics',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'category', 'topics', 'content', 'excerpt')
        }),
        ('Meta Info', {
            'fields': ('meta_title', 'meta_description', 'reading_time')
        }),
        ('Publishing Options', {
            'fields': ('status', 'is_published', 'published_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )








@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    search_fields = ('user__username', 'post__title')
    list_filter = ('created_at',)
    ordering = ('-created_at',)




@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'active', 'created_at')  
    list_filter = ('active', 'created_at', 'post')
    search_fields = ('body', 'user__username')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
