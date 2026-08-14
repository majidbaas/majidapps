import os

# آدرس پایه پروژه (همان پوشه‌ای که app.py در آن است)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# آدرس دقیق دیتابیس اصلی (همان database.db کنار app.py)
DATABASE_PATH = os.path.join(BASE_DIR, 'database.db')

# پوشه آپلود فایل‌ها
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')

# اگر پوشه آپلود وجود ندارد، آن را بساز
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)