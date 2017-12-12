# coding: utf-8

from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from watson_developer_cloud import LanguageTranslatorV2 as LanguageTranslator

language_translator = LanguageTranslator(
  username = "{{ username }}",
  password = "{{ password }}"
)

@listen_to(r'.+')                   # 正規表現.すべての発言をリッスンする.
def listen_func(message):
    text = message.body['text']     # メッセージを取り出す
    language = language_translator.identify(text) # 言語識別
    source = language['languages'][0]['language']
    if source not in ['ja','de'] :
        source = 'en'
        target1 = 'ja'
        target2 = 'de'
        msg1 = language_translator.translate(
            text=text,
            source=source,
            target=target1)
        msg2 = language_translator.translate(
            text=text,
            source=source,
            target=target2)
    else :
        if source == 'ja':
            target1 = 'en'
            target2 = 'de'
        elif source == 'de':
            target1 = 'en'
            target2 = 'ja'
        msg1 = language_translator.translate(
            text=text,
            source=source,
            target=target1)
        msg2 = language_translator.translate(
            text=msg1,
            source=target1,
            target=target2)
    message.send(msg1)      # target1への翻訳結果をsend
    message.send(msg2)      # target2への翻訳結果をsend
