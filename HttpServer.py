import socket
import signal
import time
import mimetypes
import Request
import Response
import Logger
import re
from queue import Queue
from threading import Thread

class serveRequests(Thread):
    def __init__(self, queue, handler):
        Thread.__init__(self)
        self.queue = queue
        self.handler = handler
    def run(self):
        while True:
            connection, host, port = self.queue.get()
            request = Request.Request(connection.recv(4096))
            connection = self.handler(request, connection, host, port)
            self.queue.task_done()

class HttpServer:
    def __init__(self, router,  host = None, port = 8080, configFile = None):
        
        self.__router = router
        self.__host = host or '127.0.0.1'    
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
            self.__socket.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            print('nOPe', e)
        finally:
            return self.__socket.close()
    def listenForever(self):
        while True:
            print('HTTP server listenting on {0}:{1}'.format(self.__host, self.__port))
            queue = Queue()
            self.__socket.listen(5)    
            for x in range(5):
                worker = serveRequests(queue, self.handleRequest)
                worker.daemon = True
                worker.start()       
            connection, address = self.__socket.accept()
            queue.put((connection, self.__host, self.__port), 5)
            #queue.join()
        return 0
    '''Request handler used to serve requests.'''     
    def handleRequest(self, request, connection, host, port):
        if(len(request.keys()) == 0):
            return 0
        log = Logger.Logger()
        method = request['method']
        route = request['route'] 
        server = '{0}:{1}'.format(host, port)
        referrer = request['Referer'] or ''
        data = request['params'] or request['body']
        host = request['Host']
        log.log({'method': method, 'timestamp': time.time(), 'server': server, 'host': host, 'referrer': referrer, 'url': route, 'data': data})
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
                return response.send406NotAcceptable()
            resourceExtension = resourceExtension.group(1)
            for mimeType in contentType:
                if(mimeType == self.__mimetypes[resourceExtension]):
                    isValid = True
                    break
            if(contentType == self.__mimetypes[resourceExtension]):
                    isValid = True
            if(not isValid):
                print('not a valid resource for type')
                return response.send406NotAcceptable()
        response.setStatusCode(200)
        return self.__router[method].get(route)(request, response)

