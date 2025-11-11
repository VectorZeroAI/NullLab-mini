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



# I coded this from a mobile device, so have some respect of this work !!!

# Lets get this fun little thingy.

base_dir = None
state = 0

projekt_parts = ["plan.json", "blueprint.json", "metadata.json", "config.py", "bugs.json", "projekt.db", "memory.json", "memory.db"]


# ----------------------------------------------------------------------------------------------------

"""

State0, the init state. 
This state loads all the actual dependancies, as well as interactivly initialises the programm. 

TODO: FUTURE: add a configuration option that loads you into a projekt instantly. 

"""

def state0():   
    while True:
        
        global exep

        print("initialising NullLab-mini")
        print("import sequense beginns now.")
        
        # Gracefull handling of missing dependancies. 

        try:
            from pathlib import Path
            
            # All the imports go here. This block handles missing dependancies gracefully, and tells the user about them. 

        except ImportError as exep:
            raise RuntimeError(f"missing dependancy {exep}. Install it to use the programm.") from exep

        """
        The import should be in try expect with proper handling of missing imports, but it didnt work for some reason, so I just cut it out. 
        """

        print("early initialisation complete.")
        
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
                print("directory found. Continuing")
                pass
            else:
                print("dir not found, plese retry.")
                continue
                                               

            print(f"NullLab-mini will now assume full controll over dir {input_dir}.")
            if input("Confirmation. Yes or No") == "Yes" or "Y":
                break
            else:
                print("No confirmation recived. Aborting one step back.")
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
                    print(f"file {name} not found.")            # Just a simple check. 
                    if flag_file_not_found == None: 
                        flag_file_not_found = 0
                    else:
                        flag_file_not_found =+ 1
                    
            
            # if True, break, if false, pass.
            if flag_file_not_found != None:
                print(f"Projekt not found on {dir}")
                if input("initialise an empty projekt?") == "Yes" or "Y":              # Init of an empty projekt.                                                      # The list of required files.
                    
                    for file in projekt_parts:
                        file_path = base_dir / file
                        if not file_path.exists():
                            file_path.touch
                            print(f"created file {file}")
                        else:
                            print(f"file {file} already existed. Ignoring.")   # I think this is pretty good design. 

                    break
                else:
                    global flag_retry   # I hate flags. 
                    flag_retry = 1
                    break
            if flag_retry != 1:         # Like, why the fuck do I need to do this? Why doesnt python support loop labels?
                flag_retry = 0          # I will switch to rust after this. I hate this!!!!
                break
            else:
                global flag_state_0_complete
                flag_state_0_complete = 1
                break
        if flag_state_0_complete == 1:
            break

    #TODO Double check everything. 
    # Or not. Dont really know myself how to nor what for. 


    global state 
    state = 1
    
    return True       # True means sucsess, False or crash means fatal error, None means unknown error scale. 
    
"""
There is a problem with error handling, and that is that I dont get how it works. I will implement that at some point, but for now its not present.
The programm just crashes if an error occures, for the user to fix. 
This will be improoved later on.
"""
    
# TODO: Implement error handling. 

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
        raise RuntimeError("STATE MASHINE BROKE. SHUTTING DOWN. CRITICAL ERROR.")
