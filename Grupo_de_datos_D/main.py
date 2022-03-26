import logging.config
import os

LOGGING_CONF = os.path.join(os.path.dirname(__file__), 'logging.cfg')
logging.config.fileConfig(LOGGING_CONF)
logger = logging.getLogger("Grupo_de_datos_D")
