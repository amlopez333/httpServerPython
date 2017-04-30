import HttpServer
import signal
import sys
import Router
router = Router.Router()
def callback(response):
    body = '<p>Stuff</p>\r\n'
    contentType = 'text/html'
    response.writeHeader('Content-Type', contentType)
    response.setBody(body)
    response.send()
router.get('/index.html', callback)
def gracefulShutdown(sig, dummy):
    httpServer.shutdownServer()
    sys.exit(1)
signal.signal(signal.SIGINT, gracefulShutdown)
httpServer = HttpServer.Server(router)
httpServer.initiateServer()
sys.exit(1)
