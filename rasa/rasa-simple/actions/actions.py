from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class CustomSymptomCheckAction(Action):
    def name(self) -> Text:
        return "custom_actions.CustomSymptomCheckAction"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        covid_symptoms = tracker.get_slot("covid_symptom_entity")
        other_symptoms = tracker.get_slot("symptom")

        if covid_symptoms:
            if len(covid_symptoms) > 0 and len(other_symptoms) == 0:
                dispatcher.utter_message(template="utter_ask_for_testing")
            elif len(covid_symptoms) > 0 and len(other_symptoms) > 0:
                dispatcher.utter_message(template="utter_suggest_testing")
            else:
                dispatcher.utter_message(template="utter_not_sure_testing")
        elif other_symptoms:
            dispatcher.utter_message(template="utter_no_testing")
        else:
            dispatcher.utter_message(template="utter_reiterate_question")

        return []