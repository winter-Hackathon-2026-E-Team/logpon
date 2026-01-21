# 「開発」環境変数の読み込みファイル base.pyをimportして差分だけを記述
from .base import *

DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',')

MATTERMOST_WEBHOOK_URL = "https://chat.raretech.site/hooks/y9maqimxapdybrg65p3hu8ix7o"
