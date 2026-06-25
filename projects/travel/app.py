from flask import Flask, render_template, request, redirect, session
import json
import os

print("HELLO FROM TRIP REPO")

# ===== تنظیم مسیرهای پروژه =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)
app.secret_key = "1642300Mb"

# ===== تغییر مسیر فایل داده =====
def load_data():
    data_path = os.path.join(BASE_DIR, 'data.json')  # مسیر مطلق
    with open(data_path, encoding="utf-8") as f:
        return json.load(f)

def rule_match(rules, form):
    for key, values in rules.items():
        print("CHECK:", key, "FORM=", form.get(key), "RULE=", values)
        if form.get(key) not in values:
            return False
    return True

def generate_checklist(form):
    data = load_data()
    result = {}

    for category in data["categories"]:
        category_rules = category.get("rules", {})
        if category_rules and not rule_match(category_rules, form):
            continue

        items_list = []
        for item in category["items"]:
            item_rules = item.get("rules", {})
            if item_rules and not rule_match(item_rules, form):
                continue
            items_list.append(item["name"])

        if items_list:
            result[category["title"]] = items_list

    return result

# ------------------------
# صفحه 1: فرم اصلی
# ------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session["form"] = request.form.to_dict()
        return redirect("/review")

    return render_template("index.html", form=session.get("form"))

# ------------------------
# صفحه 2: بررسی اطلاعات
# ------------------------
@app.route("/review", methods=["GET"])
def review():
    form = session.get("form")
    if not form:
        return redirect("/")

    trip_type_map = {
        "solo": "انفرادی",
        "family": "خانوادگی"
    }

    accommodation_map = {
        "hotel": "هتل",
        "hostel": "هاستل",
        "villa": "ویلا",
        "suite": "سوئیت آپارتمان",
        "eco": "اقامتگاه بوم‌گردی",
        "camp": "چادر کمپ",
        "familyHome": "خانه اقوام"
    }

    travel_type = form.get("travel_type")
    hotel_type = form.get("hotel_type")

    trip_type_fa = trip_type_map.get(travel_type, travel_type)
    accommodation_fa = accommodation_map.get(hotel_type, hotel_type)

    return render_template(
        "review.html",
        form=form,
        trip_type=trip_type_fa,
        accommodation=accommodation_fa
    )

# ------------------------
# صفحه 3: نتیجه نهایی
# ------------------------
@app.route("/result", methods=["POST"])
def result():
    form = session.get("form")
    if not form:
        return redirect("/")

    travel_type_fa = {
        "solo": "به‌صورت انفرادی",
        "family": "به‌همراه خانواده"
    }

    transport_fa = {
        "plane": "با هواپیما",
        "train": "با قطار",
        "car": "با خودرو",
        "motor": "با موتور",
        "bus": "با اتوبوس"
    }

    season_fa = {
        "spring": "در بهار",
        "summer": "در تابستان",
        "autumn": "در پاییز",
        "winter": "در زمستان"
    }

    name = form.get("name")
    travel_type = form.get("travel_type")
    transport = form.get("transport")
    season = form.get("season")
    city = form.get("city_fa")

    try:
        stay_days = int(form.get("stay_days", 1))
    except:
        stay_days = 1

    checklist = generate_checklist(form)

    title = (
        f"چک‌لیست سفر {name} "
        f"{travel_type_fa.get(travel_type)} "
        f"{transport_fa.get(transport)} "
        f"{season_fa.get(season)} "
        f"به {city} ({stay_days} شب اقامت)"
    )

    session.pop("form", None)

    for category in checklist:
        checklist[category] = list(set(checklist[category]))

    return render_template(
        "result.html",
        checklist=checklist,
        title=title,
    )

# ===== تغییر پورت برای جلوگیری از تداخل با صفحه اصلی =====
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))  # تغییر به ۵۰۰۱
    app.run(host="0.0.0.0", port=port, debug=True)