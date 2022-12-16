#%%
from twilio.rest import Client 
import pandas as pd

#%%



#%%
def send_sms_epic_to(recipient, body, account_sid, auth_token):
    client = Client(account_sid, auth_token) 
    message = client.messages.create(body = body,
                                    from_ = '+16508307908',        
                                    to = recipient 
                                )


# phone_numbers = {
#     "kristin" : "+15038930864",
#     "porter"  : "+17193385009",
#     "nate"    : "+15035803396"
# }

# monday 8
# tue 9
# wed 7:33
# thu 8:11
# fri 10:18
# sunday 9
# phone_numbers = ["+15038930864", "+17193385009", "+15035803396", "+19712005681", "+18016693768", "+13852303728"]
# __to__ = ["+17193385009", "+17192002026"]
# def main(recipient, body):
#     send_sms_epic_to(recipient, body)