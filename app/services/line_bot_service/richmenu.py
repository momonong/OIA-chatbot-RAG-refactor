
import os
import sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import time
import linebot.v3.messaging
from linebot.v3.messaging.models.rich_menu_id_response import RichMenuIdResponse
from linebot.v3.messaging.rest import ApiException
from pprint import pprint
from asyncdatabase import Database



from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    MessagingApiBlob,
    RichMenuRequest,
    RichMenuArea,
    RichMenuSize,
    RichMenuBounds,
    URIAction,
    RichMenuSwitchAction,
    CreateRichMenuAliasRequest,
    MessageAction
)

channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

configuration = Configuration(
    access_token=channel_access_token
)
TOP_LEFT = {
    "bounds": {
        "x": 0,
        "y": 0,
        "width": 1250,
        "height": 843
    }
}
TOP_RIGHT = {
    "bounds": {
        "x": 1250,
        "y": 0,
        "width": 1250,
        "height": 843
    }
}
BOTTOM_LEFT = {
    "bounds": {
        "x": 0,
        "y": 843,
        "width": 1250,
        "height": 843
    }
}
BOTTOM_RIGHT = {
    "bounds": {
        "x": 1250,
        "y": 843,
        "width": 1250,
        "height": 843
    }
}


def rich_menu_object_c_json(_name='', _barname=''):
    return {
        "size": {
            "width": 2500,
            "height": 1686
        },
        "selected": False,
        "name": _name,
        "chatBarText": _barname,
        "areas": [
            {
                "bounds": {
                    "x": TOP_LEFT['bounds']['x'],
                    "y": TOP_LEFT['bounds']['y'],
                    "width": TOP_LEFT['bounds']['width'],
                    "height": TOP_LEFT['bounds']['height']
                },
                "action": {
                    "type": "text",
                    "text": "switch language"
                }
            },
            {
                "bounds": {
                    "x": TOP_RIGHT['bounds']['x'],
                    "y": TOP_RIGHT['bounds']['y'],
                    "width": TOP_RIGHT['bounds']['width'],
                    "height": TOP_RIGHT['bounds']['height']
                },
                "action": {
                    "type": "uri",
                    "uri": "https://docs.google.com/forms/d/e/1FAIpQLSfbz0JUPqNDQ52owFHXLwYgBPEUIHm8yQgxcSEhj12IZMdDgw/viewform"
                }
            },
            {
                "bounds": {
                    "x": BOTTOM_LEFT['bounds']['x'],
                    "y": BOTTOM_LEFT['bounds']['y'],
                    "width": BOTTOM_LEFT['bounds']['width'],
                    "height": BOTTOM_LEFT['bounds']['height']
                },
                "action": {
                    "type": "uri",
                    "uri": "https://drive.google.com/file/d/1F54hz1VJmB9VmDCfEmvMNCOZ6ln4jQP9/view?usp=sharing"
                }
            },
            {
                "bounds": {
                    "x": BOTTOM_RIGHT['bounds']['x'],
                    "y": BOTTOM_RIGHT['bounds']['y'],
                    "width": BOTTOM_RIGHT['bounds']['width'],
                    "height": BOTTOM_RIGHT['bounds']['height']
                },
                "action": {
                    "type": "uri",
                    "uri": "https://liff.line.me/2005821112-DoNkm4zM"
                }}
        ]
    }


def create_action(action):
    if action['type'] == 'uri':
        return URIAction(uri=action.get('uri'))
    elif action['type'] == 'text':
        return MessageAction(text=action.get('text'))
    else:
        return RichMenuSwitchAction(
            rich_menu_alias_id=action.get('richMenuAliasId'),
            data=action.get('data')
        )


