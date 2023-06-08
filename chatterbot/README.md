# Chatterbot

## Getting started
The prerequisites are: 
1. Visual Studio Code or PyCharm
2. Python version I used is 3.8.8 (conda)

## Installation
You can install ChatterBot on your system using Python’s pip command.

    pip install chatterbot

Then after installing chatterbot, create a python file in order to work and an example of how the code could look like is: 

    from chatterbot import ChatBot
    from chatterbot.trainers import ListTrainer

    # Create a new chat bot named Charlie
    chatbot = ChatBot('Charlie')

    trainer = ListTrainer(chatbot)

    trainer.train([
        "Hi, can I help you?",
        "Sure, I'd like to book a flight to Iceland.",
        "Your flight has been booked."
    ])

    # Get a response to the input text 'I would like to book a flight.'
    response = chatbot.get_response('I would like to book a flight.')

    print(response)

In order to train Chatterbot, you will need to use ListTrainer and the function train(). The parameter for train() is a list and a list should consists of strings, and each list should also represent a conversation.

Sometimes SQLlite might not work, therefore an alternative adapter would be MongoDB. Simply download MongoDB, and install it. The link is the following: https://www.mongodb.com/try/download/community

In order to connect MongoDB with Chatterbot you'll need to enter the following code when configuring the bot, for example: 

    bot = ChatBot(
        'Terminal',
        storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
        logic_adapters=[
            'chatterbot.logic.BestMatch'
        ],
        database_uri='mongodb://localhost:27017/chatterbot-database'
    )

So in specific, you'll need to specify the storage adapter as well as the database_uri, which in this case it's a local one with the chatterbot database.

After installing MongoDB, open MongoDB Compass and create a connection at port 27017. Proceed to create a database with the name "chatterbot-database" and then enter whatever collection name, it just needs one in order to create it. I went with "test". After doing so, you can the import data from the content folder and you can either use JSON or SQL. Import the data and then try connecting Chatterbot with MongoDB, and it should work.

## Additional links for support
In case you need to consult the chatterbot documentation this is the link: https://chatterbot.readthedocs.io/en/stable/setup.html

In case you need to consult the MongoDB manual, here's the link: 
https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-windows-unattended/