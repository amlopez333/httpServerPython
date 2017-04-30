class Request:
    def __init__(self, httpRequest):
        self._request = self._processRequest(httpRequest)
    def _processRequest(self, httpRequest):
        decodedRequest = httpRequest.decode()
        requestString = decodedRequest.replace('\r\n', ' ').replace('\n\n', ' ').replace(':', '')
        requestArray = requestString.split(' ')
        requestDict = self._arrayToDict(requestArray)
        print(requestDict)
        return requestDict
    def _arrayToDict(self, array):
        requestDict = {}
        if(array[0] != ''):
            requestDict = {'method': array[0]}
            requestDict['route'] = array[1]
            requestDict['protocol'] = array[2]
            for i in range(3, len(array)-1, 2):
                requestDict[array[i]] = array[i + 1]
        return requestDict
    def __getitem__(self, key):
        return self._request.get(key)
    def keys(self):
        return self._request.keys()
    def values(self):
        return self._request.values()