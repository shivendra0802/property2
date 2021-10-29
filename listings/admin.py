from django.contrib import admin

from .models import Listing, ListingPhoto, Multiple, Danger

class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_published', 'price', 'list_date', 'realtor')
    list_display_links = ('id', 'title')
    list_filter = ('realtor',)
    list_editable = ('is_published',)
    search_fields = ('title', 'is_published', 'price', 'list_date', 'realtor', 'city', 'state', 'zipcode')

admin.site.register(Listing, ListingAdmin)
admin.site.register(Danger)
admin.site.register(Multiple)
admin.site.register(ListingPhoto)