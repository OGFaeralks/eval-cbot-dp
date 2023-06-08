import { io } from 'https://cdn.socket.io/4.6.0/socket.io.esm.min.js';
const socket = io();

document.getElementById('sendButton').addEventListener('click', () => {
  const userInput = document.getElementById('userInput');
  const userMessage = userInput.value.trim();
  if (userMessage.length > 0) {
      const messagesDiv = document.getElementById('messages');
      const messageElement = document.createElement('div');
      messageElement.classList.add('chat-message', 'sent');
      messageElement.textContent = userMessage;
      messagesDiv.appendChild(messageElement);
      userInput.value = '';
      socket.emit('message', { text: userMessage });
  }
});

function summarizeText(text, maxSentences = 2) {
  const sentences = text.match(/[^.!?]+[.!?]+/g) || [];
  const summary = sentences.slice(0, maxSentences).join(' ');
  return summary || text;
}

function emitUserMessage(text) {
  const message = document.createElement('div');
  message.className = 'message user';
  message.innerText = text;
  document.getElementById('messages').appendChild(message);
}

function displayMainMenu() {
  const optionsDiv = document.getElementById('options');
  optionsDiv.innerHTML = '';

  const mainMenuOptions = [
    { text: 'COVID-19 Information', value: 'covid_info' },
    { text: 'Check Symptoms', value: 'check_symptoms' },
    { text: 'Book Appointment', value: 'book_appointment' },
    { text: 'Search Illness', value: 'search_illness' },
    { text: 'Ask a Question', value: 'ask_question' }
  ];

  mainMenuOptions.forEach((option) => {
    const button = document.createElement('button');
    button.classList.add('chat-option');
    button.textContent = option.text;
    button.onclick = () => {
      optionSelected(option.value);
    };
    optionsDiv.appendChild(button);
  });
}

function removeHTMLTags(text) {
  const div = document.createElement('div');
  div.innerHTML = text;
  return div.textContent || div.innerText || '';
}


socket.on('connect', () => {
    console.log('Connected to the server');
    socket.emit('hello');
});

socket.on('message', (message) => {
  const messagesDiv = document.getElementById('messages');
  const messageElement = document.createElement('div');
  messageElement.classList.add('chat-message', 'received');
  messageElement.textContent = removeHTMLTags(summarizeText(message.text));
  messagesDiv.appendChild(messageElement);
});

socket.on('ask_question', (message) => {
  const messagesDiv = document.getElementById('messages');
  const messageElement = document.createElement('div');
  messageElement.classList.add('chat-message', 'received');
  messageElement.textContent = message;
  messagesDiv.appendChild(messageElement);
});

socket.on('options', (options) => {
  const optionsDiv = document.getElementById('options');
  optionsDiv.innerHTML = '';

  options.forEach((option) => {
      const button = document.createElement('button');
      button.classList.add('chat-option');
      button.textContent = option.text;
      button.onclick = () => {
          socket.emit('optionSelected', option.value);
          
      };
      optionsDiv.appendChild(button);
  });
});

socket.on('multiSelectOptions', (options) => {
    const optionsDiv = document.getElementById('options');
    optionsDiv.innerHTML = '';
  
    options.forEach((option) => {
      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.value = option;
      checkbox.id = option;
  
      const label = document.createElement('label');
      label.htmlFor = option;
      label.textContent = option;
  
      optionsDiv.appendChild(checkbox);
      optionsDiv.appendChild(label);
    });
  
    const submitButton = document.createElement('button');
    submitButton.textContent = 'Submit';
    submitButton.onclick = () => {
      const selectedOptions = options
        .map((option) => document.getElementById(option).checked)
        .filter((checked) => checked).length;
      const percentage = (selectedOptions / options.length) * 100;
      socket.emit('symptomsSelected', percentage);
    
      // Display main menu after submitting symptoms
      displayMainMenu();
    };
    optionsDiv.appendChild(document.createElement("br"));
    optionsDiv.appendChild(submitButton);
});

socket.on('input', (inputType) => {
  const messagesDiv = document.getElementById('messages');
  if (inputType === 'illnessName') {
      const inputElement = document.createElement('input');
      inputElement.type = 'text';
      inputElement.placeholder = 'Enter illness name';
      inputElement.onchange = () => {
          socket.emit('illnessName', inputElement.value);
          inputElement.remove();
      };
      messagesDiv.appendChild(inputElement);
  }
  if (inputType === 'question') {
    const inputElement = document.createElement('input');
    inputElement.type = 'text';
    inputElement.placeholder = 'Type your question';
    inputElement.onchange = () => {
        socket.emit('question', inputElement.value);
        inputElement.remove();
    };
    messagesDiv.appendChild(inputElement);
  }
});

window.optionSelected = function (optionValue) {
  socket.emit('optionSelected', optionValue);
  if (optionValue === 'search_illness') {
    document.getElementById('userInput').style.display = 'inline-block';
    document.getElementById('sendButton').style.display = 'inline-block';
  } else if (optionValue === 'covid_info') {
    document.getElementById('userInput').style.display = 'none';
    socket.emit('covidInfo');
  } else if (optionValue === 'ask_question') { // Add this block
    document.getElementById('userInput').style.display = 'inline-block';
    document.getElementById('sendButton').style.display = 'inline-block';
  } else {
    document.getElementById('userInput').style.display = 'none';
    document.getElementById('sendButton').style.display = 'none';
  }
};

document.getElementById('sendButton').addEventListener('click', () => {
  const userInput = document.getElementById('userInput');
  const userMessage = userInput.value.trim();
  if (userMessage.length > 0) {
      const messagesDiv = document.getElementById('messages');
      const messageElement = document.createElement('div');
      messageElement.classList.add('chat-message', 'sent');
      messageElement.textContent = userMessage;
      messagesDiv.appendChild(messageElement);
      userInput.value = '';
      socket.emit('userInput', userMessage);
  }
});