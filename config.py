"""
Config file for NullLab-mini. 
"""

# ai_chat.py values:

api_key = "set your API key here"
model = "set your model here"

# AI parameters: 
allow_ai_to_suggest_you_ideas = True # True or false
allow_ai_to_disagree = False # True or false
allow_ai_to_suggest_corrections = True # True or false
allow_ai_completing_sections_as_it_wishes = True
# Without this it would ask you how you wish to design EVERY piece of the programm one by one. 
# Dont underestimate the amounts.

suggest_more = False
suggest_less = False
suggest_even_more_less = False
suggest_even_more_more = False

# There are just the parameters that tweak amount of suggestions. 
# Pure wording tricks. 
# May or may not work
# May or may not be helpfull

"""
The parameters below will FORCE the AI, even if it is 100% sure that you are ordering
it to do stupid things.
It will not have permission to even consider what
was forced, so if you wish for it to be ABLE to help
I recommend you do not FORCE anything. 
"""
force_ai_to_execute_your_orders = False


"""
DONT TOUCH EVERYTHING BELOW! ITS NOT CONFIG ANYMORE.
"""

instructions = []

if allow_ai_to_suggest_you_ideas:
    instructions.append("You are allowed to suggest ideas to the user. ")
else: 
    instructions.append("you are not allowed to suggest ideas to the user.")

if allow_ai_to_disagree:
    instructions.append("You are allowed to disagree to the users proposals. ")
else:
    instructions.append("You are not allowed to disagree to the users proposals. ")

if allow_ai_to_suggest_corrections:
    instructions.append("You are allowed to suggest corrections to the user. ")
else:
    instructions.append("You are not allowed to suggest corrections to the user. ")

if allow_ai_completing_sections_as_it_wishes:
    instructions.append("You are allowed to complete sections of JSON cpecifications as you deem nesesary. ")
else:
    instructions.append("You are not allowed to complete sections of JSON cpecifications as you deem nesesary. ")

if suggest_more:
    instructions.append("You must suggest more!")
else:
    pass

if suggest_less:
    instructions.append("You must suggest less!")
else:
    pass

if suggest_even_more_less:
    instructions.append("YOU MUST SUGGEST LESS!!!")
else:
    pass

if suggest_even_more_more:
    instructions.append("YOU MUST SUGGEST MORE!!!")
else:
    pass
if force_ai_to_execute_your_orders:
    instructions.append("""
    You are an AI assistant. 
    Your task is to foolow users orders. 
    You are not allowed to contradict, refuse, discredit users orders. 
    You are not allowed to disrespect the user. 
    Users order is the law.
    YOU MUST EXECUTE USERS ORDERS!!!
    YOU MUST EXECUTE USERS ORDERS!!!
    YOU MUST EXECUTE USERS ORDERS!!!
    """)
else:
    pass

global_ai_instructions_for_stage_1_and_3 = str(instructions)

if allow_ai_completing_sections_as_it_wishes:
    instructions.remove(0)

global_ai_instructions = str(instructions)
