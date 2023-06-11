# eval-cbot-dp

A repository for the degree project done by Fabian and Fredric. This repository contains the code that was utilized throughout the project as well as some additional extras such as code used for graphing the results, images, testing code and so forth.

## Installing requirements for Python
```
pip install -r requirements.txt
```

## Training files
For the training data itself, it was retrieved from these repositories: 
1. https://github.com/rushic24/DialoGPT-Finetune
2. https://github.com/Azmarie/GPT2-finetune/tree/main/data

The files in question are ***train_data.json*** and ***test_data.json***, they must be downloaded and put in a folder to be used in relation to the applications here.

Both the aforementioned repos are believed to have utilised the following the repository (which is the original) in turn: 

3. https://github.com/UCSD-AI4H/COVID-Dialogue

## Botkit-related chatbot
Install Node.js: Make sure you have Node.js installed on your system. You can download and install it from the official Node.js website (https://nodejs.org).

After Node.js has been installed in your system, navigate to the botkit folder by using the following command in the terminal:
    ```
    cd botkit
    ```

Having navigated to the botkit directory, next the packages will need to be installed and to do so, run the following command: 
    ```
    npm install
    ```

The packages being installed will allow for the application to be run, and to run the app:
    ```
    node app.js
    ```
Access the app: The app will start running on localhost:4000.

Note: Make sure you have an active internet connection because the app relies on external resources such as Wikipedia and WHO API for fetching information. 

That's it! You should now be able to run the app and interact with the chatbot.

### The code
- The script starts by importing necessary modules, including Botkit for bot functions, Express.js for serving a web interface, socket.io for real-time server-client communication, axios for API requests, cheerio for HTML parsing, and Natural for NLP tasks.
- It defines the path to the training and testing data and the results file.
- It loads the testing and training data from specified JSON files.
- It initializes a Bayes classifier, a machine learning model, using the Natural library.
- The training data consisting of conversations is then added to the classifier, with each user message being treated as a separate document.
- After the classifier is trained, an Express.js server is started and a Socket.io server is attached to it.
- The script serves static files from 'public' and 'node_modules' directories. A Botkit controller is created.
- The Jaccard Similarity function is used to measure the similarity between two sets of data.
- The generateResponse function processes user input, classifies it using the trained model, and generates an appropriate response.

There is also the "client-side" code in which can be found in the public folder, named client.js. This JavaScript script primarily interacts with the server through the Socket.io library and manipulates DOM elements to control the chatbot interface.
**Connection**: The script first establishes a connection with the server using Socket.io.
**Message Sending**: It adds an event listener to a button in the HTML with the ID 'sendButton'. When this button is clicked, it sends a message to the server with the current text value from the input element with the ID 'userInput'. It also creates a new div element in the messages container with the sent message.
**Message Receiving**: It listens for messages from the server. When a message is received, it creates a new div in the messages container with the received message.
**MainMenu Displaying**: A function displayMainMenu is defined to display various options for the user to choose from. When one of these options is selected, a message is sent to the server with the selected option.
**Input Fields**: When an 'input' event is emitted from the server, the script creates an input field for the user to input an illness name or a question.
**Option Selection**: A global function optionSelected is declared. This function is used to handle the various options that the user can select from the main menu. It sends a message to the server with the selected option and also adjusts the visibility of the input field and the send button based on the selected option.
**Message Sending** (again): Another event listener is added to the 'sendButton'. When this button is clicked, it sends a 'userInput' event to the server with the current value of the input field. It also creates a new div in the messages container with the sent message.

Please note that the 'removeHTMLTags' and 'summarizeText' functions are utility functions used to clean up and shorten text before displaying it in the chat. The 'emitUserMessage' function is not currently used in this script.

After the results from testing have been retrieved, considering that there is no BLEU or ROUGE library in JavaScript (to my knowledge), instead the csv files are used in the /extra/testing_code in order to retrieve the BLEU and ROUGE scores which can then be used to analyse the responses.

## Chatterbot-based chatbot 
The Python version used in this instance is 3.8.0 (conda) although 3.7 or higher is recommended.


ChatterBot uses built-in adapter classes to connect to different databases for storing and retrieving conversation data. By default, ChatterBot uses SQLStorageAdapter to connect to SQLite databases, but it also supports MongoDBStorageAdapter for MongoDB databases. Specify the storage adapter in the ChatBot constructor. Next, specify the logic adapters, which determine how the chatbot processes input and generates responses. ChatterBot selects the response with the highest confidence score. Examples of logic adapters include:

    chatterbot.logic.BestMatch: Returns the closest matching response from the chatbot's training data.
    chatterbot.logic.MathematicalEvaluation: Solves basic mathematical problems.
    chatterbot.logic.TimeLogicAdapter: Returns the current time when asked.

Add logic adapters to the constructor like so:
```
bot = ChatBot(
    'Test',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter'
    ],
    database_uri='sqlite:///database.sqlite3')
```

### Training

ChatterBot is trained using the ListTrainer function, which accepts a list of input-response pairs known as a conversation. Import ListTrainer from chatterbot.trainers, create a trainer instance by passing the chatbot instance into the ListTrainer constructor, and start training by calling the train method:

```
from chatterbot.trainers import ListTrainer

trainer = ListTrainer(bot)

conversation = [
    "Hello",
    "Hi there!",
    "How are you doing?",
    "I'm doing great.",
    "That is good to hear",
    "Thank you."
]

trainer.train(conversation)
```

Train the chatbot multiple times with different dialogues to improve the chatbot's responses. In this project, the chatbot was trained using two types of data sources - a list of FAQs related to COVID-19 and a JSON file filled with medical conversation data. The responses are generated using the BestMatch logic adapter with the Levenshtein distance and the most frequent response selection method.

#### Customization
ChatterBot allows for the integration of custom logic adapters and the use of popular machine learning libraries such as TensorFlow, PyTorch, and spaCy for more complex and accurate response generation.

### Imports: 
The script begins by importing necessary packages. Flask is a lightweight web server framework. ChatterBot is a Python library to generate automated responses based on the collection of input and output pairs it is trained on.

- **Data Scraping and Processing**: Two functions, get_faq_from_who and read_and_process_json, are defined for data scraping from a webpage and reading data from a local JSON file respectively. The scraped and processed data are used later for training the bot.

- **ChatBot Training**: The train_bot function is defined to train a given ChatterBot instance on provided list of tuples and FAQ data scraped from the WHO website.

- **Bot Creation and Configuration**: The bot is created using the ChatBot class from ChatterBot, with a SQL storage adapter (using SQLite) and a logic adapter that uses the Levenshtein distance for comparing input statements with known statements. The database is cleared before each run to ensure the bot is trained from scratch every time. The bot is trained first on the English greetings corpus, then on the data read from the training JSON file for COVID-19 related queries and FAQs.

- **Flask App Setup**: A Flask application is set up with two routes. The first route ("/") is the home page that renders a provided HTML file named "index.html". The second route ("/get") is an API endpoint that gets a message from the user as a request parameter, generates a response using the chatbot, and returns that response.

### Running 
To use this code with the base provided by chamkank: https://github.com/chamkank/flask-chatterbot

1. Replace the existing Flask application code (app.py) with this script.

2. Ensure the necessary packages are installed. If not, install them with pip: pip install flask chatterbot chatterbot_corpus pandas requests beautifulsoup4.

3. Run the Flask application. The command is typically python app.py. 

    - Navigate to localhost:5000 (or another port, if you've configured it differently) in your web browser to interact with the chatbot.

    - The bot will provide responses based on its training data and the logic adapter. It will respond with a default message if it doesn't find a suitable response.

Please note that this bot is stateless – it doesn't remember the context of a conversation, and every response it generates is based on the single message input it receives.

### Testing
There is also the testing file called ***test_chatterbot.py***. The testing file used to retrieve the results has the following procedure: 

**An FAQ scraping function is utilised**: 
The get_faq_from_who function scrapes FAQs from the WHO's COVID-19 page. The questions and answers are added to a list of tuples and returned.

There are also evaluation functions related to the Jaccard similarity, BLEU and ROUGE metrics: 
**Evaluation Functions**: The evaluate_bleu_and_rouge and test_chatterbot_with_bleu_and_rouge functions are used for evaluating the bot's performance. The Bot's responses are compared to actual responses using BLEU and ROUGE metrics. The evaluation data is written to a CSV file and the average scores are printed out.

For **data cleaning and loading**: 
The remove_punctuation, jaccard_similarity, read_and_process_json, and load_data_from_json functions are used to clean and load the data for training and testing.

**Bot Training**: 
The bot is instantiated with certain configurations and trained using an English greeting corpus and the list of conversations retrieved from the FAQ and the COVID-19 related dataset.

**Similarity Calculation**: 
The calculate_similarity_score function calculates the Jaccard Similarity, BLEU Score, and ROUGE Scores between the response from the bot and the expected response.

**Bot Testing**: 
The test_chatterbot function tests the bot using some test data and saves the test results (response, expected response, and their similarity scores) into a CSV file. It also measures the response time of the bot.

**Consistency Testing**: 
The test_chatterbot_consistency function tests the bot's consistency by checking its responses to several variations of the same question. It saves the results, including the Jaccard Similarity between responses, into a CSV file.

The queries list contains groups of queries that are different variations of the same question and are used to test the bot's consistency. The bot is tested with these queries at the end of the script.

## DialoGPT-based chatbot 
To utilise the already existing model used in the thesis, download the model from [here](https://drive.google.com/drive/folders/1EVEsc9-lNyaoorEZDm0OU3Tee8Lb6vsy?usp=drive_link) (it is a Google Drive folder as GitHub has a 200MB size limit, and the model is 8GB). 
There will be a bit of information on the training process as well as the testing one.

### Training
If you have download the files necessary for training and testing, this step will require ***train_data.json***. 

**Preparing the Data**: The function read_and_process_json is used to read a JSON file containing the conversation data. The conversation data should be formatted in a way that each conversation is a list of sentences, where each sentence is a string. These lists of sentences are loaded into memory as a Python list. No need to worry about this as ***train_data.json*** is exactly in that format.

**Creating the Dataset**: The DatasetFromJSON class takes this list of conversations, along with a tokenizer, and processes it into a format suitable for training the model. It iteratively goes through each sentence in each conversation and tokenizes the input and output pairs. Tokenization is the process of converting input text into a format that a model can understand. The input to the model will be a sentence, and the target output will be the subsequent sentence. This format is used because DialoGPT is trained to predict the next sentence given a sentence.

**Initializing the Model and Tokenizer**: The train_dialo_gpt function first initializes the tokenizer and the model. The GPT2Tokenizer and GPT2LMHeadModel classes are used to load a pre-trained DialoGPT model and its corresponding tokenizer. These are loaded using the model's name, which in this case is "microsoft/DialoGPT-large". The model is moved to the GPU if one is available for faster training.

**Preparing for Training**: The training arguments are set up with the TrainingArguments class. This includes the output directory for the model, the number of epochs (full passes through the data), the batch size (number of examples processed simultaneously), and the frequency of saving the model and logging progress.

**Training the Model**: The Trainer class is used to handle the training. It is given the model, the training arguments, the data collator (which is responsible for batching examples together and preparing them for input into the model), and the dataset. The trainer then trains the model and saves it to the specified output directory.

#### GPT2Tokenizer and GPT2LMHeadModel
As for why I have to use ***GPT2Tokenizer.from_pretrained(model_name)*** and ***GPT2LMHeadModel.from_pretrained(model_name)***, these commands are used to load the pre-trained DialoGPT model and its corresponding tokenizer. The tokenizer is responsible for turning the input text into a format that the model can understand. This includes splitting words into subwords if necessary, converting these into numerical IDs, and creating the necessary formatting for model inputs. The **GPT2LMHeadModel** is the actual model architecture. This includes the transformer layers that process the input data and the final layer (the "LM Head") that turns the model's internal representations into predictions for the next word in the sentence. The from_pretrained(model_name) function loads the pre-trained weights for these components, allowing to start from a model that has already been trained on a large amount of data and fine-tune it on a specific task, which is generally a more efficient approach than training a model from scratch. In this case, model_name is "microsoft/DialoGPT-large", which refers to the large variant of the DialoGPT model trained by Microsoft. This is a powerful language model that's particularly well-suited to generating conversational responses.

### Testing
To measure accuracy and response time, the process went like this briefly: 

**Setup**: ***measure_acc_rt*** starts by loading the necessary libraries and modules. It uses AutoTokenizer and AutoModelWithLMHead to load the fine-tuned DialoGPT model and its tokenizer. It also initializes the Rouge class for later computing ROUGE scores (a metric for evaluating text generation models).

**Similarity Calculation Function**: The calculate_similarity_score function is defined to calculate the similarity between two texts. This function uses the Jaccard similarity, BLEU score, and ROUGE score. The Jaccard similarity is a measure of the intersection over union of two sets of words, the BLEU score is a metric that compares a candidate translation of text to one or more reference translations, and the ROUGE score measures the overlap of n-grams between the system and reference translations.

**Chatbot Response Function**: The query function takes an input text (a question) and generates a response using the model and tokenizer.

**Loading Test Data**: The script reads a JSON file, which is ***test_data.json*** if you forgot which consists of a list of question-answer pairs, pretty much same format as ***train_data.json***.

**Evaluation**: The main part of the script is a loop that performs several "runs" of the evaluation. For each run, it loops over all question-answer pairs in the test data. It queries the model with the question, calculates the response time, and compares the generated response to the ground truth answer using the calculate_similarity_score function. It collects all the response texts, response times, and similarity scores.

**Result Compilation**: After each run, it compiles the results into a pandas DataFrame and saves it to a CSV file. The results include the original question, the model's response, the expected response, the Jaccard similarity, BLEU score, ROUGE-1, ROUGE-2, ROUGE-L scores, and the response time for each question.

So essentially, this script is for evaluating the quality of the model's responses (using various metrics) and the time it takes for the model to generate these responses.

Whereas for the consistency testing: 
**Imports and Setup** : ***measure_cons_dia.py*** begins by importing the necessary libraries. It uses the transformers library from Hugging Face to work with the DialoGPT-Large model. The Jaccard similarity function is defined for measuring consistency later on.
**Model Loading**: The tokenizer and model are loaded. The tokenizer is used to convert input text into tokens that can be processed by the model, and the model itself is used to generate responses.
**Query Function**: The query function is defined to generate a response from the model given an input. The function tokenizes the input, then feeds it to the model to generate a response. The generated tokens are then decoded back into text and returned.
**Queries**: The queries are a list of groups of related questions. Each group contains different phrasings of the same question. They can also be found in appendix 2 in the thesis.
**Response Generation and Consistency Calculation**: ***measure_cons_dia.py*** then loops over each group of questions. For each question in a group, it generates a response using the query function and stores it in a list. Then it calculates the Jaccard similarity between each pair of responses within a group, and stores the results in a CSV file.

To run these scripts, replace ./models with the path to your fine-tuned DialogPT model. Make sure you have the Hugging Face transformers library installed.

### Running
To run the model, replace the model used in https://huggingface.co/spaces/rushic24/DialoGPT-Covid-Help-Doctor/tree/main with the one you intend on using. After doing so, make sure to have the parameters the same as what the model was trained and tested on for consistency's sake, or if you feel like experimenting tweak them. Maybe you will end up with a better chatbot.
To actually run app.py use the command: 
```
streamlit app.py
```
and a webpage will be opened in which you can interact with the chatbot.

## Rasa-based chatbot
To run the Rasa chatbot, first download either the [simple](https://drive.google.com/drive/folders/1pghl9Z5eFdelyP7xSqeEAnWJtrpwdibs?usp=drive_link) or [complex](https://drive.google.com/drive/folders/1_j8Ty-Kg3fEs0eC4fCoqQ9X15gCE4y4G?usp=drive_link) model. 

One note: When download the simple models, please do download **archaic-alert.tar.gz** or generally the bottom one since it is the latest and 
most fine-tuned one.

In order to implement these models, to install Rasa the following python pip version was used: 21.3.1 and not the latest version because due to a new feature. Install rasa using the following command: 

``` 
pip install rasa
``` 
, then once Rasa is installed run the next command: 

```
rasa init

```
Once the Rasa folder has been setup, copy-paste the model downloaded to the "models" sub-folder found in the Rasa folder.

Lastly, once this step has been completed, navigate to the folder of your choice and these commands can be used to train and run Rasa: 
    - **rasa train** - Holds information about the results of training.
    - **rasa shell** - Loads your trained model and lets you talk to your assistant on the command line.
    - **rasa run** - Starts a server with your trained model.
    - **rasa test** - Tests a trained Rasa model on any files starting with test.

## Extra
This folder contains some additional code that was used for graphing, you can also use shiny.chemgrid.org/boxplotr/ as long as the csv files from folders /accuracy_refined_results/ are used. Testing code was more specifically used for re-processing the Botkit files retrieved from testing for BLEU and ROUGE purposes.

## Results
This folder contains all of the results or more specifically, csv files and pictures that were utilised in the thesis.

## License
This repository has an MIT license, please do check it for further details!
