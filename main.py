"""
main.py of NullLab-mini projekt.
"""

from mygo import enable_goto, label, goto

# I coded this from a mobile device, so have some respect of this work !!!

# Lets get this fun little thingy.

dir = None
state = 0

projekt_parts = ["plan.json", "blueprint.json", "metadata.json", "config.py", "bugs.json", "projekt.db", "memory.json", "memory.db"]


def state0():   
    while True:
        print("initialising NullLab-mini")
        print("import sequense beginns now.")
        Try:
            from pathlib import Path
            # All the imports go here.

        expect exeptions as e:      
            if e is not None:                                           
                print(f"following error was found: {e} . Aborting execution.")
                print("early diagnostics: problem was found in main.py, in the initialisation of state0. Possible culprints:")
                print("Python dependancies, partial installation, broken installation.")
                raise RunTimeError(f"Failed to initialise. {e}")

        # import sequence completed
        print("early initialisation complete.")
        
        # Now comes the projekt init
        
        while True:                                                                         
            global dir = input("input path to work directory.")     
            d = Path(dir)
            print("initialising at {dir}")                  
            
            if my_dir.exists():
                print("directory found. Continuing")
                pass
            else:
                print("dir not found, plese retry.")
                continue
                                               

            print("NullLab-mini will now assume full controll over dir {dir}.")
            if input("Confirmation. Yes or No") == "Yes" or "Y":
                break
            else:
                print("No confirmation recived. Aborting one step back.")
                continue

        while True:
            
            for name in global projekt_parts:
                file_path = global dir / name
                if file_path.exists() and file_path.is_file():
                    pass
                else:
                    print(f"file {name} not found.")
                    
            
            # if True, break, if false, pass.

            print("Projekt not found on {global dir}")
            if input("initialise an empty projekt?") == "Yes" or "Y":                                                                   # The list of required files.
                # Initialise the empty projekt.
                # just a bunch of "subprocess run cd {dir} && touch {filename.}"

                break
            else:
                continue


    # Double check everything.                              
    global state = 1
    return None
