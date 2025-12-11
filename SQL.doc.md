# SQL and sqlite doc

This is my SQL and sqlite doc. Its my referense handbook, 
so I dont forget important stuff. 

Kinda like that. 

## SQL

SQL is the languege used to write querries into Databases. 
Funnily enough, I will be using it to write querries and
commands to my SQLite3 database in python, for my LMIA_context
and LMIA_context_mini plugins

### TYPES INFO

TEXT = str
NULL = None
BLOB = bytes

BLOB is the faster choise for Embeddings, but it must be converted
back and forth. 

Conversion funktions should just be taken from ChatGPT without questions,
since brain capasity for questions is missing. 

### Syntax and keywords

**CREATE TABLE name(shema)**

This is the may to create tables. 

Syntax inside of there is like this:
    
    name TYPE STUFF

**PRIMARY KEY AUTOINCREMENT**   --> means **"create UUID for it, please"**

**TEXT DEFAULT CURRENT_TIMESTAMP** --> means **GET THE CURRENT TIMESTAMP**

### Examples

CREATE TABLE memory(
    UUID PRIMARY KEY AUTOINCREMENT,
    user_prompt TEXT NOT NULL,
    ai_response TEXT,
    embedded_user_prompt BLOB,
    embedded_ai_response BLOB,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
);

