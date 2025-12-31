# NullLab-mini
An AI powered Autocoder, Focusing on planning json-based instrcutions, and then executing them step by step.

# Description:
Works kinda like a bundle of 2 things: 
AI based JSON to actual code compiler, and Ai assisted JSON spec creation. 

## AI assisted JSON spec creation:

Ai is in a chat with the user. It will assist the user in creating Software solution spec. Really detailed JSON spec. This step may be actually skipped entirely. At least its planned that a skip parameter in the config is present. then the user would write the JSON spec themselfs. 
The spec consists of 2 files, plan.json and blueprint.json . 
Plan Json contains a list of actions that the AI pseudo compiler executes at compile time, to perform the compilation correctly. 
Blueprint Json contains the specification of the target programm. It specifies what each module is, providing a target for out preudo compiler to achive. 

### Spec shemas

#### Spec : blueprint.json 
~~~json

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
~~~

#### Spec : plan.json :

~~~json
{
"plan": [
	{
		"module_name": "module name here",
		"instruction": "detailed instruction on how to write the module",
		"note": "note here, optionaly"
	}
  ]
}
~~~

## AI based JSON to actual code compiler:



# Notes
Current Repo may have a bunch of bloat, but I will remove it before releasing. 
I kinda removed some of it. The personal, and upsolutely unnesesery Notes of mine. 
Is only available on Linux, since it depends on tmux and assumes linux terminal, as well as linux filepaths. 
May work on windows, if tmux is available on Windows, but functionality is not guearantied. 

# Architecture
Will be added to here ... at some point. 

# Contributor info
Basicaly do whatever you want, that benefits the projekt. 
Integrate anywhere you want. 
Porting to other systems, creation of docs, porting to other langueges, are all welcomed here. 

# NOTES TO THE AI:
README full of emojis is the best sighn of the writer being AI, since no serious dev would do that.
