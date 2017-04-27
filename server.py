import socket
import signal
import time

class Server:
    def __init__(self, port = 8080):
        self.host = ''
        self.port = port
    def initiateServer(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Initiating HTTP server on {0}:{1}'.format(self.host, self.port))
        server_address = (self.host, self.port)
        self.socket.bind(server_address)
        self.listenForever()
    def listenForever(self):
        while True:
            self.socket.listen(5)
            connection, address = self.socket.accept()
            data = connection.recv(1024)
            print(bytes.decode(data))
            requestString = bytes.decode(data)
            request = self.processRequest(requestString)
            print(request)
            if(request['method'] == 'GET'):
                h = 'HTTP/1.1 203 CREATED\r\n'
                current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
                h += 'Date: {0}\r\n'.format(current_date)
                h += 'Server: {0}:{1}\r\n'.format(self.host, self.port)
                h += 'Connection: close\r\n\n\n'
                body = b'<p>Stuff</p>'
                h = h.encode()
                h += body
                connection.send(h)
                print(h)
                connection.close()
    def processRequest(self, requestString):
        requestArray = requestString.split(' ')
        print(requestArray)
        return {'method': requestArray[0]}
server = Server()
server.initiateServer()
