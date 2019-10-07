#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time


__author__ = 'Akinava'
__author_email__ = 'akinava@gmail.com'
__copyright__ = "Copyright © 2019"
__license__ = "MIT License"
__version__ = [0, 0]


test_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(test_dir, '../src')
sys.path.append(src_dir)
import host
import sstn
import settings
from settings import logger


# TODO test case sstn server shutdown
# TODO test case sstn fingerprint is wrong
# TODO test case peers connect to sstn, peers shutdown, peers connect again

class Handler:
    def __init__(self, interface):
        self.__sctn = sstn.SignalClientHandler(interface, self)
        self.__interface = interface

    def handle_request(self, msg, connection):
        logger.debug('Handler.handle_request')
        # do something
        logger.info('swarm peer {} message {} bytes from connection {}'.format(self.__interface._default_listener_port(), len(msg), connection))

    def send(self, msg, connection):
        logger.debug('Handler.send')
        self.__interface.send(msg, connection)

    def close(self):
        self.__sctn.close()
        logger.info('Handrel close')


def rm_peers():
    if os.path.isfile(settings.peers_file):
        os.remove(settings.peers_file)


def stop_thread(server_thread):
    server_thread._tstate_lock = None
    server_thread._stop()


def get_fingerprint(self):
    return self.__handler.get_fingerprint()


if __name__ == "__main__":
    logger.info('start test')

    # run SS0
    peers = []
    last_peer = -1

    '''
    # run SSTN
    signal_server_0 = host.UDPHost(handler=sstn.SignalServerHandler, host='', port=10002)
    signal_server_0.get_fingerprint = get_fingerprint
    peers.append(signal_server_0)
    # save fingerprint to peers
    if not os.path.isfile(settings.peers_file):
        settings.add_peer(
            {'ip': '127.0.0.1',
             'port': 10002,
             'fingerprint': signal_server_0.get_fingerprint(),
             'signal': True})
    '''

    # run NP
    for port in range(10003, 10005):
        peers.append(host.UDPHost(handler=Handler, host='', port=port))

    while not peers[last_peer].is_ready():
        time.sleep(0.1)
    logger.info('the last peer has connect with swarm')

    # print ('test: lost connection with peer', peers[1]._default_listener_port())
    # peers[last_peer].stop()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        pass

    for h in peers:
        h.stop()

    # rm_peers()
    logger.info('end test')