def create_rich_menu(alias_name: str, _rich_menu_object, image_path=''):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_blob_api = MessagingApiBlob(api_client)
        rich_menu_object = _rich_menu_object
        if alias_name == 'zh' or alias_name == 'en':
            areas = [
                RichMenuArea(
                    bounds=RichMenuBounds(
                        x=info['bounds']['x'],
                        y=info['bounds']['y'],
                        width=info['bounds']['width'],
                        height=info['bounds']['height']
                    ),
                    action=create_action(info['action'])
                ) for i, info in enumerate(rich_menu_object['areas']) if i < 3
            ]
        else:
            areas = [
                RichMenuArea(
                    bounds=RichMenuBounds(
                        x=info['bounds']['x'],
                        y=info['bounds']['y'],
                        width=info['bounds']['width'],
                        height=info['bounds']['height']
                    ),
                    action=create_action(info['action'])
                ) for info in rich_menu_object['areas']
            ]
        rich_menu_to_a_create = RichMenuRequest(
            size=RichMenuSize(width=rich_menu_object['size']['width'],
                              height=rich_menu_object['size']['height']),
            selected=rich_menu_object['selected'],
            name=rich_menu_object['name'],
            chat_bar_text=rich_menu_object['name'],
            areas=areas
        )
        rich_menu_id = line_bot_api.create_rich_menu(
            rich_menu_request=rich_menu_to_a_create
        ).rich_menu_id
        with open(image_path, 'rb') as image:
            line_bot_blob_api.set_rich_menu_image(
                rich_menu_id=rich_menu_id,
                body=bytearray(image.read()),
                _headers={'Content-Type': 'image/png'}
            )
        alias = CreateRichMenuAliasRequest(
            rich_menu_alias_id=alias_name,
            rich_menu_id=rich_menu_id
        )
        line_bot_api.create_rich_menu_alias(alias)
        print('success')
        return True


def set_rich_menu(alias_id, user_id):
    with linebot.v3.messaging.ApiClient(configuration) as api_client:
        try:
            api_instance = linebot.v3.messaging.MessagingApi(api_client)
            # step1: use rich-menu-alias to get rich-menu-id
            api_response = api_instance.get_rich_menu_alias(alias_id)
            print("The response of MessagingApi->get_rich_menu_alias:\n")
            pprint(api_response)
            # step2: link the rich-menu to selected user
            rich_menu_id = api_response.dict()['rich_menu_id']
            api_instance.link_rich_menu_id_to_user(user_id, rich_menu_id)
        except Exception as e:
            print("Exception when calling MessagingApi->link_rich_menu_id_to_user: %s\n" % e)


def set_default_rich_menu(alias_id):
    with linebot.v3.messaging.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = linebot.v3.messaging.MessagingApi(api_client)
        # step1: use rich-menu-alias to get rich-menu-id
        api_response = api_instance.get_rich_menu_alias(alias_id)
        print("The response of MessagingApi->get_rich_menu_alias:\n")
        pprint(api_response)
        # step2: link the rich-menu to selected user

        rich_menu_id = api_response.dict()['rich_menu_id']

        try:
            api_instance.set_default_rich_menu(rich_menu_id)
        except Exception as e:
            print("Exception when calling MessagingApi->set_default_rich_menu: %s\n" % e)


#main()
def reset_rich_menu():
    with linebot.v3.messaging.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = linebot.v3.messaging.MessagingApi(api_client)
        try:
            api_response = api_instance.get_rich_menu_list()
            #pprint(api_response)
            for menu in api_response.to_dict()['richmenus']:
                print(menu['richMenuId'])
                api_instance.delete_rich_menu(menu['richMenuId'])
            api_response = api_instance.get_rich_menu_alias_list()
            for menu in api_response.to_dict()['aliases']:
                print(menu['richMenuAliasId'])
                api_instance.delete_rich_menu_alias(menu['richMenuAliasId'])
        except Exception as e:
            print("Exception when calling MessagingApi->get_rich_menu_list: %s\n" % e)


async def initialize_rich_menu(database):
    with linebot.v3.messaging.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = linebot.v3.messaging.MessagingApi(api_client)
        try:
            api_response = api_instance.get_rich_menu_list()
            #pprint(api_response)
            for menu in api_response.to_dict()['richmenus']:
                print(menu['richMenuId'])
                api_instance.delete_rich_menu(menu['richMenuId'])
            api_response = api_instance.get_rich_menu_alias_list()
            for menu in api_response.to_dict()['aliases']:
                print(menu['richMenuAliasId'])
                api_instance.delete_rich_menu_alias(menu['richMenuAliasId'])
        except Exception as e:
            print("Exception when calling MessagingApi->get_rich_menu_list: %s\n" % e)
    create_rich_menu('zh', rich_menu_object_c_json(_name='Chinese', _barname='Chinese'), 'image/chinese.png')
    create_rich_menu('en', rich_menu_object_c_json(_name='English', _barname='English'), 'image/english.png')
    create_rich_menu('zh-escalation', rich_menu_object_c_json(_name='Chinese', _barname='Chinese'), 'image/chinese-escalation.png')
    create_rich_menu('en-escalation', rich_menu_object_c_json(_name='English', _barname='English'), 'image/english-escalation.png')
    all_user_info=await database.get_all_users_info('info')
    for user_info in all_user_info:
        language = 'en' if user_info['language'] == 'en' else 'zh'
        mode = '-escalation' if 'todo:1' in user_info['mode'] else ''
        set_rich_menu(language+mode, user_info['line_id'])
