from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('UzFnhrsqy19REPz39xCFMhTB8M+49+STi2gjerNG8yicwbe1VXcPlEB0+zw0RkFONbLUGQRdiMWojVoEgACwTTxj8/Lnbm/MYX3jSKmsVf+KymyNknKf/MUOnWID3pie7q0tl+7LNSIJleQ/7GoARgdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('56d1a8ab519fd0dfe6480dd78948ba4b')

@app.route("/webhook", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # Get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

user_context = ''
total_income = 0
total_expense = 0

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    user_id = event.source.user_id
    global user_context,total_income, total_expense

    if text.lower() == 'รายรับ':
        user_context = 'รายรับ'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='กรุณากรอกจำนวนเงินที่ได้รับ:'))
    elif text.lower() == 'รายจ่าย':
        user_context = 'รายจ่าย'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='กรุณากรอกจำนวนเงินที่ใช้จ่าย:'))
    elif text.isdigit():
        amount = int(text)
        if user_context == 'รายรับ':
            record_transaction(user_id, 'income', amount)
            total_income += amount
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f'บันทึกรายรับเรียบร้อยแล้ว: {amount} บาท'))
        elif user_context == 'รายจ่าย':
            record_transaction(user_id, 'expense', amount)
            total_expense += amount
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f'บันทึกรายจ่ายเรียบร้อยแล้ว: {amount} บาท'))
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='กรุณาเลือก "รายรับ" หรือ "รายจ่าย" ก่อนที่จะกรอกจำนวนเงิน'))
    
    elif text.lower() == 'ยอดรวม':
        In = int(total_income)
        Out = int(total_expense)
        if In > 0 or Out > 0:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f'ยอดรวมรายรับ: {In} บาท\nยอดรวมรายจ่าย: {Out} บาท'))
        else:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='ยังไม่มีรายรับหรือรายจ่ายถูกบันทึก'))

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='ขอโทษครับ ฉันไม่เข้าใจข้อความที่คุณส่ง'))
    

def record_transaction(user_id, type, amount):
    pass


