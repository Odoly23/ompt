from django.contrib import admin

from .models import MemberProfile


@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "member_number", "municipality", "status", "created_at")
    list_filter = ("status", "municipality")
    search_fields = ("full_name", "phone", "member_number", "user__email")
