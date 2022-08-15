try:
    import tkinter as tk  # python 3
    from tkinter import font as tkfont, ttk  # python 3
except ImportError:
    import Tkinter as tk  # python 2
    import tkFont as tkfont  # python 2


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Times New Roman Baltic', size=120, weight="bold")
        self.small_title_font = tkfont.Font(family='Times New Roman Baltic', size=80, weight="bold")
        self.menu_button_font = tkfont.Font(family='Helvetica', size=18, weight="bold")
        self.geometry('1280x720')
        container = tk.Frame(self)
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (
                OpeningPage, MainMenu, DungeonDelve, CreateTeamPage, CreditPage, How2PlayPage, LeaderboardPage,
                LoginMenu,
                RegisterMenu):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0)

        self.show_frame("OpeningPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        for frame in self.frames.values():
            frame.grid_remove()
        frame = self.frames[page_name]
        frame.tkraise()
        frame.grid()

    def breakcode(self):
        self.destroy()

    def check_password(self, username_entry, password_entry, confirm_password_entry):
        global no_pw_warning
        global not_equal_pw_warning
        global no_us_and_pw_warning
        global no_us_warning
        global inputted_username
        global inputted_password
        inputted_username = username_entry.get()
        inputted_username.strip()
        inputted_password = password_entry.get()
        inputted_password.strip()
        inputted_confirm_password = confirm_password_entry.get()
        inputted_confirm_password.strip()
        if inputted_password == "":
            if inputted_username == "":
                not_equal_pw_warning = 0
                no_pw_warning = 0
                no_us_warning = 0
                no_us_and_pw_warning = 0
                no_us_and_pw_warning = ttk.Label(self, text="Username and Password cannot be empty")
                no_us_and_pw_warning.grid(row=3, column=0, padx=10, pady=10)
            else:
                not_equal_pw_warning = 0
                no_us_warning = 0
                no_us_and_pw_warning = 0
                no_pw_warning = 0
                no_pw_warning = ttk.Label(self, text="Password cannot be empty")
                no_pw_warning.grid(row=3, column=0, padx=10, pady=10)
        elif inputted_confirm_password == inputted_password:
            if inputted_username == "":
                not_equal_pw_warning = 0
                no_pw_warning = 0
                no_us_and_pw_warning = 0
                no_us_warning = 0
                no_us_warning = ttk.Label(self, text="Username cannot be empty")
                no_us_warning.grid(row=3, column=0, padx=10, pady=10)
            else:
                no_pw_warning = 0
                not_equal_pw_warning = 0
                no_us_and_pw_warning = 0
                no_us_warning = 0
                self.final_register_check()

        else:
            no_pw_warning = 0
            no_us_and_pw_warning = 0
            no_us_warning = 0
            not_equal_pw_warning = 0
            not_equal_pw_warning = ttk.Label(self, text="Passwords aren't the same")
            not_equal_pw_warning.grid(row=3, column=0, padx=10, pady=10)

    def user_account_set(self):
        file = open("C:/Users/gabolinscya/Documents/L2_ASSIGNMENT_RPG/account_data_username.txt", "a")
        file.write("\n")
        file.write(inputted_username)
        file.close()
        file = open("C:/Users/gabolinscya/Documents/L2_ASSIGNMENT_RPG/account_data_password.txt", "a")
        file.write("\n")
        file.write(inputted_password)
        file.close()
        successful_user_addition = ttk.Label(self, text="You're account has been created!")
        successful_user_addition.grid(row=4, column=1, padx=10, pady=10)


    def final_register_check(self):
        register_window = registery_window(self)
        registery_window.grab_set(self)

    def register_to_login(self):
        no_pw_warning = 0
        no_us_and_pw_warning = 0
        no_us_warning = 0
        not_equal_pw_warning = 0
        self.show_frame("LoginMenu")


class registery_window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Confirmation")
        register_window_label = ttk.Label(self, text="Are you sure you want to register with these details?")
        register_window_button_yes = ttk.Button(self, text="Yes",
                                                command=lambda: self.access_user_account_set())
        register_window_button_no = ttk.Button(self, text="No",
                                               command=self.destroy)
        register_window_label.grid(column=1, row=1)
        register_window_button_yes.grid(column=1, row=2)
        register_window_button_no.grid(column=1, row=3)

    def access_user_account_set(self):
        SampleApp.user_account_set(self)

class OpeningPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Game Title", font=controller.title_font)
        label.grid(row=1, column=2, pady=10, sticky="new")
        invis_label1 = tk.Label(self)
        invis_label2 = tk.Label(self)
        invis_label3 = tk.Label(self)

        button = tk.Button(self, text="Start Game", padx=100, pady=80, font=controller.menu_button_font,
                           command=lambda: controller.show_frame("LoginMenu"))
        invis_label1.grid(column=2, row=2, pady=50)
        invis_label2.grid(column=1, row=1, padx=95)
        invis_label3.grid(column=1, row=2, padx=95)
        button.grid(row=3, column=2)


class LoginMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Game Title", font=controller.title_font)
        label.grid(row=1, column=2, pady=10, sticky="new")
        invis_label1 = tk.Label(self)
        invis_label2 = tk.Label(self)
        invis_label3 = tk.Label(self)
        Loginbutton = tk.Button(self, text="Login", font=controller.menu_button_font,
                                command=lambda: controller.show_frame("MainMenu"))
        Regibutton = tk.Button(self, text="Register", font=controller.menu_button_font,
                               command=lambda: controller.show_frame("RegisterMenu"))
        Returnbutton = tk.Button(self, text="Back", font=controller.menu_button_font,
                                 command=lambda: controller.show_frame("OpeningPage"))
        username_label = ttk.Label(self, text="Username:")
        username_entry = ttk.Entry(self)
        password_label = ttk.Label(self, text="Password:")
        password_entry = ttk.Entry(self, show="*")
        invis_label1.grid(column=2, row=2, pady=50)
        invis_label2.grid(column=1, row=1, padx=95)
        invis_label3.grid(column=1, row=2, padx=95)
        Loginbutton.grid(row=5, column=2)
        Regibutton.grid(row=6, column=2)
        Returnbutton.grid(row=7, column=2)
        username_label.grid(row=3, column=2, ipadx=100, padx=10, pady=10)
        username_entry.grid(row=3, column=2, padx=10, pady=10)
        password_label.grid(row=4, column=2, ipadx=100, padx=10, pady=10)
        password_entry.grid(row=4, column=2, padx=10, pady=10)


class RegisterMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Register your account", font=controller.small_title_font)
        label.grid(row=1, column=1, pady=10)
        invis_label1 = tk.Label(self)
        invis_label2 = tk.Label(self)
        invis_label3 = tk.Label(self)
        username_label = ttk.Label(self, text="Username:")
        username_entry = ttk.Entry(self)
        password_label = ttk.Label(self, text="Password:")
        password_entry = ttk.Entry(self, show="*")
        confirm_password_label = ttk.Label(self, text="Confirm Password:")
        confirm_password_entry = ttk.Entry(self, show="*")
        confirm_registerbutton = tk.Button(self, text="Register Details",
                                           command=lambda: controller.check_password(username_entry, password_entry,
                                                                                     confirm_password_entry))
        back_to_login = tk.Button(self, text="Back to Login",
                                  command=lambda: controller.register_to_login())
        back_to_login.grid(row=7, column=1, padx=10, pady=10)
        confirm_registerbutton.grid(row=6, column=1)
        username_label.grid(row=3, column=1, ipadx=100, padx=10, pady=10)
        username_entry.grid(row=3, column=1, padx=10, pady=10)
        password_label.grid(row=4, column=1, ipadx=100, padx=10, pady=10)
        password_entry.grid(row=4, column=1, padx=10, pady=10)
        confirm_password_label.grid(row=5, column=1, ipadx=120, padx=10, pady=10)
        confirm_password_entry.grid(row=5, column=1, padx=10, pady=10)
        invis_label1.grid(row=0, pady=15)
        invis_label2.grid(column=0, row=1, padx=25)
        invis_label3.grid(row=2, column=1, pady=35)


class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Surface Menu", font=controller.title_font)
        label.grid(column=2)
        invis_label1 = tk.Label(self)
        invis_label2 = tk.Label(self)
        invis_label3 = tk.Label(self)
        invis_label4 = tk.Label(self)
        invis_label5 = tk.Label(self)
        invis_label6 = tk.Label(self)
        invis_label7 = tk.Label(self)
        buttonDungeon = tk.Button(self, text="Delve into the Dungeon", padx=10, pady=10,
                                  font=controller.menu_button_font,
                                  command=lambda: controller.show_frame("DungeonDelve"))
        buttonTeam = tk.Button(self, text="Champion Camp", padx=10, pady=10, font=controller.menu_button_font,
                               command=lambda: controller.show_frame("CreateTeamPage"))
        buttonCredit = tk.Button(self, text="Credits", padx=10, pady=10, font=controller.menu_button_font,
                                 command=lambda: controller.show_frame("CreditPage"))
        buttonH2P = tk.Button(self, text="How to Play", padx=10, pady=10, font=controller.menu_button_font,
                              command=lambda: controller.show_frame("How2PlayPage"))
        buttonLeaderboard = tk.Button(self, text="Leaderboard", padx=10, pady=10, font=controller.menu_button_font,
                                      command=lambda: controller.show_frame("LeaderboardPage"))
        buttonLogout = tk.Button(self, text="Log Out", padx=10, pady=10, font=controller.menu_button_font,
                                 command=lambda: controller.show_frame("LoginMenu"))
        buttonQuit = tk.Button(self, text="Exit game", padx=10, pady=10, font=controller.menu_button_font,
                               command=lambda: controller.breakcode())
        buttonDungeon.grid(row=1, column=2, pady=2, sticky="w")
        buttonTeam.grid(row=2, column=2, pady=2, sticky="w")
        buttonCredit.grid(row=5, column=2, pady=2, sticky="w")
        buttonH2P.grid(row=4, column=2, pady=2, sticky="w")
        buttonLeaderboard.grid(row=3, column=2, pady=2, sticky="w")
        buttonLogout.grid(row=6, column=2, pady=2, sticky="w")
        buttonQuit.grid(row=7, column=2, pady=2, sticky="w")
        invis_label1.grid(column=1, row=1, padx=50)
        invis_label2.grid(column=1, row=2, padx=50)
        invis_label3.grid(column=1, row=3, padx=50)
        invis_label4.grid(column=1, row=4, padx=50)
        invis_label5.grid(column=1, row=5, padx=50)
        invis_label6.grid(column=1, row=6, padx=50)
        invis_label7.grid(column=1, row=7, padx=50)


class DungeonDelve(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Dungeon", font=controller.title_font)
        label.grid(row=0, pady=10)

        buttonReturn = tk.Button(self, text="Return to Menu",
                                 command=lambda: controller.show_frame("MainMenu"))
        buttonReturn.grid()


class CreateTeamPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Champion Camp", font=controller.title_font)
        label.grid(row=0, sticky="nsew", pady=10)
        button = tk.Button(self, text="Return to Menu",
                           command=lambda: controller.show_frame("MainMenu"))
        button.grid()


class CreditPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Credits", font=controller.title_font)
        label.grid(row=0, sticky="nsew", pady=10)
        button = tk.Button(self, text="Return to Menu",
                           command=lambda: controller.show_frame("MainMenu"))
        button.grid()


class How2PlayPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="How To Play", font=controller.title_font)
        label.grid(row=0, sticky="nsew", pady=10)
        button = tk.Button(self, text="Return to Menu",
                           command=lambda: controller.show_frame("MainMenu"))
        button.grid()


class LeaderboardPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Leaderboards", font=controller.title_font)
        label.grid(row=0, sticky="nsew", pady=10)
        button = tk.Button(self, text="Return to Menu",
                           command=lambda: controller.show_frame("MainMenu"))
        button.grid()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
