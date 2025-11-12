import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ihm_backend.settings')
django.setup()

from users.models import User

print("=== 현재 데이터베이스의 사용자 목록 ===")
users = User.objects.all()
if users.exists():
    for user in users:
        print(f"Username: {user.username}, Type: {user.user_type}, Active: {user.is_active}")
else:
    print("사용자가 없습니다!")

print("\n=== 특정 사용자 확인 ===")
for username in ['operator', 'supplier1', 'customer1']:
    try:
        user = User.objects.get(username=username)
        print(f"✓ {username} 존재 (type: {user.user_type})")
        # 비밀번호 확인
        if user.check_password('password123'):
            print(f"  비밀번호 'password123' 검증 성공")
        else:
            print(f"  비밀번호 'password123' 검증 실패!")
    except User.DoesNotExist:
        print(f"✗ {username} 존재하지 않음")
