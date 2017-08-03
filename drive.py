# -*- coding: utf-8 -*-

from __future__ import print_function
import httplib2
import os
from StringIO import StringIO

from apiclient import discovery, http
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_Qidian_Novels_folder(service):
    results = service.files().list(fields="nextPageToken, files(id, name)", q="mimeType = 'application/vnd.google-apps.folder' and name = 'Qidian Novels'").execute()
    items = results.get('files', [])
    if not items:
        print('Qidian Novels folder not found.')
    return items[0]
def get_novel_folders(service, Qidian_Novels_folder_id):
    results = service.files().list(fields="nextPageToken, files(id, name)", 
        q="mimeType = 'application/vnd.google-apps.folder' and '{0}' in parents and trashed = false".format(Qidian_Novels_folder_id)).execute()
    items = results.get('files', [])
    if not items:
        print('No novel folders found.')
    return items
    
def create_novel_folder_if_not_exist(service, parent_folder_id, folder_name):
    #Check if folder exists
    
    
    results = service.files().list(fields="nextPageToken, files(id, name)", 
        q="mimeType = 'application/vnd.google-apps.folder' and '{0}' in parents and name = '{1}' and trashed = False".format(
            parent_folder_id.replace("'", r"\'"), folder_name.replace("'", r"\'"))).execute()
    items = results.get('files', [])
    if items:
        print("Folder already exists")
        return items[0] #Folder exists
    file_metadata = {
        'name': folder_name,
        'mimeType':'application/vnd.google-apps.folder',
        'parents':[parent_folder_id]
    }
    f = service.files().create(body=file_metadata, fields='id, name').execute()
    print("Folder created")
    return f
def add_string_as_docs_file_to_folder(service, parent_folder_id, file_name, text, update=False):
    
    #Check if item exists
    results = service.files().list(fields="nextPageToken, files(id, name)", 
        q="mimeType = 'application/vnd.google-apps.document' and '{0}' in parents and name = '{1}' and trashed = False".format(
            parent_folder_id.replace("'", r"\'"), file_name.replace("'", r"\'"))).execute()
    items = results.get('files', [])
    if items:
        print("File {0} already exists".format(file_name))
        if update: #If update, delete old file and create new one
            for item in items:
                service.files().delete(items.get('id'))
        else:
            return items[0]
    temp_f = StringIO(text)
    file_metadata = {'name' : file_name,
                     'mimeType': 'application/vnd.google-apps.document',
                     'parents' : [parent_folder_id]}
    media = http.MediaIoBaseUpload(temp_f, mimetype='text/plain;charset=utf-8', chunksize=-1, resumable=True)
    f = service.files().create(body=file_metadata, media_body=media, fields="id, name").execute()
    print("File {0} added".format(file_name))
    return f
    
def create_service():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    return service
def main():
    service = create_service()
    folder_id = get_Qidian_Novels_folder(service)['id']
    print(get_novel_folders(service, folder_id))
    test_f = create_novel_folder_if_not_exist(service, folder_id, 'test')
    print(add_string_as_docs_file_to_folder(service, test_f['id'], "test", u"test test test"))
    
#    results = service.files().list(fields="nextPageToken, files(id, name)").execute()
#    items = results.get('files', [])
#    if not items:
#        print('No files found.')
#    else:
#        print('Files:')
#        for item in items:
#            print('{0} ({1})'.format(item['name'], item['id']))

if __name__ == '__main__':
    main()