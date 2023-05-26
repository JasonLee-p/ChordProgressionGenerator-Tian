from threading import Thread
import pygame.midi as pm
# from PIL import Image, ImageTk
from tkwebview2.tkwebview2 import WebView2
from pyPCS import Chord
from TkGUI import *
from musicxmlReader import *
import queue


class BottomFrame:
    """
    The bottom frame of the main window.
    """
    def __init__(self, frame):
        self.basic = tk.Frame(master=frame, bg='ivory', height=250)
        self.basic.pack(side='bottom', fill='x', expand=False)
        self.basic.propagate(0)


class LeftFrame:
    """
    The left frame of the main window, which contains the entry box, the start button and the play button.
    """
    def __init__(self, frame):
        self.basic = tk.Frame(master=frame, bg=BG_COLOUR, width=320)
        self.basic.propagate(0)
        self.basic.pack(side='left', padx=15, pady=5, fill='y', expand=False)
        main_title(self.basic, text='Chord Progression Generator', side='top')
        self.entryBox = EntryBoxMouseWheel(
            self.basic, None,
            position='top', font=(FONT0, FONT_SIZE), width=10, default='16', setRange=[8, 64], _queue=beat_q)
        self.startButton = button(self.basic, False, None, self.start_generating, 'Start', 'top', width=10)
        self.playButton = button(self.basic, False, None, self.start_playing, 'Play', 'top', width=10)
        self.clearButton = None

    def init_clearButton(self):
        """
        Initialize the clear button.
        """
        self.clearButton = button(self.basic, False, None, DrawCanvas.clear_cv, 'Clear', 'top', width=10)

    def start_generating(self):
        """
        Start generating the chord progression.
        """
        if DrawCanvas.Canvas.line_num != 2:
            return
        # Disable the entry box and the start button.
        self.entryBox.box.config(state='disabled')
        self.startButton.config(state='disabled')
        self.clearButton.config(state='disabled')
        values = self.get_values_and_draw()
        print(values)
        # Generate the chord progression.

        # Restore the entry box and the start button.
        self.entryBox.box.config(state='normal')
        self.startButton.config(state='normal')
        self.clearButton.config(state='normal')

    @staticmethod
    def get_values_and_draw():
        """
        Get the values from the entry box and draw dots on the canvas.
        :return: values: a dictionary containing the values from the entry box.
        """
        cv_wid = DrawCanvas.Canvas.cv.winfo_width() - 2 * DrawCanvas.padx
        x_values = [(_i * cv_wid / int(DrawCanvas.beats) + DrawCanvas.padx) for _i in DrawCanvas.split_points]
        x_values.append(45)
        x_values.append(45 + cv_wid)
        x_values.sort()
        _split_points = DrawCanvas.split_points
        _split_points.append(0)
        _split_points.append(int(DrawCanvas.beats))
        _split_points.sort()
        values = {}
        # find the line that go through x_value and calculate the y value.
        for x_value in x_values:
            y_value0 = 0
            y_value1 = 0
            for line in DrawCanvas.Canvas.freshness_lines:
                x1, y1, x2, y2 = DrawCanvas.Canvas.cv.coords(line)
                if x1 <= x_value <= x2:
                    # y = kx + b
                    k = (y2 - y1) / (x2 - x1)
                    b = y1 - k * x1
                    y_value0 = k * x_value + b
                    DrawCanvas.Canvas.cv.create_oval(x_value - 5, y_value0 - 5, x_value + 5, y_value0 + 5,
                                                     fill='ivory', outline='firebrick', width=3, tag='color_point0')
            for line in DrawCanvas.Canvas.tension_lines:
                x1, y1, x2, y2 = DrawCanvas.Canvas.cv.coords(line)
                if x1 <= x_value <= x2:
                    k = (y2 - y1) / (x2 - x1)
                    b = y1 - k * x1
                    y_value1 = k * x_value + b
                    DrawCanvas.Canvas.cv.create_oval(x_value - 5, y_value1 - 5, x_value + 5, y_value1 + 5,
                                                     fill='ivory', outline='steelblue', width=3, tag='color_point1')
            cv_h = DrawCanvas.Canvas.cv.winfo_height()  # canvas height
            if y_value0 < DrawCanvas.pady:
                y_value0 = DrawCanvas.pady
            elif y_value0 > cv_h - DrawCanvas.pady * 2:
                y_value0 = cv_h - DrawCanvas.pady * 2
            if y_value1 < DrawCanvas.pady:
                y_value1 = DrawCanvas.pady
            elif y_value1 > cv_h - DrawCanvas.pady * 2:
                y_value1 = cv_h - DrawCanvas.pady * 2
            values[_split_points[x_values.index(x_value)]] = [
                20 * (cv_h - y_value0 - DrawCanvas.pady) / (cv_h - DrawCanvas.pady * 2),
                20 * (cv_h - y_value1 - DrawCanvas.pady) / (cv_h - DrawCanvas.pady * 2)
            ]
        return values

    def start_playing(self):
        ...


