from django.contrib import admin

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserCreationForm
from .models import MyUser

# Register your models here.

class UserAdmin(BaseUserAdmin):
	add_form = UserCreationForm

	list_display = ('full_name', 'email', 'username', 'is_admin', 'id')
	list_filter = ('is_admin',)

	fieldsets = (
			(None, {'fields': ('email', 'username', 'full_name','password')}),
			('Permissions', {'fields': ('is_admin',)}),
			('History', {'fields': ('search_history',)}),
		)
	search_fields = ('username','email', 'full_name', 'id')
	ordering = ('username','email','full_name')

	filter_horizontal = ()


admin.site.register(MyUser, UserAdmin)


admin.site.unregister(Group)