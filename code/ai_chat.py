#!/usr/bin/env python3
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
            1. blueprint creation
            2. blueprint validation
            3. Plan creation
            4. Plan validation
"""
# NOTE: I dont need the second horisontal split, since only 1 file is modified and worked on at a time. 

print("Initialising ai_chat")

from pydantic import SecretStr
from rich import print

print("[green]Colors initiated. =)[/green]")

import sys
import LMIA_context_mini
import config
import json
from pathlib import Path

print("[green]basic initialisation completed. [/green]")
print("[green]initialising langchain agent.[/green]")

from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.json.toolkit import JsonToolkit
from langchain_community.tools.json.tool import JsonSpec
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
# from langchain_community.agent_toolkits.json.base import create_json_agent

print("[green]Everything else initialised[/green]")

dump_file = Path("./dump.json")
if dump_file.is_file():
    with open("./dump.json", "rw") as f:
        save_file_json = json.load(f)
        if save_file_json:
            raise NotImplementedError()

        # TODO: Finish this
else:
    print("No save file was found. Starting a new conversation.")

# Json loading
try:
    global data_blueprint
    data_blueprint = json.load(open("blueprint.json"))
except Exception as e:
    print("[red] ERROR: DIDNT FIND blueprint.json file. [/red]")
    print(f"For debug purpuses: Error is: {e}")
    print("[red]creating an empty blueprint.json file.[/red]")
    bluep = Path("./blueprint.json")
    bluep.touch()
    bluep.write_text("{}")
    data_blueprint = json.load(open("blueprint.json"))

# Creation of tools.
spec = JsonSpec(dict_=data_blueprint)
toolkit = JsonToolkit(spec=spec)
tools = toolkit.get_tools()

tools_by_name = {tool.name: tool for tool in tools}

# creation of the llm, e.g. client:
llm = ChatOpenAI(
    model=config.model, 
    base_url="https://openrouter.ai/api/v1", 
    api_key=SecretStr(config.api_key)
    )

# Bind the tools to the client
llm = llm.bind_tools(tools)

prompt = ChatPromptTemplate.from_messages([
        ("system", "{system_prompt},"),
        ("system", "Relevant memory: {memory}"),
        ("human", "{input}")
    ])

print("[bold][italic][red]Hello, human. Welcome to NullLab-mini chat[/red][/italic][/bold]")

print("defining funktions")

def agent_turn(user_input_for_turn, system_prompt_for_the_turn, memory):
    messange = prompt.invoke({"input": user_input_for_turn, "system_prompt": system_prompt_for_the_turn, "memory": memory}).to_messages()

    for _ in range(config.max_tool_runs):
        ai_message = llm.invoke(messange)
        messange.append(ai_message)

        if not ai_message.tool_calls:
            return ai_message.content
        
        for call in ai_message.tool_calls:
            tool = tools_by_name[call["name"]]
            result = tool.invoke(call["args"])

            messange.append(ToolMessage(content=str(result), tool_call_id=call["id"]))
            
    raise RuntimeError("AI tried doing to many tool calls. If you think it did everything correctly, increase the max_tool_runs config parameter. Else do nothing and just retry.")
stage = 1
mem = LMIA_context_mini.LMIA_context_mini("./DB.db", interactive=True) # Memory initialisation

# Variable mess.
error_action = None
_flag_first_time = True

# Main loop
while stage in (1, 2, 3, 4):
    # This is the user input handling
    user_input = input("You: ").strip()
    if user_input.lower() in ("exit", "quit"):
        prev_stage = stage
        error_action = "exit"
    elif user_input.lower == "COMMAND:go_next_stage":
        stage =+ 1
        _flag_first_time = True

    mem.input_context(user_input, 1) # NOTE: 0 == ai , 1 == user

    # This is the response handling
    if stage == 1:
        if _flag_first_time:
            system_prompt = config.global_ai_instructions_for_stage_1_and_3
            
            system_prompt = system_prompt + """
            Your goal is, to collaboratively with the user, create the Blueprint.json . 
            Blueprint.json is a plan for a programm that the user wants to create. 
            It must be cristal clear, without any underspecifications, and follow a strict shema. 
            This is an example of Blueprint.json: 


            {
                "full_workflow_description": "workflow",
                "modules": [
                    {
                        "module_name": "Insert ModuleName",
                        "main_function": {
                            "name": "insert funktion name",
                            "workflow": "inser funktion high level workflow here",
                            "return": "insert the returned values, what they mean, and their types. ",
                            "depends_on": ["list", "of", "funktions", "and", "modules", "this", "funktion", "depends", "on"]
                        },    
                        
                        "funktions": [
                            {
                                "name": "insert funktion name",
                                "workflow": "inser funktion high level workflow here",
                                "return": "insert the returned values, what they mean, and their types. ",
                                "depends_on": ["list", "of", "funktions", "and", "modules", "this", "funktion", "depends", "on"]
                            }
                        ],
                        "requirements": [
                            {
                                "import_name": "Library or module name here",
                                "use_cases": [
                                    {
                                        "funktion": "Insert funktion name here",
                                        "workflow": "Insert funktion workflow here",
                                        "note": "Insert How? Why? Where? here."
                                    }
                                ]
                            }
                        ]
                    }
                ],
                "dependancy_graph": [
                    {
                        "funktion_name": "name",
                        "depends_on": "funktion_name" 
                    }
                ]
            }
            Blueprint.json MUST FOLLOW THIS SHEMA. 
            """

            _flag_first_time = False
        else:
            pass
            # Note: Moving to normal execution. 
        
        relevant_memory = mem.get_context(user_input)
        response = agent_turn(user_input_for_turn=user_input, system_prompt_for_the_turn=system_prompt, memory=relevant_memory)
        mem.input_context(response, 0)
        print("[green]AI answers: [/green]")
        print(f"{response}")


    elif stage == 2:
        if _flag_first_time:
            print("[yellow]Moved to stage 2. [/yellow]")
            print("[red]Would you like to clear Ais memory or[/red]")
            answer = input("(Y/N/Abort) : ").lower().strip()
            if answer in ("yes", "y"):
                print("[red] Are you sure you want to clear AI memory ? [/red]")
                if input().lower().strip() in ("yes", "y"):
                    raise NotImplementedError("Plugin doesnt yet have a function to.")
                    #mem.clear_memory() # TODO: Implement the clear_memory() method. 
                else:
                    print("[red]aborting clearanse. [/red]")
            else:
                print("keeping the memory.")
                _flag_first_time = False    # NOTE: DONT FORGET. 
        else:
            pass

        system_prompt = config.global_ai_instructions
        system_prompt = system_prompt + """
        """ #TODO: FIXME
        raise NotImplementedError("line 217. Stage 2. repo/code/ai_chat.py")


    elif stage == 3:
        pass
    elif stage == 4:
        pass

    # ERROR ACTION handling here. This is kinda the shit that should handle everything. 
    if error_action is not None:
        if error_action == "exit":
            print("[red]shutting down.[/red]")
            print("[red]FEATURE OF SAVING PROGRESS NOT IMPLEMENTED[/red]")
            print("[red]You sure you want to exit[/red]")
            print("[red][bold]???[/bold][/red]")
            if input("Answer: ").strip().lower() in ("no", "n", "nope", "never", "nah"):
                error_action = None
            else:
                print("[red]Due to the fact that this programm is still NOT FINISHED, and NOTHING IS IMPLEMENTED[/red]")
                print("[red]I just exit and thats it.[/red]")
                sys.exit("Yep, just exiting")
else:
    sys.exit("WTF HAPPENED HERE?")
