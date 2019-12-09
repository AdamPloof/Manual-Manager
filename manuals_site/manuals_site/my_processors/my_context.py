from django.contrib.messages.api import get_messages

def custom_message_processor(request):
    # removes duplicate messages from message storage

    messages = []
    uniq_messages = []

    for m in get_messages(request):
        if m.message not in messages:
            messages.append(m.message)
            uniq_messages.append(m)
            
    return {'messages': uniq_messages}