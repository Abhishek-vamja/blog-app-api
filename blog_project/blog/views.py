"""
View for blog API.
"""

from rest_framework import viewsets , mixins , status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView

from core.models import *
from blog.serializers import *


class BlogViewSet(viewsets.ModelViewSet):
    """View for manage blog APIs."""

    serializer_class = BlogDetailSerializer
    queryset = Blog.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _params_to_ints(self,qs):
        """Convert a list of string to integers."""
        return [int(str_id) for str_id in qs.split(',')] 
    
    def get_queryset(self):
        """Retrieve blogs for authenticated user."""
        tags = self.request.query_params.get('tags')
        queryset = self.queryset

        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)

        return queryset.filter(user=self.request.user).order_by('-id').distinct()
    
    def get_serializer_class(self):
        """Return serializer class from request."""
        if self.action == 'list':
            return BlogSerializer
        
        return self.serializer_class
    
    def perform_create(self,serializer):
        """Create new blog."""
        return serializer.save(user=self.request.user)


class TagViewSet(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,         
    mixins.ListModelMixin, 
    viewsets.GenericViewSet):
    """Manage tags in the database."""
    
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset for authenticated user."""
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only',0))
            )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(blog__isnull=False)
        
        return queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()

class BlogAPIView(viewsets.ReadOnlyModelViewSet):
    """List all blog for authenticated user."""
    queryset =  Blog.objects.all()
    serializer_class = BlogViewSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]