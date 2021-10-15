from linebot.models import (QuickReply, QuickReplyButton, PostbackAction)

food_type_reply = QuickReply(
    items=[
        QuickReplyButton(
            action=PostbackAction(label="咖哩", data="咖哩")
        ),
        QuickReplyButton(
            action=PostbackAction(label="火鍋", data="火鍋")
        ),
        QuickReplyButton(
            action=PostbackAction(label="餃子", data="餃子")
        ),
        QuickReplyButton(
            action=PostbackAction(label="小吃", data="小吃")
        ),
        QuickReplyButton(
            action=PostbackAction(label="健康", data="健康")
        ),
        QuickReplyButton(
            action=PostbackAction(label="鐵板燒", data="鐵板燒")
        ),
        QuickReplyButton(
            action=PostbackAction(label="義式", data="義式")
        ),
        QuickReplyButton(
            action=PostbackAction(label="東南亞", data="東南亞")
        ),
        QuickReplyButton(
            action=PostbackAction(label="素食", data="素食")
        ),
        QuickReplyButton(
            action=PostbackAction(label="便當", data="便當")
        ),
        QuickReplyButton(
            action=PostbackAction(label="美式", data="美式")
        ),
        QuickReplyButton(
            action=PostbackAction(label="日韓", data="日韓")
        ),
        QuickReplyButton(
            action=PostbackAction(label="滷味", data="滷味")
        )
    ]
)
