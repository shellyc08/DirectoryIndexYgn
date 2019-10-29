import requests
import random

ACCESS_TOKEN = "EAAGqnPsZBGFIBAKDNZBusLZAlhQgTBXoLAQRGI2c5fsX0PDIZCxznpqfnCkK0ZCnLOy3d5aFjL4bg4FgTSKvbWnFOsZAafbGROEqScve0eQfj6VPPT1JzkXFbaGZAbZCeyNXmYxKiFYXqZAzIEzOKjlHEdWuBhVz9kn8cK1yZAh9HAagZDZD"
GREETING_RESPONSES = [u"Hi", u"Hello", u"Hey there"]
FLIRT_RESPONSES = [u"I like you too \U0001f609", u"You are a nice person \U0001f607"]
INSULT_RESPONSES = [u"No, I am not. You are. \U0001f620", u"I have feelings too \U0001f641", u"Humans are cruel \U0001f62d"]
THANK_RESPONSES = [u"No problem.", u"Glad to help you.", u"Bye bye."]
CATAGORIES = ["Food", "Automotive", "Transport", "Health", "Beauty", "Education", "Travel", "Entertainment", "Electronics", "Equipment"]

def reply(user_id, msg):
  print msg
  data = {
      "recipient": {"id": user_id},
      "message": msg
  }
  resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)

def confirm():
  return {
    "text":"Did you find what you want?",
    "quick_replies":[
      {
        "content_type":"text",
        "title":"Yes",
        "payload":"yes"
      },
      {
        "content_type":"text",
        "title":"No",
        "payload":"no"
      }
    ]
  }

def greet():
  return {'text' : random.choice(GREETING_RESPONSES)}

def flirt():
  return {'text' : random.choice(FLIRT_RESPONSES)}

def insult():
  return {'text' : random.choice(INSULT_RESPONSES)}

def thank():
  return {'text' : random.choice(THANK_RESPONSES)}

def welcome():
  return {
    "text": u"Let me help you find places in Yangon. Wanna have some cake \U0001f370? Try this!",
    "quick_replies": [
      {
        "content_type":"text",
        "title":"Shwe Pu Zun",
        "payload":"Shwe Pu Zun"
      },
      {
        "content_type":"text",
        "title":"Shwe Pu Zun, Tarmwe",
        "payload":"Shwe Pu Zun, Tarmwe"
      }
    ]
  }

def welcome2():
  return {
    "text":"I can help you find places in Yangon. How can I help you?",
    "quick_replies":[
      {
        "content_type":"text",
        "title":"Find by name",
        "payload":"information"
      },
      {
        "content_type":"text",
        "title":"Find by catalogue",
        "payload":"nearby"
      }
    ]
  }

def getCategories(TEXT = "What do you want to find?"):
  category_json = {
    "text": TEXT,
    "quick_replies":[]
  }

  for category in CATAGORIES:
    category_json.get("quick_replies").append({
      "content_type":"text",
      "title": category,
      "payload": category.lower()
    })
  return category_json

def getSearchResults(results):
  json = {
    "attachment": {
      "type": "template",
      "payload": {
        "template_type": "generic",
        "elements": []
      }
    }
  }
  count = 0
  for result in results:
    count = count + 1
    address = result['street'] + ", " + result['township']
    contacts = []
    for contact in result['contact'].split(","):
      if contact: 
        contacts.append({
          "type": "phone_number", 
          "title" : "Call " + contact, 
          "payload" : contact
        })
      if len(contacts) == 2:
        break
    contacts.append({"type": "element_share"})    
 
    json["attachment"]["payload"]["elements"].append({
      "title": result['businessName'],
      "subtitle": address,
      "buttons": contacts
    })
    # Messenger doesn't allow more than 10 results
    if count >= 10:
      break
  return json
