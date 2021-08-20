# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

import dj_database_url 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pos',
        'USER': 'postgres',
        'PASSWORD': 'b1o2l3u4',
        'HOST': 'localhost',
    }
}

prod_db  =  dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(prod_db)