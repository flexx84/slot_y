from django.contrib import admin
from .models import Slot, Notice


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ['keyword', 'url', 'user', 'start_date', 'end_date', 'is_expired', 'days_remaining']
    list_filter = ['user', 'start_date', 'end_date', 'created_at']
    search_fields = ['keyword', 'url', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('user', 'keyword', 'url')
        }),
        ('기간 설정', {
            'fields': ('start_date', 'end_date')
        }),
        ('시스템 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at', 'user']
    search_fields = ['title', 'content', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('공지사항 정보', {
            'fields': ('title', 'content', 'user', 'is_active')
        }),
        ('시스템 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    ) 