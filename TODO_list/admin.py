from django.contrib import admin
from .models import *

# Register your models here.


# class Custom_User_inline(admin.TabularInline):
#     model = Custom_User.group.through


# class Custom_Group_admin(admin.ModelAdmin):
#     model = Custom_Group
#     inlines = [
#         Custom_User_inline,
#     ]
#     list_display = ('name', 'description', 'show_users',)

#     def show_users(self, obj):
#         return "\n".join([a.user.username for a in obj.group.all()])


class Access_admin(admin.ModelAdmin):
    search_fields = ['group__name', 'user__username']
    list_filter = ('is_staff', 'is_admin', 'is_developper')
    list_display = ('group', 'user', 'is_staff', 'is_admin', 'is_developper')


admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Status)
admin.site.register(Access, Access_admin)
admin.site.register(Custom_Group)
