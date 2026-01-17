#!/usr/bin/env python3
"""
LMIA context plugin, mini edition
Version 0.2
"""
from enum import IntEnum
from pathlib import Path
from sentence_transformers import SentenceTransformer
import sqlite3
import numpy as np
import heapq
from rich import print

print("imports finished with no errors. ")

class Origin:
    AI = 0
    USER = 1

class LMIA_context_mini:
    """
    The main plugin class.
    required input values for instanse creation : DB_path: str , interactive: bool

    DB_path is the path to the DB file.
    interactive is bool telling wether the enviroment of execution is interactive or not. 
    Setting to true may allow for interactive error handling, while setting to False removes those. 
    """
    def __init__(self, DB_PATH: str | None = None, INTERACTIVE: bool | None = None, LOGS: bool | None = None):
        """
    Instanse constructor. 
    I will use it as one.
    All the instanse creation logic is consentrated here. 
        """
        # Helper function
        def log_print(text: str):
            """
            Prints if logs is true
            """
            if LOGS:
                print(text)
            else:
                return
        # Default values.
        if DB_PATH is None:
            DB_PATH = "./DB.db"
        if INTERACTIVE is None:
            INTERACTIVE = False
        if LOGS is None:
            LOGS = False
                    
        DB_file = Path(DB_PATH)

        self.interactive = INTERACTIVE
        self.logs = LOGS

        if DB_file.is_file():
            try:
                self.conn = sqlite3.connect(DB_file)
                self.curr = self.conn.cursor()
            except sqlite3.Error as e:
                log_print(text=f"file found under {DB_PATH} , but unable to connect to. {e}")
                if self.interactive:
                    action = input("delete it and reinitialise? Yes means delete and reinitialise the DB, No means aborting execution.")
                    action = action.lower().strip()
                    if action == "yes" or action == "y":
                        DB_file.unlink() # This means delete
                        DB_file.touch()
                        self.conn = sqlite3.connect(DB_file)
                        self.curr = self.conn.cursor()
                            
                    elif action == "No" or action == "no" or action == "n" or action == "NO":
                        raise RuntimeError("aborting execution")
                    else:
                        raise RuntimeError(f"Aborting execution. Invalid action code supplied. Supplied {action}, expected: Yes or No")
                else:
                    raise RuntimeWarning(f"Unable to connect to data base file under given path. given path {DB_PATH}")

        elif DB_file.exists() and not DB_file.is_file():
            if self.interactive:
                print(f"Something under the supplied path was found, but its not a file. Given path = {DB_PATH} What to do?")
                print("1 = delete whatever there is and create the DB file. ")
                print("0 = abort the execution")
                action = input("Enter action code")
                if action == "1":
                    try:
                        DB_file.unlink() # This means delete
                        DB_file.touch()  # This means create
                        self.conn = sqlite3.connect(DB_PATH)  # This is just connecting
                        self.curr = self.conn.cursor()

                    except OSError as e:
                        print(f"failed. Errors: {e}")
                        raise RuntimeError("FATAL. Aborting execution.")

                elif action == "0":
                    raise RuntimeError("Aborting Execution.")
                
                else:
                    raise RuntimeError(f"Invalid action code supplied. Supplied {action} , expected 1 or 0")
                
                # This sequense is supposed to establish the connection named conn. 
            else:
                raise RuntimeError("The given path is not a connectable file. ")
        
        log_print("Connection sucsessfullly established.")

        self.curr.execute("""CREATE TABLE IF NOT EXISTS memory(
              UUID INTEGER PRIMARY KEY AUTOINCREMENT,
              user_prompt TEXT NOT NULL,
              ai_response TEXT,
              embedded_user_prompt BLOB,
              embedded_ai_response BLOB,
              timestamp TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                          """) 

        self.conn.commit()

        log_print("Assumed the table is there")
        
        log_print("initialising sentense transformer")

        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

        log_print("[green]construction of the class completed with.[/green]")

    def input_context(self, prompt: str, origin: int | IntEnum):
        """
    The method to input content into the memory. 
    prompt is the content to input. 
    There is a class Origin, whose parameters AI and USER correspond to the USER and AI Origins. 
    So you can write Origin.AI or Origin.USER , or just 0 or 1. 
    AI = 0
    USER = 1
        """
        USER: int = 1
        AI: int = 0
        def log_print(text: str):
            """
            Prints if logs is true
            """
            if self.logs:
                print(text)
            else:
                return

        log_print(f"prompt {prompt} recived")

        log_print("perofrming SQL operations")

        if origin == USER: 
            self.curr.execute("INSERT INTO memory (user_prompt) VALUES (?)", (prompt,))
            self.embedded_prompt = self.embedder.encode(prompt, normalize_embeddings=True)  
            self.embedded_prompt = self.embedded_prompt.astype(np.float32).tobytes()
            # The shenanigan above transforms the embedding to bytes, so they can be stored as BLOB in SQLite DB. 
            
            self.conn.commit()
            self.curr.execute(""" 
                UPDATE memory
                SET embedded_user_prompt = ?
                WHERE UUID = (SELECT UUID FROM memory WHERE embedded_user_prompt IS NULL ORDER BY UUID DESC LIMIT 1)
                """, (self.embedded_prompt,))
            # COMMIT IS DONE OUTSIDE THE IF STATEMENT
            log_print("successfully prepared embedding and user prompt into the corresponding places inside the SQLite DB")
        elif origin == AI:
            self.curr.execute(""" 
                UPDATE memory
                SET ai_response = ?
                WHERE UUID = (SELECT UUID FROM memory WHERE ai_response IS NULL ORDER BY UUID DESC LIMIT 1)
                """, (prompt,))
            
            self.conn.commit()
            self.embedded_prompt = self.embedder.encode(prompt, normalize_embeddings=True)  
            self.embedded_prompt = self.embedded_prompt.astype(np.float32).tobytes()
            # The shenanigan above transforms the embedding to bytes, so they can be stored as BLOB in SQLite DB. 
            
            self.curr.execute(""" 
                UPDATE memory
                SET embedded_ai_response = ?
                WHERE UUID = (SELECT UUID FROM memory WHERE embedded_ai_response IS NULL ORDER BY UUID DESC LIMIT 1)
                """, (self.embedded_prompt,))
                    
            log_print("sucsessfully prepared embedding and ai response into the corresponding places inside the SQLite DB")
        else:
            raise RuntimeError(f"INVALID origin. Expected values are 1 or 0, got value {origin}")
            
        self.conn.commit()
            
        log_print("sucsessfully inputed the data.")

    def get_context(self, prompt) -> str:
        """
    THe method to retrieve context from the memory. 
    prompt is the user prompt that would be used to querrie the database. 
        """
        def log_print(text: str):
            """
            Prints if logs is true
            """
            if self.logs:
                print(text)
            else:
                return
        # First, check if there are enough messenges to work with. Min = 5
        fetch_variable = self.curr.execute("""
            SELECT UUID FROM memory ORDER BY UUID DESC LIMIT 1
        """).fetchone()
        if fetch_variable[0] < 5:
            fetch_variable = self.curr.execute("""
                SELECT user_prompt, ai_response FROM memory
            """).fetchall()
            everything = fetch_variable

            return f"{everything}"
        else:
            pass # Continue on with the normal work

        embedded_prompt_to_compare_to = self.embedder.encode(prompt, normalize_embeddings=True)
        binary_list_of_user_prompt_embeddings = self.curr.execute("""
            SELECT embedded_user_prompt FROM memory;
        """).fetchall()
        # A list to track similarity. 
        embeddings_list = []
        similarity_list = []

        # The iteration through every row.
        for binary in binary_list_of_user_prompt_embeddings:
            embedded_user_prompt = np.frombuffer(binary[0], dtype=np.float32)
            embeddings_list.append(embedded_user_prompt)
            # np.frombuffer(blob, dtype=np.float32)
            # This funktion is the converter from BLOB to numpy. !IMPORTANT
        # This piece of code creates the list of embeddings, not binaries. The order is the same. The order is important.

        for emb in embeddings_list:
            sim = np.dot(embedded_prompt_to_compare_to, emb)
            similarity_list.append(sim)

        # This piece of code just calculates the similarity of each element, and appends it to a list. 
        # The order is the same. 

        most_similar_user_prompts = heapq.nlargest(2, similarity_list)
        """
        Now we have 2 lists, the embeddings_list, the similarity_list, and the binary_list . 
        We need to find the row, e.g. the index number of the 2_most_similar_user_prompt s in the list. 
        Because the order was never changed, the index inside similarity_list = index in binary_list, wich = the row number, + - 1, due to starts on 1 or 0. 
        This way, we get the corresponding rows from inside SQLite. 
        This is half the job of creating the output done. 
        """
        row_numbers = []
        for i in most_similar_user_prompts:
            # It doesnt matter if a different row that is equaly similar is selected, since we need similar rows, and not SPECIFIC similar rows, so ... doesnt matter =)
            row_numbers.append(similarity_list.index(i) + 1)        # +1 , because SQLite is 1 based, and lists are 0 based. 
        """
        Now that we have the index nummer, we can grab the row from the SQLite DB, and prossed with the the output creaation. 
        """
        final_2_most_similar_user_prompts = []
        for row in row_numbers:
            get_stuff = self.curr.execute(f"""
            SELECT user_prompt FROM memory WHERE UUID = {row}
            """).fetchone() # This is a tuple of 1 element
            final_2_most_similar_user_prompts.append(get_stuff[0]) # this is the element itself. 
        """
        Now, we have gotten 2 most similar user prompts, with their row numbers. 
        Now we can proseed to getting the ai_responses for the similar user prompts. 
        """
        log_print("first branch is over. Beginning second branch")
        """
        This is the beggining of the second branch. 
        """
        corresponding_ai_responses = []
        for row in row_numbers:
            fetch_variable = self.curr.execute(f"""
            SELECT ai_response FROM memory WHERE UUID = {row}
            """).fetchall()
            corresponding_ai_responses.append(fetch_variable[0][0])
        # Now we have the corresponding ai responses. 
        # Now we can grab similar responses to them, and be happpy.
        """
        Now we make the loop that would output the similar AI responses from the past. 
        Output format: variable "similar_ai_responses"
        """
        embedded_ai_responses = []
        for row in row_numbers:
            fetch_variable = self.curr.execute(f"""
            SELECT embedded_ai_response FROM memory WHERE UUID = {row}
            """).fetchall()
            intermediate = np.frombuffer(fetch_variable[0][0], dtype=np.float32) # Coversion from BLOB to numpy array.
            embedded_ai_responses.append(intermediate)
            # This puts the corresponding ai responses to the 2 most similar user prompts into the list 
            # named embedded_ai_responses

        fetch_variable = self.curr.execute(f"""
        SELECT embedded_ai_response FROM memory WHERE UUID != {row_numbers[0]} AND UUID != {row_numbers[1]}
        """).fetchall() 
        # This here gets all the embedded ai responses, excluding the AI responses that they are gonna be compared to. 

        similarity_list = [] # This list is the list of lists that I am gonna be using to store the comarason results

        for emb in embedded_ai_responses:    # for each of the corresponsding ai_responses to the 2 most similar user promots:

            embeddings_list = []

            for binary in fetch_variable:
                intermediate = np.frombuffer(binary[0], dtype=np.float32)    # Conversion
                embeddings_list.append(intermediate)                            # Conversion from BLOB to np.array
            
            inter_list = []      

            for embedding in embeddings_list:       # For each of the ai_responses, excluding the ... the ones in the comment just on top of this one. 

                similarity = np.dot(emb, embedding)   # Compute similarity
                inter_list.append(similarity)   # Append similarity to the internal list

            similarity_list.append(inter_list)  # And once its done, append the internal list to the similarity list. 
            """
            This makes a double for loop, wich returns a list of lists called similarity_list, wich we can later on loop through to compare the embeddings 
            """
        """
        This is the second branch of search, wich pulls in 5 most ai_respons'es to the previous user prompts similar to the quesrry prompt
        wich puts this part as the second branch. 
        """
        indexes_of_similar_ai_responses = [] # This is a list of lists, of the indexes of the similar user embeddings. 
        for sim_list in similarity_list:
            top_sim_items_5 = heapq.nlargest(5, sim_list)
            intermediate = []
            for i in top_sim_items_5:
                index = sim_list.index(i)  
                intermediate.append(index + 1)   # Now this is correct. 
            indexes_of_similar_ai_responses.append(intermediate)

        similar_ai_responses = []

        for index_list in indexes_of_similar_ai_responses:
            for index in index_list:
                element = self.curr.execute(f"""
            SELECT ai_response FROM memory WHERE UUID = {index}
                """).fetchall()
                similar_ai_responses.append(element[0][0])
        """
        Branch 2 over.
        """
        log_print("branch 2 over.")
        """
        Out of branch 1: last 5 messegnes by TIMESTAMP
        """
        last_5_messenges = self.curr.execute("""
            SELECT user_prompt, ai_response FROM memory ORDER BY timestamp DESC LIMIT 5;
                                             """).fetchall()
        return f"{final_2_most_similar_user_prompts}, {corresponding_ai_responses}, {similar_ai_responses}, {last_5_messenges}"


    def __db_deletion_funk__(self):
        """
    Helper function of the clear memory method, and an abstraction. 
    Deletes everything from the DB. 
    Direct use is not recommended, usage of the clear_memory method is recommeneded
        """
        def log_print(text: str):
            """
            Prints if logs is true
            """
            if self.logs:
                print(text)
            else:
                return

        try:
            self.curr.execute("""
            DELETE * FROM memory
            """)
            self.conn.commit()
        except RuntimeError as e:
            log_print(f"The following error occured: {e}")
            log_print("[red] DELETION FAILED [/red]")
            raise RuntimeWarning("DELETION FAILED") from e


    def clear_memory(self) -> bool:
        """
    Method for clearing the memory DB. Clears the Database. Doesnt clear the variables. 
    Traling variables may still be there. To remove them, restart the programm. 
        """
        def log_print(text: str):
            """
            Prints if logs is true
            """
            if self.logs:
                print(text)
            else:
                return

        if self.interactive:
            print("[red] Are you sure you want to errase the memory ? [/red]")
            print("[red][bold] ITS IRREVERSABLE [/bold][/red]")
            answer = input("configration (Y/N) : ").lower().strip()
            if answer in ("y", "yes"):
                self.__db_deletion_funk__()
            else:
                print("aborting deletion")
        else:
            log_print("initiating deletion without requiring confirmation due to non interactivity of the execution enviroment. ")
            self.__db_deletion_funk__()
        return True
            
