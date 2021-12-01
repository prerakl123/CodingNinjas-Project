from tkinter import *
from tkinter import ttk
from tkinter import messagebox as tk_mb

text_font = ('Hebrew', 12)
font = ('Corbel', 12)
add_new_font = ('Corbel', 20)


class SmoothScrollFrame(LabelFrame):
    def __init__(self, master, **kw):
        LabelFrame.__init__(self, master, **kw)
        self.canvas = Canvas(self)
        v_scroll = Scrollbar(self, orient=VERTICAL)
        h_scroll = Scrollbar(self, orient=HORIZONTAL)

        v_scroll.config(command=self.canvas.yview)
        h_scroll.config(command=self.canvas.xview)
        self.canvas.config(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set, yscrollincrement=1)

        v_scroll.pack(side=RIGHT, fill=Y)
        h_scroll.pack(side=BOTTOM, fill=X)
        self.canvas.pack(side=LEFT, expand=YES, fill=BOTH)

        self.widget_frame = Frame(self.canvas)
        self.canvas.create_window(0, 0, window=self.widget_frame, anchor=NW)

        self.bind('<Configure>', self.on_interior_config)
        self.master.bind_all('<MouseWheel>', self.on_mouse_wheel)

    @staticmethod
    def pack_multiple_widgets(*widgets, **kwargs):
        if len(kwargs.items()) < 1:
            for i in widgets:
                i.pack()
        else:
            for i in widgets:
                i.pack(**kwargs)

    def on_interior_config(self, event=None):
        self.update_idletasks()
        width, height = self.widget_frame.winfo_reqwidth(), self.widget_frame.winfo_reqheight()
        self.canvas.config(scrollregion=(0, 0, width, height+50))

    refresh = on_interior_config

    def on_mouse_wheel(self, event=None):
        def _scroll(e=None):
            """For smooth scrolling"""
            nonlocal shift_scroll, scroll, scrolled
            if shift_scroll:
                if scrolled == 15:
                    return
                self.canvas.xview_scroll(scroll, 'units')
                scrolled += 1
                self.after(30, _scroll)
            else:
                if scrolled == 105:
                    return
                self.canvas.yview_scroll(scroll, 'units')
                scrolled += 1
                self.after(5, _scroll)

        scrolled = 0
        shift_scroll = (event.state & 0x1) != 0
        scroll = -1 if event.delta > 0 else 1
        _scroll()


class NewEntryFrame(Frame):
    def __init__(self, master, parent, **kwargs):
        Frame.__init__(self, master, **kwargs)
        self.entry_name = ''
        self.entry_type = 'entry'
        self.entry_value = ''

        self.master = master
        self.parent = parent

        # WIDGETS
        self.entry_name_lbl = Label(self, text='Name: ', font=font)
        self.entry_name_entry = Entry(self, width=10)

        self.entry_type_lbl = Label(self, text='Type: entry', font=font)

        self.entry_value_lbl = Label(self, text='Value: ', font=font)
        self.entry_value_entry = Entry(self, width=10)

        # PACKINGS
        self.entry_name_lbl.pack(side=LEFT, ipadx=3, ipady=3, padx=2, pady=2)
        self.entry_name_entry.pack(side=LEFT, ipadx=3, ipady=3, padx=2, pady=2)
        self.entry_type_lbl.pack(side=LEFT, ipadx=3, ipady=3, padx=2, pady=2)
        self.entry_value_lbl.pack(side=LEFT, ipadx=3, ipady=3, padx=2, pady=2)
        self.entry_value_entry.pack(side=LEFT, ipadx=3, ipady=3, padx=2, pady=2)

        self.entry_value_entry.bind('<Any-Key>', self.deny_edit)

    def deny_edit(self, event=None):
        tk_mb.showinfo('Spin a Yarn Story Generator', 'Initial values of all entries are supposed to be empty!')
        return 'break'


