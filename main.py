from threading import Thread

import pygame.midi as pm
# from PIL import Image, ImageTk
from pyPCS import Chord
from TkGUI import *
# from musicxmlReader import *
import queue


class BottomFrame:
    def __init__(self, frame):
        self.basic = tk.Frame(master=frame, bg='ivory', height=250)
        self.basic.pack(side='bottom', fill='x', expand=False)
        self.basic.propagate(0)
        self.entryBox = EntryBoxMouseWheel(
            self.basic, None,
            position='top', font=(FONT0, FONT_SIZE), width=10, default='8', setRange=[4, 36], _queue=beat_q)
        self.startButton = button(self.basic, False, None, self.start_generating, 'Start', 'top', width=10)

    def start_generating(self):
        ...


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
        self.Canvas = PianoRollCV(self.right)


class DrawCPGCanvas(NoteBookBasic):
    def __init__(self, frame):
        super().__init__(frame)
        self.Canvas = CPGCanvas(self.right)
        self.Canvas.cv.bind('<Configure>', self.window_resize)
        self.Canvas.cv.update()
        self.height = self.Canvas.cv.winfo_height()
        self.width = self.Canvas.cv.winfo_width()
        self.padx = 45
        self.pady = 45
        self.beats = beat_q.get()
        self.frame = (self.width - self.padx * 2) / int(self.beats)
        self.Canvas.cv.create_line(self.padx, self.padx, self.padx, self.height - self.pady + 1,
                                   fill='tan', width=2, tags='line1')
        self.Canvas.cv.create_line(self.padx, self.height - self.pady, self.width - self.padx, self.height - self.pady,
                                   fill='tan', width=2, tags='line2')
        self.Canvas.cv.create_text(30, 45,
                                   text=20, font=(FONT0, FONT_SIZE2), fill='black', tags=f't0')
        for i in range(37):
            self.Canvas.cv.create_text(
                self.width - self.padx, self.height - 30,
                text=i, font=(FONT0, FONT_SIZE2), fill='black', tags=f'text{i}')
        t = Thread(target=self.change_beat, args=[beat_q, ])
        t.daemon = True
        t.start()

    def change_beat(self, q):
        while True:
            self.beats = q.get()
            self.frame = (self.width - self.padx * 2) / int(self.beats)
            for i in range(37):
                self.Canvas.cv.coords(f"text{i}", self.padx + i * self.frame, self.height - 30)

    def window_resize(self, ent):
        self.height = ent.height
        self.width = ent.width
        self.frame = (self.width - self.padx * 2) / int(self.beats)
        self.Canvas.cv.coords(
            "line1", self.padx, self.padx, self.padx, self.height - self.pady + 1)
        self.Canvas.cv.coords(
            "line2", self.padx, self.height - self.pady, self.width - self.padx, self.height - self.pady)
        for i in range(37):
            self.Canvas.cv.coords(f"text{i}", self.padx + i * self.frame, self.height - 30)


class Logging(NoteBookBasic):
    ...


class Help(NoteBookBasic):
    ...


def set_ttk():
    # 设置ttk样式
    BTStyle = ttk.Style()
    BTStyle.configure('TButton', borderradius=10, font=(FONT0, 15))
    CBStyle = ttk.Style()
    CBStyle.configure('TCombox', borderradius=10, font=(FONT0, 15))
    FStyle = ttk.Style()
    FStyle.configure('1.TFrame', background=BG_COLOUR)
    FStyle2 = ttk.Style()
    FStyle2.configure('2.TFrame', background='tan')


if __name__ == '__main__':
    player = pm.Output(0)
    # Tkinter窗口
    window = tk.Tk()  # 窗口对象
    TransparentColor = 'gray'
    window.wm_attributes("-transparentcolor", TransparentColor)
    set_window(window)
    # 图片
    # ico109 = Image.open(os.path.join(own_path, 'images/ico2_109.png'))
    # photo = ImageTk.PhotoImage(ico109)
    # 全局队列
    beat_q = queue.Queue()

    notebook = ttk.Notebook(window)
    Bottom = BottomFrame(window)
    # 初始化标签页
    PianoRoll_Frame = tk.Frame(bg=BG_COLOUR)
    Draw_Frame = tk.Frame(bg=BG_COLOUR)
    Log_Frame = tk.Frame(bg=BG_COLOUR)
    Help_Frame = tk.Frame(bg=BG_COLOUR)
    # 加入，打包绘制
    notebook.add(PianoRoll_Frame, text='   Piano roll   ')
    notebook.add(Draw_Frame, text=' Draw&Generate ')
    notebook.add(Log_Frame, text='     Logging     ')
    notebook.add(Help_Frame, text='        Help       ')
    notebook.pack(fill='x', side='top')
    # 绘制
    Pianoroll = PianoRoll(PianoRoll_Frame)
    DrawCanvas = DrawCPGCanvas(Draw_Frame)
    Log = Logging(Log_Frame)
    Help = Help(Help_Frame)
    #
    Pianoroll.Canvas.draw_chord(Chord([48, 55, 60, 64]), 4, 4)
    Pianoroll.Canvas.draw_chord(Chord([47, 55, 62, 65]), 8, 4)
    # s1 = MusicxmlReader('scores/example.musicxml')
    window.mainloop()
