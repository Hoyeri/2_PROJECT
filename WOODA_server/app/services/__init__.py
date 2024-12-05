# app/services/__init__.py

from .auth_service import create_user, verify_user
from .diary_service import (
    create_diary, get_diary_by_id, get_all_diaries_with_friends, update_diary, delete_diary
)
from .schedule_service import (
    create_schedule, get_schedule_by_id, get_all_schedules_with_friends, update_schedule, delete_schedule
)
from .friends_service import add_friend, get_friends, remove_friend

# 각 서비스 모듈에서 주요 함수들을 가져와 초기화 파일에 등록합니다.
