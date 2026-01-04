#!/usr/bin/env python3
from rich import print
from pydantic import SecretStr, ValidationError
import sys
import LMIA_context_mini
import config
import json
from pathlib import Path
from jsonschema import validate
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.json.toolkit import JsonToolkit
from langchain_community.tools.json.tool import JsonSpec
from langchain_core.messages import ToolMessage
from langchain_core.prompts import ChatPromptTemplate
# from langchain_community.agent_toolkits.json.base import create_json_agent

print("[green]Everything else initialised[/green]")

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
# -------------- function declaration / creation --------------------------------------------
"""
In this section all functions declarations are performed
"""
# ---------- agent turn function --------------
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
# --------------- json validation function ------------------
def validate_json_file(stage_for_this_func: int | None = None) -> bool:
    """
    function to test the work of ai with. 
    returns True if valid, False if invalid. 
    needs current stage_for_this_func given, although it can default to loading stage variable. 
    """
    if stage_for_this_func is None:
        stage_for_this_func = stage

    if stage_for_this_func == 1:
        with open("./blueprint.schema.json") as f:
            schema = json.load(f)
        try:
            validate(data_blueprint, schema)
        except ValidationError:
            return False
        else:
            return True
    elif stage_for_this_func == 2:
        return True
    elif stage_for_this_func == 3:
         with open("./plan.schema.json") as f:
            schema = json.load(f)
         try:
             validate(data_plan, schema)
         except ValidationError:
             return False
         else:
             return True
    elif stage_for_this_func == 4:
        return True
    else:
        raise RuntimeError("invalid stage")

# --------------- save function ------------------------
def save() -> bool:
    """
    Saves data specified inside this functions body. 
    Currently only saves stage. 
    Cannot possibly save chatbot memories, they are saved by the plugin. 
    """
    data_to_save = {
        "stage": stage
    }
    try:
        with open("./dump.json", "w") as f:
            json.dump(data_to_save, f, indent=4)
    except RuntimeError as e:
        print(f"following error occured during save: {e}")
        return False
    return True

# --------------- json loading --------------------------------------------------------
# blueprint loading
try:
    global data_blueprint
    data_blueprint = json.load(open("blueprint.json"))
except Exception as e:
    print("[red] ERROR: DIDNT FIND blueprint.json file. [/red]")
    print(f"For debug purpuses: Error is: {e}")
    print("[red]creating an empty blueprint.json file.[/red]")
    Bluep = Path("./blueprint.json")
    Bluep.touch()
    Bluep.write_text("{}")
    data_blueprint = json.load(open("blueprint.json"))
# plan loading
try:
    global data_plan
    data_plan = json.load(open("plan.json"))
except Exception as e:
    print("[red] ERROR: DIDNT FIND plan.json file. [/red]")
    print(f"For debug purpuses: Error is: {e}")
    print("[red]creating an empty plan.json file.[/red]")
    pla = Path("./plan.json")
    pla.touch()
    pla.write_text("{}")
    data_plan = json.load(open("plan.json"))

# ======= AGENT INIT =====================================================================
# Creation of tools for blueprint.json
spec_blueprint = JsonSpec(dict_=data_blueprint)
toolkit_blueprint = JsonToolkit(spec=spec_blueprint)
tools_blueprint = toolkit_blueprint.get_tools()

# Creation of tools for plan.json
spec_plan = JsonSpec(dict_=data_plan)
toolkit_plan = JsonToolkit(spec=spec_plan)
tools_plan = toolkit_plan.get_tools()

# Merge tools
tools = tools_blueprint + tools_plan
tools_by_name = {tool.name: tool for tool in tools}

# creation of the llm, e.g. client:
llm = ChatOpenAI(
    model=config.model, 
    base_url="https://openrouter.ai/api/v1", 
    api_key=SecretStr(config.api_key)
    )

# Bind the tools to the client
llm = llm.bind_tools(tools)
# Creation of the prompt template
prompt = ChatPromptTemplate.from_messages([
        ("system", "{system_prompt},"),
        ("system", "Relevant memory: {memory}"),
        ("human", "{input}")
    ])

