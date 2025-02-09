import json
import tkinter as tk
from tkinter.messagebox import showinfo, showerror
from tkinter.filedialog import askopenfilename, askdirectory
from function import Password, ListPassword
from tkinter import ttk
import os


class InputTkinter(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title('Введите ваше имя')
        self.geometry('300x100')
        self.name = None
        self.input_field = tk.Entry(self, width=30)
        self.input_field.pack()
        self.button = tk.Button(self, text='Отправить', command=self.send_name)
        self.button.pack()

    def send_name(self):
        self.name = self.input_field.get()
        if self.name:
            self.quit()
        else:
            showerror('Ошибка', 'Введите имя')


def on_mouse_wheel(event, canvas):
    if event.num == 4 or event.delta > 0:
        canvas.yview_scroll(-1, "units")
    elif event.num == 5 or event.delta < 0:
        canvas.yview_scroll(1, "units")


def first_start(master):
    if os.path.exists('config.json'):
        with open('config.json', 'r') as file:
            data = json.load(file)
            name = data['name']

        list_password = ListPassword(name)
        list_password.from_json()
        return list_password, name

    else:
        input_window = InputTkinter(master)
        input_window.mainloop()
        name = input_window.name
        with open('config.json', 'w') as file:
            json.dump({'name': name}, file)
        list_password = ListPassword(name=name)
        list_password.to_json()
        input_window.destroy()
        master.wm_attributes('-topmost', 1)
        return list_password, name


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        list_password, name = first_start(self)
        self.list_password: ListPassword = list_password
        self.name: str = name
        self.title(f'Manager_Password_{self.name}')
        self.geometry('600x500')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.create_widgets()

    def create_widgets(self, company=None):
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        frame_vision_password = tk.Frame(self.canvas)
        frame_vision_password.pack(fill='both', padx=10, pady=10)
        self.canvas_window = self.canvas.create_window((0, 0), anchor='nw', window=frame_vision_password)
        frame_vision_password.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", lambda event: on_mouse_wheel(event, self.canvas))
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.grid(column=0, row=0, sticky='nsew')
        self.scrollbar.grid(column=1, row=0, sticky='ns')
        self.create_widget_password(frame_vision_password, company)

        self.frame_add_password = tk.LabelFrame(self, text='Add Password')
        self.frame_add_password.grid(column=0, row=1, padx=10, pady=10, columnspan=2)
        tk.Label(self.frame_add_password, text='Company, website:').grid(column=0, row=0, padx=5, pady=5)
        self.company_entry = tk.Entry(self.frame_add_password)
        self.company_entry.grid(column=1, row=0, padx=5, pady=5)
        tk.Label(self.frame_add_password, text='Login:').grid(column=0, row=1, padx=5, pady=5)
        self.login_entry = tk.Entry(self.frame_add_password)
        self.login_entry.grid(column=1, row=1, padx=5, pady=5)
        tk.Label(self.frame_add_password, text='Password:').grid(column=0, row=2, padx=5, pady=5)
        self.password_entry = tk.Entry(self.frame_add_password)
        self.password_entry.grid(column=1, row=2, padx=5, pady=5)
        self.button_create_password = tk.Button(self.frame_add_password, text='Create', command=self.create_password)
        self.button_create_password.grid(column=1, row=3, padx=5, pady=5)
        self.search_widget = ttk.Combobox(self.frame_add_password,
                                          values=sorted(list(set([passw.company for passw in self.list_password.list_pass]))),
                                          state='normal')
        self.search_widget.grid(column=2, row=0, padx=5, pady=5)
        self.search_button = tk.Button(self.frame_add_password, text='Search',
                                       command=self.filter_password)
        self.search_button.grid(column=2, row=1, padx=5, pady=5)

    def on_canvas_configure(self, event):
        # При изменении размера Canvas обновляем ширину внутреннего окна
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def create_password(self):
        if self.password_entry.get() and self.login_entry.get() and self.company_entry.get():
            new_password = Password(password=self.password_entry.get(),
                                    login=self.login_entry.get(),
                                    company=self.company_entry.get())
            self.list_password.add(new_password)
            self.list_password.to_json()
            self.refresh_display()
        else:
            showinfo('Not data', message='Enter the data')

    def refresh_display(self):
        self.destroy()
        new_app = MainApp()
        new_app.mainloop()

    def delete_password(self, i):
        self.list_password.delete_pass(i)
        self.refresh_display()

    def create_widget_password(self, frame: tk.Frame, company: str = None):
        self.list_password.list_pass.sort(key=lambda x: x.company)

        if company is None:
            i = 0
            for password in self.list_password.list_pass:
                string = f'{password.company}\n{password.login}\n{password.password}'
                text = tk.Text(frame, height=3, width=80, font=('Times New Roman', 10))
                text.insert('1.0', string)
                text.grid(column=0, row=i, padx=5, pady=5)
                text.config(state='disabled')
                button = tk.Button(frame, text='Delete',
                                   command=lambda key=f'{password.company};{password.login}': self.delete_password(key))
                button.grid(column=1, row=i, padx=5, pady=5)
                i += 1
        if company is not None:
            i = 0
            for password in self.list_password.list_pass:
                if password.company == company:
                    string = f'{password.company}\n{password.login}\n{password.password}'
                    text = tk.Text(frame, height=3, width=80, font=('Times New Roman', 10))
                    text.insert('1.0', string)
                    text.grid(column=0, row=i, padx=5, pady=5)
                    text.config(state='disabled')
                    button = tk.Button(frame, text='Delete',
                                       command=lambda key=f'{password.company};{password.login}': self.delete_password(
                                           key))
                    button.grid(column=1, row=i, padx=5, pady=5)
                    i += 1

    def filter_password(self):
        company = self.search_widget.get()
        self.canvas.destroy()
        self.frame_add_password.destroy()
        self.scrollbar.destroy()
        if company:
            self.create_widgets(company)
        else:
            self.create_widgets()



app = MainApp()
app.mainloop()


