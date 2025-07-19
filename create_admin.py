#!/usr/bin/env python
"""
관리자 계정 자동 생성 스크립트
Railway 배포 후 자동으로 실행됩니다.
"""

import os
import django

# Django 설정 초기화
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rslot.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin_user():
    """관리자 계정 생성"""
    try:
        # 기존 admin 계정이 있는지 확인
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            print("✅ 관리자 계정이 성공적으로 생성되었습니다!")
            print("   사용자명: admin")
            print("   비밀번호: admin123")
        else:
            print("ℹ️ 관리자 계정이 이미 존재합니다.")
            
        # 일반 사용자 계정도 생성
        if not User.objects.filter(username='user').exists():
            User.objects.create_user(
                username='user',
                email='user@example.com',
                password='user123'
            )
            print("✅ 일반 사용자 계정이 성공적으로 생성되었습니다!")
            print("   사용자명: user")
            print("   비밀번호: user123")
        else:
            print("ℹ️ 일반 사용자 계정이 이미 존재합니다.")
            
    except Exception as e:
        print(f"❌ 계정 생성 중 오류 발생: {e}")

if __name__ == '__main__':
    create_admin_user() 