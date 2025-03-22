import os
import shutil
def empty_then_copy():
    source = "../static"
    destination = "../public"
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    copyDirectory(source, destination)
    

def copyDirectory(source,destination):
    if not os.path.exists(destination):
        os.mkdir(destination)
    for item in os.listdir(source):
        source_path = os.path.join(source,item)
        dest_path = os.path.join(destination,item)

        if os.path.isfile(source_path):
            shutil.copy(source_path,dest_path)
        else:
            copyDirectory(source_path, dest_path)

        