class NewEntryWindow(Toplevel):
    def __init__(self, master, **kwargs):
        Toplevel.__init__(self, master, **kwargs)

        self.entry_name = ''
        self.entry_type = 'entry'
        self.entry_value = ''

        self.master = master

        # WIDGETS
        self.entry_name_lbl = Label(self, text='Name: ', font=font)
        self.entry_name_entry = Entry(self, width=10)

        self.entry_type_lbl = Label(self, text='Type: entry', font=font)

        self.entry_value_lbl = Label(self, text='Value: ', font=font)
        self.entry_value_entry = Entry(self, width=10)

        # PACKINGS
        self.entry_name_lbl.pack(side=LEFT, ipadx=3, ipady=3, padx=2, pady=2)
        self.entry_name_entry.pack(side=LEFT, ipadx=3, ipady=3, padx=2, pady=2)
        self.entry_type_lbl.pack(side=LEFT, ipadx=3, ipady=3, padx=2, pady=2)
        self.entry_value_lbl.pack(side=LEFT, ipadx=3, ipady=3, padx=2, pady=2)
        self.entry_value_entry.pack(side=LEFT, ipadx=3, ipady=3, padx=2, pady=2)

        self.entry_value_entry.bind('<Any-Key>', self.deny_edit)

    def deny_edit(self, event=None):
        tk_mb.showinfo('Spin a Yarn Story Generator', 'Initial values of all entries are supposed to be empty!')
        return 'break'

    def create_frame_in_parent(self, event=None):
        frame = NewEntryFrame(self.master.value_editor_widget_frame, self.master)
        frame.pack(side=TOP, padx=2, pady=2, ipadx=2, ipady=2, fill=X)
        self.master.entry_frames_list.append(frame)


class NewComboFrame(Frame):
    def __init__(self, master, parent, **kwargs):
        Frame.__init__(self, master, **kwargs)

        self.master = master
        self.parent = parent


class NewComboWindow(Toplevel):
    def __init__(self, master, **kwargs):
        Toplevel.__init__(self, master, **kwargs)

        self.master = master


class Window(Tk):
    # STORIES WITH THIS SOFTWARE ARE FROM: https://www.squiglysplayhouse.com/WritingCorner/StoryBuilder/

    def __init__(self):
        Tk.__init__(self)

        self.entry_frames_list = []
        self.combo_frames_list = []

        # STORY FRAME AND IT'S WIDGETS
        self.story_frame = Frame(self, relief=RAISED)
        self.story_text_box = Text(self.story_frame, font=text_font)

        # FILL VALUE EDITOR FRAME AND IT'S WIDGETS
        self.value_frame = Frame(self)
        self.new_btns_frame = Frame(self.value_frame)
        self.value_editor_frame = SmoothScrollFrame(self.value_frame)
        self.value_editor_widget_frame = self.value_editor_frame.widget_frame
        self.add_new_entry_btn = Label(self.new_btns_frame, text='Add New Entry', font=add_new_font, fg='blue', cursor='hand2')
        self.add_new_entry_btn.bind('<ButtonPress-1>', self.add_new_entry_frame_btn_press)
        self.add_new_entry_btn.bind('<ButtonRelease-1>', self.add_new_entry_frame_btn_release)
        self.add_new_combo_btn = Label(self.new_btns_frame, text='Add New Dropdown', font=add_new_font, fg='blue', cursor='hand2')

        # PACKINGS
        self.story_frame.pack(side=LEFT, fill=BOTH, expand=TRUE)
        self.story_text_box.pack(side=TOP, fill=BOTH, expand=TRUE, pady=4, padx=4)

        self.value_frame.pack(side=RIGHT, fill=BOTH, expand=TRUE)
        self.new_btns_frame.pack(side=TOP, fill=X)
        self.value_editor_frame.pack(side=BOTTOM, fill=BOTH, expand=TRUE)
        self.add_new_entry_btn.pack(side=LEFT)
        self.add_new_combo_btn.pack(side=RIGHT)

    def add_new_combo_frame_btn_release(self, event=None):
        frame = NewComboFrame(self.value_editor_widget_frame, self)
        frame.pack(side=TOP, padx=2, pady=2, ipadx=2, ipady=2, fill=X)
        self.combo_frames_list.append(frame)
        self.value_editor_frame.refresh()

    def add_new_entry_frame_btn_press(self, event=None):
        self.add_new_entry_btn.config(fg='orange')

    def add_new_entry_frame_btn_release(self, event=None):
        win = NewEntryWindow(self)
        win.transient(self)
        win.wm_protocol('WM_DELETE_WINDOW', lambda _=None: [win.create_frame_in_parent(_), win.destroy()])
        self.add_new_entry_btn.config(fg='blue')
        self.value_editor_frame.refresh()


def main():
    win = Window()
    win.wm_state('zoomed')
    win.mainloop()


if __name__ == '__main__':
    main()
