# Albañil - An AI-powered application bootstrapper

This script is designed to create the file structure of a complex application based on the provided specifications. It uses the LangChain library to interact with the language model and generate the necessary code for each file in the structure.

## Requirements

- Python 3.x
- LangChain library
- dotenv library

## Setup

1. Install the required dependencies by running the following command:

```shell
pip install langchain python-dotenv
```

2. Create a `.env` file in the same directory as the script and add the following line, replacing `OPENAI_API_KEY` with your OpenAI API key:

```plaintext
OPENAI_API_KEY=<your_openai_api_key>
```

## Usage

1. Create a Python script and copy the provided script into it.

2. Modify the `specs` variable to include the desired application specifications.

3. Run the script using the following command:

```shell
python your_script_name.py
```

4. The script will prompt you to provide the file structure of the application based on the specifications. Follow the instructions and input the requested information.

5. The script will generate the file structure and create the necessary files based on the provided specifications.

6. Once the script completes, you will find the application file structure and files in the specified directory.

## Notes

- This script utilizes the LangChain library, which interfaces with the ChatGPT language model. The model generates the code for each file based on the provided specifications.

- The generated code is written directly to the corresponding files. Please ensure that the file paths and content are correct before running the script.

- The script uses the dotenv library to load environment variables from the `.env` file. Make sure to provide your OpenAI API key in the `.env` file for the script to work properly.

- The script makes use of the `os` and `re` modules for file operations and regular expression matching, respectively. These modules are imported and used within the script.

- The script will pause for 10 seconds after writing each file to allow time for rate limiting and prevent excessive API requests.

- If any errors occur during file creation or writing, error messages will be displayed in the console.

Please refer to the script comments and specifications for further details on its functionality and customization.