This is a good place to put your python files that you will actually run to do things. These scripts will likely import the functions that you have defined within ~/repo/src. 

For example, let's say you have a program, generate_embeddings.py, that lives in ~/repo/scripts, which takes raw text from papers and feeds them to some model to convert into vector embeddings. The functionality you need to do this will mostly live in files from ~/repo/src, which you can
import into generate_embeddings.py to make use of. This means that generate_embeddings.py won't be cluttered with a bunch of function definitions.
