# Albañil - A prompt-driven application bootstrapper

Albañil is a personal application builder that helps you create applications based on a set of specifications provided by the user. It generates the file structure and code for the application based on the given specifications.

## Prerequisites

Before using Albañil, make sure you have the following:

- Python 3.x installed on your system.
- The required Python packages installed. You can install them by running the following command:

  ```shell
  pip install -r requirements.txt
  ```

## Getting Started

1. Clone the repository:

   ```shell
   git clone https://github.com/gultar/albanil.git
   cd albanil
   ```

2. Install the dependencies:

   ```shell
   pip install -r requirements.txt
   ```

3. Set up the environment variables:

   Create a `.env` file in the project directory and provide the following variables:

   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

   Replace `your_openai_api_key` with your OpenAI API key.

4. Run the application:

   ```shell
   python albanil.py [-f FILE] [-y]
   ```

   The optional arguments are as follows:

   - `-f FILE` or `--file FILE`: Specify a `.md` file to use as the value of the `spec` variable.
   - `-y` or `--yes`: Accept all created files automatically without user confirmation.

   If the `-f` option is not provided, the application will prompt you to provide the details of the application you want to create.

## Usage

1. Run the application using the command mentioned in the "Getting Started" section.

2. The application will display the specifications of the application and ask you to provide the filepaths and their descriptions in a JSON key/value pair format.

3. Enter the JSON data containing the filepaths and descriptions. The application will create the file structure of the application in the `./generated` folder.

4. For each file in the file structure, the application will prompt you to write the code for the file. Only the code should be provided without any explanation, acknowledgement, comments, or markdown styling.

5. After writing the code for a file, the application will create the file and save the code content to it.

6. If the `-y` option is provided, the application will automatically proceed with each file without asking for user confirmation. Otherwise, you will be asked to confirm whether you want to proceed with each file.

7. Once all the files have been created, the application will display a message indicating the completion of the file creation process.

## License

This project is licensed under the [MIT License](LICENSE).