class PianoRoll:
    """
    The piano roll frame of the main window, which contains the piano roll and the scroll bar.
    """
    def __init__(self, master):
        self.MouseState = 'out'
        self.piano_keys_frames = []
        self.keyIndex2midi = dict(zip(range(1, 89), range(108, 19, -1)))
        self.midi2keyIndex = dict(zip(range(108, 19, -1), range(1, 89)))
        self.key_height = 12
        self.bw = 25
        self.width = 400
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
        for j in range(88):
            if j % 12 in [0, 1, 3, 5, 7, 8, 10]:
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
        """
        滚动条函数
        :param ent: scroll event
        :return:
        """
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
        """
        鼠标滚轮事件
        :param ent:
        :return:
        """
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
    """
    """
    def __init__(self, frame):
        self.Canvas = CPGCanvas(frame)
        self.Canvas.cv.bind('<Configure>', self.window_resize)
        self.Canvas.cv.update()
        self.padx = 45
        self.pady = 45
        self.height = self.Canvas.cv.winfo_height()
        self.width = self.Canvas.cv.winfo_width()
        self.range = Left.entryBox.range[1]
        self.beats = beat_q.get()
        self.split_points = []
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
        for j in range(self.range + 1):
            text = self.Canvas.cv.create_text(
                self.padx + j * self.frame, self.height - 30,
                text=j, font=(FONT0, FONT_SIZE), fill='black', tags=f'text{j}')
            self.Canvas.cv.tag_bind(text, '<Button-1>', self.on_text_click)
            if not j % 4 and j:
                self.Canvas.cv.create_line(
                    self.padx + j * self.frame, self.pady + 1,
                    self.padx + j * self.frame, self.height - self.pady - 1,
                    width=2, fill=BG_COLOUR, tags=f'line{j}')
            elif j:
                self.Canvas.cv.create_line(
                    self.padx + j * self.frame, self.pady + 1,
                    self.padx + j * self.frame, self.height - self.pady - 1,
                    width=2, fill='ivory', tags=f'line{j}')
        _t = Thread(target=self.change_beat, args=[beat_q, ])
        _t.daemon = True
        _t.start()

    def on_text_click(self, ent):
        """
        点击小节线数字事件，切换小节线颜色，记录切分点，切分点为小节线数字，切分点为红色，未切分点为黑色。
        :param ent:
        :return:
        """
        text_id = ent.widget.find_closest(ent.x, ent.y)[0]
        text_tag = ent.widget.gettags(text_id)[0]
        text_i = int(text_tag[4:])
        if text_i and text_i != int(self.beats):
            if text_color := ent.widget.itemcget(text_id, 'fill') == 'black':
                self.Canvas.cv.itemconfig(text_tag, fill='firebrick')
                self.Canvas.cv.itemconfig(f'line{text_i}', fill='firebrick')
                self.split_points.append(int(text_i))
            elif not text_i % 4:
                self.Canvas.cv.itemconfig(text_tag, fill='black')
                self.Canvas.cv.itemconfig(f'line{text_i}', fill=BG_COLOUR)
                self.split_points.append(int(text_i))
            else:
                self.Canvas.cv.itemconfig(text_tag, fill='black')
                self.Canvas.cv.itemconfig(f'line{text_i}', fill='ivory')
                self.split_points.pop(int(text_i))

    def change_beat(self, q):
        """
        修改需要生成的总拍数，修改后，重新计算小节线位置，修改小节线位置，修改小节线数字位置。
        :param q: 拍数队列
        :return:
        """
        while True:
            Pianoroll.width = int(q.get()) * Pianoroll.bw
            Pianoroll.cvFrame.configure(width=Pianoroll.width)
            Pianoroll.canvas.configure(
                scrollregion=(0, 0, Pianoroll.width, 90 * (Pianoroll.key_height + 1)),  # TODO:
                width=Pianoroll.width  # TODO:
            )
            self.beats = q.get()
            self.frame = (self.width - self.padx * 2) / int(self.beats)
            for _i in range(self.range + 1):
                self.Canvas.cv.coords(f"text{_i}", self.padx + _i * self.frame, self.height - 30)
                if _i:
                    self.Canvas.cv.coords(
                        f"line{_i}",
                        self.padx + _i * self.frame, self.pady + 1,
                        self.padx + _i * self.frame, self.height - self.pady - 1)

    def window_resize(self, ent):
        """
        窗口大小改变事件，重新计算小节线位置，修改小节线位置，修改小节线数字位置。
        :param ent:
        :return:
        """
        self.height = ent.height
        self.width = ent.width
        try:
            self.frame = (self.width - self.padx * 2) / int(self.beats)
            self.Canvas.cv.coords(
                "ordinate", self.padx, self.pady - 1, self.padx, self.height - self.pady + 1)
            self.Canvas.cv.coords(
                "abscissa", self.padx, self.height - self.pady, self.width - self.padx + 1, self.height - self.pady)
            self.Canvas.cv.coords(
                "abscissa2", self.padx, self.pady, self.width - self.padx + 1, self.pady)
            for j in range(self.range + 1):
                self.Canvas.cv.coords(f"text{j}", self.padx + j * self.frame, self.height - 30)
                if j:
                    self.Canvas.cv.coords(
                        f"line{j}",
                        self.padx + j * self.frame, self.pady + 1,
                        self.padx + j * self.frame, self.height - self.pady - 1)
        except AttributeError:
            pass

    def clear_cv(self):
        """
        清除画布上绘制的和生成的内容，包括小节线，小节线数字，颜色点，颜色线。
        :return:
        """
        self.Canvas.cv.delete('draw0', 'draw1', 'color_point0', 'color_point1')
        self.Canvas.line_num = 0
        self.Canvas.freshness_lines.clear()
        self.Canvas.X.set(0)
        self.Canvas.Y.set(0)
        self.Canvas.lastline = 0


