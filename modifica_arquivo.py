import shutil

original = r'MAT.txt'
file_path = r'SecMAT.txt' 
shutil.copyfile(original, file_path)

match_string = "Daniel"
insert_string = "//"
with open(file_path, 'r+') as fd:
    contents = fd.readlines()
    if match_string in contents[-1]:  # Handle last line to prevent IndexError
        contents.append(insert_string)
    else:
        for index, line in enumerate(contents):
            print(index)
            if match_string in line and insert_string not in contents[index + 1]:
                contents.insert(index , insert_string)
                break
    fd.seek(0)
    fd.writelines(contents)
    fd.close()
