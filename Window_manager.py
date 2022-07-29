import time
from tkinter import *
from tkinter import messagebox
import sqlite3


from utilz import error_msg
import threading
conn = sqlite3.connect('Text journey database.db')
curs = conn.cursor()


def for_chpt(funct: str):
    import chpt
    return getattr(chpt, funct)

# create
def create_new_invent_table(_input0: int): # A new inventory table will be created for every world save
    _input0 = _input0.__str__()
    curs.execute(f"""CREATE TABLE inventory{_input0} (
    item_name text,
    is_enchanted integer,
    enchant_name text
    )""")


def create_new_character_table(char_name: str, num, owner: str, last_name: str):
    num = num.__str__()
    curs.execute(f"""CREATE TABLE '{num}' (
        char_name text,
        char_id integer,
        owner text,
        world_id integer,
        last_name text
        )""")
    curs.execute(f"INSERT INTO '{num}' VALUES ('{char_name}', {num}, '{owner}', 1, '{last_name}')")
    conn.commit()



def create_new_world(name):
    curs.execute("SELECT * FROM loaded_char")
    char_id = curs.fetchall()[0]
    char_id = char_id[0]
    x = isinstance(char_id, int)
    if x:
        char_id = str(char_id)
    curs.execute(f"SELECT world_id FROM '{char_id}'")
    wrld_id = int(curs.fetchone()[0])
    _conn = sqlite3.connect(f'{char_id}__{name}_{wrld_id}.db')
    _curs = _conn.cursor()
    wrld_id += 1
    update_table(f"'{char_id}'", 'world_id', '1', wrld_id)
    curs.execute(f"UPDATE loaded_world SET world_filename = '{char_id}__{name}_{wrld_id - 1}.db' WHERE rowid = 1")
    curs.execute(f"UPDATE loaded_world SET org_name = '{name}' WHERE rowid = 1")
    curs.execute(f"INSERT INTO '{char_id}_worlds' VALUES ('{char_id}__{name}_{wrld_id}.db', '{name}')")
    _curs.execute("CREATE TABLE ident_data (org_wrld_name text)")
    _curs.execute("CREATE TABLE autosaves (auto_saves text, choice text)")
    _curs.execute("CREATE TABLE manualsaves (manual_saves text)")
    _curs.execute("CREATE TABLE inventory (item_id integer, is_enhanced integer, enhancement_id integer)")
    _curs.execute(f"INSERT INTO ident_data VALUES ('{name}')")
    conn.commit()
    _conn.commit()
    


def create_worlds_table(char_id: str):
    curs.execute(f"""CREATE TABLE '{char_id}_worlds' (
        world_filename text,
        org_name text
        )""")


def update_table(table_name: str, column: str, row_id: str, value):
    value_ = isinstance(value, str)
    value = str(value)
    if value_:
        curs.execute(f"UPDATE {table_name} SET {column} = '{value}' WHERE rowid = {row_id}")
    elif not value_:
        curs.execute(f"UPDATE {table_name} SET {column} = {value} WHERE rowid = {row_id}")
    conn.commit()



def look_up(value, var: int = 1):
    """
    Looks up a character in the database
    :param value: if var = true: value should be an integer. if var = false: value should be a string.
    :param var: default value: True. Look up by char_id is True, look up by char_name is false
    :return: String if looking up by char_id, Integer if looking up by char_name
    """
    curs.execute('SELECT * FROM char_storage')
    all_ = curs.fetchall()

    def look_up_by_char_id(char_id: int):
        for item_ in all_:
            char__id = item_[1]
            if char__id == char_id:
                char_name: str = item_[0]
                return char_name

    def look_up_by_char_name(char_name: str):
        for item_ in all_:
            char__name = item_[0]
            if char__name == char_name:
                char_id: int = item_[1]
                return char_id
    
    def look_up_by_owner(input_: tuple):
        owner: str = input_[0]
        var2: bool = input_[1]
        match var2:
            case True:
                for item_ in all_:
                    owner__ = item_[2]
                    if owner__ == owner:
                        owner_:int = item_[1]
                        return owner_
            case False:
                for item_ in all_:
                    owner__ = item_[2]
                    if owner__ == owner:
                        owner_: str = item_[0]
                        return owner_
        
    if var == 2:
        return look_up_by_owner(value)
    elif var == 1:
        return look_up_by_char_id(value)
    elif var == 0:
        return look_up_by_char_name(value)


