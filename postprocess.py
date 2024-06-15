
import pandas as pd
from datetime import datetime
import json

def filter_lines(lines):
    start_index = None
    end_index = None

    # Find start and end indices
    for i, line in enumerate(lines):
        if "INCOME TAX DEPARTMENT" in line:
            start_index = i
        if "Signature" in line:
            end_index = i
            break

    # Filter lines based on conditions
    filtered_lines = []
    if start_index is not None and end_index is not None:
        for line in lines[start_index:end_index + 1]:
            if len(line.strip()) > 2:
                filtered_lines.append(line.strip())
    
    return filtered_lines

def create_dataframe(texts):

    lines = filter_lines(texts)
    print("="*20)
    print(lines)
    print("="*20)
    data = []
    name = lines[2].strip()
    father_name = lines[3].strip()
    dob = lines[4].strip()
    for i in range(len(lines)):
        if "Permanent Account Number" in lines[i]:
            pan = lines[i+1].strip()
    data.append({"ID": pan, "Name": name, "Father's Name": father_name, "DOB": dob, "ID Type": "PAN"})
    df = pd.DataFrame(data)
    return df

def extract_information(data_string):
    # Split the data string into a list of words based on "|"
    updated_data_string = data_string.replace(".", "")
    words = [word.strip() for word in updated_data_string.split("|") if len(word.strip()) > 2]

    # Initialize the dictionary to store the extracted information
    extracted_info = {
        "ID": "",
        "Name": "",
        "Father's Name": "",
        "DOB": "",
        "ID Type": "PAN"
    }

    try:
        name_index = words.index("GOVT OF INDIA") + 1
        extracted_info["Name"] = words[name_index]

        fathers_name_index = name_index + 1
        extracted_info["Father's Name"] = words[fathers_name_index]

        id_number_index = words.index("Permanent Account Number") + 1
        extracted_info["ID"] = words[id_number_index]

        dob_index = None
        for i, word in enumerate(words):
            try:
                datetime.strptime(word, "%d/%m/%Y")
                dob_index = i
                break
            except ValueError:
                continue

        if dob_index is not None:
            extracted_info["DOB"] = datetime.strptime(words[dob_index], "%d/%m/%Y")
        else:
            print("Error: Date of birth not found.")
    except ValueError:
        print("Error: Some required information is missing or incorrectly formatted.")

    return extracted_info