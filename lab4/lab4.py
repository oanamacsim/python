import os
import sys

def folder_path(director):
    extensions = [];
    try:
        #generating the file names in a directory tree 
        for(root, dirs, file) in os.walk(director):
        #parsing the tree and searching for every extension
            for f in files:
                ext = os.path.splittext(f)[1]
                if ext != "" :
                    extensions += [ext]
    except Exception as e:
        print(str(e))
    finally:
        #returning the extensions in a fixed set that cannot be modified
        return list(set(extensions))

def file_and_folder_path(director, file):
    try:
        with open(file, "w") as f:
            for element in os.listdir(director):
                #method chosen to concatenate the file name with its director
                name = os.path.join(director, element)
                if os.path.isfile(name) and element.startswith("A"):
                 #printing the pathnames of the files from the director, one on a line 
                    print(repr(os.path.abspath(name) + os.linesep))
                    f.write(os.path.abspath(name) + os.linesep)
    except Exception as e:
        print(str(e))

def file_or_folder(my_path):
    # two branches for two possible cases: the path returns a file
    # case two: the path returns a folder
    if os.path.isfile(my_path):
        with open(my_path, "rb") as f:
            #getting the size of the file and verifying if it has at least
            #20 characters in it 
            size = os.path.getsize(my_path)
            assert(size >= 20), "File doesn't have at least 20 characters"
            f.seek(size - 20)
            return f.read()
    elif os.path.isdir(my_path):
        list_of_tuples = {}
        for root, dirs, files in os.walk(my_path):
            for file in files:
                extension = os.path.splittext(file)[1]
                #creating the list of tuples with the extensions 
                if extension in list_of_tuples:
                    list_of_tuples[extension] += 1
                else:
                    list_of_tuples[extension] = 1
        list_of_tuples = list_of_tuples.items()
        return sorted(list_of_tuples, key = lambda el:el[1], reverse = True)
    else:
        raise Exception("Invalid parameter")

def distinct_extensions():
    try:
        #variable to check if we have enough parameters and if we have chosen a valid director chosen 
        ok = False
        if len(sys.argv)>1:
            ok = True
        else: print("Invalid number of parameters")
        if os.path.isdir(sys.argv[1]):
            ok = True
        else: print ("Invalid director")
        if(ok == True): 
            return sorted(list(set([os.path.splitext(el)[1][1:] for el in os.listdir(sys.argv[1]) if os.path.isfile(os.path.join(sys.argv[1],el)) and os.path.splitext(el)[1]!=""])))
    except Exception as e:
        print(str(e))
        return []

def search_tool(target,to_search):
    def file_with_to_search(target, to_search):
        with open(target,"rt") as f:
            text = f.read()
            return to_search in text

    if (os.path.isfile(target)):
        if file_with_to_search(target,to_search):
            return [target]
        else:
            return []
    elif(os.path.isdir(target)):
        result = []
        for root,dirs,files in os.walk(target):
            for f in files:
                name = os.path.join(root,f)
                if file_with_to_search(name,to_search):
                   result+=[name]
        return result
    else:
        raise ValueError("Target needs to be file/directory")

def search_tool_with_callback(target, to_search, callback):
    try:
        return search_tool(target,to_search)
    except Exception as e:
        callback(e)
        return []

def indicators(file):
    try:
        assert(os.path.isfile(file)),"The parameter needs to be a file path"
        return {"full_path":os.path.abspath(file),
                "file_size":os.path.getsize(file),
                "file_extension":os.path.splitext(file)[1],
                "can_read":os.access(file,os.R_OK),
                "can_write":os.access(file,os.W_OK)}
    except Exception as e:
        print(str(e))
        return {}