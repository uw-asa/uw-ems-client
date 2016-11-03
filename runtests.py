import sys
import django
from django.conf import settings
from django.test.utils import get_runner


settings.configure(
    INSTALLED_APPS=('ems_client',),
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3'}},
    USE_TZ=True,
)


def runtests():
    django.setup()
    test_class = get_runner(settings)
    test_runner = test_class()
    failures = test_runner.run_tests(['ems_client'])
    sys.exit(bool(failures))

if __name__ == "__main__":
    runtests()
