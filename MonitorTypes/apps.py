from django.apps import AppConfig

import logging
logger = logging.getLogger(__name__)


class MonitorTypesConfig(AppConfig):
    name = 'MonitorTypes'

    def ready(self):
        logger.info("MonitorTypesConfig ready")
        from MonitorTypes.signal_processor import post_save_callback
