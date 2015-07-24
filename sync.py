#!/usr/bin/env python

try:
    import json
except:
    import simplejson as json

import ConfigParser
import httplib
import logging
import os
import time
import urlparse

Config = ConfigParser.ConfigParser()
Config.read(os.path.dirname(os.path.abspath(__file__))+'/config.ini')

logging.basicConfig(
    filename=Config.get('logs', 'filename'),
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG)

filePath = os.path.realpath(Config.get('output', 'file'))

def callHome():
    url = Config.get('api', 'url')
    url = urlparse.urlparse(Config.get('api', 'url'))

    if url.scheme == 'https':
        h = httplib.HTTPSConnection(url.netloc, timeout=30)
    else:
        h = httplib.HTTPConnection(url.netloc, timeout=30)

    h.request('GET', '/api/users', '', {
            'X-Api-Id': Config.get('api', 'id'),
            'X-Api-Key': Config.get('api', 'key')
        })

    return h.getresponse()

def wait():
    time.sleep(float(Config.get('wait', 'time')))

while True:

    try:
        logging.debug('Start circle...')
        r = callHome()
        response = r.read()

        # If response was not successful because of
        # an invalid API ID/Key, clear the file
        if r.status == 403:
            logging.debug('Invalid credentials, clearing file')

            file = open(filePath, 'w')
            file.truncate()
            file.close()

            wait()
            continue

        elif r.status != 200:
            logging.debug(r.reason)
            wait()
            continue

    except Exception as e:
        logging.debug(e)
        wait()
        continue

    # Open & clear target file
    file = open(filePath, 'w')
    file.truncate()

    # Add company & server group as a comment
    try:
        data = json.loads(response)
    except ValueError as e:
        logging.debug(e)
        wait()
        continue

    file.write('# ' + data['company'] + ' (' + data['group'] + ')\n')

    # Write users to file
    for user in data['users']:
        file.write(user['username'] + ':' + user['password'] + '\n')

    file.close()

    wait()
