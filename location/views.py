from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.contrib.auth import authenticate, logout, login
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson

from location.forms import MapForm, SearchMapForm, LocationForm, RegistrationForm, UserForm
from location.models import Location

from gmapi import maps
from emailusernames.utils import create_user

def create_info_content(location):
    activities = '<ul>'
    for activity in location.activities.all():
        activities += '<li>'+activity.name+'</li>'
    activities += '</ul>'    
    return '<div style="height:130px; width:300px;">%s</br>%s %s</br>%s, %s%s</div>' % (
        location.place_name, location.user.first_name, 
        location.user.last_name, location.phone_number, 
        location.user.email, activities)

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
        }
    )
    
    for location in Location.objects.all():
        marker = maps.Marker(opts = {
                'map': gmap,
                'position': maps.LatLng(location.latitude, location.longitude),
            })
        maps.event.addListener(marker, 'mouseover', 'm_listener.markerOver')
        maps.event.addListener(marker, 'mouseout', 'm_listener.markerOut')
        info = maps.InfoWindow({
            'content': create_info_content(location),
            'disableAutoPan': True
        })
        info.open(gmap, marker)    
    
    context = {'form': MapForm(initial={'gmap': gmap}), 'active_menu':0 }
    if 'message' in request.flash and request.flash['message']:
        context['alert_type'], context['alert_message'] = request.flash['message']
        
    return render(request, 'map_page.html', context)

def create_search_map_form():
    gmap = maps.Map(
        opts = {
            'center': maps.LatLng(15.87003, 100.99254),
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
        'position': maps.LatLng(15.87003, 100.99254),
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
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            location = form.save(commit=False)
            location.user = request.user;
            location.save()
            request.flash['message'] = ('alert-success', _('Place updated successfully'))
            return HttpResponseRedirect('/places')
    else:        
        form = LocationForm(instance=location)
    
    context = {'form': form, 'map_form': create_search_map_form()}
    return render(request, 'edit_location_page.html', context)
    
@login_required
def add_location_page(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            location = form.save(commit=False)
            location.user = request.user;
            location.save()
            request.flash['message'] = ('alert-success', _('New place added successfully'))
            return HttpResponseRedirect('/places')
    else:
        form = LocationForm()
    
    context = {'form': form, 'map_form': create_search_map_form()}
    return render(request, 'add_location_page.html', context)

@csrf_exempt
@login_required
def delete_location_page(request):    
    Location.objects.filter(pk=int(request.POST.get('pk'))).delete()
    return HttpResponse(simplejson.dumps(0), mimetype="application/json")
    
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
    