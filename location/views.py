#-:- coding:utf-8 -:-

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.contrib.auth import authenticate, logout, login
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from django.db.models import Count
from django.views.generic import CreateView, DeleteView
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.files import File

from location.forms import MapForm, SearchMapForm, LocationForm, RegistrationForm, UserForm
from location.models import Location, Profile, Picture

from gmapi import maps
from emailusernames.utils import create_user
from django_countries.fields import Country

def response_mimetype(request):
    if "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    else:
        return "text/plain"

class PictureCreateView(CreateView):
    model = Picture
    
    def get(self, request, *args, **kwargs):
        location = Location.objects.get(pk=int(kwargs['pk']))
        
        if request.user.id != location.user.id:
            return HttpResponseRedirect('/places')
            
        if request.is_ajax():
            files = {'files': map(lambda p:{'name':p.file.name, 
                'size':p.file.size, 'url':p.file.url, 
                'thumbnail_url':p.thumbnail.url, 'delete_type': 'DELETE',
                'delete_url':reverse('upload-delete', args=[p.id])}, location.pictures.all())}
            print simplejson.dumps(files)
            return HttpResponse(simplejson.dumps(files), mimetype="application/json")
        else:
            response = super(PictureCreateView, self).get(request, args, kwargs)
            response.context_data = dict(response.context_data, **{'location': location})
            return response

    def form_valid(self, form):
        self.object = form.save()
        
        f = self.request.FILES.get('file')    
        
        files = {'files': [{
            'name': f.name,
            'size': f.size,
            'url': self.object.file.url,
            'thumbnail_url': self.object.thumbnail.url,
            'delete_url': reverse('upload-delete', args=[self.object.id]),
            'delete_type': 'DELETE'
        }]}
        
        return HttpResponse(simplejson.dumps(files), mimetype="application/json")

class PictureDeleteView(DeleteView):
    model = Picture

    def delete(self, request, *args, **kwargs):
        """
        This does not actually delete the file, only the database record.  But
        that is easy to implement.
        """
        self.object = self.get_object()
        self.object.delete()
        if request.is_ajax():
            response = JSONResponse(True, {}, response_mimetype(self.request))
            response['Content-Disposition'] = 'inline; filename=files.json'
            return response
        else:
            return HttpResponseRedirect('/new_upload')

class JSONResponse(HttpResponse):
    """JSON response class."""
    def __init__(self,obj='',json_opts={},mimetype="application/json",*args,**kwargs):
        content = simplejson.dumps(obj,**json_opts)
        super(JSONResponse,self).__init__(content,mimetype,*args,**kwargs)

def upload_files_page(request, pk):
    if request.method == 'POST':
        print request
        return HttpResponse(simplejson.dumps(0), mimetype="application/json")
    
    context = {'location': Location.objects.get(pk=pk)}
    return render(request, 'upload_files_page.html', context)

def create_info_content(location):
    return '<div id="%d" style="height:100px; width:300px;"><h4>%s, %s</h4>%s</div>' % (
        location.id,
        location.place_name, location.city,
        ', '.join(map(lambda x:x.name,location.activities.all())))

def get_map_type(request):
    if request.user.is_authenticated():
        try:
            request.user.profile
        except Profile.DoesNotExist, e:
            profile = Profile(user=request.user)
            profile.save()
        
    return maps.MapTypeId.ROADMAP if not request.user.is_authenticated() else request.user.profile.map_type.lower()

def map_page(request):
    request.session['next'] = '/'
    gmap = maps.Map(
        opts = {
            'center': maps.LatLng(14.01012, 100.82302),
            'mapTypeId': get_map_type(request),
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
        
        color = '846744' if unicode(location.status) == u'ภิกษุ' or unicode(location.status) == u'ภิกษุณี' else 'F3F3F3'
                    
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
        
    first_order = 'pk'
    try:
        first_order = 'city' if request.user.is_authenticated() and request.user.profile.sorting == 'city' else 'pk'
    except Profile.DoesNotExist, e:
        pass
        
    nav_list = []    
    total_country = 0
    countries = ''
    for value in Location.objects.values('country').annotate(total=Count('country')):
        query = Location.objects.filter(country=value['country']).order_by(first_order, 'place_name')
        country_name = unicode(Country(code=value['country']).name)
        nav_list.append({'type':'header', 'value': '%s (%d)' % (country_name, query.count())})        
        for location in query.all():
            nav_list.append({'type':'item', 'value': location, 
                'has_picture': 'ok'})    
        total_country += 1
        countries += '<p>%s (%d)</p>' % (country_name, query.count())
            
    context = {'form': MapForm(initial={'gmap': gmap}), 
        'active_menu':0, 'nav_list': nav_list, 'total': Location.objects.count(), 
        'total_country': total_country, 'countries': countries }
    if 'message' in request.flash and request.flash['message']:
        context['alert_type'], context['alert_message'] = request.flash['message']
        
    return render(request, 'map_page.html', context)

def create_search_map_form(request, lat, lng):
    gmap = maps.Map(
        opts = {
            'center': maps.LatLng(lat, lng),
            'mapTypeId': get_map_type(request),
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

    if location.user.id != request.user.id:
        return HttpResponseRedirect('/places')
        
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
    
    context = {'form': form, 'map_form': create_search_map_form(request, lat, lng)}
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
    
    context = {'form': form, 'map_form': create_search_map_form(request, lat, lng)}
    return render(request, 'add_location_page.html', context)

@csrf_exempt
@login_required
def delete_location_page(request):    
    Location.objects.filter(pk=int(request.POST.get('pk'))).delete()
    return HttpResponse(simplejson.dumps(0), mimetype="application/json")

@csrf_exempt
@login_required
def set_map_type_page(request):
    try:
        request.user.profile
    except Profile.DoesNotExist, e:
        profile = Profile(user=request.user)
        profile.save()

    request.user.profile.map_type = request.POST.get('map_type', 'ROADMAP')
    request.user.profile.save()
    
    return HttpResponse(simplejson.dumps(0), mimetype="application/json")
    
@csrf_exempt
@login_required
def set_sorting_page(request):
    try:
        request.user.profile
    except Profile.DoesNotExist, e:
        profile = Profile(user=request.user)
        profile.save()

    request.user.profile.sorting = request.POST.get('sorting', 'entry')
    request.user.profile.save()

    return HttpResponse(simplejson.dumps(0), mimetype="application/json")
    
@csrf_exempt
def find_location_by_id_page(request):    
    location = Location.objects.get(pk=int(request.POST.get('id', 1)))    
    is_authenticated = request.user.is_authenticated()
    data = {
        'place_name': location.place_name,
        'email': location.user.email if is_authenticated else unicode(_('Only member')),
        'first_name': location.user.first_name,
        'last_name': location.user.last_name,
        'address': location.address if is_authenticated else unicode(_('Only member')),
        'city': location.city,
        'info': unicode(_('Organization')) if location.organization else unicode(_('Person')),
        'status': location.status.name if location.status else '-',
        'additional_info': location.additional_info if location.additional_info and len(location.additional_info.strip()) > 0 else '-',
        'country': unicode(location.country.name),
        'phone_number': location.phone_number if is_authenticated else unicode(_('Only member')),
        'activities': ', '.join(map(lambda x:x.name,location.activities.all())),
        'relation': location.relation.name if location.relation else '',
        'has_picture': location.pictures.count() > 0,
        'pictures': map(lambda p:(p.file.url, p.thumbnail.url), location.pictures.all()),
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
    