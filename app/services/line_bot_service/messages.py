from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.models import FlexSendMessage
import json




class EscalationMessage:
    def __init__(self, language):
        self.language = language

    def create_escalation_status_message(self):
        msg = {
            'zh': '請等待專人服務, 若要取消真人服務請點選 https://liff.line.me/2005821112-DoNkm4zM',
            'en': 'Please wait for a human service. If you want to cancel the human service, please click on the link https://liff.line.me/2005821112-DoNkm4zM.'
        }
        return TextMessage(text=msg[self.language])
        
    def create_escalation_info_message(self):
        msg = {
            'zh': '''
若你認為這個回答沒有幫助請點選 
https://liff.line.me/2005821112-DoNkm4zM
我們會將訊息轉交給真人服務
        ''',
        'en': '''
If you feel that this answer is not helpful, please click on the link 
https://liff.line.me/2005821112-DoNkm4zM
We will forward the message to a human service
        '''
        }
        return "\n" + msg[self.language]



class NotifyRegisterMessage:
    def create_message(self):
        return TextMessage(text='''若您是已經有學號的學生請先點選以下連結註冊以啟用服務\n
If you are a student who already has a student ID, please click the following link to register first to enable service.
https://liff.line.me/2005821112-eyqO6WR5

若您是校外人士，或尚未取得學號請點選以下連結註冊以啟用服務\n
If you are outside the school or have not yet obtained a student ID, please click the link below to register to activate the service.
https://liff.line.me/2005821112-y2RGX5Ep''')



class MessageFormatter:
    @staticmethod
    def clean_response(response):
        return response.replace("回答: ", "").replace("reply:", "").lstrip("\n")

class RatingMessage:
    @staticmethod
    def create_rating_message(response, language):
        with open("flex.json", "r", encoding="utf-8") as jsonfile:
            flex_message = json.load(jsonfile)
        
        flex_message["header"]["contents"][0]["text"] = MessageFormatter.clean_response(response)
        flex_message["header"]["contents"][1]["text"] = EscalationMessage(language).create_escalation_info_message()
        return FlexSendMessage(alt_text="rating", contents=flex_message)

class NormalMessage:
    @staticmethod
    def create_normal_message(response, language):
        cleaned_response = MessageFormatter.clean_response(response)
        escalation_info = EscalationMessage(language).create_escalation_info_message()
        return TextMessage(text=f"{cleaned_response}{escalation_info}")


