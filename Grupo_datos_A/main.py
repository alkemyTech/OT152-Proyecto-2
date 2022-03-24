import logging
import logging.config
import logging.handlers

logging.config.fileConfig('logging.cfg')
logger = logging.getLogger("main")
logger.info("start")
