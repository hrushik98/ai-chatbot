


import streamlit as st
import os
import openai


openai.api_key =  st.secrets['API_KEY']

st.title("Cleverbot")
st.header("created by @Hrush1k")
if st.button('Go to website'):
    
   st.write('<script>window.open("https://www.google.com","_blank");</script>', unsafe_allow_html=True)

st.text("")
if st.button("to do list"):

    st.write("""
To do list:
1. Improve the User Interface  ✅ 
2. Fix issue with remembering chat history ✅ 
2. Take care of punctuation ✅ 
3. Make it feel more chat-like 
4. Implement Internet search (via, google or bing) 
5. Integrate human voice for input 
6. Take care of token limit ✅ 
""")
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



