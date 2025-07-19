from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Slot(models.Model):
    """슬롯 모델"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255)
    url = models.URLField(max_length=500)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.keyword} - {self.url}"
    
    @property
    def is_expired(self):
        return timezone.now() > self.end_date
    
    @property
    def days_remaining(self):
        if self.is_expired:
            return 0
        return (self.end_date - timezone.now()).days
    
    def extend_slot(self, days=30):
        """슬롯 연장"""
        self.end_date += timedelta(days=days)
        self.save()
    
    def reset_slot(self):
        """슬롯 초기화 (30일로 재설정)"""
        self.start_date = timezone.now()
        self.end_date = self.start_date + timedelta(days=30)
        self.save()


class Notice(models.Model):
    """공지사항 모델"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title


class TrafficLog(models.Model):
    """트래픽 활동 로그 모델"""
    TRAFFIC_TYPES = [
        ('basic', '기본 백링크'),
        ('multi_hop', '다단계 우회'),
        ('scheduled', '스케줄 백링크'),
    ]
    
    STATUS_CHOICES = [
        ('success', '성공'),
        ('failed', '실패'),
        ('pending', '대기중'),
    ]
    
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, related_name='traffic_logs')
    traffic_type = models.CharField(max_length=20, choices=TRAFFIC_TYPES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    # 트래픽 경로 정보
    search_engine = models.CharField(max_length=100, blank=True)
    intermediate_site = models.CharField(max_length=200, blank=True)
    intermediate_site_category = models.CharField(max_length=50, blank=True)
    target_url = models.URLField()
    
    # 상세 정보
    user_agent = models.TextField(blank=True)
    referer = models.URLField(blank=True)
    response_code = models.IntegerField(null=True, blank=True)
    response_time = models.FloatField(null=True, blank=True)  # 초 단위
    
    # 체류 시간 정보
    search_stay_time = models.FloatField(null=True, blank=True)  # 검색 페이지 체류 시간
    intermediate_stay_time = models.FloatField(null=True, blank=True)  # 중간 사이트 체류 시간
    target_stay_time = models.FloatField(null=True, blank=True)  # 타겟 사이트 체류 시간
    
    # 오류 정보
    error_message = models.TextField(blank=True)
    
    # 메타데이터
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.slot.keyword} - {self.get_traffic_type_display()} - {self.status}"
    
    @property
    def total_duration(self):
        """총 소요 시간"""
        times = [self.search_stay_time, self.intermediate_stay_time, self.target_stay_time]
        return sum(t for t in times if t is not None)
    
    @property
    def is_completed(self):
        return self.status in ['success', 'failed']


class TrafficSettings(models.Model):
    """트래픽 설정 모델"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # 기본 트래픽 설정
    basic_traffic_count = models.IntegerField(default=3, help_text="기본 백링크 트래픽 수")
    multi_hop_traffic_count = models.IntegerField(default=2, help_text="다단계 우회 트래픽 수")
    scheduled_daily_count = models.IntegerField(default=8, help_text="스케줄 백링크 일일 트래픽 수")
    
    # 체류 시간 설정 (초 단위)
    min_search_stay_time = models.FloatField(default=2.0, help_text="최소 검색 페이지 체류 시간")
    max_search_stay_time = models.FloatField(default=5.0, help_text="최대 검색 페이지 체류 시간")
    
    min_intermediate_stay_time = models.FloatField(default=30.0, help_text="최소 중간 사이트 체류 시간")
    max_intermediate_stay_time = models.FloatField(default=180.0, help_text="최대 중간 사이트 체류 시간")
    
    min_target_stay_time = models.FloatField(default=60.0, help_text="최소 타겟 사이트 체류 시간")
    max_target_stay_time = models.FloatField(default=300.0, help_text="최대 타겟 사이트 체류 시간")
    
    # 지연 시간 설정
    min_delay_between_requests = models.FloatField(default=1.0, help_text="요청 간 최소 지연 시간")
    max_delay_between_requests = models.FloatField(default=5.0, help_text="요청 간 최대 지연 시간")
    
    # 고급 설정
    enable_user_behavior_simulation = models.BooleanField(default=True, help_text="사용자 행동 시뮬레이션 활성화")
    enable_random_delays = models.BooleanField(default=True, help_text="랜덤 지연 시간 활성화")
    enable_multi_hop = models.BooleanField(default=True, help_text="다단계 우회 활성화")
    
    # 생성/수정 시간
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user']
    
    def __str__(self):
        return f"{self.user.username}의 트래픽 설정"
    
    @classmethod
    def get_or_create_for_user(cls, user):
        """사용자의 트래픽 설정을 가져오거나 생성"""
        settings, created = cls.objects.get_or_create(user=user)
        return settings 