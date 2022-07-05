from parser import get_data
from translate import Translator
from db_dispatcher import DbDispatcher


# data = get_data()

data = ["On display? I eventually had to go down to the cellar to find them.",
          "That's the display department.",
          "With a flashlight.",
          "Ah, well the lights had probably gone.",
          "So had the stairs.",
          "But look, you found the notice didn't you?",
          "Yes, said Arthur, yes I did. It was on display in the bottom of a locked filing cabinet stuck in a disused lavatory with a sign on the door saying 'Beware of the Leopard'"]

translator = Translator(to_lang="ru")

# Сделать запись в бд

for phrase in data:
    print(f'{phrase}\t{translator.translate(phrase)}')
