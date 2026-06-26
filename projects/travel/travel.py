from flask import Blueprint, render_template, request, redirect, session
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

travel_bp = Blueprint('travel', __name__, 
                         template_folder=os.path.join(BASE_DIR, 'templates'), 
                         static_folder=os.path.join(BASE_DIR, 'static'))
                         
                         
@travel_bp.route("/static/<path:filename>")
def static_files(filename):
    print(f"📂 Static file requested: {filename}")
    return send_from_directory('static', filename)
                         
                         

travel_bp.secret_key = "1642300Mb"

# ===== بارگذاری داده =====
def load_data():
    # مسیر فایل data.json را به صورت مطلق و بر اساس محل فایل travel.py بساز
    data_path = os.path.join(BASE_DIR, 'data.json')
    
    # این خط رو اضافه کن تا در لاگ سرور ببینی که مسیر چیست (برای دیباگ)
    print(f"Looking for data.json at: {data_path}")
    
    if not os.path.exists(data_path):
        raise Exception(f"DATA FILE NOT FOUND at {data_path}")
    
    with open(data_path, encoding="utf-8") as f:
        return json.load(f)

def rule_match(rules, form):
    for key, values in rules.items():
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

# ===== صفحه اصلی =====
@travel_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session["form"] = request.form.to_dict()
        return redirect("/travel/review")
   
    return render_template("index2.html", form=session.get("form"))
# ===== صفحه بررسی =====
@travel_bp.route("/review", methods=["GET"])
def review():
    form = session.get("form")
    if not form:
        return redirect("/travel/")

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

# ===== صفحه نتیجه =====
@travel_bp.route("/result", methods=["POST"])
def result():
    form = session.get("form")
    if not form:
        return redirect("/travel/")

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