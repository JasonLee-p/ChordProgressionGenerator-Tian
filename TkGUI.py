# -*- coding: utf-8 -*-
"""

"""
import ctypes
import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
# from tkinter import filedialog
import os

BG_COLOUR = 'Beige'  # 背景色
FONT0 = 'microsoft yahei'
FONT1 = 'microsoft yahei'
FONT_SIZE = 12
FONT_SIZE2 = 10
own_path = os.path.dirname(__file__)


def set_window(window):
    """
    initialize the window, set the window size, title, icon, etc.
    :param window: tk.Tk() object.
    """
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # 告诉操作系统使用程序自身的dpi适配
    ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)  # 获取屏幕的缩放因子
    window.tk.call('tk', 'scaling', ScaleFactor / 75)  # 设置程序缩放
    try:
        window.state("zoomed")
    except tk.TclError:
        w = window.winfo_screenwidth()
        h = window.winfo_screenheight()
        window.geometry("%dx%d" % (w, h))
    # master.iconbitmap(os.path.join(os.path.dirname(own_path), 'images/icon.ico'))  # 更改窗口图标
    window.title('Chord Progression Generator')  # 窗口名
    window.minsize(1200, 860)
    window.configure(bg=BG_COLOUR)  # 背景色


def main_title(master, text, side):
    tk.Frame(master=master, bg=BG_COLOUR, height=10).pack(side='top', fill='x')
    title_v = tk.Label(
        master,
        text=text,  # 标签的文字
        bg=BG_COLOUR,  # 标签背景颜色
        font=(FONT1, 11),  # 字体和字体大小
        width=30, height=1)  # 标签长宽
    title_v.pack(side=side, pady=0, expand=False, anchor='center')  # 固定窗口位置
    tk.Frame(master=master, bg=BG_COLOUR, height=6).pack(side='top', fill='x')
    tk.Frame(master=master, bg='ivory', height=4).pack(side='top', fill='x')


# 显示的音符名
def title(title_text_var, bg_colour):
    def _title(belonging, master, position, font_size, expand, wid, hei, fill=None, padx=0, pady=0, ipadx=0, ipady=0):
        _title_v = tk.Label(
            master,
            textvariable=title_text_var,  # 标签的文字
            bg=bg_colour,  # 标签背景颜色
            font=(FONT0, font_size),  # 字体和字体大小
            width=wid, height=hei)  # 标签长宽
        _title_v.pack(side=position, fill=fill, padx=padx, pady=pady, expand=expand, ipadx=ipadx, ipady=ipady)  # 固定窗口位置
        if belonging:
            belonging.append(_title_v)
        title_text_var.set('')
        return _title_v

    return _title


def button(master, expand, belonging, hit_func, text, side, width):
    BTStyle = ttk.Style()
    BTStyle.configure('TButton', borderradius=5, font=(FONT0, FONT_SIZE))
    b = ttk.Button(master, text=text, width=width, command=hit_func, style='TButton')
    b.configure()
    b.pack(side=side, padx=5, pady=4, expand=expand)
    if belonging:
        belonging.append(b)
    return b


# 定义下拉选择框
def combox(master, belonging, selected_func, values, position='basic', width=19, height=5, style_name=None):
    text_var = tk.StringVar()
    cb = ttk.Combobox(
        master, textvariable=text_var, state='readonly',
        font=(FONT0, FONT_SIZE), width=width, height=height,
        values=values
    )
    if style_name:
        cb.configure(style=style_name)
    cb.bind("<<ComboboxSelected>>", selected_func)  # 绑定事件(下拉列表框被选中时，绑定函数selected_func)
    cb.bind("<Leave>", selected_func)  # 绑定事件(鼠标离开时，绑定函数selected_func)
    # _combox.bind("<Return>", selected_func)  # 绑定事件(下拉列表框被选中时，绑定函数selected_func)
    cb.pack(side=position, padx=5)
    if belonging:
        belonging.append(cb)
    return cb


def column_selected(name):
    messagebox.showinfo('', f'{name}')


def logging_f(master):
    columns = ['Date', 'Time', 'Sheet', 'Score']
    TVStyle = ttk.Style()
    TVStyle.configure('Treeview', rowheight=45, font=(FONT0, 12))
    VScroll1 = tk.Scrollbar(
        master, relief='flat', troughcolor=BG_COLOUR, width=30, orient='vertical')
    VScroll1.pack(side='basic', fill='y', padx=0)
    table = ttk.Treeview(
        master=master,  # 父容器
        height=20,  # 表格显示的行数,height行
        columns=columns,  # 显示的列
        show='headings',  # 隐藏首列
        style='Treeview',
        yscrollcommand=VScroll1.set
    )

    def treeviewClick(ent):  # 单击
        print('单击')
        for item in table.selection():
            item_text = table.item(item, "values")
            print(item_text[0])  # 输出所选行的第一列的值

    for column in columns:
        table.heading(column=column, text=column, anchor=tk.CENTER,
                      command=lambda name=column:
                      column_selected(name)
                      )
        table.column(column=column, width=150, minwidth=150, anchor=tk.CENTER, )  # 定义列
    VScroll1.configure(command=table.yview)
    table.bind('<ButtonRelease-1>', treeviewClick)
    table.pack()
    table.yview_moveto(1)
    return table


