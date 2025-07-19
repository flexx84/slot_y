from django import forms
from .models import Slot, Notice, TrafficSettings


class SlotForm(forms.ModelForm):
    """슬롯 생성/수정 폼"""
    class Meta:
        model = Slot
        fields = ['keyword', 'url']
        widgets = {
            'keyword': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': '검색 키워드를 입력하세요'
            }),
            'url': forms.URLInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'https://example.com'
            })
        }


class NoticeForm(forms.ModelForm):
    """공지사항 생성/수정 폼"""
    class Meta:
        model = Notice
        fields = ['title', 'content', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': '공지사항 제목'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'rows': 5,
                'placeholder': '공지사항 내용을 입력하세요'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'rounded border-gray-300 text-indigo-600 focus:ring-indigo-500'
            })
        }


class TrafficSettingsForm(forms.ModelForm):
    class Meta:
        model = TrafficSettings
        exclude = ['user', 'created_at', 'updated_at']
        widgets = {
            # 기본 트래픽 설정
            'basic_traffic_count': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'min': 1,
                'max': 50
            }),
            'multi_hop_traffic_count': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'min': 1,
                'max': 20
            }),
            'scheduled_daily_count': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'min': 1,
                'max': 100
            }),
            
            # 체류 시간 설정
            'min_search_stay_time': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'step': 0.1,
                'min': 0.1
            }),
            'max_search_stay_time': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'step': 0.1,
                'min': 0.1
            }),
            'min_intermediate_stay_time': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'step': 1,
                'min': 1
            }),
            'max_intermediate_stay_time': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'step': 1,
                'min': 1
            }),
            'min_target_stay_time': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'step': 1,
                'min': 1
            }),
            'max_target_stay_time': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'step': 1,
                'min': 1
            }),
            
            # 지연 시간 설정
            'min_delay_between_requests': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'step': 0.1,
                'min': 0.1
            }),
            'max_delay_between_requests': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'step': 0.1,
                'min': 0.1
            }),
            
            # 고급 설정
            'enable_user_behavior_simulation': forms.CheckboxInput(attrs={
                'class': 'rounded border-gray-300 text-indigo-600 focus:ring-indigo-500'
            }),
            'enable_random_delays': forms.CheckboxInput(attrs={
                'class': 'rounded border-gray-300 text-indigo-600 focus:ring-indigo-500'
            }),
            'enable_multi_hop': forms.CheckboxInput(attrs={
                'class': 'rounded border-gray-300 text-indigo-600 focus:ring-indigo-500'
            })
        }
    
    def clean(self):
        cleaned_data = super().clean()
        
        # 최소값이 최대값보다 클 수 없도록 검증
        min_search = cleaned_data.get('min_search_stay_time')
        max_search = cleaned_data.get('max_search_stay_time')
        if min_search and max_search and min_search > max_search:
            raise forms.ValidationError("검색 체류 시간의 최소값은 최대값보다 클 수 없습니다.")
        
        min_intermediate = cleaned_data.get('min_intermediate_stay_time')
        max_intermediate = cleaned_data.get('max_intermediate_stay_time')
        if min_intermediate and max_intermediate and min_intermediate > max_intermediate:
            raise forms.ValidationError("중간 사이트 체류 시간의 최소값은 최대값보다 클 수 없습니다.")
        
        min_target = cleaned_data.get('min_target_stay_time')
        max_target = cleaned_data.get('max_target_stay_time')
        if min_target and max_target and min_target > max_target:
            raise forms.ValidationError("타겟 사이트 체류 시간의 최소값은 최대값보다 클 수 없습니다.")
        
        min_delay = cleaned_data.get('min_delay_between_requests')
        max_delay = cleaned_data.get('max_delay_between_requests')
        if min_delay and max_delay and min_delay > max_delay:
            raise forms.ValidationError("지연 시간의 최소값은 최대값보다 클 수 없습니다.")
        
        return cleaned_data


class AdminPasswordForm(forms.Form):
    """관리자 비밀번호 확인 폼"""
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': '관리자 비밀번호를 입력하세요'
        }),
        label='관리자 비밀번호'
    ) 