def insert_into_table(table: str, value):
    """
    :param value: The value(s) in the form of a sqlite command (ex: ('x', y, 'z'))
    :param table: The name of the table
    :return:
    """
    _value = isinstance(value, str)
    if _value:
        curs.execute(f"INSERT INTO {table} VALUES ('{value}')")
    elif not _value:
        curs.execute(f"INSERT INTO {table} VALUES ({value})")


def auto_save(data: tuple): # TODO: :)
    """
    :param data: A tuple which needs the name of the section_funct to be in spot 0
    :return:
    """
    if autosave == 1:
        curs.execute(f"SELECT * FROM loaded_world")
        world_name = curs.fetchall()[0]
        conn_ = sqlite3.connect(f'{world_name[0]}')
        curs_ = conn_.cursor()
        curs_.execute(f"INSERT INTO autosaves VALUES ('{data[0]}', '{data[1]}')")
        conn_.commit()
        conn_.close()

        
    elif autosave == 0:
        pass
    # curs_.execute(f"")
    return

def manual_save():
    return


def insert_into_table_1(table: str, values: str):
    curs.execute(f"INSERT INTO {table} VALUES ({values})")



def add_to_char_storage(char_name: str, char_id: int):
    char_id = char_id.__str__()
    insert_into_table_1('char_storage', [char_name, char_id])


# def create_save_data_holder(char_id: int):
#     curs.execute(f"CREATE TABLE 'save_holder{char_id}' ()")


def delete_char(char: int | str):
    x = isinstance(char, int)
    if x:
        curs.execute(f"DROP TABLE '{char}'")
        curs.execute(f"DELETE FROM char_storage {char}")
    elif not x:
        x = look_up(x)
        curs.execute(f"DROP TABLE '{x}'")
    conn.commit()

def delete(table: str):
    curs.execute(f"DROP TABLE {table}")
    conn.commit()

# Holy fricken mackerel, this is the longest python file I have ever done, gosh

curs.execute("SELECT * FROM config")


comm0 = curs.fetchall()
comm0 = comm0[0]

back_color: str = comm0[1]


if back_color == 'black':
    txt_color = 'white'
elif back_color == 'blue':
    txt_color = 'white'
elif back_color == 'red':
    txt_color = 'white'
elif back_color == 'purple':
    txt_color = 'white'
elif back_color == 'gray':
    txt_color = 'white'
elif back_color == 'yellow':
    txt_color = 'black'
elif back_color == 'green':
    txt_color = 'white'
elif back_color == 'white':
    txt_color = 'black'
else:
    txt_color = 'black'


autosave = comm0[0]

awareness = comm0[2]

if autosave == 1:
    autosave_text = 'On'
elif autosave == 0:
    autosave_text = 'Off'

if awareness == 1:
    awareness_text = 'On'
elif awareness == 0:
    awareness_text = 'Off'

#global variables


