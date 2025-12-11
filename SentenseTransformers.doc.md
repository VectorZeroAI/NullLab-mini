# Sentense transformer library DOC. 

first off, we import the library like this: 

**from sentense_transformers import SentenseTransformer**

Then we load a model, e.g. :

**model = SentenseTransformer("all-MiniLM-L6-v2")**

Now we can call the model, objekt, created via the model loading line, 
to embedd text. 

**embedding = model.encode(text)**

text may be a variable with value type str, or str. 

****

A better name for the objekt is ***embedder***

# call examples

These will look like that: 

**embedder = SentenseTransformer("all-MiniLM-L6-v2")**

**embedder.encode(text)**
**embedder.encode("text")**
