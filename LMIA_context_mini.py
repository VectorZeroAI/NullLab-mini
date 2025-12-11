"""
LMIA context plugin, mini edition
Version 0.1
"""

"""
PLAN: 
    Is located at: 
        ./LMIA_context_mini_doc.md 
"""

# Imports
from pathlib import Path
from sentence_transformers import SentenceTransformer
import sqlite3
import numpy as np

class LMIA_context_mini:

    def __init__(self, DB_path):
        # The DB inialisation
        DB_file = Path(DB_path)

        if DB_file.exists() and DB_file.is_file():
            try:
                self.conn = sqlite3.connect(DB_file)
                self.curr = self.conn.cursor()
            except RuntimeError as e:
                print(f"file found under {DB_path} , but unable to connect to. {e}")
                action = None
                action = input("delete it and reinitialise? Yes means delete and reinitialise the DB, No means aborting execution.")
                if action == "Yes" or action == "Y" or action == "yes" or action == "YES":
                    DB_file.unlink() # This means delete
                    DB_file.touch()
                    self.conn = sqlite3.connect(DB_file)
                    self.curr = self.conn.cursor()
                        
                elif action == "No" or action == "no" or action == "n" or action == "NO":
                    raise RuntimeError("aborting execution")
                else:
                    raise RuntimeError(f"Aborting execution. Invalid action code supplied. Supplied {action}, expected: Yes or No")

        elif DB_file.exists() and not DB_file.is_file():
            print(f"Something under the supplied path was found, but its not a file. Given path = {DB_path} What to do?")
            print("1 = delete whatever there is and create the DB file. ")
            print("0 = abort the execution")
            action = input("Enter action code")
            if action == "1":
                try:
                    DB_file.unlink() # This means delete
                    DB_file.touch()  # This means create
                    self.conn = sqlite3.connect(DB_path)  # This is just connecting
                    self.curr = self.conn.cursor()

                except RuntimeError as e:
                    print("failed. Errors: {e}")
                    raise RuntimeError("FATAL. Aborting execution.")

            elif action == "0":
                raise RuntimeError("Aborting Execution.")
            
            else:
                raise RuntimeError(f"Invalid action code supplied. Supplied {action} , expected 1 or 0")
            
            # This sequense is supposed to establish the connection named conn. 
        
        print("Connection sucsessfullly established.")
        print("magiking the types into understanding. ")

        print("Doing SQL stuff (Assuming the table is there)")


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

        print("Assumed the table is there")
        
        print("initialising sentense transformer")

        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

        print("init state is over")
        
        return True

    def input_context(self, prompt, origin):
        print(f"prompt {prompt} recived")
        print("perofrming SQL operations")

        if origin == 1: 
            self.curr.execute("INSERT INTO memory (user_prompt) VALUES (?)", (prompt,))
            self.embedded_prompt = self.embedder.encode(prompt)  
            self.embedded_prompt = self.embedded_prompt.astype(np.float32).tobytes()
            # The shenanigan above transforms the embedding to bytes, so they can be stored as BLOB in SQLite DB. 
            
            self.curr.execute(""" 
                UPDATE memory
                SET embedded_user_prompt = ?
                WHERE UUID = (SELECT UUID FROM memory WHERE embedded_user_prompt IS NULL ORDER BY UUID DESC LIMIT 1)
                """, (self.embedded_prompt,))
            # COMMIT IS DONE OUTSIDE THE IF STATEMENT
            print("sucsessfully prepared embedding and user prompt into the corresponding places inside the SQLite DB")
        elif origin == 0:
            self.curr.execute(""" 
                UPDATE memory
                SET ai_response = ?
                WHERE UUID = (SELECT UUID FROM memory WHERE ai_response IS NULL ORDER BY UUID DESC LIMIT 1)
                """, (prompt,))
 
            self.embedded_prompt = self.embedder.encode(prompt)  
            self.embedded_prompt = self.embedded_prompt.astype(np.float32).tobytes()
            # The shenanigan above transforms the embedding to bytes, so they can be stored as BLOB in SQLite DB. 
            
            self.curr.execute(""" 
                UPDATE memory
                SET embedded_ai_response = ?
                WHERE UUID = (SELECT UUID FROM memory WHERE embedded_ai_response IS NULL ORDER BY UUID DESC LIMIT 1)
                """, (self.embedded_prompt,))
 
            print("sucsessfully prepared embedding and ai response into the corresponding places inside the SQLite DB")
 
        else:
            raise RuntimeError(f"YOU ARE AN IDIOT! INVALID origin. Expected values are 1 or 0, got value {origin}")
        
        self.conn.commit()
        
        print("sucsessfully inputed the data.")

    def get_context(self, prompt):
        pass
        # This is supposed to be the funktion for getting the context
        # This is where the core logic of the programm is located at. 
        # TODO: FINISH THIS


