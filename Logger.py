
import json
class Logger:
    def __init__(self):
        super()
    def log(self, values):
        with open('log.txt', 'a+') as logFile:
            jsonString = json.dumps(values, indent = 4, separators = (',', ': '))
            logFile.write(jsonString + ',\n')
        logFile.close()
