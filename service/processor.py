from sqlalchemy import create_engine
import pandas as pd
import json
import sys
import time
import os
import time
sys.path.append(".")
from helper.facebookHelper import FacebookUtility
from helper.requestHelper import RequestUtility
from helper.whatsappHelper import WhatsappUtility
from config.config import DB_NAME, TENANT_ID, API_KEY, CHANNEL_FACEBOOK, CHANNEL_TELEGRAM, CHANNEL_WEB, CHANNEL_WHATSAPP, EBOTIFY_URL

channel = {}

class ProcessorUtils():
    def __init__(self):
        self.db_name = DB_NAME
        self.tenant_id = TENANT_ID
        self.api_key = API_KEY
        self.channel_facebook = int(CHANNEL_FACEBOOK)
        self.channel_telegram = int(CHANNEL_TELEGRAM)
        self.channel_whatsapp = int(CHANNEL_WHATSAPP)
        self.channel_web = int(CHANNEL_WEB)
        self.ebotify_url = EBOTIFY_URL
        self.timeout_time = 10
        self.record_inserted = 0
    
    def get_sessionId(self, record):
        senderId = self.get_senderId(record)
        self.set_channel(record)

        if channel[senderId] == 6 or channel[senderId] == 1 or channel[senderId] == 0:
            sessionId = senderId+"-"+self.api_key
        elif channel[senderId] == 2:
            sessionId = record.get('sender_id')
        return sessionId

    def get_senderId(self, record):
        return record.get('sender_id')

    def get_timestamp(self, record):
        return time.time() * 1000000000

    def set_channel(self, record):
        senderId = self.get_senderId(record)
        if senderId in channel.keys():
            pass
        else:
            if record.get('input_channel') == "facebook":
                channel[senderId] = self.channel_facebook
            elif record.get('input_channel') == "telegram":
                channel[senderId] = self.channel_telegram
            elif record.get('input_channel') == "whatsapp":
                channel[senderId] = self.channel_whatsapp
            elif (record.get('input_channel') == "socketio") or (record.get('input_channel') == "rest") :
                channel[senderId] = self.channel_web
            elif record.get('input_channel') == "API":
                channel[senderId] = self.channel_whatsapp # check here
        return

    def get_info(self, record, sender):
        info = []
        fullname = ''
        sessionId = self.get_sessionId(record)
        senderId = self.get_senderId(record)

        if channel[senderId] == 6:
            facebook_name = FacebookUtility(senderId)
            fullname = facebook_name.get_Name()

            if fullname is not None:
                info.append({'key':'name','value':fullname})

        if channel[senderId] == 0:
            fullname = None
            try:
                whatsapp_utility = WhatsappUtility()
                fullname = whatsapp_utility.get_Name(record)
                
                if fullname is not None:
                    info.append({'key':'name','value':fullname})
            except:
                info.append({'key':'name','value': senderId})

        if channel[senderId] == 2:
            info.append({'key':'name','value':'Web User'})

        if channel[senderId] == 1:
            info.append({'key':'name','value':'Telegram User'})

        if sessionId is not None:
            info.append({'key': 'uniqueId', 'value': sessionId})
            
        if senderId is not None:
            info.append({'key': 'biriId', 'value': senderId})

            if channel[senderId] == 0:
                if fullname is None:
                    info.append({'key': 'mobileNo', 'value': ' - '})
                else:
                    info.append({'key': 'mobileNo', 'value': senderId})
        
        if sender == 2:
            if fullname is None:
                print("inside fullname")
                info.append({'key': 'intent', 'value': 'Notification'})
            else:
                parse_data = record.get('parse_data')
                intent = parse_data.get('intent')
                name = intent.get('name')
                if name is not None:
                    info.append({'key': 'intent', 'value': name})

                    if name == "number_entry" : # business logic
                        print("number_entry intent detected")
                        return        
        
        return info

    def get_message(self, record):
        messages = []

        text = record.get('text')
        if text is not None:
            messages.append({"type": "text", "message": text})

        data = record.get('data')

        if data is not None:
            image = data.get('image')
            
            buttons = data.get('buttons')

            quick_replies = data.get('quick_replies')

            attachment = data.get('attachment')

            if (attachment is not None) and (type(attachment)!= str):
                type_a = attachment.get('type')
                if type_a == "video":
                    url = attachment.get('payload').get('src')
                    messages.append({"type": "video", "message": url})
                    
                if type_a == "template":
                    payload = attachment.get('payload')
                    template_type = payload.get('template_type')
                    if template_type == "generic":
                        cards = payload.get('elements')
                        messages.append({"type": "carousel", "message": cards})
                        
                if type_a == "document":
                    url = attachment.get('document')
                    messages.append({"type": "pdf", "message": url})  # currently we can send pdf only
                
                if type_a == "audio":
                    url = attachment.get('payload').get('src')
                    messages.append({"type": "audio", "message": url})

                if type_a == "image":
                    url = attachment.get('payload').get('src')
                    caption = attachment.get('payload').get('caption')
                    messages.append({"type": "image", "message": url})
                    messages.append({"type": "text", "message": caption})

            custom = data.get("custom")
            if custom is not None:
                attachment = custom.get('attachment')

                if attachment is not None:
                    type_a = attachment.get('type')
                    if type_a == "video":
                        payload = attachment.get('payload')
                        video = payload.get('url')
                        messages.append({"type": "video", "message": video})
                    if type_a == "template":
                        payload = attachment.get('payload')
                        template_type = payload.get('template_type')
                        if template_type == "generic":
                            cards = payload.get('elements')
                            messages.append(
                                {"type": "carousel", "message": cards})
                
                type_custom = custom.get("type")
                if type_custom == "email":
                    messages.append({"type": "email", "message": custom})
                if type_custom == "phone_number":
                    messages.append({"type": "phone_number", "message": custom})
                if type_custom == "calender":
                    type_calender = custom.get("calender_type")
                    if type_calender == "date":
                        messages.append({"type": "date", "message": custom})
                    if type_calender == "date_time":
                        messages.append({"type": "date_time", "message": custom})
                    if type_calender == "multi_date":
                        messages.append({"type": "multi_date", "message": custom})
                    if type_calender == "multi_date_time":
                        messages.append({"type": "multi_date_time", "message": custom})

            if image is not None:
                messages.append({"type": "image", "message": image})

            if buttons is not None:
                for button in buttons:
                    messages.append({"type": "button", "message": button.get('title')})

            if quick_replies is not None:
                for button in quick_replies:
                    messages.append({"type": "button", "message": button.get('title')})
    
        return messages
    
    def send_message(self, record, sender):
        try:
            message = {
                'sessionId': self.get_sessionId(record),
                'tenantId': self.tenant_id,
                'apiKey': self.api_key,
                'messages': self.get_message(record),
                'sender': sender,
                'channel': channel[self.get_senderId(record)],
                "timestamp": self.get_timestamp(record),
                'info': self.get_info(record, sender)
            }
            if message.get('info') is not None:
                message=json.dumps(message)
                print('\n** Queue Message {} ** =>\n{}\n'.format(self.record_inserted, message))
                request_utility = RequestUtility()
                response = request_utility.send_request("POST", self.ebotify_url, message)
                print(response)
            
            else:
                print('Empty info')

        except Exception as e:
            print('inside exception')
            print(e)
        finally:
            return


    def get_data(self, last_db_id):
        query = '''
        SELECT *, data as records FROM events WHERE id > {} AND (data LIKE '%"event": "user"%' OR data LIKE '%"event": "bot"%');
        ''' .format(last_db_id)

        database = create_engine(self.db_name)
        data_frame = pd.read_sql_query(query, database)
        data = json.loads(data_frame.to_json())

        records = data.get('records')
        db_ids = data.get('id')

        for number in records:
            self.record_inserted = db_ids[number]
            record = json.loads(records[number])
            if record.get('event') == 'bot':
                self.send_message(record, 1)
            elif record.get('event') == 'user':
                self.send_message(record, 2)

        return

    def start_precessor(self):
        while (1):
            try:
                self.get_data(self.record_inserted)
                time.sleep(self.timeout_time)
                print('\n\n\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Timeout $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n\n\n')
            except:
                error = sys.exc_info()
                print('Error : {}' .format(error))
                continue

        return

processor_utils = ProcessorUtils()
processor_utils.start_precessor()