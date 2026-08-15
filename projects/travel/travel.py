from flask import Blueprint, render_template, request, redirect, session , url_for
import json
import os
import uuid
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

travel_bp = Blueprint('travel', __name__, 
                         template_folder=os.path.join(BASE_DIR, 'templates'), 
                         static_folder=os.path.join(BASE_DIR, 'static'))
                         
                         
               


# ===== بارگذاری داده =====
def load_data():
    # مسیر فایل data.json را به صورت مطلق و بر اساس محل فایل travel.py بساز
    data_path = os.path.join(BASE_DIR, 'data.json')
    
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"DATA FILE NOT FOUND at {data_path}")
    
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

            items_list.append({
                "name": item["name"],
                "icon": item.get("icon", ""),
                "count": item.get("default_count", 1),
                "description": item.get("description", ""),
                "priority": item.get("priority", "")
            })

        if items_list:

            result[category["title"]] = {
                "icon": category.get("icon", "📦"),
                "items": items_list
            }

    return result
# ===== صفحه اصلی =====
@travel_bp.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        session["form"] = request.form.to_dict()
        return redirect(url_for("travel.review"))

    return render_template(
        "index2.html",
        form=session.get("form")
    )
    # ===== چک لیست های من =====

@travel_bp.route("/my-lists")
def my_lists():
    return render_template("travel_lists.html")
    
    
    
    
# ===== صفحه بررسی =====
@travel_bp.route("/review", methods=["GET"])
def review():
    form = session.get("form")
    if not form:
        return redirect(url_for("travel.index"))
    travel_type_map = {
        "solo": "انفرادی",
        "family": "خانوادگی"
    }

    transport_map = {
        "plane": "هواپیما",
        "train": "قطار",
        "car": "خودرو",
        "bus": "اتوبوس",
        "ship": "کشتی",
        "motor": "موتور",
        "taxi": "تاکسی"
    }

    hotel_map = {
        "hotel": "هتل",
        "villa": "ویلا",
        "suite": "سوئیت",
        "hostel": "هاستل",
        "camp": "کمپ",
        "eco": "بوم‌گردی",
        "familyHome": "منزل اقوام",
        "my_villa": "ویلای شخصی"
    }

    season_map = {
        "spring": "بهار",
        "summer": "تابستان",
        "autumn": "پاییز",
        "winter": "زمستان"
    }

    budget_map = {
        "economic": "اقتصادی",
        "medium": "متوسط",
        "luxury": "لاکچری"
    }

    travel_type = travel_type_map.get(form["travel_type"], form["travel_type"])

    hotel = hotel_map.get(form["hotel_type"], form["hotel_type"])

    transport = transport_map.get(form["transport"], form["transport"])

    season = season_map.get(form["season"], form["season"])

    budget = budget_map.get(form["budget"], form["budget"])

    return render_template(
    "review.html",
    form=form,

    travel_type=travel_type,
    hotel=hotel,
    transport=transport,
    season=season,
    budget=budget,

    city=form["city_fa"],
    stay_days=form["stay_days"],
    adult=form["adult_count"],
    child=form["child_count"]
)

# ===== صفحه نتیجه =====
@travel_bp.route("/result", methods=["POST"])
def result():
    form = session.get("form")
    if not form:
        return redirect(url_for("travel.index"))

    travel_type_fa = {
        "solo": "به‌صورت انفرادی",
        "family": "به‌همراه خانواده"
    }

    transport_fa = {
        "plane": "با هواپیما",
        "train": "با قطار",
        "car": "با خودرو",
        "motor": "با موتور",
        "taxi": "با تاکسی",
        "bus": "با اتوبوس",
        "ship": "با کشتی"
        
    }

    season_fa = {
        "spring": "در بهار",
        "summer": "در تابستان",
        "autumn": "در پاییز",
        "winter": "در زمستان"
    }

    name = form.get("name") or "کاربر"
    travel_type = form.get("travel_type")
    transport = form.get("transport")
    season = form.get("season")
    city = form.get("city_fa", "")

    try:
        stay_days = int(form.get("stay_days", 1))
    except (TypeError, ValueError):
        stay_days = 1

    checklist = generate_checklist(form)
    print(checklist)
    title = (
        f"چک‌لیست سفر {name} "
        f"{travel_type_fa.get(travel_type , "")} "
        f"{transport_fa.get(transport, "")} "
        f"{season_fa.get(season, "")} "
        f"به {city} ({stay_days} شب اقامت)"
    )

    session.pop("form", None)
    
    
    checklist_id = str(uuid.uuid4())
   
    return render_template(
        "travel_result.html",
        checklist=checklist,
        title=title,
        checklist_id=checklist_id

    )