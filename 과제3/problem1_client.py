import argparse, random, socket, zen_utils

MAX_BYTES = 65535

def recvall(sock, length):
    data=b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('was expecting %d bytes but only recevied %d bytes before the socket closed'%(length, len(data)))
        data += more
    return data

def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print('Client has been assigned socket name',sock.getsockname())

    while True :
        print("  <<Guess the number>>  enter  (start) or (close) ")
        text = input()
        data=text.encode('ascii')
        sock.sendall(data)
        
        if text == 'start' : #start를 입력받으면 게임 시작
            reply, adress=sock.recvfrom(MAX_BYTES)
            _reply=reply.decode('ascii')
            print(_reply)
            for i in range(1,6) :
                print("Guess the number 1~10 (or enter (end) to end the game):")
                guess=input()  #숫자 입력받고
                data=guess.encode('ascii')
                sock.sendall(data) #guess 보내기
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
                if answer == 3:
                    print("restart the game")
                    break
                if i == 5:
                    print("You used up every opportunity.")
                    i=0
                
            continue
        
        elif text == 'close' : #close 입력받으면 연결 끝
            print('End game And Close the connection')
            sock.sendall(text.encode('ascii'))
            sock.close()
            break
        else :
            continue

            
        

    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Example client')
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('-e', action='store_true', help='cause an error')
    parser.add_argument('-p', metavar='port', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    client(args.host, args.p)