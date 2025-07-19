from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db import models
from django.core.paginator import Paginator
from django.contrib.auth.hashers import check_password
from .models import Slot, Notice, TrafficLog, TrafficSettings
from .forms import SlotForm, NoticeForm, TrafficSettingsForm, AdminPasswordForm
from .traffic_generator import TrafficManager
from .backlink_system import BacklinkTrafficManager
import json


def login_view(request):
    """로그인 뷰"""
    if request.user.is_authenticated:
        return redirect('slot_list')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('slot_list')
    else:
        form = AuthenticationForm()
    
    return render(request, 'slots/login.html', {'form': form})


@login_required
def slot_list(request):
    """슬롯 목록 뷰"""
    search_query = request.GET.get('search', '')
    slots = Slot.objects.filter(user=request.user)
    
    if search_query:
        slots = slots.filter(
            models.Q(keyword__icontains=search_query) |
            models.Q(url__icontains=search_query)
        )
    
    notices = Notice.objects.filter(is_active=True).order_by('-created_at')[:5]
    
    context = {
        'slots': slots,
        'notices': notices,
        'search_query': search_query,
        'total_slots': slots.count(),
    }
    return render(request, 'slots/slot_list.html', context)


@login_required
def slot_create(request):
    """슬롯 생성 뷰"""
    if request.method == 'POST':
        form = SlotForm(request.POST)
        if form.is_valid():
            slot = form.save(commit=False)
            slot.user = request.user
            slot.save()
            messages.success(request, '슬롯이 성공적으로 생성되었습니다.')
            return redirect('slot_list')
    else:
        form = SlotForm()
    
    return render(request, 'slots/slot_form.html', {'form': form, 'title': '새 슬롯 생성'})


