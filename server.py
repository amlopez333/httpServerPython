import socket
import signal
import time
import mimetypes
class Request:
    def __init__(self, httpRequest):
        self._request = self._processRequest(httpRequest)
        self._keys = self._request.keys()
    def _processRequest(self, httpRequest):
        decodedRequest = httpRequest.decode()
        requestString = decodedRequest.replace('\r\n', ' ').replace('\n\n', ' ').replace(':', '')
        requestArray = requestString.split(' ')
        requestDict = self._arrayToDict(requestArray)
        return requestDict
    def _arrayToDict(self, array):
        requestDict = {'method': array[0]}
        requestDict['route'] = array[1]
        requestDict['protocol'] = array[2]
        for i in range(3, len(array)-1, 2):
            requestDict[array[i]] = array[i + 1]
        return requestDict
    def __getitem__(self, key):
        if(not key in self._keys):
            return None
        return self._request[key]
    def keys(self):
        return self._keys
    def values(self):
        return self._request.values()

class Response:
    _statusCodes = {
                    200: '200 OK',
                    201: '201 Created',
                    400: '400 Bad Request',
                    404: '404 Not Found',
                    406: '406 Not Acceptable',
                    500: '500 Internal Server Error',
                    501: '501 Not Implemented'
    }
    def __init__(self):
        currentDate = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        self._response = {'headers': {'protocol': 'HTTP/1.1', 'statusCode': '',
                                      'Date': 'Date: {}'.format(currentDate) },
                          'body': ''}
    def __setitem__(self, key, value):
        self._response[key] = value
    def __getitem__(self, key):
        return self._response[key]
    def keys(self):
        return self._response.keys()
    def setStatusCode(self, statusCode):
        self._response['headers']['statusCode'] = self._statusCodes[statusCode]
    def setBody(self, bodyContent):
        self._response['body'] = bodyContent
    def writeHeader(self, header, content):
        self._response['headers'][header] = '{0}: {1}'.format(header, str(content))
    def prepareResponseForSending(self, sendBody = True):
        responseHeaders = '\r\n'.join(self._response['headers'].values()).replace('\r\n', ' ', 1) + '\r\n\n\n'
        responseString = responseHeaders
        if(sendBody):
            responseString += self._response['body']
        return responseString.encode()
class Server:
    def __init__(self, port = 8080):
        self._host = '127.0.0.1'
        self._port = port
        mimetypes.init()
        self._mimetypes = mimetypes.types_map
        self._mimetypes['.webp']='image/webp'
    def initiateServer(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Initiating HTTP server on {0}:{1}'.format(self._host, self._port))
        server_address = (self._host, self._port)
        self.socket.bind(server_address)
        self.listenForever()
    def listenForever(self):
        while True:
            self.socket.listen(5)
            print('HTTP server listenting on {0}:{1}'.format(self._host, self._port))
            connection, address = self.socket.accept()
            data = connection.recv(1024)
            print(bytes.decode(data))
            request = Request(data)        
            print(request.values())
            if(not 'Host' in request.keys()):
                response = Response()
                response.setStatusCode(400)
                response.writeHeader('Server', '{0}:{1}'.format(self._host, self._port)) 
                body = '<h1>400 Bad Request</h1>\r\n'
                contentLength = len(body)
                contentType = 'text/html'
                response.writeHeader('Content-Length', contentLength)
                response.writeHeader('Content-Type', contentType)
                response.setBody(body)
                responseString = response.prepareResponseForSending()
                connection.send(responseString)
                print(responseString)
                connection.close()
            else:
                contentType = request['Accept'] or request['Content-Type']
                if ',' in contentType:
                  contentType = contentType.split(',')
                  for mimeType in contentType:
                      if(mimeType in self._mimetypes.values()):
                          self.handleRequest(request, connection)
                          break
                elif(not contentType or '*/*' == contentType):
                    self.handleRequest(request, connection)
                elif(not contentType in self._mimetypes.values()):
                    response = Response()
                    response.setStatusCode(406)
                    response.writeHeader('Server', '{0}:{1}'.format(self._host, self._port)) 
                    body = '<h1>406 Not Acceptable</h1>\r\n'
                    contentLength = len(body)
                    contentType = 'text/html'
                    response.writeHeader('Content-Length', contentLength)
                    response.writeHeader('Content-Type', contentType)
                    response.setBody(body)
                    responseString = response.prepareResponseForSending()
                    connection.send(responseString)
                    print(responseString)
                    connection.close()
                else:
                    self.handleRequest(request, connection)
    def handleRequest(self, request, connection):
        if(request['method'] == 'GET'):
            response = Response()
            response.setStatusCode(200)
            response.writeHeader('Server', '{0}:{1}'.format(self._host, self._port)) 
            body = '<p>Stuff</p>\r\n'
            contentLength = len(body)
            contentType = 'text/html'
            response.writeHeader('Content-Length', contentLength)
            response.writeHeader('Content-Type', contentType)
            response.setBody(body)
            responseString = response.prepareResponseForSending()
            connection.send(responseString)
            print(responseString)
            connection.close()
        elif(request['method'] == 'HEAD'):
            response = Response()
            response.setStatusCode(200)
            response.writeHeader('Server', '{0}:{1}'.format(self._host, self._port)) 
            body = '<p>Stuff</p>'
            contentLength = len(body)
            contentType = 'text/html'
            response.writeHeader('Content-Length', contentLength)
            response.writeHeader('Content-Type', contentType)
            responseString = response.prepareResponseForSending()
            connection.send(responseString)
            print(responseString.decode())
            connection.close()
    
server = Server()
server.initiateServer()
