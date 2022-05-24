import asyncio
import argparse, random

@asyncio.coroutine
def server(reader, writer) :
    address = writer.get_extra_info('peername')
    print('Accepted connection from {}'.format(address))

    while True:
        message = yield from reader.read(4096)
        text=str(message).split('\'')[1]

        if text == 'start' : #start가 들어오면 게임 시작
            flag = 0
        
        elif text == "close" :
            print('Close the connect with client')
            return

        if flag == 0 : #게임 시작 상태이면
            x = random.randrange(1,10)
            alrm='Start game'
            print('Start game')
            writer.write(alrm.encode('ascii'))
            
            for i in range(1,6) : #다섯 번 동안 반복
                guess_str = yield from reader.read(4096)
                message = str(guess_str).split('\'')[1]

                if message == "end" :
                    print('end the game')
                    text = '3'
                    writer.write(text.encode('ascii')) # 숫자 맞췄는지 여부 보냄
                    break

                elif guess_str.isdigit():
                    guess=int(guess_str)
                    if guess == x: 
                        print("Congratulations you did it.")
                        text = '0'
                        flag = 1
                        writer.write(text.encode('ascii'))
                        i=0
                        break
                
                    elif guess < x :
                        text = '1'
                        print("You guessed too small!")
                    elif guess > x : 
                        text = '2'
                        print("You guessed too high!")
                
                    writer.write(text.encode('ascii')) # 숫자 맞췄는지 여부 보냄

        else:
            continue


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='"Guess the number" game over TCP')
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('-p', metavar='port', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()

    address = (args.host, args.p)
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(server, *address)
    server = loop.run_until_complete(coro)
    print('Listening at {}'.format(address))
    try:
        loop.run_forever()
    finally:
        server.close()
        loop.close()