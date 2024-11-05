

from pathlib import Path
import os

# ###########################################################################################################
# Preciso configurar a nova base de dados no 'https://dashboard.sqlitecloud.io/projects/cby0ni6znk/nodes' 
# pois no render nao esta salvando os dados por causa do plano.
# entao abaixo esta a configuração da conexão da base de dados
# verificar o link -> 'https://chatgpt.com/g/g-HxPrv1p8v-code-tutor/c/67297721-7788-800d-9c1e-5b8c4ddf51f4'

# ou jogar esse texto no gpt 
# o meu banco de dados em sqlite3 esta em minha aplicação no render.com, porem preciso colocar ela no https://docs.sqlitecloud.io/docs/connect-cluster para guardar as informações. Estou usando python3 com Django e a estruturação de pastas esta essa no print acima. porem preciso separar o banco de dados da aplicação, como faço isso?

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',  # ou outro backend se necessário
#         'NAME': 'System-estoque',  # nome do seu banco no SQLiteCloud
#         'USER': 'Arthur',                    # seu usuário do SQLiteCloud
#         'PASSWORD': '08102004Mg!',                  # sua senha do SQLiteCloud
#         'HOST': 'host_sqlitecloud.com',           # URL ou IP do host do SQLiteCloud
#         'PORT': 'porta_necessaria',               # porta se for necessária
#     }
# }

# ###########################################################################################################

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_jjoltkqc&fmn)m2+!q!9l+@6m%b3i+#v8z98(79=tminxhyc8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS
ALLOWED_HOSTS = ['.onrender.com', 'localhost']

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = ['https://sistema-de-estoque-sq8r.onrender.com']

#PARA RODAR LOCALMENTE
#ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
#CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1', 'http://localhost']


STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app' #PASSO 01 - COLOCAR O NOME PARA O DJANGO INTENDER O PROJETO
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'  # URL onde os arquivos estáticos são servidos

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] 

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
