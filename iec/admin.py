from django.contrib import admin
from .models import Iec,Book




admin.site.site_header = 'IEC Management System '

class IecAdmin(admin.ModelAdmin):
    list_display = ('title', 'thematic', 'copies', 'issued')
    list_filter = ('issued', 'thematic','user')
    search_fields = ('title__title', 'description','user')
    list_per_page = 6

admin.site.register(Iec, IecAdmin)

admin.site.register(Book)