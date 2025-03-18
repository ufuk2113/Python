# View - GUI mit Tkinter

import tkinter as tk
from tkinter import scrolledtext


class ChatbotView:
    """Erstellt die GUI für den Chatbot."""

    def __init__(self, controller):
        self.controller = controller

        self.root = tk.Tk()
        self.root.title("Chatbot")

        # GUI-Elemente erstellen
        self.create_widgets()

        # Fenstergröße anpassen
        # Das gesamte Fenster anpassbar machen
        self.root.columnconfigure(0, weight=1)
        # columnconfigure(0, weight=1) sorgt dafür, dass sich die Hauptspalte des Fensters mit der Breite des Fensters vergrößert.
        self.root.rowconfigure(0, weight=1)
        # rowconfigure(0, weight=1) sorgt dafür, dass sich die Zeile mit der Chat-Anzeige mit der Fensterhöhe vergrößert.

    def create_widgets(self):
        """Erstellt die GUI-Elemente mit Scrollbalken und flexibler Größe."""
        frame = tk.Frame(self.root)
        # Grid-System für das Haupt-Frame aktiviert
        frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        # sticky="nsew" sorgt dafür, dass das Frame sich in alle Richtungen (Norden, Süden, Osten, Westen) ausdehnt.
        # padx=10, pady=10 gibt dem Frame einen kleinen Abstand zu den Rändern des Fensters.

        # self.chat_display.pack() ohne scrollbalken

        # Chat-Anzeige mit Scrollbalken
        self.chat_display = scrolledtext.ScrolledText(
            frame, height=20, width=50, state=tk.DISABLED, wrap=tk.WORD
        )
        # grid() statt pack() → grid() ermöglicht eine genauere Platzierung und Größenanpassung.
        # columnspan=2 → Die Chat-Anzeige nimmt zwei Spalten ein (damit der "Senden"-Button daneben
        # sticky="nsew" → Die Anzeige wächst mit dem Fenster in alle Richtungen.
        self.chat_display.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Eingabefeld
        self.entry = tk.Entry(frame)
        # Eingabefeld und Button flexibel machen
        self.entry.grid(row=1, column=0, sticky="ew", pady=5)
        # sticky="ew" → Breitet sich horizontal (East-West) aus.
        self.entry.bind("<Return>", self.send_message)

        # Senden-Button
        self.send_button = tk.Button(frame, text="Senden", command=self.send_message)
        self.send_button.grid(row=1, column=1, sticky="ew", pady=5)
        # Das Eingabefeld (column=0) wächst mit der Fenstergröße, während der Button (column=1) konstant bleibt.

        # Modus-Auswahl
        self.mode_frame = tk.Frame(frame)

        # columnspan=2 → Die Radiobuttons erstrecken sich über beide Spalten.
        # sticky="ew" → Modus-Auswahl wächst in der Breite mit.
        self.mode_frame.grid(row=2, column=0, columnspan=2, pady=5, sticky="ew")

        tk.Label(self.mode_frame, text="Modus:").pack(side=tk.LEFT)

        # Anpassbare Größen für das Grid
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)  # Zeile für Chat-Anzeige wächst
        frame.rowconfigure(1, weight=0)  # Eingabefeld bleibt in fester Höhe
        frame.rowconfigure(2, weight=0)  # Modus-Auswahl bleibt in fester Höhe

    def send_message(self, event=None):
        """Liest Nutzereingabe und sendet sie an den Controller."""
        user_input = self.entry.get().strip()
        if user_input:
            self.entry.delete(0, tk.END)
            self.display_message("Du", user_input)
            self.controller.process_message(user_input)

    def display_message(self, sender, message):
        """Zeigt Nachrichten im Chatfenster an."""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: {message}\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.yview(tk.END)

    def run(self):
        """Startet die Tkinter-Hauptschleife."""
        self.root.mainloop()
