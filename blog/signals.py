from django.core.cache import cache
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils import timezone
from django.utils.html import strip_tags
from .models import Post
import markdown2

@receiver(pre_save, sender=Post)
def set_post_fields(sender, instance, **kwargs):
    # Slug generation
    if not instance.slug:
        base_slug = slugify(instance.title)
        slug = base_slug
        num = 1
        while Post.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
            slug = f"{base_slug}-{num}"
            num += 1
        instance.slug = slug

    # Render Markdown to HTML and strip tags to get plain text
    html_content = markdown2.markdown(instance.content or "")
    plain_text = strip_tags(html_content).replace('\n', ' ').strip()

    # Excerpt generation
    if not instance.excerpt:
        instance.excerpt = ' '.join(plain_text.split()[:30]) + '...'

    # Reading time estimation
    if not instance.reading_time:
        word_count = len(plain_text.split())
        instance.reading_time = max(1, word_count // 200)

    # Auto-set published_at
    if instance.is_published and not instance.published_at:
        instance.published_at = timezone.now()

    # Meta title generation
    if not instance.meta_title:
        instance.meta_title = instance.title[:57] + '...' if len(instance.title) > 60 else instance.title

    # Meta description generation
    if not instance.meta_description:
        instance.meta_description = plain_text[:157] + '...' if len(plain_text) > 160 else plain_text


@receiver(post_save, sender=Post)
@receiver(post_delete, sender=Post)
def clear_post_cache(sender, **kwargs):
    cache.clear()
