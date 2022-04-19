# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from html import entities
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import sqlite3
import os
import datetime

def get_product_info(tracker):
    ents = tracker.latest_message['entities']

    category = None
    brand = None
    price = None
    gender = None
    color = None
    size = None

    for ent in ents:
        entity = ent['entity']
        if entity == 'product':
            category = ent['value']
        if entity == 'brand':
            brand = ent['value']
        if entity == 'price':
            price = ent['value']
        if entity == 'gender':
            gender = ent['value']
        if entity == 'color':
            color = ent['value']
        if entity == 'size':
            size = ent['value']
    
    return category, brand, price, gender, color, size

class Connection(Action):

    def __init__(self) -> None:
        super(Connection, self).__init__()
        self.conn = self.create_connection("db/database.db")
    
    def name(self) -> Text:
        return "db_connection"
    
    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Exception as e:
            print(e)

        return conn

class Reset_info_product(Action):

    def __init__(self) -> None:
        super(Reset_info_product, self).__init__()
    
    def name(self) -> Text:
        return "reset_info_product"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        return [
            # SlotSet("product_to_buy", None), cannot reset this slot
            SlotSet("brand_to_buy", None),
            SlotSet("price_to_buy", None),
            SlotSet("gender_to_buy", None),
            SlotSet("color_to_buy", None),
            SlotSet("size_to_buy", None),
            SlotSet("number_to_buy", None),
            SlotSet("quantity_to_buy", None),
            SlotSet("product_to_buy_name", None),
            SlotSet("color_available_slot", None),
            SlotSet("size_available_slot", None),
            SlotSet("color_exist", None),
            SlotSet("size_exist", None),
            SlotSet("color_check", None),
            SlotSet("size_check", None),
            SlotSet("product_exist", None)
        ]

class Reset_info_product_no_color(Action):

    def __init__(self) -> None:
        super(Reset_info_product_no_color, self).__init__()
    
    def name(self) -> Text:
        return "reset_info_product_no_color"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        return [
            # SlotSet("product_to_buy", None), cannot reset this slot
            SlotSet("brand_to_buy", None),
            SlotSet("price_to_buy", None),
            SlotSet("gender_to_buy", None),
            SlotSet("size_to_buy", None),
            SlotSet("number_to_buy", None),
            SlotSet("quantity_to_buy", None),
            SlotSet("product_to_buy_name", None),
            SlotSet("color_available_slot", None),
            SlotSet("size_available_slot", None),
            SlotSet("color_exist", None),
            SlotSet("size_exist", None),
            SlotSet("color_check", None),
            SlotSet("size_check", None),
            SlotSet("product_exist", None)
        ]

class Reset_info_product_no_size(Action):

    def __init__(self) -> None:
        super(Reset_info_product_no_size, self).__init__()
    
    def name(self) -> Text:
        return "reset_info_product_no_size"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        return [
            # SlotSet("product_to_buy", None), cannot reset this slot
            SlotSet("brand_to_buy", None),
            SlotSet("price_to_buy", None),
            SlotSet("gender_to_buy", None),
            SlotSet("color_to_buy", None),
            SlotSet("number_to_buy", None),
            SlotSet("quantity_to_buy", None),
            SlotSet("product_to_buy_name", None),
            SlotSet("color_available_slot", None),
            SlotSet("size_available_slot", None),
            SlotSet("color_exist", None),
            SlotSet("size_exist", None),
            SlotSet("color_check", None),
            SlotSet("size_check", None),
            SlotSet("product_exist", None)
        ]

class Reset_info_product_no_color_no_size(Action):

    def __init__(self) -> None:
        super(Reset_info_product_no_color_no_size, self).__init__()
    
    def name(self) -> Text:
        return "reset_info_product_no_color_no_size"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        return [
            # SlotSet("product_to_buy", None), cannot reset this slot
            SlotSet("brand_to_buy", None),
            SlotSet("price_to_buy", None),
            SlotSet("gender_to_buy", None),
            SlotSet("number_to_buy", None),
            SlotSet("quantity_to_buy", None),
            SlotSet("product_to_buy_name", None),
            SlotSet("color_available_slot", None),
            SlotSet("size_available_slot", None),
            SlotSet("color_exist", None),
            SlotSet("size_exist", None),
            SlotSet("color_check", None),
            SlotSet("size_check", None),
            SlotSet("product_exist", None)
        ]

