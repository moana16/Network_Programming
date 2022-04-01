import argparse
from secrets import choice
import socket
from datetime import datetime
from turtle import delay
from urllib.parse import quote_plus

MAX_BYTES = 65535

def server(port) :
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1',port))
    print('Listening at {}'.format(sock.getsockname()))
    while True : 
        data, address = sock.recvfrom(MAX_BYTES)
        text = data.decode('ascii')
        print('The Client at {} says {!r}'.format(address,text))
        #text='Your data was {} bytes long'.format(len(data))
        if len(data) %2 == 0 :
            text= 'Your data was {} bytes long'.format(len(data))
        else : 
            text = 'Error 403 Forbidden.'

        data=text.encode('ascii')
        sock.sendto(data,address)

def client (port) :
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    text = input('')
    #text = 'The time is {}'.format(datetime.now())
    data = text.encode('ascii')
    sock.sendto(data,('127.0.0.1',port))
    print('The OS assigned me the adress {}'.format(sock.getsockname()))
    data, address = sock.recvfrom(MAX_BYTES)
    text = data.decode('ascii')
    print('The server {} replied {!r}'.format(address, text))


if __name__ == '__main__' :
    choices={'client' : client, 'server' : server}
    parser = argparse.ArgumentParser(description='Send and receive UDP locally')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('-p', metavar='PORT', type=int, default=1061, help='UDP port (default 1061)')
    
    args = parser.parse_args()
    function=choices[args.role]
    function(args.p)