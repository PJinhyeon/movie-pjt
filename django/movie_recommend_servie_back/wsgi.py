"""
WSGI config for movie_recommend_servie_back project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.conf import settings

from django.core.wsgi import get_wsgi_application

# 환경 변수로 인증 파일 경로 설정
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = settings.GOOGLE_CLOUD_CREDENTIALS

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_recommend_servie_back.settings')

application = get_wsgi_application()
