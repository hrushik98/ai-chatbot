


import streamlit as st
import os
import openai


openai.api_key =  st.secrets['API_KEY']


st.title("Fueza - an AI chatbot")
st.text("created by @Hrush1k")
st.text("")
if st.button("to do list"):

st.text("")
input_question = st.text_input("enter the message: ")
l1 = []


def listToString(s):
    str1 = ""
    for ele in s:
        str1 += ele

    return str1


start_sequence = "\nAI:"
restart_sequence = "\nHuman: "


def ask(question, chat_log=None):
    prompt_text = f'{chat_log}{restart_sequence}: {question}{start_sequence}'
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt_text,
        temperature=0.9,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    story = response['choices'][0]['text']
    return story




import csv


def writetocsvh(question):
    with open("results.csv", "a") as f:
        data = csv.writer(f)
        name = "\nHuman:" + question
        data.writerow([name])
def writetocsvb(question):
    with open("results.csv", "a") as f:
        data = csv.writer(f)
        name = "\nAI:" + question
        data.writerow([name])
    
if st.button("Go"):
    try:
        
        writetocsvh(str(input_question))
        with open("results.csv", 'r') as f:
            data = csv.reader(f)
            for i in data:
                l1.append(i)

        flat_list = []

        for sublist in l1:
            for item in sublist:
                flat_list.append(item)

        question = listToString(flat_list)
        answer = ask(question)
        st.header(answer)
        writetocsvb(answer)
 
    except:
        os.remove("results.csv")
        writetocsvh(str(input_question))
        with open("results.csv", 'r') as f:
            data = csv.reader(f)
            for i in data:
                l1.append(i)

        flat_list = []

        for sublist in l1:
            for item in sublist:
                flat_list.append(item)

        question = listToString(flat_list)
        answer = ask(question)

        st.header(answer)

        writetocsvb(answer)

