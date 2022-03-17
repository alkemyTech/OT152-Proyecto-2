import logging
import logging.config
logging.config.fileConfig('logging.cfg')
logger = logging.getLogger('gian')
logger.info('tets')
