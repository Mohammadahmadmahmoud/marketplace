from django.contrib import admin
from .models import *

# Register your models here.
class AdsAdmin(admin.ModelAdmin):
    list_display = ['image','title', 'description','category','name','approved']
    list_editable = ['approved']
    
admin.site.register(CategoryAds)
# admin.site.register(SilverPart)
# admin.site.register(FreePart)
admin.site.register(Ads,AdsAdmin)
fields = ( 'image_tag', )
readonly_fields = ('image_tag',)

admin.site.site_header  = " AU79 Code Admin Panel "

admin.site.site_title  = " AU79Cod"