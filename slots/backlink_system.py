"""
백링크 우회 트래픽 생성 시스템
중간 사이트들을 경유하여 자연스러운 트래픽을 생성하는 시스템
"""
import requests
import time
import random
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Slot, TrafficLog, TrafficSettings


class BacklinkNetwork:
    """백링크 네트워크 관리 클래스"""
    
    def __init__(self):
        # 중간 사이트들 (백링크용) - 실제 접근 가능한 사이트들
        self.intermediate_sites = [
            {
                'name': '블로그 포스트',
                'urls': [
                    'https://medium.com/topic/technology',
                    'https://dev.to/t/javascript',
                    'https://hashnode.com/t/web-development',
                    'https://blog.logrocket.com/',
                    'https://css-tricks.com/'
                ],
                'content_type': 'blog'
            },
            {
                'name': '뉴스 사이트',
                'urls': [
                    'https://techcrunch.com/',
                    'https://www.theverge.com/',
                    'https://www.wired.com/',
                    'https://www.engadget.com/',
                    'https://www.gizmodo.com/'
                ],
                'content_type': 'news'
            },
            {
                'name': '포럼/커뮤니티',
                'urls': [
                    'https://stackoverflow.com/',
                    'https://reddit.com/r/programming/',
                    'https://reddit.com/r/webdev/',
                    'https://reddit.com/r/javascript/',
                    'https://reddit.com/r/Python/'
                ],
                'content_type': 'forum'
            },
            {
                'name': '소셜 미디어',
                'urls': [
                    'https://twitter.com/',
                    'https://www.linkedin.com/',
                    'https://github.com/',
                    'https://www.producthunt.com/',
                    'https://www.behance.net/'
                ],
                'content_type': 'social'
            }
        ]
        
        # 검색 엔진들
        self.search_engines = [
            'https://www.google.com/search?q=',
            'https://www.bing.com/search?q=',
            'https://search.naver.com/search.naver?query=',
            'https://search.daum.net/search?q=',
            'https://www.yahoo.com/search?p='
        ]
        
        # User-Agent 목록
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1.2 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Android 14; Mobile; rv:120.0) Gecko/120.0 Firefox/120.0'
        ]
    
    def get_random_intermediate_site(self):
        """랜덤 중간 사이트 선택"""
        site_category = random.choice(self.intermediate_sites)
        return {
            'category': site_category['name'],
            'url': random.choice(site_category['urls']),
            'content_type': site_category['content_type']
        }
    
    def get_random_search_engine(self):
        """랜덤 검색 엔진 선택"""
        return random.choice(self.search_engines)


