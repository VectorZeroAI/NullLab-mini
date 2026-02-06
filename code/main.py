#!/usr/env/python3
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

from pathlib import Path
import subprocess
from rich import print

print("initialising NullLab-mini")

projekt_dir: object | None = None
state: int = 0

BASE = Path(__file__).resolve().parent

projekt_parts: list[str] = ["plan.json", "blueprint.json", "metadata.json", "config.py", "bugs.json", "projekt.db", "memory.json", "memory.db"]


"""
The import should be in try expect with proper handling of missing imports, but it didnt work for some reason, so I just cut it out. 
"""

print("[green]early initialisation complete.[/green]")



def state0() -> bool | None:
    """
    State0, the init state. 
    This state loads all the actual dependancies, as well as interactivly initialises the programm. 

    TODO: FUTURE: add a configuration option that loads you into a projekt instantly. 

    state0 also downloads the Nulllab-mini compiler, as that thing is now a separate repo!
    """
    while True:
        
        #!!! Now comes the projekt init
        # TODO: add the compiler downloading code
        
        # This is the interactive projekt initialisation, with per step retry via the nested loops. 
        # I think more people should do this kind of stuff more often in their programms. 
        # Goto may have made this way cleaner then this, but whatever, python doesnt have good goto support. 

        while True:                                                                         
            
            global projekt_dir 
            
            input_dir: str = input("input path to work directory.")     
            print(f"initialising at {input_dir}")
            projekt_dir = Path(input_dir)
            
            if projekt_dir.exists():
                print("[green]directory found. Continuing[/green]")
                pass
            else:
                print("[red]dir not found, plese retry.[/red]")
                continue
                                               

            print(f"NullLab-mini will now assume [red]full controll[/red] over dir {input_dir}.")
            if input("Confirmation. Yes / No").lower().strip() in ("yes", "y"):
                print("[green]confirmation recieved. Proceesing[/green]")
                break
            else:
                print("[red]No confirmation recived. Aborting one step back.[/red]")
                continue

        # The Nulllab-compiler download stage
        while True:
            import subprocess
            try:
                subprocess.run("git clone http://github.com/VectorZeroAI/Nulllab-compiler {BASE}/", shell=True)
            except subprocess.SubprocessError as e:
                print("[red] download of Nulllab-compiler failed [/red]")
                print(e)
                print("would you like to retry?")
                if input("Y/n : ").lower().strip() in ("yes", "y", "yep", ""):
                    continue
                else:
                    print("Impossible to proseed without the compiler: failing ...")
                    raise RuntimeError("failed to download tje Nulllab-compiler") from e
            else:
                print("assuming Nulllab-compiler is installed.")
                break

        while True:
            
            global projekt_parts
            # Yes, I slapped those everywhere, because I dont really get how these work, I will separate by name most of the time anyway. 
            flag_file_not_found: int | None
            flag_file_not_found = None

            for name in projekt_parts:
                file_path = projekt_dir / name
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
                flag_retry = False
                print(f"[red]Projekt not found on {dir}[/red]")
                if input("initialise an empty projekt? Y/n").lower().strip() in ("y", "yes", ""):
                    
                    for file in projekt_parts:
                        file_path = projekt_dir / file
                        if not file_path.exists():
                            file_path.touch()
                            print(f"[green]created file {file}[/green]")
                        else:
                            print(f"file {file} already existed. Ignoring.")   # I think this is pretty good design. 
                    
                    break # This one breaks the loop 2.
                else:
                    flag_retry = True
                    flag_retry: bool | None # I hate flags. 
                    break
        if flag_retry:         # Like, why the fuck do I need to do this? Why doesnt python support loop labels?
            flag_retry = False          # I will switch to rust after this. I hate this!!!!
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


