class Router:
    def __init__(self):
        self.__routes = {'GET': {},
                         'HEAD': {},
                         'POST': {}}
        self.__knownMethods = ['TRACE', 'DELETE', 'PUT']
        self.__defaultGet()
    '''defines routes for GET method. 
    callback should be a function that takes request and response
    as params. response.send() needs to be called at end of callback.'''    
    def get(self, route, callback):
        self.__routes['GET'][route] = callback
    '''defines routes for HEAD method. 
    callback should be a function that takes request and response
    as params. response.send() needs to be called at end of callback.''' 
    def head(self, route, callback):
        self.__routes['HEAD'][route] = callback
    '''defines routes for POST method. 
    callback should be a function that takes request and response
    as params. response.send() needs to be called at end of callback.''' 
    def post(self, route, callback):
        self.__routes['POST'][route] = callback
    '''sets the default callback for GET request with URI = /'''
    def __defaultGetCallback(self, request, response):
        body = '<h1>ESTE ES EL SERVIDOR LOCAL DE LA CASA LOPEZ URENA</h1>\r\n'
        contentType = 'text/html'
        response.writeHeader('Content-Type', contentType)
        #response.writeHeader('Connection', 'close')
        response.setBody(body.encode())
        return response.send()
    def __defaultGet(self):
        self.__routes['GET']['/'] = self.__defaultGetCallback
    def __getitem__(self, key):
        return self.__routes.get(key)
    def getKeys(self):
        return self.__routes.keys
    def getKnownMethods(self):
        return self.__knownMethods

