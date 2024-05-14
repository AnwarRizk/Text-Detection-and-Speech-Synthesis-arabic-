import easyocr
from gtts import gTTS
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import arabic_reshaper
import pygame

def recognize_text(image_path, language='ar'):
    # Initialize the OCR reader with Arabic as the language
    reader = easyocr.Reader([language])

    # Read the text from the image
    result = reader.readtext(image_path)

    # Extract text from the result
    text = ' '.join([entry[1] for entry in result])

    return text

def text_to_speech(text, language='ar'):
    # Generate speech from the text
    speech = gTTS(text=text, lang=language)

    # Save the speech as an MP3 file
    speech.save("output.mp3")

def select_image():
    # Open a file dialog to select an image
    file_path = filedialog.askopenfilename()
    if file_path:
        # Update the image label
        update_image(file_path)
        # Recognize text from the selected image
        recognized_text = recognize_text(file_path)
        # Convert recognized text to speech
        text_to_speech(recognized_text)
        # Reshape the text to display it correctly
        recognized_text = arabic_reshaper.reshape(recognized_text)
        # Reverse the text to display it correctly
        recognized_text = recognized_text[::-1]
        # Display the recognized text
        text_label.config(text="Recognized Text:\n" + recognized_text, font=('Arial', 14, 'bold'), justify='center', wraplength=600)

def update_image(file_path):
    # Open and display the selected image
    image = Image.open(file_path)
    image.thumbnail((600, 600)) # Resize the image to fit in the window
    photo = ImageTk.PhotoImage(image) # Create a PhotoImage object
    image_label.config(image=photo) # Update the image label
    image_label.image = photo # Keep a reference

def play_mp3():
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()

def pause_resume_mp3():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()

def stop_mp3():
    pygame.mixer.music.stop()

# Initialize pygame
pygame.init()

# Create main application window
root = tk.Tk() # Create the root window
root.title("Text Recognition and Speech Synthesis")

# Set colors
background_color = '#23272f'
button_color = '#4CAF50'
text_color = '#c87f52'

# Set background color
root.configure(bg=background_color)

# Create widgets
# Button to select an image
select_button = tk.Button(root, text="Select Image", command=select_image, font=('Arial', 12, 'bold'), bg=button_color, fg='white')

# Label to display the selected image
image_label = tk.Label(root, bg=background_color)

# Label to display the recognized text
text_label = tk.Label(root, text="Recognized Text:\n", font=('Arial', 12, 'bold'), bg=background_color, fg=text_color)

# Button to play the generated MP3
play_button = tk.Button(root, text="Read Aloud 🎤", command=play_mp3, font=('Arial', 12, 'bold'), bg='#f97c3a', fg='white')

# Button to pause and resume the MP3
pause_resume_button = tk.Button(root, text="Pause/Resume", command=pause_resume_mp3, font=('Arial', 12, 'bold'), bg='#3170c1', fg='white')

# Button to stop the MP3
stop_button = tk.Button(root, text="Stop", command=stop_mp3, font=('Arial', 12, 'bold'), bg='#913a49', fg='white')

# Layout widgets
select_button.pack(pady=50, padx=200) # Display the select button
image_label.pack() # Display the selected image
text_label.pack(pady=20) # Display the recognized text
play_button.pack(pady=10) # Display the play button
pause_resume_button.pack(pady=10) # Display the pause & resume button
stop_button.pack(pady=10) # Display the stop button

# Run the application
root.mainloop()