# ------- Memory initialisation ------------------------------------------------

mem = LMIA_context_mini.LMIA_context_mini("./DB.db", INTERACTIVE=True) 

# ---------------- SAVE LOADING -----------------------------------------------------------

dump_file = Path("./dump.json")
if dump_file.is_file():
    with open("./dump.json", "rw") as f:
        save_file_json = json.load(f)
        stage = save_file_json["stage"]
else:
    print("No save file was found. Starting a new conversation.")
    stage = 1
    mem.clear_memory()

# ----------- First time flag declaration -------------------------------------------------

_flag_first_time = True

# Variable decaration
error_action = None
system_prompt = None

# Fun messange
print("[bold][italic][red]Hello, human. Welcome to NullLab-mini chat[/red][/italic][/bold]")

# Main loop
while stage in (1, 2, 3, 4):
    # This is the user input handling
    user_input = input("You: ").strip()
    if user_input.lower() in ("exit", "quit"):
        prev_stage = stage
        error_action = "exit"
    elif user_input.lower == "COMMAND:go_next_stage":
        passed = validate_json_file(stage)
        if passed:
            stage =+ 1
            _flag_first_time = True
        else:
            print("[red] shema verification failed [/red]")

    mem.input_context(user_input, 1) # NOTE: 0 == ai , 1 == user
                                     # NOTE: There is also an enum implemented for that. its called Origin
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
        if system_prompt is None:
            raise RuntimeWarning("System prompt was not set correctly ! ")
        relevant_memory = mem.get_context(user_input)
        response = agent_turn(user_input_for_turn=user_input, system_prompt_for_the_turn=system_prompt, memory=relevant_memory)
        mem.input_context(str(response), 0)
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
                    mem.clear_memory()
                else:
                    print("[red]aborting clearanse. [/red]")
            else:
                print("keeping the memory.")
                _flag_first_time = False    # NOTE: DONT FORGET. 
            system_prompt = config.global_ai_instructions
            system_prompt = system_prompt + """
            Your task is to check if the existing blueprint.json is describing the programm user wants. 
            Question the user about how he wishes the programm to be, and bring up any mismatches with what blueprint.json specifies. 
            """ 
        else:
            pass

        if system_prompt is None:
            raise RuntimeWarning("System prompt was not set correctly ! ")
        relevant_memory = mem.get_context(user_input)
        response = agent_turn(user_input_for_turn=user_input, system_prompt_for_the_turn=system_prompt, memory=relevant_memory)
        mem.input_context(str(response), 0)
        print("[green]AI answers: [/green]")
        print(f"{response}")

    elif stage == 3:
        if _flag_first_time:
            system_prompt = config.global_ai_instructions_for_stage_1_and_3 + """
        Your task is to collaboratively with the user create plan.json , wich must be the specification on how
        to implement blueprint.json. 
        Blueprint.json is complete right now, you must not redact it. 
        Here is a plan.json example:

        {
        "plan": [
            {
                "module_name": "module name here",
                "instruction": "detailed instruction on how to write the module",
                "note": "note here, optionaly"
            }
          ]
        }
        """
            _flag_first_time = False
        else:
            pass
        
        if system_prompt is None:
            raise RuntimeWarning("System prompt was not set correctly ! ")
        relevant_memory = mem.get_context(user_input)
        response = agent_turn(user_input_for_turn=user_input, system_prompt_for_the_turn=system_prompt, memory=relevant_memory)
        mem.input_context(str(response), 0)
        print("[green]AI answers: [/green]")
        print(f"{response}")

    elif stage == 4:
        pass

    # ERROR ACTION handling here. This is kinda the shit that should handle everything. 
    if error_action is not None:
        if error_action == "exit":
            print("[red]shutting down.[/red]")
            print("Would you like to save the progress ?")
            print("[green]Yes[/green] / [red]no[/red]")
            if input(": ").strip().lower() in ("yes", "y", ""):
                save()
            else:
                print("[yellow]are you sure you dont want to save?[/yellow]")
                if input(": ").strip().lower() in ("yes", "y", ""):
                    print("Not saving")
                else:
                    print("saving")
                    save()
