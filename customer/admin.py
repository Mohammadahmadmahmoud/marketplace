from django.contrib import admin
from .models import Customer,User,Role,SecurityQuestion

admin.site.register(Customer)
admin.site.register(User)
admin.site.register(Role)
admin.site.register(SecurityQuestion)
