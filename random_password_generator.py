import random
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as tk_mb

LOW = 'low'
MEDIUM = 'medium'
HIGH = 'high'

comp_gen_passwd_warning_displayed = False


def comp_gen_passwd(level: str = HIGH) -> str:
    """Returns a computer generated random strong password"""
    password = []

    chars = 4 if level is LOW else 8 if level is MEDIUM else 16
    num_list = [chr(i) for i in range(48, 58)]
    caps_alpha_list = [chr(i) for i in range(65, 91)]
    small_aplha_list = [chr(i) for i in range(97, 123)]
    special_char_list = [chr(i) for i in range(32, 48)] + [chr(i) for i in range(58, 65)] + \
                        [chr(i) for i in range(91, 98)] + [chr(i) for i in range(123, 127)]

    # LOW STRENGTH
    if level is LOW:
        small_chars = random.randint(1, 3)

        small_list = random.choices(small_aplha_list, k=small_chars)
        number_list = random.choices(num_list, k=chars - small_chars)

        password.extend(small_list + number_list)

    # MEDIUM STRENGTH
    elif level is MEDIUM:
        small_chars = random.randint(1, 4)
        caps_chars = random.randint(1, 3)

        small_list = random.choices(small_aplha_list, k=small_chars)
        caps_list = random.choices(caps_alpha_list, k=caps_chars)
        number_list = random.choices(num_list, k=chars - small_chars - caps_chars)

        password.extend(small_list + caps_list + number_list)

    # HIGH STRENGTH
    elif level is HIGH:
        small_chars = random.randint(1, 6)
        caps_chars = random.randint(1, 5)
        special_chars = random.randint(1, 4)

        small_list = random.choices(small_aplha_list, k=small_chars)
        caps_list = random.choices(caps_alpha_list, k=caps_chars)
        spchar_list = random.choices(special_char_list, k=special_chars)
        number_list = random.choices(num_list, k=chars - caps_chars - small_chars - special_chars)

        password.extend(small_list + caps_list + spchar_list + number_list)

    else:
        raise Exception(f"Invalid level: '{level}', should be LOW, MEDIUM or HIGH.")

    random.shuffle(password)
    return ''.join(password)


def user_gen_password(level=MEDIUM, string: str = None):
    global comp_gen_passwd_warning_displayed

    special_char_list = [chr(i) for i in range(32, 48)] + [chr(i) for i in range(58, 65)] + \
                        [chr(i) for i in range(91, 98)] + [chr(i) for i in range(123, 127)]
    password = ''

    if string is None:
        comp_gen_passwd_warning_displayed = True
        password = comp_gen_passwd(level)

    else:
        small_alpha = []
        caps_alpha = []
        numbers = []
        special_chars = []

        for i in string:
            if 48 <= ord(i) < 58:
                numbers.append(i)
            elif 65 <= ord(i) < 91:
                caps_alpha.append(i)
            elif 97 <= ord(i) < 123:
                small_alpha.append(i)
            elif 32 <= ord(i) < 48 or 58 <= ord(i) < 65 or 91 <= ord(i) < 98 or 123 <= ord(i) < 127:
                special_chars.append(i)
            else:
                raise Exception(f"Invalid character '{i}', enter alphabets - capital or small, numbers, or special characters")
        random.shuffle(small_alpha)
        random.shuffle(caps_alpha)
        random.shuffle(numbers)
        random.shuffle(special_chars)

        # LOW STRENGTH
        if level is LOW:
            password = ''.join(small_alpha + caps_alpha + numbers + special_chars)

        # MEDIUM STRENGTH
        elif level is MEDIUM:
            _l1 = small_alpha + caps_alpha
            _l2 = numbers + special_chars
            random.shuffle(_l1)
            random.shuffle(_l2)

            password = ''.join(_l1 + _l2)

        # HIGH STRENGTH
        elif level is HIGH:
            _l1 = small_alpha + caps_alpha + numbers + special_chars
            random.shuffle(_l1)
            random.shuffle(_l1)

            password = ''.join(_l1)

        else:
            raise Exception(f"Invalid level: '{level}', should be low, medium or high.")

    return password


# for _ in range(10):
#     print(comp_gen_passwd(LOW), comp_gen_passwd(MEDIUM), comp_gen_passwd(HIGH))
#
# string = 'O28dm20dMa;%@#'
# print(user_gen_password(LOW, string), user_gen_password(MEDIUM, string), user_gen_password(HIGH, string))

