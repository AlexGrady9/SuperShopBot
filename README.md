# SuperShopBot

A soulful Telegram shop bot built with Python and aiogram.

---

## ✨ Features
- Warm greeting and intuitive main menu
- Browse products by category (with photos, prices, and descriptions)
- Seamless order flow: collects name, phone, and delivery address
- Payment emulation (easy to adapt for real payments)
- Order status notifications (accepted, paid, shipped)
- Collects user feedback after purchase
- Simple admin panel: view new orders and reviews
- Clean, well-tested codebase

## 🚀 Quick Start
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

## 🗂️ Project Structure
- `bot.py` — entry point
- `handlers/` — message and command handlers
- `services/` — business logic for products and orders
- `data/` — product and order data (JSON)
- `admin/` — admin panel handlers
- `tests/` — unit tests for services

## 🛒 Adding Products
Edit the file `data/products.json` (see example structure inside).

## 🧪 Testing
Run all tests:
```bash
pytest
```

## 📦 Dependencies
- aiogram
- (see requirements.txt for full list)

## 🌱 Contributing
Pull requests and ideas are welcome! This project is a great starting point for your own shop bot or portfolio.

## 🙏 Acknowledgements
Thanks to everyone who inspires clean code and friendly bots.

## 📋 Portfolio Note
This project is designed to showcase:
- Clean architecture and modularity
- Professional English code and comments
- Realistic commit history
- User-friendly UX and error handling

---

Happy coding! If you enjoyed this bot, feel free to star the repo or reach out for collaboration.
