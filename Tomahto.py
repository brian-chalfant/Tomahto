import tkinter
from tkinter import PhotoImage
from tkinter import messagebox
import datetime
DEFAULT_GAP = 60 * 25


class Tomahto:
    def __init__(self, master):
        self.master = master
        self.time = datetime.datetime.now()
        self.mainframe = tkinter.Frame(self.master, bg='#eeeeee')
        self.mainframe.pack(fill=tkinter.BOTH, expand=True)
        self.date_time_text =tkinter.StringVar()
        self.date_time_text.trace('w', self.build_status)
        self.timer_text = tkinter.StringVar()
        self.timer_text.trace('w', self.build_timer)
        self.timer_text.trace('w', self.uptime)
        self.time_left = tkinter.IntVar()
        self.time_left.trace('w', self.alert)
        self.time_left.set(DEFAULT_GAP)
        self.running = False
        self.build_grid()
        self.build_banner()
        self.build_buttons()
        self.build_timer()
        self.build_status()
        self.update()

    def build_grid(self):
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.columnconfigure(1, weight=0)
        self.mainframe.rowconfigure(0, weight=0, minsize=72)
        self.mainframe.rowconfigure(1, weight=1)
        self.mainframe.rowconfigure(2, weight=0, minsize=72)
        self.mainframe.rowconfigure(3, weight=0)

    def build_banner(self):
        background_image = PhotoImage(file='Port_Clockwork Spider_small.png')
        background_label = tkinter.Label(self.mainframe,
                                         image=background_image,
                                         bg='#2a7265'
                                         )
        background_label.image = background_image

        banner = tkinter.Label(
            self.mainframe,
            background='#2a7265',
            text='Tomahto',
            fg='white',
            font=('Agency FB', 48)
        )
        banner.grid(
            row=0, column=0,
            sticky='ew'
        )
        background_label.grid(row=0, column=1, sticky='nsew')

    def build_buttons(self):
        buttons_frame = tkinter.Frame(self.mainframe)
        buttons_frame.grid(row=2, rowspan=2, column=0, columnspan=2, sticky='ew', padx=10, pady=10)
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)
        buttons_frame.rowconfigure(0, weight=1)
        buttons_frame.rowconfigure(1, weight=0)

        self.start_button = tkinter.Button(
            buttons_frame,
            text='Start',
            fg='#2a7265',
            font=('Agency FB', 12),
            command=self.start_time
        )
        self.stop_button = tkinter.Button(
            buttons_frame,
            text='Stop',
            fg='#2a7265',
            font=('Agency FB', 12),
            command=self.stop_time
        )

        self.start_button.grid(row=2, column=0, sticky='ew')
        self.stop_button.grid(row=2, column=1, sticky='ew')
        self.stop_button.config(state=tkinter.DISABLED)

    def build_status(self, *args):
        status_bar_frame = tkinter.Frame(self.mainframe)
        status_bar_frame.grid(row=3, column=1, sticky='sw')
        status_bar_time = tkinter.Label(status_bar_frame,
                                        fg='black',
                                        text=self.date_time_text.get(),
                                        font=('Digital-7', 12),
        )
        status_bar_date = tkinter.Label(status_bar_frame,
                                        fg='black',
                                        text='{}/{}/{}'.format(self.time.month, self.time.day, self.time.year),
                                        font=('Digital-7', 12),
                                        )
        status_bar_date.grid(row=0, column=0)
        status_bar_time.grid(row=0, column=1)

    def build_timer(self, *args):

        background_label = tkinter.Label(self.mainframe,
                                         fg='black',
                                         text=self.timer_text.get(),
                                         font=('Digital-7', 24),
                                         )
        background_label.grid(row=1, column=0, columnspan=2, sticky='nsew')

    def start_time(self):
        self.time_left.set(DEFAULT_GAP)
        self.running = True
        self.stop_button.config(state=tkinter.NORMAL)
        self.start_button.config(state=tkinter.DISABLED)

    def stop_time(self):
        self.running = False
        self.stop_button.config(state=tkinter.DISABLED)
        self.start_button.config(state=tkinter.NORMAL)

    def minutes_seconds(self, seconds):
        return int(seconds/60), int(seconds%60)

    def update(self):
        time_left = self.time_left.get()

        if self.running and time_left:
            minutes, seconds = self.minutes_seconds(time_left)
            self.timer_text.set(
                '{:0>2}:{:0>2}'.format(minutes, seconds)
            )
            self.time_left.set(time_left-1)

        else:
            minutes, seconds = self.minutes_seconds(DEFAULT_GAP)
            self.timer_text.set(
                '{:0>2}:{:0>2}'.format(minutes, seconds)
            )
            self.stop_time()
        self.master.after(1000, self.update)

    def alert(self, *args):
        if not self.time_left.get():
            messagebox.showinfo('Tomahto', 'Ding!')

    def uptime(self, *args):
        time = datetime.datetime.now()
        self.date_time_text.set(
            '{}:{:0>2} {}'.format(time.strftime("%I"), time.strftime("%M"), time.strftime("%p"))

        )
        self.master.after(15000, self.uptime)





if __name__ == '__main__':
    root = tkinter.Tk()
    app = Tomahto(master=root)
    app.master.title("Tomahto")
    app.master.iconbitmap('tomahto.ico')
    root.mainloop()
