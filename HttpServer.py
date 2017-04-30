import socket
import signal
import time
import mimetypes
import Request
import Response
import re
from queue import Queue
from threading import Thread
import os
import select
from multiprocessing.pool import Pool
class serveRequests(Thread):
    def __init__(self, queue, handler):
        Thread.__init__(self)
        self.queue = queue
        self.handler = handler
    def run(self):
        while True:
            connection, host, port = self.queue.get()
            request = Request.Request(connection.recv(1024))
            #print(connection.recv(1024).decode())
            connection = self.handler(request, connection, host, port)
            self.queue.task_done()
            #time.sleep(20)

            

class Server:
    def __init__(self, router,  port = 8080, configFile = None):
        self.__router = router
        self.__host = '' or '192.168.1.109'    
        self.__port = port
        mimetypes.init()
        self.__mimetypes = mimetypes.types_map
        self.__mimetypes['.webp'] = 'image/webp'
        self.__mimetypes['.ico'] = 'image/*'
    def initiateServer(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Initiating HTTP server on {0}:{1}'.format(self.__host, self.__port))
        server_address = (self.__host, self.__port)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__socket.bind(server_address)
        self.listenForever()
    def shutdownServer(self):
        try:
            server.__socket.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            print('nOPe', e)
        finally:
            return self.__socket.close()
    def listenForever(self):
        while True:
            print('HTTP server listenting on {0}:{1}'.format(self.__host, self.__port))
            queue = Queue()
            
            for x in range(5):
                worker = serveRequests(queue, self.handleRequest)
                worker.daemon = True
                worker.start()
            self.__socket.listen(5)           
            connection, address = self.__socket.accept()
            queue.put((connection, self.__host, self.__port))
            
        queue.join()
            # self.__socket.listen(5)
            # connection, address = self.__socket.accept()
            # data = connection.recv(4096)
            # print(bytes.decode(data))
            # request = Request.Request(data)
            # connection = self.handleRequest(request, connection)
            #time.sleep(15)

         
        return 0    
    def handleRequest(self, request, connection, host, port):
        if(request.keys() == ''):
            print('bunga')
        method = request['method']
        route = request['route']
        response = Response.Response(connection, self.__host, self.__port)
        if(not 'Host' in request.keys()):
            return response.send400BadRequest()
        if(not self.__router[method]):
            if(not method in self.__router.getKnownMethods()):
                return response.send405MethodNotAllowed()
            return response.send503NotImplemented()
        if(not self.__router[method].get(route)):
            return response.send404NotFound()
        contentType = request['Accept'] or request['Content-Type']
        if ',' in contentType:
            contentType = contentType.split(',')
            for mimeType in contentType:
                if(mimeType in self.__mimetypes.values()):
                    break
        elif(not contentType or  contentType == '*/*' ):
            '''this will go to next check'''
            pass
        elif(not contentType in self.__mimetypes.values()):
            print('Not In MimyTypes')
            return response.send406NotAcceptable()
        elif(route != '/'):
            isValid = False
            resourceExtension = re.match('.*(\.[a-z]*)', route)
            if(not resourceExtension):
                print('noResourceExtensions')
                return response.send406NotAcceptable()
            resourceExtension = resourceExtension.group(1)
            for mimeType in contentType:
                print(mimeType, resourceExtension)
                if(mimeType == self.__mimetypes[resourceExtension]):
                    isValid = True
                    break
            if(not isValid):
                print('not a valid resource for type')
                return response.send406NotAcceptable()
        response.setStatusCode(200)
        return self.__router[method].get(route)(response)
        
#server = Server()
#server.initiateServer()
