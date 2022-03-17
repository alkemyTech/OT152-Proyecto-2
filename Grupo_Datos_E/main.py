from decouple import config
import logging
from logging.config import fileConfig

cfg_logging = config('CFG_PATH')

fileConfig(cfg_logging)

logger = logging.getLogger('log_datos_e')
