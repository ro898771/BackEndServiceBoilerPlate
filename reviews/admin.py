from django.contrib import admin
from .models import HandshakeToken, Review


@admin.register(HandshakeToken)
class HandshakeTokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'used', 'is_valid', 'created_at')
    list_filter = ('used',)
    readonly_fields = ('token', 'created_at')
    ordering = ('-created_at',)

    def is_valid(self, obj):
        return obj.is_valid()
    is_valid.boolean = True
    is_valid.short_description = 'Valid'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'rating', 'short_comment', 'created_at', 'updated_at')
    list_filter = ('rating',)
    search_fields = ('comment',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    def short_comment(self, obj):
        return obj.comment[:60] + '...' if len(obj.comment) > 60 else obj.comment
    short_comment.short_description = 'Comment'
