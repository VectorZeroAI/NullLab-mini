# LMIA context mini doc

This is an LMIA context, version mini, doc.

## PLAN:

The plugin provides LMIA_context_mini class.
The usage of the class is as following:

### Instanse creation: 

Each instanse requires defining 3 parameters for it to work with. 
1. DB_path , wich is a string defining the DB path. Defaults to ./DB.db if not specified.
2. interactive, wich is a bool, defining wether interactive behaviour is allowed or not. (e.g. interactive error handling)
3. logs , wich is a bool, defining wether log like print statements are to be outputed or not. 

Both 2 and 3 default to False. 

The instanse doesnt need anything specified, but this is the amount of parameters it offeres. 

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

### clear memory function

The clear memory function is called clear_memory() , and it just cleares the DB, and catches errors. 

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

The actually numbers should be config tweakable, but I will implement that in the next version. 
#TODO: IMPLEMENT configurable numbers

#### The actual funktion architecture:
Execution audict (for future me to understand the fuck its doing)
1. Check if these are enough inputs in the database, if yes, prossed, if no, return everything. 
2. First, fetch all the embedded_user_prompt BLOB
3. Then convert them to proper numpy arrays. **Important** Dont fuck up the order.
4. Then define the similarity_list, that is used to gather all the similarities. **Important**: DONT OVERWRITE THE ORIGINAL LIST, else there is no way in hell to know from wich ROW the embedding was from.
5. The loop through the list of the fetched user prompt embeddings to get similarity, and append every similarity to the similarity_list.
6. Then get the 2 biggest embeddings out of the list
7. Then get their row numbers via .index.
8. Then we get the corresponding ai responses. 
9. Then per each ai response similar responses. 
10. Then we get the last 5 exchanges via ordering by Timestamp. 

Thats basicaly it. 
I compressed the logic, because its pretty much self explanatory if we look at the code. 
Its basicaly the same thing as in the first half, just over new set of data. 
With some creativity, you could even abstract the thing into a function that can be called twice, although that is not a practical solution. 
