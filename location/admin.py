from django.contrib import admin
from location.models import Location, Status, Activity, ColorModelField, Relation, Picture, Skill, Province, Region, Profile, CredentialsModel
from location.tasks import sync_table_task
from location.widgets import JSColorColorPicker
from django.contrib.admin import SimpleListFilter
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

import os.path

class IsEditor(SimpleListFilter):
    title = _('Editor')
    parameter_name = 'editor'
    
    def lookups(self, request, model_admin):
        return (
            ('yes', _('Yes')),
            ('no', _('No')),
        )
        
    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(editor=True)
            
        if self.value() == 'no':
            return queryset.filter(editor=False)

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
    actions = ('sync_table',)
    
    def sync_table(self, request, queryset):
        import tempfile
        content = ''
        for location in queryset:
            content += "%d\t%.6f,%.6f\t%d\t%d\n" % (location.id, location.latitude, 
                location.longitude, location.status.id, location.organization)

        with tempfile.NamedTemporaryFile(suffix='.bin', delete=False, dir=os.path.join(os.path.dirname(__file__), '..', 'tmp')) as temp:
            temp.write(content)
            temp.flush()
            temp.close()
            sync_table_task.apply_async((temp.name,), countdown=0)
        
    sync_table.short_description = "Sync table"
    
class ProfileAdmin(admin.ModelAdmin):
    list_filter = (IsEditor,)
    search_fields = ('user__email', 'user__first_name', 'user__last_name',)
    
class PictureAdmin(admin.ModelAdmin):
    list_display = ('slug', 'admin_image',)
    
class CredentialsAdmin(admin.ModelAdmin):
    pass

admin.site.register(CredentialsModel, CredentialsAdmin)    
admin.site.register(Location, LocationAdmin)
admin.site.register(Status)
admin.site.register(Relation)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(Skill)
admin.site.register(Province)
admin.site.register(Region)
admin.site.register(Profile, ProfileAdmin)