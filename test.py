import tkinter as tk
from tkinter.messagebox import showinfo, showerror
from tkinter.filedialog import askopenfilename, askdirectory
from function import Password, ListPassword
from tkinter import ttk


def on_mouse_wheel(event, canvas):
    if event.num == 4 or event.delta > 0:
        canvas.yview_scroll(-1, "units")
    elif event.num == 5 or event.delta < 0:
        canvas.yview_scroll(1, "units")


class MainApp(tk.Tk):
    def __init__(self, name: ListPassword):
        super().__init__()
        self.list_password = name
        self.name = name.name
        self.title(f'Manager_Password_{self.name}')
        self.geometry('600x500')
        self.create_widgets()

    def create_widgets(self, company=None):
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        frame_vision_password = tk.Frame(self.canvas)
        frame_vision_password.pack(fill='x', padx=10, pady=10)
        self.canvas.create_window((0, 0), anchor='center', window=frame_vision_password)
        frame_vision_password.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.bind_all("<MouseWheel>", lambda event: on_mouse_wheel(event, self.canvas))
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="top", fill='x', expand=True)
        self.scrollbar.pack(side="right", fill="x")
        self.create_widget_password(frame_vision_password, company)

        self.frame_add_password = tk.LabelFrame(self, text='Add Password')
        self.frame_add_password.pack(fill='x', padx=10, pady=10)
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
                                          values=list(set([passw.company for passw in self.list_password.list_pass])),
                                          state='normal')
        self.search_widget.grid(column=2, row=0, padx=5, pady=5)
        self.search_button = tk.Button(self.frame_add_password, text='Search',
                                       command=self.filter_password)
        self.search_button.grid(column=2, row=1, padx=5, pady=5)

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
        new_app = MainApp(self.list_password)
        new_app.mainloop()

    def delete_password(self, i):
        self.list_password.delete_pass(i)
        self.refresh_display()

    def create_widget_password(self, frame: tk.Frame, company: str = None):
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


new_pass = ListPassword('Ivan')
new_pass.from_json()
app = MainApp(new_pass)
app.mainloop()