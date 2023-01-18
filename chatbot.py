


import streamlit as st
import os
import openai
from bs4 import BeautifulSoup as bs
from googlesearch import search
import wolframalpha
import requests
session = requests.Session()
session.headers['User-Agent']
my_headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 14685.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.4992.0 Safari/537.36",
              "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"}
#2 openai.api_key = "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"
openai.api_key = st.secrets['API_KEY2']
client = wolframalpha.Client("HYGK4Y-T5TL57KJ8H")

st.title("Created by @Hrush1k")
if st.button("View Code"):
    st.write(f'''
    <a target="_self" href="https://github.com/hrushik98/ai-chatbot">
        <button>
            github
        </button>
    </a>
    ''',
    unsafe_allow_html=True
)
st.text("")
if st.button("to do list"):

    st.write("""
To do list:
1. Improve the User Interface  ✅ 
2. Take care of punctuation
3. Make it feel more chat-like
4. Implement Internet search (via, google or bing) 
5. Integrate human voice for input 
6. Take care of token limit
""")
st.text("")
input_question = st.text_input("enter the message: ")
l1 = []


def internet_search(question):

  #1 openai.api_key = "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" #dec12 lfqa api key
  openai.api_key = st.secrets['API_KEY1']
  con = ""
  urls = []
  passages = []
  query = question
  for j in search(query, num=10, stop=10, pause=2):
    urls.append(j)
  file_name = "text-data"
  for url in urls:
    result = session.get(url, headers = my_headers)
    doc = bs(result.content, "html.parser")
    contents = doc.find_all("p")
    for content in contents:
      passages.append(content.text)
      con = con + content.text + "\n"
  with open('./{}.txt'.format(file_name), mode='wt', encoding='utf-8') as file:
      file.write(con)
  #the edited code
  passages2 = []
  i = 0
  for x in range(1,11):
    i = i
    Z = ""
    P = ""
    while len(Z) <=80:
      P += (passages[i])
      Z = P.split()
      i+=1
    passages2.append(P)
  from rank_bm25 import BM25Okapi
  from sklearn.feature_extraction import _stop_words
  import string
  from tqdm.autonotebook import tqdm
  import numpy as np

  def bm25_tokenizer(text):
      tokenized_doc = []
      for token in text.lower().split():
          token = token.strip(string.punctuation)

          if len(token) > 0 and token not in _stop_words.ENGLISH_STOP_WORDS:
              tokenized_doc.append(token)
      return tokenized_doc

  tokenized_corpus = []
  for passage in tqdm(passages2):
      tokenized_corpus.append(bm25_tokenizer(passage))

  bm25 = BM25Okapi(tokenized_corpus)

  bm25_scores = bm25.get_scores(bm25_tokenizer(query))
  top_n = np.argpartition(bm25_scores, -10)[-10:]
  bm25_hits = [{'corpus_id': idx, 'score': bm25_scores[idx]} for idx in top_n]
  bm25_hits = sorted(bm25_hits, key=lambda x: x['score'], reverse=True)

  bm25_passages = []
  for hit in bm25_hits:
    bm25_passages.append(passages2[hit["corpus_id"]])
  try:

    response = openai.Completion.create(
      
        model="curie:ft-personal-2022-12-12-13-15-37",
        prompt = "Imagine an AI agent that can generate human-like text based on the Customer query on the Dialogue History and Supporting Texts. The information on the Supporting Texts can be used to reinforce the AI's response. It can provide information on a wide range of topics, answer questions, and engage in conversation on a variety of subjects including history, science, literature, art, and current events. It can provide information on basic facts to more complex topics. If one has a question about a specific topic, It'll do it's best to provide a relevant and accurate response. It can also generate text in a variety of styles and formats, depending on the task at hand. It can write narratives, descriptions, articles, reports, letters, emails, poems, stories and many other types of texts. \n\n###\n\nDialogue History:\nCustomer: "+str(query)+"\n\nSupporting Texts:\nSupporting Text 1: "+str(bm25_passages[0])+"\nSupporting Text 2: "+str(bm25_passages[1])+"\nSupporting Text 3: "+str(bm25_passages[2])+"\nSupporting Text 4: "+str(bm25_passages[3])+"\n\nAgent Response:"+"\nSupporting Text 5: "+str(bm25_passages[4])+"\n\nAgent Response:"+"\nSupporting Text 6: "+str(bm25_passages[5])+"\n\nAgent Response:",
        temperature=0.7,
        max_tokens=500,
        top_p=0.3,
        frequency_penalty=2,
        presence_penalty=0,
        stop = ['Supporting Text','Agent']
  )
    ans2 = response['choices'][0]['text']
    return ans2



  except:

    st.warning("Error")


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

prompt = """Given the query, you have to figure out if you need WolframAlpha to solve it. Answer only either "Yes" or "No" and nothing else. 
You have to use WolframAlpha if the query is about info like movie reviews, movie ratings, weather, date etc.., the topics that change with time. 
You have to also use WolframAlpha if the query has mathematical symbols like "+","/","^","-","%" etc... but not if it's a word problem involving mathematics.
Query: """ +str(input_question)
def estimator(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    openai_result = response['choices'][0]['text']
    openai_result = str(openai_result).replace("\n", "")
    return openai_result 


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
        # answer = ask(question)
        if print(estimator(input_question)) == "No":
            answer = ask(question)
            st.header(answer)
            writetocsvb(answer)
        else:
            try:

                res = client.query(input_question)
                answer = next(res.results).text
                st.header(answer)
                writetocsvb(answer)
            except:
                answer = print(internet_search(input_question))
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