def fill_tv_with_json(json_filepath, tv):
    with open(json_filepath, 'r') as rf:
        json_data = json.load(rf)
    for i in range(len(json_data['date'])):
        tv.insert(
            '', i,
            values=(json_data['date'][i], json_data['time'][i], json_data['sheet'][i], json_data['score'][i])
        )


def treeview_sort_column(treeview, column, reverse):  # Treeview、列名、排列方式
    lst = [(treeview.set(k, column), k) for k in treeview.get_children('')]
    print(treeview.get_children(''))
    lst.sort(reverse=reverse)
    # rearrange items in sorted positions
    for index, (val, k) in enumerate(lst):  # 根据排序后索引移动
        treeview.move(k, '', index)
        print(k)
    treeview.heading(column, command=lambda: treeview_sort_column(treeview, column, not reverse))  # 重写标题，使之成为再点倒序的标题


class PianoRollCV:
    """
    Piano roll Canvas, which shows the generated chord progressions.
    """
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
        # # 绘制分割线
        # for j in range(1, 3000 // self.bw + 1):
        #     tk.Frame(self.cvFrame, bg='#222222', width=1, height=1000).place(
        #         x=j * self.bw, y=0)
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

        def rolling_func(ent):
            self.canvas.configure(
                xscrollcommand=self.top_sb.set,
                yscrollcommand=self.left_sb.set,
                scrollregion=(0, 0, self.width, 90 * (self.key_height + 1)),  # TODO:
                width=self.width  # TODO:
            )

        self.canvas.bind("<Configure>", rolling_func)  # 绑定滚动条
        self.canvas.bind("<Enter>", self.enter_func)  # 进入
        self.canvas.bind("<Leave>", self.leave_func)  # 离开
        self.cvFrame.bind_all("<MouseWheel>", self.cv_mousewheel)  # 绑定鼠标
        self.cvFrame.bind_all("<Shift-MouseWheel>", self.cv_mousewheel)  # 绑定shift
        self.cvFrame.bind_all("<Control-MouseWheel>", self.cv_mousewheel)  # 绑定Ctrl
        master.update()

    # def change_beat(self, q):
    #     while True:
    #         self.width = q.get() * self.bw
    #         self.cvFrame.configure(width=self.width)

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


