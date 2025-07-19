#!/usr/bin/env python
"""
슬롯 생성 테스트 스크립트
"""
import os
import sys
import django

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rslot.settings')
django.setup()

from slots.models import Slot
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

def test_slot_creation():
    """슬롯 생성 테스트"""
    print("=== 슬롯 생성 테스트 ===")
    
    # 테스트용 사용자 가져오기 (admin 사용자 사용)
    try:
        user = User.objects.get(username='admin')
    except User.DoesNotExist:
        print("admin 사용자가 없습니다. 테스트를 중단합니다.")
        return
    
    print(f"테스트 사용자: {user.username}")
    
    # 기존 슬롯 수 확인
    initial_count = Slot.objects.count()
    print(f"테스트 전 슬롯 수: {initial_count}")
    
    try:
        # 새 슬롯 생성 (views.py의 slot_create 로직과 동일)
        slot = Slot(
            user=user,
            keyword='테스트 키워드',
            url='https://example.com/test'
        )
        # end_date를 30일 후로 설정 (fix 적용)
        slot.end_date = slot.start_date + timedelta(days=30)
        slot.save()
        
        print(f"슬롯 생성 성공!")
        print(f"슬롯 ID: {slot.id}")
        print(f"키워드: {slot.keyword}")
        print(f"URL: {slot.url}")
        print(f"시작일: {slot.start_date}")
        print(f"종료일: {slot.end_date}")
        print(f"생성일: {slot.created_at}")
        
        # 슬롯 수 확인
        final_count = Slot.objects.count()
        print(f"테스트 후 슬롯 수: {final_count}")
        print(f"생성된 슬롯 수: {final_count - initial_count}")
        
        # 생성된 슬롯 삭제 (테스트 정리)
        slot.delete()
        print("테스트 슬롯 삭제 완료")
        
    except Exception as e:
        print(f"슬롯 생성 중 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_slot_creation() 