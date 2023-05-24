from threading import Thread
import pygame.midi as pm
# from PIL import Image, ImageTk
from pyPCS import Chord
from TkGUI import *
from musicxmlReader import *
import queue


class BottomFrame:
    def __init__(self, frame):
        self.basic = tk.Frame(master=frame, bg='ivory', height=250)
        self.basic.pack(side='bottom', fill='x', expand=False)
        self.basic.propagate(0)


class LeftFrame:
    def __init__(self, frame):
        self.basic = tk.Frame(master=frame, bg=BG_COLOUR, width=320)
        self.basic.propagate(0)
        self.basic.pack(side='left', padx=15, pady=5, fill='y', expand=False)
        main_title(self.basic, text='Chord Progression Generator', side='top')
        self.entryBox = EntryBoxMouseWheel(
            self.basic, None,
            position='top', font=(FONT0, FONT_SIZE), width=10, default='8', setRange=[8, 64], _queue=beat_q)
        self.startButton = button(self.basic, False, None, self.start_generating, 'Start', 'top', width=10)
        self.playButton = button(self.basic, False, None, self.start_playing, 'Play', 'top', width=10)
        self.clearButton = None

    def init_clearButton(self):
        self.clearButton = button(self.basic, False, None, DrawCanvas.clear_cv, 'Clear', 'top', width=10)

    def start_generating(self):
        ...

    def start_playing(self):
        ...


