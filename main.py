from os.path import abspath, dirname
import json
import time
import threading
import multiprocessing
import sys
from pushover import init, Client

#My modules
from activity import Activity

#Check for amount of cores
cpu_count = multiprocessing.cpu_count()
if cpu_count < 2:
    print("Sorry. This cannot run with less than 2 cores.")
    sys.exit()
else:
    #Open the config json file
    script = dirname(abspath(__file__))
    with open(f'{script}\\config.json') as f:
        config = json.load(f)

    #This stores name and stuff
    with open(f'{script}\\name.json') as f:
        settings = json.load(f)

    #get config stuffs for pushover
    user = config.get("user_key")
    api = config.get("api_key")

    #Start the Pushover client
    client = Client(user, api_token=api)

    #Start activity class
    activity = Activity()

    if settings["name"] is None:
        activity.get_name()

    #get current acts
    with open(f'{script}\\activities.json') as f:
        acts = json.load(f)

    #sleep so the computer can write to file
    time.sleep(.1)

    activity.greeting()

    #As a wise man once said; LETS GO!
    while True:
        checking = threading.Thread(target=activity.check_for_act)
        checking.start()
        user_input = input(">")
        if user_input == "help" or user_input == "h" or user_input == "man" or user_input == "?":
            activity.help()
        elif user_input == "change_name":
            activity.get_name()
        elif user_input == "add_activity":
            activity.add_activity()
        elif user_input == "delete_all":
            activity.delete_all()
        elif user_input == "list_all":
            activity.list_all()
        elif user_input == "delete_one":
            activity.delete_one()
        elif user_input == "time" or user_input == "get_time":
            activity.get_time()

        elif user_input == "exit" or user_input == "quit":
            print("Exiting. Please be aware that activities will not be notified while this is not running.")
            print("idk how to stop threads")
            sys.exit()
        else:
            print("Unknown command. Do help to learn more.")

