main.py of NullLab-mini projekt.
# I coded this from a mobile device, so have some respect of this work !!!

# Lets get this fun little thingy.

dir = None
state = 0

projekt_parts = ["plan.json";"blueprint.json";"metadata.json";"config.py";"bugs.json";"projekt.db";"memory.json";"memory.db";]

def state0():                                                   while True:
        print("initialising NullLab-mini")
        print("import sequense beginns now.")
        Try:
            from pathlib import Path as p
            # All the imports go here.

        expect exeptions as e:                                          if e is not None:                                               print(f"following error was found: {e} . Aborting execution.")
                print("early diagnostics: problem was found in main.py, in the initialisation of state0. Possible culprints:")
                print("Python dependancies, partial installation, broken installation.")
                raise RunTimeError(f"Failed to initialise. {e}")

        # import sequence completed
        print("early initialisation complete.")
                                                                    # Now comes the projekt init
        while True:                                                                                                                 global dir = input("input path to work directory.")                                                                     d = Path(dir)
            print("initialising at {dir}")                  
            # Path checks.
            #
            #
            #
            #
            #
            #
            #                                                           #

            print("NullLab-mini will now assume full controll over dir {dir}.")
            if input("Confirmation. Yes or No") == "Yes" or "Y":
                break
            else:
                print("No confirmation recived. Aborting one step back.")
                continue

        while True:

                                                                        # Check if projekt files exist.
            # if True, break, if false, pass.               
            print("Projekt not found on {dir}")
            if input("initialise an empty projekt?") == "Yes" or "Y":                                                                   # The list of required files.
                # Initialise the empty projekt.
                # just a bunch of "subprocess run cd {dir} && touch {filename.}"

                break
            else:
                continue


    # Double check everything.                              
    global state = 1
    return None