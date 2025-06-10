from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from django.db.models import Count
from .models import *
from .serializers import PostListSerializer,PostDetailSerializer, BookmarkSerializer
from django.db.models import F, Prefetch
from django.shortcuts import get_object_or_404
from .filters import PostFilter
# Create your views here.



@api_view(['GET'])
def posts_list(request):

    posts = Post.objects.filter(is_published=True).select_related(
    'author', 'category'
    ).only(
        'id', 'title', 'slug', 'excerpt', 'reading_time',
        'meta_title', 'meta_description', 'published_at',
        'author__first_name', 'author__last_name',
        'category__name',
    )


    paginator = LimitOffsetPagination()
    result_page = paginator.paginate_queryset(posts, request)  

    serializer = PostListSerializer(result_page, many=True)  
    return paginator.get_paginated_response(serializer.data)



@api_view(['GET'])
def post_detail(request, slug):
    post = get_object_or_404(
        Post.objects.select_related('author', 'category').prefetch_related(
            'topics',
            Prefetch(
                'category__posts',
                queryset=Post.objects.filter(status='published', is_published=True)
                             .select_related('author', 'category')
                             .prefetch_related('topics')
                             .order_by(F('published_at').desc(nulls_last=True))
            )
        ),
        slug=slug,
        is_published=True
    )
    serializer = PostDetailSerializer(post)
    return Response(serializer.data, status=status.HTTP_200_OK)





def get_user_bookmark_or_404(bookmark_id, user):
    try:
        return Bookmark.objects.get(id=bookmark_id, user=user)
    except Bookmark.DoesNotExist:
        return None


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_bookmarks(request, post_id=None):
    user = request.user

    if request.method == 'GET':
        if post_id:
            bookmarks = Bookmark.objects.filter(user=user, post_id=post_id).select_related('post')
        else:
            bookmarks = Bookmark.objects.filter(user=user).select_related('post')

        serializer = BookmarkSerializer(bookmarks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = request.data.copy()
        if post_id:
            data['post'] = post_id  # Ensure post_id is used in serializer data

        serializer = BookmarkSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            bookmark = serializer.save()
            return Response(BookmarkSerializer(bookmark).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def manage_bookmark(request, bookmark_id):
    user = request.user
    bookmark = get_user_bookmark_or_404(bookmark_id, user)
    if not bookmark:
        return Response({'detail': 'Bookmark not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BookmarkSerializer(bookmark)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        bookmark.delete()
        return Response({'detail': 'Bookmark deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)























# Fetch a single post with all details
# @api_view(['GET'])
# @vary_on_cookie
# @vary_on_headers("Authorization") 
# @cache_page(600)
# def fetch_single_post(request, post_id):
#     post = get_object_or_404(
#         Post.objects.prefetch_related('tags', 'comments').select_related('author', 'category'), id=post_id, status='published')
#     serializer = PostDetailSerializer(post)
#     return Response(serializer.data)




# # Create a new comment for a post
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def create_comment(request, post_id):
#     post = get_object_or_404(Post, id=post_id)

#     data = request.data.copy()
#     data['post'] = post.id  

#     serializer = CommentSerializer(data=data, context={'request': request})
#     if serializer.is_valid(raise_exception=True):
#         serializer.save(user=request.user, post=post) 
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# @api_view(['PATCH'])  
# @permission_classes([IsAuthenticated])
# def update_comment(request, comment_id):
#     comment = get_object_or_404(Comment, id=comment_id)

#     # Ensure the user can only update their own comments
#     if comment.user != request.user:
#         return Response({'detail': 'You can only edit your own comments.'}, status=status.HTTP_403_FORBIDDEN)

#     serializer = CommentSerializer(comment, data=request.data, context={'request': request}, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def delete_comment(request, comment_id):
#     comment = get_object_or_404(Comment, id=comment_id)
#     comment.delete()
#     return Response({"detail": "Comment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)