import HttpServer
import signal
import sys
import Router
router = Router.Router()
def indexCallback(request, response):
    body = ''
    with open('index.html', 'rb') as indexHTML:
        body = indexHTML.read()
    indexHTML.close()
    contentType = 'text/html'
    response.writeHeader('Content-Type', contentType)
    response.setBody(body)
    return response.send()
def callback2(response):
    with open('chico.jpg', 'rb') as indexHTML:
        body = indexHTML.read()
    indexHTML.close()
    contentType = 'image/jpeg'
    response.writeHeader('Content-Type', contentType)
    response.setBody(body)
    return response.send()
router.get('/index.html', indexCallback)
router.get('/LogoSandia.jpg', callback2)
def gracefulShutdown(sig, dummy):
    httpServer.shutdownServer()
    return sys.exit(1)
signal.signal(signal.SIGINT, gracefulShutdown)
httpServer = HttpServer.HttpServer(router)
httpServer.initiateServer()
sys.exit(1)
