# This is my main file. 
"""
main.py of NullLab-mini projekt.
This is my Structured auto coder projekt. 
The key idea is that the more input the LLM gets the better code it produces. 

The projekt is written in presedural style. 

It has 4 states, the state0, state1, state2 and state3 .

State0 is the init state. 
State1 is the planning state.
State2 is the coding state.
State3 is the debugging/analysis state. 

The key idea is that the whole projekt is planned before the first line of code is even written, and everything is planned 
through with mashine like clarity. 

Everything is saved in json. 
The projekt was originaly planned to be coded via AI like all my other projekts, but this one I write myself, so the code
quality will be better then "it doesnt crash".

This is the first time I actually write code myself, so I hope you can all be ... tolerant to mistakes. 

I try to document as much as I can, since this makes the code fat better. 
"""

# ----------------------------------------------------------------------------------------------------------------

"""
This is pre state globals, and some basics. 
mygo is the library I use for the goto funktion, since I may need it, I keep it here. 
I will delete it the moment I make sure I dont need it here.
Every goto use case will be clearly documented, in order to not cause spagetti code. 
UPDATE: mygo didnt work, so I removed the line.
I will use it the moment I have to deal with confusing loop heuristics again!!!!
"""

# from mygo import enable_goto, label, goto


# Lets get this fun little thingy.

base_dir = None
state = 0

projekt_parts = ["plan.json", "blueprint.json", "metadata.json", "config.py", "bugs.json", "projekt.db", "memory.json", "memory.db"]


# ----------------------------------------------------------------------------------------------------
"""
Early init state
Dependancy loading
"""


print("initialising NullLab-mini")
print("import sequense beginns now.")

from pathlib import Path
import subprocess
from rich import print

"""
The import should be in try expect with proper handling of missing imports, but it didnt work for some reason, so I just cut it out. 
"""

print("[green]early initialisation complete.[/green]")


"""

State0, the init state. 
This state loads all the actual dependancies, as well as interactivly initialises the programm. 

TODO: FUTURE: add a configuration option that loads you into a projekt instantly. 

"""

def state0():   
    while True:
        
        #!!! Now comes the projekt init
        
        # This is the interactive projekt initialisation, with per step retry via the nested loops. 
        # I think more people should do this kind of stuff more often in their programms. 
        # Goto may have made this way cleaner then this, but whatever, python doesnt have good goto support. 

        while True:                                                                         
            
            global base_dir 
            
            input_dir = input("input path to work directory.")     
            print(f"initialising at {input_dir}")
            base_dir = Path(input_dir)
            
            if base_dir.exists():
                print("[green]directory found. Continuing[/green]")
                pass
            else:
                print("[red]dir not found, plese retry.[/red]")
                continue
                                               

            print(f"NullLab-mini will now assume full controll over dir {input_dir}.")
            if input("Confirmation. Yes or No").lower() in ("yes", "y"):
                print("[green]confirmation recieved. Proceesing[/green]")
                break
            else:
                print("[red]No confirmation recived. Aborting one step back.[/red]")
                continue

        while True:
            
            global flag_file_not_found
            global projekt_parts
            # Yes, I slapped those everywhere, because I dont really get how these work, I will separate by name most of the time anyway. 

            for name in projekt_parts:
                file_path = base_dir / name
                if file_path.exists() and file_path.is_file():
                    pass
                else:
                    print(f"[red]file {name} not found.[/red]")            # Just a simple check. 
                    if flag_file_not_found is None: 
                        flag_file_not_found = 0
                    else:
                        flag_file_not_found =+ 1
                    
            
            # if True, break, if false, pass.
            if flag_file_not_found is not None:
                print(f"[red]Projekt not found on {dir}[/red]")
                if input("initialise an empty projekt?").lower in ("y", "yes"):
                    
                    for file in projekt_parts:
                        file_path = base_dir / file
                        if not file_path.exists():
                            file_path.touch()
                            print(f"[green]created file {file}[/green]")
                        else:
                            print(f"file {file} already existed. Ignoring.")   # I think this is pretty good design. 
                    
                    break # This one breaks the loop 2.
                else:
                    global flag_retry   # I hate flags. 
                    flag_retry = 1
                    break
        if flag_retry == 1:         # Like, why the fuck do I need to do this? Why doesnt python support loop labels?
            flag_retry = 0          # I will switch to rust after this. I hate this!!!!
            continue
        else:
            break # This one breaks loop 1.


    global state 
    state = 1    # This one switches the state. 
    
    print("[green]init state over. Return status = good[/green]")
    return True       # True means sucsess, False or crash means fatal error, None means unknown error scale. 
    
"""
The error handling was implemented. The Import errors are now able to be 
catched, and then displayed, insdead of sshowing them one by one
as the normal python error traceback does. 

This is my way to handle errors, wich is just a clean error messenge / s .
"""

# ----------------------------------------------------------------------------------------------------------------

"""
State 1, the planning state. 

This is the state where AI and the user collaborate on planning the projekt through. 
The projekt blueprint is saved under "blueprint.json".
The projekt implementation plan is saved under "plan.json".
I will at some point make a json shema.

The main problem is: How will the user see the files, and how to make the collaboration work? 
... This needs more consideration. 

Done for today!!!
"""

#TODO: make shemas for json. 

def state1():
    while True:
        print("initialising tmux session")
        tmux_session_name = "NullLab_mini_session"
        print(f"tmux session name : {tmux_session_name}")
        subprocess.run([
            "tmux", "new-session", "-d", "-s", f"{tmux_session_name}", "-n", "main"
            ])

        subprocess.run([
            "tmux", "split-window", "-v", "-t", f"{tmux_session_name}:main"
            ])
        # NOTE: We will only be showing one of the files at a time. So, no need for the second split
        # NOTE: Since only one of those is modified at a time. 
        subprocess.run([
            "tmux", "send-keys",
            "-t", f"{tmux_session_name}:main.0",
            "python3 ai_chat.py",
            "C-m"
        ])      # This here runs the ai_chat.py app into the session on the side.
        # subprocess.run(["tmux", "<tmux-command>", "-t", "<target>", "<shell command>"])    
        # This is the template for tmux command launching. 
        global state
        while state == 1:
            pass
            # TODO: FINISH THIS BLOCK. 
            # this block must check for changes in files blueprint.json and plan.json, 
            # via watchdog
            # and update the view in the second half of the screen. 
            # ...
            # As well as monitor for changes in "signal.json" file. 
            # Once changes detected, look into the value in there. 
            # And the value in there is the signal. 
            # This will be used by the ai_chat.py to signal that the view must be changed. 



# TODO: DONT FORGET COLORS

# --------------------------------------------------------------------------------

"""
This is state 2, the implementation state. It will just be a for loop of API calls and DataBase saves. 
"""

def state2():
    pass






# --------------------------------------------------------------------------------

"""
This is state 3, the debugging state. 
This is gonna be a set of for loops, with a bunch of json saves. 
"""

def state3():
    pass



# --------------------------------------------------------------------------------
"""
This is the state mashine, that transmits the states. 
All the logic is inside states. 
States manage transmition themself. 
States management is inside states. 
This is just a small script. 
"""


while True:
    if state == 0:
        state0()
    if state == 1:
        state1()
    if state == 2:
        state2()
    if state == 3:
        state3()
    else:
        raise RuntimeError("STATE MASHINE BROKE. SHUTTING DOWN. CRITICAL ERROR. IDK what the fuck happened here. ")
