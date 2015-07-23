#!/usr/bin/env python

import ConfigParser, os, requests, time

Config = ConfigParser.ConfigParser()
Config.read('config.ini')

filePath = os.path.realpath(Config.get('output', 'file'))

while True:
    r = requests.get(Config.get('api', 'url'), headers={
            'X-Api-Id': Config.get('api', 'id'),
            'X-Api-Key': Config.get('api', 'key')
        })

    if r.status_code == 404:
        try:
            response = r.json()

            # If response was not successful because of
            # an invalid API ID/Key, clear the file
            if not response['success']:
                file = open(filePath, 'w')
                file.truncate()
                file.close()
        except Exception, e:
            import logging
            logging.basicConfig(filename=Config.get('logs', 'filename'),level=logging.DEBUG)
            logging.debug('Something went wrong. Exiting.')
            pass
        finally:
            exit()
    elif r.status_code != requests.codes.ok:
        exit()

    # Open & clear target file
    file = open(filePath, 'w')
    file.truncate()

    # Add company & server group as a comment
    response = r.json()
    file.write('# ' + response['company'] + ' (' + response['group'] + ')\n')

    # Write users to file
    for user in response['users']:
        file.write(user['username'] + ':' + user['password'] + '\n')

    file.close()

    time.sleep(float(Config.get('wait', 'time')))
