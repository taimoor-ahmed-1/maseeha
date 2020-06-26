from typing import Dict, Text, Any, List, Union, Optional
from datetime import datetime
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from datetime import datetime,date
import json
class EmergencyForm(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "emergency_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["location","etype","people"]
    
    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "location": [self.from_entity(entity="location",intent=["inform",]),self.from_text()],
            "people": [self.from_entity(entity="people",intent="inform")],
            "etype": [self.from_entity(entity="etype",intent="inform")]
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        records = open('slots.txt', 'a+')
        records.write('\nEmergency Alert: {}\n'.format(datetime.now()))
        slots_list = ["Etype: "+str(tracker.get_slot('etype')),"people: "+str(tracker.get_slot('people')),"Location: "+str(tracker.get_slot('location'))]
        records.write('\n'.join(slots_list))
        records.close()
        peeps = tracker.get_slot('people')
        if isinstance(peeps,list):
            temp = ""
            peeps = temp.join(peeps)
        new_obj = {"Time":datetime.now().strftime("%H:%M:%S"),"Date":date.today().strftime("%d/%m/%Y"),"call_id": tracker.sender_id,"etype":tracker.get_slot('etype'),"people":peeps,"location":tracker.get_slot('location')}
        filename = "emergency.json"
        with open(filename, 'r+',encoding='utf-8') as f:
            text = json.load(f)
            text.append(new_obj)
            f.seek(0)
            f.write(json.dumps(text))
            f.truncate() 
        dispatcher.utter_message(template="utter_confirmation")
        dispatcher.utter_message(template="utter_submit")
        return []

class CoronaForm(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "corona_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["cough","fever","breath","flu","international","daystwo","province"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "cough": [self.from_intent(intent="affirm", value=True), self.from_intent(intent="deny", value=False)],
            "fever": [self.from_intent(intent="affirm", value=True), self.from_intent(intent="deny", value=False)],
            "breath": [self.from_intent(intent="affirm", value=True), self.from_intent(intent="deny", value=False)],
            "flu": [self.from_intent(intent="affirm", value=True), self.from_intent(intent="deny", value=False)],
            "daystwo": [self.from_intent(intent="affirm", value=True), self.from_intent(intent="deny", value=True)],
            "international": [self.from_intent(intent="affirm", value=True), self.from_intent(intent="deny", value=False)],
            "province": [self.from_entity(entity="province",intent=["inform"]),self.from_text()]
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        records = open('slots.txt', 'a+')
        records.write('\nCorona Alert: {}\n'.format(datetime.now()))
        slots_list = ["Cough: "+str(tracker.get_slot('cough')),"Fever: "+str(tracker.get_slot('fever')),"breath: "+str(tracker.get_slot('breath')), "flu: "+str(tracker.get_slot('flu')),"international: "+str(tracker.get_slot('international')),"daystwo: "+str(tracker.get_slot('daystwo')),"province: "+str(tracker.get_slot('province'))]
        records.write('\n'.join(slots_list))
        records.close() 
        cough = tracker.get_slot('cough')
        fever = tracker.get_slot('fever')
        flu  = tracker.get_slot('flu')
        international  = tracker.get_slot('international')
        breath = tracker.get_slot('breath')
        daystwo = tracker.get_slot('daystwo')
        province = tracker.get_slot('province')  
        print("submit: "+province)  
        counter = 0
        if cough:
            counter+=1	
        if flu: 
            counter+=1
        if fever: 
            counter+=1
        if breath: 
            counter+=1
        if international:
            counter+=1
        if cough: 
            counter+=1
        print("counter: {}".format(counter))        
#province_dict = {"پنجاب": "punjab", "اسلام آباد": "islamabad", "سندھ": "sindh", "بلوچستان":"balochistan", "پختونخواہ":"kpk", "گلگت بلتستان" : "gilgit"}	
        positive = False
        if daystwo:
            if counter >= 3:
                dispatcher.utter_message(template="utter_focal_"+str(province))
                positive = True
            elif counter >= 2:
                dispatcher.utter_message(template="utter_hospital")	
            else:
                dispatcher.utter_message(template="utter_quarantine")
        else: 
            dispatcher.utter_message(template="utter_quarantine") 
        new_obj = {"Time":datetime.now().strftime("%H:%M:%S"),"Date":date.today().strftime("%d/%m/%Y"),"call_id":tracker.sender_id,"cough": cough,"flu":flu,"breath":breath,"fever":fever,"international_travel":international, "two_days": daystwo,"province":province,"positive":positive}
        
        filename = "corona.json"
        with open(filename, 'r+',encoding='utf-8') as f:
            text = json.load(f)
            text.append(new_obj)
            f.seek(0)
            f.write(json.dumps(text))
            f.truncate()   
	#if tracker.get_slot('international') and (tracker.get_slot('cough') or tracker.get_slot('fever')):
        #    dispatcher.utter_message(template="utter_confirmation")
        #elif tracker.get_slot('cough') and tracker.get_slot('fever'):
        #    dispatcher.utter_message(template="utter_confirmation")
        #else:
        #    dispatcher.utter_message(template="utter_quarantine")
        #    dispatcher.utter_message(template="utter_submit")
        return []
    def validate_province(self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> Dict[Text, Any]:

        # put your tests here
        print(value)
        #if value not in ['islamabad','punjab','balochistan', 'sarhad','پنجاب','سندھ','بلوچستان' ,'gilgit', 'گلگت بلتستان','گلگت', 'سرحد', 'اسلام آباد','خیبر پختونخواہ']:
            #dispatcher.utter_message(template="utter_wrong_province")
        # if value is not valid, return this:
            #return {"province": None}
        
        if value in ['gilgit','gilgit baltistan', 'baltistan','گلگت','گلگت بلتستان','بلتستان']:
            value = 'gilgit'
        if value in ['islamabad','اسلام آباد']:
            value == 'islamabad'
        if value in ['kpk','sarhad','خیبر پختونخواہ','سرحد', 'خیبر','پختونخوا','خیبرپختونخوا','ے پی کے']:
            value = 'kpk'
        if value in ['balochistan','بلوچستان']:
            value = 'balochistan'
        if value in ['sindh','سندھ']:
            value = 'sindh'
        if value in ['punjab','پنجاب']:
            value = 'punjab'
        if value not in ['sindh','punjab','gilgit','islamabad','balochistan','kpk']:
            dispatcher.utter_message(template="utter_wrong_province")
            return {"province": None}
        else:
            print(value)
# if value is valid, return this:
            return {"province": value}
        return []
	
  

