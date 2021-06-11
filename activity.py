from os.path import abspath, dirname
import json
from datetime import datetime
import time
from pushover import init, Client

#get file path
script = dirname(abspath(__file__))

with open(f'{script}\\activities.json', "r") as f:
        acts = json.load(f)
        f.close()

with open(f'{script}\\config.json', "r") as f:
        config = json.load(f)
        user = config.get("user_key")
        api = config.get("api_key")
        f.close()

client = Client(user, api_token=api)

#activity class
class Activity:
    def __init__(self):
        self.acts = acts
        self.user = user
        self.api = api
        self.client = client

    def get_name(self):
        self.name = input("What is your name?\n> ")
        name_dict = {"name": self.name}
        with open(f'{script}\\name.json', "w", encoding="utf-8") as f:
            json.dump(name_dict, f, ensure_ascii=False, indent=4)

    def check_for_act(self):
        while True:
            its_time = datetime.now().strftime("%H:%M")
            if its_time in self.acts:
                self.client.send_message(self.acts[its_time], title=self.acts[its_time])
            time.sleep(60)

    def look_at_json(self):
        with open(f'{script}\\activities.json', "r") as f:
            data = json.load(f)
            f.close()
        self.acts = data

    def add_activity(self):
        new_act = input("Please enter the name of the new activity: ")
        new_time = input("Please enter the time in 24 hour format (hour:minute):")
        try:
            (hour,minute) = new_time.split(":")
            if int(hour) <= 24 and int(hour) >= 0 and int(minute) <= 60 and int(minute) >=0:
                if int(hour) < 10 and hour != "01" and hour != "02" and hour != "03" and hour != "04" and hour != "05" and hour != "06" and hour != "07" and hour != "08" and hour != "09":
                    hour = "0" + hour
                if int(minute) < 10 and minute != "01" and minute != "02" and minute != "03" and minute != "04" and minute != "05" and minute != "06" and minute != "07" and minute != "08" and minute != "09":
                    minute = "0" + minute
                act_dict = {f"{hour}:{minute}": new_act}
                with open(f'{script}\\activities.json', "r") as f:
                    data = json.load(f)
                    data.update(act_dict)
                    f.close()
                with open(f'{script}\\activities.json', "w", encoding="utf-8") as asdf:
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
            with open(f'{script}\\activities.json', "w", encoding="utf-8") as f:
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
        with open(f'{script}\\activities.json') as f:
            lists = json.load(f)
            listed = str(lists)
            list_strip = listed.strip("\{\}")
            print(list_strip)
            f.close()

    def delete_one(self):
        with open(f'{script}\\activities.json', "r") as f:
            acts = json.load(f)
            f.close()
        listed = str(acts)
        list_strip = listed.strip("\{\}")
        print(list_strip)
        which = input("Which activity would you like to delete?: ")
        if which in acts.keys():
            del acts[which]
            with open(f'{script}\\activities.json', "w", encoding="utf-8") as f:
                json.dump(acts, f)
                f.close()
            print(f"{which} has been deleted.")
        else:
            print("Not found")
        self.look_at_json()

    def get_time(self):
        date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        print(f"It is currently {date_time}")

    def greeting(self):
        with open(f'{script}\\name.json') as f:
            names = json.load(f)
            f.close()
        name = names.get("name")
        date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        print(f"Hello, {name}, it is currently {date_time}.")

    def help(self):
        print("""Welcome to the activity tracker!\nCommands:\nchange_name: changes your name
add_activity: adds an activity.\ndelete_all: deletes ALL activities\nlist_all: lists all current activities\ndelete_one: Delete one specified activity\ntime: tells the time """)
