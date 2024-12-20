from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler, 
    MessageHandler, 
    filters, 
    ConversationHandler
)
import PyPDF2
from pathlib import Path
import aiohttp  # Changed: Using aiohttp instead of requests
import json
import asyncio

# Conversation states
AWAITING_PDF = 0
AWAITING_QUESTION = 1

# Store PDF content for each user
user_contexts = {}

class PDFProcessor:
    @staticmethod
    def extract_text(pdf_path):
        """Extract text from PDF file"""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")

class LlamaHandler:
    OLLAMA_API_URL = "http://localhost:11434/api/generate"
    
    @staticmethod
    async def create_context(text):
        """Create initial context with the PDF content"""
        try:
            prompt = f"""Please read and understand the following content, then acknowledge that you have processed it:

Content:
{text}

Please respond with 'Content processed successfully' if you have understood the text."""

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    LlamaHandler.OLLAMA_API_URL,
                    json={
                        "model": "llama2",
                        "prompt": prompt,
                        "stream": False
                    }
                ) as response:
                    if response.status == 200:
                        return text
                    else:
                        error_text = await response.text()
                        raise Exception(f"Error from Llama 2: {error_text}")
                
        except Exception as e:
            raise Exception(f"Error creating context: {str(e)}")

    @staticmethod
    async def get_answer(question, context):
        """Get answer from Llama 2 based on context and question"""
        try:
            prompt = f"""Based on the following content, please answer the question. Only use information from the provided content. If the answer cannot be found in the content, say so clearly.

Content:
{context}

Question: {question}

Answer:"""

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    LlamaHandler.OLLAMA_API_URL,
                    json={
                        "model": "llama2",
                        "prompt": prompt,
                        "stream": False
                    }
                ) as response:
                    if response.status == 200:
                        response_json = await response.json()
                        return response_json['response']
                    else:
                        error_text = await response.text()
                        raise Exception(f"Error from Llama 2: {error_text}")
                
        except Exception as e:
            raise Exception(f"Error getting answer: {str(e)}")

class TelegramBot:
    def __init__(self, token):
        self.application = Application.builder().token(token).build()
        self.setup_handlers()

    def setup_handlers(self):
        conv_handler = ConversationHandler(
            entry_points=[
                CommandHandler('start', self.start),
                MessageHandler(filters.Document.PDF, self.handle_pdf)
            ],
            states={
                AWAITING_PDF: [
                    MessageHandler(filters.Document.PDF, self.handle_pdf)
                ],
                AWAITING_QUESTION: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_question)
                ]
            },
            fallbacks=[
                CommandHandler('cancel', self.cancel),
                CommandHandler('help', self.help)
            ]
        )
        
        self.application.add_handler(conv_handler)
        self.application.add_handler(CommandHandler("help", self.help))

    async def start(self, update, context):
        await update.message.reply_text(
            "👋 Hello! I'm your PDF Assistant powered by Llama 2!\n\n"
            "Send me a PDF file, and I'll help you answer questions about its content.\n\n"
            "Commands:\n"
            "/help - Show this help message\n"
            "/cancel - Reset the conversation"
        )
        return AWAITING_PDF

    async def help(self, update, context):
        await update.message.reply_text(
            "📚 How to use this bot:\n\n"
            "1. Send me a PDF file\n"
            "2. Wait while I process it\n"
            "3. Ask any questions about the content\n"
            "4. Use /cancel to reset and start with a new PDF"
        )
        return AWAITING_PDF

    async def handle_pdf(self, update, context):
        try:
            file = update.message.document
            if not file.file_name.lower().endswith('.pdf'):
                await update.message.reply_text("❌ Please send only PDF files!")
                return AWAITING_PDF

            await update.message.reply_text("📥 Downloading and processing your PDF...")
            file_path = Path("temp.pdf")
            pdf_file = await context.bot.get_file(file.file_id)
            await pdf_file.download_to_drive(str(file_path))

            # Extract text
            text = PDFProcessor.extract_text(file_path)
            if not text.strip():
                raise Exception("No text could be extracted from the PDF")

            # Create context with Llama 2
            await update.message.reply_text("🔄 Creating context from your PDF using Llama 2...")
            context_text = await LlamaHandler.create_context(text)
            
            # Store context for this user
            user_id = update.effective_user.id
            user_contexts[user_id] = context_text

            # Cleanup and inform user
            file_path.unlink(missing_ok=True)
            await update.message.reply_text(
                "✅ PDF processed successfully!\n\n"
                "You can now ask me any questions about the content.\n"
                "Type /cancel to reset and start with a new PDF."
            )
            return AWAITING_QUESTION

        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
            return AWAITING_PDF

    async def handle_question(self, update, context):
        user_id = update.effective_user.id
        if user_id not in user_contexts:
            await update.message.reply_text("❌ Please send a PDF file first!")
            return AWAITING_PDF

        try:
            question = update.message.text
            await update.message.reply_text("🤔 Thinking about your question...")
            
            answer = await LlamaHandler.get_answer(question, user_contexts[user_id])
            await update.message.reply_text(answer)
            
            return AWAITING_QUESTION

        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
            return AWAITING_QUESTION

    async def cancel(self, update, context):
        user_id = update.effective_user.id
        if user_id in user_contexts:
            del user_contexts[user_id]
        await update.message.reply_text("🔄 Conversation reset. Send a new PDF to start again!")
        return AWAITING_PDF

    def run(self):
        """Run the bot until stopped"""
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    # Create and run the bot
    bot = TelegramBot('7731699746:AAGhVEnVmY7viPaS2791WqO-4VtLMbSsckc')
    print("🤖 Bot is running...")
    bot.run()

if __name__ == '__main__':
    main()