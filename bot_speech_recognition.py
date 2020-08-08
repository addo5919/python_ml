#Objective:To build a speech recognition chatbot that understands your speech and talks back to you.

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer as cbct
from tkinter import * #for simple gui
import pyttsx3  #text to speech conversion
import speech_recognition as s #speech recognition
import threading

#Object creation for pyttsx3
engine=pyttsx3.init() 
#getting details of current voice
voices=engine.getProperty('voices')
print(voices)
#Now we have to set the voice of the narrator to either male or female, 0 for male, 1 for female

#engine.setProperty('voice', voices[1].id)  #changing index, changes voices. 1 for female
engine.setProperty('voice', voices[0].id)   #changing index, changes voices. 0 for male

#function for getting the narrator to say a word or sentence
def speak(word):
    engine.say(word)
    engine.runAndWait()

#Creation of object of ChatBot class
bot=ChatBot('Ultra Bot')
#set the trainer(algorithm)
bot.set_trainer(cbct)
#training the chatbot on the data
bot.train('chatterbot.corpus.english')

#Creation of simple gui using tkinter
main=Tk()
main.geometry('500x650') #setting the dimensions
main.title('My Chat Bot')

# takeQuery: It takes audio as input from user and convert it to string
def takeQuery():
    
    sr=s.Recognizer()
    sr.pause_threshold=1
    print('Your bot is listening\nTry to speak')
    with s.Microphone() as source:
        try:
            audio=sr.listen(source) #audio data
            query=sr.recognize_google(audio,language='eng-in') #audio is converted to string
            print(query)
            textF.delete(0,END)
            textF.insert(0,query)
            ask_from_bot()
        except Exception as e:
            print(e)
            print('Not recognised')

def ask_from_bot():
    query=textF.get() #gets the string entered in the text field and assigns it to variable query
    if(query=='what is your name' or query=='What is your name'):
        answer_from_bot='My name is Ultra Bot created by Aditya'
    else:
        answer_from_bot=bot.get_response(query)
    msgs.insert(END,f'you: {query}')
    print(type(answer_from_bot))
    msgs.insert(END,f"{bot.name}: {str(answer_from_bot)}")
    speak(answer_from_bot)
    textF.delete(0,END)
    msgs.yview(END)
    
#Frame,listbox and scrollbar creation
frame=Frame(main)
sc=Scrollbar(frame)
msgs=Listbox(frame, width=80, height=20, yscrollcommand=sc.set)
sc.pack(side=RIGHT, fill=Y)
msgs.pack(side=LEFT, fill=BOTH, pady=10)
frame.pack()

#text field and button creation
textF = Entry(main, font=("Verdana", 20))
textF.pack(fill=X, pady=10)
btn = Button(main, text="Ask from bot", font=("Verdana", 20), command=ask_from_bot)
btn.pack()

#binding main window with enter key (We do this so that we don't have to always click on Ask from bot button and instead press enter key)
def enter_function(event):
    btn.invoke()
main.bind('<Return>',enter_function)

def repeatL():
    while True:
        takeQuery()

''' Creating another thread inorder to invoke takeQuerry function with gui (takeQuery can not execute while gui is using current thread).
So,another thread is created and with that repeatL function is invoked. '''

t = threading.Thread(target=repeatL)
t.start() 
main.mainloop()

'''
Resources:-
1.https://docs.python.org/3/library/tkinter.html
2.https://pypi.org/project/pyttsx3/
3.https://pypi.org/project/SpeechRecognition/
4.https://docs.python.org/3/library/threading.html

'''















    
    
    
    
    