class BacklinkTrafficGenerator:
    """백링크 우회 트래픽 생성기"""
    
    def __init__(self):
        self.backlink_network = BacklinkNetwork()
        self.session = requests.Session()
    
    def generate_backlink_traffic(self, slot, count=1):
        """
        백링크를 통한 우회 트래픽 생성
        
        Args:
            slot: Slot 모델 인스턴스
            count: 생성할 트래픽 수
        """
        if slot.is_expired:
            return False, "슬롯이 만료되었습니다."
        
        success_count = 0
        for i in range(count):
            start_time = timezone.now()
            intermediate_site = None
            status = 'failed'
            details = ''
            
            try:
                # 1단계: 검색 엔진에서 키워드 검색
                print(f"=== 트래픽 {i+1} 시작: {slot.keyword} ===")
                search_success = self._perform_search(slot.keyword)
                if not search_success:
                    details = '검색 엔진 접근 실패'
                    # 검색 실패 로그 기록
                    self._log_traffic_step(slot, 'search_failed', '검색 엔진 접근 실패', start_time)
                    continue
                
                # 검색 성공 로그 기록
                self._log_traffic_step(slot, 'search_success', '검색 엔진에서 키워드 검색 완료', start_time)
                
                # 2단계: 중간 사이트 방문 (백링크 사이트)
                intermediate_site = self.backlink_network.get_random_intermediate_site()
                intermediate_success = self._visit_intermediate_site(intermediate_site)
                if not intermediate_success:
                    details = '중간 사이트 접근 실패'
                    # 중간 사이트 실패 로그 기록
                    self._log_traffic_step(slot, 'intermediate_failed', f"중간 사이트 접근 실패: {intermediate_site['category']}", start_time)
                    continue
                
                # 중간 사이트 방문 성공 로그 기록
                self._log_traffic_step(slot, 'intermediate_visit', f"중간 사이트 방문 성공: {intermediate_site['category']} - {intermediate_site['url']}", start_time)
                
                # 3단계: 중간 사이트에서 체류 (자연스러운 행동 시뮬레이션)
                stay_log = self._simulate_user_behavior(intermediate_site)
                self._log_traffic_step(slot, 'intermediate_stay', stay_log, start_time)
                
                # 4단계: 백링크를 통해 타겟 사이트로 이동
                target_success = self._visit_target_via_backlink(slot.url, intermediate_site)
                
                if target_success:
                    success_count += 1
                    status = 'success'
                    details = f"백링크 트래픽 생성 성공: {intermediate_site['category']} -> {slot.url}"
                    print(f"백링크 트래픽 생성 성공: {intermediate_site['category']} -> {slot.url}")
                    # 타겟 방문 성공 로그 기록
                    self._log_traffic_step(slot, 'target_success', f"타겟 사이트 방문 성공: {slot.url}", start_time)
                else:
                    details = f"타겟 사이트 접근 실패: {slot.url}"
                    print(f"타겟 사이트 접근 실패: {slot.url}")
                    # 타겟 실패 로그 기록
                    self._log_traffic_step(slot, 'target_failed', f"타겟 사이트 접근 실패: {slot.url}", start_time)
                    
            except Exception as e:
                details = f"백링크 트래픽 생성 오류: {str(e)}"
                print(f"백링크 트래픽 생성 오류: {slot.keyword} -> {slot.url} - {str(e)}")
                # 오류 로그 기록
                self._log_traffic_step(slot, 'error', f"트래픽 생성 오류: {str(e)}", start_time)
            
            finally:
                # 최종 트래픽 로그 기록
                end_time = timezone.now()
                total_duration = (end_time - start_time).total_seconds()
                
                TrafficLog.objects.create(
                    slot=slot,
                    traffic_type='basic',
                    status=status,
                    intermediate_site=intermediate_site['url'] if intermediate_site else '',
                    intermediate_site_category=intermediate_site['category'] if intermediate_site else '',
                    target_url=slot.url,
                    error_message=details if status == 'failed' else '',
                    response_time=total_duration,
                    completed_at=end_time
                )
        
        return True, f"{success_count}/{count} 백링크 트래픽 생성 완료"
    
    def _log_traffic_step(self, slot, step_type, message, start_time):
        """트래픽 단계별 로그 기록"""
        step_mapping = {
            'search_success': '검색 성공',
            'search_failed': '검색 실패',
            'intermediate_visit': '중간사이트 방문',
            'intermediate_failed': '중간사이트 실패',
            'intermediate_stay': '중간사이트 체류',
            'target_success': '타겟 방문 성공',
            'target_failed': '타겟 방문 실패',
            'error': '오류 발생'
        }
        
        TrafficLog.objects.create(
            slot=slot,
            traffic_type='basic',
            status='pending' if step_type in ['search_success', 'intermediate_visit', 'intermediate_stay'] else 'failed',
            intermediate_site='',
            intermediate_site_category=step_mapping.get(step_type, step_type),
            target_url=slot.url,
            error_message=message,
            response_time=(timezone.now() - start_time).total_seconds(),
            completed_at=timezone.now()
        )
    
    def _perform_search(self, keyword):
        """검색 엔진에서 키워드 검색"""
        try:
            search_engine = self.backlink_network.get_random_search_engine()
            search_url = f"{search_engine}{keyword}"
            
            headers = {
                'User-Agent': random.choice(self.backlink_network.user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            # 검색 결과 페이지 방문
            response = self.session.get(search_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                # 검색 결과에서 잠시 체류 (스크롤, 클릭 등 시뮬레이션)
                time.sleep(random.uniform(2, 5))
                return True
            else:
                print(f"검색 엔진 접근 실패: {search_url} (상태코드: {response.status_code})")
                return False
                
        except Exception as e:
            print(f"검색 수행 오류: {str(e)}")
            return False
    
    def _visit_intermediate_site(self, intermediate_site):
        """중간 사이트 방문"""
        try:
            headers = {
                'User-Agent': random.choice(self.backlink_network.user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            # 중간 사이트 방문
            response = self.session.get(intermediate_site['url'], headers=headers, timeout=30)
            
            if response.status_code == 200:
                print(f"중간 사이트 방문 성공: {intermediate_site['category']} - {intermediate_site['url']}")
                return True
            else:
                print(f"중간 사이트 접근 실패: {intermediate_site['url']} (상태코드: {response.status_code})")
                return False
                
        except Exception as e:
            print(f"중간 사이트 방문 오류: {str(e)}")
            return False
    
    def _simulate_user_behavior(self, intermediate_site):
        """사용자 행동 시뮬레이션"""
        try:
            # 사이트에서 체류 시간 (5초~15초로 단축)
            stay_time = random.uniform(5, 15)
            print(f"중간 사이트에서 {stay_time:.1f}초 체류 중...")
            time.sleep(stay_time)
            
            # 페이지 스크롤 시뮬레이션 (여러 번의 짧은 대기)
            scroll_count = random.randint(2, 4)
            scroll_total_time = 0
            for i in range(scroll_count):
                scroll_time = random.uniform(0.5, 1.5)
                scroll_total_time += scroll_time
                time.sleep(scroll_time)
                print(f"페이지 스크롤 {i+1}/{scroll_count}...")
            
            # 내부 링크 클릭 시뮬레이션
            click_time = 0
            if random.random() < 0.3:  # 30% 확률로 내부 링크 클릭
                click_time = random.uniform(2, 5)
                print("내부 링크 클릭 시뮬레이션...")
                time.sleep(click_time)
            
            total_time = stay_time + scroll_total_time + click_time
            return f"중간 사이트에서 {total_time:.1f}초 체류 완료 (기본체류: {stay_time:.1f}초, 스크롤: {scroll_count}회, 링크클릭: {'있음' if click_time > 0 else '없음'})"
                
        except Exception as e:
            print(f"사용자 행동 시뮬레이션 오류: {str(e)}")
            return f"사용자 행동 시뮬레이션 오류: {str(e)}"
    
    def _visit_target_via_backlink(self, target_url, intermediate_site):
        """백링크를 통해 타겟 사이트 방문"""
        try:
            # 백링크를 통한 방문 시뮬레이션
            headers = {
                'User-Agent': random.choice(self.backlink_network.user_agents),
                'Referer': intermediate_site['url'],  # 중간 사이트를 리퍼러로 설정
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            # 타겟 사이트 방문
            response = self.session.get(target_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                # 타겟 사이트에서 체류 (자연스러운 방문자 행동)
                target_behavior_log = self._simulate_target_site_behavior()
                print(f"타겟 사이트 방문 성공: {target_url} (리퍼러: {intermediate_site['url']})")
                print(f"타겟 사이트 행동: {target_behavior_log}")
                return True
            else:
                print(f"타겟 사이트 접근 실패: {target_url} (상태코드: {response.status_code})")
                return False
                
        except Exception as e:
            print(f"타겟 사이트 방문 오류: {str(e)}")
            return False
    
    def _simulate_target_site_behavior(self):
        """타겟 사이트에서의 사용자 행동 시뮬레이션"""
        try:
            # 타겟 사이트에서 체류 시간 (10초~30초로 단축)
            stay_time = random.uniform(10, 30)
            print(f"타겟 사이트에서 {stay_time:.1f}초 체류 중...")
            time.sleep(stay_time)
            
            # 페이지 상호작용 시뮬레이션
            interaction_count = random.randint(1, 3)
            interaction_total_time = 0
            for i in range(interaction_count):
                interaction_time = random.uniform(1, 3)
                interaction_total_time += interaction_time
                time.sleep(interaction_time)
                print(f"페이지 상호작용 {i+1}/{interaction_count}...")
            
            total_time = stay_time + interaction_total_time
            return f"타겟 사이트에서 {total_time:.1f}초 체류 완료 (기본체류: {stay_time:.1f}초, 상호작용: {interaction_count}회)"
                
        except Exception as e:
            print(f"타겟 사이트 행동 시뮬레이션 오류: {str(e)}")
            return f"타겟 사이트 행동 시뮬레이션 오류: {str(e)}"
    
    def generate_multi_hop_traffic(self, slot, count=1):
        """
        다단계 우회 트래픽 생성 (여러 중간 사이트 경유)
        
        Args:
            slot: Slot 모델 인스턴스
            count: 생성할 트래픽 수
        """
        if slot.is_expired:
            return False, "슬롯이 만료되었습니다."
        
        success_count = 0
        for i in range(count):
            start_time = timezone.now()
            site1 = None
            site2 = None
            status = 'failed'
            details = ''
            
            try:
                # 1단계: 검색 엔진에서 키워드 검색
                search_success = self._perform_search(slot.keyword)
                if not search_success:
                    details = '검색 엔진 접근 실패'
                    continue
                
                # 2단계: 첫 번째 중간 사이트 방문
                site1 = self.backlink_network.get_random_intermediate_site()
                if not self._visit_intermediate_site(site1):
                    details = '첫 번째 중간 사이트 접근 실패'
                    continue
                
                # 3단계: 첫 번째 사이트에서 체류
                self._simulate_user_behavior(site1)
                
                # 4단계: 두 번째 중간 사이트 방문 (다단계 우회)
                site2 = self.backlink_network.get_random_intermediate_site()
                if not self._visit_intermediate_site(site2):
                    details = '두 번째 중간 사이트 접근 실패'
                    continue
                
                # 5단계: 두 번째 사이트에서 체류
                self._simulate_user_behavior(site2)
                
                # 6단계: 최종 타겟 사이트 방문
                target_success = self._visit_target_via_backlink(slot.url, site2)
                
                if target_success:
                    success_count += 1
                    status = 'success'
                    details = f"다단계 우회 트래픽 생성 성공: {site1['category']} -> {site2['category']} -> {slot.url}"
                    print(f"다단계 우회 트래픽 생성 성공: {site1['category']} -> {site2['category']} -> {slot.url}")
                else:
                    details = f"다단계 우회 타겟 접근 실패: {slot.url}"
                    print(f"다단계 우회 타겟 접근 실패: {slot.url}")
                    
            except Exception as e:
                details = f"다단계 우회 트래픽 생성 오류: {str(e)}"
                print(f"다단계 우회 트래픽 생성 오류: {slot.keyword} -> {slot.url} - {str(e)}")
            
            finally:
                # 트래픽 로그 기록
                end_time = timezone.now()
                total_duration = (end_time - start_time).total_seconds()
                
                intermediate_sites = []
                if site1:
                    intermediate_sites.append(site1['url'])
                if site2:
                    intermediate_sites.append(site2['url'])
                
                TrafficLog.objects.create(
                    slot=slot,
                    traffic_type='multi_hop',
                    status=status,
                    intermediate_site=' -> '.join(intermediate_sites),
                    intermediate_site_category=f"{site1['category']} -> {site2['category']}" if site1 and site2 else '',
                    target_url=slot.url,
                    error_message=details if status == 'failed' else '',
                    response_time=total_duration,
                    completed_at=end_time
                )
        
        return True, f"{success_count}/{count} 다단계 우회 트래픽 생성 완료"
    
    def schedule_backlink_traffic(self, slot, daily_count=10):
        """
        백링크 트래픽 스케줄링 (24시간 분산)
        
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
        
        # 스케줄링 로그 기록
        TrafficLog.objects.create(
            slot=slot,
            traffic_type='scheduled',
            status='pending',
            intermediate_site='',
            intermediate_site_category='',
            target_url=slot.url,
            error_message=f"{daily_count}개 백링크 트래픽 스케줄링 완료. 스케줄 시간: {start_time} ~ {end_time}",
            response_time=0,
            completed_at=None
        )
        
        print(f"슬롯 '{slot.keyword}'에 대해 {daily_count}개의 백링크 트래픽이 스케줄링되었습니다.")
        print(f"스케줄 시간: {start_time} ~ {end_time}")
        
        return True, f"{daily_count}개 백링크 트래픽 스케줄링 완료"


class BacklinkTrafficManager:
    """백링크 트래픽 관리자"""
    
    def __init__(self):
        self.generator = BacklinkTrafficGenerator()
    
    def activate_backlink_traffic(self, slot_id, traffic_type='basic'):
        """
        백링크 트래픽 활성화
        
        Args:
            slot_id: 활성화할 슬롯 ID
            traffic_type: 트래픽 타입 (basic, multi_hop, scheduled)
        """
        try:
            slot = Slot.objects.get(id=slot_id)
            
            if slot.is_expired:
                return False, "슬롯이 만료되었습니다."
            
            if traffic_type == 'basic':
                success, message = self.generator.generate_backlink_traffic(slot, count=3)
            elif traffic_type == 'multi_hop':
                success, message = self.generator.generate_multi_hop_traffic(slot, count=2)
            elif traffic_type == 'scheduled':
                success, message = self.generator.schedule_backlink_traffic(slot, daily_count=8)
            else:
                return False, "잘못된 트래픽 타입입니다."
            
            if success:
                return True, f"백링크 트래픽 활성화 완료: {message}"
            else:
                return False, f"백링크 트래픽 활성화 실패: {message}"
                
        except Slot.DoesNotExist:
            return False, "슬롯을 찾을 수 없습니다."
        except Exception as e:
            return False, f"백링크 트래픽 활성화 오류: {str(e)}"
    
    def batch_activate_backlink_traffic(self, slot_ids, traffic_type='basic'):
        """
        여러 슬롯의 백링크 트래픽 일괄 활성화
        
        Args:
            slot_ids: 활성화할 슬롯 ID 리스트
            traffic_type: 트래픽 타입
        """
        results = []
        
        for slot_id in slot_ids:
            success, message = self.activate_backlink_traffic(slot_id, traffic_type)
            results.append({
                'slot_id': slot_id,
                'success': success,
                'message': message
            })
        
        return results 