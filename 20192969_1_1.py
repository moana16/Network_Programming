import socket

# Construct GET request (GET operation followed by Headers)
request_text = """\
GET /iss-pass.json?lat={}&format=json&lon={}&format=json HTTP/1.1\r\n\
Host: api.open-notify.org\r\n\
User-Agent: jimin\r\n\
Connection: close\r\n\
\r\n\
"""

def geocode(lat,lon) :
    sc=socket.socket() #create a client socket()
    sc.connect(('api.open-notify.org',80))
    request = request_text.format(lat,lon)
    print(request)
    sc.sendall(request.encode('ascii'))
    raw_reply = b''
    while True : 
        more = sc.recv(4096)
        if not more:
            break
        raw_reply += more
    print(raw_reply.decode('utf-8'))
    

if __name__ == '__main__' :
    geocode(45,180)


