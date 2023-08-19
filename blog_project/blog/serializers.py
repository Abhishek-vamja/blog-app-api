"""
Serializer for blog API.
"""

from rest_framework import serializers

from core.models import Blog , Tag


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag."""

    class Meta:
        model = Tag
        fields = ['id','name']
        read_only_fields = ['id']


class BlogSerializer(serializers.ModelSerializer):
    """Serializer for blog."""

    tags = TagSerializer(many=True,required=False)

    class Meta:
        model = Blog
        fields = ['id','title','link','tags']
        read_only_fields = ['id']

    def _get_or_create_tags(self,tags,recipe):
        """Handle getting or creating tags as needed."""
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj,created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            recipe.tags.add(tag_obj)

    def create(self, validated_data):
        """Create a recipe."""
        tags = validated_data.pop('tags', [])    
        blog = Blog.objects.create(**validated_data)
        self._get_or_create_tags(tags,blog)

        return blog
    
    def update(self,instance,validated_data):
        """Update recipe."""
        tags = validated_data.pop('tags',None)

        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags,instance) 
        
        for attr,value in validated_data.items():
            setattr(instance,attr,value)
        
        instance.save()
        return instance

class BlogDetailSerializer(BlogSerializer):
    """Serializer for recipe detail view."""

    class Meta(BlogSerializer.Meta):
        fields = BlogSerializer.Meta.fields + ['description','image']

class TagViewSerializer(serializers.ModelSerializer):
    """Serializer for list all objects."""

    class Meta:
        model = Tag
        fields = ['name']

class BlogViewSerializer(serializers.ModelSerializer):
    """Serializer for list all objects."""

    tags = TagViewSerializer(many=True,required=False)

    class Meta:
        model = Blog
        fields = ['title','description','link','tags','image','created_at']