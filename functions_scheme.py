import re
import json

def clean_response(content):
        resp = content.split(" ")
        clean_res =""
        for word in resp:
            new_word=""
            for char in word:
                if char !="*":
                    new_word += char
            word = new_word
            clean_res += word.replace("\n", " ") +" "
        
        return clean_res
            
def weather(resp):
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
                "arguments": parsed_json,          # The arguments as a JSON object
            }
        except json.JSONDecodeError as error:
            # If there's an error in parsing the JSON, print the error
            print(f"Error parsing function arguments: {error}")
            return None

        # If no match is found, return None
    return None

print(weather('<function=get_current_weather>{"latitude":30.5, "longitude":77.9,"Comment":"Please hold on for a moment."}')['arguments']['latitude'])
