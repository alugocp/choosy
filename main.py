import random
import json
import math
import sys
import re
CACHE_FILEPATH = "/tmp/choosy.json"
GREEN = "\x1b[32m"
RED = "\x1b[31m"
UNDER = "\x1b[4m"
BOLD = "\x1b[1m"
END = "\x1b[0m"

# Loads cached data from your previous session
def get_cached_data():
    try:
        with open(CACHE_FILEPATH, "r") as cached:
            return json.loads(cached.read())
    except:
        return []

# Saves data for your next session
def save_cached_data(data):
    with open(CACHE_FILEPATH, "w") as cached:
        cached.write(json.dumps(data))

# TUI output logic
def print_choosy(data):
    print(f"Welcome to {BOLD}Choosy{END}! Here are your options:")
    print(f"• {GREEN}+<number>{END}  ->  includes the element at an index")
    print(f"• {GREEN}-<number>{END}  ->  excludes the element at an index")
    print(f"• {GREEN}_<number>{END}  ->  removes an element from the pool")
    print(f"• {GREEN}+<string>{END}  ->  adds an element to the pool")
    print(f"• {GREEN}choose{END}     ->  chooses pairs from the pool")
    print(f"• {GREEN}q{END}          ->  quits Choosy")
    print("")
    print(f"{UNDER}Pool:{END}")
    if len(data) == 0:
        print(f" {RED}Pool is empty{END}")
    for i in range(len(data)):
        label = data[i]["label"]
        state = data[i]["state"]
        print(f"• {i} {GREEN}ON{END} {BOLD}{label}{END}" if state else f"• {i} {RED}OFF{END} {BOLD}{label}{END}")
    print("")
    sys.stdout.write("Command: ")
    sys.stdout.flush()
    return 11 + (1 if len(data) == 0 else len(data))

# Pair assignment logic
def choose(data):
    names = list(map(lambda x: x["label"], filter(lambda x: x["state"] == True, data)))
    print("")
    print(f"{UNDER}Pairings:{END}")
    if len(names) == 0:
        print(f"{RED}No elements for pairing{END}")
        return
    random.shuffle(names)
    num_pairs = math.floor(len(names) / 2)
    if len(names) % 2 == 1:
        num_pairs -= 1
    for i in range(num_pairs):
        print(f"• {GREEN}{names[i * 2]}{END} and {GREEN}{names[(i * 2) + 1]}{END}")
    if len(names) % 2 == 1:
        i = len(names)
        print(f"• {GREEN}{names[i - 3]}{END}, {GREEN}{names[i - 2]}{END}, and {GREEN}{names[i - 1]}{END}")

# Main loop method
def main():
    data = get_cached_data()
    lines = 0
    while True:

        # Clear lines
        if lines > 0:
            sys.stdout.write(f"\x1b[{lines}A\x1b[0J")
            sys.stdout.flush()

        # Prompt for command and process
        lines = print_choosy(data)
        command = input()
        if re.search("^q$", command):
            break
        if re.search("^choose$", command):
            choose(data)
            break
        if re.search("^\+[0-9]+$", command):
            data[int(command[1:])]["state"] = True
            continue
        if re.search("^\-[0-9]+$", command):
            data[int(command[1:])]["state"] = False
            continue
        if re.search("^\_[0-9]+$", command):
            data.pop(int(command[1:]))
            continue
        if re.search("^\+", command):
            data.append({
                "label": command[1:],
                "state": True
            })
            continue

    # Save updated data after the program ends
    save_cached_data(data)

if __name__ == "__main__":
    main()
