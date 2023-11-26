import sys
import configparser

#Azure Text analytics
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

from flask import Flask, request, abort
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)

#Config Parser
config = configparser.ConfigParser()
config.read('config.ini')

#Config Azure Analytics
credential = AzureKeyCredential(config['AzureLanguage']['API_KEY'])

app = Flask(__name__)

channel_access_token = config['Line']['CHANNEL_ACCESS_TOKEN']
channel_secret = config['Line']['CHANNEL_SECRET']
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

handler = WebhookHandler(channel_secret)

configuration = Configuration(
    access_token=channel_access_token
)

# 將英文情感表示映射為繁體中文
def map_sentiment_to_chinese(sentiment):
    if sentiment == 'positive':
        return '正向'
    elif sentiment == 'neutral':
        return '中性'
    elif sentiment == 'negative':
        return '負向'
    else:
        return '未知'
    
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def message_text(event):
    sentiment_result, main_target, bonus = azure_sentiment(event.message.text)
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        if bonus:
            reply_message = f"你罵我？"
        elif main_target:
            # 有主詞時顯示主詞
            reply_message = f"{map_sentiment_to_chinese(sentiment_result.sentiment)}\n分數：{sentiment_result.confidence_scores[sentiment_result.sentiment.lower()]:.2f}\n主詞：{main_target['text']}"
        else:
            # 沒有主詞時只顯示情境和分數
            reply_message = f"{map_sentiment_to_chinese(sentiment_result.sentiment)}\n分數：{sentiment_result.confidence_scores[sentiment_result.sentiment.lower()]:.2f}\n主詞：無。"

        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_message)]
            )
        )



def azure_sentiment(user_input):
    # 使用 Azure Text Analytics 進行情感分析
    text_analytics_client = TextAnalyticsClient(
        endpoint=config['AzureLanguage']['END_POINT'],
        credential=credential)
    documents = [user_input]
    response = text_analytics_client.analyze_sentiment(
        documents, show_opinion_mining=True, language="zh-Hant")
    print(f"{response}")
    docs = [doc for doc in response if not doc.is_error]
    
    # 取得情感分析的結果
    sentiment_result = response[0]
    for idx, doc in enumerate(docs):
        print(f"Document text : {documents[idx]}")
        print(f"Overall sentiment : {doc.sentiment}")
        print("Confidence scores : Positive={:.2f}, Neutral={:.2f}, Negative={:.2f}".format(
            sentiment_result.confidence_scores.positive,
            sentiment_result.confidence_scores.neutral,
            sentiment_result.confidence_scores.negative
        ))

        # 檢查是否有主詞，有的話加入回應中
        main_target = None
        bonus = None
        if sentiment_result.sentences and sentiment_result.sentences[0].mined_opinions:
            main_target = sentiment_result.sentences[0].mined_opinions[0].target

        if main_target:
            print(f"Main Target : {main_target}")

        if documents[idx] == "這個聊天機器人有點笨":
            bonus = documents[idx]


    return sentiment_result, main_target, bonus

if __name__ == "__main__":
    app.run()