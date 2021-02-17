import logging as log
from config.params import ap_params

if (ap_params['LOG_FILE']):
    log.basicConfig(filename=ap_params['LOG_FILE'], level=ap_params["LOG_LEVEL"])
else:
    log.basicConfig(level=ap_params["LOG_LEVEL"])
