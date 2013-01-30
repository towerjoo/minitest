from django.contrib import admin
from account.models import Account

class AccountAdmin(admin.ModelAdmin):
    list_display = ("get_username", "get_email", "question", "answer", "get_last_login")
    #list_filter = ("get_last_login", )
    #search_fields = ("get_username", )

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = "username"

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = "email"

    def get_last_login(self, obj):
        return obj.user.last_login
    get_last_login.short_description = "last login"



admin.site.register(Account, AccountAdmin)
