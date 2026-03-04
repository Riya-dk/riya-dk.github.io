"""Recipe goals app – find recipes by nutrition goal (TheMealDB API)."""
import random
import re
from urllib.parse import quote
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
MEALDB = "https://www.themealdb.com/api/json/v1/1"

GOAL_INGREDIENTS = {
    "increasing_estrogen": ["tofu", "tempeh", "soy", "edamame", "flax", "chickpeas", "lentils", "beans", "hummus", "sesame", "peas"],
    "gaining_weight": ["chicken", "beef", "salmon", "pasta", "rice", "eggs", "cheese", "milk", "nuts", "avocado", "potato", "oats", "bread", "pork", "lamb", "turkey"],
    "high_protein": ["chicken", "beef", "salmon", "tuna", "eggs", "tofu", "lentils", "chickpeas", "cheese", "pork", "turkey", "lamb"],
}

def get_meals_by_ingredient(ingredient):
    r = requests.get(f"{MEALDB}/filter.php", params={"i": ingredient}, timeout=10)
    if not r.ok:
        return []
    data = r.json()
    return data.get("meals") or []

def get_meal_by_id(meal_id):
    r = requests.get(f"{MEALDB}/lookup.php", params={"i": meal_id}, timeout=10)
    if not r.ok:
        return None
    data = r.json()
    meals = data.get("meals")
    return meals[0] if meals else None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/recipes")
def get_recipes():
    goals = request.args.getlist("goal")[:2]
    cuisine = (request.args.get("cuisine") or "").strip()
    meals = []
    ingredients = []
    for g in goals:
        ingredients.extend(GOAL_INGREDIENTS.get(g, []))
    if not ingredients:
        return jsonify({"recipes": []})
    seen = set()
    for ing in ingredients[:15]:
        for m in get_meals_by_ingredient(ing):
            if m and m.get("idMeal") and m["idMeal"] not in seen:
                seen.add(m["idMeal"])
                meals.append(m)
    random.shuffle(meals)
    results = []
    for m in meals[:30]:
        full = get_meal_by_id(m["idMeal"])
        if not full:
            continue
        if cuisine and (full.get("strArea") or "") != cuisine:
            continue
        results.append({
            "id": full["idMeal"],
            "name": full.get("strMeal", ""),
            "thumb": full.get("strMealThumb", ""),
            "category": full.get("strCategory", ""),
            "area": full.get("strArea", ""),
            "ingredients": [
                (full.get(f"strIngredient{i}") or "").strip() + " " + (full.get(f"strMeasure{i}") or "").strip()
                for i in range(1, 21) if (full.get(f"strIngredient{i}") or "").strip()
            ],
        })
    return jsonify({"recipes": results})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
