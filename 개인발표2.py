from tkinter import *
from tkinter import messagebox
#from tkinter.ttk import *
from functools import partial
from datetime import datetime
import csv

day_max = 4
ban_list = '1-1 1-2 1-3 1-4 1-5 1-6 2-5 2-6 2-7'.split()
#stu_points = [None] * 20
stu_name = []
stu_points = []
#stu_p = [[None] * 20] * 20
stu_p = []
data = []
ban = ''
df = ('Malgun Gothic', 15)
bf = ('Malgun Gothic', 15, 'bold')
stu_max = 19

def open_file(ban):
    #global data
    data.clear()
    f = open(ban+'.CSV', encoding='euckr')
    g = csv.reader(f)
    #data = list(g)
    for row in g:
        if len(row):
            data.append(row)
    print('open', ban)
    f.close()
def save_file(fname='', message=False):
    global ban
    if not fname:
        fname = ban
    f = open(fname+'.CSV', 'w', encoding='euckr')
    g = csv.writer(f, delimiter=',')

    for row in data:
        g.writerow(row)

    print('saved', fname)
    f.close()
    if message:
        messagebox.showinfo('알림', fname+'.CSV 저장됨')
def save_file_old():
    global ban
    f = open(ban+'.CSV', 'w', encoding='euckr')
    g = csv.writer(f, delimiter=',')

    for row in data:
        g.writerow(row)

    print('saved', ban)
    f.close()
def backup_ban():
    global ban
    bt = datetime.now().strftime('_%m_%d_%H_%M_%S')
    save_file(ban+bt, True)
def backup_ban_old():
    global ban
    bt = datetime.now().strftime('_%m_%d_%H_%M_%S')
    f = open(ban+bt+'.CSV', 'w', encoding='euckr')
    g = csv.writer(f, delimiter=',')

    for row in data:
        g.writerow(row)

    print('backup', ban)
    f.close()
    messagebox.showinfo('알림', ban+bt+'.CSV 백업 완료')
def ban_select(b):
    global ban_cb
    global ban
    ban = b
    #ban = ban_cb.get()
    ban_l.configure(text=ban)
    print('select', ban)
    open_file(ban)
    for i in range(stu_max):
        try:
            stu_name[i].configure(text=data[i][1])
            stu_points[i].configure(text=data[i][2], fg='black')
            for j in range(20):
                try:
                    stu_p[i][j].configure(text=data[i][j+3], fg='black')
                except:
                    stu_p[i][j].configure(text='.', fg='black')
        except:
            stu_name[i].configure(text='')
            stu_points[i].configure(text='', fg='black')
            for j in range(20):
                stu_p[i][j].configure(text='', fg='black')
def month_day():
    n = datetime.now()
    m = str(n.month)
    d = str(n.day)
    return m + '/' + d
def hour_minute():
    n = datetime.now()
    h = str(n.hour)
    m = str(n.minute)
    return h + ':' + m
def add_p(bun):
    global ban
    count = int(data[bun-1][2])
    md = month_day()
    if data[bun-1].count(md) < day_max and data[bun-1][2] != '20':    # 횟수제한
        print('run add', ban, bun)
        # 내부 자료 처리
        data[bun-1].append(md)
        data[bun-1][2] = str(count+1)
        save_file()
        # 위젯 처리
        stu_points[bun-1].configure(text=data[bun-1][2], fg='blue')
        stu_p[bun-1][count].configure(text=data[bun-1][count+3], fg='blue')
def del_p(bun):
    global ban
    count = int(data[bun-1][2])
    md = month_day()
    if data[bun-1].count(md) > 0:
        # 내부 자료 처리
        data[bun-1].pop()
        data[bun-1][2] = str(count-1)
        save_file()
        # 위젯 처리
        stu_points[bun-1].configure(text=data[bun-1][2])
        stu_p[bun-1][count-1].configure(text='.')
def del_all():
    global ban
    answer = messagebox.askyesno('경고', '진짜 지울래요?')
    if answer:
        backup_ban()
        for stu in data:
            del stu[3:]
            stu[2] = '0'
        for i in range(stu_max):
            try:
                stu_name[i].configure(text=data[i][1])
                stu_points[i].configure(text=data[i][2])
                for j in range(20):
                    stu_p[i][j].configure(text='.')
            except:
                stu_name[i].configure(text='')
                stu_points[i].configure(text='')
                for j in range(20):
                    stu_p[i][j].configure(text='')
        save_file(ban)
# 여기부터 시작
wd = Tk()
#w, h = wd.winfo_screenwidth(), wd.winfo_screenheight()
wd.geometry("+0+0")
wd.title('정보 개인발표 카운터')
# 반 표시 레이블
ban_l = Label(wd, font=df)
ban_l.grid(row=0, column=1)
# 지우기 버튼
ban_clean = Button(wd, text='초기화', width=5, command=del_all)
ban_clean.grid(row=0, column=3)
# 개인발표 숫자 표시
for i in range(1, 21):
    Label(wd, text=str(i), font=df).grid(row=0, column=i+3)
#open_file(ban)
for bun in range(1, stu_max+1):
    # 0. 번호
    Label(wd, text=str(bun), font=df).grid(row=bun, column=0)
    # 1. 이름 버튼(발표 추가)
    stu_name.append(Button(wd, font=bf, width=7, command=partial(add_p, bun)))
    stu_name[-1].grid(row=bun, column=1)
    # 2. 발표횟수 합계
    stu_points.append(Label(wd, text='.', font=df, width=3))
    stu_points[-1].grid(row=bun, column=2)
    # 3. 발표 삭제 버튼
    Button(wd, text='삭제', width=5, command=partial(del_p, bun)).grid(row=bun, column=3)
    # 4~23. 발표 날짜들
    jl = []
    for i in range(20):
        jl.append(Label(wd, text='.', font=df, width=5))
        jl[-1].grid(row=bun, column=i+4)
    stu_p.append(jl)
# 백업 버튼
backup = Button(wd, text='백업', width=5, command=backup_ban)
backup.grid(row=stu_max+1, column=3)
# 반 선택 버튼
for b in ban_list:
    Button(wd, text=b, font=df, width=10, command=partial(ban_select, b)).grid(row=stu_max+1, column=ban_list.index(b)*2+4, columnspan=2)
wd.mainloop()
