from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth import get_user_model
from markdownx.models import MarkdownxField

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)

    class Meta:
        indexes = [models.Index(fields=['name'])]

    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)

    class Meta:
        indexes = [models.Index(fields=['name'])]

    def __str__(self):
        return self.name


STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
)


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, db_index=True)
    content = MarkdownxField()

    excerpt = models.TextField(max_length=500, blank=True)
    reading_time = models.PositiveIntegerField(null=True, blank=True, help_text="Estimated reading time in minutes")
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts', db_index=True)
    topics = models.ManyToManyField(Topic, related_name='posts')

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', db_index=True)
    is_published = models.BooleanField(default=False, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
            models.Index(fields=['is_published']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.title

    def get_author_full_name(self):
        return f"{self.author.first_name} {self.author.last_name}"







class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='bookmarked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        indexes = [
            models.Index(fields=['user', 'post']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} bookmarked {self.post.title}"





   

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    body = models.TextField()
    active = models.BooleanField(default=True, db_index=True)  
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  

    def __str__(self):
        return f'Comment by {self.user.email} on {self.post}'
    
    def get_user_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
