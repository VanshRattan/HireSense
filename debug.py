import urllib.request, json, os

v_data = b'test dummy data'

req = urllib.request.Request('http://127.0.0.1:8000/sessions/start', data=json.dumps({'user_id':1}).encode('utf-8'), headers={'Content-Type': 'application/json'})
res = urllib.request.urlopen(req)
sid = json.loads(res.read())['id']

import mimetypes
boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
body = (f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name=\"file\"; filename=\"test.webm\"\r\n'
        f'Content-Type: video/webm\r\n\r\n').encode('utf-8') + v_data + f'\r\n--{boundary}--\r\n'.encode('utf-8')

req_u = urllib.request.Request(f'http://127.0.0.1:8000/sessions/{sid}/upload', data=body, headers={
    'Content-Type': f'multipart/form-data; boundary={boundary}',
    'Content-Length': str(len(body))
})
urllib.request.urlopen(req_u)

try:
    req_f = urllib.request.Request(f'http://127.0.0.1:8000/sessions/{sid}/finish', method='POST')
    urllib.request.urlopen(req_f)
except Exception as e:
    print(e.read().decode())
