import logging
import logging.config

from decouple import config

cfg_logging = config('CFG_PATH')

logging.config.fileConfig(cfg_logging)

logger = logging.getLogger('log_datos_e')
