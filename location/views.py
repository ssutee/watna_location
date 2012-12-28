from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.contrib.auth import authenticate, logout, login
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from django.db.models import Count

from location.forms import MapForm, SearchMapForm, LocationForm, RegistrationForm, UserForm
from location.models import Location

from gmapi import maps
from emailusernames.utils import create_user
from django_countries.fields import Country

def create_info_content(location):
    return '<div id="%d" style="height:70px; width:300px;"><h4>%s, %s</h4>%s</div>' % (
        location.id,
        location.place_name, location.city,
        ', '.join(map(lambda x:x.name,location.activities.all())))

def map_page(request):
    request.session['next'] = '/'
    gmap = maps.Map(
        opts = {
            'center': maps.LatLng(14.01012, 100.82302),
            'mapTypeId': maps.MapTypeId.ROADMAP,
            'zoom': 8,
            'mapTypeControlOptions': {
                 'style': maps.MapTypeControlStyle.DROPDOWN_MENU
            },
            'navigationControlOptions': {
                'style': maps.NavigationControlStyle.ANDROID
            }            
        }
    )
    
    for index, location in enumerate(Location.objects.all()):
        color = 'FF776B'
        
        if location.activities.count() > 0:            
            activity = location.activities.order_by('priority').all()[0]
            color = activity.color.strip('#')
            
        marker = maps.Marker(opts = {
                'color': color,
                'map': gmap,
                'position': maps.LatLng(location.latitude, location.longitude),
            })
        maps.event.addListener(marker, 'mouseover', 'm_listener.markerOver')
        maps.event.addListener(marker, 'mouseout', 'm_listener.markerOut')
        maps.event.addListener(marker, 'click', 'm_listener.markerClick')
        info = maps.InfoWindow({
            'content': create_info_content(location),
            'disableAutoPan': True
        })
        info.open(gmap, marker)
        
    nav_list = []    
    for value in Location.objects.values('country').annotate(total=Count('country')):
        nav_list.append({'type':'header', 'value': unicode(Country(code=value['country']).name)})        
        for location in Location.objects.filter(country=value['country']).order_by('city', 'place_name').all():
            nav_list.append({'type':'item', 'value': location})    
            
    context = {'form': MapForm(initial={'gmap': gmap}), 
        'active_menu':0, 'nav_list': nav_list }
    if 'message' in request.flash and request.flash['message']:
        context['alert_type'], context['alert_message'] = request.flash['message']
        
    return render(request, 'map_page.html', context)

def create_search_map_form(lat, lng):
    gmap = maps.Map(
        opts = {
            'center': maps.LatLng(lat, lng),
            'mapTypeId': maps.MapTypeId.ROADMAP,
            'zoom': 6,
            'mapTypeControlOptions': {
                'style': maps.MapTypeControlStyle.DROPDOWN_MENU
            },
            'navigationControlOptions': {
                'style': maps.NavigationControlStyle.SMALL
            }
        }
    )
    
    marker = maps.Marker(opts = {
        'map': gmap,
        'position': maps.LatLng(lat, lng),
        'draggable': True,
    })
    
    maps.event.addListener(marker, 'dragend', 'm_listener.markerDragEnd')
    maps.event.addListener(gmap, 'idle', 'm_listener.mapIdle')
        
    return SearchMapForm(initial={'gmap': gmap})
    
@login_required
def locations_page(request):
    request.session['next'] = '/places'
    context = {'active_menu':1, 'locations': Location.objects.filter(user=request.user).all()}
    if 'message' in request.flash and request.flash['message']:
        context['alert_type'], context['alert_message'] = request.flash['message']
    return render(request, 'locations_page.html', context)

@login_required
def edit_user_page(request):
    if request.method == 'POST':
        form = UserForm(request.POST);
        if form.is_valid():
            password = form.cleaned_data['new_password1']
            if len(password) > 0:
                request.user.set_password(password)
            request.user.first_name = form.cleaned_data['first_name'];
            request.user.last_name = form.cleaned_data['last_name'];
            request.user.save()            
            request.flash['message'] = ('alert-success', _('User updated successfully'))
            return HttpResponseRedirect(request.session.get('next', '/'))                  
    else:        
        form = UserForm(initial={
            'email':request.user.email,
            'first_name':request.user.first_name,
            'last_name':request.user.last_name})

    context = {'form': form}
    return render(request, 'edit_user_page.html', context)


@login_required
def edit_location_page(request, pk):
    location = Location.objects.get(pk=int(pk))   
    lat, lng = location.latitude, location.longitude     
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            location = form.save()
            location.user = request.user;
            location.save()
            request.flash['message'] = ('alert-success', _('Place updated successfully'))
            return HttpResponseRedirect('/places')
        else:
            try:
                lat = float(form.data.get('latitude'))
                lng = float(form.data.get('longitude'))                
            except ValueError,e:
                pass
    else:                
        form = LocationForm(instance=location)
    
    context = {'form': form, 'map_form': create_search_map_form(lat, lng)}
    return render(request, 'edit_location_page.html', context)
    
@login_required
def add_location_page(request):
    lat, lng = 15.87003, 100.99254 # Thailand     
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            location = form.save(commit=False)
            location.user = request.user;
            location.save()
            request.flash['message'] = ('alert-success', _('New place added successfully'))
            return HttpResponseRedirect('/places')
        else:
            try:
                lat = float(form.data.get('latitude'))
                lng = float(form.data.get('longitude'))                
            except ValueError,e:
                pass
    else:       
        form = LocationForm()
    
    context = {'form': form, 'map_form': create_search_map_form(lat, lng)}
    return render(request, 'add_location_page.html', context)

@csrf_exempt
@login_required
def delete_location_page(request):    
    Location.objects.filter(pk=int(request.POST.get('pk'))).delete()
    return HttpResponse(simplejson.dumps(0), mimetype="application/json")
    
@csrf_exempt
def find_location_by_id_page(request):    
    location = Location.objects.get(pk=int(request.POST.get('id', 1)))    

    data = {
        'place_name': location.place_name,
        'email': location.user.email,
        'first_name': location.user.first_name,
        'last_name': location.user.last_name,
        'address': location.address,
        'city': location.city,
        'info': unicode(_('Organization')) if location.organization else unicode(_('Person')),
        'status': location.status.name if location.status else '-',
        'additional_info': location.additional_info if location.additional_info and len(location.additional_info.strip()) > 0 else '-',
        'country': unicode(location.country.name),
        'phone_number': location.phone_number,
        'activities': ', '.join(map(lambda x:x.name,location.activities.all())),
    }
        
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    
def logout_page(request):
    logout(request)
    request.flash['message'] = ('alert-success', _('Logout successfully'))
    return HttpResponseRedirect('/')

def login_page(request):
    user = authenticate(email=request.POST.get('email'), password=request.POST.get('password'))
    if user:
        login(request, user)
        request.flash['message'] = ('alert-success', _('Login successfully'))
    else:
        request.flash['message'] = ('alert-error', _('Invalid email or password'))
    return HttpResponseRedirect('/')
    
def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():            
            user = create_user(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'])
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            logout(request)
            login(request, authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password1']))
            request.flash['message'] = ('alert-success', _('Registration completed successfully'))
            return HttpResponseRedirect('/')
    else:
        form = RegistrationForm()

    context = {'form': form, 'active_menu':1}
    return render(request, 'registration/register.html', context)    
    