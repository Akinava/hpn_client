# -*- coding: utf-8 -*-
__author__ = 'Akinava'
__author_email__ = 'akinava@gmail.com'
__copyright__ = "Copyright © 2019"
__license__ = "MIT License"
__version__ = [0, 0]


from settings import logger


def server_run():
    logger.info('server start')
    logger.info('server shutdown')


if __name__ == '__main__':
    server_run()