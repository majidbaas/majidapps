from flask import Blueprint, render_template, request, redirect, url_for, session
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

food_bp = Blueprint('food', __name__, 
                    template_folder=os.path.join(BASE_DIR, 'templates'), 
                    static_folder=os.path.join(BASE_DIR, 'static'))

food_bp.secret_key = "food_secret_2024"

# ===== بارگذاری داده =====
def load_recipes():
    data_path = os.path.join(BASE_DIR, 'data', 'recipes.json')
    print(f"📂 Loading recipes from: {data_path}")
    
    if not os.path.exists(data_path):
        print(f"❌ File not found: {data_path}")
        return []
    
    with open(data_path, encoding='utf-8') as f:
        recipes = json.load(f)['recipes']
        print(f"✅ Loaded {len(recipes)} recipes")
        return recipes

# ===== تابع جستجو =====
def find_recipes_by_ingredients(user_ingredients, recipes):
    """
    پیدا کردن غذاهایی که حداقل ۳۰٪ از موادشان با مواد کاربر تطابق دارد
    """
    user_ingredients = [ing.strip().lower() for ing in user_ingredients if ing.strip()]
    print(f"🔍 User ingredients: {user_ingredients}")
    
    results = []
    
    for recipe in recipes:
        recipe_ingredients = [ing.lower() for ing in recipe['ingredients']]
        
        # محاسبه تعداد مواد مشترک
        common = set(user_ingredients) & set(recipe_ingredients)
        match_percent = (len(common) / len(recipe_ingredients)) * 100
        
        print(f"   Recipe: {recipe['name']} - Common: {len(common)}/{len(recipe_ingredients)} = {match_percent:.1f}%")
        
        # اگر حداقل ۳۰٪ مواد تطابق داشت، پیشنهاد بده
        if match_percent >= 30:
            results.append({
                'name': recipe['name'],
                'ingredients': recipe['ingredients'],
                'instructions': recipe['instructions'],
                'prep_time': recipe['prep_time'],
                'difficulty': recipe['difficulty'],
                'match_percent': round(match_percent, 0),
                'missing_ingredients': list(set(recipe_ingredients) - set(user_ingredients))
            })
    
    print(f"✅ Found {len(results)} matching recipes")
    results.sort(key=lambda x: x['match_percent'], reverse=True)
    return results

# ===== صفحه اصلی =====
@food_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ingredients_raw = request.form.get('ingredients', '')
        
        # تبدیل جداکننده‌ها
        ingredients_raw = ingredients_raw.replace('،', ',').replace(';', ',').replace('؛', ',')
        ingredients_list = [ing.strip() for ing in ingredients_raw.split(',') if ing.strip()]
        
        print(f"📝 Form submitted: {ingredients_list}")
        
        if not ingredients_list:
            return render_template('index.html', error='لطفاً حداقل یک ماده وارد کنید.')
        
        session['ingredients'] = ingredients_list
        return redirect(url_for('food.result'))  # ← تغییر مسیر به food.result
    
    return render_template('index3.html')

# ===== صفحه نتیجه =====
@food_bp.route('/result')
def result():
    ingredients = session.get('ingredients', [])
    print(f"📋 Session ingredients: {ingredients}")
    
    if not ingredients:
        return redirect(url_for('food.index'))  # ← تغییر مسیر به food.index
    
    recipes = load_recipes()
    
    if not recipes:
        return render_template(
            'result.html',
            ingredients=ingredients,
            results=[],
            total_recipes=0,
            error="هیچ دستور پختی در پایگاه داده وجود ندارد."
        )
    
    results = find_recipes_by_ingredients(ingredients, recipes)
    
    return render_template(
        'result.html',
        ingredients=ingredients,
        results=results,
        total_recipes=len(results)
    )

# ===== بخش تست لوکال (اختیاری) =====
if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.secret_key = "food_secret_2024"
    app.register_blueprint(food_bp, url_prefix='/food')
    
    port = int(os.environ.get("PORT", 5002))
    app.run(host="0.0.0.0", port=port, debug=True)