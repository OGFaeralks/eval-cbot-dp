import { Botkit } from 'botkit';
import axios from 'axios';
import cheerio from 'cheerio';
import express from 'express';
import { Server } from 'socket.io';
import natural from 'natural'; 
import fs from 'fs'; 
import { performance } from 'perf_hooks';

const trainingDataFile = '../training/train_data.json';
const testingDataFile = '../training/test_data.json';
const resultsFile = './newest_results_accuracy_run_3.csv';

const queries = [
    ["I'm experiencing lung pain and discomfort, but it's not constant or in the same place. I don't have a fever, and I only cough or sneeze once a day. Should I get tested for COVID-19?",
      "My lungs feel uncomfortable and painful, but the location keeps changing and it's not in both lungs at the same time. I have no fever, and I sneeze and cough infrequently. Do I need a coronavirus test?",
      "I have some lung discomfort and pain that moves around and isn't simultaneous in both lungs. I don't have a high temperature, and I only cough and sneeze occasionally. Is it necessary for me to get tested for COVID-19?"],
    ["Should I get tested for COVID-19 if I have a blocked nose and recently returned from a high-risk country?",
      "I just came back from a country with a high COVID-19 risk, and my nose is congested. Do I need a coronavirus test?",
      "If I have nasal congestion and have traveled from a high-risk area, should I be tested for COVID-19?"],
    ["I've had a dry cough and a sore throat for a week, which seems to be worsening. I don't have a runny nose or fever but sometimes experience headaches. Do I need a COVID-19 test?",
      "My dry cough and sore throat have been persisting for a week and are getting worse. There's no fever or runny nose, but I occasionally have headaches. Should I get tested for COVID-19?",
      "I've been dealing with a worsening dry cough and sore throat for the past week. I don't have a fever or runny nose, but I do get headaches from time to time. Is it necessary to test for COVID-19?"],
    ["Can COVID-19 symptoms vary in severity, with some people experiencing mild symptoms like fatigue and a low-grade fever, while others have more extreme symptoms?",
      "Is it possible for coronavirus symptoms to be mild in some cases, such as only having fatigue and a low fever, rather than severe symptoms like difficulty breathing?",
      "Can the symptoms of COVID-19 be different for each person, with some having mild symptoms like tiredness and a low fever, while others experience more severe symptoms?"],
    ["I've been self-quarantining after a flight on March 8th and have experienced headaches and a sore throat. With only two days left in my quarantine, should my symptoms be worse by now?",
      "Since my flight on March 8th, I've been in self-quarantine and have had a sore throat and headaches. As my quarantine is almost over, should my symptoms have worsened by now?",
      "I've been self-isolating after a plane journey on March 8th, and I've had a runny throat and headaches. With only two days left in my self-quarantine, should I expect more severe symptoms by now?"]
]

// Load testing data from the JSON file
const testingData = JSON.parse(fs.readFileSync(testingDataFile, 'utf-8'));

// Load training data from the JSON file
const trainingData = JSON.parse(fs.readFileSync(trainingDataFile, 'utf-8'));

// Initialize the natural language classifier
const classifier = new natural.BayesClassifier();

trainingData.forEach((conversation, conversationIndex) => {
  conversation.forEach((message, index) => {
      if (index % 2 === 0) { // User messages
          classifier.addDocument(message, conversationIndex);
      }
  });
});

// Train the classifier
classifier.train();
testChatbot();
// testChatbotConsistency(queries);  
const app = express();
const server = app.listen(4000);
const io = new Server(server);

app.use(express.static('public')); 
app.use('/node_modules', express.static('node_modules')); 

const controller = new Botkit({
  debug: false,
});

function jaccardSimilarity(a, b) {
  const aSet = new Set(a);
  const bSet = new Set(b);
  const intersection = new Set([...aSet].filter(x => bSet.has(x)));
  return intersection.size / (aSet.size + bSet.size - intersection.size);
}

function generateResponse(userInput) {
  return new Promise((resolve) => {
    const bestMatchIndex = classifier.classify(userInput);
    const response = trainingData[bestMatchIndex][1];
    resolve(response);
  });
}