if __name__ == '__main__':
    root = Tk()
    root.title('Text Journey')
    root.config(background=back_color)
    root.geometry('400x300')
    from chpt import *

    __tkvartxt_0 = StringVar()



    def redirect():
        _start_btn.config(state=DISABLED)
        start()


    def update_loaded_char():
        curs.execute('SELECT * FROM loaded_char')
        ___laugh = curs.fetchall()[0]
        loaded_char_ = look_up(___laugh[0])
        return loaded_char_


    def update_config():
        curs.execute("SELECT * FROM config")

        global comm0
        global back_color
        global autosave
        global awareness
        global awareness_text
        global autosave_text

        comm0 = curs.fetchall()
        comm0 = comm0[0]

        back_color = comm0[1]

        autosave = comm0[0]

        awareness = comm0[2]

        if autosave == 1:
            autosave_text = 'On'
        elif autosave == 0:
            autosave_text = 'Off'

        if awareness == 1:
            awareness_text = 'On'
        elif awareness == 0:
            awareness_text = 'Off'



        return [autosave_text, awareness_text, back_color]


    loaded_char = update_loaded_char()

    #functions


    # curs.execute("CREATE TABLE config (autosave INTEGER, background TEXT)")
    # conn.commit()







    def opt_window():
        global autosave
        # local variables
        aroot = Toplevel(root)
        aroot.config(bg=back_color)
        aroot.title('Config')
        # aroot

        tkvar_drop0 = StringVar()
        tkvar_drop1 = StringVar()
        tkvar_drop2 = StringVar()
        opt_list_0 = ['On', 'Off']
        opt_list_1 = ['white', 'gray', 'black', 'red', 'yellow', 'blue', 'green', 'purple']
        opt_list_2 = ['On', 'Off']
        tkvar_drop0.set(autosave_text)
        tkvar_drop1.set(back_color)
        tkvar_drop2.set(awareness_text)
        
        #functions
        def back():
            aroot.destroy()

        def save():
            auto = tkvar_drop0.get()
            match auto:
                case 'On':
                    auto = 1
                case 'Off':
                    auto = 0

            aware = tkvar_drop2.get()

            match aware:
                case 'On':
                    aware = 1
                case 'Off':
                    aware = 0

            bg_color = tkvar_drop1.get()
            curs.execute(f"UPDATE config SET autosave = {auto}")
            curs.execute(f"UPDATE config SET background = '{bg_color}'")
            curs.execute(f"UPDATE config SET self_awareness = {aware}")
            conn.commit()
            _label2.grid(column=1, row=1)


            update_config()
            root.config(bg=bg_color)
            aroot.config(bg=bg_color)
            _opt_lable_0.config(text=f'Currently: {autosave_text}')
            _opt_lable_1.config(text=f'Currently: {back_color}')
            _opt_lable_2.config(text=f'Currently: {awareness_text}')



            pass
        #everything else
        _btn_back = Button(aroot, text='Back', command=back, bg='red')
        _btn_save = Button(aroot, text='Save', bg='green', command=save)
        _label0 = Label(aroot, text='Autosave Every Section', bg=back_color, fg=txt_color)
        _label1 = Label(aroot, text='Background color', bg=back_color, fg=txt_color)
        _label2 = Label(aroot, text='Saved', fg='green')
        _label3 = Label(aroot, text='Self Awareness', bg=back_color, fg=txt_color)
        _drop0 = OptionMenu(aroot, tkvar_drop0, *opt_list_0)
        _drop1 = OptionMenu(aroot, tkvar_drop1, *opt_list_1)
        _drop2 = OptionMenu(aroot, tkvar_drop2, *opt_list_2)
        _opt_lable_0 = Label(aroot, text=f'Currently: {autosave_text}', bg=back_color, fg=txt_color)
        _opt_lable_1 = Label(aroot, text=f'Currently: {back_color}', bg=back_color, fg=txt_color)
        _opt_lable_2 = Label(aroot, text=f'Currently: {awareness_text}', bg=back_color, fg=txt_color)
        #Grid the buttons and stuff
        _btn_back.grid(column=5, row=6)
        _btn_save.grid(column=2, row=0)
        _opt_lable_0.grid(column=0, row=1)
        _opt_lable_1.grid(column=0, row=4)
        _opt_lable_2.grid(column=0, row=7)
        _label0.grid(column=0, row=0)
        _label1.grid(column=0, row=3)
        _label3.grid(column=0, row=6)
        _drop0.grid(column=0, row=2)
        _drop1.grid(column=0, row=5)
        _drop2.grid(column=0, row=8)
        aroot.mainloop()


    def game_info():
        aroot = Toplevel(root)
        aroot.title('Game info')
        aroot.config(background=back_color)
        #functions

        def back():
            aroot.destroy()

        #everything else
        _btn_back = Button(aroot, text='Back', command=back, bg='red')
        _btn_back.grid(column=5, row=6)
        _label0 = Label(aroot, text="""
    Version: 0.4
    Chances of you seeing this: 0.0000001% (Yes that is supposed to be humor)
    Was this a pain in the rear end to make? Yes. Was it fun sometimes? Also yes.
    This game is pretty much going to be about 60-90% 'fantasy'.
    closeness to launchpad: 60-80%
    closeness to being put onto github: 40%


    
    Change log: (7/27/2022)
    Fixed a critical bug that disrupted button display

    Change log: (7/12/2022)
    Added a primitive autosave system
    Added the ability to load a world


    Change log: (7/2/2022)
    Added the game engine
    Added the ability to enter a last name
    Removed 'Save History'; Replaced with 'Load' on the Game Engine
    Fixed a bug where the drop down menus weren't working right
    Added a system to change the color of the text between white and black based of the color of the background



    Change log: (6/10/2022)
    Added Character creation
    Added Character info to data window
    Added Character Selection to the main window
    Added a label to tell you the character selected
    
        """, bg=back_color, fg=txt_color)
        _label0.grid(column=0, row=0)
        aroot.mainloop()


    def game_progress():
        aroot = Toplevel(root)
        aroot.title('in-game progress')
        aroot.config(background=back_color)
        label0 = Label(aroot, text="""
    Ah, hello. Progress stuff will be implemented later.
    For now enjoy this text: LOOOOOOOOLLLLLLLZZZZZZEEEEEEERRRRRRR
    Thank you for listening to my ted talk.
    
    This will be interesting to try and implement.
        """)

        def back():
            aroot.destroy()

        _btn_back = Button(aroot, text='Back', command=back, bg='red')
        _btn_back.grid(column=5, row=6)
        label0.grid(column=0, row=0)
        aroot.mainloop()


    def config_help():
        aroot = Toplevel(root)
        aroot.title('Config Help')
        aroot.config(background=back_color)
        #functions


        def back():
            aroot.destroy()

        def awareness_help():
            troot =  Toplevel(aroot)
            troot.title('Awareness help page')
            options_ = ['']
            troot.mainloop()
            return

        def autosave_help():
            broot = Toplevel(aroot)
            broot.title('Autosave help page')
            broot.config(background=back_color)

            tkvar_txt = StringVar()
            options_drop___0 = ['Basic explanation (suggested)', 'More in-depth explanation']
            #functions


            def print_to_ui(x):
                x = tkvar_txt.get()
                x = x.lower()
                match x:
                    case 'basic explanation (suggested)':
                        _label__0.config(text="""
    Section: What is a section? A section in this case is several sentences for the reader to read before a choice.
    ^^^ to break it down, autosave saves your progress right before the choice.
                        """)
                    case 'more in-depth explanation':
                        # error_msg('04')
                        _label__0.config(text="""
                        This is a more technical breakdown for those that are curious on how the system works.
                        With how it is currently coded each section is a function which also hold the info for the buttons.
                        The 'words' breakdown isn't fully correct when saying 'autosave saves your progress right before the choice'.
                        It actually saves when you complete that section, but doesn't use the saved button info, effectivly restarting the section when you come back.
                        Now when reading the line above you may be asking 'wait, it saves my button info?'. The button info saved (Note that this is NOT set in stone yet) will
                        affect the Path and Karma. Karma is self explanitory, but what is Path? To see the definition of Path in this context see Feature plans.
                        """)
                return

            def _back():
                broot.destroy()


            #everything else

            _btn__back = Button(broot, text='Back', command=_back, bg='red')
            _btn__back.grid(column=5, row=6)
            _drop__0 = OptionMenu(broot, tkvar_txt, *options_drop___0, command=print_to_ui)
            _drop__0.grid(column=0, row=0)
            _label__0 = Label(broot, bg=back_color, fg=txt_color)
            _label__0.grid(column=0, row=1)
            return


        #everything else
        _btn_autosave_help = Button(aroot, text='Autosave', command=autosave_help)
        _btn_back = Button(aroot, text='Back', command=back, bg='red')
        _btn_back.grid(column=5, row=6)
        _btn_autosave_help.grid(column=0, row=0)
        return


    def plans():
        aroot = Toplevel(root)
        aroot.config(background=back_color)
        _label__0 = Label(aroot, text="""
    Here are some of the features planned:
    Manual saves (high priority)
    console (low priority)
    Karma (low priority)
    Path (low priority)
    Random events (low priority)
    More storyline(top priority)
    (Also note that this window will not always be available, and may be removed later on)
        """, bg=back_color, fg=txt_color)
        _label__0.pack()

    def char_window():
        aroot = Toplevel(root)
        aroot.title('Character')
        aroot.config(background=back_color)

        tktxtvar = StringVar()
        opt_list__0 = ['Character data', 'Save data', 'Config data']

        def data_viewer(var):
            var = tktxtvar.get()
            var = var.lower()
            match var:
                case 'character data':
                    curs.execute('SELECT * FROM loaded_char')
                    x = curs.fetchall()[0]
                    x = x[0]
                    y = look_up(x)
                    curs.execute(f"SELECT * FROM '{x}'")
                    z = curs.fetchall()
                    z = z[0]
                    z = z[2]
                    x = str(x)
                    _label__0.config(text=f"""
    Character name: {y}
    Unique Character ID: {x}
    Owner: {z}
                    """)
                case 'save data':
                    error_msg('04')
                case 'config data':
                    _label__0.config(text=f'''
    Auto save: {autosave_text}
    Background: {back_color}
    Awareness: {awareness_text}
    ''')



        def back():
            aroot.destroy()

        _drop__0 = OptionMenu(aroot, tktxtvar, *opt_list__0, command=data_viewer)
        _label__0 = Label(aroot)
        _label__1 = Label(aroot, text='Use the dropdown menu to select what data to view', bg=back_color, fg=txt_color)
        _btn_back = Button(aroot, text='Back', command=back, bg='red')
        _btn_back.grid(column=5, row=6)
        _drop__0.grid(column=0, row=1)
        _label__0.grid(column=0, row=2)
        _label__1.grid(column=0, row=0)
        aroot.mainloop()


    def char_select(a):
        a = __tkvartxt_0.get()
        b = look_up(a, 0)
        update_table('loaded_char', 'char_id', '1', b)
        _opt0_.config(state=DISABLED)
        xyzbc = update_loaded_char()
        label_1_.config(text=f'Current character: {xyzbc}', fg='blue')


    def create_char():
        aroot = Toplevel(root)
        aroot.config(bg=back_color)


        def back():
            aroot.destroy()

        def submit():
            try:
                userinput = input_field_0.get()
                input_field_0.delete(0, END)
                userinput2 = input_field_1.get()
                input_field_1.delete(0, END)
                userinput3 = _input_lastname.get()
                _input_lastname.delete(0, END)

                req1 = False
                req2 = False
                req3 = False
                req4 = True

                if userinput != '':
                    req1 = True
                    if userinput3 != '':
                        if userinput2 != '':
                            req2 = True
                        req3 =True
                        curs.execute("SELECT * FROM config")
                        x = curs.fetchall()[0]
                        num: int = int(x[3])
                        num_ = num + 1
                        time.sleep(0.3)
                        curs.execute(f"UPDATE config SET non_ui_char_num = '{num_}' WHERE rowid = 1")
                        # update_table('config', 'non_ui_char_num', '1', num_)
                        if not req2:
                            userinput2 = 'Not provided'
                        create_new_character_table(userinput, num, userinput2, userinput3)
                        create_worlds_table(str(num))
                        curs.execute(f"INSERT INTO char_storage VALUES ('{userinput}', {num}, '{userinput2}')")
                        global ze_list
                        global item
                        global randomvar_a
                        curs.execute('SELECT char_name FROM char_storage')
                        randomvar_a = curs.fetchall()
                        ze_list = []

                        for item in randomvar_a:
                            ze_list.append(item[0])



                        # _reset_opt0_btn_.config(state=DISABLED)
                        messagebox.showinfo('Character created', f"Your character {userinput} {userinput3} has been created")
                        global loaded_char
                        loaded_char = userinput
                        update_table('loaded_char', 'char_id', '1', f"{num}")
                        label_1_.config(text=f'Current character: {loaded_char}')
                        aroot.destroy()
                if not req1:
                    req4 = False
                if not req3:
                    req4 = False
                if not req4:
                    messagebox.showwarning('MUST ENTER REQUIRED FIELDS', "In order to create a character you must enter information in the required fields. required fields have * above them.")
                    return
            except sqlite3.OperationalError:
                error_msg('01')
                aroot.destroy()
            return

        input_field_0 = Entry(aroot, width=40, bg='yellow')
        input_field_0.grid(column=0, row=1)
        input_field_1 = Entry(aroot, width=40, bg='yellow')
        input_field_1.grid(column=0, row=5)
        _input_lastname = Entry(aroot, width=40, bg='yellow')
        _input_lastname.grid(column=0, row=3)
        _btn_back = Button(aroot, text='Back', command=back, bg='red')
        _btn_back.grid(column=5, row=6)
        _btn_sub = Button(aroot, text='Submit all', command=submit, bg='green')
        _btn_sub.grid(column=2, row=6)
        _label0_ = Label(aroot, text='Enter first (and middle if you want) name*', bg=back_color, fg=txt_color)
        _label0_.grid(column=0, row=0)
        _label1_ = Label(aroot, text='Enter Character Owner/Author/Creator(aka, the one who created the character)', bg=back_color, fg=txt_color)
        _label1_.grid(column=0, row=4)
        _lable2_ = Label(aroot, text='Enter last name of character*', bg=back_color, fg=txt_color)
        _lable2_.grid(column=0, row=2)


        aroot.mainloop()







    def create_world():
        aroot = Toplevel()
        aroot.title('New World')
        aroot.config(bg=back_color)
        _lable_0_ = Label(aroot, text='Enter world name below', bg=back_color, fg=txt_color)
        _lable_0_.grid(column=0, row=0)
        _textbox0 = Entry(aroot, width=40, bg='yellow')
        _textbox0.insert(0, 'New World')
        _textbox0.grid(column=0, row=1)

        def submit():
            x = _textbox0.get()
            _textbox0.delete(0, END)
            create_new_world(x)
        __btn_sub = Button(aroot, text='Submit', command=submit)
        __btn_sub.grid(column=0, row=2)




        aroot.mainloop()
        return

    def other():
        aroot = Toplevel(root)
        aroot.title('Other')
        aroot.config(bg=back_color)



        aroot.mainloop()
        return


    #everything else

    _menu0 = Menu(root)
    root.config(menu=_menu0)
    opt_menu = Menu(_menu0)
    create_menu = Menu(_menu0)
    _menu0.add_cascade(label='Create', menu=create_menu)
    create_menu.add_command(label='New Character', command=create_char)
    create_menu.add_command(label='New World Save', command=create_world)
    _menu0.add_cascade(label='Options', menu=opt_menu)
    opt_menu.add_command(label='Open config menu', command=opt_window)
    opt_menu.add_command(label='Exit', command=root.destroy, background='red')
    info_menu = Menu(_menu0)
    _menu0.add_cascade(label='Info', menu=info_menu)
    info_menu.add_command(label='Game info', command=game_info)
    info_menu.add_command(label='Progress info', command=lambda: error_msg('00'))
    info_menu.add_command(label='Feature plans/Future Updates', command=plans)
    help_menu = Menu(_menu0)
    _menu0.add_cascade(label='Help', menu=help_menu)
    help_menu.add_command(label='config', command=config_help)
    help_menu.add_command(label='Console', command=lambda: error_msg('04'))
    help_menu.add_command(label='other')
    delete_menu = Menu(_menu0)
    _menu0.add_cascade(menu=delete_menu, label='Delete...')
    delete_menu.add_command(label='Delete Loaded character')


    _data_btn = Button(root, text='Open data window', command=char_window)
    _data_btn.grid(column=0, row=0)




    curs.execute('SELECT char_name FROM char_storage')
    randomvar_a = curs.fetchall()
    ze_list = []

    for item in randomvar_a:
        ze_list.append(item[0])

    label_0_ = Label(root, text='Choose your character', fg='blue')
    label_0_.grid(column=0, row=1)
    __tkvartxt_0.set(loaded_char)
    _opt0_ = OptionMenu(root, __tkvartxt_0, *ze_list, command=char_select)
    _opt0_.grid(column=0, row=2)
    _reset_opt0_btn_ = Button(root, text='Reset character selection', command=lambda: _opt0_.config(state=NORMAL))
    _reset_opt0_btn_.grid(column=0, row=3)
    label_1_ = Label(root, text=f'Current character: {loaded_char}', fg='blue')
    label_1_.grid(column=0, row=4)
    _start_btn = Button(root, text='Start', command=redirect)
    _start_btn.grid(column=6, row=6)



    root.mainloop()
    conn.close()
pass
