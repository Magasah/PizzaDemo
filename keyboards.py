from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from typing import List


def main_menu_keyboard(cart_total: int = 0) -> InlineKeyboardMarkup:
    btn_pizzas = InlineKeyboardButton(text="🍕 Пиццы", callback_data="category:pizzas")
    btn_snacks = InlineKeyboardButton(text="🍟 Закуски", callback_data="category:snacks")
    btn_drinks = InlineKeyboardButton(text="🥤 Напитки", callback_data="category:drinks")
    btn_cart = InlineKeyboardButton(text=f"🛒 Корзина ({cart_total} TJS)", callback_data="cart:view")

    rows: List[List[InlineKeyboardButton]] = [
        [btn_pizzas, btn_snacks, btn_drinks],
        [btn_cart]
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def product_navigation_keyboard(category: str, index: int, total: int, product_id: str, price: int, cart_total: int) -> InlineKeyboardMarkup:
    left_cb = f"product:{category}:{max(0, index-1)}"
    right_cb = f"product:{category}:{min(total-1, index+1)}"

    btn_left = InlineKeyboardButton(text="⬅️", callback_data=left_cb)
    btn_page = InlineKeyboardButton(text=f"{index+1}/{total}", callback_data="noop")
    btn_right = InlineKeyboardButton(text="➡️", callback_data=right_cb)
    btn_add = InlineKeyboardButton(text=f"➕ В корзину - {price} TJS", callback_data=f"add:{product_id}")
    btn_cart = InlineKeyboardButton(text=f"🛒 Корзина ({cart_total} TJS)", callback_data="cart:view")
    btn_back = InlineKeyboardButton(text="🏠 В главное меню", callback_data="back:menu")

    rows: List[List[InlineKeyboardButton]] = [
        [btn_left, btn_page, btn_right],
        [btn_add],
        [btn_cart, btn_back]
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def cart_keyboard() -> InlineKeyboardMarkup:
    btn_checkout = InlineKeyboardButton(text="💳 Оформить тестовый заказ", callback_data="cart:checkout")
    btn_clear = InlineKeyboardButton(text="🗑 Очистить", callback_data="cart:clear")
    btn_back = InlineKeyboardButton(text="🏠 Назад", callback_data="back:menu")

    rows: List[List[InlineKeyboardButton]] = [
        [btn_checkout, btn_clear],
        [btn_back]
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)
