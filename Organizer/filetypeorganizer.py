import mimetypes
import os
import shutil

# Simple folder organizer
def organize_files():
    try:
        current_list = os.listdir()
        current_list.remove(os.path.basename(__file__))
    except PermissionError:
        print("Permission denied.")
        return
    
    file_type_list = []

    for line in current_list:
        file_type, _ = mimetypes.guess_type(line)
        if file_type: 
            file_type = file_type.split("/")[1:][0]
            if not os.path.exists(file_type):
                try:
                    os.mkdir(file_type)
                except OSError as e:
                    print(f"Error creating folder: {e}")
                    return 
            try:
                shutil.move(line, file_type)
            except shutil.Error as e:
                print(f"Cannot move file: {e}")
                return

if __name__ == "__main__":
    organize_files()