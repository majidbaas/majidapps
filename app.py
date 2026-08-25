from flask import Flask, render_template
import os
app = Flask(__name__)

app.config["DEBUG"] = False
app.config["TESTING"] = False



app.secret_key = "global_super_secret_key"
app.config["UPLOAD_FOLDER"] = "projects/invoice/static/uploads"


# ===== ثبت Blueprintها =====
# ===== ثبت Blueprintها =====
from projects.travel.travel import travel_bp
from projects.food.food import food_bp
# from projects.invoice.invoice import invoice_bp

app.register_blueprint(travel_bp, url_prefix='/travel')
app.register_blueprint(food_bp, url_prefix='/food')
# app.register_blueprint(invoice_bp, url_prefix='/invoice')

# لیست پروژه‌ها (برای نمایش در صفحه اصلی)
PROJECTS = [
   {
        "id": "travel",
        "title": "چک‌لیست سفر",
        "description": "برنامه‌ریزی سفر با انتخاب امکانات مورد نیاز",
        "status": "فعال",
        "url": "/travel/",
        "icon": "🧳"
    },
   {
       "title": "پیشنهاد غذا",
        "description": "بر اساس مواد اولیه موجود، غذا پیشنهاد بده",
        "status": "فعال",
        "url": "/food/",
        "icon": "🍳"
    },
    {
        "id": "invoice",
        "title": "فاکتور ساز",
        "description": "ایجاد و مدیریت فاکتورهای ساده",
        "status": "فعال",
        "url": "/invoice/",
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
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get("PORT", 8000)),
        debug=False,
        use_reloader=False
    )