class Retrieve_product(Action):

    def __init__(self) -> None:
        super(Retrieve_product , self).__init__()
        self.conn = Connection().conn
    
    def name(self) -> Text:
        return "db_retrieve_product"

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, 
        domain: "DomainDict") -> List[Dict[Text, Any]]:

        category, brand, price, gender, color, size = get_product_info(tracker)

        cur = self.conn.cursor()

        query = "SELECT * FROM product WHERE category=?"

        params = (category,)

        if(brand != None):
            query += " AND brand LIKE ?"
            params += (brand,)
        
        if(price != None):
            query += " AND price LIKE ?"
            params += (price,)
        
        if(gender != None):
            query += " AND gender LIKE ?"
            params += (gender,)
        
        if(size != None):
            query += " AND sizes LIKE ?"
            params += ("%" + size + "%",)

        if(color != None):
            query += " AND colors LIKE ?"
            params += ("%" + color + "%",)

        cur.execute(query, params)
        
        rows = cur.fetchall()
        products = []

        ordinal_num = {
            1: "first",
            2: "second",
            3: "third",
            4: "fourth",
            5: "fifth"
        }
        response = []
        for i, product in enumerate(rows):
            if(i == 5):
                break
            if(product[5] != None):
                color_p = product[5].replace(" ", "").split(";")
                image_name = product[8].replace("*", color_p[0])
                image = os.path.join("db", "images", image_name) # could be the image + color does not exist -> to check
            else:
                image = os.path.join("db", "images", product[8])
            
            title = product[1]
            gender_p = product[2]
            price_p = product[3]
            size_p = product[4]
            color_p = product[5]
            description = product[6]
            category = product[7]

            subtitle = "Sizes: " + str(size_p) + "\n Colors: " + str(color_p) + "\n Price: " + "$" + str(price_p)

            payload = "The " + ordinal_num[i + 1] + " one"

            # products.append(
            #     {
            #         "title": title,
            #         "subtitle": subtitle,
            #         "image_url": image,
            #         "buttons": [ {
            #                 "title": "Buy",
            #                 "type": "postback",
            #                 "payload": payload
            #             }
            #         ]
            #     }
            # )
            response.append(
                {
                    "name": product[1],
                    "gender": product[2],
                    "price": product[3],
                    "size": product[4],
                    "color": product[5],
                    "description": product[6],
                    "category": product[7],
                    "image": image
                }
            )
        
        # carousel = {
        #     "type": "template",
        #     "payload": {
        #         "template_type": "generic",
        #         "elements": products
        #     }
        # }
        
        if(len(rows) != 0):
            dispatcher.utter_message(
                response = "utter_visualize_product",
                products = response
            )
            # dispatcher.utter_message(
            #     attachment=carousel
            # )
            dispatcher.utter_message(
                response = "utter_buy_something"
            )
            return [SlotSet("product_exist", True),
                    SlotSet("product_to_buy", category),
                    SlotSet("brand_to_buy", brand),
                    SlotSet("price_to_buy", price),
                    SlotSet("gender_to_buy", gender),
                    SlotSet("color_to_buy", color),
                    SlotSet("size_to_buy", size)]
        else:
            if(len(params) > 1):
                dispatcher.utter_message(
                    response = "utter_no_specified_product"
                )
            else:
                dispatcher.utter_message(
                    response = "utter_no_product"
                )
            return [SlotSet("product_exist", False)]

