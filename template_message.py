def escalation_info(language):
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
    return "\n" + msg[language]


def escalation_status(language):
    msg = {
        'zh': '請等待專人服務, 若要取消真人服務請點選 https://liff.line.me/2005821112-DoNkm4zM',
        'en': '''Please wait for a human service. 
        If you want to cancel the human service, please click on the link https://liff.line.me/2005821112-DoNkm4zM.'''
    }
    return msg[language]


def notify_register():
    return ('''若您是已經有學號的學生請先點選以下連結註冊以啟用服務\n
If you are a student who already has a student ID, please click the following link to register first to enable service.
https://liff.line.me/2005821112-eyqO6WR5

若您是校外人士，或尚未取得學號請點選以下連結註冊以啟用服務\n
If you are outside the school or have not yet obtained a student ID, please click the link below to register to activate the service.
https://liff.line.me/2005821112-y2RGX5Ep''')


