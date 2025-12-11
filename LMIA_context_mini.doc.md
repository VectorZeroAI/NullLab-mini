# LMIA context mini doc

This is an LMIA context, version mini, doc.

## PLAN:

The plugin provides LMIA_context_mini class.
The usage is as following:

### input funktion
All the input prompts get inputed into a DB. 
The funktion for inputing is "input_context("prompt", origin)"
explanation:
    origin = type , e.g. 1 or 0, 1 = user, 0 = AI. 

### Output funktion
Output funktion is called get_context("prompt"), and provides relevant context to the prompt. 

*Kepp In mind that it doesnt input the prompt itself, so if you intent to do so, you must do that manualy as well.*

The sorting and finding logic also is located inside that funktion, so dont expect the response to be instant. 
So it may not work correcly with async. 

# Architecture

The architecture is relatively simplistic: 

After the DB is initialised, we treat each **ROW** as an **exchange** 

Each **exchange** is made up by a human prompt, and an AI prompt, e.g. response, whatever. 

*The terminology here doesnt matter.* 

As well as their corresponding transformations and metadata. Each of those goes into its corresponding collum. 
*More on that in the table layout section*

### Table layout

extandable amount of rows, stable amount of collums. 

##### COLLUMS LIST

1. UUID PRIMARY KEY AUTOINCREMENT
2. user_prompt TEXT
3. ai_response TEXT
4. embedded_user_prompt BLOB
5. embedded_ai_response BLOB
6. timestamp TIMESTAMP

### Context retrieval method

The method is clever:

2 most similar user prompts + the AI responses to them + 3 most similar AI responses to each one of those + 5 last messenges. 

The actually numbers should be config tweakable, but I will implement that in the next version. #TODO: IMPLEMENT configurable numbers