class Set_product_info(Action):

    def __init__(self) -> None:
        super(Set_product_info, self).__init__()
        self.conn = Connection().conn

    def name(self) -> Text:
        return "set_product_info"

    def ordinals(self) -> Dict:
        return {
            "first": 1,
            "second": 2,
            "third": 3,
            "fourth": 4,
            "fifth": 5,
            "sixth": 6,
            "seventh": 7,
            "eighth": 8
        }
    
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker,
        domain: "DomainDict") -> List[Dict[Text, Any]]:
        
        entities = tracker.latest_message['entities']

        product_number_list = None
        for ent in entities:
            if ent['entity'] == 'number_on_the_list':
                product_number_list = ent['value']
                break

        product_number_list = self.ordinals()[product_number_list]

        category = tracker.get_slot("product_to_buy")
        brand = tracker.get_slot("brand_to_buy")
        price = tracker.get_slot("price_to_buy")
        gender = tracker.get_slot("gender_to_buy")
        color = tracker.get_slot("color_to_buy")
        size = tracker.get_slot("size_to_buy")

        cur = self.conn.cursor()

        query = "SELECT * FROM product WHERE category=?"

        params = (category,)

        if(brand != None):
            query += " AND brand LIKE ?"
            params += (brand,)
        
        if(price != None):
            query += " AND price LIKE ?"
            params += (price,)
        
        if(gender != None):
            query += " AND gender LIKE ?"
            params += (gender,)
        
        if(size != None):
            query += " AND sizes LIKE ?"
            params += ("%" + size + "%",)

        if(color != None):
            query += " AND colors LIKE ?"
            params += ("%" + color + "%",)

        cur.execute(query, params)
        rows = cur.fetchall()
        try:
            product_name = rows[product_number_list-1][1]
            if(rows[product_number_list-1][5] != None):
                colors = rows[product_number_list-1][5]
                colors = colors.replace(" ", "").split(";")
                colors = ", ".join(colors)
                color_available = True
            else: 
                colors = None
                color_available = False
            if(rows[product_number_list-1][4] != None):
                sizes = rows[product_number_list-1][4]
                sizes = sizes.replace(" ", "").split(";")
                sizes = ", ".join(sizes)
                size_available = True
            else:
                sizes = None
                size_available = False
            return [
                SlotSet("product_to_buy_name", product_name),
                SlotSet("out_range", False),
                SlotSet("color_available_slot", colors),
                SlotSet("size_available_slot", sizes),
                SlotSet("color_exist", color_available),
                SlotSet("size_exist", size_available)                
            ]
        except:
            dispatcher.utter_message(
                response = "utter_selection_out_range"
            )
            return [
                SlotSet("product_to_buy_name", None),
                SlotSet("out_range", True),
                SlotSet("color_available_slot", None),
                SlotSet("size_available_slot", None),
                SlotSet("color_exist", None),
                SlotSet("size_exist", None)
            ]

class Check_size(Action):
    def __init__(self) -> None:
        super(Check_size, self).__init__()
    
    def name(self) -> Text:
        return "check_size"
    
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker,
        domain: "DomainDict") -> List[Dict[Text, Any]]:

        size_selected = None
        entities = tracker.latest_message['entities']
        for ent in entities:
            if ent['entity'] == 'size':
                try:
                    size_selected = int(ent['value'])
                except:
                    size_selected = str(ent['value']).upper()
                break
        
        size_available = tracker.get_slot("size_available_slot")
        if(size_available == None):
            dispatcher.utter_message(
                response = "utter_no_size_available"
            )
            return []
        if(str(size_selected) in size_available.split(", ")):
            return [
                SlotSet("size_to_buy", size_selected),
                SlotSet("size_check", True)
            ]
        else:
            dispatcher.utter_message(
                response = "utter_size_not_available",
                sizes = size_available
            )
            return [
                SlotSet("size_check", False),
                SlotSet("size_to_buy", None)
            ]