async function testChatbot() {
  fs.writeFileSync(resultsFile, 'Question,Generated Answer,Actual Answer,Jaccard Similarity,Response Time\n');

  let accurateAnswersCount = 0;
  let totalQuestions = 0;

  for (const conversation of testingData) {
    for (let i = 0; i < conversation.length; i += 2) {
      const question = conversation[i];
      const actualAnswer = conversation[i + 1];

      const startTime = performance.now();
      const generatedAnswer = await generateResponse(question);
      const responseTime = performance.now() - startTime;

      const similarity = jaccardSimilarity(generatedAnswer, actualAnswer);

      if (similarity >= 0.75) {
        accurateAnswersCount++;
      }

      totalQuestions++;

      // Write the result to the CSV file
      const resultLine = `"${question.replace(/"/g, '""').replace(/\n/g, ' ')}","${generatedAnswer.replace(/"/g, '""').replace(/\n/g, ' ')}","${actualAnswer.replace(/"/g, '""').replace(/\n/g, ' ')}",${similarity},${responseTime}\n`;      
      fs.appendFileSync(resultsFile, resultLine);
      console.log(`Question: ${question}\nGenerated Answer: ${generatedAnswer}\nActual Answer: ${actualAnswer}\nJaccard Similarity: ${similarity}\nResponse Time: ${responseTime}ms\n---\n`);
    }
  }
  const accuracy = (accurateAnswersCount / totalQuestions) * 100;
  console.log(`Testing completed. Results saved to ${resultsFile}\nAccuracy: ${accuracy}%`);
}


async function testChatbotConsistency(queries) {
  const consistencyResults = [];
  fs.writeFileSync('botkit_natural_consistency_run.csv', 
    'query_group,response1,response2,jaccard_similarity\n');

  for (let queryGroupNum = 0; queryGroupNum < queries.length; queryGroupNum++) {
    console.log(`Testing consistency for query group ${queryGroupNum + 1}`);
    const queryGroup = queries[queryGroupNum];
    const responses = [];

    for (const query of queryGroup) {
      const response = await generateResponse(query);
      console.log(`\nQuery ${queryGroup.indexOf(query) + 1} : ${query}`);
      console.log(`Response ${queryGroup.indexOf(query) + 1} : ${response}`);
      responses.push(response);
    }

    let consistencyScores = [];
    for (let i = 0; i < responses.length; i++) {
      for (let j = i + 1; j < responses.length; j++) {
        const score = jaccardSimilarity(responses[i], responses[j]);
        console.log(`\nJaccard Similarity between Response ${i + 1} and Response ${j + 1}: ${score}`);
        consistencyScores.push(score);
        fs.appendFileSync('botkit_natural_consistency_run.csv', 
          `${queryGroupNum + 1},"${responses[i]}","${responses[j]}",${score}\n`);
      }
    }
    const avgConsistency = consistencyScores.reduce((a, b) => a + b) / consistencyScores.length;
    console.log(`\nAverage consistency for query group ${queryGroupNum + 1}: ${avgConsistency}\n`);
    consistencyResults.push({ queryGroup: queryGroupNum + 1, averageConsistency: avgConsistency });
  }
  return consistencyResults;
}

async function getWikipediaSummary(title) {
    try {
      const response = await axios.get('https://en.wikipedia.org/api/rest_v1/page/summary/' + encodeURIComponent(title));
      return response.data.extract;
    } catch (error) {
      console.error('Error fetching Wikipedia summary:', error);
      return 'Sorry, there was an error fetching the information. Please try again later.';
    }
}

async function getWHOCovidFAQAnswer(question) {
  try {
    const url = "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19";
    const response = await axios.get(url);
    const $ = cheerio.load(response.data);
    const questions = $('div.sf-accordion__trigger-panel');
    const answers = $('div.sf-accordion__content');
    const faqs = [];

    questions.each((i, q) => {
      const questionText = $(q).find('span[itemprop="name"]').text().trim();
      const answerText = answers.eq(i).find('div[itemprop="text"]').text().trim();
      faqs.push({ question: questionText, answer: answerText });
    });

    const relevantFAQ = faqs.find((faq) => faq.question.toLowerCase().includes(question.toLowerCase()));

    if (relevantFAQ) {
      return relevantFAQ.answer;
    } else {
      const theOtherResponse = await generateResponse(question);      
      return theOtherResponse;
    }
  } catch (error) {
    console.error('Error fetching WHO COVID FAQ & Natural cannot process:', error);
    return 'Sorry, there was an error fetching the information. Please try again later.';
  }
}

