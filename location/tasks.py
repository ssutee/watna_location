from celery import task

import os.path, httplib2
from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials
from django.conf import settings

KEY = ''
with open('ddd6cbbb3fa5f618dafbb45d893aae97609eb4b3-privatekey.p12', 'rb') as f:
    KEY = f.read()

credentials = SignedJwtAssertionCredentials(
    '905290935225@developer.gserviceaccount.com', 
    KEY, scope='https://www.googleapis.com/auth/fusiontables')

def create_query():
    return build('fusiontables', 'v1', http=credentials.authorize(httplib2.Http())).query()

def create_table():
    return build('fusiontables', 'v1', http=credentials.authorize(httplib2.Http())).table()

@task()
def insert_location_task(location):
    cmd = "INSERT INTO %s (Number, Location, Status, Organization) VALUES (%d, '%.6f,%.6f', %d, %d)"
    sql = cmd % (settings.TABLE_ID, location.id, 
        location.latitude, location.longitude, 
        location.status.id, location.organization)
    create_query().sql(sql=sql).execute()

def get_rows(location):
    sql = "SELECT ROWID FROM %s WHERE Number = %d" % (settings.TABLE_ID, location.id)
    ret = create_query().sql(sql=sql).execute()
    for row in ret.get('rows', []):
        yield row    

@task()
def delete_location_task(location):
    for row in get_rows(location):
        sql = "DELETE FROM %s WHERE ROWID = '%s'" % (settings.TABLE_ID, row[0])
        create_query().sql(sql=sql).execute()

@task()
def update_location_task(location):
    for row in get_rows(location):
        sql = "UPDATE %s SET Location = '%.6f,%.6f', Status = %d, Organization = %d WHERE ROWID = '%s'" % \
            (settings.TABLE_ID, location.latitude, location.longitude, 
            location.status.id, location.organization, row[0])
        create_query().sql(sql=sql).execute()
        
@task()
def sync_table_task(file_name):
    create_query().sql(sql="DELETE FROM %s" % (settings.TABLE_ID)).execute()
    create_table().importRows(tableId=settings.TABLE_ID, media_body=file_name, delimiter='\t').execute()
