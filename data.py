"""Fake catalog data for the demo Dodo-like bot.

Structure:
CATALOG = {
    "pizzas": [ {id,name,description,price,image}, ... ],
    "snacks": [...],
    "drinks": [...]
}
"""

CATALOG = {
    "pizzas": [
        {
            "id": "p1",
            "name": "Пепперони",
            "description": "Сочная пицца с колбасками и хрустящей корочкой.",
            "price": 65,
            "image": "https://picsum.photos/seed/p1/800/600"
        },
        {
            "id": "p2",
            "name": "Маргарита",
            "description": "Классическая Маргарита с томатами и моцареллой.",
            "price": 58,
            "image": "https://picsum.photos/seed/p2/800/600"
        },
        {
            "id": "p3",
            "name": "Четыре сыра",
            "description": "Насыщенная сырная пицца для гурманов.",
            "price": 72,
            "image": "https://picsum.photos/seed/p3/800/600"
        },
        {
            "id": "p4",
            "name": "Барбекю",
            "description": "Пикантная пицца с соусом барбекю и курицей.",
            "price": 75,
            "image": "https://picsum.photos/seed/p4/800/600"
        },
    ],
    "snacks": [
        {
            "id": "s1",
            "name": "Картофель фри",
            "description": "Хрустящая порция картофеля фри.",
            "price": 20,
            "image": "https://picsum.photos/seed/s1/800/600"
        },
        {
            "id": "s2",
            "name": "Куриные наггетсы",
            "description": "Золотистые наггетсы, 6 шт.",
            "price": 28,
            "image": "https://picsum.photos/seed/s2/800/600"
        }
    ],
    "drinks": [
        {
            "id": "d1",
            "name": "Кола",
            "description": "Холодная кола 0.5л.",
            "price": 10,
            "image": "https://picsum.photos/seed/d1/800/600"
        },
        {
            "id": "d2",
            "name": "Лимонад",
            "description": "Освежающий лимонад 0.5л.",
            "price": 12,
            "image": "https://picsum.photos/seed/d2/800/600"
        }
    ]
}

# A nice welcoming banner image (Unsplash)
WELCOME_BANNER = "https://picsum.photos/seed/banner/1200/600"
