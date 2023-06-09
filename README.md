# eval-cbot-dp
**Under construction**

A repository for the degree project done by Fabian and Fredric. This repository contains the code that was utilized throughout the project as well as some additional extras such as code used for graphing the results, images, testing code and so forth.


1. To run botkit and natural, simply navigate to botkit "cd botkit" and **node bot.js**.

2. To run the flask application for chatterbot, run **app.py** found in flask-chatterbot.

3. To run the streamlit application for dialogpt, first download the model from [here](https://drive.google.com/drive/folders/1EVEsc9-lNyaoorEZDm0OU3Tee8Lb6vsy?usp=drive_link) (it is a Google Drive folder as GitHub has a 200MB size limit, and the model is 8GB) and then place it under **models** which is found in the dialogpt folder. Afterward, run app.py found in dialogpt.

4. To run the Rasa chatbot, first download either the [simple](https://drive.google.com/drive/folders/1pghl9Z5eFdelyP7xSqeEAnWJtrpwdibs?usp=drive_link) or [complex](https://drive.google.com/drive/folders/1_j8Ty-Kg3fEs0eC4fCoqQ9X15gCE4y4G?usp=drive_link) model and place it under **models** sub-folder found in both rasa-simple and rasa-complex. Afterwards navigate to the folder of your choice and these commands can be used to run Rasa: 
    - **rasa shell** - Loads your trained model and lets you talk to your assistant on the command line.
    - **rasa run** - Starts a server with your trained model.
    - **rasa test** - Tests a trained Rasa model on any files starting with test.

## License
This repository is under no license and the rightful licenses apply for the works used that are set by their creators.