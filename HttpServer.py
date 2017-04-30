import socket
import signal
import time
import mimetypes
import Request
import Response
import re
class Server:
    def __init__(self, router,  port = 8080, configFile = None):
        self.__router = router
        self.__host = '127.0.0.1' or '192.168.1.109'    
        self.__port = port
        mimetypes.init()
        self.__mimetypes = mimetypes.types_map
        self.__mimetypes['.webp'] = 'image/webp'
        self.__mimetypes['.ico'] = 'image/*'
    def initiateServer(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Initiating HTTP server on {0}:{1}'.format(self.__host, self.__port))
        server_address = (self.__host, self.__port)
        self.__socket.bind(server_address)
        self.listenForever()
    def shutdownServer(self):
        try:
            self.__socket.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            print('nOPe', e)
        finally:
            return
    def listenForever(self):
        while True:
            self.__socket.listen(10)
            print('HTTP server listenting on {0}:{1}'.format(self.__host, self.__port))
            connection, address = self.__socket.accept()
            data = connection.recv(1024)
            print(bytes.decode(data))
            request = Request.Request(data)        
            print(request.values())
            self.handleRequest(request, connection)
            '''
            if False:
                response = Response.Response(connection)
                response.setStatusCode(400)
                response.writeHeader('Server', '{0}:{1}'.format(self.__host, self.__port)) 
                body = '<h1>400 Bad Request</h1>\r\n'
                contentLength = len(body)
                contentType = 'text/html'
                response.writeHeader('Content-Length', contentLength)
                response.writeHeader('Content-Type', contentType)
                response.setBody(body)
                response.send()
            else:
                contentType = request['Accept'] or request['Content-Type']
                if ',' in contentType:
                  contentType = contentType.split(',')
                  for mimeType in contentType:
                      if(mimeType in self.__mimetypes.values()):
                          self.handleRequest(request, connection)
                          break
                elif(not contentType or  contentType == '*/*' ):
                    self.handleRequest(request, connection)
                elif(not contentType in self.__mimetypes.values()):
                    response = Response.Response(connection)
                    response.setStatusCode(406)
                    response.writeHeader('Server', '{0}:{1}'.format(self.__host, self.__port)) 
                    body = '<h1>406 Not Acceptable</h1>\r\n'
                    contentLength = len(body)
                    contentType = 'text/html'
                    response.writeHeader('Content-Length', contentLength)
                    response.writeHeader('Content-Type', contentType)
                    response.setBody(body)
                    responseString = response.prepareResponseForSending()
                    response.send()
                else:
                    self.handleRequest(request, connection)'''
        return 0    
    def handleRequest(self, request, connection):
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
            return response.send406NotAcceptable()
        if(route != '/'):
            isValid = False
            resourceExtension = re.match('.*(\.[a-z]*)', route)
            if(not resourceExtension):
                return response.send406NotAcceptable()
            resourceExtension = resourceExtension.group(1)
            for mimeType in contentType:
                if(mimeType == self.__mimetypes[resourceExtension]):
                    isValid = True
                    break
            if(not isValid):
                print (contentType, self.__mimetypes[resourceExtension])
                return response.send406NotAcceptable()
        
        response.setStatusCode(200)
        return self.__router[method].get(route)(response)
        if(request['method'] == 'HEAD'):
            response = Response.Response(connection)
            response.setStatusCode(200)
            response.writeHeader('Server', '{0}:{1}'.format(self.__host, self.__port)) 
            body = '<p>Stuff</p>'
            contentLength = len(body)
            contentType = 'text/html'
            response.writeHeader('Content-Length', contentLength)
            response.writeHeader('Content-Type', contentType)
            responseString = response.prepareResponseForSending()
            response.send()
            return 0
#server = Server()
#server.initiateServer()
