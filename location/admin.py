from django.contrib import admin
from location.models import Location, Status, Activity, ColorModelField, Relation, Picture, Skill
from location.widgets import JSColorColorPicker

class ActivityAdmin(admin.ModelAdmin):
    formfield_overrides = {
        ColorModelField: {'widget': JSColorColorPicker }
    }
        
    list_display = ('name', 'priority',)
    
class LocationAdmin(admin.ModelAdmin):
    list_display = ('place_name', 'approved',)
    
admin.site.register(Location, LocationAdmin)
admin.site.register(Status)
admin.site.register(Relation)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Picture)
admin.site.register(Skill)