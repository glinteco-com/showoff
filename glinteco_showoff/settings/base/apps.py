DJANGO_APPs = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
]

EXTERNAL_APPS = [
    "django_extensions",
    "django_filters",
    "easy_thumbnails",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "drf_standardized_errors",
    "drf_yasg",
    "django_celery_beat",
    "django_celery_results",
]

INTERNAL_APPS = [
    "learning.apps.LearningConfig",
]

INSTALLED_APPS = DJANGO_APPs + EXTERNAL_APPS + INTERNAL_APPS