@login_required
def slot_update(request, pk):
    """슬롯 수정 뷰"""
    slot = get_object_or_404(Slot, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = SlotForm(request.POST, instance=slot)
        if form.is_valid():
            form.save()
            messages.success(request, '슬롯이 성공적으로 수정되었습니다.')
            return redirect('slot_list')
    else:
        form = SlotForm(instance=slot)
    
    return render(request, 'slots/slot_form.html', {'form': form, 'title': '슬롯 수정'})


@login_required
def slot_delete(request, pk):
    """슬롯 삭제 뷰"""
    slot = get_object_or_404(Slot, pk=pk, user=request.user)
    slot.delete()
    messages.success(request, '슬롯이 삭제되었습니다.')
    return redirect('slot_list')


@login_required
@require_POST
def slot_extend(request, pk):
    """슬롯 연장 뷰"""
    slot = get_object_or_404(Slot, pk=pk, user=request.user)
    days = int(request.POST.get('days', 30))
    slot.extend_slot(days)
    return JsonResponse({'success': True, 'message': f'{days}일 연장되었습니다.'})


@login_required
@require_POST
def slot_reset(request, pk):
    """슬롯 초기화 뷰"""
    slot = get_object_or_404(Slot, pk=pk, user=request.user)
    slot.reset_slot()
    return JsonResponse({'success': True, 'message': '슬롯이 초기화되었습니다.'})


@login_required
@csrf_exempt
def bulk_action(request):
    """대량 작업 뷰"""
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')
        slot_ids = data.get('slot_ids', [])
        
        slots = Slot.objects.filter(id__in=slot_ids, user=request.user)
        
        if action == 'extend':
            for slot in slots:
                slot.extend_slot(30)
            message = f'{len(slots)}개 슬롯이 30일 연장되었습니다.'
        elif action == 'reset':
            for slot in slots:
                slot.reset_slot()
            message = f'{len(slots)}개 슬롯이 초기화되었습니다.'
        elif action == 'delete':
            count = slots.count()
            slots.delete()
            message = f'{count}개 슬롯이 삭제되었습니다.'
        else:
            return JsonResponse({'success': False, 'message': '잘못된 작업입니다.'})
        
        return JsonResponse({'success': True, 'message': message})
    
    return JsonResponse({'success': False, 'message': '잘못된 요청입니다.'})


@login_required
@csrf_exempt
def activate_traffic(request):
    """트래픽 활성화 뷰 (백링크 우회 시스템)"""
    if request.method == 'POST':
        data = json.loads(request.body)
        slot_id = data.get('slot_id')
        traffic_type = data.get('traffic_type', 'basic')  # basic, multi_hop, scheduled
        
        if not slot_id:
            return JsonResponse({'success': False, 'message': '슬롯 ID가 필요합니다.'})
        
        # 슬롯이 사용자의 것인지 확인
        slot = get_object_or_404(Slot, id=slot_id, user=request.user)
        
        if slot.is_expired:
            return JsonResponse({'success': False, 'message': '만료된 슬롯은 활성화할 수 없습니다.'})
        
        try:
            # 백링크 트래픽 매니저 사용
            backlink_manager = BacklinkTrafficManager()
            success, message = backlink_manager.activate_backlink_traffic(slot_id, traffic_type)
            
            if success:
                return JsonResponse({
                    'success': True, 
                    'message': f'백링크 트래픽 활성화 완료: {message}',
                    'slot_id': slot_id
                })
            else:
                return JsonResponse({'success': False, 'message': f'백링크 트래픽 활성화 실패: {message}'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'백링크 트래픽 활성화 오류: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': '잘못된 요청입니다.'})


@login_required
@csrf_exempt
def batch_activate_traffic(request):
    """대량 백링크 트래픽 활성화 뷰"""
    if request.method == 'POST':
        data = json.loads(request.body)
        slot_ids = data.get('slot_ids', [])
        traffic_type = data.get('traffic_type', 'basic')
        
        if not slot_ids:
            return JsonResponse({'success': False, 'message': '선택된 슬롯이 없습니다.'})
        
        # 슬롯들이 사용자의 것인지 확인
        slots = Slot.objects.filter(id__in=slot_ids, user=request.user)
        active_slots = [slot for slot in slots if not slot.is_expired]
        
        if not active_slots:
            return JsonResponse({'success': False, 'message': '활성화할 수 있는 슬롯이 없습니다.'})
        
        try:
            # 백링크 트래픽 매니저 사용
            backlink_manager = BacklinkTrafficManager()
            results = backlink_manager.batch_activate_backlink_traffic(slot_ids, traffic_type)
            
            success_count = sum(1 for r in results if r['success'])
            
            return JsonResponse({
                'success': True,
                'message': f'{success_count}/{len(active_slots)}개 슬롯 백링크 트래픽 활성화 완료',
                'results': results
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'대량 백링크 활성화 오류: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': '잘못된 요청입니다.'})


@login_required
def traffic_stats(request, pk):
    """트래픽 통계 뷰"""
    slot = get_object_or_404(Slot, pk=pk, user=request.user)
    
    try:
        traffic_manager = TrafficManager()
        success, stats = traffic_manager.get_traffic_stats(pk)
        
        if success:
            context = {
                'slot': slot,
                'stats': stats
            }
            return render(request, 'slots/traffic_stats.html', context)
        else:
            messages.error(request, stats)
            return redirect('slot_list')
            
    except Exception as e:
        messages.error(request, f'통계 조회 오류: {str(e)}')
        return redirect('slot_list')


@login_required
def traffic_logs(request):
    """트래픽 로그 모니터링 뷰 (관리자 인증 필요)"""
    if not request.user.is_staff:
        messages.error(request, '접근 권한이 없습니다.')
        return redirect('slot_list')
    
    # 관리자 비밀번호 확인
    if request.method == 'POST':
        form = AdminPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            if check_password(password, request.user.password):
                # 비밀번호가 맞으면 세션에 로그인 상태 저장
                request.session['admin_logs_verified'] = True
                return redirect('traffic_logs')
            else:
                messages.error(request, '관리자 비밀번호가 올바르지 않습니다.')
    else:
        form = AdminPasswordForm()
    
    # 관리자 인증이 완료되지 않았으면 비밀번호 입력 페이지 표시
    if not request.session.get('admin_logs_verified', False):
        return render(request, 'slots/admin_password.html', {'form': form})
    
    # 트래픽 로그 조회
    logs = TrafficLog.objects.select_related('slot', 'slot__user').order_by('-created_at')
    
    # 필터링
    status_filter = request.GET.get('status', '')
    traffic_type_filter = request.GET.get('traffic_type', '')
    user_filter = request.GET.get('user', '')
    
    if status_filter:
        logs = logs.filter(status=status_filter)
    if traffic_type_filter:
        logs = logs.filter(traffic_type=traffic_type_filter)
    if user_filter:
        logs = logs.filter(slot__user__username__icontains=user_filter)
    
    # 페이징
    paginator = Paginator(logs, 50)  # 페이지당 50개
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # 통계 정보
    total_logs = logs.count()
    success_logs = logs.filter(status='success').count()
    failed_logs = logs.filter(status='failed').count()
    pending_logs = logs.filter(status='pending').count()
    
    context = {
        'page_obj': page_obj,
        'total_logs': total_logs,
        'success_logs': success_logs,
        'failed_logs': failed_logs,
        'pending_logs': pending_logs,
        'status_filter': status_filter,
        'traffic_type_filter': traffic_type_filter,
        'user_filter': user_filter,
    }
    
    return render(request, 'slots/traffic_logs.html', context)


@login_required
def traffic_settings(request):
    """트래픽 설정 뷰"""
    # 사용자의 트래픽 설정 가져오기
    settings = TrafficSettings.get_or_create_for_user(request.user)
    
    if request.method == 'POST':
        form = TrafficSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, '트래픽 설정이 저장되었습니다.')
            return redirect('traffic_settings')
    else:
        form = TrafficSettingsForm(instance=settings)
    
    context = {
        'form': form,
        'settings': settings
    }
    
    return render(request, 'slots/traffic_settings.html', context)


@login_required
def notice_list(request):
    """공지사항 목록 뷰 (관리자용)"""
    if not request.user.is_staff:
        messages.error(request, '접근 권한이 없습니다.')
        return redirect('slot_list')
    
    notices = Notice.objects.all().order_by('-created_at')
    return render(request, 'slots/notice_list.html', {'notices': notices})


@login_required
def notice_create(request):
    """공지사항 생성 뷰 (관리자용)"""
    if not request.user.is_staff:
        messages.error(request, '접근 권한이 없습니다.')
        return redirect('slot_list')
    
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.user = request.user
            notice.save()
            messages.success(request, '공지사항이 생성되었습니다.')
            return redirect('notice_list')
    else:
        form = NoticeForm()
    
    return render(request, 'slots/notice_form.html', {'form': form, 'title': '새 공지사항'})


def logout_view(request):
    """로그아웃 뷰"""
    logout(request)
    messages.success(request, '로그아웃되었습니다.')
    return redirect('login') 