class Check_color(Action):
    def __init__(self) -> None:
        super(Check_color, self).__init__()
    
    def name(self) -> Text:
        return "check_color"
    
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker,
        domain: "DomainDict") -> List[Dict[Text, Any]]:

        color_selected = None
        entities = tracker.latest_message['entities']
        for ent in entities:
            if ent['entity'] == 'color':
                color_selected = ent['value']
                break
        
        color_available = tracker.get_slot("color_available_slot")
        if(color_available == None):
            dispatcher.utter_message(
                response = "utter_no_color_available"
            )
            return []
        if(color_selected in color_available.split(", ")):
            return [
                SlotSet("color_to_buy", color_selected),
                SlotSet("color_check", True)
            ]
        else:
            dispatcher.utter_message(
                response = "utter_color_not_available",
                colors = color_available
            )
            return [
                SlotSet("color_check", False),
                SlotSet("color_to_buy", None)
            ]

class Set_quantity_slot(Action):

    def __init__(self) -> None:
        super(Set_quantity_slot, self).__init__()
        self.conn = Connection().conn
    
    def name(self) -> Text:
        return "set_quantity_slot"
    
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker,
        domain: "DomainDict") -> List[Dict[Text, Any]]:
        
        quantity = None
        entities = tracker.latest_message['entities']
        for ent in entities:
            if ent['entity'] == 'quantity':
                quantity = ent['value']
                break

        return [SlotSet("quantity_to_buy", quantity)]

class Buy_product(Action):

    def __init__(self) -> None:
        super(Buy_product, self).__init__()
        self.conn = Connection().conn
    
    def name(self) -> Text:
        return "db_buy_product"
    
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker,
        domain: "DomainDict") -> List[Dict[Text, Any]]:
        
        quantity = tracker.get_slot("quantity_to_buy")
        color = tracker.get_slot("color_to_buy")
        size = tracker.get_slot("size_to_buy")
        if(size != None):
            size = size.upper()
        name = tracker.get_slot("product_to_buy_name")

        if(name == None):
            dispatcher.utter_message(
                response = "utter_fail_buy"
            )
        else:
            cur = self.conn.cursor()

            product_id_query = "SELECT ID FROM product WHERE name = ?"
        
            cur.execute(product_id_query, (name,))
            rows = cur.fetchall()
            product_id = rows[0][0]
            
            ID = tracker.get_slot("ID_logged")

            if(ID == None):
                print("ID is None")
                dispatcher.utter_message(
                    response = "utter_pleaseLogin"
                )
                return []

            query = "SELECT Address from account where ID = ?"

            cur.execute(query, (ID,))
            rows = cur.fetchall()
            address = rows[0][0]

            query = "INSERT INTO purchase (quantity, size, color, 'shipping address', date, 'product ID', 'account ID') VALUES (?, ?, ?, ?, ?, ?, ?)"

            today = str(datetime.date.today())


            params = (int(quantity), size, color, address, today, product_id, ID)
            
            try:
                cur.execute(query, params)
                rows = cur.fetchall()
                self.conn.commit()
                dispatcher.utter_message(
                    response = "utter_success_buy"
                )

                dispatcher.utter_message(
                    response = "utter_anything_else"
                )
            except Exception as e:
                print(e)
                dispatcher.utter_message(
                    response = "utter_fail_buy"
                )
            
            return [
                SlotSet("product_to_buy", None), 
                SlotSet("brand_to_buy", None),
                SlotSet("price_to_buy", None),
                SlotSet("gender_to_buy", None),
                SlotSet("color_to_buy", None),
                SlotSet("size_to_buy", None),
                SlotSet("number_to_buy", None),
                SlotSet("quantity_to_buy", None),
                SlotSet("product_to_buy_name", None),
                SlotSet("color_available_slot", None),
                SlotSet("size_available_slot", None),
                SlotSet("color_exist", None),
                SlotSet("size_exist", None),
                SlotSet("color_check", None),
                SlotSet("size_check", None),
                SlotSet("product_exist", None)
            ]

