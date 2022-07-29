from tkinter import messagebox
import threading

from pyxel import icon


items = {
        'tools':{
        1:{'is_weapon':False, 'item':'Magnifying glass'},
        2:{'is_weapon':False, 'item':'Binochulars'},
        3:{'is_weapon':True, 'item':'Screwdriver', 'pen':0, 'dmg':5},
        4:{'is_weapon':True, 'item':'Crowbar', 'pen':0, 'dmg':10},
        5:{'is_weapon':False, 'item':'Wrench'},
        6:{'is_weapon':True, 'item':'Hammer', 'pen':0, 'dmg':10}
    },
    'weapons':{}
    }


def start_thread(function):
    th = threading.Thread(target=function)
    th.start()


def error_msg(error_num: str):
    match error_num:
        case '00':
            messagebox.showinfo('feature not implemented, ERROR:00', 'Sorry, this feature has not been programed in yet')
        case '01':
            messagebox.showerror('MEMORY ERROR, ERROR:01', """
Unknown Memory Error, the database could be lost or damaged, or the config file could've been tampered with.


Why tampereing with the config file can cause this: The config file holds the character_id for the next character,
and changing that number could interact with another character due to the id's being the same.
When you create a new character the id from the config is given to that new character.
After that new character is created, the program adds 1 to the id.

HOW TO FIX IF THE CONFIG IS TAMPERED WITH:
Step 1: Get some sort of sqlite database manager (If you tampered with it you probably already have one) 
Step 2: Look for the table with the largest number in the name.
Step 3: After that, go and find the config elsewhere in the database and change non_ui_char_num to the number you found in step 2 but add 1 too it.

If you tampered with the config, I can't really blame you. You probably decided to toy around with things just to see what would happen.
But just know that tampering with the config doesn't give you anything cool. I can't say the same about the inventory ;)
            """)
        case '02':
            messagebox.showinfo('MEMORY ERROR, ERROR:02', '''
            This character has no world saves. 
            To create one, follow this path: Create > create new world''')
        case '03':
            messagebox.showwarning("No character", '')
        case '04':
            messagebox.showwarning('UNDECIED, ERROR:04', """
There are two possiblities as why you are seeing this:
1) The feature you are trying to access may not be decided apon yet (you will get a ERROR:00 if that feature is likely to make the cut)
2) The feature you are trying to access may be under review, and possiblely removed later
            """)
        case '05':
            messagebox.showinfo('End reached', "I am so sorry to inform you that this is the end of the story so far, play again when a new update is out")


def send_info(title: str, message: str):
    messagebox.showinfo(title, message)

def send_warning(title: str, message: str):
    messagebox.showwarning(title, message)

def send_error(title: str, message: str):
    messagebox.showerror(title, message)

def item_look_up(item_id: int, item_type: str):
    x = items[item_type]
    y = x[item_id]
    return y




if __name__ == '__main__':
    # use for testing functions
    print(item_look_up(4, 'tools'))

