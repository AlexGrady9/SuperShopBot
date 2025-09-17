
import logging
from typing import Any
from services import product_service
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram import Router, types, F

router = Router()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@router.message(Command("orders"))
@router.message(F.text.lower() == "my orders")
async def show_orders(message: types.Message) -> None:
    """
    Display the user's orders. (Stub for demonstration.)
    In a real project, you would fetch and display the user's order history here.
    """
    logger.info(
        f"[HANDLER] show_orders called. User: {getattr(message.from_user, 'id', None)}, Text: '{message.text}'")
    await message.answer("You don't have any orders yet. But every journey starts with a first step! 🚀")


@router.message(Command("feedback"))
@router.message(F.text.lower() == "feedback")
async def feedback(message: types.Message) -> None:
    """
    Handle user feedback. (Stub for demonstration.)
    In a real project, you would collect and store user feedback here.
    """
    logger.info(
        f"[HANDLER] feedback called. User: {getattr(message.from_user, 'id', None)}, Text: '{message.text}'")
    await message.answer("Thank you for sharing your thoughts! Your feedback makes me better every day. 💌")
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class OrderStates(StatesGroup):
    """
    States for the order process.
    """
    waiting_for_name: State = State()
    waiting_for_phone: State = State()
    waiting_for_address: State = State()


def build_category_keyboard(categories: list[str]) -> types.ReplyKeyboardMarkup:
    """
    Build a reply keyboard with product categories.
    """
    return types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text=cat)] for cat in categories],
        resize_keyboard=True
    )


def is_valid_phone(phone: str) -> bool:
    """
    Simple phone validation. You can improve this with regex for real projects.
    """
    return phone.isdigit() and 7 <= len(phone) <= 15


def is_category_message(message: types.Message) -> bool:
    """
    Check if the message text matches a product category.
    """
    if not message.text:
        return False
    categories = product_service.get_categories()
    return message.text.strip().lower() in {cat.strip().lower() for cat in categories}


@router.message(Command("start"))
@router.message(Command("menu"))
async def cmd_start(message: types.Message) -> None:
    """
    Greet the user and show the main menu with product categories.
    """
    try:
        categories = product_service.get_categories()
        logger.info(f"Categories: {categories}")
        if not categories:
            await message.answer("Sorry, there are no product categories available right now. Please check back soon!")
            return
        keyboard = build_category_keyboard(categories)
        await message.answer(
            "Hello! 👋\nI'm your personal shop assistant. Please choose a product category below:",
            reply_markup=keyboard
        )
    except Exception as e:
        logger.exception("Error in cmd_start")
        await message.answer("Oops! Something went wrong. Please try again later.")


@router.message(is_category_message)
async def show_products(message: types.Message) -> None:
    """
    Display products for the selected category.
    """
    try:
        logger.info(f"User sent: '{message.text}'")
        categories = product_service.get_categories()
        normalized_categories = {
            cat.strip().lower(): cat for cat in categories}
        user_text = (message.text or '').strip().lower()
        if user_text in normalized_categories:
            category = normalized_categories[user_text]
            products = product_service.get_products_by_category(category)
            for product in products:
                btn = types.InlineKeyboardButton(
                    text=f"Buy {product['name']}", callback_data=f"buy_{product['id']}")
                markup = types.InlineKeyboardMarkup(inline_keyboard=[[btn]])
                caption = f"<b>{product['name']}</b>\nPrice: {product['price']}\n{product['description']}"
                await message.answer_photo(product['photo'], caption=caption, reply_markup=markup)
    except Exception as e:
        logger.exception("Error in show_products")
        await message.answer("Sorry, I couldn't show the products right now. Please try again later.")