async function getIllnessInfo(illnessName) {
    const url = `https://en.wikipedia.org/w/api.php?action=query&prop=extracts&format=json&exintro=&titles=${encodeURIComponent(illnessName)}&origin=*`;
    const response = await fetch(url);
    const data = await response.json();
    const pageId = Object.keys(data.query.pages)[0];

    return data.query.pages[pageId].extract;
}

// At most returns 5 symptoms and makes them a bit nicer.
function extractSymptoms(text) {
    const commonSymptoms = text.match(/Common symptoms include (.+?), with less common ones/);
    const lessCommonSymptoms = text.match(/with less common ones including (.+?), and in moderate/);
    const moderateSymptoms = text.match(/and in moderate to severe cases, (.+)\./);
  
    if (!commonSymptoms || !lessCommonSymptoms || !moderateSymptoms) {
      return [];
    }
  
    const symptoms = [    ...commonSymptoms[1].split(', '),
      ...lessCommonSymptoms[1].split(', '),
      moderateSymptoms[1],
    ].map((symptom) => symptom.charAt(0).toUpperCase() + symptom.slice(1)).slice(0, 5);
  
    return symptoms;
}


io.on('connection', (socket) => {
    console.log('Client connected');
    console.log('Server starting at localhost:4000'); 
    socket.on('hello', async () => {
        console.log('Received hello event from the client');
        socket.emit('message', { text: 'Hello! What can I help you with today?' });
        const options = [
            { text: 'COVID-19 Information', value: 'covid_info' },
            { text: 'COVID-19 Symptoms', value: 'check_symptoms' },
            { text: 'Book Appointment', value: 'book_appointment' },
            { text: 'Search illness', value: 'search_illness' },
            { text: 'Ask a Question', value: 'ask_question' },
        ];
        socket.emit('options', options);
    });

    socket.on('optionSelected', async (optionValue) => {
        console.log('Received optionSelected event from the client with value:', optionValue);
        if (optionValue === 'search_illness') {
          socket.emit('message', { text: 'Please enter the name of the illness you would like to know more about.' });
          socket.emit('input', 'illnessName');
        }
        if (optionValue === 'covid_info') {
          const summary = await getWikipediaSummary('COVID-19');
          socket.emit('message', { text: summary });
        } 
        if (optionValue === 'check_symptoms') {
            const symptomsText = await getWikipediaSummary('Symptoms of COVID-19');
            const symptomsList = extractSymptoms(symptomsText);
            socket.emit('message', {text : symptomsText})
            socket.emit('message', { text: 'Which of the following symptoms do you have?' });
            socket.emit('multiSelectOptions', symptomsList);
        } 
        if (optionValue === 'book_appointment') {
          socket.emit('message', { text: 'Please call us at our office number to book a time!' });
        } 
        if (optionValue === 'ask_question') {
          socket.emit('message', { text: 'Please enter your question.' });
          socket.emit('input', 'question');
        }
    });

    socket.on('question', async (question) => {
      const answer = await getWHOCovidFAQAnswer(question);
      socket.emit('message', { text: answer });
  });

    socket.on('illnessName', async (illnessName) => {
        const illnessInfo = await getIllnessInfo(illnessName);
        socket.emit('message', { text: illnessInfo });
    });

    socket.on('symptomsSelected', (percentage) => {
        if (percentage >= 50) {
          socket.emit('message', { text: 'You have selected more than 50% of the symptoms. It is recommended that you book an appointment.' });
        } else {
          socket.emit('message', { text: 'You have selected fewer than 50% of the symptoms. If you still feel unwell, consider booking an appointment.' });
        }
      });

});