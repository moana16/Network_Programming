
import socket
import random
import argparse

MAX_BYTES = 65535

def recvall(sock, length):
    data=b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('was expecting %d bytes but only recevied %d bytes before the socket closed'%(length, len(data)))
        data += more
    return data


def client(host, port) :
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host,port))
    print('Client has been assigned socket name',sock.getsockname())
    text='start'
    data=text.encode('ascii')
    sock.sendto(data,(host,port))
    reply, address=sock.recvfrom(MAX_BYTES)
    _reply=reply.decode('ascii')
    print('The server {} replied {!r}'.format(port, _reply)) #게임 시작하라고 답변받음
    for i in range(1,6) :
        print("Guess the number 1~10 :")
        guess=input()  #숫자 입력받고
        data=guess.encode('ascii')
        sock.sendto(data,(host,port)) #guess 보내기
        data, adress =sock.recvfrom(MAX_BYTES)
        answer_str = data.decode('ascii')
        answer=int(answer_str)
        if answer == 0:
            print("Congratulations you did it.")
            break

        if answer == 1:
            print("You guessed too small!")
        
            
        if answer == 2:
            print("You guessed too high!")

        if i == 5:
            print("You used up every opportunity.")
        


    reply=recvall(sock,16)
    print('The server said', repr(reply))
    sock.close()

def server(interface, port) :
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    sock.bind((interface,port))
    sock.listen(1)
    print('Listening at', sock.getsockname())
    while True:
        print('Waiting to accept a new connection')
        sc, sockname=sock.accept()
        print('We have accepted a connection from', sockname)
        print('   Socket name:', sc.getsockname())
        print('   Socket peer:', sc.getpeername())
        message, address =sc.recvfrom(MAX_BYTES)
        text=message.decode('ascii')
        if text == 'start' : #start가 들어오면 게임 시작
            flag = 0

        if flag == 0 : #게임 시작 상태이면
            x = random.randrange(1,10)
            alrm='Start the game'
            data=alrm.encode('ascii')
            sc.sendto(data,('127.0.0.1',port))
            for i in range(1,6) : #다섯 번 동안 반복
    
                num, address =sc.recvfrom(MAX_BYTES)
                guess_str=num.decode('ascii')
                guess=int(guess_str) #client가 guess한 숫자

                if guess == x: 
                    print("Congratulations you did it.")
                    text = '0'
                    data=text.encode('ascii')
                    sc.sendto(data,('127.0.0.1',port))
                    flag = 1
                    break
                
                if guess < x :
                    text = '1'
                    data=text.encode('ascii')
                    sc.sendto(data,('127.0.0.1',port))
                    print("You guessed too small!")
                if guess > x : 
                    text = '2'
                    data=text.encode('ascii')
                    sc.sendto(data,('127.0.0.1',port))
                    print("You guessed too high!")

        sc.sendall(b'Farewell, client')
        sc.close()


if __name__ == '__main__' :
    choices={'client' : client, 'server' : server}
    parser = argparse.ArgumentParser(description='Send and receive  over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;' 'host the client send to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='TCP port (default 1060)')
    
    args = parser.parse_args()
    function=choices[args.role]
    function(args.host, args.p)