def state1():
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
    while True:
        print("Initialising tmux session")
        TMUX_SESSION_NAME: str = "NullLab_mini_session"
        print(f"Tmux session name : {TMUX_SESSION_NAME}")
        subprocess.run([
            "tmux", "new-session", "-d", "-s", f"{TMUX_SESSION_NAME}", "-n", "main"
            ])

        subprocess.run([
            "tmux", "split-window", "-v", "-t", f"{TMUX_SESSION_NAME}:main"
            ])
        subprocess.run([
            "tmux", "send-keys",
            "-t", f"{TMUX_SESSION_NAME}:main.0",
            "python3 ai_chat.py",
            "C-m"
        ])      # This here runs the ai_chat.py app into the session on the side.
        # subprocess.run(["tmux", "<tmux-command>", "-t", "<target>", "<shell command>"])    
        # This is the template for tmux command launching. 

        global state
        global previous_text_blueprint
        global previous_text_plan
        global currrent_text_plan
        global current_text_bluep

        from time import sleep

        import threading

        def state_1_json_print(input_text: str) -> None:
            subprocess.run([
                    "tmux", "send-keys", "-t", f"{TMUX_SESSION_NAME}:main.1",
                    f"echo '{input_text}'", "C-m"
                ])

        def PlanJsonLoop() -> None:
            global previous_text_plan
            global currrent_text_plan
            while not JSON_PRINTERS_STOP:
                sleep(1)
                currrent_text_plan = PlanJson.read_text()
                if previous_text_plan != currrent_text_plan:
                    previous_text_plan = currrent_text_plan
                    state_1_json_print(currrent_text_plan)
            print("json_printer thread for PlanJson has stopped")

        def BlueprintJsonLoop() -> None:
            global previous_text_blueprint
            global current_text_bluep
            while not JSON_PRINTERS_STOP:
                sleep(1)
                current_text_bluep = BlueprintJson.read_text()
                if previous_text_blueprint != current_text_bluep:
                    previous_text_blueprint = current_text_bluep
                    state_1_json_print(current_text_bluep)
            print("json_printer thread for BlueprintJson has stopped")

        JSON_PRINTERS_STOP: bool = False

        print(f" The files that you are getting displayed are located at [green] {BASE}/Nulllab-compiler/blueprint.json [/green] \n")
        print(f" and at [green]{BASE}/Nulllab-compiler/blueprint.json [/green] \n")
        print(f" To see the [red]BEAUTIFUL[/red] interface, go to the tmux session here {TMUX_SESSION_NAME}")

        BlueprintJson = Path(f"{BASE}/Nulllab-compiler/blueprint.json")
        PlanJson = Path(f"{BASE}/Nulllab-compiler/plan.json")

        while state == 1:

            sleep(1)

            if BlueprintJson.exists():
                _flag_blueprint_json_found = True
            else:
                _flag_blueprint_json_found = False

            if PlanJson.exists():
                _flag_plan_json_found = True
            else:
                _flag_plan_json_found = False

            # ----

            if not _flag_plan_json_found and not _flag_blueprint_json_found:
                continue

            if _flag_plan_json_found:
                threading.Thread(target=PlanJsonLoop, daemon=True).start()

            if _flag_blueprint_json_found:
                threading.Thread(target=BlueprintJsonLoop, daemon=True).start()

            else:
                sleep(1)
                # FIXME : MAKE THE LOOP BREAKAGE WORK !!!
                # The issue with breakage is that state is never set to anything other then 1 .
                # Basically I never implemented the shutdown logic for the state. 
                # TODO: Implement the shutdown logic. 
        else:
            JSON_PRINTERS_STOP = True # FIXME : This here also needs to be revised




# --------------------------------------------------------------------------------


def state2():
    """
    This is state 2, the implementation state. It will just be a for loop of API calls and file saves. 
    """
    pass






# --------------------------------------------------------------------------------


def state3():
    """
    This is state 3, the debugging state. 
    This is gonna be a set of for loops, with a bunch of json saves. 
    """
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