@router.callback_query(F.data.startswith("buy_"))
async def start_order(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Start the order process after the user selects a product.
    """
    user_id = getattr(callback.from_user, 'id', None)
    logger.info(f"CallbackQuery: buy_. User: {user_id}, Data: {callback.data}")
    if not callback.data or not callback.message:
        logger.warning(
            f"CallbackQuery: missing data or message. User: {user_id}")
        await callback.answer("Something went wrong. Please try again.", show_alert=True)
        return
    try:
        product_id = int(callback.data.split('_')[1])
    except (IndexError, ValueError):
        logger.warning(
            f"CallbackQuery: invalid product_id. User: {user_id}, Data: {callback.data}")
        await callback.answer("Invalid product data.", show_alert=True)
        return
    await state.update_data(product_id=product_id)
    await callback.message.answer(
        "Wonderful choice! What's your name?",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(OrderStates.waiting_for_name)
    current_state = await state.get_state()
    logger.info(
        f"CallbackQuery: set_state to waiting_for_name. User: {user_id}, State: {current_state}")
    await callback.answer()


@router.message(OrderStates.waiting_for_name)
async def ask_phone(message: types.Message, state: FSMContext) -> None:
    """
    Ask the user for their phone number after receiving their name.
    """
    current_state = await state.get_state()
    user_id = getattr(message.from_user, 'id', None)
    logger.info(
        f"Handler: waiting_for_name. User: {user_id}, State: {current_state}, Text: '{message.text}'")
    categories = product_service.get_categories()
    text = message.text.strip() if message.text else ""
    if not text:
        await message.answer("Please enter your name (it can't be empty). If you made a mistake, just type your name again.")
        return
    if text.lower() in {cat.strip().lower() for cat in categories}:
        await message.answer("Please enter your name, not a category name. If you made a mistake, just type your name again.")
        return
    await state.update_data(name=text)
    await message.answer("Could you share your phone number?")
    await state.set_state(OrderStates.waiting_for_phone)


@router.message(OrderStates.waiting_for_phone)
async def ask_address(message: types.Message, state: FSMContext) -> None:
    """
    Ask the user for their delivery address after receiving their phone number.
    """
    current_state = await state.get_state()
    user_id = getattr(message.from_user, 'id', None)
    logger.info(
        f"Handler: waiting_for_phone. User: {user_id}, State: {current_state}, Text: '{message.text}'")
    phone = message.text.strip() if message.text else ""
    if not is_valid_phone(phone):
        await message.answer("Please enter a valid phone number (digits only, 7-15 characters). If you made a mistake, just type your phone number again.")
        return
    await state.update_data(phone=phone)
    await message.answer("Almost done! What's your delivery address?")
    await state.set_state(OrderStates.waiting_for_address)


@router.message(OrderStates.waiting_for_address)
async def confirm_order(message: types.Message, state: FSMContext) -> None:
    """
    Confirm the order and finish the FSM process.
    """
    current_state = await state.get_state()
    user_id = getattr(message.from_user, 'id', None)
    logger.info(
        f"Handler: waiting_for_address. User: {user_id}, State: {current_state}, Text: '{message.text}'")
    address = message.text.strip() if message.text else ""
    if not address:
        await message.answer("Please enter a valid delivery address. If you made a mistake, just type your address again.")
        return
    await state.update_data(address=address)
    data = await state.get_data()
    summary = (
        f"Thank you, {data['name']}!\n"
        f"Order details:\nProduct ID: {data['product_id']}\nPhone: {data['phone']}\nAddress: {data['address']}\n"
        "Your order has been received! (Payment is simulated for demo purposes)"
    )
    await message.answer(summary, reply_markup=types.ReplyKeyboardRemove())
    await state.clear()


# Fallback handler for any unhandled messages (should always be last!)
@router.message(F.text & ~F.text.startswith("/"))
async def fallback(message: types.Message, state: FSMContext) -> None:
    """
    Fallback for any unrecognized messages. Gently guides the user back to the menu.
    """
    current_state = await state.get_state()
    user_id = getattr(message.from_user, 'id', None)
    logger.info(
        f"Fallback handler. User: {user_id}, State: {current_state}, Text: '{message.text}'")
    await message.answer("I'm sorry, I didn't quite catch that. Please use the menu or type /start to begin again. 🌟")
