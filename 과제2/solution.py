from email import message
import json
from multiprocessing import context
from re import I
import zlib
import socket
import ssl
import base64
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class Solution():
    
    def special_bits(self, L=1, R=2, k=1):
        num = -2
        # Write your code between start and end for solution of problem 1
        # Start
        while True :
            sbl = bin (L).count ("1")
            if 2 ** k -1 > R :
                num = -1 
                break
            if sbl == k :
                num = 1
                break
            lbit = L.bit_length()
            if k > sbl :
                df = k-sbl
                if lbit > k :
                    for i in range(65):
                        i2 = 2 ** i
                        if not (i2 & L):
                            df -= 1
                            L += i2
                        if not df: num = L if L <= R else -1
                    break
                else :
                    num = 2 ** k -1
                    break
            else :
                df = sbl - k + 1
                abc = 0
                for i in range (65):
                    i2 = 2 ** i
                    if not df and not (i2 & L):
                        L += i2 + 2 ** abc - 1
                        num = L if L <= R else -1
                        break
                    if i2 & L:
                        L -= i2
                        if df: df -= 1
                        else: abc += 1
        # End
        return num

    def toggle_string(self, S):
        s = ""
        # Write your code between start and end for solution of problem 2
        # Start
        for i in S:
            if(i>= 'a' and i<= 'z') : 
                s = s + chr((ord(i) - 32))
            elif( i>='A' and i <= 'Z') : 
                s = s +chr((ord(i) + 32))
            else :
                s = s + i

        # End
        return s

    def send_message(self, message):
        message = self.to_json(message)
        message = self.encode(message)
        message = self.compress(message)
        return message

    def recv_message(self, message):
        message = self.decompress(message)
        message = self.decode(message)
        message = self.to_python_object(message)
        return message
    
    # String to byte
    def encode(self, message):
        # Write your code between start and end for solution of problem 3
        # Start
        encoded = message.encode('utf-8')
        return encoded
        # End
        
    
    # Byte to string
    def decode(self,message):
        # Write your code between start and end for solution of problem 3
        # Start
        decoded = message.decode('utf-8')
        return decoded
        # End 

    # Convert from python object to json string
    def to_json(self, message):
        # Write your code between start and end for solution of problem 3
        # Start
        data = json.dumps(message)
        return data
        # End 

    # Convert from json string to python object
    def to_python_object(self, message):
        # Write your code between start and end for solution of problem 3
        # Start
        data = json.loads(message)
        return data
        # End 
    
    # Returns compressed message 
    def compress(self, message):
        # Write your code between start and end for solution of problem 3
        # Start
        compressed = zlib.compress(message)
        return compressed
        # End 

    # Returns decompressed message
    def decompress(self, compressed_message):
        # Write your code between start and end for solution of problem 3
        # Start
        decompressed = zlib.decompress(compressed_message)
        return decompressed
        # End 


    def client(self, host, port, cafile=None):
        # Write your code between start and end for solution of problem 4
        # Start
        purpose = ssl.Purpose.SERVER_AUTH
        context = ssl.create_default_context(purpose, cafile=cafile) #create default context

        raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket
        raw_sock.connect((host,port)) #connect
        print('Connected to host {!r} and port {}'.format(host,port))
        ssl_sock = context.wrap_socket(raw_sock,  server_hostname=host) #create encrypted socket

        while True : 
            msg = ssl_sock.recv(1024) # Variable to store message received from server
            if not msg : 
                break

        cert = ssl_sock.getpeercert() # Variable to store the certificate received from server 
        if cert is None : 
            print('Certificate is None')
        else :
            print('Certificate is provided')
            subject = cert.get('subject',[])
            names = [name for names in subject for (key, name) in names if key == 'commomName']
            if 'subjectName' in cert :
                names.extend(name for (key, name) in cert ['subjectName'] if key == 'DNS')
            try :
                ssl.match_hostname(cert, host)
            except ssl.CertificateError as e :
                message = str(e)
            else : 
                message='Yes'
        cipher = ssl_sock.cipher() # Variable to store cipher used for connection


        # End
        return cert, cipher, msg
    
    

    
