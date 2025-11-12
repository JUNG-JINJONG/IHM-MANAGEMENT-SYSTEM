# Railway 배포 가이드

## 백엔드 배포 (Django)

### 1. GitHub 저장소 생성 및 푸시
```bash
git init
git add .
git commit -m "Initial commit for Railway deployment"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### 2. Railway 백엔드 배포
1. Railway 대시보드 접속: https://railway.app
2. "New Project" 클릭
3. "Deploy from GitHub repo" 선택
4. 저장소 선택
5. 환경 변수 설정:
   - `SECRET_KEY`: 새로운 시크릿 키 생성
   - `DEBUG`: False
   - `DATABASE_URL`: (이미 있는 Railway MySQL URL 사용)
   - `ALLOWED_HOSTS`: your-app-name.up.railway.app
   - `CORS_ALLOWED_ORIGINS`: https://your-frontend-url.up.railway.app
   - `CSRF_TRUSTED_ORIGINS`: https://your-frontend-url.up.railway.app

6. 배포 후 마이그레이션 실행 (Railway CLI 또는 대시보드에서):
```bash
python manage.py migrate
python manage.py createsuperuser
```

## 프론트엔드 배포 (Vue.js)

### 1. 프론트엔드 빌드 설정 수정
`ihm-frontend/.env.production` 파일 생성:
```
VITE_API_URL=https://your-backend-url.up.railway.app/api
```

### 2. Railway 프론트엔드 배포
1. Railway 대시보드에서 "New Project" 클릭
2. "Deploy from GitHub repo" 선택 (같은 저장소)
3. 설정:
   - Root Directory: `ihm-frontend`
   - Build Command: `npm install && npm run build`
   - Start Command: `npm run preview`

4. 환경 변수:
   - `VITE_API_URL`: https://your-backend-url.up.railway.app/api

### 3. 백엔드 CORS 설정 업데이트
프론트엔드 URL이 생성되면 백엔드 환경 변수 업데이트:
- `CORS_ALLOWED_ORIGINS`: https://your-frontend-url.up.railway.app
- `CSRF_TRUSTED_ORIGINS`: https://your-frontend-url.up.railway.app

## 배포 체크리스트
- [ ] .gitignore 확인
- [ ] requirements.txt 확인
- [ ] Procfile 생성
- [ ] runtime.txt 생성
- [ ] Django settings.py 프로덕션 설정
- [ ] 프론트엔드 API URL 환경 변수 설정
- [ ] GitHub 푸시
- [ ] Railway 백엔드 배포
- [ ] Railway 프론트엔드 배포
- [ ] 마이그레이션 실행
- [ ] 테스트
