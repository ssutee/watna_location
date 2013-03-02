from location.models import Profile

def profile(request):    
    map_type = 'ROADMAP'
    sorting = 'entry'
    display = 0
    if hasattr(request, 'user'):
        try:
            if request.user.is_authenticated():
                map_type = request.user.profile.map_type
                sorting = request.user.profile.sorting
                display = request.user.profile.display
        except Profile.DoesNotExist, e:
            profile = Profile(user=request.user)
            profile.save()
    return {'map_type': map_type, 'sorting': sorting}