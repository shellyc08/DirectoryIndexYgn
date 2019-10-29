import time
import string
from threading import Thread, Event
from flask import Flask, request, redirect
import messenger_utils
import sqlMethods
app = Flask(__name__)

GREETINGS = ['hi', 'hello', 'hey', 'search', 'find']
FLIRTS = ['love', 'like', 'smart', 'clever']
INSULTS = ['bot', 'stupid', 'dumb', 'hate']
THANKS = ['thank', 'thanks']
CATAGORIES_QUICK_REPLIES = messenger_utils.getCategories()
SESSION = {}

def is_ascii(text):
    if isinstance(text, unicode):
        try:
            text.encode('ascii')
        except UnicodeEncodeError:
            return False
    else:
        try:
            text.decode('ascii')
        except UnicodeDecodeError:
            return False
    return True

def preprocess(query):
    exclude = set(string.punctuation)
    exclude.discard("'")
    query = ''.join(ch for ch in query if ch not in exclude).lower()
    words = query.split(' ')
    stopwords = ['of', 'is', 'find', 'search']
    for stopword in stopwords:
        try:
            index = len(words) - words[::-1].index(stopword)
        except ValueError:
            index = -1

        if index > 0:
            processed_str = ' '.join(words[index:]) 
            if len(processed_str):
                query = processed_str
    return query.strip()

def small_talk(inputMsg, sender):
    for keyword in FLIRTS:
        if keyword in inputMsg:
            messenger_utils.reply(sender, messenger_utils.flirt())
            messenger_utils.reply(sender, messenger_utils.welcome())
            return True
    for keyword in INSULTS:
        if keyword in inputMsg:
            messenger_utils.reply(sender, messenger_utils.insult())
            messenger_utils.reply(sender, messenger_utils.welcome())
            return True
    for keyword in THANKS:
        if keyword in inputMsg:
            messenger_utils.reply(sender, messenger_utils.thank())
            return True
    return False

@app.route('/', methods=['GET'])
def handle_get():
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.verify_token') == 'secret':
        return request.args.get('hub.challenge')
    return redirect("https://www.facebook.com/yangonIndex", code=302)

@app.route('/', methods=['POST'])
def handle_incoming_messages():
    try:
        now = time.time()
        data = request.json
        sender = data['entry'][0]['messaging'][0]['sender']['id']
        if sender not in SESSION:
            SESSION[sender] = {"lastActive": now, "errorCount":0}

        if data['entry'][0]['messaging'][0].get("message") and data['entry'][0]['messaging'][0]['message'].get("quick_reply"):
            inputMsg = data['entry'][0]['messaging'][0]['message']['quick_reply']['payload']
        elif data['entry'][0]['messaging'][0].get("message") and data['entry'][0]['messaging'][0]['message'].get('text'):
            inputMsg = data['entry'][0]['messaging'][0]['message']['text']
        elif data['entry'][0]['messaging'][0].get("postback") and data['entry'][0]['messaging'][0]['postback'].get("payload"):
            inputMsg = data['entry'][0]['messaging'][0]['postback']['payload']
        else:
            return "ignored"

        if not is_ascii(inputMsg):
            message = {u'text': u'I am having a hard time trying to understand you \U0001f635'}
            messenger_utils.reply(sender, message)
            messenger_utils.reply(sender, messenger_utils.welcome())
            return "ignored"

        if inputMsg.lower() in GREETINGS:
            messenger_utils.reply(sender, messenger_utils.greet())
            messenger_utils.reply(sender, messenger_utils.welcome())
            return "ok"        
        
        input_words = inputMsg.lower().split(' ')
        if small_talk(input_words, sender):
            return "ok"
        
        if 'in' in input_words:
            index = len(input_words) - input_words[::-1].index('in')
            name = ' '.join(input_words[:index-1])
            township = ' '.join(input_words[index:])
        else:
            queries = inputMsg.split(',')
            name = preprocess(queries[0])
            township = preprocess(queries[1] if len(queries) >= 2 else '')

        if len(name) == 0:
            messenger_utils.reply(sender, {"text" : "I'm sorry. I don't understand."})
            messenger_utils.reply(sender, messenger_utils.welcome())
            return "empty input"

        business_list = sqlMethods.get_all_businesses(NAME=name, TOWNSHIP=township)
        if business_list:
            message = messenger_utils.getSearchResults(business_list)
            messenger_utils.reply(sender, message)
        #information.noResults
        else:
            message = {"text": "I cannot find " + name + ". Try again?"}
            if len(township):
               message = {"text": "I cannot find " + name + " in " + township + ". Try again?"}
            messenger_utils.reply(sender, message)
        return "ok"
    except Exception as e:
        print "Unhandled Exception:"
        print e
        del SESSION[sender]
        messenger_utils.reply(sender, {"text" : "I'm sorry. I don't understand."})
        messenger_utils.reply(sender, messenger_utils.welcome())
        return "ok"

"""
Clear inactive sessions using a scheduler
"""
def doMaintenance(frequency):
    global SESSION
    expired = time.time() - frequency

    for user_id, context in SESSION.items():
        if context["lastActive"] < expired:
            del SESSION[user_id]

class SessionManagerThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        frequency = 60 * 30 #30 minutes
        while not self.stopped.wait(frequency):
            doMaintenance(frequency)

session_manager_thread = SessionManagerThread(Event())
session_manager_thread.daemon = True
session_manager_thread.start()

if __name__ == '__main__':
    app.run(debug=True)

