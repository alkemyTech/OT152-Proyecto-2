import logging.config
from decouple import config as cfg

# Loading logging configuration file
logging.config.fileConfig(cfg('LOG_PATH'))

# Create Logger
logger = logging.getLogger('Grupo_Datos_F')