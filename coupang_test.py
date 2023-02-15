import sys
import time
import tkinter as tk
from tkinter import scrolledtext
from coupang import Pasing
import threading


class WindowUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.url = ""
        self.search_name = ""
        self.min_price = 0
        self.max_price = 0
        self.filter_array = []
        self.auto = Pasing()
        self.title("auto_Search")
        self.geometry("640x360+100+100")
        self.resizable(False, False)
        #############################################
        # label_frame
        self.labelframe_progress = tk.LabelFrame(self, text='진행창', relief='solid', bd=1)
        self.labelframe_progress.pack()
        self.labelframe_progress.place(x=5, y=10, width=320, height=350)

        #############################################

        # button
        self.button_start = tk.Button(self, anchor="center", text="자동화 시작", command=self.coupang_run,
                                      overrelief="solid", repeatdelay=1000)
        self.button_start.place(x=550, y=330)
        self.button_exit = tk.Button(self, anchor="center", text="자동화 종료", command=lambda: self.thread_control(True),
                                     overrelief="solid", repeatdelay=1000)
        self.button_exit.place(x=450, y=330)
        #############################################
        # label
        self.label_progress_info = scrolledtext.ScrolledText(self.labelframe_progress)
        # self.label_progress_info.configure(state='disabled')
        self.label_progress_info.pack()

        self.label_url = tk.Label(self, text="가격 필터")
        self.label_url.place(x=350, y=190)

        self.label_url = tk.Label(self, text="filter ','로 구분")
        self.label_url.place(x=350, y=220)

        self.label_url = tk.Label(self, text="url입력창")
        self.label_url.place(x=350, y=250)

        self.label_name = tk.Label(self, text="검색입력")
        self.label_name.place(x=350, y=280)

        self.label_name = tk.Label(self, text="~", font=("궁서체", 20))
        self.label_name.place(x=510, y=183)

        #############################################
        # entry
        self.entry_min_price = tk.Entry(self, width=9)
        self.entry_min_price.place(x=440, y=190)

        self.entry_max_price = tk.Entry(self, width=11)
        self.entry_max_price.place(x=530, y=190)

        self.entry_filter = tk.Entry(self)
        self.entry_filter.place(x=450, y=220)

        self.entry_url = tk.Entry(self)
        self.entry_url.place(x=450, y=250)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=450, y=280)

        #############################################
        # scrollbar

    def swap_min_max_num(self):
        if self.min_price > self.max_price:
            self.min_price, self.max_price = self.max_price, self.min_price

    def auto_method(self):
        # 값을 불러와 저장.
        self.label_progress_info.delete('1.0', 'end')
        self.label_progress_info.insert('current', "자동화 시작...")
        self.url = self.entry_url.get() if self.entry_url.get() else "https://www.coupang.com"
        self.search_name = self.entry_name.get() if self.entry_name.get() else "아이"
        self.min_price = int(self.entry_min_price.get() if self.entry_min_price.get() else 0)
        self.max_price = int(self.entry_max_price.get() if self.entry_max_price.get() else sys.maxsize)
        self.filter_array = self.entry_filter.get() if self.entry_filter.get() else ""
        self.filter_array = self.filter_array.split(",")
        self.swap_min_max_num()
        #  매크로 실행
        result = self.auto.auto_start(self.url, self.search_name, self.min_price, self.max_price, self.filter_array)
        # 매크로 실행 결과 출력
        print(result)
        if result == 'success':
            result = self.save_to_csv()
        print(result)

    def thread_control(self, value):
        self.auto.thread = value

    def save_to_csv(self):
        return self.auto.ary_to_csv()

    def coupang_run(self):
        # target에 auto.start()를하면 리턴값을 타겟에 지정하는 것이므로 주의 ()사용은 알고 쓰자.
        thread = threading.Thread(target=self.auto_method)
        thread.daemon = True
        thread.start()

        def thread_alive_check():
            while thread.is_alive():
                self.window_update()
                time.sleep(0.25)

        thread2 = threading.Thread(target=thread_alive_check)
        thread2.daemon = True
        thread2.start()

    def window_update(self):
        temp = self.auto.__progress_info__
        self.auto.__progress_info__ = ''
        self.label_progress_info.insert(index='end', chars=temp)
        self.label_progress_info.see('end')


window = WindowUI()
window.mainloop()
