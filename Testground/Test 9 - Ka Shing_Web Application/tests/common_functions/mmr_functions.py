# MMR functions for tests

# === Imports ===
from werkzeug.datastructures import FileStorage
from mmr import MMRFile

def instantiate_mmr_file_from_path(file): 
    with open(file, mode="rb") as fb:
        return MMRFile(FileStorage(fb)) 


def instantiate_mmr_files(files): 
    return [instantiate_mmr_file_from_path(f) for f in files]
