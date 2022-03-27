import logging
import logging.config
import os

file_conf = os.path.join(os.path.dirname(__file__), 'logging.cfg')
logging.config.fileConfig(file_conf)
logger = logging.getLogger('tooy')
logger.info('inicio')
