import os

# Directory where the files will be created
folder_path = os.getcwd()

# Loop to create files from automata1.txt to automata44.txt
for i in range(20, 30):
    file_name = f"{i}.txt"
    file_path = os.path.join(folder_path, file_name)

    # Create the file and close it
    with open(file_path, 'w') as file:
        pass  # The 'pass' statement is used here to indicate an empty block

print(f"44 files have been created in {folder_path}")
