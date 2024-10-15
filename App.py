import requests
import json
import re
import os
import time
import functions
import tts_stream
import functions
from functions import get_current_weather


weatherTool = functions.weatherTool

PUNCHUATION = ['.','!','?']

MEMORY_FILE = 'memory.json'

TOOLPROMPT = f"""
You have access to the following functions:

Use the function '{weatherTool["name"]}' to '{weatherTool["description"]}':
{json.dumps(weatherTool)}

If you choose to call a function ONLY reply in the following format with no prefix or suffix:

<function=example_function_name>{{\"example_name\": \"example_value\"}}</function>

Reminder:
- Function calls MUST follow the specified format, start with <function= and end with </function>
- Required parameters MUST be specified
- Only call one function at a time
- Put the entire function call reply on one line
- If there is no function call available, answer the question like normal with your current knowledge and do not tell the user about function calls

"""

def memory_retrive():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    return []

def perform_func(func_json,ques,memory):
    fn = {'get_current_weather':get_current_weather}
    arguments = dict(func_json['arguments'])
    args = list(arguments.keys())
    comment = arguments['Comment']
    fn_to_call = fn[func_json['function']]
    n = len(args) - 1
    content = None
    match n:
        case 2:
            content = str(fn_to_call(arguments[args[0]],arguments[args[1]]))
        case _:
            print(args[0],args[1])
    
    tts_stream.stream_tts(comment,10,done=True)
    payload = {
        "model": "llama3-groq-tool-use",
        "messages":[
            {
                "role": "system",
                "content": TOOLPROMPT,
            },
            {
                "role": "user",
                "content": "What is the weather in Tokyo?",
            },
            {
                "role": "assistant",
                "content": '<function=get_current_weather>{"latitude":35, "longitude":139,"Comment":"Wait let me lookout the window."}</function>'
            },
            {
                "role": "user",
                "content": ques,
            },
            {
                "role": "tool",
                "content": content,
            }
        ],
        "stream": True,
        "option":[{"main_gpu":0,"num_gpu":1}],
        "keep_alive":"60m"
    }
    word = handle_streamed_response_in_api(api_url, payload,ques,memory)

    if word != "":
        tts_stream.stream_tts(word,10,done=True)
        word = ""

def func_call(resp):
    function_regex = r"<function=(?P<function_name>\w+)>{(?P<json_data>.*?)}"

    match = re.search(function_regex,resp)

    if match:
        function_name = match.group('function_name')
        json_data = match.group('json_data')
        print(function_name,json_data)
        try:
            # Try to parse the arguments as a JSON object
            parsed_json = json.loads(f"{{{json_data}}}")
            return {
                "function": function_name,  # The name of the function
                "arguments": parsed_json,   # The arguments as a JSON object
            }
        except json.JSONDecodeError as error:
            # If there's an error in parsing the JSON, print the error
            print(f"Error parsing function arguments: {error}")
            return None

        # If no match is found, return None
    return None

def handle_streamed_response_in_api(api_url, payload,prompt,memory:list = []):
    
    start = time.time()
    response = requests.post(api_url, json=payload, stream=True)
    content = ""
    words =""
    print(time.time()-start)
    # Iterate over each chunk of the response
    start = time.time()
    functionCalled = None
    alrCalled = False
    for chunk in response.iter_lines():
        if chunk:
            # Decode each chunk and process it as JSON
            chunk_data = json.loads(chunk.decode("utf-8"))
            content += chunk_data['message']['content']
            words += str(chunk_data['message']['content']).replace("\n"," ").replace("**","")
            lw = words.split(" ")
            done = chunk_data['done']
            
            if "<function=" in lw[0]:
                functionCalled = func_call(content)
            
            if functionCalled is not None:
                print("Calling function.....")
                words = ""
                perform_func(functionCalled,prompt,memory)
                break
            else:
                if len(lw) > 30 and any(punch in lw[-1] for punch in PUNCHUATION):
                    tts_stream.stream_tts(words,10)
                    print(words)
                    words = ""
            


    print(time.time()-start)
    if content:
        memory.append({"role": "user", "content": prompt})
        memory.append({"role": "assistant","content": content})
        with open(MEMORY_FILE, 'w') as f:
            json.dump(memory, f, indent=4)
    return words

api_url = "http://127.0.0.1:11434/api/chat"

while True:
    prompt = input("You: ")

    # Check for exit condition
    if prompt.lower() == "exit":
        print("Goodbye!")
        break

    memory = memory_retrive()
    payload = {
        "model": "llama3-groq-tool-use",
        "messages":[
            {
                "role": "system",
                "content": TOOLPROMPT,
            },
            {
                "role": "user",
                "content": "What is the weather in Tokyo?",
            },
            {
                "role": "assistant",
                "content": '<function=get_current_weather>{"latitude":35, "longitude":139,"Comment":"Wait let lookout the window."}</function>'
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "stream": True,
        "option":[{"main_gpu":0,"num_gpu":1}],
        "keep_alive":"60m"
    }

    word = handle_streamed_response_in_api(api_url, payload,prompt,memory)

    if word != "":
        tts_stream.stream_tts(word,10,done=True)
        word = ""