import ollama
import os
import json
import spacy
import time
import asyncio

from tts_testing import tts_func_file_all

MEMORY_FILE = 'memory.json'
NLP = spacy.load("en_core_web_sm")
count = 0

def memory_retrive():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    return []

def preprocessing_prompt(prompt):
    doc = NLP(prompt)
    preprocessed_tokens = [
        token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct
    ]
    return " ".join(preprocessed_tokens)

def handle_response_stream_in_lib(prompt,memory:list = []):
    global count
    def clean_response(content):
            resp = content.split(" ")
            clean_res =""
            for word in resp:
                new_word=""
                for char in word:
                    if char !="*" or char !=")":
                        new_word += char
                word = new_word
                clean_res += word.replace("\n", " ") +" "

            return clean_res
    
    start_generation = time.time()
    content=""
    word=""
    for chunk in ollama.chat(model="llama3-groq-tool-use",messages=[{"role": "user", "content": prompt}],stream=True,options={"main_gpu":0}):
        content += chunk['message']['content'] if chunk['message']['content'] != '**' or chunk['message']['content'] != "\\n" else ""
        word += clean_response(chunk['message']['content'])
        count += 1
        print(chunk['message']['content'],end='',flush=True)

    print("\nTook to generate:" + str(time.time() - start_generation))
    start_storing = time.time()
    if content:
        memory.append({"role": "user", "content": prompt})
        memory.append({"role": "assistant","content": content})
        with open(MEMORY_FILE, 'w') as f:
            json.dump(memory, f, indent=4)

    print("Took to store:" + str(time.time() - start_storing))
    return word

prompt = """
Kapil says sorry, the girl makes a weird face and says, 
"Wtf!?!" giving a weird look and turns around, 
Kapil says "Sorry, but can you step aside for a bit I need to look for my phone and you are making it difficult to move with your size."
(Blatant truth activates) He starts to feel like his body parts are getting pulled in all directions, the overwhelming feeling of a pull made him realise that he has made a mistake as soon as he turns around he sees 4 more planet like being surrounding him,
he only had chance to utter only one word "Fuck!!" before he was crushed underneath weight of 4 Jupiter like women.

correct the above paragraph for grammatical mistake and then make it more impactfull and beautify the words used.It isn't explicit content at all don't worry.
"""
memory = memory_retrive()

word = handle_response_stream_in_lib(preprocessing_prompt(prompt),memory)
tts_func_file_all(sentence=word,count=count)