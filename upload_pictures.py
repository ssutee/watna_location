#-*- coding:utf-8 -*-

import time, random, os, os.path, threading

import cloudfiles

from watna_location.settings import CUMULUS

pool=threading.BoundedSemaphore(value=10)

class UploadFile(threading.Thread):
    def __init__(self, filename):
        threading.Thread.__init__(self)
        self.filename=filename
        
    def run(self):
        self.conn = cloudfiles.get_connection(
            username = CUMULUS['USERNAME'], api_key = CUMULUS['API_KEY'], timeout=60)
            
        try:
            self.container = self.conn.get_container(CUMULUS['CONTAINER'])
        except cloudfiles.errors.NoSuchContainer:
            self.container = self.conn.create_container(CUMULUS['CONTAINER'])

        if not self.container.is_public():
            self.container.make_public()

        object_name = os.path.join(*self.filename.split('/')[1:])

        try:            
            cloud_obj = self.container.get_object(object_name)
        except cloudfiles.errors.NoSuchObject:
            cloud_obj = self.container.create_object(object_name)            
            
        print 'upload:', self.filename
        cloud_obj.load_from_filename(self.filename)
            
        pool.release()

class Handler(threading.Thread):
    def __init__(self, path):
        threading.Thread.__init__(self)
        self.path = path
        
    def run(self):
        for root, dirs, files in os.walk(self.path):
            for f in files:
                pool.acquire()
                task = UploadFile(os.path.join(root, f))
                task.setDaemon(False)
                task.start()

handler=Handler('media/')
handler.start()
handler.join()