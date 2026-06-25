import json
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def match_conditions(item, form):
    conditions = item.get("conditions", {})

    for key, value in conditions.items():
        if str(form.get(key)) != str(value):
            return False

    return True


def load_data():
    file_path = os.path.join(BASE_DIR, "data", "data.json")
    print("LOADING FROM:", file_path)

    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)

    print("JSON LOADED:", data)
    return data

def rules_match(rules, form):
    for key, allowed in rules.items():
        value = form.get(key)

        # اگر فرم این فیلد را نداشت، rule را رد نکن
        if value is None:
            continue

        if value not in allowed:
            return False

    return True


def generate_checklist(form):
    data = load_data()
    print("JSON LOADED:", data)
    result = []

    for category in data["categories"]:

        # بررسی قوانین دسته
        if not rules_match(category.get("rules", {}), form):
            continue

        filtered_items = []

        for item in category["items"]:
            if rules_match(item.get("rules", {}), form):
                filtered_items.append(item)
        if not match_conditions(item, form):
            continue

        if filtered_items:
            result.append({
                "title": category["title"],
                "items": filtered_items
            })

    return result
