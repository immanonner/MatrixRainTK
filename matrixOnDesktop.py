#!./venv/Scripts/python
import traceback
from re import search
from random import randint, shuffle, choice, sample
from string import ascii_uppercase, digits
from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
from kanji_lists import JOYO
import tkinter as tk
import tkinter.font as tkf
import tkinter.constants as tkc
import sys
import os
'''
key take aways:
--when bundling datafiles into a onefile exe, they're unpacked during runtime and located in the sys._MEIPASS (pyinstaller) temp folder
on a user's computer.
--locate missing modules during exe pack by manipulating the spec file and appending the pathex to include
the missing module/library folder path
--the only (easy) way for a nobody(like me) to send applications is in a password protected zip folder on google drive as of 20 may 21
--tkinter's text alignment kinda sucks, especially because it automatically trims any preceding spaces and forces you to
adjust the alignment mid animation and causes a jerky visual despite my best efforts at math-ing EDIT: i did better maths and its smooth now
--math is hard
--had some weird run-away when i had 1 new string object created per string that was deleted...dont know why... 
--adjusting the coordinates of a rectangle object is less load than creating 12k+ blocks of black....good job me.
--you can give tkinter objects names! also known as TAGS =)
--animating a typing cursor was interesting....
--animation in general is just difficult in tkinter--which is probably not the best platform for this but....it was fun.

'''


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.matrix_font = tkf.Font(family="Courier", size=25)
        self.config_master()
        self.pack()
        self.grid_dict_info = {'x_max_pxl': self.master.winfo_screenwidth(),
                               'y_max_pxl': self.master.winfo_screenheight(),
                               'col_width': int(self.matrix_font.measure('A\n')),
                               'row_height': int(self.matrix_font.metrics('ascent')),
                               'x_max_col': self.master.winfo_screenwidth() // self.matrix_font.measure('A\n'),
                               'y_max_row':
                                   self.master.winfo_screenheight() // self.matrix_font.metrics('ascent'),
                               'center_coordinates': (self.master.winfo_screenwidth() // 2,
                                                      self.master.winfo_screenheight() // 2)
                               }
        self.black_curtain_fall()
        # self.greeting_anderson()
        try:
            strings = self.matrix_strings_generator(1, self.grid_dict_info['x_max_col'])
            self.matrix_rain(strings)
        except Exception as er:
            traceback.print_exc()
            print(er)
            # time.sleep(10)
            raise er

    def kill_app(self, event):
        self.master.destroy()
        print('\nEnded Matrix Interface by Command\n')

    def config_master(self):
        self.master.attributes('-fullscreen', True, '-transparentcolor', 'purple')
        self.master.configure(bg='purple')
        self.master.bind('<Escape>', self.kill_app)

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller !!!THANK YOU STACK_OVERFLOW!!! """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def loadfont(self, fontpath, private=True, enumerable=False):

        '''
        Makes fonts located in file `fontpath` available to the font system.

        `private`     if True, other processes cannot see this font, and this
                      font will be unloaded when the process dies
        `enumerable`  if True, this font will appear when enumerating fonts

        See https://msdn.microsoft.com/en-us/library/dd183327(VS.85).aspx

        '''
        # This function was taken from
        # https://github.com/ifwe/digsby/blob/f5fe00244744aa131e07f09348d10563f3d8fa99/digsby/src/gui/native/win/winfonts.py#L15
        # This function is written for Python 2.x. For 3.x, you
        # have to convert the isinstance checks to bytes and str
        FR_PRIVATE = 0x10
        FR_NOT_ENUM = 0x20
        if isinstance(fontpath, bytes):
            pathbuf = create_string_buffer(fontpath)
            AddFontResourceEx = windll.gdi32.AddFontResourceExA
        elif isinstance(fontpath, str):
            pathbuf = create_unicode_buffer(fontpath)
            AddFontResourceEx = windll.gdi32.AddFontResourceExW
        else:
            raise TypeError('fontpath must be of type str or unicode')

        flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
        numFontsAdded = AddFontResourceEx(byref(pathbuf), flags, 0)
        return bool(numFontsAdded)

    def black_curtain_fall(self):
        self.master.black_canvas = tk.Canvas(self, bg='purple',
                                             width=self.grid_dict_info['x_max_pxl'],
                                             height=self.grid_dict_info['y_max_pxl'])
        all_columns = list(range(0, self.grid_dict_info['x_max_col']))
        all_rows = list(range(0, self.grid_dict_info['y_max_row']))
        shuffle(all_columns)
        tags_list = []
        try:
            while len(all_columns) > 0:
                execute_columns = all_columns[:randint(5, 10)]
                for _ in execute_columns:
                    all_columns.pop(0)
                for y in all_rows:
                    for x in execute_columns:
                        if y == 1:
                            self.master.black_canvas.create_rectangle(x * self.grid_dict_info['col_width'],
                                                                      y * self.grid_dict_info['col_width'],
                                                                      x * self.grid_dict_info['col_width'] +
                                                                      self.grid_dict_info['col_width'],
                                                                      y * self.grid_dict_info['col_width'] +
                                                                      self.grid_dict_info['col_width'],
                                                                      fill='black', tag=f'block{x}')
                            tags_list.append(f'block{x}')
                        if y != 1:
                            self.master.black_canvas.coords(f'block{x}',
                                                            x * self.grid_dict_info['col_width'],
                                                            1 * self.grid_dict_info['col_width'],
                                                            x * self.grid_dict_info['col_width'] +
                                                            self.grid_dict_info['col_width'],
                                                            y * self.grid_dict_info['col_width'] +
                                                            self.grid_dict_info['col_width'], )
                        self.master.black_canvas.pack()
                        self.update()
            self.master.black_canvas.configure(bg='black')
            for tag in tags_list:
                self.master.black_canvas.delete(tag)
            self.update()
        except tk.TclError as err:
            print(f'\n{err}: Process Interrupted\n')
            exit()

    def greeting_anderson(self):
        greeting_options = [
            'The Matrix has you...',
            'Hello, Mr Anderson...',
            'Are you sure this line is clean?',
            'The Matrix is everywhere. It is all around us...',
            'You have a problem with authority, Mr. Anderson...',
            'Did Morpheus ever really ask \'What if I told you\'?',
            'Are you the One?',
            'There is no spoon...',
            'Red pill or blue pill?',
            'Do you think that\'s air you\'re breathing now?'
            'Ignorance is bliss',
            'Welcome...To the real world.'
        ]
        greeting = choice(greeting_options)
        # self.master.black_canvas = tk.Canvas(self, bg='black',
        #                                      width=self.grid_dict_info['x_max_pxl'],
        #                                      height=self.grid_dict_info['y_max_pxl'])
        # self.master.black_canvas.pack()
        temp_string = '|'
        canvas_greeting_text = self.master.black_canvas.create_text(self.grid_dict_info['center_coordinates'][0] -
                                                                    self.matrix_font.measure(greeting) // 2,
                                                                    self.grid_dict_info['center_coordinates'][1],
                                                                    text=temp_string,
                                                                    fill='black', font=self.matrix_font, anchor='w')
        # blinky cursor beginning
        for i in range(4):
            self.master.black_canvas.after(500, self.master.black_canvas.itemconfig(canvas_greeting_text, fill='green'))
            self.update()
            self.master.black_canvas.after(500, self.master.black_canvas.itemconfig(canvas_greeting_text, fill='black'))
            self.update()
        temp_string = ''
        self.master.black_canvas.itemconfig(canvas_greeting_text, fill='green', text=temp_string)
        self.update()
        # animated type of greeting
        for ltr in greeting:
            temp_string += ltr
            self.master.black_canvas.after(randint(50, 300),
                                           self.master.black_canvas.itemconfig(canvas_greeting_text,
                                                                               text=temp_string + '|'))
            self.update()
        # blinky cursor ending
        for i in range(4):
            self.master.black_canvas.after(500, self.master.black_canvas.itemconfig(canvas_greeting_text,
                                                                                    text=temp_string))
            self.update()
            self.master.black_canvas.after(500, self.master.black_canvas.itemconfig(canvas_greeting_text,
                                                                                    text=temp_string + '|'))
            self.update()
        # switch to unchanged greeting so we can begin to delete text on screen randomly
        self.master.black_canvas.itemconfig(canvas_greeting_text, fill='green', text=greeting)
        self.update()
        shuffled_greeting = list(temp_string)
        shuffle(shuffled_greeting)
        while greeting != ' ' * len(temp_string):
            for ltr in set(temp_string):
                greeting = greeting.replace(ltr, ' ')
                self.master.black_canvas.after(randint(100, 500),
                                               self.master.black_canvas.itemconfig(canvas_greeting_text, text=greeting))
                self.update()
        self.master.black_canvas.delete(canvas_greeting_text)

    def matrix_strings_generator(self, a: int, b: int = None):
        fontpath = self.resource_path('MatrixCodeFont.otf')
        self.loadfont(fontpath, True, False)
        num_of_strings = 0
        if a == b or b is None:
            num_of_strings = a
        elif a != b and b is not None and b > a:
            num_of_strings = randint(a, b)
        elif a != b and b is not None and a > b:
            num_of_strings = randint(b, a)

        matrix_strings = {}
        characters = list((ascii_uppercase + digits * 2)*100)
        kanji = list(JOYO)[:len(characters)-1]

        # bakes in the \newline for vertical printing
        choices = {'Eng': list(characters), 'Kanji': kanji, 'Matrix': list(characters)}
        for n in range(num_of_strings):
            chosen_x_col = randint(1, self.grid_dict_info['x_max_col'] - 1)
            name = f'id{chosen_x_col}'
            font_size = choice([12, 12, 25, 50, 150])
            length = randint(3, (self.grid_dict_info['y_max_pxl']//tkf.Font(family="Courier", size=font_size).metrics('ascent'))//2)
            row = randint(0, self.grid_dict_info['y_max_pxl']//tkf.Font(family="Courier", size=font_size).metrics('ascent') - length + 2)
            lang = choice(['Eng', 'Kanji', 'Matrix'])
            if lang == 'Matrix':
                font_family = "Matrix Code NFI"
            else:
                font_family = "Courier"
            generated_string = sample(choices[lang], length)
            generated_string[-1] = generated_string[-1].replace('\n', '')
            matrix_strings[name] = {'column': chosen_x_col,
                                    'row': row,
                                    'length': length,
                                    'counter': 0,
                                    'generated_string': generated_string,
                                    'font': tkf.Font(family=font_family, size=font_size),
                                    'font_family': font_family,
                                    'font_size': font_size}
            # using the x column as the key prevents multiple strings in the same column in the future
            # because IF a x_col is chosen and it already exists in the dict...
            # it will only overwrite the value and continue
            # self.master.black_canvas.create_text(matrix_strings[name]['column'] * self.grid_dict_info['col_width'],
            #                                      matrix_strings[name]['row'] * self.grid_dict_info['col_width'],
            #                                      text=matrix_strings[name]['generated_string'],
            #                                      fill='green', font=tkf.Font(family="Courier",
            #                                      size=matrix_strings[name]['font_size']),
            #                                      anchor='n', tag=name)
        # pprint.pprint(matrix_strings)
        return matrix_strings

    def matrix_rain(self, matrix_strings: dict):
        # self.master.black_canvas = tk.Canvas(self, bg='black',
        #                                      width=self.grid_dict_info['x_max_pxl'],
        #                                      height=self.grid_dict_info['y_max_pxl'])
        # self.master.black_canvas.pack()
        while len(matrix_strings.items()) != 0:
            for string_name in list(matrix_strings):
                str_obj = matrix_strings[string_name]
                if str_obj['counter'] == 0:  # stage 1 create text obj on canvas
                    next_ltr = str_obj['counter']
                    temp_str = str_obj['generated_string'][next_ltr]
                    self.master.black_canvas.create_text(str_obj['column'] * self.grid_dict_info['col_width'],
                                                         str_obj['row'] * str_obj['font'].metrics('linespace'),
                                                         width=str_obj['font'].measure(str_obj['generated_string'][0]),
                                                         text=temp_str,
                                                         fill='green',
                                                         font=str_obj['font'],
                                                         anchor='nw', tag=string_name)

                if 0 < str_obj['counter'] <= str_obj['length']-1:  # stage 2 print new text
                    next_ltr = str_obj['generated_string'][str_obj['counter']]
                    self.master.black_canvas.insert(string_name, tkc.END, next_ltr)

                if str_obj['counter'] > str_obj['length']-1 and \
                        bool(search(r'\S', f'{self.master.black_canvas.itemcget(string_name, "text")}')) is True: # stage 3 delete text
                    old_str = f'{self.master.black_canvas.itemcget(string_name, "text")}'
                    num = old_str.index(search(r'\S', old_str).group())
                    if str_obj['counter'] == str_obj['length']:
                        self.master.black_canvas.coords(string_name, str_obj['column'] * self.grid_dict_info['col_width'],
                                                        (str_obj['row'] * str_obj['font'].metrics('linespace')) + ((len(old_str)) * str_obj['font'].metrics('linespace')))
                        self.master.black_canvas.itemconfig(string_name, text=old_str, anchor='sw')
                    else:
                        temp_str = f'\n{old_str[num+1:]}'
                        self.master.black_canvas.itemconfig(string_name, text=temp_str)

                if bool(search(r'\S', f'{self.master.black_canvas.itemcget(string_name, "text")}')) is False: # stage 4 create new strings
                    self.master.black_canvas.delete(string_name)
                    matrix_strings.pop(string_name)
                    new_str_objs = self.matrix_strings_generator(1, 5)
                    for obj in list(new_str_objs):
                        if obj in matrix_strings:
                            new_str_objs.pop(obj)
                    matrix_strings.update(new_str_objs)
                str_obj['counter'] += 1
            self.update()


def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()


if __name__ == '__main__':
    main()
