from django.contrib import admin
from location.models import Location, Status, Activity, ColorModelField
from location.widgets import JSColorColorPicker

class ActivityAdmin(admin.ModelAdmin):
    formfield_overrides = {
        ColorModelField: {'widget': JSColorColorPicker }
    }
        
    list_display = ('name', 'priority',)
    
admin.site.register(Location)
admin.site.register(Status)
admin.site.register(Activity, ActivityAdmin)