class Logging:
    def __init__(self, frame):
        self.frame = frame
        self.text = tk.Text(frame, font=(FONT0, FONT_SIZE))
        self.text.pack(expand=True, fill=tk.BOTH)
        self.text.tag_config('info', foreground='green')
        self.text.tag_config('warning', foreground='orange')
        self.text.tag_config('error', foreground='red')
        self.text.tag_config('debug', foreground='blue')
        self.text.tag_config('critical', foreground='red', background='yellow')
        self.text.tag_config('default', foreground='black')
        self.text.tag_config('help', foreground='darkblue')
        self.text.tag_config('command', foreground='darkgreen')
        self.text.tag_config('result', foreground='darkblue')
        self.text.tag_config('input', foreground='darkgreen')
        self.text.tag_config('output', foreground='darkblue')
        self.text.tag_config('file', foreground='darkblue')
        self.text.tag_config('select', foreground='darkgreen')


class Help:
    def __init__(self, frame):
        web_frame = WebView2(frame, frame.winfo_width(), frame.winfo_height(), bg=BG_COLOUR)
        web_frame.load_url('https://zhuanlan.zhihu.com/p/580555176')
        web_frame.pack(side='right', fill='both', expand=True)


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
    player = pm.Output(0)  # 初始化音频输出
    # Tkinter窗口
    window = tk.Tk()
    TransparentColor = 'gray'
    window.wm_attributes("-transparentcolor", TransparentColor)
    set_window(window)
    # 图片
    # ico109 = Image.open(os.path.join(own_path, 'images/ico2_109.png'))
    # photo = ImageTk.PhotoImage(ico109)

    beat_q = queue.Queue()  # 拍数队列

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
    chord_group = [
        Chord([48, 55, 60, 64]),
        Chord([47, 55, 62, 65]),
        Chord([48, 57, 60, 65]),
        Chord([52, 55, 60, 67]),
        Chord([53, 57, 60, 72]),
        Chord([48, 55, 60, 71]),
        Chord([53, 57, 60, 72]),
        Chord([47, 55, 62, 74]),
    ]
    for i in range(len(chord_group)):
        Pianoroll.draw_chord(chord_group[i], i * 2, 2)


    def play():
        for chord in chord_group:
            chord.play(player, 2)


    t = Thread(target=play)
    t.daemon = True
    t.start()

    # s1 = MusicxmlReader('scores/example.musicxml')
    # s1.get_start_beat()
    window.mainloop()
