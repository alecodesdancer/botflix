
import json
from django.views import generic
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from constants.keys import fb_verify_token
from .core.fb_services import fb_interpret_message



# Principal View. Here ir where the request arrives.
class BotflixView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == fb_verify_token:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error! Token is not valid.')
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)
    # Function that handle the FB messages
    def post(self, request, *args, **kwargs):
        # get & transform the messages
        messages = json.loads(self.request.body.decode('utf-8'))
        """ In case the user send more that one  messages we saved them on a dictionary """
        for entry in messages['entry']:
            for message in entry['messaging']:
                """
                    FB has multiple types of messages, in this case we're gonna handle
                    simple text message(message) & button (postback)
                """
                if 'message' in message:
                    fb_interpret_message(message['sender']['id'], 'message', message['message']['text'])
                if 'postback' in message:
                    fb_interpret_message(message['sender']['id'], 'postback', message['postback'])
                  
        return HttpResponse()