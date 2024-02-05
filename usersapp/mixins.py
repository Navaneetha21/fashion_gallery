# from django.conf import settings
# from twilio.rest import Client
# import random
# class MessageHandler:
#     phone_number=None
#     otp=None
#     def __int__(self,phone_number,otp)->None:
#         self.phone_number=phone_number
#         self.otp=otp
#     def send_otp_on_phone(self):
#         client=Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)
#         messange=client.messages.create(body=f'Your OTP is {self.otp}',from_='9995917284',to=self.phone_number)
