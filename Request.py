from collections import OrderedDict
class Request:
    def __init__(self, httpRequest):
        self._request = self._processRequest(httpRequest)
    def _processRequest(self, httpRequest):
        decodedRequest = httpRequest.decode()
        print(decodedRequest)
        requestString = decodedRequest.replace('\n\n', '\r\n')
        requestArray = requestString.split('\r\n')
        requestDict = self._arrayToDict(requestArray)
        print(requestDict)
        return requestDict
    def _arrayToDict(self, array):
        requestDict = OrderedDict()
        if(array[0] != ''):
            method, route, protocol = array[0].split(' ')
            requestDict['method'] = method
            requestDict['route'] = route
            requestDict['protocol'] = protocol
        for i in range(1, len(array)-2, 1):
            headerValue = array[i].split(':', 1)
            header, value = headerValue[0], headerValue[1].lstrip()
            requestDict[header] = value
        return requestDict
    def __getitem__(self, key):
        return self._request.get(key)
    def keys(self):
        return self._request.keys()
    def values(self):
        return self._request.values()
