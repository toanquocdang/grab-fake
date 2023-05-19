from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'Accounts'

class CustomUserAdmin(UserAdmin):
    inlines = (AccountInline, )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(OrderPlaced)
admin.site.register(Rider)
admin.site.register(Merchants)
admin.site.register(RiderSavedOrders)