class CPGCanvas:
    """
    """
    def __init__(self, master):
        self.cv = tk.Canvas(master=master, bg="ivory", bd=0)
        self.cv.configure(highlightthickness=0)
        self.cv.bind('<Button-1>', self.onLeftButtonDown)
        self.cv.bind('<B1-Motion>', self.onLeftButtonMove)
        self.cv.bind('<ButtonRelease-1>', self.onLeftButtonUp)
        self.cv.bind('<ButtonRelease-3>', self.onRightButtonUp)
        self.cv.pack(fill='both', expand=True, pady=15, padx=15)
        self.LButtonState = tk.IntVar(value=0)
        self.X = tk.IntVar(value=45)
        self.Y = tk.IntVar(value=self.cv.winfo_height()-45)
        self.line_num = 0
        self.T = 5
        self.LINE_COLOR = 'black'
        self.L_width = 3
        self.lastline = 0
        self.freshness_lines = []
        self.tension_lines = []
        self.size = "20"
        self.Mode = 'Main'

    def onLeftButtonDown(self, ent):
        # print("c")
        if ent.x < 45 and 45 < ent.y < self.cv.winfo_height()-45 and self.line_num < 2:
            self.line_num += 1
            self.LButtonState.set(1)
            self.X.set(ent.x)
            if self.cv.winfo_height() - 45 > ent.y > 45:
                self.Y.set(ent.y)
            elif ent.y > self.cv.winfo_height() - 45:
                self.Y.set(self.cv.winfo_height() - 45)
            elif ent.y < 45:
                self.Y.set(45)
        elif self.X.get() < ent.x < self.cv.winfo_width() - 45:
            pass
        elif ent.x < 45 and 45 < ent.y < self.cv.winfo_height() - 45 and self.line_num == 2:
            messagebox.showinfo("", "You have created two lines.\nIf unsatisfied, you can press 'Clear' and redraw.",
                                parent=self.cv)

    def onLeftButtonMove(self, ent):
        if self.LButtonState.get() == 0:
            return
        if self.Mode == 'line':
            # try:
            #     self.cv.delete(self.lastline)
            # except Exception:
            #     pass
            self.cv.delete(self.lastline)
            self.lastline = self.cv.create_line(
                self.X.get(), self.Y.get(), ent.x, ent.y,
                fill=self.LINE_COLOR, width=self.L_width, tags=f'draw{self.line_num}')
        elif ent.x > self.X.get() and self.T >= 6:
            if ent.x < self.cv.winfo_width() - 45:  # 在结束区域之前
                if self.cv.winfo_height() - 45 > ent.y > 45:
                    self.lastline = self.cv.create_line(
                        self.X.get(), self.Y.get(), ent.x, ent.y,
                        fill=self.LINE_COLOR, width=self.L_width, tags=f'draw{self.line_num}')
                    self.Y.set(ent.y)
                elif ent.y > self.cv.winfo_height() - 45:  # 在结束区域
                    self.lastline = self.cv.create_line(
                        self.X.get(), self.Y.get(), ent.x, self.cv.winfo_height() - 45,
                        fill=self.LINE_COLOR, width=self.L_width, tags=f'draw{self.line_num}')
                    self.Y.set(self.cv.winfo_height() - 45)
                elif ent.y < 45:
                    self.lastline = self.cv.create_line(
                        self.X.get(), self.Y.get(), ent.x, 45,
                        fill=self.LINE_COLOR, width=self.L_width, tags=f'draw{self.line_num}')
                    self.Y.set(45)
                self.X.set(ent.x)
            else:
                self.lastline = self.cv.create_line(
                    self.X.get(), self.Y.get(), ent.x, ent.y,
                    fill=self.LINE_COLOR, width=self.L_width, tags=f'draw{self.line_num}')
                self.LButtonState.set(0)
            self.freshness_lines.append(self.lastline) if self.line_num == 1 \
                else self.tension_lines.append(self.lastline)
            self.T = 0
        self.T += 1
        # print(f"{self.X.get()}, {self.Y.get()}")

    def onLeftButtonUp(self, ent):
        """
        鼠标左键抬起，绘制最后一条线，将鼠标状态置为0
        """
        if self.X.get() < ent.x < self.cv.winfo_width() - 45 and self.LButtonState.get():
            if 45 > ent.y > self.cv.winfo_height() - 45:
                self.lastline = self.cv.create_line(
                    self.X.get(), self.Y.get(), ent.x, ent.y,
                    fill=self.LINE_COLOR, width=self.L_width, tags=f'draw{self.line_num}')
                self.Y.set(self.cv.winfo_height() - 45)
            elif ent.y > self.cv.winfo_height() - 45:
                self.lastline = self.cv.create_line(
                    self.X.get(), self.Y.get(), ent.x, self.cv.winfo_height() - 45,
                    fill=self.LINE_COLOR, width=self.L_width, tags=f'draw{self.line_num}')
                self.Y.set(self.cv.winfo_height() - 45)
            elif ent.y < 45:
                self.lastline = self.cv.create_line(
                    self.X.get(), self.Y.get(), ent.x, 45,
                    fill=self.LINE_COLOR, width=self.L_width, tags=f'draw{self.line_num}')
            self.X.set(ent.x)
            self.freshness_lines.append(self.lastline) if self.line_num == 1 \
                else self.tension_lines.append(self.lastline)
        elif ent.x > self.cv.winfo_width() and self.LButtonState.get():
            self.LButtonState.set(0)

    def onRightButtonUp(self, ent):
        pass


class EntryBoxMouseWheel:
    """
    可以鼠标滚动控制值的输入框，用于输入整数
    """
    def __init__(self, master, belonging, position, font, width, default,
                 setRange: list, touch_func=None, msWheel_func=None, _queue=None):
        self.get = default
        EStyle = ttk.Style()
        EStyle.configure('TEntry', borderradius=10)
        self.box = ttk.Entry(master, justify="center", font=font, width=width, style='TEntry')
        self.box.pack(side=position, expand=0)
        self.box.insert(0, default)
        if _queue:
            self.q = _queue
            self.q.put(default)
        if touch_func:
            self.box.bind("<Return>", touch_func)
            self.box.bind("<Button-1>", touch_func)
            self.box.bind("<Leave>", touch_func)
            # self.box.bind("<Enter>", touch_func)
        else:
            self.range = setRange
            self.box.bind("<Return>", self.get_beat)
            self.box.bind("<Enter>", self.get_beat)
            self.box.bind("<Button-1>", self.get_beat)
            self.box.bind("<Leave>", self.get_beat)
        if msWheel_func:
            self.box.bind("<MouseWheel>", msWheel_func)
        else:
            self.box.bind("<MouseWheel>", self.mouse_wheel_change)
        if belonging:
            belonging.append(self.box)

    def mouse_wheel_change(self, ent):
        num = int(ent.widget.get())
        if ent.delta > 0 and num < self.range[1]:
            ent.widget.delete(0, 'end')
            ent.widget.insert(0, str(num + 1))
            self.q.put(str(num + 1))
        if ent.delta <= 0 and num > self.range[0]:
            ent.widget.delete(0, 'end')
            ent.widget.insert(0, str(num - 1))
            self.q.put(str(num - 1))
        if num <= self.range[0] or num >= self.range[1]:
            pass

    def get_beat(self, ent):
        txt = ent.widget.get()
        try:
            entry_num = abs(int(txt))
            if self.range[0] <= entry_num <= self.range[1]:
                self.get = entry_num
                self.q.put(entry_num)
            else:
                ent.widget.delete(0, 'end')
        except ValueError:
            ent.widget.delete(0, 'end')


if __name__ == "__main__":
    ...
