import logging

import logging.config

from decouple import config as cfg

# Load logging configurations
logging.config.fileConfig(cfg('FILE_PATH'))
# Instansiate logger class
logger = logging.getLogger('Grupo_Datos_G')
