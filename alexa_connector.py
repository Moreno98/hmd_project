import logging
import json
from sanic import Blueprint, response
from sanic.request import Request
from typing import Text, Optional, List, Dict, Any
import random
from random import randrange

from rasa.core.channels.channel import UserMessage, OutputChannel
from rasa.core.channels.channel import InputChannel
from rasa.core.channels.channel import CollectingOutputChannel

logger = logging.getLogger(__name__)

class AlexaConnector(InputChannel):
    """A custom http input channel for Alexa.
    You can find more information on custom connectors in the 
    Rasa docs: https://rasa.com/docs/rasa/user-guide/connectors/custom-connectors/
    """

    @classmethod
    def name(cls):
        return "alexa_assistant"

    # Sanic blueprint for handling input. The on_new_message
    # function pass the received message to Rasa Core
    # after you have parsed it
    def blueprint(self, on_new_message):
        alexa_webhook = Blueprint("alexa_webhook", __name__)

        # required route: use to check if connector is live
        @alexa_webhook.route("/", methods=["GET"])
        async def health(request):
            return response.json({"status": "ok"})

        # required route: defines
        @alexa_webhook.route("/webhook", methods=["POST"])
        async def receive(request):
            # get the json request sent by Alexa
            payload = request.json
            # check to see if the user is trying
            # to launch the skill
            intenttype = payload["request"]["type"]
            session_object = payload.get("session")
            session_id = session_object.get('sessionId')
            user_id = session_object.get('user',{}).get("userId")
            sender_id = user_id + session_id

            print("intenttype: ", intenttype)

            if(intenttype == "SessionEndedRequest"):
                return response.json({"status": "ok"})

            # if the user is starting the skill, let them
            # know it worked & what to do next
            if intenttype == "LaunchRequest":
                message = "Hello! Welcome to the e-commerce assistant. Please ask me something."
                session = "false"
                r = {
                    "version": "1.0",
                    "response": {
                        "outputSpeech": {
                            "type": "PlainText",
                            "text": message
                        },
                        "reprompt": {
                            "outputSpeech": {
                                "type": "PlainText",
                                "text": message,
                                "playBehavior": "REPLACE_ENQUEUED",
                            }
                        },
                        "card": {
                            "type": "Standard",
                            "title": "Hello! Welcome to the e-commerce assistant.",
                            "text": "Please ask me something.",
                            "image": {
                                "smallImageUrl": "https://acquire.io/wp-content/uploads/2022/01/79546_Acquire_BlogImages-01_SS.jpg",
                                "largeImageUrl": "https://acquire.io/wp-content/uploads/2022/01/79546_Acquire_BlogImages-01_SS.jpg"
                            }
                        },
                        "shouldEndSession": "false"
                    }
                }
                return response.json(r)
            else:
                # get the Alexa-detected intent
                intent = payload["request"].get("intent", {}).get("name", "")

                # makes sure the user isn't trying to
                # end the skill
                if intent == "AMAZON.StopIntent":
                    session = "true"
                    message = "Talk to you later"
                else:
                    # get the user-provided text from
                    # the slot named "text"
                    text = payload["request"].get("intent", {}).get("slots",{}).get("text",{}).get("value","")

                    # initialize output channel
                    out = CollectingOutputChannel()

                    # send the user message to Rasa &
                    # wait for the response
                    await on_new_message(UserMessage(text, out,sender_id=sender_id))
                    # extract the text from Rasa's response
                    ith = 0
                    if("text" in out.messages[0]):
                        ith = 1
                    if('amzn' in out.messages[0]['recipient_id'] and ("attachment" in out.messages[0] or ("text" in out.messages[0] and "Available colors:" in out.messages[0]['text']))):
                        products = out.messages[ith]["attachment"]['payload']['elements']
                        mode = out.messages[ith]["attachment"]['payload']['mode']
                        if(mode == "details"):
                            title = "These are the details"
                            hint_text = "Do you want to buy it?"
                        elif(mode == "retrieve_product"):
                            title = "These are the products I found"
                            hint_text = "You can select a product by saying 'the first'"
                        elif(mode == "visualize_cart"):
                            title = "These are the products in your cart"
                            hint_text = "You can delete a product by saying 'delete the first'"
                        elif(mode == "visualize_purchases"):
                            title = "These are your purchases" 
                            hint_text = ""
                        message = out.messages[int(not ith)]['text']
                        list_item_to_show = []
                        for element in products:
                            random_rating = random.uniform(0, 5)
                            ratings = randrange(500)
                            list_item_to_show.append(
                                {
                                    "primaryText": element["title"],
                                    "secondaryText": element["subtitle"],
                                    "imageSource": element["image_url"],
                                    "imageShowProgressBar": True,
                                    "ratingSlotMode": "multiple",
                                    "ratingNumber": random_rating,
                                    "ratingText": f"({ratings} ratings)"
                                }
                            )
                        r = {
                            "version": "1.0",
                            "response": {
                                "outputSpeech": {
                                    "type": "PlainText",
                                    "text": message,
                                    "playBehavior": "REPLACE_ENQUEUED",
                                },
                                "directives": 
                                [
                                    {
                                        "type": "Alexa.Presentation.APL.RenderDocument",
                                        "token": "product_listToken",
                                        "document": {
                                            "src": "doc://alexa/apl/documents/product_list",
                                            "type": "Link"
                                        },
                                        "datasources": {
                                            "imageListData": {
                                                "type": "object",
                                                "objectId": "imageListSample",
                                                "backgroundImage": {
                                                    "sources": [
                                                        {
                                                            "url": "https://www.whoson.com/wp-content/uploads/2020/02/what-is-an-intent-based-chatbot-1024x576.png",
                                                            "size": "large"
                                                        }
                                                    ]
                                                },
                                                "title": title,
                                                "listItems": list_item_to_show,
                                                "logoUrl": "https://media.istockphoto.com/vectors/chat-bot-ai-and-customer-service-support-concept-vector-flat-person-vector-id1221348467?k=20&m=1221348467&s=612x612&w=0&h=hp8h8MuGL7Ay-mxkmIKUsk3RY4O69MuiWjznS_7cCBw=",
                                                "hintText": hint_text
                                            }
                                        }
                                    }
                                ],
                                "shouldEndSession": "false"
                            }
                        }
                        print("RESPONSE:", r)
                        return response.json(r)
                    else:
                        responses = [m["text"] for m in out.messages]
                        if len(responses) >0:
                            message = " ".join(responses)
                        else:
                            message = "Sorry, can you repeat that please?"
                            logger.error("No Response returned from the Assistant")
            r = {
                "version": "1.0",
                "sessionAttributes": {"status": "test"},
                "response": {
                    "outputSpeech": {
                        "type": "PlainText",
                        "text": message,
                        "playBehavior": "REPLACE_ENQUEUED",
                    },
                    "reprompt": {
                        "outputSpeech": {
                            "type": "PlainText",
                            "text": message,
                            "playBehavior": "REPLACE_ENQUEUED",
                        }
                    },
                    "shouldEndSession": "false",
                },
            }
            return response.json(r)

        return alexa_webhook