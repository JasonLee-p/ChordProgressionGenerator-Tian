import pygame.midi as pm
from PIL import Image, ImageTk
from pyPCS import Chord
from TkGUI import *
from musicxmlReader import *


class BottomFrame:
    def __init__(self, frame):
        self.basic = tk.Frame(master=frame, bg='ivory', height=250)
        self.basic.pack(side='bottom', fill='x', expand=False)
        self.basic.propagate(0)


class NoteBookBasic:
    def __init__(self, frame):
        """
        ———————————————————————————————————————左区和右区的分割———————————————————————————————————————"""
        self.basic = tk.Frame(master=frame, bg='ivory')
        self.left = tk.Frame(master=self.basic, bg=BG_COLOUR, width=320, height=700)
        self.right = tk.Frame(master=self.basic, bg=BG_COLOUR)
        self.left.propagate(0)
        self.basic.pack(side="top", fill="x")
        self.left.pack(side='left', padx=15, pady=5, fill='y', expand=False)
        self.right.pack(side='right', padx=5, pady=5, fill='both', expand=True)
        self.left.propagate(0)
        main_title(self.left, text='Chord Progression Generator', side='top')
        # button(self.right, False, None, None, None, 'top', 10, 'TButton')


class PianoRoll(NoteBookBasic):
    def __init__(self, frame):
        super().__init__(frame)
        self.Canvas = CPGCanvas(self.right)


class DrawCPGCanvas(NoteBookBasic):
    ...


class Logging(NoteBookBasic):
    ...


class Help(NoteBookBasic):
    ...


if __name__ == '__main__':
    player = pm.Output(0)
    # Tkinter窗口
    window = tk.Tk()  # 窗口对象
    TransparentColor = 'gray'
    window.wm_attributes("-transparentcolor", TransparentColor)
    set_window(window)
    BTStyle = ttk.Style()
    BTStyle.configure('TButton', borderradius=10, font=(FONT0, 12))
    CBStyle = ttk.Style()
    CBStyle.configure('TCombox', borderradius=10, font=(FONT0, 12))
    FStyle = ttk.Style()
    FStyle.configure('1.TFrame', background=BG_COLOUR)
    FStyle2 = ttk.Style()
    FStyle2.configure('2.TFrame', background='tan')
    # ico109 = Image.open(os.path.join(own_path, 'images/ico2_109.png'))
    # photo = ImageTk.PhotoImage(ico109)
    Bottom = BottomFrame(window)
    notebook = ttk.Notebook(window)
    PianoRoll_Frame = tk.Frame(bg=BG_COLOUR)
    Draw_Frame = tk.Frame(bg=BG_COLOUR)
    Log_Frame = tk.Frame(bg=BG_COLOUR)
    Help_Frame = tk.Frame(bg=BG_COLOUR)
    notebook.add(PianoRoll_Frame, text='   Piano roll   ')
    notebook.add(Draw_Frame, text=' Draw&Generate ')
    notebook.add(Log_Frame, text='     Logging     ')
    notebook.add(Help_Frame, text='        Help       ')
    notebook.pack(fill='x', side='top')
    Pianoroll = PianoRoll(PianoRoll_Frame)
    DrawCanvas = DrawCPGCanvas(Draw_Frame)
    Log = Logging(Log_Frame)
    Help = Help(Help_Frame)
    Pianoroll.Canvas.draw_chord(Chord([48, 55, 60, 64]), 4, 4)
    Pianoroll.Canvas.draw_chord(Chord([47, 55, 62, 65]), 8, 4)
    s1 = MusicxmlReader('scores/example.musicxml')
    window.mainloop()