class PianoRoll:
    def __init__(self, master):
        self.MouseState = 'out'
        self.piano_keys_frames = []
        self.keyIndex2midi = dict(zip(range(1, 89), range(108, 19, -1)))
        self.midi2keyIndex = dict(zip(range(108, 19, -1), range(1, 89)))
        self.key_height = 12
        self.bw = 25
        self.width = 200
        self.canvas = tk.Canvas(master=master, height=700, bg=BG_COLOUR, bd=0)
        self.top_sb = tk.Scrollbar(
            master, relief='raised', troughcolor=BG_COLOUR, width=15, orient='horizontal',
            command=self.canvas.xview
        )  # 定义水平滚动条
        self.left_sb = tk.Scrollbar(
            master, relief='raised', troughcolor=BG_COLOUR, width=15, orient='vertical',
            command=self.canvas.yview
        )  # 定义水平滚动条
        self.left_sb.pack(side='left', fill='y')
        self.top_sb.pack(side='top', fill='x')  # 放置垂直滚动条在顶部,占满x轴
        self.cvFrame = tk.Frame(self.canvas, height=90 * (self.key_height + 1), width=self.width)  # 画布滚动区域
        self.cvFrame.propagate(0)
        self.piano_keys_frames.append(
            f_ := tk.Frame(self.cvFrame, bg=BG_COLOUR, height=self.key_height, bd=0))
        f_.pack(side='top', fill='x', padx=0)
        # 绘制分割线
        for j in range(1, (4 * self.width) // self.bw):
            tk.Frame(self.cvFrame, bg='#222222', width=1, height=50).place(
                x=j * 4 * self.bw, y=0)
        # 绘制键盘
        for i in range(88):
            if i % 12 in [0, 1, 3, 5, 7, 8, 10]:
                wk = tk.Frame(self.cvFrame, bg='#555555', height=self.key_height, bd=0)
                wk.pack(side='top', fill='x', padx=0)
                self.piano_keys_frames.append(wk)
            else:
                bk = tk.Frame(self.cvFrame, bg='#464646', height=12, bd=0)
                bk.pack(side='top', fill='x', padx=0)
                self.piano_keys_frames.append(bk)
            tk.Frame(self.cvFrame, bg='#222222', height=1, bd=0).pack(
                side='top', fill='x', padx=0)

        self.piano_keys_frames.append(
            _f := tk.Frame(self.cvFrame, bg=BG_COLOUR, height=self.key_height, bd=0))
        _f.pack(side='top', fill='x', padx=0)
        # TODO: 钢琴
        self.canvas.create_window((0, 0), window=self.cvFrame, anchor='nw')
        self.canvas.pack(side='top', padx=20, fill='both')
        self.canvas.bind("<Configure>", self.rolling_func)  # 绑定滚动条
        self.canvas.bind("<Enter>", self.enter_func)  # 进入
        self.canvas.bind("<Leave>", self.leave_func)  # 离开
        self.cvFrame.bind_all("<MouseWheel>", self.cv_mousewheel)  # 绑定鼠标
        self.cvFrame.bind_all("<Shift-MouseWheel>", self.cv_mousewheel)  # 绑定shift
        self.cvFrame.bind_all("<Control-MouseWheel>", self.cv_mousewheel)  # 绑定Ctrl
        master.update()

    def change_beat(self, q):
        while True:
            self.width = int(q.get()) * self.bw
            self.cvFrame.configure(width=self.width)

    def rolling_func(self, ent):
        self.canvas.configure(
            xscrollcommand=self.top_sb.set,
            yscrollcommand=self.left_sb.set,
            scrollregion=(0, 0, self.width, 90 * (self.key_height + 1)),
            width=self.width
        )

    def enter_func(self, ent):
        self.MouseState = 'in'

    def leave_func(self, ent):
        self.MouseState = 'out'

    def cv_mousewheel(self, ent):
        if self.MouseState == 'in':
            if ent.state == 0:
                self.canvas.yview_scroll(ent.delta // -120, "units")
            elif ent.state == 4:
                # if 7 < self.key_height < 35:
                if ent.delta < 0:
                    self.key_height -= 1
                elif ent.delta > 0:
                    self.key_height += 1
                for key_f in self.piano_keys_frames:
                    key_f.configure(height=self.key_height)
                    self.canvas.configure(scrollregion=(0, 0, self.width, 90 * (1 + self.key_height)))
                    self.cvFrame.configure(height=90 * (1 + self.key_height))
                if self.key_height <= 7:
                    self.key_height = 8
                elif self.key_height >= 35:
                    self.key_height = 34
            else:
                self.canvas.xview_scroll(ent.delta // -120, "units")

    def draw_note(self, note, start_beat, duration):
        keyI = self.midi2keyIndex[note]
        tk.Frame(self.piano_keys_frames[keyI], bg='burlywood',
                 width=duration * self.bw - 1, height=40).place(
            x=start_beat * self.bw, y=0)

    def draw_chord(self, chord_obj, start_beat, duration):
        for note in chord_obj.pitch_group:
            keyI = self.midi2keyIndex[note]
            tk.Frame(self.piano_keys_frames[keyI], bg='burlywood',
                     width=duration * self.bw - 1, height=40).place(
                x=start_beat * self.bw, y=0)


class DrawCPGCanvas:
    def __init__(self, frame):
        self.Canvas = CPGCanvas(frame)
        self.Canvas.cv.bind('<Configure>', self.window_resize)
        self.Canvas.cv.update()
        self.height = self.Canvas.cv.winfo_height()
        self.width = self.Canvas.cv.winfo_width()
        self.padx = 45
        self.pady = 45
        self.range = Left.entryBox.range[1]
        self.beats = beat_q.get()
        self.frame = (self.width - self.padx * 2) / int(self.beats)
        self.Canvas.cv.create_line(self.padx, self.pady - 1, self.padx, self.height - self.pady + 1,
                                   fill='tan', width=2, tags='ordinate')
        self.Canvas.cv.create_line(self.padx, self.height - self.pady,
                                   self.width - self.padx + 1, self.height - self.pady,
                                   fill='tan', width=2, tags='abscissa')
        self.Canvas.cv.create_line(self.padx, self.pady,
                                   self.width - self.padx + 1, self.pady,
                                   fill='tan', width=2, tags='abscissa2')
        self.Canvas.cv.create_text(25, self.pady,
                                   text=20, font=(FONT0, FONT_SIZE), fill='black', tags=f't0')
        for i in range(self.range + 1):
            text = self.Canvas.cv.create_text(
                self.padx + i * self.frame, self.height - 30,
                text=i, font=(FONT0, FONT_SIZE), fill='black', tags=f'text{i}')
            self.Canvas.cv.tag_bind(text, '<Button-1>', self.on_text_click)
            if not i % 4 and i:
                self.Canvas.cv.create_line(
                    self.padx + i * self.frame, self.pady + 1,
                    self.padx + i * self.frame, self.height - self.pady - 1,
                    width=2, fill=BG_COLOUR, tags=f'line{i}')
            elif i:
                self.Canvas.cv.create_line(
                    self.padx + i * self.frame, self.pady + 1,
                    self.padx + i * self.frame, self.height - self.pady - 1,
                    width=2, fill='ivory', tags=f'line{i}')
        t = Thread(target=self.change_beat, args=[beat_q, ])
        t.daemon = True
        t.start()

    def on_text_click(self, ent):
        text_id = ent.widget.find_closest(ent.x, ent.y)[0]
        text_tag = ent.widget.gettags(text_id)[0]
        text_i = int(text_tag[4:])
        if text_i != 0 and text_i != int(self.beats):
            if text_color := ent.widget.itemcget(text_id, 'fill') == 'black':
                self.Canvas.cv.itemconfig(text_tag, fill='firebrick')
                self.Canvas.cv.itemconfig(f'line{text_i}', fill='firebrick')
            elif not text_i % 4:
                self.Canvas.cv.itemconfig(text_tag, fill='black')
                self.Canvas.cv.itemconfig(f'line{text_i}', fill=BG_COLOUR)
            else:
                self.Canvas.cv.itemconfig(text_tag, fill='black')
                self.Canvas.cv.itemconfig(f'line{text_i}', fill='ivory')

    def change_beat(self, q):
        while True:
            Pianoroll.width = int(q.get()) * Pianoroll.bw
            Pianoroll.cvFrame.configure(width=Pianoroll.width)
            Pianoroll.canvas.configure(
                scrollregion=(0, 0, Pianoroll.width, 90 * (Pianoroll.key_height + 1)),  # TODO:
                width=Pianoroll.width  # TODO:
            )
            self.beats = q.get()
            self.frame = (self.width - self.padx * 2) / int(self.beats)
            for i in range(self.range + 1):
                self.Canvas.cv.coords(f"text{i}", self.padx + i * self.frame, self.height - 30)
                if i:
                    self.Canvas.cv.coords(
                        f"line{i}",
                        self.padx + i * self.frame, self.pady + 1,
                        self.padx + i * self.frame, self.height - self.pady - 1)

    def window_resize(self, ent):
        self.height = ent.height
        self.width = ent.width
        self.frame = (self.width - self.padx * 2) / int(self.beats)
        self.Canvas.cv.coords(
            "ordinate", self.padx, self.pady - 1, self.padx, self.height - self.pady + 1)
        self.Canvas.cv.coords(
            "abscissa", self.padx, self.height - self.pady, self.width - self.padx + 1, self.height - self.pady)
        self.Canvas.cv.coords(
            "abscissa2", self.padx, self.pady, self.width - self.padx + 1, self.pady)
        for i in range(self.range + 1):
            self.Canvas.cv.coords(f"text{i}", self.padx + i * self.frame, self.height - 30)
            if i:
                self.Canvas.cv.coords(
                    f"line{i}",
                    self.padx + i * self.frame, self.pady + 1,
                    self.padx + i * self.frame, self.height - self.pady - 1)

    def clear_cv(self):
        self.Canvas.cv.delete('draw')


class Logging:
    def __init__(self, frame):
        ...


class Help:
    def __init__(self, frame):
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
    Left = LeftFrame(window)
    # 初始化标签页
    Draw_Frame = tk.Frame(bg=BG_COLOUR)
    PianoRoll_Frame = tk.Frame(bg=BG_COLOUR)
    Log_Frame = tk.Frame(bg=BG_COLOUR)
    Help_Frame = tk.Frame(bg=BG_COLOUR)
    # 加入，打包绘制
    notebook.add(Draw_Frame, text=' Draw&Generate ')
    notebook.add(PianoRoll_Frame, text='   Piano roll   ')
    notebook.add(Log_Frame, text='     Logging     ')
    notebook.add(Help_Frame, text='        Help       ')
    notebook.pack(fill='both', side='right', expand=True)
    # 绘制
    DrawCanvas = DrawCPGCanvas(Draw_Frame)
    Left.init_clearButton()
    Pianoroll = PianoRoll(PianoRoll_Frame)
    Log = Logging(Log_Frame)
    Help = Help(Help_Frame)
    #
    Pianoroll.draw_chord(Chord([48, 55, 60, 64]), 4, 4)
    Pianoroll.draw_chord(Chord([47, 55, 62, 65]), 8, 4)
    s1 = MusicxmlReader('scores/example.musicxml')
    s1.get_start_beat()
    window.mainloop()
