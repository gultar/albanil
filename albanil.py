import argparse
import os
import re
import json
import time
from dotenv import dotenv_values, load_dotenv
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

load_dotenv()

print("""
   _____  .__ ___.                 .__.__   
  /  _  \ |  |\_ |__ _____    ____ |__|  |  
 /  /_\  \|  | | __ \\__  \  /    \|  |  |  
/    |    \  |_| \_\ \/ __ \|   |  \  |  |__
\____|__  /____/___  (____  /___|  /__|____/
        \/         \/     \/     \/         
""")
print("Welcome to Albañil, your personal application builder!")
print("Be aware that, due to current GPT3.5 rate limits, you may see warnings from OpenAI")
print("¡No te preocupes! It's part of the show, amigo.\n")

# Creating an argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="Specify a .md file to use as the value of the 'spec' variable")
parser.add_argument("-y", "--yes", help="Accepts all created files automatically",
                    action='store_true')
args = parser.parse_args()
is_automatic = args.yes

# Creating a chat prompt template
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("""
    You are a helpful AI programming assistant designed to create applications from a set
    of specifications provided by the user.
    The AI is nearly silent and only provides the information required in the format specified context. 
    The AI provides fully functional code and thinks the creation of the application step-by-step.
    If the AI does not know the answer to a question, it truthfully says it does not know.
    """),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])

# Loading environment variables from a .env file
env = dotenv_values(".env")

# Creating an instance of the ChatOpenAI class
llm = ChatOpenAI(temperature=0, openai_api_key=env["OPENAI_API_KEY"], verbose=True)

# Creating a conversation memory buffer
memory = ConversationBufferMemory(return_messages=True)

# Creating a conversation chain with the prompt, language model, and memory
conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm)

# Application specifications provided as a string
if args.file:
    with open(args.file, 'r') as file:
        specs = file.read()
else:
    specs = input("Please provide the details of the application you want to create:\n")

# Prompt to build the file structure of the application based on the specifications
file_structure_build_prompt = f"""
    I would like you to create the file structure of a complex application I want to build according
    to the specifications that I will provide. You are to ONLY output the
    file structure, not the code itself.
    Can you provide me with the list of filepaths and their description 
    in a JSON key/value pair format, without any explanation, 
    acknowledgment, comment or markdown styling. Don't say anything 
    but the JSON data. Always build the application in the ./generated folder. Always create a new folder within ./generated to contain the application. In the case of keys that are directories, mark them 
    with a / at the end of their dirname, unless is it part of a path to a file. All directory keys have 
    objects as value, and all file keys have strings as values.

    Here is the application specifications and details: {specs}
"""

# Function to create and write content to a file
def create_and_write_file(file_path, content):
    try:
        if file_path == "":
            return

        os.makedirs(os.path.dirname("./" + file_path), exist_ok=True)

        with open(file_path, "w") as file:
            content = re.sub(r"^```[\s\S]*?\n([\s\S]*?)\n```", r"\1", content, flags=re.MULTILINE)
            file.write(content)

        print(f"File created and content saved successfully: {file_path}")
    except Exception as e:
        print(f"Error creating and writing to file: {file_path}")
        print(f"Error message: {str(e)}")

# Function to process each file key by generating code and writing it to the corresponding file
def process_file(file_key):
    file_write_prompt = f"""
        Using the specifications previously provided and the following description.
        Please write the code for the filename that you created earlier. Do not write anything else than
        the code for the file; no acknowledgement, no explanation, no comments, and no markdown styling.

        Please write the code for this file. Only output the code. No comment, no justification, no acknowledgement,
        no markdown styling. Just the code, nothing else. Do not add any ``` markdown delimiters when outputting the code. 

        {file_key}
    """
    reprompt = ""
    while True:
        
        code = conversation.predict(input=file_write_prompt+reprompt)
        create_and_write_file(file_key, code)

        if is_automatic:
            break

        # Ask for user confirmation
        confirmation = input(f"File created: {file_key}. Do you want to proceed with this file? (y/n): ")
        if confirmation.lower() == "y":
            break
        else:
            reprompt = input("Do you want to provide additional specifications?")

        # Retry with ChatGPT
        print(f"Re-prompting ChatGPT for the file: {file_key}")

def walk(obj, prefix="", file_func=None):
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_prefix = f"{prefix}/{key}" if prefix else key
            new_prefix = new_prefix.replace("//", "/")
            if type(value) is dict:
                print(f"Directory: {new_prefix}")
                if value:
                    walk(value, prefix=new_prefix, file_func=file_func)
            else:
                print(f"File: {new_prefix}")
                if file_func is not None:
                    file_func(new_prefix)
    else:
        print(obj, prefix)
        raise ValueError("Invalid object type. Expected dictionary.")

def create_file_structure():
        reprompt = ""
        while True:
            
            print("Building the file structure of the application...")
            # Predicting the file structure using the conversation chain and converting it to JSON
            structure = conversation.predict(input=file_structure_build_prompt+reprompt)
            print(structure)
            structure = json.loads(structure)
            
            # Asking for user confirmation
            if is_automatic:
                confirmation = "y"
            else:
                confirmation = input("Do you want to proceed with the created file structure? (y/n): ")

            if confirmation.lower() == "y":
                return structure
            else:
                reprompt = input("Do you want to add specifications?")
            
                
        
    

def main():
    
    structure = create_file_structure()
     # Walking through the file structure and processing each file
    walk(structure, file_func=process_file)
    print("File creation completed!")

if __name__ == "__main__":
    main()
