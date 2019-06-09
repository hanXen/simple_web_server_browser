import socket

def make_header(content):
        header = ''
        header += 'GET '
        header += content
        header += ' HTTP/1.1\r\n'
        header += 'Host: ' + host +'\r\n'
        header += 'Connection: keep-alive\r\n\r\n'
        return header
        
while True:  
        serv = input('input host:port ex) 127.0.0.1:50007 : ')
        try:
                host = serv.split(':')[0]
                host = host.split('/')[0]
                try:
                        port = serv.split(':')[1]
                except Exception :
                        port = 80
               
                addr = (host,int(port))
                s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.connect(addr)
        except Exception as e:
                print("Failed to connect: ", e)
                continue

        request = make_header('/');
        #print(request)
        s.send(request.encode())
        data2 = s.recv(65536)
        if not data2:
                break
        print(data2.decode())
        data_s = data2.decode()
        cnt = data_s.count('src="')
        ccnt = data2.decode().count('href="')

        while cnt > 0:
                tmp = data_s[data_s.find('src="'):]
                tmp = tmp[5:tmp.find('>')]
                data_s = data_s[data_s.find('src="')+1:]
                tmp = tmp[:tmp.find('"')]
                tmp = '/' + tmp
                request = make_header(tmp)
                #print(request)
                try:
                        s.send(request.encode())
                        data3 = s.recv(1024)
                        print(data3.decode(),'\n')
                except Exception as ex:
                        print("Error",ex)
                cnt = cnt - 1

        data_s = data2.decode() 
        while ccnt > 0:
                tmp = data_s[data_s.find('href="'):]
                tmp = tmp[6:tmp.find('>')]
                data_s = data_s[data_s.find('href="')+1:]
                tmp = tmp[:tmp.find('"')]
                tmp = '/' + tmp
                request = make_header(tmp)
                    #print(request)
                try:
                        s.send(request.encode())
                        data3 = s.recv(1024)
                        print(data3.decode(),'\n')
                except Exception as ex:
                        print("Error",ex)
                ccnt = ccnt -1 

