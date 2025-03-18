# Startet die Anwendung

from controller import ChatbotController

if __name__ == "__main__":
    chatbot = ChatbotController("ChatbotTraining.csv")
    chatbot.run()
