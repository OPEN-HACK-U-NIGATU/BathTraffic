import random
from datetime import datetime, timedelta
from home.models import Snapshot

# 各時間帯ごとに風呂の人数データを生成
def generate_bath_data(hour):
    if 16 <= hour < 20:
        small_number = random.randint(3, 5)
        big_number = random.randint(6,9)
    elif 20 <= hour < 24:
        small_number = random.randint(0,3)
        big_number = random.randint(0,6)

    return small_number, big_number

def date_data(hour):
    now = datetime.now()
    random_date = now - timedelta(days=random.randint(1, 30))
    random_minute = random.randint(1, 59)
    random_second = random.randint(1, 59)
    
    return random_date.replace(
        hour=hour,
        minute=random_minute,
        second=random_second
    )

# ダミーデータの生成とデータベースへの挿入
for hour in range(16, 24):  # 16:00から23:00まで
    small_number, big_number = generate_bath_data(hour)
    
    # 過去の日時をランダムに生成
    past_time = date_data(hour)
    
    snapshot = Snapshot.objects.create(
        small_number=small_number,
        big_number=big_number,
        time=past_time
    )

    snapshot.save()
