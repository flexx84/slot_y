#!/usr/bin/env python
import os
import sys
import django

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rslot.settings')
django.setup()

from django.contrib.auth.models import User

# 관리자 계정 생성
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("관리자 계정이 생성되었습니다:")
    print("사용자명: admin")
    print("비밀번호: admin123")
else:
    print("관리자 계정이 이미 존재합니다.") 