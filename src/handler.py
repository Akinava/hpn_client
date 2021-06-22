# -*- coding: utf-8 -*-
__author__ = 'Akinava'
__author_email__ = 'akinava@gmail.com'
__copyright__ = 'Copyright © 2019'
__license__ = 'MIT License'
__version__ = [0, 0]


import sys
from settings import logger
from crypt_tools import Tools as CryptTools
from connection import Connection, NetPool
from package_parser import Parser
from utilit import encode


class Handler:
    def __init__(self, protocol, message=None):
        logger.info('')
        self.net_pool = NetPool()
        self.crypt_tools = CryptTools()
        self.response = message
        self.transport = None
        self.protocol = protocol
        self.parser = Parser(protocol)

    def connection_made(self, transport):
        logger.info('')
        self.transport = transport

    def datagram_received(self, request, remote_addr):
        logger.info('request %s from %s' % (request, remote_addr))
        connection = Connection()
        connection.datagram_received(request, remote_addr, self.transport)
        self.net_pool.save_connection(connection)
        self.__handle(connection)

    def connection_lost(self, remote_addr):
        logger.info('')

    def make_connection(self, remote_host, remote_port):
        connection = Connection(transport=self.transport, remote_addr=(remote_host, remote_port))
        self.net_pool.save_connection(connection)
        return connection

    def __send_request(self, connection, request):
        request = encode(request)
        connection.send(request)

    def __handle(self):
        logger.debug('')
        # TODO make a tread
        package_protocol = self.__define_package()
        self.parser.set_package_protocol(package_protocol)
        logger.info('GeneralProtocol function defined as {}'.format(package_protocol['name']))
        if package_protocol is None:
            return
        response_function = self.__get_response_function(package_protocol)
        return response_function()

    def __define_package(self):
        logger.debug('')
        for package_protocol in self.protocol['package']:
            if self.__define_request(package_protocol):
                return package_protocol
        logger.warn('GeneralProtocol can not define request')

    def __define_request(self, package_protocol):
        define_protocol_functions = self.__get_define_protocol_functions(package_protocol)
        for define_func_name in define_protocol_functions:
            define_func = getattr(self, define_func_name)
            if not define_func(package_protocol) is True:
                return False
        return True

    def __get_define_protocol_functions(self, package_protocol):
        define_protocol_functions = package_protocol['define']
        if isintance(define_protocol_functions, list):
            return define_protocol_functions
        return [define_protocol_functions]

    def __get_response_function(self, request_protocol):
        logger.info('GeneralProtocol response_name {}'.format(request_protocol['name']))
        response_function_name = request_protocol.get('response')
        if response_function_name in None:
            logger.info('GeneralProtocol no response_function_name')
        logger.info('GeneralProtocol response_function_name {}'.format(response_function_name))
        return getattr(self, response_function_name)

    def make_message(self, **kwargs):
        message = b''
        package_structure = self.protocol['packages'][kwargs['package_name']]['structure']
        for part_structure in package_structure:
            if part_structure.get('type') == 'markers':
                build_part_message_function = self.get_markers
                kwargs['markers'] = part_structure
            else:
                build_part_message_function = getattr(self, 'get_{}'.format(part_structure['name']))
            message += build_part_message_function(**kwargs)
        return message

    def define_swarm_ping(self, connection):
        if connection.get_request() == msg_ping:
            return True
        return False

    def do_swarm_ping(self, connection):
        connection.send(b'')