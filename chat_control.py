import time
import os
import linebot.v3.module
from linebot.v3.module.models.acquire_chat_control_request import AcquireChatControlRequest
from linebot.v3.module.rest import ApiException
from pprint import pprint
from dotenv import load_dotenv

'''
Use of optional functions requires an application
Only corporate users who have submitted the required applications can use the functions described in this document. 
To use these functions with your LINE Official Account, contact your sales representative or contact our Sales partners
https://developers.line.biz/en/reference/partner-docs/#send-mission-stickers-v3
'''

# Defining the host is optional and defaults to https://api.line.me
# See configuration.py for a list of all supported configuration parameters.
configuration = linebot.v3.module.Configuration(
    host = "https://api.line.me"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.
load_dotenv()
# Configure Bearer authorization: Bearer
configuration = linebot.v3.module.Configuration(
    access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')
)

def acquire(chat_id):
    # Enter a context with an instance of the API client
    with linebot.v3.module.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = linebot.v3.module.LineModule(api_client)
        #chat_id = 'Ubeeee573977c493cb830458ced3c754d' # str | The `userId`, `roomId`, or `groupId`
        acquire_chat_control_request = linebot.v3.module.AcquireChatControlRequest() # AcquireChatControlRequest |  (optional)

        try:
            api_instance.acquire_chat_control(chat_id, acquire_chat_control_request=acquire_chat_control_request)
        except Exception as e:
            print("Exception when calling LineModule->acquire_chat_control: %s\n" % e)

def release(chat_id):
    # Enter a context with an instance of the API client
    with linebot.v3.module.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = linebot.v3.module.LineModule(api_client)
        #chat_id = 'chat_id_example' # str | The `userId`, `roomId`, or `groupId`

        try:
            api_instance.release_chat_control(chat_id)
        except Exception as e:
            print("Exception when calling LineModule->release_chat_control: %s\n" % e)

