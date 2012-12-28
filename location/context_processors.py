from location.models import Profile

def map_type(request):
    map_type = 'ROADMAP'
    try:
        if request.user.is_authenticated():
            map_type = request.user.profile.map_type
    except Profile.DoesNotExist, e:
        profile = Profile(user=request.user)
        profile.save()
    return {'map_type': map_type}