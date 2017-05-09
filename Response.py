import time
from collections import OrderedDict
class Response:
    _statusCodes = {
                    200: '200 OK',
                    201: '201 Created',
                    400: '400 Bad Request',
                    404: '404 Not Found',
                    405: '405 Method Not Allowed',
                    406: '406 Not Acceptable',
                    500: '500 Internal Server Error',
                    503: '503 Not Implemented'
    }
    def __init__(self, connection, host, port):
        currentDate = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        orderedDict = OrderedDict()
        orderedDict['protocol'] = 'HTTP/1.1'
        orderedDict['statusCode'] = ''
        orderedDict['Date'] = 'Date: {}'.format(currentDate)
        orderedDict['Server'] = 'Server: {0}:{1}'.format(host, port)
        orderedDict['Content-Length'] = {}
        orderedDict['Content-Type'] = {}
        self.__response = {'headers': orderedDict,
                          'body': ''}
        self.__connection = connection
    def __setitem__(self, key, value):
        self.__response[key] = value
    def __getitem__(self, key):
        return self.__response.get(key)
    def keys(self):
        return self.__response.keys()
    def setStatusCode(self, statusCode):
        self.__response['headers']['statusCode'] = self._statusCodes[statusCode]
    def setBody(self, bodyContent):
        self.__response['body'] = bodyContent
    def writeHeader(self, header, content):
        self.__response['headers'][header] = '{0}: {1}'.format(header, str(content))
    def __prepareResponseForSending(self, sendBody):
        contentLength = len(self.__response['body'])
        self.__response['headers']['Content-Length'] = 'Content-Length: {}'.format(str(contentLength))
        self.__response['headers']['Connection'] = 'Connection: close'
        responseHeaders = '\r\n'.join(self.__response['headers'].values()).replace('\r\n', ' ', 1) + '\r\n\r\n'
        responseString = responseHeaders
        responseString = responseString.encode()
        if(sendBody):
            responseString += self.__response['body']
        return responseString
    def send(self, sendBody = True):
        responseString = self.__prepareResponseForSending(sendBody)
        self.__connection.send(responseString)
        return self.__connection.close()
    '''Default handler for 400 error'''
    def send400BadRequest(self):
        self.setStatusCode(400)
        body = '<h1>400 Bad Request</h1>\r\n'
        contentType = 'text/html'
        self.writeHeader('Content-Type', contentType)
        self.setBody(body.encode())
        return self.send()
    '''Default handler for 404 error'''
    def send404NotFound(self):
        self.setStatusCode(404)
        body = '<h1>404 Not Found</h1>\r\n'
        contentType = 'text/html'
        self.writeHeader('Content-Type', contentType)
        self.setBody(body.encode())
        return self.send()
    '''Default handler for 406 error'''
    def send406NotAcceptable(self):
        self.setStatusCode(406)
        body = '<h1>406 Not Acceptable</h1>\r\n'
        contentType = 'text/html'
        self.writeHeader('Content-Type', contentType)
        self.setBody(body.encode())
        return self.send()
    '''Default handler for 405 error'''
    def send405MethodNotAllowed(self):
        self.setStatusCode(405)
        body = '<h1>405 Method Not Allowed</h1>\r\n'
        contentType = 'text/html'
        self.writeHeader('Content-Type', contentType)
        self.setBody(body.encode())
        return self.send()
    '''Default handler for 500 error'''
    def send500InternalServerError(self):
        self.setStatusCode(500)
        body = '<h1>500 Internal Server Error</h1>\r\n'
        contentType = 'text/html'
        self.writeHeader('Content-Type', contentType)
        self.setBody(body.encode())
        return self.send()
    '''Default handler for 503 error'''
    def send503NotImplemented(self):
        self.setStatusCode(503)
        body = '<h1>503 Not Implemented</h1>\r\n'
        contentType = 'text/html'
        self.writeHeader('Content-Type', contentType)
        self.setBody(body.encode())
        return self.send()
