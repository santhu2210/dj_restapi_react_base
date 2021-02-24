import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'user_mng_dev',
        'USER': 'devuser',
        'PASSWORD': 'Welcome123',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

USE_TOKEN = True

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'log_dir')


