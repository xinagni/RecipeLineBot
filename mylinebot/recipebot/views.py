from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

 
from .scrape import Recipe

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
 
 
@csrf_exempt
def callback(request):
 
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:

            if isinstance(event, MessageEvent):  # 如果有訊息事件
                message = []
                if event.message.type == 'text':
                    mtext = event.message.text
                    if mtext == '嗨':
                        line_bot_api.reply_message(event.reply_token,
                            TemplateSendMessage(
                                    alt_text='Buttons Template',
                                    template=ButtonsTemplate(
                                        title='找食譜',
                                        text='請選擇使用甚麼方式找尋食譜',
                                        thumbnail_image_url='https://www.hucc-coop.tw/uploads/03%E9%A3%9F%E8%AD%9C%E5%9C%96%E6%AA%94/%E7%B5%9E%E8%82%89%E6%BC%A2%E5%A0%A1%E6%8E%92.jpg',
                                        actions=[
                                            MessageTemplateAction(
                                                label='依食材搜尋',
                                                text='依食材搜尋'
                                            ),
                                            MessageTemplateAction(
                                                label='依料理類型搜尋',
                                                text='依料理類型搜尋'
                                            )
                                        ]
                                    )
                            )
                        )
                    
                    elif mtext == '依食材搜尋':
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text="請輸入食材：\n(如需多個食材請用空白分離)\n格式：搜尋 [食材] [食材]\n範例:搜尋 番茄 蛋 牛肉")
                        )
                    
                    elif mtext == '依料理類型搜尋':
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text="請輸入料理類型：\n格式：搜尋 [料理類型]\n範例 : 搜尋 日式料理")
                        )
                    
                    elif "搜尋" in mtext:
                        cook1 = Recipe(mtext.replace("搜尋 ",""))
                        content = cook1.scrape()
                        print(content[0])
                        line_bot_api.reply_message(event.reply_token,
                            TemplateSendMessage(
                                alt_text='Carousel template',
                                template=CarouselTemplate(
                                    columns=[
                                        CarouselColumn(
                                            thumbnail_image_url=content[0][3],
                                            title=content[0][0],
                                            text=str(content[0][4]),
                                            actions=[
                                                MessageTemplateAction(
                                                    label='顯示食材',
                                                    text= "▼" + content[0][0] + "▼\n----------\n" + content[0][1]
                                                ),
                                                MessageTemplateAction(                                                     
                                                    label='顯示步驟',
                                                    text=content[0][2]
                                                )]),
                                        CarouselColumn(
                                            thumbnail_image_url=content[1][3],
                                            title=content[1][0],
                                            text=str(content[1][4]),
                                            actions=[
                                                MessageTemplateAction(
                                                    label='顯示食材',
                                                    text= "▼\n" + content[1][0] + "▼\n----------\n" + content[1][1]
                                                ),
                                                MessageTemplateAction(                                                     
                                                    label='顯示步驟',
                                                    text=content[1][2]
                                                )]),
                                        CarouselColumn(
                                            thumbnail_image_url=content[2][3],
                                            title=content[2][0],
                                            text=str(content[2][4]),
                                            actions=[
                                                MessageTemplateAction(
                                                    label='顯示食材',
                                                    text= "▼" + content[2][0] + "▼\n----------\n" + content[2][1]
                                                ),
                                                MessageTemplateAction(                                                     
                                                    label='顯示步驟',
                                                    text=content[2][2]
                                                )]),
                                        CarouselColumn(
                                            thumbnail_image_url=content[3][3],
                                            title=content[3][0],
                                            text=str(content[3][4]),
                                            actions=[
                                                MessageTemplateAction(
                                                    label='顯示食材',
                                                    text= "▼" + content[3][0] + "▼\n----------\n" + content[3][1]
                                                ),
                                                MessageTemplateAction(                                                     
                                                    label='顯示步驟',
                                                    text=content[3][2]
                                                )]),
                                        CarouselColumn(
                                            thumbnail_image_url=content[4][3],
                                            title=content[4][0],
                                            text=str(content[4][4]),
                                            actions=[
                                                MessageTemplateAction(
                                                    label='顯示食材',
                                                    text= "▼" + content[4][0] + "▼\n----------\n" + content[4][1] 
                                                ),
                                                MessageTemplateAction(                                                     
                                                    label='顯示步驟',
                                                    text=content[4][2]
                                                )])
                                    ]
                                )
                            )
                        )

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