class Visualize_cart(Action):
    def __init__(self) -> None:
        super(Visualize_cart, self).__init__()
        self.conn = Connection().conn
    
    def name(self) -> Text:
        return "db_visualize_cart"
    
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker,
        domain: "DomainDict") -> List[Dict[Text, Any]]:
        
        cur = self.conn.cursor()

        query = "SELECT * FROM cart JOIN product ON cart.Product_id = product.id JOIN brand ON product.Brand = brand.ID"
    
        cur.execute(query)
        rows = cur.fetchall()

        if(len(rows) == 0):
            dispatcher.utter_message(
                response = "utter_cart_empty"
            )
        else:
            response = []
            for product in rows:
                quantity = product[1]
                size = product[2]
                color = product[3]
                product_name = product[7]
                gender = product[8]
                price = product[9]
                brand = product[17]
                image = product[14]

                response.append(
                    {
                        "name": product_name,
                        "gender": gender,
                        "price": price,
                        "quantity": quantity,
                        "size": size,
                        "color": color,
                        "brand": brand,
                        "image": image
                    }
                )
            
            dispatcher.utter_message(
                response = "utter_cart_visualize",
                products = response
            )
            dispatcher.utter_message(
                response = "utter_change_cart"
            )

class Delete_cart(Action):
    def __init__(self) -> None:
        super(Delete_cart, self).__init__()
        self.conn = Connection().conn
    
    def name(self) -> Text:
        return "db_delete_cart"

    def ordinals(self) -> Dict:
        return {
            "first": 1,
            "second": 2,
            "third": 3,
            "fourth": 4,
            "fifth": 5,
            "sixth": 6,
            "seventh": 7,
            "eighth": 8
        }
    
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker,
        domain: "DomainDict") -> List[Dict[Text, Any]]:
        
        cur = self.conn.cursor()

        n_delete = None
        entities = tracker.latest_message['entities']
        for ent in entities:
            if ent['entity'] == 'number_on_the_list':
                n_delete = self.ordinals()[ent['value']]
                break

        query = "SELECT * FROM cart"

        cur.execute(query)
        cart_objects = cur.fetchall()
        if(n_delete > len(cart_objects)):
            dispatcher.utter_message(
                response = "utter_cart_empty"
            )
        else:
            print(cart_objects[n_delete-1])
            id_to_delete = cart_objects[n_delete-1][0]

            query = "DELETE FROM cart WHERE ID = ?"
        
            try:
                cur.execute(query, (id_to_delete,))
                rows = cur.fetchall()
                self.conn.commit()

                dispatcher.utter_message(
                    response = "utter_cart_deleted"
                )            
            except Exception as e:
                print(e)
                dispatcher.utter_message(
                    response = "utter_fail_delete"
                )

class UpdateUserFirstName(Action):

    def __init__(self) -> None:
        super(UpdateUserFirstName, self).__init__()
        self.conn = Connection().conn

    def name (self) -> Text:
        return "action_updateUserFirstName"
    
    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        cur = self.conn.cursor()
        #link = sqlite3.connect("database.db")
        #linkCursor = link.cursor()
        
        slot_firstName = tracker.get_slot("PERSON")
        slot_emailAddress = tracker.get_slot("email")
        
        stmt = "UPDATE account SET Name = ? WHERE Email = ?"
        cur.execute(stmt, (slot_firstName, slot_emailAddress, ))
        self.conn.commit()
        
        resultDisplayed = "First name changed"

        dispatcher.utter_message(text=resultDisplayed)

        return [SlotSet("PERSON", None)]


# class UpdateUserSurname(Action):

#     def __init__(self) -> None:
#         super(UpdateUserSurname, self).__init__()
#         self.conn = Connection().conn

#     def name (self) -> Text:
#         return "action_updateUserSurname"
    
#     def run(self,
#             dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         cur = self.conn.cursor()
#         #link = sqlite3.connect("database.db")
#         #linkCursor = link.cursor()
        
#         slot_Surname = tracker.get_slot("surname_PERSON")
#         slot_emailAddress = tracker.get_slot("email")
        
#         stmt = "UPDATE account SET Surname = ? WHERE Email = ?" 
#         print(stmt, (slot_Surname, slot_emailAddress))
#         cur.execute(stmt)

        # print("action_updateUserSurname")
        
        # resultDisplayed = "Surname changed"

        # dispatcher.utter_message(text=resultDisplayed)

        # return [SlotSet("surname_PERSON", None)]

