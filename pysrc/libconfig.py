#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import system
from tkinter import (END, BooleanVar, Listbox, OptionMenu, Spinbox, StringVar,
                     TclError, Tk, Toplevel, Variable, Widget, filedialog)
from tkinter.ttk import (Button, Checkbutton, Entry, Frame, Label, LabelFrame,
                         Radiobutton, Scrollbar)

from config import *
from libunits import *

CONF_PATH = '/opt/cobraav/config.py'

def center_win(win: Tk, geom: str = '') -> None:
    if geom:
        ww, wh = map(int, geom.split('x'))
    else:
        ww = win.winfo_reqwidth()
        wh = win.winfo_reqheight()
    x = win.winfo_screenwidth() // 2 - ww // 2
    y = win.winfo_screenheight() // 2 - wh // 2
    if geom:
        win.geometry('{}x{}+{}+{}'.format(ww, wh, x, y))
    else:
        win.geometry('+{}+{}'.format(x, y))


class EntryOptionsWindow:
    def __init__(self, ls: str, tk: Tk, select_path=False) -> None:
        self.select_path = select_path
        self.List = ls
        self.Tk = tk
        self.Root = Toplevel(self.Tk)
        self.Root.withdraw()
        self.Frame = Frame(self.Root)
        self.Box = Listbox(self.Frame, selectmode='extended', width=54, height=24)
        for i in globals()[self.List]:
            self.Box.insert(END, i)
        self.Scroll = Scrollbar(self.Frame, command=self.Box.yview)
        self.Entry = Entry(self.Frame)
        self.ButtonAdd = Button(self.Frame, text='Добавить', command=self.__add_item)
        self.ButtonDel = Button(self.Frame, text='Удалить', command=self.__del_item)
        self.ButtonDone = Button(self.Frame, text='Готово', command=self.__save_list)
        self.ButtonExit = Button(self.Frame, text='Отмена', command=self.Root.destroy)

    def __add_item(self) -> None:
        if self.select_path:
            text = filedialog.askdirectory()
        else:
            text = self.Entry.get()
        if text:
            self.Box.insert(END, text)
            self.Entry.delete(0, END)

    def __del_item(self) -> None:
        select = list(self.Box.curselection())
        select.reverse()
        for i in select:
            self.Box.delete(i)

    def __save_list(self) -> None:
        globals()[self.List] = list(self.Box.get(0, END))
        self.Root.destroy()

    def main(self) -> None:
        center_win(self.Root, '500x400')
        self.Root.deiconify()
        self.Root.title(f'Editing {self.List}')
        self.Box.pack(side='left', expand=True)
        self.Scroll.pack(side='left', fill='y')
        self.Box.config(yscrollcommand=self.Scroll.set)
        self.Frame.pack(side='left', padx=10)
        if not self.select_path:
            self.Entry.pack(anchor='n')
        self.ButtonAdd.pack(fill='x')
        self.ButtonDel.pack(fill='x')
        self.ButtonDone.pack(fill='x')
        self.ButtonExit.pack(fill='x')
        self.Root.mainloop()


