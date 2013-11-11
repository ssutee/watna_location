from django.core.management import setup_environ
import watna_location.settings
setup_environ(watna_location.settings)

import os, os.path, httplib2

from django.conf import settings
from location.models import Location
from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

from location.tasks import insert_location_task

KEY = ''
with open(os.path.join(os.path.dirname(__file__), '.', 'ddd6cbbb3fa5f618dafbb45d893aae97609eb4b3-privatekey.p12'), 'rb') as f:
    KEY = f.read()

credentials = SignedJwtAssertionCredentials(
    '905290935225@developer.gserviceaccount.com', 
    KEY, scope='https://www.googleapis.com/auth/fusiontables')

def create_query():
    return build('fusiontables', 'v1', http=credentials.authorize(httplib2.Http())).query()

def get_all_rows():
    sql = "SELECT ROWID,Number FROM %s" % (settings.TABLE_ID)
    ret = create_query().sql(sql=sql).execute()
    return ret.get('rows', [])    

def get_rows(location):
    sql = "SELECT ROWID FROM %s WHERE Number = %d" % (settings.TABLE_ID, location.id)
    ret = create_query().sql(sql=sql).execute()
    return ret.get('rows', [])

def insert_location(location):
    cmd = "INSERT INTO %s (Number, Location, Status, Organization) VALUES (%d, '%.6f,%.6f', %d, %d)"
    sql = cmd % (settings.TABLE_ID, location.id, 
        location.latitude, location.longitude, 
        location.status.id, location.organization)
    create_query().sql(sql=sql).execute()

for location in Location.objects.filter(pk__gte=1985):
    if not get_rows(location):
        print location
        insert_location(location)
#for row in get_all_rows():
#    if not Location.objects.filter(pk=int(row[1])):
#        sql = "DELETE FROM %s WHERE ROWID = '%s'" % (settings.TABLE_ID, row[0])
#        create_query().sql(sql=sql).execute()
        