class UpdateUserBirthDate(Action):

    def __init__(self) -> None:
        super(UpdateUserBirthDate, self).__init__()
        self.conn = Connection().conn

    def name (self) -> Text:
        return "action_updateUserBirthDate"
    
    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        cur = self.conn.cursor()
        #link = sqlite3.connect("database.db")
        #linkCursor = link.cursor()
        
        slot_BirthDate = tracker.get_slot("time")
        slot_emailAddress = tracker.get_slot("email")
        stmt = "UPDATE account SET Birthdate = ? WHERE Email = ?"
        cur.execute(stmt, (slot_BirthDate[:10], slot_emailAddress, ))
        self.conn.commit()
        
        resultDisplayed = "Birth date changed"

        dispatcher.utter_message(text=resultDisplayed)

        return [SlotSet("time", None)]

class UpdateUserAddress(Action):

    def __init__(self) -> None:
        super(UpdateUserAddress, self).__init__()
        self.conn = Connection().conn

    def name (self) -> Text:
        return "action_updateUserAddress"
    
    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        cur = self.conn.cursor()
        #link = sqlite3.connect("database.db")
        #linkCursor = link.cursor()
        
        slot_emailAddress = tracker.get_slot("email")
        slot_street = tracker.get_slot("STREET")
        slot_zipCode = tracker.get_slot("ZIP_CODE")
        slot_city = tracker.get_slot("CITY")
        slot_country = tracker.get_slot("COUNTRY")
        slot_state = tracker.get_slot("STATE")

        slot_address = ''
        if slot_street != None:
            slot_address = slot_address + slot_street
        if slot_zipCode != None and slot_address != '':
            slot_address = slot_address + ' ' + str(slot_zipCode)
        elif slot_zipCode != None and slot_address == '':
            slot_address = slot_address + str(slot_zipCode)
        if slot_city != None and slot_address != '':
            slot_address = slot_address + ' ' + slot_city
        elif slot_city != None and slot_address == '':
            slot_address = slot_address + slot_city
        if slot_state != None and slot_address != '':
            slot_address = slot_address + ' ' + slot_state
        elif slot_state != None and slot_address == '':
            slot_address = slot_address + slot_state
        if slot_country != None and slot_address != '':
            slot_address = slot_address + ' ' + slot_country
        elif slot_country != None and slot_address == '':
            slot_address = slot_address + slot_country
        

        stmt = "UPDATE account SET Address = ? WHERE Email = ?"
        cur.execute(stmt, (slot_address, slot_emailAddress, ))
        self.conn.commit()
        
        resultDisplayed = "Address changed"

        dispatcher.utter_message(text=resultDisplayed)

        return [SlotSet("address", None)]


class CheckIfUserIsRegistered(Action):

    def __init__(self) -> None:
        super(CheckIfUserIsRegistered, self).__init__()
        self.conn = Connection().conn

    def name(self) -> Text:
        return "action_checkIfUserIsRegistered"
    
    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        cur = self.conn.cursor()
        #link = sqlite3.connect("database.db")
        #linkCursor = link.cursor()
        
        slot_emailAddress = tracker.get_slot("email")
        stmt = "SELECT ID, email FROM account WHERE email = ?" 
        cur.execute(stmt, (slot_emailAddress, ))
        result = cur.fetchone()
        print("action_checkifuserisregistered")
        #print(result)
        #print(slot_emailAddress)

        if result != None:
            ID = result[0]
            return [SlotSet("userIsRegistered", True), SlotSet("ID_logged", ID)]
        else:            
            return [SlotSet("userIsRegistered", False), SlotSet("ID_logged", None)]

