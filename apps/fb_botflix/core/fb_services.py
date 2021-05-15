import json, requests, re
from pprint import pprint
from constants.questions import questions
from constants.keys import fb_url, fb_access_token


#create optional question with buttons using questions saved on constants
def create_response_by_question(question_id):
    question = next(item for item in questions if item['id'] == question_id)
    if question['options']:
        #if has options show the options
        buttons = []
        for option in question['options']:
            buttons.append({
                "type": "postback",
                "payload": option['id'],
                "title": option['text']
            })

        return {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type":"button",
                        "text": question['text'],
                        "buttons": buttons
                    }
                }
            }
    else:
        # if doesn't have options means is the final of the test
        return {
            "text": question['text']
        }

#create text messages
def create_text_message(user_name, recevied_messages):
    #get all messages
    messages_list = re.sub(r"[^a-zA-Z0-9\s]",' ',recevied_messages).lower().split()
    #if message is 'start' means that the test begins and call the first question.
    if messages_list[0] == 'start':
        message = create_response_by_question(1)
    else :
        message = { "text": 'Hola '+ user_name +' no sabes que serie ver hoy? escribe start para comenzar el test.'}
    return message

def fb_interpret_message(fb_user_id, type_message, payload):
    #get user data
    user_details_url = fb_url+fb_user_id
    user_details_params = {
        'fields':'first_name,last_name,profile_pic', 
        'access_token': fb_access_token}
    user_details = requests.get(user_details_url, user_details_params).json()
    
    #get message by type
    if type_message == 'message':
        message = create_text_message(user_details['first_name'], payload)
    if type_message == 'postback':
        message = create_response_by_question(int(payload['payload']))
    
    post_message_url = fb_url +'me/messages?access_token='+ fb_access_token 
    response_msg = json.dumps({
        "recipient":{"id":fb_user_id}, 
        "message": message
    })

    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())
