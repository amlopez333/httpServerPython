import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import HttpServer
import signal
import sys
import Router
#Defines callbacks for routes.
#Routes are as follow:
#get -> /index.html
#get -> /logosandia.jpg
#head -> /index.html
#post -> /index.html
#ANY OTHER ROUTES WILL GIVE ERROR!!!!!!!

print('Test Server v0.5')
print('Routes defined are as follow: ')
print('GET -> /index.html')
print('GET -> /logosandia.jpg')
print('HEAD -> /index.html')
print('POST -> /index.html')
print('ANY OTHER ROUTES WILL GIVE ERROR')
print('------------------------------')
print('Creating Router...')
#Creates router
router = Router.Router()
#defines callbacks
print('Defining callbacks...')
def indexCallback(request, response):
    body = ''
    with open('index.html', 'rb') as indexHTML:
        body = indexHTML.read()
    indexHTML.close()
    contentType = 'text/html'
    response.writeHeader('Content-Type', contentType)
    response.setBody(body)
    return response.send()
def logoSandiaCallback(request, response):
    with open('chico.jpg', 'rb') as image:
        body = image.read()
    image.close()
    contentType = 'image/jpeg'
    response.writeHeader('Content-Type', contentType)
    response.setBody(body)
    return response.send()
def indexHeadCallback(request, response):
    body = ''
    with open('index.html', 'rb') as indexHTML:
        body = indexHTML.read()
    indexHTML.close()
    contentType = 'text/html'
    response.writeHeader('Content-Type', contentType)
    response.setBody(body)
    return response.send(sendBody = False)
def indexPostCallback(request, response):
    reqBody = request['body']
    body = '<p> The post values are: {}</p>'.format(reqBody).encode()
    contentType = 'text/html'
    response.writeHeader('Content-Type', contentType)
    response.setBody(body)
    return response.send()
#register callbacks
print('Registering callbacks...')
router.get('/', indexCallback)
router.get('/index.html', indexCallback)
router.get('/logosandia.jpg', logoSandiaCallback)
router.head('/index.html', indexHeadCallback)
router.post('/index.html', indexPostCallback)
def gracefulShutdown(sig, dummy):
    httpServer.shutdownServer()
    return sys.exit(1)
signal.signal(signal.SIGINT, gracefulShutdown)
httpServer = HttpServer.HttpServer(router)
httpServer.initiateServer()
sys.exit(1)
