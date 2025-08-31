
# Cafe Telegram Bot

A simple Telegram bot for a restaurant that allows users to view the menu, contacts, hot prices, leave feedback, and visit the website. Feedback is saved in a SQLite database and can also be viewed in the bot.

## Features

- View the restaurant menu (`Menu`)
- Get contact information (`Kontakti`)
- Check hot prices (`HOT PRICES`)
- Leave feedback (`Atsauksmes`)
- Visit the restaurant website (`Mūsu tīmekļa vietne`)
- View all feedback using the `/all_feedback` command

## Installation

1. Clone the repository:

```bash
git clone https://github.com/marlonhtml/cafe-telegram-bot.git
cd cafe-telegram-bot
```

Install required packages:

```python
pip install -r requirements.txt
```

Create a .env file with your Telegram bot token:

```python
TELEGRAM_TOKEN=your_bot_token_here
```

Run the bot:

```python
python bot.py
```

## Usage

Start the bot with `/start`.

Click inline buttons to navigate through the menu, contacts, hot prices, or leave feedback.

Use `/all_feedback` to see all collected feedback in the bot.

## Database

The bot uses SQLite to store feedback. The database file users.db will be created automatically when the bot is first run.

Table feedback structure:

`id` (INTEGER, primary key)

`user_id` (INTEGER)

`username` (TEXT)

`feedback` (TEXT)

`date` (TEXT)

## Contributing

This bot is for portfolio purposes.
