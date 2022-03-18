import logging
import logging.config
from decouple import config as cfg

logging.config.fileConfig(cfg('FILE_PATH'))
#logging.config.fileConfig('logging.cfg')
logger = logging.getLogger('root')
logger.info('inicio')
