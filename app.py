import tkinter as tk
import genanki
import os
from dotenv import load_dotenv
import openai
from tqdm import tqdm
import random

#define an api caller function
def API_caller(prompt):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"[[Use Q and A format]]. Create spanish anki flashcards based on the following text, be extensive: \n" + "'" + prompt + "'\n",
        max_tokens=2000,
        temperature=0.9,
        )
        print("\n\nprompt to generate anki from: \n\n"+ prompt)
        print("\n\n response:\n\n" + response.choices[0].text)
        return response.choices[0].text

#define a function to generate an anki deck
def generate_deck(Response_list):
    global deck_name, deck_id, questions, answers

    # Process the response list and populate questions and answers lists
    for text in Response_list:
        start = 0
        while True:
            index_q = text.find("Q:", start)
            if index_q == -1:
                break
            index_a = text.find("A:", index_q)
            question = text[index_q+len("Q:"):index_a].strip()
            answer = text[index_a+len("A:"):text.find("Q:",index_a)].strip()
            questions.append(question)
            answers.append(answer)
            start = index_a

    def confirm_and_close():
        global deck_name, deck_id, questions, answers

        deck_name = text_box2.get("1.0", "end-1c")
        window2.destroy()

        # Initialize the deck with the name given by the user and a random deck ID
        random_suffix = int(random.randint(0, 10**8))
        deck_id = random_suffix
        deck = genanki.Deck(deck_id, deck_name)

        # Initialize the model
        model = genanki.Model(
                1607392319,
                'Simple Model',
                fields=[
                        {'name': 'Question'},
                        {'name': 'Answer'},
                ],
                templates=[
                        {
                                'name': 'Card 1',
                                'qfmt': '{{Question}}',
                                'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
                        },
                ])

        # Initialize the note
        for i in range(len(questions)):
            my_note = genanki.Note(
                    model=model,
                    fields=[questions[i], answers[i]]
            )
            deck.add_note(my_note)

        # Generate the deck
        genanki.Package(deck).write_to_file(deck_name + '.apkg')

    window2 = tk.Tk()
    window2.title("Deck Name")
    window2.minsize(300, 100)
    window2.resizable(False, False)
    text_box2 = tk.Text(window2, height=1, width=30, font=("Arial", 12), wrap="word")
    text_box2.pack()
    confirm_button = tk.Button(window2, text="Confirm", command=confirm_and_close)
    confirm_button.pack()
    window2.mainloop()

# Define a function to open the .env file and write the API key
def open_api_key_file():
    # Define a function to be called when the "Confirm" button is clicked
    def confirm_and_close():
        # Access the global variable api_key
        global api_key
        # Get the content of the text box (API key entered by the user)
        api_key = text_box2.get("1.0", "end-1c")
        # Close the API key input window
        window2.destroy()
        # Open the .env file in write mode
        with open(".env", "w") as f:
                # Write the API key to the .env file
                f.write("OPENAI_API_KEY=" + api_key)

    # Create a new window to input the API key
    window2 = tk.Tk()
    window2.title("API Key")
    window2.minsize(300, 100)
    window2.resizable(False, False)

    # Create a text box for entering the API key
    text_box2 = tk.Text(window2, height=1, width=30, font=("Arial", 12), wrap="word")
    text_box2.pack()

    # Create a "Confirm" button to save the entered API key
    confirm_button = tk.Button(window2, text="Confirm", command=confirm_and_close)
    confirm_button.pack()

    # Start the API key input window's main event loop
    window2.mainloop()

# Declare global variables
deck_name = ""
deck_id = 0
questions = []
answers = []

#initialize the window
window = tk.Tk()
window.title("Anki Deck Generator")

#set the minimum size of the window
window.minsize(1000, 800)

#make the window resizable
window.resizable(True, True)

# initialize the button to enter the API key
api_key_button = tk.Button(window, text="Enter API Key", command=open_api_key_file)
api_key_button.pack()

# initialize the text box for the user to input their flashcard prompt
text_box = tk.Text(window, height=20, width=100, font=("Arial", 12), wrap="word")
text_box.pack()

# initialize a text box for displaying the response generated by the API call
response_box = tk.Text(window, height=20, width=100, font=("Arial", 12), wrap="word")
response_box.pack()

# initialize the API caller button that triggers the OpenAI API call
api_caller_button = tk.Button(window, text="GPT", command=lambda: response_box.insert("1.0", API_caller(text_box.get("1.0", "end-1c"))))
api_caller_button.pack()

# initialize a list to store the responses generated by the OpenAI API calls
Openai_responses = []

# initialize the "add" button to append the response to the list of responses and to delete both the text box and the response box once the button is clicked
add_button = tk.Button(window, text="Add", command=lambda: [Openai_responses.append(response_box.get("1.0", "end-1c")), text_box.delete("1.0", "end-1c"), response_box.delete("1.0", "end-1c")])
add_button.pack()

# initialize the "generate" button to generate the flashcard deck from the list of responses
generate_button = tk.Button(window, text="Generate", command=lambda: (generate_deck(Openai_responses), Openai_responses.clear()))
generate_button.pack()

#run the window
window.mainloop()






