from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet
from helper import resturant_dict,resturants
from send_mail import send_mail
import zomatopy
import json
import re

class ActionLookupLocation(Action):
    def name(self):
        return 'lookup_location'
        
    ## Search for the location entered by the user. If location is not found inform.
    def run(self, dispatcher, tracker, domain):
        try:
            location = tracker.get_slot('location')
            x_y_cities = ['Bangalore', 'Chennai', 'Delhi', 'Hyderabad', 'Kolkata', 'Mumbai', 'Agra', 'Ajmer', 'Aligarh', 'Amravati',
                          'Amritsar', 'Asansol', 'Aurangabad', 'Ahmedabad', 'Bareilly', 'Belgaum', 'Bhavnagar', 'Bhiwandi', 'Bhopal',
                          'Bhubaneswar', 'Bikaner', 'Bokaro Steel City', 'Chandigarh', 'Coimbatore', 'nagpur', 'Cuttack', 'Dehradun',
                          'Dhanbad', 'Durg-Bhilai Nagar', 'Durgapur', 'Erode', 'Faridabad', 'Firozabad', 'Ghaziabad', 'Gorakhpur', 'Gulbarga',
                          'Guntur', 'Gwalior', 'Gurgaon', 'Guwahati', 'Hubli-Dharwad', 'Indore', 'Jabalpur', 'Jaipur', 'Jalandhar', 'Jammu',
                          'Jamnagar', 'Jamshedpur', 'Jhansi', 'Jodhpur', 'Kakinada', 'Kannur', 'Kanpur', 'Kochi', 'Kottayam', 'Kolhapur', 'Kollam',
                          'Kota', 'Kozhikode', 'Kurnool', 'Lucknow', 'Ludhiana', 'Madurai', 'Malappuram', 'Mathura', 'Goa', 'Mangalore', 'Meerut',
                          'Moradabad', 'Mysore', 'Nanded', 'Nashik', 'Nellore', 'Noida', 'Palakkad', 'Patna', 'Pondicherry', 'Prayagraj', 'Pune',
                          'Raipur', 'Rajkot', 'Rajahmundry', 'Ranchi', 'Rourkela', 'Salem', 'Sangli', 'Siliguri', 'Solapur', 'Srinagar', 'Sultanpur',
                          'Surat', 'Thiruvananthapuram', 'Thrissur', 'Tiruchirappalli', 'Tirunelveli', 'Tiruppur', 'Tiruvannamalai', 'Ujjain'
                          , 'Bijapur', 'Vadodara', 'Varanasi', 'Vasai-Virar City', 'Vijayawada', 'Visakhapatnam', 'Vellore', 'Warangal']
          
            if(location.capitalize() in x_y_cities):
                response = "Thank you , we need bit more details?"
                dispatcher.utter_message('----'+response)
            else:
                response = "We do not operate in the area yet. Can you please specify some other location?"
                dispatcher.utter_message('----'+response)
        except:
            response = "City name was not captured successfully."
            dispatcher.utter_message('----'+response)
        
class ActionSearchRestaurants(Action):
    def name(self):
        return 'action_restaurant'
    
    ## Code will search for the restaurant once all slots are filles except email request. 
    def run(self, dispatcher, tracker, domain):
        try:
            location = tracker.get_slot('location')
            cuisine = tracker.get_slot('cuisine')
            price_pref = tracker.get_slot('price_preference')
            d = resturant_dict(location,cuisine)
            response=""
            if d['results_found'] == 0:
                response= "No results for the preferences"
            else:
                df = resturants(d['restaurants'],5,price_pref)
                if(len(df)>0):
                    for x in df['bot_response']:
                        response=response+ "Found "+x+"\n"
                else:
                    response = "No results for the price preference"

            dispatcher.utter_message("-----"+response)
        except:
            response = 'We"re unable to lookup any restaurants in the given city location. Please try a different option'
            dispatcher.utter_message("-----"+response)

class ActionSendMail(Action):
    def name(self):
        return 'send_mail'
    
    ## Send email to the user
    def run(self, dispatcher, tracker, domain):
        try:
            location = tracker.get_slot('location')
            cuisine = tracker.get_slot('cuisine')
            price_pref = tracker.get_slot('price_preference')
            email_address = tracker.get_slot('email_address')
            d = resturant_dict(location,cuisine)
            response = resturants(d['restaurants'],10,price_pref)
            resp_dict=dict(response)
            sent_body=" "
        
            if(len(resp_dict['Resturant_Name'])>0):
                for x in range(0,len(resp_dict['Resturant_Name'])):
                    sent_body+='Resturant Name  : '+resp_dict['Resturant_Name'][x]+'\nLocation_Details : '+resp_dict['Location_Address'][x]+'\nAverage_Cost     : '+str(resp_dict['Average_Cost'][x])+'\nUser_Rating        : '+str(resp_dict['User_Rating'][x])+'\n\n'
                    sent_body+="***This is an automatically generated email, please do not reply***"
                
                sent_to = email_address
                send_mail(sent_to,sent_body,location)
                response = 'Mail has been sent to the given mail address'
                dispatcher.utter_message("-----"+response)
            else:
                response = 'No Resturants found for the given preference, no mail sent'
                dispatcher.utter_message("-----"+response)
        except:
            response = 'We"re unable to send email. Please check if email is valid'
            dispatcher.utter_message("-----"+response)

class ActionMailRequest(Action):
    def name(self):
        return "mail_request"
    ## Ask user if she wants to send the details over email. If yes, bot will ask for a valid email address
    def run(self, dispatcher, tracker, domain):
        email_request = tracker.get_slot('email_request')
        if(re.search('yes',email_request.lower())):
            dispatcher.utter_message('Thank you , need last detail?')
        else:
            dispatcher.utter_message('Thank You, Bye')