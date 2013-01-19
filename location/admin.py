from django.contrib import admin
from location.models import Location, Status, Activity, ColorModelField, Relation, Picture, Skill, Province, Region
from location.widgets import JSColorColorPicker
from django.contrib.admin import SimpleListFilter
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

class InvalidCity(SimpleListFilter):
    title = _('invalid city')
    parameter_name = 'invalid_city'
    
    def lookups(self, request, model_admin):
        return (
            ('yes', _('Yes')),
            ('no', _('No')),
        )
        
    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(~Q(city__in=map(lambda x:x.name, Province.objects.all())), country='TH')
            
        if self.value() == 'no':
            return queryset.filter(city__in=map(lambda x:x.name, Province.objects.all()), country='TH')

class ActivityAdmin(admin.ModelAdmin):
    formfield_overrides = {
        ColorModelField: {'widget': JSColorColorPicker }
    }
        
    list_display = ('name', 'priority',)
    
class LocationAdmin(admin.ModelAdmin):
    list_display = ('place_name', 'city', 'additional_info', 'user_name', 'user_skills',)
    list_filter = (InvalidCity,)
    search_fields = ('place_name', 'additional_info', 'city', 'country', 'address',)
    
class PictureAdmin(admin.ModelAdmin):
    list_display = ('slug', 'admin_image',)
    
admin.site.register(Location, LocationAdmin)
admin.site.register(Status)
admin.site.register(Relation)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(Skill)
admin.site.register(Province)
admin.site.register(Region)