import socket
import sys
import os
import threading

list_lock = threading.Lock()
clients_list = []
path = os.getcwd()

def lis(client_socket,addr,content_dir):    
    print(clients_list)
    while True:
        try:
            data = client_socket.recv(2048).decode()
            if not data: break
            print(data)
        except Exception as eee:
            print('error',eee)
            break
        try:
            ''' Method '''
            request_method =data.split(' ')[0]

            if request_method == "GET":
                request_file = data.split()[1]
                
            if request_file == "/":
                request_file = "/index.html"
        
            filepath = content_dir + request_file
        
            try:
                f = open(filepath, 'rb')
                if request_method == 'GET':
                    response_data = f.read()
                f.close
                data_type = os.path.splitext(filepath)
                if data_type[1] == '.html':
                    data_type = ' text/html'
                elif data_type[1] == '.js':
                    data_type = ' application/js'
                elif data_type[1] == '.css':
                    data_type = ' text/css'
                    
                data_size = os.path.getsize(filepath)
                response_header = make_header(200,data_type,data_size)
        
            except Exception as e:
                print("File notfound. Serving 404 page.",e)
                response_header = make_header(404,None,None)

                if request_method == "GET": 
                    response_data = '<!DOCTYPE html><html><body><center><h1>Error 404: File not found</h1></center><p></body></html>'.encode()
                break

        except Exception as ex:
            print("Bad request. Serving 400 page.",ex)
            response_header = make_header(400,None,None)

            response_data ='<!DOCTYPE html><html><body><center><h1>Error 400: Bad Request</h1></center><p></body></html>'.encode()
            break      

        response = str(response_header).encode()
        
        if request_method == "GET":
            response += response_data

        #print(response.decode())
        client_socket.send(response)
        print("connected client:" ,addr[0], addr[1] ,'\n')
    
    list_lock.acquire()
    clients_list.remove(client_socket)
    list_lock.release()
    client_socket.close()

def make_header(response_code,data_type,data_size):
    header = ''
    if response_code == 200:
        header += 'HTTP/1.1 200 OK\r\n'
    elif response_code == 400:
        header += 'HTTP/1.1 400 Bad Request\r\n'
    elif response_code ==404:
        header += 'HTTP/1.1 404 Not Found\r\n'

    header += 'Content-Type: ' + str(data_type) + '\r\n'  
    header += 'Content-Length: ' + str(data_size) + '\r\n'
    header += 'Connection: keep-alive\r\n\r\n'
    return header


def main():
    #content_dir = r'''C:\Users\HOME-PC\Desktop\source'''
    content_dir = path + '/' + "source"
    server_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('127.0.0.1',50007))
    server_socket.listen(16)
    try:
        while True:
            print("waiting for connection\nhost: 127.0.0.1 port: 50007\n")
            (client_socket,addr) = server_socket.accept()
            list_lock.acquire()
            clients_list.append(client_socket)
            list_lock.release()
            print("***",addr,"connected ***")
            t = threading.Thread(target = lis, args = (client_socket,addr,content_dir))
            t.start()
    except KeyboardInterrupt:
        print("\n--- Server Closed ---")
        list_lock.acquire()
        for client in clients_list:
            client.close()
        list_lock.release()
        server_socket.close()
        
if __name__ == '__main__':
	main()

