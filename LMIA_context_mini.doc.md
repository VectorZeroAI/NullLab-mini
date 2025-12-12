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
<<<<<<< HEAD
4. embedded_user_prompt BLOB
5. embedded_ai_response BLOB
6. timestamp TIMESTAMP
=======
4. embedded_user_prompt *whatever the fuck the embedding is*
5. embedded_ai_response *whatever the fuck the embedding is*
6. timestamp TIMESTAMP *or however its actually called.*
>>>>>>> 972256a4674e34a92813b35f16fc8494725c7a25

### Context retrieval method

The method is clever:

2 most similar user prompts + the AI responses to them + 3 most similar AI responses to each one of those + 5 last messenges. 

The actually numbers should be config tweakable, but I will implement that in the next version. #TODO: IMPLEMENT configurable numbers
<<<<<<< HEAD

#### The actual funktion architecture:
Execution audict (for future me to understand the fuck its doing)
1. First, fetch all the embedded_user_prompt BLOBs
2. Then convert them to proper numpy arrays. **Important** Dont fuck up the order.
3. Then define the similarity_list, that is used to gather all the similarities. **Important**: DONT OVERWRITE THE ORIGINAL LIST, else there is no way in hell to know from wich ROW the embedding was from.
4. The loop through the list of the fetched user prompt embeddings to get similarity, and append every similarity to the similarity_list.
5. Then get the biggest embedding out of the list. 
=======
>>>>>>> 972256a4674e34a92813b35f16fc8494725c7a25
