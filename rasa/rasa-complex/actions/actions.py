# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import UserUtteranceReverted, SlotSet
from rasa_sdk.executor import CollectingDispatcher

class ActionCheckSymptom(Action):

    def name(self) -> Text:
        return "action_check_symptom"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # get list of symptoms from the symptom slot
        symptoms = tracker.get_slot("symptom")
        covid_symptoms = ["fever", "cough", "shortness of breath", "fatigue", "fatigued", "muscle ache", "body aches", "headache", "loss of taste", "loss of smell", "sore throat", "congestion"  "runny nose", "nausea or vomiting", "diarrhea"]
        
        # get the latest intent and its confidence
        latest_intent = tracker.latest_message['intent'].get('name')
        latest_intent_confidence = tracker.latest_message['intent'].get('confidence')
        
        # set the confidence threshold (0.7 by default)
        confidence_threshold = 0.7
        print(f"symptom: {symptoms}")
        print(f"confidence: {latest_intent_confidence}")

        if symptoms == None:
            # if none of the above conditions are met, respond with fallback message
            dispatcher.utter_message("I'm sorry, I couldn't understand you. Could you please rephrase your question?")
            return [SlotSet('symptom', symptoms)]
            

        bool_all = all(elem in covid_symptoms for elem in symptoms)
        bool_some = any(element in covid_symptoms for element in symptoms)
        
        
        
        if bool_all:
            # if symptoms are recognized, respond with "You may have COVID-19"
            dispatcher.utter_message("Yes, based on your symptoms, you may have COVID-19. Please get tested and seek medical attention immediately.")
            return [SlotSet('symptom', symptoms)]
        elif bool_some:
            dispatcher.utter_message("based on your symptoms, you may have COVID-19. however not all symptoms mentioned match so I suggest to test")
            return [SlotSet('symptom', symptoms)]
        elif (not bool_all and not bool_some):
            # if confidence of latest intent is below threshold, respond with "I'm not sure"
            dispatcher.utter_message("Based on the database I have I recognized your symptoms but these do not seem they are covid, I suggest testing regardless.")
            return [SlotSet('symptom', symptoms)]
        elif latest_intent_confidence < confidence_threshold:
            # if none of the above conditions are met, respond with fallback message
            dispatcher.utter_message("I'm sorry, I couldn't understand you. Could you please rephrase your question?")
            return [SlotSet('symptom', symptoms)]


