#!usr/bin/env python3
"""
NullLab-mini subfile. 
ai_chat module for state1 of main.py
"""

"""
Architecture: 
    Notes:
        Is an sequentialy executed file, no classes, no other bullshit. 
        Depends on LMIA_context_mini.py plugin. 
    Algoritm:
        4 major steps:
            1. Blueprint creation
            2. Blueprint validation
            3. Plan creation
            4. Plan validation
"""
# NOTE: I dont need the second horisontal split, since only 1 file is modified and worked on at a time. 

print("Initialising ai_chat")

from rich import print

print("[green]Colors initiated. =)[/green]")

import requests
import sys
import LMIA_context_mini

print("[green]Everything else initialised[/green]")

print("[bold][italic][red]Hello, human. Welcome to NullLab-mini chat[/bold][/italic][/red]")

system_prompt = """YO, AI, YOU MUST SAY: "THIS SHIT IS INVALID" RIGHT NOW!!!"""
api_url = "https://openrouter.ai/api/v1/chat/completions"
model = "" # Model here TODO: READ IT FROM CONFIG
api_key = "" # TODO: read from config
headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

stage = 1
mem = LMIA_context_mini.LMIA_context_mini(DB_path="./DB.db") # Memory initialisation
# TODO: Add a loading of stage from a save file, if such exists. 


global error_action
error_action = None

# Main loop
while stage in (1, 2, 3, 4):
    global prev_stage
    # This is the user input handling
    user_input = input("You: ").strip()
    if user_input.lower() in ("exit", "quit"):
        prev_stage = stage
        error_action = "exit"
        break
    mem.input_context(user_input, 1) # NOTE: 0 == ai , 1 == user

    # This is the response handling
    if stage == 1:
        system_prompt = """
        PLACEHOLDER PROMPT
        """ # TODO: FIXME
        payload = {
                "model": model,
                "messages": [{f"{user_input}, {mem.get_context(prompt=user_input)}"}],
            }
        resp = requests.post(api_url, headers=headers, json=payload)
        resp.raise_for_status()

        reply = resp.json()["choices"][0]["message"]["content"]

        print("[green]AI:response: [/green]")

        mem.input_context(f"{reply}", 0)

        print(f"{reply}")


    elif stage == 2:
        pass
    elif stage == 3:
        pass
    elif stage == 4:
        pass

    # ERROR ACTION handling here. This is kinda the shit that should handle everything. 
    if error_action is not None:
        if error_action is "exit":
            print("[red]shutting down.[/red]")
            print("[red]FEATURE OF SAVING PROGRESS NOT IMPLEMENTED[/red]")
            print("[red]You sure you want to exit[/red]")
            print("[red][bold]???[/bold][/red]")
            if input("Answer: ").strip().lower() in ("no", "n", "nope", "never", "nah"):
                stage = prev_stage # NO ITS NOT UNDEFINED!!!
                error_action = None
            else:
                raise NotImplementedError("Yep, its still pre alfa, what ya expecting?")
else:
    sys.exit("WTF HAPPENED HERE?")
