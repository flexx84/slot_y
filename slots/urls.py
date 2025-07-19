from django.urls import path
from . import views

urlpatterns = [
    # 인증 관련
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # 슬롯 관리
    path('', views.slot_list, name='slot_list'),
    path('slot/', views.slot_list, name='slot_list'),
    path('slot/create/', views.slot_create, name='slot_create'),
    path('slot/<int:pk>/update/', views.slot_update, name='slot_update'),
    path('slot/<int:pk>/delete/', views.slot_delete, name='slot_delete'),
    path('slot/<int:pk>/extend/', views.slot_extend, name='slot_extend'),
    path('slot/<int:pk>/reset/', views.slot_reset, name='slot_reset'),
    path('slot/bulk-action/', views.bulk_action, name='bulk_action'),
    
    # 트래픽 활성화
    path('slot/activate-traffic/', views.activate_traffic, name='activate_traffic'),
    path('slot/batch-activate-traffic/', views.batch_activate_traffic, name='batch_activate_traffic'),
    path('slot/<int:pk>/traffic-stats/', views.traffic_stats, name='traffic_stats'),
    
    # 트래픽 로그 및 설정
    path('traffic/logs/', views.traffic_logs, name='traffic_logs'),
    path('traffic/settings/', views.traffic_settings, name='traffic_settings'),
    
    # 공지사항 관리 (관리자용)
    path('notice/', views.notice_list, name='notice_list'),
    path('notice/create/', views.notice_create, name='notice_create'),
] 