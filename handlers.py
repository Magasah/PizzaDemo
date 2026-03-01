import asyncio
from typing import Dict

from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command

import data
import keyboards

# In-memory carts: {user_id: {product_id: qty}}
CARTS: Dict[int, Dict[str, int]] = {}


def get_cart(user_id: int) -> Dict[str, int]:
    return CARTS.setdefault(user_id, {})


def add_to_cart(user_id: int, product_id: str) -> None:
    cart = get_cart(user_id)
    cart[product_id] = cart.get(product_id, 0) + 1


def clear_cart(user_id: int) -> None:
    CARTS[user_id] = {}


def cart_total_amount(user_id: int) -> int:
    cart = get_cart(user_id)
    total = 0
    for pid, qty in cart.items():
        prod = find_product(pid)
        if prod:
            total += prod["price"] * qty
    return total


def find_product(product_id: str):
    for cat, items in data.CATALOG.items():
        for item in items:
            if item["id"] == product_id:
                return item
    return None


async def start_handler(message: Message):
    cart_total = cart_total_amount(message.from_user.id)
    caption = "🟠 Добро пожаловать в демо-бота доставки еды!\nВыберите категорию, чтобы сделать заказ."
    await message.answer_photo(photo=data.WELCOME_BANNER, caption=caption, reply_markup=keyboards.main_menu_keyboard(cart_total))


async def callback_router(callback: CallbackQuery):
    data_str = callback.data or ""
    user_id = callback.from_user.id

    # category:<key>
    if data_str.startswith("category:"):
        _, cat = data_str.split(":", 1)
        items = data.CATALOG.get(cat, [])
        if not items:
            await callback.answer("Пустая категория.")
            return
        # Show first item
        index = 0
        try:
            await callback.answer()
        except Exception:
            pass
        await show_product(callback, cat, index)
        return

    if data_str.startswith("product:"):
        # product:category:index
        _, cat, idx = data_str.split(":", 2)
        idx = int(idx)
        try:
            await callback.answer()
        except Exception:
            pass
        await show_product(callback, cat, idx)
        return

    if data_str.startswith("add:"):
        _, pid = data_str.split(":", 1)
        add_to_cart(user_id, pid)
        await callback.answer("✅ Добавлено в корзину!", show_alert=False)
        # update reply_markup cart total if message present
        if callback.message:
            total = cart_total_amount(user_id)
            # if currently viewing product, rebuild its keyboard
            # Try to parse current message caption to find product context - easier: just update main menu button if present
            try:
                await callback.message.edit_reply_markup(reply_markup=keyboards.main_menu_keyboard(total))
            except Exception:
                # ignore if cannot edit
                pass
        return

    if data_str == "cart:view":
        cart = get_cart(user_id)
        if not cart:
            await callback.answer("Ваша корзина пуста.")
            # show main menu
            await callback.message.edit_caption(caption="Ваша корзина пуста.", reply_markup=keyboards.main_menu_keyboard(0))
            return

        try:
            await callback.answer()
        except Exception:
            pass

        # build receipt
        lines = ["🛒 Ваша корзина:"]
        idx = 1
        for pid, qty in cart.items():
            prod = find_product(pid)
            if prod:
                lines.append(f"{idx}. {prod['name']} x{qty} - {prod['price']*qty} TJS")
                idx += 1
        total = cart_total_amount(user_id)
        lines.append(f"Итого: {total} TJS")
        text = "\n".join(lines)
        # edit message to show receipt (use text)
        try:
            await callback.message.edit_text(text, reply_markup=keyboards.cart_keyboard())
        except Exception:
            await callback.message.answer(text, reply_markup=keyboards.cart_keyboard())
        return

    if data_str == "cart:clear":
        clear_cart(user_id)
        await callback.answer("🗑 Корзина очищена.")
        # return to main menu
        try:
            await callback.message.edit_text("Корзина очищена.", reply_markup=keyboards.main_menu_keyboard(0))
        except Exception:
            await callback.message.answer("Корзина очищена.", reply_markup=keyboards.main_menu_keyboard(0))
        return

    if data_str == "cart:checkout":
        clear_cart(user_id)
        await callback.answer()
        await callback.message.edit_text("🎉 Тестовый заказ успешно оформлен!\n\n💡 Это демонстрационный бот из портфолио. Если хотите такого же для своего бизнеса — напишите разработчику!")
        return

    if data_str == "back:menu":
        total = cart_total_amount(user_id)
        try:
            await callback.message.edit_caption(caption="🟠 Добро пожаловать в демо-бота доставки еды!\nВыберите категорию, чтобы сделать заказ.", reply_markup=keyboards.main_menu_keyboard(total))
        except Exception:
            try:
                await callback.message.edit_text("🟠 Добро пожаловать в демо-бота доставки еды!\nВыберите категорию, чтобы сделать заказ.", reply_markup=keyboards.main_menu_keyboard(total))
            except Exception:
                await callback.message.answer("🟠 Добро пожаловать в демо-бота доставки еды!\nВыберите категорию, чтобы сделать заказ.", reply_markup=keyboards.main_menu_keyboard(total))
        return

    # noop or unmatched
    await callback.answer()


async def show_product(callback: CallbackQuery, category: str, index: int):
    items = data.CATALOG.get(category, [])
    if not items:
        await callback.answer("Пусто")
        return
    index = max(0, min(index, len(items)-1))
    item = items[index]
    caption = f"<b>{item['name']}</b>\n{item['description']}\n\nЦена: <b>{item['price']} TJS</b>"
    cart_total = cart_total_amount(callback.from_user.id)

    # Try to edit media (replace photo + caption). Handle Telegram errors gracefully.
    kb = keyboards.product_navigation_keyboard(category, index, len(items), item['id'], item['price'], cart_total)
    try:
        media = InputMediaPhoto(media=item['image'], caption=caption, parse_mode='HTML')
        await callback.message.edit_media(media=media, reply_markup=kb)
        return
    except TelegramBadRequest as e:
        msg = str(e).lower()
        # Common problems: Telegram cannot fetch URL, wrong content type, or message has no text to edit.
        if "failed to get http" in msg or "wrong type of the web page content" in msg or "failed to get http url content" in msg:
            # Telegram couldn't fetch the image by URL — send a new photo message instead.
            await callback.message.answer_photo(photo=item['image'], caption=caption, reply_markup=kb)
            return
        if "there is no text in the message to edit" in msg:
            # Message likely contains media only — try to edit caption instead.
            try:
                await callback.message.edit_caption(caption, reply_markup=kb)
                return
            except Exception:
                await callback.message.answer_photo(photo=item['image'], caption=caption, reply_markup=kb)
                return
        # Other TelegramBadRequest: fallback to sending a new photo
        await callback.message.answer_photo(photo=item['image'], caption=caption, reply_markup=kb)
        return
    except Exception:
        # Generic fallback: try edit_caption, else send new photo
        try:
            await callback.message.edit_caption(caption, reply_markup=kb)
        except Exception:
            await callback.message.answer_photo(photo=item['image'], caption=caption, reply_markup=kb)


def register_handlers(dp: Dispatcher):
    dp.message.register(start_handler, Command(commands=["start"]))  # /start
    dp.callback_query.register(callback_router)


if __name__ == "__main__":
    print("This module is not intended to be run directly. Use main.py")
