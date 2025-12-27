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

from os import system
from pydantic import SecretStr
from rich import print

print("[green]Colors initiated. =)[/green]")

import requests
import sys
import LMIA_context_mini
import config
import json

print("[green]basic initialisation completed. [/green]")
print("[green]initialising langchain agent.[/green]")

from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.json.toolkit import JsonToolkit
from langchain_community.tools.json.tool import JsonSpec
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
# from langchain_community.agent_toolkits.json.base import create_json_agent

print("[green]Everything else initialised[/green]")
# -- Langchain agent creation! ---------------------------------------------------------------

# Json loading
try:
    global data_blueprint
    data_blueprint = json.load(open("blueprint.json"))
except Exception as e:
    print("[red] ERROR: DIDNT FIND blueprint.json file. [/red]")
    print(f"For debug purpuses: Error is: {e}")
    print("[red]creating an empty blueprint.json file.[/red]")
    from pathlib import Path
    bluep = Path("./blueprint.json")
    bluep.touch()
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
        ("system", "{system_prompt}"),
        ("memory", "{memory}"),
        ("human", "{input}")
    ])

print("[bold][italic][red]Hello, human. Welcome to NullLab-mini chat[/red][/italic][/bold]")

print("defining funktions")

def agent_turn(user_input_for_turn, system_prompt_for_the_turn, memory):
    messange = prompt.invoke({"input": user_input_for_turn, "system_prompt": system_prompt_for_the_turn, "memory": memory}).to_messages()

    while True:
        AIMessage = llm.invoke(messange)
        messange.append(AIMessage)

        if not AIMessage.tool_calls:
            return AIMessage.content
        
        for call in AIMessage.tool_calls:
            tool = tools_by_name[call["name"]]
            result = tool.invoke(call["args"])

            messange.append(ToolMessage(content=str(result), tool_call_id=call["id"]))
            

api_url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
        "Authorization": f"Bearer {config.api_key}",
        "Content-Type": "application/json"
    }

stage = 1
mem = LMIA_context_mini.LMIA_context_mini(DB_path="./DB.db") # Memory initialisation

# Variable mess.
error_action = None

# Main loop
while stage in (1, 2, 3, 4):
    # This is the user input handling
    user_input = input("You: ").strip()
    if user_input.lower() in ("exit", "quit"):
        prev_stage = stage
        error_action = "exit"
    mem.input_context(user_input, 1) # NOTE: 0 == ai , 1 == user

    # This is the response handling
    if stage == 1:
        system_prompt = f"""
        You are NullLab-mini AI. 
        You are an AI assistant.
        You must assist the user in creating Blueprint.json
        You are to cooperate and listen to the user. 
        You are to follow the users orders
        {config.allowance}
        """ # TODO: FIXME
        relevant_memory = mem.get_context(user_input)
        response = agent_turn(user_input_for_turn=user_input, system_prompt_for_the_turn=system_prompt, memory=relevant_memory)
        mem.input_context(response, 0)
        print("[green]AI answers: [/green]")
        print(f"{response}")


    elif stage == 2:
        pass
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
