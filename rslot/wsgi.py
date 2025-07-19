"""
WSGI config for rslot project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import subprocess
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rslot.settings')

# Railway에서 자동으로 마이그레이션 실행
def run_migrations():
    try:
        print("🔄 마이그레이션 실행 중...")
        subprocess.run([sys.executable, 'manage.py', 'makemigrations'], check=True)
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
        print("✅ 마이그레이션 완료!")
        
        # 관리자 계정 생성
        print("🔄 관리자 계정 생성 중...")
        subprocess.run([sys.executable, 'create_admin.py'], check=True)
        print("✅ 관리자 계정 생성 완료!")
    except Exception as e:
        print(f"⚠️ 마이그레이션 오류: {e}")

# 앱 시작 시 마이그레이션 실행
run_migrations()

application = get_wsgi_application() 