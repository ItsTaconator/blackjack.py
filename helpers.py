import os

def clear():
    """
    Platform independent terminal clear(er)
    """
    os.system("cls" if os.name == "nt" else "clear")


def confirm(prompt: str = "\nAre you sure?", error: str = "\nPlease enter yes/y, no/n, or 1 or 2.", draw_options: bool = True) -> bool:
    """
    Gets a user's confirmation for something

    prompt (str): Prompt shown when asking for input
    error (str): Error shown when user enters invalid value
    draw_options (bool): Whether to draw the available options to the user automatically
    """
    res = ""
    while res == "" or not "yes".startswith(res) and not "no".startswith(res) and res != '1' and res != '2':
        if res != "":
            print(error)

        print(prompt)
        if draw_options:
            print("1: (Y)es\n2: (N)o")

        res = input().lower()

    return "yes".startswith(res) or res == "1"

def input_num(prompt: str = "Please enter a number.\n", error: str = "Invalid input. Please try again.\n", bounds: range = None) -> int:
    """
    Like input(), but it only wants a number

    prompt (str): Prompt shown whenever asking user for input
    error (str): Error shown whenever user enters invalid value
    bounds (range): Allowed range for input number, if set to None, it can be any integer
    """
    num = ""
    while not num.isnumeric() or bounds is not None and int(num) not in bounds:
        if num != "":
            print(error)
        
        num = input(prompt)
    
    return int(num)

def center_many(*args, width: int = 30) -> str:
    """
    Centers an unlimited amount of strings
    """
    out = ""
    for arg in args:
        out += '\n' + f"{arg}".center(width)

    return out[1:]
