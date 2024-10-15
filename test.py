import requests
import json
import os
import re
import time
import functions

api_url = "http://127.0.0.1:11434/api/chat"

weatherTool = functions.weatherTool

#Use the function '{weatherTool["name"]}' to '{weatherTool["description"]}':
toolPrompt = f"""
You have access to the following functions:

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

def initial_response(question):
    payload = {
        "model": "llama3-groq-tool-use",
        "messages":[
            {
                "role": "system",
                "content": toolPrompt,
            },
            {
                "role": "user",
                "content": "What is the weather in Tokyo?",
            },
            {
                "role": "assistant",
                "content": '<function=get_current_weather>{"latitude":35, "longitude":139}</function>'
            },
            {
                "role": "user",
                "content": question,
            }
        ],
        "stream": False,
        "option":[{"main_gpu":0,"num_gpu":1}],
        "keep_alive":"60m"
    }

    start = time.time()
    response = requests.post(api_url, json=payload, stream=False)
    end = time.time()
    raw_response = response.json()
    print(raw_response['message']['content'])
    #try:r̥
    #    fn_calls = str(raw_response).replace("[TOOL_CALLS] ", "")
    #    print (raw_response,fn_calls)
    #except Exception as e:
    #    print (raw_response, None, e, (end-start))
    print(end-start)
    return raw_response['message']['content']

response = initial_response("Hey how are you doing?",functions.definitions)


def func_call(resp):
    function_regex = r"<function=(\w+)>(.*?)</function>"

    match = re.search(function_regex,response)

    if match:
        function_name, args_string = match.groups()

        try:
            # Try to parse the arguments as a JSON object
            args = json.loads(args_string)
            return {
                "function": function_name,  # The name of the function
                "arguments": args,          # The arguments as a JSON object
            }
        except json.JSONDecodeError as error:
            # If there's an error in parsing the JSON, print the error
            print(f"Error parsing function arguments: {error}")
            return None

        # If no match is found, return None
        return None
    
print(func_call(response))