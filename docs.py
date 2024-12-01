import pygsheets
import pandas as pd
from datetime import datetime
import os

gc = pygsheets.authorize(service_file="/home/oiachatbot/ncku_oia_chatbot_refactor/credentials.json")    

def append_rating_record(name, score, current_time):
    sht = gc.open_by_url('https://docs.google.com/spreadsheets/d/1i8DrQDmIouS06YNh8-jocdBySpiIs5bg1AyBBOOygt8/edit?gid=0#gid=0')
    ws = sht.worksheet()
    data_to_append = [
        name,
        score,
        current_time 
    ]    
    try:
        ws.append_table(values=data_to_append, dimension='ROWS', overwrite=False)
    except Exception as e:
        pass




def log(message, response, t, name, mode):
    sht = gc.open_by_url('https://docs.google.com/spreadsheets/d/1tGk-W7S4sKaeA2BH7OnCJVPjJm-LlddJ67dkASBnSJg/edit?usp=sharing')
    ws = sht.worksheet()
    current_datetime = datetime.now()
    print(t)
    # 將日期和時間格式化為指定的字符串
    formatted_datetime = current_datetime.strftime('%Y/%m/%d %H:%M:%S')
    data_to_append = [
        formatted_datetime,
        message,
        response,
        t,
        mode,
        name
    ]
    try:
        ws.append_table(values=data_to_append, dimension='ROWS', overwrite=False)
    except Exception as e:
        print(f"Error appending log: {e}")


if __name__ == '__main__':
    import time
    append_student("123", "456", "Ubeeee573977c493cb830458ced3c754d")
    # todo_insert("hello", "123")
    # time.sleep(10)
    # cancel_todo("Ubeeee573977c493cb830458ced3c754d")





#     def todo_insert(message, user_id):
#     sht = gc.open_by_url('https://docs.google.com/spreadsheets/d/1TEI45VR0JFI2XzAmfunnMFppdGJTSXk14SsN33NEURY/edit?usp=sharing')
#     ws = sht.worksheet()
#     cell = ws.find(user_id)[0]
#     #print(cell)
#     ws.update_value(f'E{cell.row}', True)
#     ws.update_value(f'D{cell.row}', True)
#     ws.update_value(f'C{cell.row}', message)

# def cancel_todo(user_id):
#     sht = gc.open_by_url('https://docs.google.com/spreadsheets/d/1TEI45VR0JFI2XzAmfunnMFppdGJTSXk14SsN33NEURY/edit?usp=sharing')
#     ws = sht.worksheet()
#     cell = ws.find(user_id)[0]
#     ws.update_value(f'E{cell.row}', False)
#     ws.update_value(f'D{cell.row}', True)
#     #ws.update_value(f'C{cell.row}', "")
 

# def append_student(student_id, name, line_name, student_status, user_id):
#     sht = gc.open_by_url('https://docs.google.com/spreadsheets/d/1TEI45VR0JFI2XzAmfunnMFppdGJTSXk14SsN33NEURY/edit?usp=sharing')
#     ws = sht.worksheet()
#     data_to_append = [
#         student_id,
#         name,
#         "",
#         True,
#         False,
#         line_name,
#         "student",
#         student_status,
#         user_id,
#     ]    
#     try:
#         ws.append_table(values=data_to_append, dimension='ROWS', overwrite=False)
#     except Exception as e:
#         pass


# def append_non_student(name, line_name, identity, user_id):
#     sht = gc.open_by_url('https://docs.google.com/spreadsheets/d/1TEI45VR0JFI2XzAmfunnMFppdGJTSXk14SsN33NEURY/edit?usp=sharing')
#     ws = sht.worksheet()
#     data_to_append = [
#         "",
#         name,
#         "",
#         True,
#         False,
#         line_name,
#         identity,
#         "",
#         user_id
#     ]
#     try:
#         ws.append_table(values=data_to_append, dimension='ROWS', overwrite=False)
#     except Exception as e:
#         pass