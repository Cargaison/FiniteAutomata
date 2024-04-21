import os
#just a little code to create all the files
folder_path = os.getcwd()

for i in range(20, 30):
    file_name = f"{i}.txt"
    file_path = os.path.join(folder_path, file_name)

    with open(file_path, 'w') as file:
        pass

print(f"44 files have been created in {folder_path}")
