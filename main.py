import csv
import json
import random

STATE_SIZE = 2

def build_model(names):
    model = {}
    for name in names:
        for i in range(STATE_SIZE, len(name)):
            current_char = name[i]
            previous_chars = name[i-STATE_SIZE:i]

            # add entry
            if previous_chars in model:
                model[previous_chars].append(current_char)
            else:
                model[previous_chars] = [current_char]
            
            # also add entry for the end-of-name symbol (#)
            if i == len(name)-1:
                previous_chars = name[i-STATE_SIZE+1:i+1]
                current_char = "#"
                
                if previous_chars in model:
                    model[previous_chars].append(current_char)
                else:
                    model[previous_chars] = [current_char]

    return model

def generate(model, start):
    result = start

    while result[len(result)-1] != "#":
        previous_chars = result[-STATE_SIZE:]
        
        if previous_chars in model:
            result += random.choice(model[previous_chars])
        else:
            result += "#"
    
    # Remove last char (which is always #)
    return result[:len(result)-1]
        


print("Loading data...")

names = []
with open("us-names-by-year.csv", "r") as file:
    reader = csv.reader(file)
    next(reader) # skip first row
    for row in reader:
        names.append(row[1])

with open('names.json', 'w') as f:
    json.dump(names, f, ensure_ascii=False, indent=4)

print("Done!")


print("Building model...")

model = build_model(names)

with open('model.json', 'w') as f:
    json.dump(model, f, ensure_ascii=False, indent=4)

print("Done!")


while True:
    start = input("Enter start of name: ")
    print(f"Generated name: {generate(model, start)}")
