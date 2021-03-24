import os, time, datetime, logging, json, sys
import pipeclient

# create logger
logger = logging.getLogger('start-recording')
logger.setLevel(logging.DEBUG)

logDirectory = os.path.join(os.path.dirname(os.path.realpath (__file__)), 'logs')
timeNow = datetime.datetime.now()
logFileName = timeNow.strftime("%Y%m%d") + 'pipeclient.log'
logPath = os.path.join( logDirectory, logFileName)

# create file handler which logs even debug messages
fh = logging.FileHandler(logPath)
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

logger.info('Starting Pipeclient')
client = pipeclient.PipeClient()

logger.info('Getting Current Tracks')
client.write('getInfo: Type=Tracks')
while client.reply == '':
    time.sleep(0.1)

pipeJSON = client.read()
if ('' == pipeJSON): 
    logger.error('**********No response from Audactiy**********')
    # TODO:do something here to flag the issue
    sys.exit()
pipeJSON = pipeJSON[:pipeJSON.rfind('BatchCommand finished: OK')]
pipeResponse = json.loads(pipeJSON)

logger.info("JSON Response: " + pipeJSON)

if (len(pipeResponse) == 0):
    logger.info("No tracks found. Clear to proceed")
    # Start Recording on New Track
else:
    logger.info("Found " + str(len(pipeResponse)) + " existing track(s)")
    logger.debug("SelAllTracks")
    client.write('SelAllTracks:')
    while client.reply == '':
        time.sleep(0.1)
    logger.debug("Stop")
    client.write('Stop:')
    while client.reply == '':
        time.sleep(0.1)