def center_window(win: Tk or Toplevel):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('+{}+{}'.format(x, y))
    win.deiconify()


class PasswordGeneratorWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry('550x330')

        self.user_input_entry_editable = True
        self.user_input_password_strength_var = IntVar()
        self.comp_gen_password_strength_var = IntVar()
        self.strength_to_num_dict = {1: LOW, 2: MEDIUM, 3: HIGH}

        style = ttk.Style(self)
        style.configure('TRadiobutton', background='#585858', foreground='white', font=('Fixed Width', 10))
        style.configure('TLabelframe', background='#585858', foreground='white')
        style.configure('TLabelframe.Label', background='#585858', foreground='white', font=('Fixed Width', 10, 'bold'))

        # MAIN FRAMES
        self.user_input_frame = ttk.LabelFrame(self, text='  User Input  ')
        self.computer_generated_frame = ttk.LabelFrame(self, text='  Computer Generated  ')

        # USER INPUT FRAME WIDGETS
        self.user_input_lbl = Label(self.user_input_frame, text='Enter characters to generate a password:', font=('Fixed Width', 10))
        self.user_input_entry = Entry(self.user_input_frame, font=('Fixed Width', 11))
        self.user_input_lower_frame = Frame(self.user_input_frame)
        self.user_input_generate_btn = Button(self.user_input_lower_frame, text='Generate', width=16, relief=FLAT,
                                              command=self.generate_user_input_passwd, cursor='hand2', font=('Fixed Width', 10, 'bold', 'underline'))

        self.user_input_radio_low = ttk.Radiobutton(self.user_input_lower_frame, text='LOW', value=1,
                                                    variable=self.user_input_password_strength_var, width=12)
        self.user_input_radio_medium = ttk.Radiobutton(self.user_input_lower_frame, text='MEDIUM', value=2,
                                                       variable=self.user_input_password_strength_var, width=16)
        self.user_input_radio_high = ttk.Radiobutton(self.user_input_lower_frame, text='HIGH', value=3,
                                                     variable=self.user_input_password_strength_var, width=12)
        self.user_input_password_strength_var.set(2)

        # COMPUTER GENERATED FRAME WIDGETS
        self.comp_gen_input_lbl = Label(self.computer_generated_frame, text='Generate a random password based on the level of strength:',
                                        font=('Fixed Width', 10))
        self.comp_gen_input_entry = Entry(self.computer_generated_frame, font=('Fixed Width', 11))
        self.comp_gen_input_lower_frame = Frame(self.computer_generated_frame)
        self.comp_gen_input_generate_btn = Button(self.comp_gen_input_lower_frame, text='Generate', width=16, cursor='hand2',
                                                  relief=FLAT, command=self.generate_comp_gen_passwd, font=('Fixed Width', 10, 'bold', 'underline'))

        self.comp_gen_input_radio_low = ttk.Radiobutton(self.comp_gen_input_lower_frame, text='LOW', width=12,
                                                        variable=self.comp_gen_password_strength_var, value=1)
        self.comp_gen_input_radio_medium = ttk.Radiobutton(self.comp_gen_input_lower_frame, text='MEDIUM', width=16,
                                                           variable=self.comp_gen_password_strength_var, value=2)
        self.comp_gen_input_radio_high = ttk.Radiobutton(self.comp_gen_input_lower_frame, text='HIGH', width=12,
                                                         variable=self.comp_gen_password_strength_var, value=3)
        self.comp_gen_password_strength_var.set(2)

        # USER INPUT FRAME WIDGETS PACKING
        self.user_input_frame.pack(side=TOP, fill=BOTH, padx=2, pady=2)
        self.user_input_lbl.pack(side=TOP, padx=12, pady=3, anchor=W)
        self.user_input_entry.pack(side=TOP, padx=12, pady=12, ipady=6, ipadx=1, anchor=W, fill=X)
        self.user_input_lower_frame.pack(side=BOTTOM, padx=2, pady=2, ipady=8, fill=BOTH)
        self.user_input_generate_btn.pack(side=RIGHT, anchor=S, padx=12, pady=2)
        self.user_input_radio_high.pack(side=LEFT, anchor=S, padx=12, pady=2)
        self.user_input_radio_medium.pack(side=LEFT, anchor=S, padx=12, pady=2)
        self.user_input_radio_low.pack(side=LEFT, anchor=S, padx=12, pady=2)

        # COMPUTER GENERATED FRAME WIDGETS PACKING
        self.computer_generated_frame.pack(side=BOTTOM, fill=BOTH, padx=2, pady=2)
        self.comp_gen_input_lbl.pack(side=TOP, padx=12, pady=3, anchor=W)
        self.comp_gen_input_entry.pack(side=TOP, fill=X, padx=12, pady=12, ipady=6, ipadx=1, anchor=W)
        self.comp_gen_input_lower_frame.pack(side=BOTTOM, padx=2, pady=2, ipady=8, fill=BOTH)
        self.comp_gen_input_generate_btn.pack(side=RIGHT, anchor=S, padx=12, pady=2)
        self.comp_gen_input_radio_high.pack(side=LEFT, anchor=S, padx=12, pady=2)
        self.comp_gen_input_radio_medium.pack(side=LEFT, anchor=S, padx=12, pady=2)
        self.comp_gen_input_radio_low.pack(side=LEFT, anchor=S, padx=12, pady=2)

        self.comp_gen_input_entry.insert(0, 'aloo pakoda')
        self.user_input_entry.bind('<Control-c>', lambda _=None: self.copy_password(self.user_input_entry))
        self.comp_gen_input_entry.bind('<Control-c>', lambda _=None: self.copy_password(self.comp_gen_input_entry))
        self.user_input_entry.bind('<Double-1>', self.on_user_input_entry_double_click)
        self.make_readable(self.comp_gen_input_entry)

        # COLOR CONFIG
        self.color_dict = {
            'bg': '#585858',
            'fg': 'white',
            'insertbackground': 'white'
        }
        self.config(background=self.color_dict['bg'])
        # self.user_input_frame.config(background=self.color_dict['bg'], foreground=self.color_dict['fg'])
        self.user_input_entry.config(background=self.color_dict['bg'], foreground=self.color_dict['fg'],
                                     insertbackground=self.color_dict['insertbackground'])
        self.user_input_lbl.config(background=self.color_dict['bg'], foreground=self.color_dict['fg'])
        self.user_input_lower_frame.config(background=self.color_dict['bg'])
        self.user_input_generate_btn.config(background=self.color_dict['bg'], foreground=self.color_dict['fg'])
        # self.computer_generated_frame.config(background=self.color_dict['bg'], foreground=self.color_dict['fg'])
        self.comp_gen_input_entry.config(background=self.color_dict['bg'], foreground=self.color_dict['fg'])
        self.comp_gen_input_lbl.config(background=self.color_dict['bg'], foreground=self.color_dict['fg'])
        self.comp_gen_input_lower_frame.config(background=self.color_dict['bg'])
        self.comp_gen_input_generate_btn.config(background=self.color_dict['bg'], foreground=self.color_dict['fg'])

    def make_readable(self, widget):
        widget.bind('<Any-Key>', lambda _=None: 'break')

    def on_user_input_entry_double_click(self, event=None):
        self.user_input_entry.unbind('<Any-Key>')

    def copy_password(self, widget):
        self.clipboard_append(widget.get())

    def generate_user_input_passwd(self):
        global comp_gen_passwd_warning_displayed
        user_input_string = self.user_input_entry.get()
        password = ''
        if user_input_string == '':
            if comp_gen_passwd_warning_displayed is False:
                tk_mb.showinfo('Password Generator', 'Since there is no input, a random computer generated password '
                                                     'will be displayed based on the level of strength you have chosen.'
                                                     '\n\nPassword once generated will not be editable, it can only be'
                                                     ' copied.\n\nTo write again double click the entry field after'
                                                     ' every time password is generated.')
                comp_gen_passwd_warning_displayed = True
            password = comp_gen_passwd(level=self.strength_to_num_dict[self.user_input_password_strength_var.get()])
        else:
            password = user_gen_password(level=self.strength_to_num_dict[self.user_input_password_strength_var.get()],
                                         string=user_input_string)

        self.user_input_entry.delete(0, END)
        self.user_input_entry.insert(0, password)
        self.user_input_entry.bind('<Any-Key>', lambda _=None: 'break')

    def generate_comp_gen_passwd(self):
        password = comp_gen_passwd(level=self.strength_to_num_dict[self.comp_gen_password_strength_var.get()])
        self.comp_gen_input_entry.delete(0, END)
        self.comp_gen_input_entry.insert(0, password)


def main():
    pgw = PasswordGeneratorWindow()
    center_window(pgw)
    pgw.mainloop()


if __name__ == '__main__':
    main()