class CreatenNewAccount(Action):

    def __init__(self) -> None:
        super(CreatenNewAccount, self).__init__()
        self.conn = Connection().conn

    def name(self) -> Text:
        return "action_createNewAccount"
    
    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        cur = self.conn.cursor()
        #link = sqlite3.connect("database.db")
        #linkCursor = link.cursor()
        
        slot_emailAddress = tracker.get_slot("email")
        slot_firstName = tracker.get_slot("PERSON")
        # slot_surname = tracker.get_slot("surname_PERSON")
        slot_birthDate = tracker.get_slot("time")
        birth_date = slot_birthDate[:10]
        slot_street = tracker.get_slot("STREET")
        slot_zipCode = tracker.get_slot("ZIP_CODE")
        slot_city = tracker.get_slot("CITY")
        slot_country = tracker.get_slot("COUNTRY")
        slot_state = tracker.get_slot("STATE")

        slot_address = ''
        if slot_street != None:
            slot_address = slot_address + slot_street
        if slot_zipCode != None and slot_address != '':
            slot_address = slot_address + ' ' + str(slot_zipCode)
        elif slot_zipCode != None and slot_address == '':
            slot_address = slot_address + str(slot_zipCode)
        if slot_city != None and slot_address != '':
            slot_address = slot_address + ' ' + slot_city
        elif slot_city != None and slot_address == '':
            slot_address = slot_address + slot_city
        if slot_state != None and slot_address != '':
            slot_address = slot_address + ' ' + slot_state
        elif slot_state != None and slot_address == '':
            slot_address = slot_address + slot_state
        if slot_country != None and slot_address != '':
            slot_address = slot_address + ' ' + slot_country
        elif slot_country != None and slot_address == '':
            slot_address = slot_address + slot_country
        
        # need to know the number of rows in order to add the next ID in the table
        stmt = "SELECT email FROM account"
        cur.execute(stmt)
        result = cur.fetchall()
        id = len(result) + 1


        stmt1 = "INSERT INTO account VALUES (?, ?, ?, ?, ?)" 
        cur.execute(stmt1, (id, slot_firstName, birth_date, slot_emailAddress, slot_address, ))
        print("action_createNewAccount")

        resultDisplayed = "User correctly registered"
        dispatcher.utter_message(text=resultDisplayed)
            
        return [SlotSet("PERSON", None), 
                #SlotSet("surname_PERSON", None), 
                SlotSet("time", None),
                SlotSet("address", None),
                SlotSet("STREET", None), 
                SlotSet("ZIP_CODE", None), 
                SlotSet("CITY", None),
                SlotSet("CITY", None),
                SlotSet("COUNTRY", None)]

class RetrieveFirstName(Action):

    def __init__(self) -> None:
        super(RetrieveFirstName, self).__init__()
        self.conn = Connection().conn

    def name(self) -> Text:
        return "action_retrieveFirstName"
    
    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        cur = self.conn.cursor()
        #link = sqlite3.connect("database.db")
        #linkCursor = link.cursor()
        
        slot_emailAddress = tracker.get_slot("email")
        # need to know the number of rows in order to add the next ID in the table
        stmt = "SELECT Name FROM account WHERE Email = ?"
        cur.execute(stmt, (slot_emailAddress, ))
        result = cur.fetchone()

        resultDisplayed = "The first name for your account is: " + result[0]

        dispatcher.utter_message(text=resultDisplayed)
        
        print("action_retrieveFirstName")

# class RetrieveSurname(Action):

#     def __init__(self) -> None:
#         super(RetrieveSurname, self).__init__()
#         self.conn = Connection().conn

#     def name(self) -> Text:
#         return "action_retrieveSurname"
    
#     def run(self,
#             dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         cur = self.conn.cursor()
#         #link = sqlite3.connect("database.db")
#         #linkCursor = link.cursor()
        
#         slot_emailAddress = tracker.get_slot("email")

#         # need to know the number of rows in order to add the next ID in the table
#         stmt = "SELECT Surname FROM account WHERE Email = ?"
#         cur.execute(stmt, (slot_emailAddress, ))
#         result = cur.fetchone()

#         resultDisplayed = "The surname for your account is: " + result[0]

#         dispatcher.utter_message(text=resultDisplayed)
        
