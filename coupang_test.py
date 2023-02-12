import sys
import tkinter as tk
from coupang import Pasing
import threading


class Macro:
    def __init__(self):
        self.url = ""
        self.search_name = ""
        self.min_price = 0
        self.max_price = 0
        self.filter_array = []
        self.auto = Pasing()

    def swap_min_max_num(self):
        if self.min_price > self.max_price:
            self.min_price, self.max_price = self.max_price, self.min_price

    def auto_method(self):
        # 값을 불러와 저장.
        self.url = entry_url.get() if entry_url.get() else "https://www.coupang.com"
        self.search_name = entry_name.get() if entry_name.get() else "아이"
        self.min_price = int(entry_min_price.get() if entry_min_price.get() else 0)
        self.max_price = int(entry_max_price.get() if entry_max_price.get() else sys.maxsize)
        self.filter_array = entry_filter.get() if entry_filter.get() else ""
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


def coupang_run():
    # target에 auto.start()를하면 리턴값을 타겟에 지정하는 것이므로 주의 ()사용은 알고 쓰자.
    thread = threading.Thread(target=macro.auto_method)
    thread.daemon = True
    thread.start()


# 매크로 클래스 생성
macro = Macro()

window = tk.Tk()
window.title("auto_Search")
window.geometry("640x360+100+100")
window.resizable(False, False)
text_label = tk.LabelFrame(window, text='진행창', relief='solid', bd=1, pady=10)
text_label.pack()
text_label.place(x=5, y=10, width=320, height=350)

button = tk.Button(window, anchor="center", text="자동화 시작", command=coupang_run, overrelief="solid",
                   repeatdelay=1000)
button.place(x=550, y=330)

button = tk.Button(window, anchor="center", text="자동화 종료", command=lambda: macro.thread_control(True),
                   overrelief="solid",
                   repeatdelay=1000)
button.place(x=450, y=330)

label_url = tk.Label(window, text="가격 필터")
label_url.place(x=350, y=190)

label_url = tk.Label(window, text="filter ','로 구분")
label_url.place(x=350, y=220)

label_url = tk.Label(window, text="url입력창")
label_url.place(x=350, y=250)

label_name = tk.Label(window, text="검색입력")
label_name.place(x=350, y=280)

label_name = tk.Label(window, text="~", font=("궁서체", 20))
label_name.place(x=510, y=183)

entry_min_price = tk.Entry(window, width=9)
entry_min_price.place(x=440, y=190)

entry_max_price = tk.Entry(window, width=11)
entry_max_price.place(x=530, y=190)

entry_filter = tk.Entry(window)
entry_filter.place(x=450, y=220)

entry_url = tk.Entry(window)
entry_url.place(x=450, y=250)

entry_name = tk.Entry(window)
entry_name.place(x=450, y=280)

window.mainloop()
