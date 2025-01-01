
# PDF Assistant Bot

## Overview

The PDF Assistant Bot is a Telegram bot that helps users extract text from PDF files and answer questions about the content using Llama 2, a powerful language model. The bot is designed to be user-friendly and efficient, providing accurate responses based on the content of the provided PDF.

## Features

- Extracts text from PDF files.
- Creates a context from the extracted text using Llama 2.
- Answers user questions based on the PDF content.
- Supports remote work and can be deployed on servers.
- Utilizes modern technologies such as `aiohttp` for asynchronous HTTP requests.

## Technologies Used

- Python
- Telegram Bot API
- PyPDF2
- aiohttp
- asyncio
- Pathlib

## Prerequisites

- Python 3.7 or higher
- Telegram Bot Token
- Llama 2 API running locally

## Setup

1. **Clone the repository:**

    ```sh
    git clone https://github.com/your-repo/pdf-assistant-bot.git
    cd pdf-assistant-bot
    ```

2. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

3. **Configure your Telegram bot token:**

    Replace the placeholder token in the `TelegramBot` class with your actual Telegram bot token:

    ```python
    bot = TelegramBot('YOUR_TELEGRAM_BOT_TOKEN')
    ```

4. **Ensure the Llama 2 API is running locally:**

    The bot interacts with the Llama 2 API running on `http://localhost:11434`. Make sure the API is up and running before starting the bot.

## Running the Bot

To start the bot, run the following command:

```sh
python bot.py
```

You should see the message "🤖 Bot is running..." indicating that the bot is active and ready to receive messages.

## Usage

1. **Start the bot:**

    Send the `/start` command to the bot to initiate a conversation.

2. **Send a PDF file:**

    Upload a PDF file to the bot. The bot will download and process the file, extracting the text content.

3. **Ask questions:**

    Once the PDF is processed, you can ask any questions related to the content of the PDF. The bot will provide answers based on the extracted text.

4. **Reset the conversation:**

    If you want to reset the conversation and start with a new PDF, use the `/cancel` command.

## Command Reference

- `/start` - Initiate the conversation with the bot.
- `/help` - Display help information on how to use the bot.
- `/cancel` - Reset the conversation and start with a new PDF.

## Error Handling

If the bot encounters any issues, it will provide an appropriate error message. Common errors include:

- Uploading a non-PDF file.
- Issues with extracting text from the PDF.
- Problems with communicating with the Llama 2 API.

## Contributing

Contributions are welcome! If you have any ideas for improvements or find any bugs, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

By using this bot, you can efficiently extract and query information from PDF documents, making it a valuable tool for various applications and industries. Enjoy using the PDF Assistant Bot!
