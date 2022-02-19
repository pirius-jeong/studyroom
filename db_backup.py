from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from googleapiclient.http import MediaFileUpload
from datetime import datetime

work_dt = datetime.today().strftime("%Y%m%d")

try :
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/drive.file'
store = file.Storage('/home/kizacademy/projects/mysite/storage.json')
creds = store.get()

if not creds or creds.invalid:
    print("make new storage data file ")
    flow = client.flow_from_clientsecrets('/home/kizacademy/projects/mysite/client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store, flags) \
            if flags else tools.run(flow, store)

DRIVE = build('drive', 'v3', http=creds.authorize(Http()))

folder_id = '130Fxlqmlua9QpWym6xyc24klYn60A_v9'
filename = 'db.sqlite3_' + work_dt
request_body = {'name': filename,
                'parents': [folder_id] } # 업로드할 파일의 정보 정의
media = MediaFileUpload('db.sqlite3') # 업로드할 파일
file = DRIVE.files().create(body=request_body,media_body=media).execute()
print("File ID :",file.get('id'))