class MainWindow:
    def __init__(self) -> None:
        self.Root = Tk()
        self.App = Frame(self.Root, padding=(5, 2))
        self.UpdatesFrame = LabelFrame(self.App, text='Обновление',
                                       borderwidth=2, relief='sunken', padding=(5, 2))
        self.upd_enabled = BooleanVar()  # Флаг обновлений
        self.upd_unit = StringVar()  # Единица измерения времени
        self.time_units = {Minutes: 'Минут', Hours: 'Часов',
                           Days: 'Дней', Weeks: 'Недель', Months: 'Месяцев'}
        self.size_units = {Bytes: 'Байт', KBytes: 'Кбайт', MBytes:'Мбайт',
                           GBytes:'Гбайт', TBytes:'Тбайт'}  # Список единиц измерения времени
        self.maxfsize = StringVar()  # Максимальный размер файла
        self.size_unit = StringVar()  # Единица измерения информации
        self.units_amount1 = StringVar()  # Количество единиц
        self.quar = BooleanVar()  # False - удалять, True - карантин
        self.quar_path = StringVar() # Расположение карантина
        self.rpt_enabled = BooleanVar()  # Флаг отправки отчета
        self.email = StringVar()  # Адрес отправки
        self.passwd = StringVar() # Пароль исходящего ящика
        self.rpt_unit = StringVar()  # Единица измерения времени
        self.units_amount2 = StringVar()  # Количество единиц

        self.Upd_Label1 = Label(self.UpdatesFrame, text='Проверять обновления антивирусных баз')
        self.Upd_Checkbutton1 = Checkbutton(self.UpdatesFrame, variable=self.upd_enabled)
        self.Upd_Label2 = Label(self.UpdatesFrame, text='Частота проверки:   каждые')
        self.Upd_Spinbox1 = Spinbox(self.UpdatesFrame, textvariable=self.units_amount1,
                                    from_=1, to=999999999, width=4)
        self.Upd_OptionMenu1 = OptionMenu(self.UpdatesFrame, self.upd_unit, *self.time_units.values())
        self.Upd_Button1 = Button(
            self.UpdatesFrame, text='Источники антивирусных сигнатур', command=EntryOptionsWindow('AV_SOURCES', self.Root).main)

        self.ScanFrame = LabelFrame(self.App, text='Сканирование',
                                    borderwidth=2, relief='sunken', padding=(5, 2))
        self.Scn_Label1 = Label(self.ScanFrame, text='Максимальный размер файла:')
        self.Scn_Spinbox1 = Spinbox(self.ScanFrame, textvariable=self.maxfsize,
                                    from_=0, to=999999999, width=8)

        self.Quar_Label = Label(self.ScanFrame, text='При обнаружении угрозы')
        self.Quar_RadButton1 = Radiobutton(self.ScanFrame, text='Удаление', variable=self.quar, value=False)
        self.Quar_RadButton2 = Radiobutton(self.ScanFrame, text='Карантин', variable=self.quar, value=True)

        self.Scn_OptionMenu1 = OptionMenu(self.ScanFrame, self.size_unit, *self.size_units.values())
        self.Scn_Edit_Targets = Button(self.ScanFrame, text='Цели сканирования', command=EntryOptionsWindow('SCAN_TARGETS', self.Root, select_path=True).main)
        self.Scn_Edit_Exceptions = Button(self.ScanFrame, text='Исключения', command=EntryOptionsWindow('SCAN_EXCLUDE', self.Root).main)
        self.Quar_Button1 = Button(self.ScanFrame, text='Расположение карантина',
                                   command=lambda: self.quar_path.set(filedialog.askdirectory()))

        self.ReportFrame = LabelFrame(self.App, text='Отправка отчета',
                                      borderwidth=2, relief='sunken', padding=(5, 2))

        self.Rpt_Label1 = Label(self.ReportFrame, text='Отправлять отчеты о сканировании')
        self.Rpt_Checkbutton1 = Checkbutton(self.ReportFrame, variable=self.rpt_enabled)
        self.Rpt_Label2 = Label(self.ReportFrame, text='Адрес отправки отчетов:')
        self.Rpt_Entry1 = Entry(self.ReportFrame, textvariable=self.email, width=32)
        self.Rpt_Label3 = Label(self.ReportFrame, text='Пароль:')
        self.Rpt_Entry2 = Entry(self.ReportFrame, textvariable=self.passwd, width=32, show='*')
        self.Rpt_Label4 = Label(self.ReportFrame, text='Частота:')
        self.Rpt_Spinbox1 = Spinbox(self.ReportFrame, textvariable=self.units_amount2,
                                    from_=1, to=999999999, width=4)
        self.Rpt_OptionMenu1 = OptionMenu(self.ReportFrame, self.rpt_unit, *self.time_units.values())
        self.Rpt_Button1 = Button(self.ReportFrame, text='Получатели', command=EntryOptionsWindow('SEND_TO', self.Root).main)

        self.Buttons = Frame(self.App, padding=(5, 2))
        self.Button1 = Button(self.Buttons, text='Готово', command=self.save_conf)
        self.Button2 = Button(self.Buttons, text='Отмена', command=self.Root.destroy)

    def main(self) -> None:
        self.upd_unit.set(self.time_units[type(UPDATE_FREQ)])
        self.units_amount1.set(UPDATE_FREQ.value)
        self.upd_enabled.set(CHECK_FOR_UPDATES)
        self.Upd_Checkbutton1.configure(command=(
            lambda: self.__change_state(
                self.upd_enabled, self.Upd_Label2, self.Upd_Spinbox1, self.Upd_OptionMenu1, self.Upd_Button1)
            and self.upd_enabled.set(not self.upd_enabled.get())))
        self.Rpt_Checkbutton1.configure(command=(
            lambda: self.__change_state(
                self.rpt_enabled, self.Rpt_Label2, self.Rpt_Entry1, self.Rpt_Label3, self.Rpt_Entry2,
                 self.Rpt_Label4, self. Rpt_Spinbox1, self.Rpt_OptionMenu1, self.Rpt_Button1)
                 and self.rpt_enabled.set(not self.rpt_enabled.get())))
        self.maxfsize.set(MAX_FILE_SIZE.value)
        self.size_unit.set(self.size_units[type(MAX_FILE_SIZE)])
        self.quar.set(REMOVE_THREATS)
        self.quar_path.set(QUARANTINE_PATH)
        self.rpt_enabled.set(SEND_SCAN_REPORTS)
        self.email.set(SEND_FROM)
        self.passwd.set(SEND_PASSWD)
        self.rpt_unit.set(self.time_units[type(SEND_FREQ)])
        self.units_amount2.set(SEND_FREQ.value)

        self.App.pack(fill='both', expand=True)
        center_win(self.Root, '500x500')
        self.Root.resizable(False, False)
        self.Root.title('CobraAV Configuration')

        self.UpdatesFrame.place(y=0, height=150, width=490)
        self.__change_state(self.upd_enabled, self.Upd_Label2,
                            self.Upd_Spinbox1, self.Upd_OptionMenu1)

        self.__change_state(self.rpt_enabled, self.Rpt_Label2, self.Rpt_Entry1, self.Rpt_Label3,
                            self.Rpt_Entry2, self.Rpt_Label4, self.Rpt_Spinbox1, self.Rpt_OptionMenu1, self.Rpt_Button1)

        self.Upd_Label1.place(relx=.01, rely=.05)  # Проверять обновления ?
        self.Upd_Checkbutton1.place(relx=.8, rely=.05)  # Да/Нет

        self.Upd_Label2.place(relx=.01, rely=.3)  # Частота проверки
        self.Upd_Spinbox1.place(relx=.55, rely=.3, width=60)  # Количество
        self.Upd_OptionMenu1.place(relx=.72, rely=.28)  # Единицы измерения
        self.Upd_Button1.place(relx=.01, rely=.65)  # Источники сигнатур

        self.ScanFrame.place(y=150, height=150, width=490)

        self.Scn_Label1.place(relx=.01, rely=.05)  # Максимальный размер файла
        self.Scn_Spinbox1.place(relx=.55, rely=.05, width=60)  # Количество

        self.Quar_Label.place(relx=.01, rely=.35)
        self.Quar_RadButton1.place(relx=.52, rely=.35)  # Переключатель на удаление угрозы
        self.Quar_RadButton2.place(relx=.72, rely=.35)  # Переключатель на добавление вкарантина угрозы
        self.Quar_Button1.place(relx=.56, rely=.65)  # Расположение карантина

        self.Scn_OptionMenu1.place(relx=.72, rely=.014)  # Единицы измерения
        self.Scn_Edit_Targets.place(relx=.01, rely=.65)  # Цели сканирования
        self.Scn_Edit_Exceptions.place(relx=.33, rely=.65)  # Исключения

        self.Rpt_Label1.place(relx=.01, rely=.05)  # Отправлять отчеты ?
        self.Rpt_Checkbutton1.place(relx=.8, rely=.05)  # Да/Нет

        self.ReportFrame.place(y=300, height=150, width=490)
        self.Rpt_Label2.place(relx=.01, rely=.35)  # Адрес отправки отчетов:
        self.Rpt_Entry1.place(relx=.35, rely=.35)  # Ввод адреса отправки отчетов
        self.Rpt_Label3.place(relx=.01, rely=.50) # Пароль:
        self.Rpt_Entry2.place(relx=.35, rely=.50) # Ввод пароля:
        self.Rpt_Label4.place(relx=.01, rely=.75)  # Частота отправки
        self.Rpt_Spinbox1.place(relx=.35, rely=.75, width=60)  # Количество
        self.Rpt_OptionMenu1.place(relx=.52, rely=.72)  # Единицы измерения
        self.Rpt_Button1.place(relx=.72, rely=.74) # Получатели

        self.Buttons.place(y=450, height=50, width=490)
        self.Button1.place(relx=.62, rely=.2) # Кнопка "Готово"
        self.Button2.place(relx=.82, rely=.2) # Кнопка "Отмена"

        self.Root.mainloop()

    @staticmethod
    def __change_state(state: BooleanVar, *args: Widget) -> None:
        for i in args:
            i.configure(state=('disabled', 'normal')[state.get()])

    def save_conf(self) -> None:
        size_units = {v: k for k, v in self.size_units.items()}
        time_units = {v: k for k, v in self.time_units.items()}

        def wrap_list(a: 'list[str]') -> str:
            return '[' + ', '.join(f"r'{i}'" for i in a) + ']'

        def wrap_cls(_unit: Variable, amount: Variable) -> str:
            unit = _unit.get()
            if unit in size_units:
                return size_units[unit].__name__ + f'({amount.get()})'
            elif unit in time_units:
                return time_units[unit].__name__ + f'({amount.get()})'
            else:
                raise NotImplementedError

        with open(CONF_PATH, 'w') as f:
            f.write(
                f"""from libunits import *

CHECK_FOR_UPDATES = {int(self.upd_enabled.get())}  # Check for updates
UPDATE_FREQ = {wrap_cls(self.upd_unit, self.units_amount1)}  # Check interval
MAX_FILE_SIZE = {wrap_cls(self.size_unit, self.maxfsize)}  # Max file size

# Antivirus database sources
AV_SOURCES = {wrap_list(AV_SOURCES)}

# Antivirus database path
DB_PATH = r'{DB_PATH}'

# On threat:
# 0 - quarantine
# 1 - remove
REMOVE_THREATS = {int(self.quar.get())}

# Directories to scan
SCAN_TARGETS = {wrap_list(SCAN_TARGETS)}

# Exclude from scanning
SCAN_EXCLUDE = {wrap_list(SCAN_EXCLUDE)}

# quarantine location
QUARANTINE_PATH = r'{self.quar_path.get() or QUARANTINE_PATH}'

# Send scan reports
SEND_SCAN_REPORTS = {int(self.rpt_enabled.get())}

# Scan reports frequency
SEND_FREQ = {wrap_cls(self.rpt_unit, self.units_amount2)}

# Send from this email
SEND_FROM = r'{self.email.get()}'

# Sender email password
SEND_PASSWD = r'{self.passwd.get()}'

# Send to these emails
SEND_TO = {wrap_list(SEND_TO)}
""")
        self.Root.destroy()


def main() -> None:
    try:
        Program = MainWindow()
        Program.main()
    except TclError:
        system(f'/usr/bin/editor {CONF_PATH}')

