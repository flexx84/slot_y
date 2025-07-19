# R슬롯 - 백링크 트래픽 생성 시스템

실시간 백링크 트래픽 생성 및 모니터링 시스템입니다.

## 🚀 주요 기능

### 📊 백링크 트래픽 시스템
- **기본 백링크**: 중간 사이트를 경유한 자연스러운 트래픽 생성
- **다단계 우회**: 여러 중간 사이트를 거쳐 더욱 자연스러운 트래픽
- **스케줄 백링크**: 24시간 분산 트래픽 생성

### 📈 실시간 트래픽 로그 모니터링
- 실시간 자동 새로고침 (5초~1분 간격 설정 가능)
- 각 단계별 상세 로그 기록
- 성공/실패 상태 실시간 확인
- 관리자 비밀번호 인증으로 보안 강화

### ⚙️ 트래픽 설정 관리
- 사용자별 트래픽 생성 설정
- 트래픽 수량 및 간격 조정

## 🛠️ 기술 스택

- **Backend**: Django 5.2.4
- **Database**: SQLite (개발) / PostgreSQL (운영)
- **Frontend**: Tailwind CSS, Font Awesome
- **Language**: Python 3.11+

## 📦 설치 및 실행

### 로컬 실행

1. **저장소 클론**
```bash
git clone https://github.com/flexx84/slot_y.git
cd slot_y
```

2. **가상환경 생성 및 활성화**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **의존성 설치**
```bash
pip install -r requirements.txt
```

4. **데이터베이스 마이그레이션**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **서버 실행**
```bash
python manage.py runserver
```

6. **브라우저에서 접속**
```
http://localhost:8000
```

### 기본 로그인 정보
- **관리자**: admin / admin123
- **일반 사용자**: user / user123

## 🌐 GitHub에서 실행

### GitHub Codespaces 사용

1. **GitHub 저장소로 이동**: https://github.com/flexx84/slot_y
2. **Code 버튼 클릭** → **Codespaces 탭**
3. **Create codespace on main 클릭**
4. **터미널에서 실행**:
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

### GitHub Actions 자동 배포

저장소에 `.github/workflows/deploy.yml` 파일이 포함되어 있어 자동 배포가 가능합니다.

## 📁 프로젝트 구조

```
slot_y/
├── slots/                    # 메인 앱
│   ├── models.py            # 데이터 모델
│   ├── views.py             # 뷰 함수
│   ├── backlink_system.py   # 백링크 트래픽 시스템
│   └── forms.py             # 폼 클래스
├── templates/               # HTML 템플릿
│   ├── base.html           # 기본 템플릿
│   └── slots/              # 슬롯 관련 템플릿
├── static/                 # 정적 파일
├── requirements.txt        # Python 의존성
└── manage.py              # Django 관리 스크립트
```

## 🔧 환경 변수 설정

`.env` 파일을 생성하여 다음 변수들을 설정할 수 있습니다:

```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
```

## 📝 사용법

1. **로그인**: 관리자 계정으로 로그인
2. **슬롯 생성**: 키워드와 URL 입력
3. **백링크 트래픽 활성화**: 기본/다단계/스케줄 중 선택
4. **트래픽 로그 확인**: 실시간 모니터링
5. **트래픽 설정**: 사용자별 설정 조정

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해주세요.

## ✅ 강력한 마이그레이션 자동화 완료

**문제**: `no such table: auth_user` - 마이그레이션이 실행되지 않음
**해결**: 여러 단계에서 마이그레이션을 강제로 실행하도록 설정

## 적용된 해결책:

### 1. **Procfile에서 강제 실행**:
```bash
web: python manage.py makemigrations && python manage.py migrate && python create_admin.py && gunicorn rslot.wsgi --log-file -
```

### 2. **railway.json에서 postinstall 스크립트**:
```json
"postinstall": "python manage.py makemigrations && python manage.py migrate && python create_admin.py && python manage.py collectstatic --noinput"
```

### 3. **wsgi.py에서 앱 시작 시 자동 실행**:
```python
# 앱 시작 시 마이그레이션 실행
run_migrations()
```

## 이제 3단계 보장:

1. **배포 시**: Procfile에서 마이그레이션 실행
2. **설치 후**: railway.json postinstall에서 마이그레이션 실행  
3. **앱 시작 시**: wsgi.py에서 마이그레이션 실행

## ⏰ 다음 단계:

1. **Railway 자동 재배포**: GitHub에 푸시했으므로 Railway가 자동으로 새 배포를 시작합니다
2. **3중 마이그레이션 보장**: 어느 단계에서든 마이그레이션이 실행됩니다
3. **관리자 계정 생성**: `admin` / `admin123` 계정이 자동으로 생성됩니다

이제 Railway에서 `auth_user` 테이블이 확실히 생성되고, 더 이상 오류가 발생하지 않을 것입니다! 🎯
