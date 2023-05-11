# sanic import module
from sanic import text, Blueprint, json as Response, Sanic
from sanic.log import logger
# general ins
import aiomysql
import json
import random
import os
import smtplib
from twilio.rest import Client
from email.message import EmailMessage

#user_details_api     
async def user_details(request):
    host,port,username,password = list(request.app.config.database.values())
    # connecting to database
    mysql_db = await aiomysql.connect(host=host, port=port,user=username, password=password,db = "zogx_test")
    operator_my = await mysql_db.cursor()
    #data request
    email_id= request.json.get('email')
    first_name=request.json.get('first_name')
    last_name=request.json.get('last_name')
    pass_word=request.json.get('pass_word')
    phone_number=int(request.json.get('phone_number'))   
    status=request.json.get('status')
    created_by=request.json.get('created_by')
    last_updated_by=request.json.get('last_updated_by')
    last_updated_data=request.json.get('last_updated_data')
    # inserting the data into db    
    await operator_my.execute(f"insert into user_details values '{email_id}','{first_name}','{last_name}','{pass_word}','{phone_number}','{status}','{created_by}','{last_updated_by}','{last_updated_by}','{last_updated_data}'")
    # closing mysql connectors
    await operator_my.close()
    mysql_db.close()
    return Response({'status':'success',"data":True,"msg":"Success"},status = 200)    
 
   
#user_login_api
async def user_login(request):
    host,port,username,password = list(request.app.config.database.values())
    # connecting to database
    mysql_db = await aiomysql.connect(host=host, port=port,user=username, password=password,db = "zogx_test")
    operator_my = await mysql_db.cursor()
    #data request
    email_id= request.json.get('email')
    pass_word=request.json.get('pass_word')
    #search the data into db  
    await operator_my.execute(f"select email_id,pass_word from user_details where email='{email_id}' and pass_word='{pass_word}'")  
    data = [json.loads(json.dumps([dict(zip(map(lambda x:x[0], operator_my.description),row)) for row in await operator_my.fetchall()],default = str))]
    # closing mysql connectors
    await operator_my.close()
    mysql_db.close()
    #login logic
    if len(data)== 0:
        return Response({"status":"Failure","data":False,"msg":"Invalid username or password"},status = 500)
    else:
        return Response({'status':'success',"data":True,"msg":'Successfully login'},status = 200)
 
        
#password_update_api
async def password_reset(request):
    host,port,username,password = list(request.app.config.database.values())
    # connecting to database
    mysql_db = await aiomysql.connect(host=host, port=port,user=username, password=password,db = "zogx_test")
    operator_my = await mysql_db.cursor()
    #data request
    email_id= request.json.get('email_id')
    old_password= request.json.get('old_password')
    new_password=request.json.get('new_password')
    #search the data into db   
    await operator_my.execute(f"select pass_word user_details where email='{email_id}'and pass_word='{old_password}'")
    data = [json.loads(json.dumps([dict(zip(map(lambda x:x[0], operator_my.description),row)) for row in await operator_my.fetchall()],default = str))] 
    # closing mysql connectors
    await operator_my.close()
    mysql_db.close()
    #update the data into db 
    if len(data) != 0:
        mysql_db = await aiomysql.connect(host=host, port=port,user=username, password=password,db = "zogx_test")
        operator_my = await mysql_db.cursor()
        await operator_my.execute(f"update user_details set pass_word='{new_password}' where email='{email_id}'and pass_word='{old_password}'")
        # closing mysql connectors
        await operator_my.close()
        mysql_db.close()
        return Response({'status':'success',"data":True,"msg":'Password Updated'},status = 200)
    else:
        return Response({"status":"Failure","data":False,"msg":"Invalid username or password"},status = 500)
     
#forgot_password_api   
async def forgot_password(request):
    temp=0
    host,port,username,password = list(request.app.config.database.values())
    # connecting to database
    mysql_db = await aiomysql.connect(host=host, port=port,user=username, password=password,db = "zogx_test")
    operator_my = await mysql_db.cursor()
    #data request
    email_id= request.json.get('email_id')
    phone_number=request.json.get('phone_number')
    #search the data into db  
    await operator_my.execute(f"select phone_number from passcode where email='{email_id}' and phone_number='{phone_number}'")  
    data = [json.loads(json.dumps([dict(zip(map(lambda x:x[0], operator_my.description),row)) for row in await operator_my.fetchall()],default = str))]
    # closing mysql connectors
    await operator_my.close()
    mysql_db.close()
    #forgot logic
    if len(data) ==0:
        return Response({"status":"Failure","data":False,"msg":"No Email or Phone Number found"},status = 500)
    # Send OTP through phone
    else:
        #genrate OTP 
        otp=''.join([str(random.randint(0,9)) for i in range(6)])
        #store the OTP in temporary variable to compare
        global n
        n = otp
        #Send OTP
        account_sid = '____twilio account SID ____'
        auth_token = '______twilio auth token_________'
        client = Client (account_sid, auth_token)
        msg= client.messages.create(body = f"Your OTP is {otp}",from_="______ twilio number_______",to='data')
        return Response({'status':'success',"data":True,"msg":"OTP is sended to Phone number"},status = 200)
   
#otp_verfiy_function
def to_verfiy(otp_number):
    if otp_number == n:
        return Response({'status':'success',"data":True,"msg":""},status = 200)
    else:
       return Response({"status":"Failure","data":False,"msg":"Invalid OTP Enter valid OTP"},status = 500)   
   
#forgot_password_api   
async def otp_verfiy(request):
    otp_number= request.json.get('otp_number')
    to_verfiy(otp_number)
    

        
   