import logging
import logging.config

logging.config.fileConfig('logging.cfg')
logger = logging.getLogger('root')
logger.info('inicio')
