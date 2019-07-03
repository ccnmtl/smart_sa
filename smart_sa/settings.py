# flake8: noqa
from smart_sa.settings_shared import *
try:
    from smart_sa.local_settings import *
except ImportError:
    pass
