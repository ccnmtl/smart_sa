from settings_shared import *
TEMPLATE_DIRS = (
    "C:/Users/CCNMTLSTAFF/Downloads/smart_sa/templates/",
)

MEDIA_ROOT = 'C:/Users/CCNMTLSTAFF/Downloads/smart_sa/uploads/'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

INTERVENTION_BACKUP_HEXKEY = "d37fb81dff7672c76f4881a8f57c002403ba2ce5155dc4ac6b68a2d9caa51d88"
INTERVENTION_BACKUP_IV = "899f6762313185a9593480e6f015b0d5053464daa5ecadd00dc4e7e2984f028f"

DISABLE_OFFLINE=True

DATABASE_ENGINE = 'sqlite3' # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'masivukeni.sqlite' # Or path to database file if using sqlite3.

try:
    from local_settings import *
except ImportError:
    pass
