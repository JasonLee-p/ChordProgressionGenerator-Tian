# -*- coding: utf-8 -*-
"""

"""
import ctypes
import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os

BG_COLOUR = 'Beige'  # 背景色
FONT0 = 'microsoft yahei'
FONTT = 'microsoft yahei'
FONT_SIZE = 12
own_path = os.path.dirname(__file__)


def set_window(window):
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # 告诉操作系统使用程序自身的dpi适配
    ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)  # 获取屏幕的缩放因子
    window.tk.call('tk', 'scaling', ScaleFactor / 75)  # 设置程序缩放
    try:
        window.state("zoomed")
    except:
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
        font=(FONTT, 11),  # 字体和字体大小
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


# def button(master, expand, belonging, hit_func, text, font_size, side, width):
#     b = tk.Button(master, text=text, font=(FONT0, font_size), width=width, height=1, command=hit_func)
#     b.pack(side=side, padx=5, pady=4, expand=expand)
#     if belonging:
#         belonging.append(b)


def button(master, expand, belonging, hit_func, text, side, width, style_name):
    b = ttk.Button(master, text=text, width=width, command=hit_func)
    b.configure(style=style_name)
    b.pack(side=side, padx=5, pady=4, expand=expand)
    if belonging:
        belonging.append(b)


def result_frame(master, belonging, handler):
    f2 = tk.Frame(master, padx=0, pady=0, bg='ivory')
    f1 = tk.Frame(master, padx=0, pady=4, bg='ivory')
    f2.pack(side="bottom", fill="both")
    f1.pack(side="bottom", fill="both")
    if belonging:
        belonging.append(f1)
        belonging.append(f2)

    v_text_var = tk.StringVar()
    a_text_var = tk.StringVar()
    title(v_text_var, BG_COLOUR)(
        belonging, f1, position="left", expand=False, font_size=12, wid=29, hei=1, padx=0)
    title(a_text_var, BG_COLOUR)(
        belonging, f1, position="right", expand=False, font_size=12, wid=29, hei=1, padx=0)
    v_text_var.set("Video result:")
    a_text_var.set("Audio result:")
    #
    title(handler.result_text_var0, BG_COLOUR)(
        belonging, f2, position="left", expand=False, font_size=20, wid=18, hei=1, padx=0)
    title(handler.result_text_var1, BG_COLOUR)(
        belonging, f2, position="right", expand=False, font_size=20, wid=18, hei=1, padx=0)


def mode_frame(master, belonging, side, hit_func):
    # frame1
    f = tk.Frame(master=master, padx=10, pady=4, bg='ivory')
    f.pack(side=side, fill='both')
    if belonging:
        belonging.append(f)
    # 输出字符变量
    text_var_mode = tk.StringVar()
    title(text_var_mode, BG_COLOUR)(
        belonging, f, position="left", expand=False, font_size=FONT_SIZE, wid=12, hei=1, padx=5, ipady=3)
    text_var_mode.set("Mode:")
    combox(f, None, hit_func, ['chord', 'note', 'both']).current(0)
    return f


def bottoms_top_frame(master, belonging):
    f = tk.Frame(master=master, padx=10, pady=5, bg='ivory')
    f.pack(side="top", fill='both')
    if belonging:
        belonging.append(f)
    text_var_mode = tk.StringVar()
    title(text_var_mode, BG_COLOUR)(
        belonging, f, position="left", expand=False, font_size=FONT_SIZE, wid=12, hei=1, padx=5, ipady=3)
    text_var_mode.set("  Select Score:  ")
    return f


# 定义下拉选择框
def combox(master, belonging, selected_func, values, position='left', width=19, height=5, style_name=None):
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
    VScroll1.pack(side='right', fill='y', padx=0)
    table = ttk.Treeview(
        master=master,  # 父容器
        height=20,  # 表格显示的行数,height行
        columns=columns,  # 显示的列
        show='headings',  # 隐藏首列
        style='Treeview',
        yscrollcommand=VScroll1.set
    )

    def treeviewClick(event):  # 单击
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


class CPGCanvas:
    def __init__(self, master):
        self.MouseState = 'out'
        self.piano_keys_frames = []
        self.keyIndex2midi = dict(zip(range(1, 89), range(108, 19, -1)))
        self.midi2keyIndex = dict(zip(range(108, 19, -1), range(1, 89)))
        self.key_height = 12
        self.bw = 50
        self.canvas = tk.Canvas(master=master, height=220, bg=BG_COLOUR, bd=0)
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
        self.cvFrame = tk.Frame(self.canvas, height=90 * (self.key_height + 1), width=3000)  # 画布滚动区域
        self.cvFrame.propagate(0)
        self.piano_keys_frames.append(
             f_ := tk.Frame(self.cvFrame, bg=BG_COLOUR, height=self.key_height, bd=0))
        f_.pack(side='top', fill='x', padx=2)
        # # 绘制分割线
        # for j in range(1, 3000 // self.bw + 1):
        #     tk.Frame(self.cvFrame, bg='#222222', width=1, height=1000).place(
        #         x=j * self.bw, y=0)
        # 绘制键盘
        for i in range(88):
            if i % 12 in [0, 1, 3, 5, 7, 8, 10]:
                wk = tk.Frame(self.cvFrame, bg='#555555', height=self.key_height, bd=0)
                wk.pack(side='top', fill='x', padx=2)
                self.piano_keys_frames.append(wk)
            else:
                bk = tk.Frame(self.cvFrame, bg='#464646', height=12, bd=0)
                bk.pack(side='top', fill='x', padx=2)
                self.piano_keys_frames.append(bk)
            tk.Frame(self.cvFrame, bg='#222222', height=1, bd=0).pack(
                side='top', fill='x', padx=2)

        self.piano_keys_frames.append(
            _f := tk.Frame(self.cvFrame, bg=BG_COLOUR, height=self.key_height, bd=0))
        _f.pack(side='top', fill='x', padx=2)
        # self.score_preview0 = tk.Frame(master=self.cvFrame, bg=BG_COLOUR, bd=0)  # 标尺层
        # self.score_preview1 = tk.Frame(master=self.cvFrame, bg=BG_COLOUR, bd=0)  # 乐谱层
        # self.score_preview2 = tk.Frame(master=self.cvFrame, bg=BG_COLOUR, bd=0)  # 乐谱层
        self.canvas.create_window((0, 0), window=self.cvFrame, anchor='nw')
        # self.score_preview0.pack(side='top')
        # self.score_preview1.pack(side='top')
        # self.score_preview2.pack(side='top')
        self.canvas.pack(side='left', padx=20, fill='both')

        def rolling_func(event):
            self.canvas.configure(
                xscrollcommand=self.top_sb.set,
                yscrollcommand=self.left_sb.set,
                scrollregion=(0, 0, 3000, 90 * (self.key_height + 1)),  # TODO:
                width=3000  # TODO:
            )

        self.canvas.bind("<Configure>", rolling_func)  # 绑定滚动条
        self.canvas.bind("<Enter>", self.enter_func)  # 进入
        self.canvas.bind("<Leave>", self.leave_func)  # 离开
        self.cvFrame.bind_all("<MouseWheel>", self.cv_mousewheel)  # 绑定鼠标
        self.cvFrame.bind_all("<Shift-MouseWheel>", self.cv_mousewheel)  # 绑定shift
        self.cvFrame.bind_all("<Control-MouseWheel>", self.cv_mousewheel)  # 绑定Ctrl
        master.update()

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
                    self.canvas.configure(scrollregion=(0, 0, 3000, 90 * (1 + self.key_height)))
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


if __name__ == "__main__":
    ...
