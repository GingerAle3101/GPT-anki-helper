'''1. Define the API_caller function that takes in a prompt and an API key as arguments.
2. Set the OpenAI API key with the given api_key.
3. Create the messages list containing the user message and insert the system message at the beginning.
4. Make a ChatCompletion API call with the messages list and store the response.
5. Print the messages and the response.
6. Return the response content.

7. Define the generate_deck function that takes in a Response_list as an argument.
8. Create a loop to process the Response_list and populate questions and answers lists.
9. Define the confirm_and_close function inside generate_deck.
10. Get the user-provided deck name and destroy the window.
11. Initialize a new deck with the given deck name and a random deck ID.
12. Create a genanki model for the Anki deck.
13. Create a loop to initialize notes with the questions and answers.
14. Add the notes to the deck.
15. Generate the Anki deck and write it to a file.

16. Define the open_api_key_file function.
17. Define a function, confirm_and_close, that gets the user-provided API key and destroys the window.
18. Create a new window for the user to input their API key.
19. Initialize a text box for the user to enter their API key.
20. Create a Confirm button that saves the API key and starts the main event loop for the window.

21. Initialize the main window for the Flashcard Generator application.
22. Initialize the button to enter the API key.
23. Create frames for the text boxes.
24. Initialize a text box for the user to input their flashcard prompt.
25. Initialize a text box for displaying the API-generated response.
26. Initialize the API caller button that triggers the OpenAI API call.
27. Initialize the Add button that appends the response to Openai_responses and clears the text boxes.
28. Initialize the Generate button that calls the generate_deck function and clears Openai_responses.
29. Run the main event loop for the window.'''

# Import the necessary libraries
import tkinter.ttk as ttk
import tkinter as tk
import genanki
import openai
import random

# Set global variables
Openai_responses = []
deck_name = ""
deck_id = ""
questions = []
answers = []

# Define the API_caller function that takes in a prompt and an API key as arguments
def API_caller(prompt, api_key):
    openai.api_key = api_key
    
    messages = [{"role": "user", "content": prompt}]
    messages.insert(0, {"role": "system", "content": "Only answer in Q: and A: format. You are a helpful bot that can only answer in Q: and A: format. Please do not use any other format. Remember the 20 rules of knowledge since the content of your response will be used to memorize knowledge. Generate based on the text below."})
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    print("\n\nMessages sent:\n")
    for message in messages:
        print(f"{message['role'].capitalize()}: {message['content']}")
    
    print("\n\nResponse:\n\n" + response.choices[0]['message']['content'])
    return response.choices[0]['message']['content']

# Define the generate_deck function that takes in a Response_list as an argument
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
    window2.resizable(True, True)

    text_box2 = tk.Text(window2, height=1, width=30)
    text_box2.grid(row=0, column=0, padx=10, pady=10)

    confirm_button = tk.Button(window2, text="Confirm", command=confirm_and_close)
    confirm_button.grid(row=0, column=1, padx=10, pady=10)

    window2.mainloop()

# Define the open_api_key_file function
def open_api_key_file():
    global api_key
    # Define a function to be called when the "Confirm" button is clicked
    def confirm_and_close():
        global api_key
        # Get the content of the text box (API key entered by the user)
        api_key = text_box2.get("1.0", "end-1c")
        # Close the API key input window
        window2.destroy()

    # Create a new window to input the API key
    window2 = tk.Tk()
    window2.title("API Key")
    window2.minsize(300, 100)
    window2.resizable(True, True)

    # Create a text box for entering the API key
    text_box2 = tk.Text(window2, height=1, width=30, font=("Arial", 12), wrap="word")
    text_box2.pack()

    # Create a "Confirm" button to save the entered API key
    confirm_button = tk.Button(window2, text="Confirm", command=confirm_and_close)
    confirm_button.pack()

    # Start the API key input window's main event loop
    window2.mainloop()

# Create the main window for the Flashcard Generator application
# Initialize the window
window = tk.Tk()
window.title("Flashcard Generator")
window.configure(bg="white")
window.resizable(True, True)

# Initialize the button to enter the API key using ctk
enter_api_key_button = ttk.Button(window, text="Enter API Key", command=open_api_key_file)
enter_api_key_button.place(relx=0.5, rely=0.1, relwidth=0.2, relheight=0.1, anchor='center')

# Create frames for text boxes
text_box_frame = ttk.Frame(window)
text_box_frame.place(relx=0.5, rely=0.25, relwidth=0.95, relheight=0.25, anchor='center')

response_box_frame = ttk.Frame(window)
response_box_frame.place(relx=0.5, rely=0.55, relwidth=0.95, relheight=0.25, anchor='center')

# Initialize a resizeable text box for the user to input their flashcard prompt
text_box = tk.Text(text_box_frame, height=30, width=120, font=("Arial", 12), wrap="word")
text_box.pack()

# Initialize a resizeable text box for displaying the response generated by the API call
response_box = tk.Text(response_box_frame, height=30, width=120, font=("Arial", 12), wrap="word")
response_box.pack()

# Initialize the API caller button that triggers the OpenAI API call
api_caller_button = ttk.Button(window, text="GPT", command=lambda: (response_box.delete("1.0", "end-1c"), response_box.insert("1.0", API_caller(text_box.get("1.0", "end-1c"), api_key))))
api_caller_button.place(relx=0.5, rely=0.45, anchor='center')

# Initialize the "add" button
add_button = ttk.Button(window, text="Add", command=lambda: [Openai_responses.append(response_box.get("1.0", "end-1c")), text_box.delete("1.0", "end-1c"), response_box.delete("1.0", "end-1c")])
add_button.place(relx=0.5, rely=0.8, anchor='center')

# Initialize the "generate deck" button
generate_deck_button = ttk.Button(window, text="Generate Deck", command=lambda: [generate_deck(Openai_responses), Openai_responses.clear()])
generate_deck_button.place(relx=0.5, rely=0.9, anchor='center')

# Start the main event loop
window.mainloop()



