from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.contrib.auth import authenticate, logout, login
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson

from location.forms import MapForm, LocationForm, RegistrationForm
from location.models import Location

from gmapi import maps
from emailusernames.utils import create_user

def map_page(request):
    gmap = maps.Map(
        opts = {
            'center': maps.LatLng(38, -97),
            'mapTypeId': maps.MapTypeId.ROADMAP,
            'zoom': 3,
            'mapTypeControlOptions': {
                 'style': maps.MapTypeControlStyle.DROPDOWN_MENU
            },
        }
    )
    
    marker = maps.Marker(opts = {
            'map': gmap,
            'position': maps.LatLng(38, -97),
        })
    maps.event.addListener(marker, 'mouseover', 'myobj.markerOver')
    maps.event.addListener(marker, 'mouseout', 'myobj.markerOut')
    
    info = maps.InfoWindow({
        'content': 'Hello!',
        'disableAutoPan': True
    })
    info.open(gmap, marker)
    
    context = {'form': MapForm(initial={'gmap': gmap}), 'active_menu':0 }
    if 'message' in request.flash and request.flash['message']:
        context['alert_type'], context['alert_message'] = request.flash['message']
        
    return render(request, 'map_page.html', context)

def locations_page(request):
    context = {'active_menu':1, 'locations': Location.objects.all()}
    return render(request, 'locations_page.html', context)

def edit_location_page(request, pk):
    location = Location.objects.get(pk=int(pk))    
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            request.flash['message'] = ('alert-success', _('Place Updated Successfully'))
            return HttpResponseRedirect('/places')
    else:        
        form = LocationForm(instance=location)
    
    context = {'form': form}
    return render(request, 'edit_location_page.html', context)
    

def add_location_page(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            request.flash['message'] = ('alert-success', _('New Place Added Successfully'))
            return HttpResponseRedirect('/places')
    else:
        form = LocationForm()
    
    context = {'form': form}
    return render(request, 'add_location_page.html', context)

@csrf_exempt
@login_required
def delete_location_page(request):    
    Location.objects.filter(pk=int(request.POST.get('pk'))).delete()
    return HttpResponse(simplejson.dumps(0), mimetype="application/json")
    
def logout_page(request):
    logout(request)
    request.flash['message'] = ('alert-success', _('Logout Successfully'))
    return HttpResponseRedirect('/')

def login_page(request):
    user = authenticate(email=request.POST.get('email'), password=request.POST.get('password'))
    if user:
        login(request, user)
        request.flash['message'] = ('alert-success', _('Login Successfully'))
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
            request.flash['message'] = ('alert-success', _('Registration Completed Successfully'))
            return HttpResponseRedirect('/')
    else:
        form = RegistrationForm()

    context = {'form': form, 'active_menu':1}
    return render(request, 'registration/register.html', context)    
    