import time
from tkinter import *
from utilz import error_msg, send_warning, start_thread
from execute_hub import exec_script
import sqlite3
__conn = sqlite3.connect('Text journey database.db')
__curs = __conn.cursor()

a_num = 0

enable_next = False

next = ''

droot = Tk()



if __name__ != '__main__':
    from comm1 import back_color, autosave, auto_save, for_chpt, txt__color
    droot.config(bg='black')
    _info_lable_to_user = Label(droot, text="""
    DO NOT CLOSE: The game will be summoned here when ready
    
    If you close this window, whether the game has started or not, 
    this window cannot come back. 
    And you will have to restart the program.
    """, fg='red', bg='black')
    _info_lable_to_user.grid(column=0, row=0)
    # send_warning('Game engine window started', 'Please do not close the Game Engine window')



droot.title('Game Engine')
# droot.geometry('400x300')

_frame_gametext = LabelFrame(droot, text='Storyline')
__frame_opt = LabelFrame(droot, text='Choices')
_label = Label(_frame_gametext, text='', bg=back_color, fg=txt__color)
_label_ = Label(__frame_opt, text='Empty string', bg=back_color, fg=txt__color)

btn_a = Button(__frame_opt, text='')
btn_b = Button(__frame_opt, text='')
btn_c = Button(__frame_opt, text='')
btn_d = Button(__frame_opt, text='')
btn_e = Button(__frame_opt, text='')

def load_wrld():
    tk__var__0 = StringVar()
    aroot = Toplevel(droot)
    aroot.title('Load World')
    aroot.config(bg=back_color)
    ze_opt = []
    __curs.execute("SELECT * FROM loaded_char")
    w = __curs.fetchone()[0]
    __curs.execute(f"SELECT * FROM '{w}_worlds'")
    x = __curs.fetchall()
    for item in x:
        ze_opt.append(item[1])
    
    def load():
        var0 = tk__var__0.get()
        for item in x:
            if item[1] == var0:
                wrld_filename = item[0]
        __curs.execute(f"UPDATE loaded_world SET world_filename = '{wrld_filename}' WHERE rowid = 1")
        __curs.execute(f"UPDATE loaded_world SET org_name = '{var0}' WHERE rowid = 1")

    _drop0 = OptionMenu(aroot, tk__var__0, *ze_opt, command=load)
    _drop0.pack()
    aroot.mainloop()


def btn_config(_btns: list):
    btn_a.config(text=_btns[0])
    btn_b.config(text=_btns[1])
    btn_c.config(text=_btns[2])
    btn_d.config(text=_btns[3])
    btn_e.config(text=_btns[4])

def start(btn_reset = False): 
    """
    This is where the actual game is running
    :return: None
    """
    global enable_next, __conn, __curs, autosave, txt__color, back_color
    if __name__ != '__main__':
        droot.config(bg=back_color)
        _info_lable_to_user.grid_remove()
        droot.focus_force()
    

    ze_menu = Menu(droot)
    droot.config(menu=ze_menu)
    load_menu = Menu(ze_menu)
    ze_menu.add_cascade(label='Load', menu=load_menu)
    load_menu.add_command(label='Load world', command=load_wrld)

    __curs.execute('SELECT * FROM loaded_world')
    _loaded_world = __curs.fetchall()[0]
    _loaded_world = _loaded_world[0]
    loaded_world_ = sqlite3.connect(_loaded_world)
    loaded_world = loaded_world_.cursor()
    funct = ''
    if enable_next == False:
        try:
            if autosave == 1:
                loaded_world.execute("SELECT * FROM autosaves")
                funct = loaded_world.fetchall()[-1]
                funct = funct[0]
            elif autosave == 0:
                loaded_world.execute("SELECT * FROM manualsaves")
                funct = loaded_world.fetchall()[-1]
                funct = funct[0]
            funct_ = for_chpt(funct)
        except:
            funct_ = s001
    elif enable_next == True:
        funct_ = for_chpt(next)
        enable_next = False
    #
    # def comm(var: str):
    _frame_gametext.grid(column=0, row=0)
    __frame_opt.grid(column=0, row=1)
    w = funct_('story')
    btn_commands = funct_('choice')
    _btns = w
    _label.grid(column=0, row=0)
    _label_.grid(column=0, row=0)
    
    if _btns[0] is None:
        btn_a.grid_remove()
    elif _btns[0] is not None:
        btn_a.grid(column=0, row=2)
        btn_a.config(command=btn_commands['a'])
    if _btns[1] is None:
        btn_b.grid_remove()
    elif _btns[1] is not None:
        btn_b.grid(column=1, row=2)
        btn_b.config(command=btn_commands['b'])
    if _btns[2] is None:
        btn_c.grid_remove()
    elif _btns[2] is not None:
        btn_c.grid(column=2, row=2)
        btn_c.config(command=btn_commands['c'])
    if _btns[3] is None:
        btn_d.grid_remove()
    elif _btns[3] is not None:
        btn_d.grid(column=3, row=2)
        btn_d.config(command=btn_commands['d'])
    if _btns[4] is None:
        btn_e.grid_remove()
    elif _btns[4] is not None:
        btn_e.grid(column=4, row=2)
        btn_e.config(command=btn_commands['e'])
    droot.mainloop()


def reset_btns():
    btn_a.grid_remove()
    btn_b.grid_remove()
    btn_c.grid_remove()
    btn_d.grid_remove()
    btn_e.grid_remove()
        

    

        
    
    
def print_to_ui(x):
    _label.config(text=x)    


def s001(funct):
    def main():
        print_to_ui("""
        Introduction;
        You are about 13 at the start of this story (you will age as time goes on).
        You live in a three story house, with a hallway down the middle of every floor.
        You live on the 1st story of this house. You also have 5 siblings, 3 girls, two boys.
        The house is in a quaint little town, very quiet and peaceful. This town's name is Yolkvile.

        
        
            """)

        a = 'Next'
        b = None
        c = None
        d = None
        e = None
        options_text = [a, b, c, d, e]
        btn_config(options_text)
        return options_text

    def _a():
        global a_num
        if a_num == 0:
            print_to_ui("""

            """)
            a_num += 1
        elif a_num == 1:
            auto_save(('s001', 'a'))
            global enable_next, next
            enable_next = True
            next = 's002'
            a_num = 0
            start()

            return
        return

    match funct:
        case 'story':
            return main()
        case 'choice':
            return {'a' :_a, 'b': None, 'c': None, 'd': None, 'e': None}


def s002(funct): # TODO: Add something here
    def main():
        print_to_ui("""
        Sadly empty 😢


            """)

        a = '{enter btn name here}'
        b = None
        c = None
        d = None
        e = None
        options_text = [a, b, c, d, e]
        btn_config(options_text)
        return options_text

    def _a():
        global a_num
        if a_num == 0:
            error_msg('')
            # print_to_ui("""
            # """)
            a_num += 1
        elif a_num == 1:
            auto_save(('s002', 'a'))
            global enable_next, next
            enable_next = True
            next = 's002'
            start()
            a_num = 0
            return
        return

    match funct:
        case 'story':
            return main()
        case 'choice':
            return {'a' :_a, 'b': None, 'c': None, 'd': None, 'e': None}




if __name__ == '__main__':
    # USE FOR TESTING ONLY
    start()



pass
