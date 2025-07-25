# Generated by Django 5.2.4 on 2025-07-19 03:47

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slots', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notice',
            options={},
        ),
        migrations.AlterModelOptions(
            name='slot',
            options={},
        ),
        migrations.AlterField(
            model_name='notice',
            name='content',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='notice',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='notice',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='notice',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='notice',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='notice',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='slot',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='slot',
            name='end_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='slot',
            name='keyword',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='slot',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='slot',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='slot',
            name='url',
            field=models.URLField(max_length=500),
        ),
        migrations.AlterField(
            model_name='slot',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='TrafficLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('traffic_type', models.CharField(choices=[('basic', '기본 백링크'), ('multi_hop', '다단계 우회'), ('scheduled', '스케줄 백링크')], max_length=20)),
                ('status', models.CharField(choices=[('success', '성공'), ('failed', '실패'), ('pending', '대기중')], default='pending', max_length=10)),
                ('search_engine', models.CharField(blank=True, max_length=100)),
                ('intermediate_site', models.CharField(blank=True, max_length=200)),
                ('intermediate_site_category', models.CharField(blank=True, max_length=50)),
                ('target_url', models.URLField()),
                ('user_agent', models.TextField(blank=True)),
                ('referer', models.URLField(blank=True)),
                ('response_code', models.IntegerField(blank=True, null=True)),
                ('response_time', models.FloatField(blank=True, null=True)),
                ('search_stay_time', models.FloatField(blank=True, null=True)),
                ('intermediate_stay_time', models.FloatField(blank=True, null=True)),
                ('target_stay_time', models.FloatField(blank=True, null=True)),
                ('error_message', models.TextField(blank=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='traffic_logs', to='slots.slot')),
            ],
        ),
        migrations.CreateModel(
            name='TrafficSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basic_traffic_count', models.IntegerField(default=3, help_text='기본 백링크 트래픽 수')),
                ('multi_hop_traffic_count', models.IntegerField(default=2, help_text='다단계 우회 트래픽 수')),
                ('scheduled_daily_count', models.IntegerField(default=8, help_text='스케줄 백링크 일일 트래픽 수')),
                ('min_search_stay_time', models.FloatField(default=2.0, help_text='최소 검색 페이지 체류 시간')),
                ('max_search_stay_time', models.FloatField(default=5.0, help_text='최대 검색 페이지 체류 시간')),
                ('min_intermediate_stay_time', models.FloatField(default=30.0, help_text='최소 중간 사이트 체류 시간')),
                ('max_intermediate_stay_time', models.FloatField(default=180.0, help_text='최대 중간 사이트 체류 시간')),
                ('min_target_stay_time', models.FloatField(default=60.0, help_text='최소 타겟 사이트 체류 시간')),
                ('max_target_stay_time', models.FloatField(default=300.0, help_text='최대 타겟 사이트 체류 시간')),
                ('min_delay_between_requests', models.FloatField(default=1.0, help_text='요청 간 최소 지연 시간')),
                ('max_delay_between_requests', models.FloatField(default=5.0, help_text='요청 간 최대 지연 시간')),
                ('enable_user_behavior_simulation', models.BooleanField(default=True, help_text='사용자 행동 시뮬레이션 활성화')),
                ('enable_random_delays', models.BooleanField(default=True, help_text='랜덤 지연 시간 활성화')),
                ('enable_multi_hop', models.BooleanField(default=True, help_text='다단계 우회 활성화')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user',)},
            },
        ),
    ]
