from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Spending)
admin.site.register(Category)
admin.site.register(ExtendedUser)
admin.site.register(InviteToGroup)