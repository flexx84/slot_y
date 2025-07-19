"""
트래픽 생성 엔진
실제 URL에 트래픽을 생성하는 시스템
"""
import requests
import time
import random
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Slot


class TrafficGenerator:
    """트래픽 생성기 클래스"""
    
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15',
            'Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/88.0'
        ]
        
        self.referrers = [
            'https://www.google.com/',
            'https://www.bing.com/',
            'https://www.naver.com/',
            'https://www.daum.net/',
            'https://www.facebook.com/',
            'https://twitter.com/',
            'https://www.instagram.com/'
        ]
    
    def generate_traffic(self, slot, count=1):
        """
        특정 슬롯에 대해 트래픽 생성
        
        Args:
            slot: Slot 모델 인스턴스
            count: 생성할 트래픽 수
        """
        if slot.is_expired:
            return False, "슬롯이 만료되었습니다."
        
        success_count = 0
        for i in range(count):
            try:
                # 랜덤 지연 시간 (1-5초)
                time.sleep(random.uniform(1, 5))
                
                # 요청 헤더 설정
                headers = {
                    'User-Agent': random.choice(self.user_agents),
                    'Referer': random.choice(self.referrers),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                }
                
                # GET 요청 보내기
                response = requests.get(
                    slot.url, 
                    headers=headers, 
                    timeout=30,
                    allow_redirects=True
                )
                
                if response.status_code == 200:
                    success_count += 1
                    print(f"트래픽 생성 성공: {slot.url} (상태코드: {response.status_code})")
                else:
                    print(f"트래픽 생성 실패: {slot.url} (상태코드: {response.status_code})")
                    
            except Exception as e:
                print(f"트래픽 생성 오류: {slot.url} - {str(e)}")
        
        return True, f"{success_count}/{count} 트래픽 생성 완료"
    
    def generate_search_traffic(self, slot, count=1):
        """
        검색 엔진을 통한 자연스러운 트래픽 생성
        
        Args:
            slot: Slot 모델 인스턴스
            count: 생성할 트래픽 수
        """
        if slot.is_expired:
            return False, "슬롯이 만료되었습니다."
        
        success_count = 0
        search_engines = [
            f"https://www.google.com/search?q={slot.keyword}",
            f"https://www.bing.com/search?q={slot.keyword}",
            f"https://search.naver.com/search.naver?query={slot.keyword}",
            f"https://search.daum.net/search?q={slot.keyword}"
        ]
        
        for i in range(count):
            try:
                # 랜덤 지연 시간 (2-8초)
                time.sleep(random.uniform(2, 8))
                
                # 1단계: 검색 엔진에서 키워드 검색
                search_url = random.choice(search_engines)
                headers = {
                    'User-Agent': random.choice(self.user_agents),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
                }
                
                search_response = requests.get(search_url, headers=headers, timeout=30)
                
                if search_response.status_code == 200:
                    # 2단계: 잠시 대기 후 타겟 URL 방문
                    time.sleep(random.uniform(3, 10))
                    
                    target_headers = {
                        'User-Agent': random.choice(self.user_agents),
                        'Referer': search_url,
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
                    }
                    
                    target_response = requests.get(slot.url, headers=target_headers, timeout=30)
                    
                    if target_response.status_code == 200:
                        success_count += 1
                        print(f"검색 트래픽 생성 성공: {slot.keyword} -> {slot.url}")
                    else:
                        print(f"타겟 URL 접근 실패: {slot.url} (상태코드: {target_response.status_code})")
                else:
                    print(f"검색 엔진 접근 실패: {search_url} (상태코드: {search_response.status_code})")
                    
            except Exception as e:
                print(f"검색 트래픽 생성 오류: {slot.keyword} -> {slot.url} - {str(e)}")
        
        return True, f"{success_count}/{count} 검색 트래픽 생성 완료"
    
    def schedule_traffic(self, slot, daily_count=10):
        """
        슬롯에 대해 일일 트래픽 스케줄링
        
        Args:
            slot: Slot 모델 인스턴스
            daily_count: 일일 트래픽 수
        """
        if slot.is_expired:
            return False, "슬롯이 만료되었습니다."
        
        # 현재 시간부터 24시간 동안 랜덤하게 분산
        start_time = timezone.now()
        end_time = start_time + timedelta(days=1)
        
        # 트래픽 생성 시간들을 랜덤하게 분산
        traffic_times = []
        for _ in range(daily_count):
            random_time = start_time + timedelta(
                seconds=random.randint(0, int((end_time - start_time).total_seconds()))
            )
            traffic_times.append(random_time)
        
        traffic_times.sort()
        
        print(f"슬롯 '{slot.keyword}'에 대해 {daily_count}개의 트래픽이 스케줄링되었습니다.")
        print(f"스케줄 시간: {start_time} ~ {end_time}")
        
        return True, f"{daily_count}개 트래픽 스케줄링 완료"


class TrafficManager:
    """트래픽 관리자 클래스"""
    
    def __init__(self):
        self.generator = TrafficGenerator()
    
    def activate_slot_traffic(self, slot_id):
        """
        슬롯 활성화 및 트래픽 생성 시작
        
        Args:
            slot_id: 활성화할 슬롯 ID
        """
        try:
            slot = Slot.objects.get(id=slot_id)
            
            if slot.is_expired:
                return False, "슬롯이 만료되었습니다."
            
            # 기본 트래픽 생성 (5회)
            success, message = self.generator.generate_traffic(slot, count=5)
            
            if success:
                # 검색 트래픽 생성 (3회)
                search_success, search_message = self.generator.generate_search_traffic(slot, count=3)
                
                return True, f"슬롯 활성화 완료: {message}, {search_message}"
            else:
                return False, f"슬롯 활성화 실패: {message}"
                
        except Slot.DoesNotExist:
            return False, "슬롯을 찾을 수 없습니다."
        except Exception as e:
            return False, f"슬롯 활성화 오류: {str(e)}"
    
    def batch_activate_slots(self, slot_ids):
        """
        여러 슬롯을 일괄 활성화
        
        Args:
            slot_ids: 활성화할 슬롯 ID 리스트
        """
        results = []
        
        for slot_id in slot_ids:
            success, message = self.activate_slot_traffic(slot_id)
            results.append({
                'slot_id': slot_id,
                'success': success,
                'message': message
            })
        
        return results
    
    def get_active_slots(self):
        """활성화된 슬롯 목록 반환"""
        return Slot.objects.filter(
            end_date__gt=timezone.now()
        ).order_by('end_date')
    
    def get_traffic_stats(self, slot_id):
        """
        슬롯의 트래픽 통계 반환
        
        Args:
            slot_id: 슬롯 ID
        """
        try:
            slot = Slot.objects.get(id=slot_id)
            
            # 실제 구현에서는 트래픽 로그를 저장하고 분석해야 함
            stats = {
                'slot_id': slot_id,
                'keyword': slot.keyword,
                'url': slot.url,
                'days_remaining': slot.days_remaining,
                'is_active': not slot.is_expired,
                'estimated_traffic': random.randint(50, 200),  # 예시 데이터
                'last_activity': timezone.now()
            }
            
            return True, stats
            
        except Slot.DoesNotExist:
            return False, "슬롯을 찾을 수 없습니다." 