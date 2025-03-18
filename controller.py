# Controller - Verbindet Model & View

from model import ChatbotModel
from view import ChatbotView
import random


class ChatbotController:
    """Verwaltet die Kommunikation zwischen Model und View."""

    def __init__(self, model_path):
        self.model = ChatbotModel(model_path)
        self.view = ChatbotView(self)

    def process_message(self, user_input):
        """Verarbeitet die Nutzereingabe und gibt eine Antwort zurück."""
        predicted_tag = self.model.predict(user_input)
        response_options = [
            resp for tag, resp in self.model.responses if tag == predicted_tag
        ]
        response = (
            random.choice(response_options)
            if response_options
            else "Ich verstehe dich leider nicht."
        )
        self.view.display_message("Bot", response)

    def run(self):
        """Startet die GUI."""
        self.view.run()
