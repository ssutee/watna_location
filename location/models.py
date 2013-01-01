from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_countries import CountryField
from django_countries.fields import Country

class Picture(models.Model):

    file = models.ImageField(upload_to="pictures")
    thumbnail = models.ImageField(upload_to="thumbnails", max_length=500, null=True, blank=True)
    slug = models.SlugField(max_length=50, blank=True)
    location = models.ForeignKey('Location', null=True, blank=True, related_name="pictures")

    def create_thumbnail(self):
        if not self.file:
            return
            
        from PIL import Image
        from cStringIO import StringIO
        from django.core.files.uploadedfile import SimpleUploadedFile
        import os
        
        THUMBNAIL_SIZE = (100, 100)
        DJANGO_TYPE = self.file.file.content_type
        
        if DJANGO_TYPE == 'image/jpeg':
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'
        elif DJANGO_TYPE == 'image/png':
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'
            
        image = Image.open(StringIO(self.file.read()))
        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
        temp_handle = StringIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)
        
        suf = SimpleUploadedFile(os.path.split(self.file.name)[-1], 
            temp_handle.read(), content_type=DJANGO_TYPE)
            
        self.thumbnail.save(
            '%s_thumbnail.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION),
            suf, save=False)

    def __unicode__(self):
        return self.file.name

    @models.permalink
    def get_absolute_url(self):
        return ('upload-new', )

    def save(self, *args, **kwargs):
        self.create_thumbnail()
        self.slug = self.file.name
        super(Picture, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.file.delete(False)
        if self.thumbnail:
            self.thumbnail.delete(False)
        super(Picture, self).delete(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(User)

    map_type = models.CharField(max_length=10, default='ROADMAP')
    sorting = models.CharField(max_length=10, default='entry')

class Status(models.Model):
    name = models.CharField(max_length=200, db_index=True, 
        verbose_name=_('Name'), unique=True)
    
    class Meta:
        verbose_name = _('Status')
        verbose_name_plural = _('Status')

    def __unicode__(self):
        return u'%s' % (self.name)
        
class Location(models.Model):
    user = models.ForeignKey(User, null=True)
    place_name = models.CharField(max_length=200, verbose_name=_('Place name'))
    organization = models.BooleanField(verbose_name=_('Organization'))
    relation = models.ForeignKey('Relation', verbose_name=_('Organization relationship'),
        null=True, blank=True)
    status = models.ForeignKey(Status, verbose_name=_('Status'),
        related_name="locations", null=True)

    longitude = models.FloatField(verbose_name=_('Longitude'))
    latitude = models.FloatField(verbose_name=_('Latitude'))
    
    address = models.TextField(verbose_name=_('Address'))
    city = models.CharField(max_length=200, verbose_name=_('City'))
    country = CountryField(default='TH', verbose_name=_('Country'))
    phone_number = models.CharField(max_length=30, verbose_name=_('Phone number'))

    activities = models.ManyToManyField('Activity', verbose_name=_('Activities'),
        related_name="locations", blank=True, null=True)
    
    additional_info = models.TextField(verbose_name=_('Additional information'), 
        blank=True, null=True)
    
    approved = models.BooleanField(verbose_name=_('Approval'), default=False)
    hide_email = models.BooleanField(verbose_name=_('Hide email'), default=False)
    hide_phone_number = models.BooleanField(verbose_name=_('Hide phone number'), default=False)
    hide_address = models.BooleanField(verbose_name=_('Hide address'), default=False)
        
    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')

    def __unicode__(self):
        return u'%s' % (self.place_name)

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^location\.models\.ColorModelField"])

class Relation(models.Model):
    name = models.CharField(max_length=200, db_index=True, 
        verbose_name=_('Name'), unique=True)

    def __unicode__(self):
        return u'%s' % (self.name)

class ColorModelField(models.CharField):
    pass

class Activity(models.Model):
    name = models.CharField(max_length=200, db_index=True, 
        verbose_name=_('Name'), unique=True)
    priority = models.IntegerField(verbose_name=_('Priority'), 
        default=0)
    color = ColorModelField(max_length=7, verbose_name=_('Color'), 
        default="#FF776B")

    class Meta:
        verbose_name_plural = _('Activities')
        verbose_name = _('Activity')

    def __unicode__(self):
        return u'%s' % (self.name)    