#         print("action_retrieveSurname")

class RetrieveBirthDate(Action):

    def __init__(self) -> None:
        super(RetrieveBirthDate, self).__init__()
        self.conn = Connection().conn

    def name(self) -> Text:
        return "action_retrieveBirthDate"
    
    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        cur = self.conn.cursor()
        #link = sqlite3.connect("database.db")
        #linkCursor = link.cursor()
        
        slot_emailAddress = tracker.get_slot("email")

        # need to know the number of rows in order to add the next ID in the table
        stmt = "SELECT Birthdate FROM account WHERE Email = ?"
        cur.execute(stmt, (slot_emailAddress, ))
        result = cur.fetchone()

        resultDisplayed = "The birth date for your account is: " + result[0]

        dispatcher.utter_message(text=resultDisplayed)
        
        print("action_retrieveBirthDate")

class RetrieveAddress(Action):

    def __init__(self) -> None:
        super(RetrieveAddress, self).__init__()
        self.conn = Connection().conn

    def name(self) -> Text:
        return "action_retrieveAddress"
    
    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        cur = self.conn.cursor()
        #link = sqlite3.connect("database.db")
        #linkCursor = link.cursor()
        
        slot_emailAddress = tracker.get_slot("email")

        # need to know the number of rows in order to add the next ID in the table
        stmt = "SELECT Address FROM account WHERE Email = ?"
        cur.execute(stmt, (slot_emailAddress, ))
        result = cur.fetchone()

        resultDisplayed = "The address for your account is: " + result[0]

        dispatcher.utter_message(text=resultDisplayed)
        
        print("action_retrieveAddress")

# class EmptySlots(Action):

#     def __init__(self) -> None:
#         super(EmptySlots, self).__init__()
#         self.conn = Connection().conn

#     def name(self) -> Text:
#         return "action_emptySlots"
    
#     def run(self,
#             dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
#             slot_emailAddress = tracker.get_slot("email")
#             slot_firstName = tracker.get_slot("PERSON")
#             slot_surname = tracker.get_slot("surname")
#             slot_birthDate = tracker.get_slot("time")

#             print(slot_emailAddress)
#             print(slot_firstName)
#             print(slot_surname)
#             print(slot_birthDate)

#             print("action_emptySlots")

#             resultDisplayed = "User correctly registered"
#             dispatcher.utter_message(text=resultDisplayed)
            
#             return [SlotSet("email", None)], [SlotSet("PERSON", None)], [SlotSet("surname", None)], [SlotSet("time", None)]

class SetSlot_askAccountInfo(Action):

    def __init__(self) -> None:
        super(SetSlot_askAccountInfo, self).__init__()
        self.conn = Connection().conn

    def name(self) -> Text:
        return "action_SetSlot_askAccountInfo"
    
    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print("action_SetSlot_askAccountInfo")

        return [SlotSet("askAccountInfo", "askAccountInfo_path")]

class action_whichInfoAsked_true(Action):

    def __init__(self) -> None:
        super(action_whichInfoAsked_true, self).__init__()
        self.conn = Connection().conn

    def name(self) -> Text:
        return "action_whichInfoAsked"
    
    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
            print("action_whichInfoAsked")

            resultDisplayed = "Which info do you want to know?"
            dispatcher.utter_message(text=resultDisplayed)

            return [SlotSet("accountInfoAsked", True)]



class action_userGaveAddress(Action):

    def __init__(self) -> None:
        super(action_userGaveAddress, self).__init__()
        self.conn = Connection().conn

    def name(self) -> Text:
        return "action_userGaveAddress"
    
    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
            print("action_userGaveAddress")

            cur = self.conn.cursor()
        
        
            slot_street = tracker.get_slot("STREET")
            slot_zipCode = tracker.get_slot("ZIP_CODE")
            slot_city = tracker.get_slot("CITY")
            slot_country = tracker.get_slot("COUNTRY")
            slot_state = tracker.get_slot("STATE")

            print(slot_street, slot_zipCode, slot_city, slot_country, slot_state)

            