from django.contrib import admin

# Register your models here.
from account.models import Account, Profile,Card

# Register your models here.
class AccountAdmin(admin.ModelAdmin):
	list_display=('email', 'username', 'first_name', 'last_name','date_joined', 'last_login', 'is_active')
	list_display_links=('email','username',)
	readonly_fields=('last_login','date_joined', 'password')
	list_filter=()
	fieldsets=()

class ProfileAdmin(admin.ModelAdmin):
	list_display=('email','first_name', 'last_name', 'phone',  'age', 'gender', 'city', 'zip', 'country'
			   )

class CardAdmin(admin.ModelAdmin):
	list_display=('owner', 'cvv', 'month', 'year',  'bal' )
	search_fields=('owner', 'cvv', 'month', 'year')
	

admin.site.register(Account, AccountAdmin)
admin.site.register(Profile,  ProfileAdmin)
admin.site.register(Card,  CardAdmin)
