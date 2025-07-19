#!/usr/bin/env python
"""
백링크 트래픽 시스템 테스트 스크립트
"""
import os
import sys
import django

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rslot.settings')
django.setup()

from slots.models import Slot, TrafficLog
from slots.backlink_system import BacklinkTrafficManager

def test_backlink_traffic():
    """백링크 트래픽 테스트"""
    print("=== 백링크 트래픽 시스템 테스트 ===")
    
    # 현재 슬롯 확인
    slots = Slot.objects.all()
    print(f"현재 슬롯 수: {slots.count()}")
    
    if not slots.exists():
        print("테스트할 슬롯이 없습니다.")
        return
    
    slot = slots.first()
    print(f"테스트 슬롯: ID={slot.id}, 키워드={slot.keyword}")
    
    # 현재 로그 수 확인
    initial_log_count = TrafficLog.objects.count()
    print(f"테스트 전 로그 수: {initial_log_count}")
    
    try:
        # 백링크 트래픽 매니저 생성
        manager = BacklinkTrafficManager()
        
        # 기본 백링크 트래픽 활성화 (1개만 테스트)
        print("\n=== 백링크 트래픽 활성화 시작 ===")
        success, message = manager.activate_backlink_traffic(slot.id, 'basic')
        
        print(f"활성화 결과: {success}")
        print(f"메시지: {message}")
        
        # 로그 확인
        final_log_count = TrafficLog.objects.count()
        print(f"\n테스트 후 로그 수: {final_log_count}")
        print(f"생성된 로그 수: {final_log_count - initial_log_count}")
        
        if final_log_count > initial_log_count:
            # 최근 로그 확인
            recent_logs = TrafficLog.objects.order_by('-created_at')[:3]
            print("\n=== 최근 생성된 로그 ===")
            for log in recent_logs:
                print(f"ID: {log.id}")
                print(f"시간: {log.created_at}")
                print(f"상태: {log.status}")
                print(f"트래픽 타입: {log.traffic_type}")
                print(f"소요 시간: {log.response_time}초")
                print(f"오류 메시지: {log.error_message}")
                print(f"중간 사이트: {log.intermediate_site}")
                print("---")
        else:
            print("로그가 생성되지 않았습니다.")
            
    except Exception as e:
        print(f"테스트 중 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_backlink_traffic() 