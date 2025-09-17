
# SuperShopBot

Telegram shop bot written in Python (aiogram).

## Features
- Friendly greeting and main menu with product categories
- Browse and search products by category (photo, price, description, Buy button)
- Place orders (collects name, phone, delivery address)
- Payment emulation (or payment link for real use)
- Order status notifications (accepted, paid, shipped)
- Collects user feedback after purchase
- Simple admin panel: view new orders and reviews

## Quick Start
1. Install Python 3.8+
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your Telegram bot token in the `BOT_TOKEN` environment variable or directly in `bot.py`
4. Run the bot:
   ```bash
   python bot.py
   ```

## Project Structure
- `bot.py` — entry point
- `handlers/` — message and command handlers
- `services/` — business logic for products and orders
- `data/` — product and order data (JSON)
- `admin/` — admin panel handlers
- `tests/` — unit tests for services

## Adding Products
Edit the file `data/products.json` (see example structure inside).

## Dependencies
- aiogram

## Environment Example
```
BOT_TOKEN=your_bot_token_here
```
