from flask import Flask, render_template
import os
app = Flask(__name__)

# لیست پروژه‌ها (برای نمایش در صفحه اصلی)
PROJECTS = [
    {
        "id": "travel-checklist",
        "title": "چک‌لیست سفر",
        "description": "برنامه‌ریزی سفر با انتخاب امکانات مورد نیاز",
        "status": "فعال",
        "url": "http://localhost:5001/",  # ← این خط را عوض کن
        "icon": "🧳"
    },
     {
        "id": "food-recommender",
        "title": "پیشنهاد غذا",
        "description": "بر اساس مواد اولیه موجود، غذا پیشنهاد بده",
        "status": "فعال",  # تغییر از "در حال توسعه" به "فعال"
        "url": "http://localhost:5002/",  # پورت ۵۰۰۲
        "icon": "🍳"
    },
    {
        "id": "invoice",
        "title": "فاکتور ساز",
        "description": "ایجاد و مدیریت فاکتورهای ساده",
        "status": "فعال",
        "url": "http://localhost:5003/",
        "icon": "📄"
    },
    {
        "id": "habit-tracker",
        "title": "پیگیری عادات",
        "description": "ثبت عادات روزانه و مشاهده پیشرفت",
        "status": "به‌زودی",
        "url": "#",
        "icon": "📊"
    },
    {
        "id": "trip-budget",
        "title": "بودجه سفر",
        "description": "تخمین هزینه‌های سفر بر اساس مقصد",
        "status": "به‌زودی",
        "url": "#",
        "icon": "💰"
    },
    {
        "id": "book-tracker",
        "title": "ردیاب کتاب",
        "description": "ثبت کتاب‌های خوانده شده و هدف سالانه",
        "status": "به‌زودی",
        "url": "#",
        "icon": "📚"
    },
    {
        "id": "flashcard",
        "title": "کارت‌خوان حافظه",
        "description": "سیستم مرور لغت با الگوریتم تکرار فاصله‌دار",
        "status": "به‌زودی",
        "url": "#",
        "icon": "🧠"
    }
]

@app.route('/')
def home():
    return render_template('index.html', projects=PROJECTS)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)