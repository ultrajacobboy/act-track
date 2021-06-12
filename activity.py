from os.path import abspath, dirname
import json
from datetime import datetime
import time
from pushover import init, Client
import requests
import platform
from colorama import Fore, Back, Style

#get file path
script = dirname(abspath(__file__))

user_os = platform.system()
if user_os == "Windows":
    path = "\\"
else:
    path = "/"

with open(f'{script}{path}activities.json', "r") as f:
        acts = json.load(f)
        f.close()

with open(f'{script}{path}settings.json', "r") as f:
        setting = json.load(f)
        color = getattr(Fore, setting["color"])
        print(color, "act-tracker")
        f.close()

with open(f'{script}{path}config.json', "r") as f:
        config = json.load(f)
        user = config.get("user_key")
        api = config.get("api_key")
        discord_hook = config.get("discord_webhook")
        choose = config.get("push_or_dis")
        f.close()

client = Client(user, api_token=api)

#activity class
class Activity:
    def __init__(self):
        self.acts = acts
        self.path = path
        self.user = user
        self.api = api
        self.client = client
        self.discord_hook = discord_hook
        self.choose = choose

    def get_name(self):
        self.name = input("What is your name?\n> ")
        name_dict = {"name": self.name}
        with open(f'{script}{self.path}name.json', "w", encoding="utf-8") as f:
            json.dump(name_dict, f, ensure_ascii=False, indent=4)

    def check_for_act(self):
        while True:
            its_time = datetime.now().strftime("%H:%M")
            if its_time in self.acts:
                if choose == "push":
                    self.client.send_message(self.acts[its_time], title=self.acts[its_time])
                    time.sleep(30)
                elif choose == "dis":
                    data = {
                        "content" : self.acts[its_time],
                        "username": "acts-tracker"
                    }

                    result = requests.post(self.discord_hook, json=data)
                    time.sleep(30)
                else:
                    print("Trouble in the conf file")
            else:
                time.sleep(30)

    def look_at_json(self):
        with open(f'{script}{self.path}activities.json', "r") as f:
            data = json.load(f)
            f.close()
        self.acts = data

    def add_activity(self):
        new_act = input("Please enter the name of the new activity: ")
        new_time = input("Please enter the time in 24 hour format (hour:minute):")
        try:
            (hour,minute) = new_time.split(":")
            if int(hour) <= 24 and int(hour) >= 0 and int(minute) <= 60 and int(minute) >=0:
                if int(hour) < 10:
                    hour = "0" + hour[-1]
                if int(minute) < 10:
                    minute = "0" + minute[-1]
                act_dict = {f"{hour}:{minute}": new_act}
                with open(f'{script}{self.path}activities.json', "r") as f:
                    data = json.load(f)
                    data.update(act_dict)
                    f.close()
                with open(f'{script}{self.path}activities.json', "w", encoding="utf-8") as asdf:
                    json.dump(data, asdf)
                    asdf.close()
                print(f"OK {new_act} at {new_time}.")
            else:
                print("Invalid. Either hours or minutes is a wack number.")
        except ValueError as e:
            print(e)
            print("Invalid format. It should be hour:minute")
        self.look_at_json()

    def delete_all(self):
        confirm = input("ARE YOU SURE YOU WANT TO DELETE ALL ACTIVITES? Y/N: ")
        if confirm.lower() == "y":
            with open(f'{script}{self.path}activities.json', "w", encoding="utf-8") as f:
                blank = {}
                json.dump(blank, f, ensure_ascii=False, indent=4)
                print("All activities erased.")
                f.close()
        elif confirm.lower() == "n":
            print("Ok. Nothing has been erased.")
        else:
            print("idk what ur trying to do here so im not erasing anything.")
        self.look_at_json()

    def list_all(self):
        with open(f'{script}{self.path}activities.json') as f:
            lists = json.load(f)
            listed = str(lists)
            list_strip = listed.strip("\{\}")
            print(list_strip)
            f.close()

    def delete_one(self):
        with open(f'{script}{self.path}activities.json', "r") as f:
            acts = json.load(f)
            f.close()
        listed = str(acts)
        list_strip = listed.strip("\{\}")
        print(list_strip)
        which = input("Which activity would you like to delete? (Input the time of the activity) ")
        if which in acts.keys():
            del acts[which]
            with open(f'{script}{self.path}activities.json', "w", encoding="utf-8") as f:
                json.dump(acts, f)
                f.close()
            print(f"{which} has been deleted.")
        else:
            print("Not found")
        self.look_at_json()

    def set_color(self):
        new_color = input("What color would you like? (black, red, green, yellow, blue, magenta, cyan and white)")
        new_color = new_color.upper()
        with open(f'{script}{path}settings.json', "r") as f:
            current_settings = json.load(f)
            f.close()
        if new_color == "BLACK" or new_color == "RED" or new_color == "GREEN" or new_color == "YELLOW" or new_color == "BLUE" or new_color == "MAGENTA" or new_color == "CYAN" or new_color == "WHITE":
            current_settings["color"] = new_color 
            with open(f'{script}{path}settings.json', "w") as f:
                json.dump(current_settings, f)
                f.close()
            color = getattr(Fore, current_settings["color"])
            print(color, f"Successfully updated color to {new_color}")
        else:
            print("Invalid color")

    def get_time(self):
        date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        print(f"It is currently {date_time}")

    def greeting(self):
        with open(f'{script}{self.path}name.json') as f:
            names = json.load(f)
            f.close()
        name = names.get("name")
        date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        print(f"Hello, {name}, it is currently {date_time}.")

    def help(self):
        print("""Welcome to the activity tracker!\nCommands:\nchange_name: changes your name
add_activity: adds an activity.\ndelete_all: deletes ALL activities\nlist_all: lists all current activities\ndelete_one: Delete one specified activity\ntime: tells the time\nset_color: change color of terminal
 """)
