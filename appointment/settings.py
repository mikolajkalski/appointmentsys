

from django.conf import settings
from django.conf.global_settings import DEFAULT_FROM_EMAIL

from appointment.logger_config import get_logger

logger = get_logger(__name__)

APPOINTMENT_BASE_TEMPLATE = getattr(settings, 'APPOINTMENT_BASE_TEMPLATE', 'base_templates/base.html')
APPOINTMENT_ADMIN_BASE_TEMPLATE = getattr(settings, 'APPOINTMENT_ADMIN_BASE_TEMPLATE', 'base_templates/base.html')
APPOINTMENT_WEBSITE_NAME = getattr(settings, 'APPOINTMENT_WEBSITE_NAME', 'Website')
APPOINTMENT_PAYMENT_URL = getattr(settings, 'APPOINTMENT_PAYMENT_URL', None)
APPOINTMENT_THANK_YOU_URL = getattr(settings, 'APPOINTMENT_THANK_YOU_URL', None)
APPOINTMENT_SLOT_DURATION = getattr(settings, 'APPOINTMENT_SLOT_DURATION', 30)
APPOINTMENT_BUFFER_TIME = getattr(settings, 'APPOINTMENT_BUFFER_TIME', 0)
APPOINTMENT_LEAD_TIME = getattr(settings, 'APPOINTMENT_LEAD_TIME', (9, 0))
APPOINTMENT_FINISH_TIME = getattr(settings, 'APPOINTMENT_FINISH_TIME', (18, 30))
APP_DEFAULT_FROM_EMAIL = getattr(settings, 'DEFAULT_FROM_EMAIL', DEFAULT_FROM_EMAIL)


def check_q_cluster(hide_warning: bool = False):
    """
    Checks if Django Q is properly installed and configured in the Django settings.
    If 'django_q' is not in INSTALLED_APPS, it warns about both 'django_q' not being installed
    and 'Q_CLUSTER' likely not being configured.
    If 'django_q' is installed but 'Q_CLUSTER' is not configured, it only warns about 'Q_CLUSTER'.
    Returns True if configurations are correct, otherwise False.
    """
    missing_conf = []
    if not hide_warning:
        logger.info("Checking missing configuration for django q cluster")
    # Check if Django Q is installed
    if 'django_q' not in settings.INSTALLED_APPS:
        missing_conf.append("Django Q is not in settings.INSTALLED_APPS. Please add it to the list. "
                            "See https://django-appt-doc.adamspierredavid.com/getting-started/#installation "
                            "for more information")

    # Check if Q_CLUSTER configuration is defined
    if not hasattr(settings, 'Q_CLUSTER'):
        missing_conf.append("Q_CLUSTER is not defined in settings. Please define it. "
                            "See https://django-appt-doc.adamspierredavid.com/project-structure/#configuration "
                            "for more information.")

    # Log warnings if any configurations are missing
    if missing_conf and not hide_warning:
        for warning in missing_conf:
            logger.warning(warning)
        return False
    # Both 'django_q' is installed and 'Q_CLUSTER' is configured
    if not hide_warning:
        logger.info("Django Q cluster is properly configured")
    return True
