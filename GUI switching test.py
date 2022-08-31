import os
from Champions import *
from importlib import reload

try:
    import tkinter as tk  # python 3
    from tkinter import font as tkfont, ttk  # python 3
except ImportError:
    import Tkinter as tk  # python 2
    import tkFont as tkfont  # python 2
from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        global computer_username
        tk.Tk.__init__(self, *args, **kwargs)
        self.problem = ttk.Label(self, text="")
        self.title_font = tkfont.Font(family='Times New Roman Baltic', size=120, weight="bold")
        self.small_title_font = tkfont.Font(family='Times New Roman Baltic', size=80, weight="bold")
        self.menu_button_font = tkfont.Font(family='Helvetica', size=18, weight="bold")
        self.geometry('1280x720')
        container = tk.Frame(self)
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        computer_username = os.getlogin()
        self.frames = {}
        for F in (
                OpeningPage, MainMenu, DungeonDelve, CreateTeamPage, CreditPage, How2PlayPage, LeaderboardPage,
                LoginMenu, RegisterMenu, DungeonManagement):
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

    def login_check_password(self, username_entry, password_entry):
        inputted_username = username_entry.get()
        inputted_username.strip()
        inputted_password = password_entry.get()
        inputted_password.strip()
        username_file = open(
            "C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_username.txt".format(computer_username), "r")
        password_file = open(
            "C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_password.txt".format(computer_username), "r")
        no_us_and_pw_warning = "Please enter a username and password"
        no_pw_warning = "Password is missing"
        no_us_warning = "Username is missing"
        invalid_details = "Username and/or Password is incorrect"
        please_wait = "Logging in may take a while. Sit back and relax while we work :)"
        self.problem.destroy()
        self.problem = tk.Label(self, text="")
        self.problem.grid(row=7, column=2, padx=10, pady=10)
        username_file_r = username_file.read()
        username_file.close()
        password_encoder = inputted_username and inputted_password
        username_encoder = inputted_username
        encoded_username = username_encoder.encode("utf-8")
        if inputted_password == "":
            if inputted_username == "":
                self.problem.destroy()
                self.problem = ttk.Label(self, text="")
                self.problem.configure(text=no_us_and_pw_warning)
                self.problem.grid(row=7, column=2, padx=10, pady=10)
            else:
                self.problem.destroy()
                self.problem = ttk.Label(self, text="")
                self.problem.configure(text=no_pw_warning)
                self.problem.grid(row=7, column=2, padx=10, pady=10)
        elif inputted_username == "":
            self.problem.destroy()
            self.problem = ttk.Label(self, text="")
            self.problem.configure(text=no_us_warning)
            self.problem.grid(row=7, column=2, padx=10, pady=10)
        else:
            if str(encoded_username) in username_file_r:
                self.problem.destroy()
                self.problem = ttk.Label(self, text="")
                self.problem.configure(text=please_wait)
                self.problem.grid(row=7, column=2, padx=10, pady=10)
                while True:
                    password_file_r = password_file.readline()
                    if not password_file_r:
                        break
                    try:
                        if bcrypt.check_password_hash(password_file_r, password_encoder):
                            if password_file_r in open(
                                    "C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_password.txt".format(
                                            computer_username), "r"):
                                self.problem.destroy()
                                self.set_current_user(inputted_username)
                                self.login_to_main_menu(username_entry, password_entry)
                            else:
                                breakpoint()
                    except:
                        self.problem.destroy()
                        self.problem = ttk.Label(self, text="")
                        self.problem.configure(text=invalid_details)
                        self.problem.grid(row=7, column=2, padx=10, pady=10)
            else:
                self.problem.destroy()
                self.problem = ttk.Label(self, text="")
                self.problem.configure(text=invalid_details)
                self.problem.grid(row=7, column=2, padx=10, pady=10)

    def set_current_user(self, inputted_username):
        current_user = open(
            "C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_current_username.txt".format(computer_username), "w")
        current_user.write("{}".format(inputted_username))
        current_user.close()

    def get_user(self):
        current_user = open(
            "C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_current_username.txt".format(computer_username), "r")
        current_user_r = current_user.readline()
        for line in current_user_r:
            user = line
            current_user.close()
            return user

    def get_user_encoded(self):
        current_user = open(
            "C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_current_username.txt".format(computer_username), "r")
        current_user_r = current_user.readline()
        for line in current_user_r:
            user = line
            current_user.close()
            user = user.encode("utf-8")
            return str(user)

    def register_check_password(self, username_entry, password_entry, confirm_password_entry):
        global problem
        global encoded_username
        global encoded_password
        inputted_username = username_entry.get()
        inputted_username.strip()
        inputted_password = password_entry.get()
        inputted_password.strip()
        inputted_confirm_password = confirm_password_entry.get()
        inputted_confirm_password.strip()
        username_file = open(
            "C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_username.txt".format(computer_username), "r")
        password_file = open(
            "C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_password.txt".format(computer_username), "r")
        no_us_and_pw_warning = "Username and Password cannot be empty"
        no_pw_warning = "Password cannot be empty"
        no_us_warning = "Username cannot be empty"
        un_unavailable = "Sorry, this username is already being used!"
        not_equal_pw_warning = "Passwords aren't the same"
        self.problem.destroy()
        self.problem = ttk.Label(self, text="")
        self.problem.grid(row=3, column=0, padx=10, pady=10)
        username_file_r = username_file.read()
        username_file.close()
        password_file.close()
        if inputted_password == "":
            if inputted_username == "":
                self.problem.destroy()
                self.problem = ttk.Label(self, text="")
                self.problem.configure(text=no_us_and_pw_warning)
                self.problem.grid(row=3, column=0, padx=10, pady=10)
            else:
                self.problem.destroy()
                self.problem = ttk.Label(self, text="")
                self.problem.configure(text=no_pw_warning)
                self.problem.grid(row=3, column=0, padx=10, pady=10)
        elif inputted_confirm_password == inputted_password:
            password_encoder = inputted_username and inputted_password
            username_encoder = inputted_username
            encoded_username = username_encoder.encode("utf-8")
            encoded_password = bcrypt.generate_password_hash(password_encoder).decode("utf-8")
            if inputted_username == "":
                self.problem.destroy()
                self.problem = ttk.Label(self, text="")
                self.problem.configure(text=no_us_warning)
                self.problem.grid(row=3, column=0, padx=10, pady=10)
            else:
                if str(encoded_username) in username_file_r:
                    self.problem.destroy()
                    self.problem = ttk.Label(self, text="")
                    self.problem.configure(text=un_unavailable)
                    self.problem.grid(row=3, column=0, padx=10, pady=10)

                else:
                    self.problem.destroy()
                    username_file.close()
                    password_file.close()
                    self.final_register_check()
        else:
            self.problem.destroy()
            self.problem = ttk.Label(self, text="")
            self.problem.configure(text=not_equal_pw_warning)
            self.problem.grid(row=3, column=0, padx=10, pady=10)

    def user_account_set(self):
        file = open("C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_username.txt".format(computer_username), "a")
        file.write("\n")
        file.write(str(encoded_username))
        file.close()
        file = open("C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_championTeam_1.txt".format(computer_username),
                    "a")
        file.write("\n")
        file.write(str(encoded_username) + ", ")
        file.close()
        file = open("C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_championTeam_2.txt".format(computer_username),
                    "a")
        file.write("\n")
        file.write(str(encoded_username) + ", ")
        file.close()
        file = open("C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_championTeam_3.txt".format(computer_username),
                    "a")
        file.write("\n")
        file.write(str(encoded_username) + ", ")
        file.close()
        file = open("C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_password.txt".format(computer_username), "a")
        file.write("\n")
        file.write(str(encoded_password))
        file.close()

    def final_register_check(self):
        register_window = registery_window(self)
        registery_window.grab_set(self)

    def register_to_login(self, username_entry, password_entry, confirm_password_entry):
        self.problem.destroy()
        username_entry.delete(0, "end")
        password_entry.delete(0, "end")
        confirm_password_entry.delete(0, "end")
        self.show_frame("LoginMenu")

    def login_to_register(self, username_entry, password_entry):
        self.problem.destroy()
        username_entry.delete(0, "end")
        password_entry.delete(0, "end")
        self.show_frame("RegisterMenu")

    def login_to_main_menu(self, username_entry, password_entry):
        self.problem.destroy()
        username_entry.delete(0, "end")
        password_entry.delete(0, "end")
        self.show_frame("MainMenu")

    def login_to_start(self, username_entry, password_entry):
        self.problem.destroy()
        username_entry.delete(0, "end")
        password_entry.delete(0, "end")
        self.show_frame("OpeningPage")

    def return_users_champion_team1(self, user):
        team_line_1 = ""
        champion_file_1 = open(
            "C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_championTeam_1.txt".format(computer_username), "r")
        champion_file_1_r = champion_file_1.readlines()
        for line in champion_file_1_r:
            try:
                if str(user) in line:
                    team_line_1 = line.replace("{}, ".format(str(user)), "")
                    champion_file_1.close()
                    return team_line_1
            except:
                breakpoint()

    def return_users_champion_team2(self, user):
        team_line_2 = ""
        champion_file_2 = open(
            "C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_championTeam_2.txt".format(computer_username), "r")
        champion_file_2_r = champion_file_2.readlines()
        for line in champion_file_2_r:
            try:
                if str(user) in line:
                    team_line_2 = line.replace("{}, ".format(str(user)), "")
                    champion_file_2.close()
                    return team_line_2
            except:
                breakpoint()

    def return_users_champion_team3(self, user):
        team_line_3 = ""
        champion_file_3 = open(
            "C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_championTeam_3.txt".format(computer_username), "r")
        champion_file_3_r = champion_file_3.readlines()
        for line in champion_file_3_r:
            try:
                if str(user) in line:
                    team_line_3 = line.replace("{}, ".format(str(user)), "")
                    champion_file_3.close()
                    return team_line_3
            except:
                breakpoint()

    def mainmenu_to_login(self, validate_user_button, current_user_label):
        validate_user_button.grid(row=7, column=2, pady=2, sticky="e")
        current_user_label.destroy()
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
        registery_window.destroy(self)


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
        invis_label4 = tk.Label(self)
        Loginbutton = tk.Button(self, text="Login", font=controller.menu_button_font,
                                command=lambda: controller.login_check_password(username_entry, password_entry))
        Regibutton = tk.Button(self, text="Register", font=controller.menu_button_font,
                               command=lambda: controller.login_to_register(username_entry, password_entry))
        Returnbutton = tk.Button(self, text="Back", font=controller.menu_button_font,
                                 command=lambda: controller.login_to_start(username_entry, password_entry))
        username_label = ttk.Label(self, text="Username:")
        username_entry = ttk.Entry(self)
        password_label = ttk.Label(self, text="Password:")
        password_entry = ttk.Entry(self, show="*")
        invis_label1.grid(column=2, row=2, pady=50)
        invis_label2.grid(column=1, row=1, padx=95)
        invis_label3.grid(column=1, row=2, padx=95)
        invis_label4.grid(column=2, row=7, pady=50)
        Loginbutton.grid(row=5, column=2)
        Regibutton.grid(row=6, column=2)
        Returnbutton.grid(row=8, column=2)
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
                                           command=lambda: controller.register_check_password(username_entry,
                                                                                              password_entry,
                                                                                              confirm_password_entry))
        back_to_login = tk.Button(self, text="Back to Login",
                                  command=lambda: controller.register_to_login(username_entry, password_entry,
                                                                               confirm_password_entry))
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
        validate_user_button = tk.Button(self, text="Validate User", font=controller.menu_button_font, command=lambda: self.get_current_user(controller, validate_user_button, current_user_label))
        current_user_label = tk.Label(self)
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
                                 command=lambda: controller.mainmenu_to_login(validate_user_button, current_user_label))
        buttonQuit = tk.Button(self, text="Exit game", padx=10, pady=10, font=controller.menu_button_font,
                               command=lambda: controller.breakcode())
        buttonDungeon.grid(row=1, column=2, pady=2, sticky="w")
        buttonTeam.grid(row=2, column=2, pady=2, sticky="w")
        buttonCredit.grid(row=5, column=2, pady=2, sticky="w")
        buttonH2P.grid(row=4, column=2, pady=2, sticky="w")
        buttonLeaderboard.grid(row=3, column=2, pady=2, sticky="w")
        buttonLogout.grid(row=6, column=2, pady=2, sticky="w")
        buttonQuit.grid(row=7, column=2, pady=2, sticky="w")
        validate_user_button.grid(row=7, column=2, pady=2, sticky="e")
        current_user_label.grid(row=7, column=2, pady=2, sticky="e")
        current_user_label.grid_forget()
        invis_label1.grid(column=1, row=1, padx=50)
        invis_label2.grid(column=1, row=2, padx=50)
        invis_label3.grid(column=1, row=3, padx=50)
        invis_label4.grid(column=1, row=4, padx=50)
        invis_label5.grid(column=1, row=5, padx=50)
        invis_label6.grid(column=1, row=6, padx=50)
        invis_label7.grid(column=1, row=7, padx=50)

    def get_current_user(self, controller, validate_user_button, current_user_label):
        user = SampleApp.get_user(self)
        validate_user_button.grid_forget()
        current_user_label = tk.Label(self, text="Current User: {}".format(user), font=controller.menu_button_font)
        current_user_label.grid(row=7, column=2, pady=2, sticky="e")
        return current_user_label




class DungeonDelve(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Dungeon", font=controller.title_font)
        play_button = tk.Button(self, text="Enter the Dungeon", font=controller.menu_button_font)
        dungeon_settings_button = tk.Button(self, text="Dungeon Management", font=controller.menu_button_font,
                                            command=lambda: controller.show_frame("DungeonManagement"))
        buttonReturn = tk.Button(self, text="Return to Menu", font=controller.menu_button_font,
                                 command=lambda: controller.show_frame("MainMenu"))
        invis_label1 = tk.Label(self)
        invis_label2 = tk.Label(self)
        label.grid(row=1, column=2, pady=20)
        play_button.grid(row=3, column=2, pady=2)
        dungeon_settings_button.grid(row=4, column=2, pady=2)
        buttonReturn.grid(row=6, column=2, pady=2)
        invis_label1.grid(row=1, column=1, padx=140)
        invis_label2.grid(row=2, column=2, pady=50)


class DungeonManagement(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        buttonReturn = tk.Button(self, text="Return to Dungeon", font=controller.menu_button_font,
                                 command=lambda: controller.show_frame("DungeonDelve"))
        buttonReturn.grid()


class CreateTeamPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        user = SampleApp.get_user_encoded(self)
        champion_team = []
        team_line_1 = SampleApp.return_users_champion_team1(self, user)
        champion_team.append(team_line_1)
        team_line_2 = SampleApp.return_users_champion_team2(self, user)
        champion_team.append(team_line_2)
        team_line_3 = SampleApp.return_users_champion_team3(self, user)
        champion_team.append(team_line_3)
        team_1_data = champion_team[0]
        team_2_data = champion_team[1]
        team_3_data = champion_team[2]
        decoded_dungeoneer_team1 = self.team_1_decode(team_1_data)
        decoded_dungeoneer_team2 = self.team_2_decode(team_2_data)
        decoded_dungeoneer_team3 = self.team_3_decode(team_3_data)
        team_1_text = self.display_team1(decoded_dungeoneer_team1)
        team_2_text = self.display_team2(decoded_dungeoneer_team2)
        team_3_text = self.display_team3(decoded_dungeoneer_team3)
        team_1_button_text = self.team_1_button_message(decoded_dungeoneer_team1)
        team_2_button_text = self.team_2_button_message(decoded_dungeoneer_team2)
        team_3_button_text = self.team_3_button_message(decoded_dungeoneer_team3)
        team_1_label = tk.Label(self, text=team_1_text)
        team_2_label = tk.Label(self, text=team_2_text)
        team_3_label = tk.Label(self, text=team_3_text)
        label = tk.Label(self, text="Champion Camp", font=controller.title_font)
        team_1_button = tk.Button(self, text=team_1_button_text)
        team_2_button = tk.Button(self, text=team_2_button_text)
        team_3_button = tk.Button(self, text=team_3_button_text)
        buttonReturn = tk.Button(self, text="Return to Menu",
                                 command=lambda: controller.show_frame("MainMenu"))
        label.grid(row=1, column=2, sticky="nsew", pady=10)
        team_1_label.grid(row=2, column=2)
        team_2_label.grid(row=4, column=2)
        team_3_label.grid(row=6, column=2)
        team_1_button.grid(row=3, column=2)
        team_2_button.grid(row=5, column=2)
        team_3_button.grid(row=7, column=2)
        buttonReturn.grid(row=8, column=2)

    def display_team1(self, decoded_dungeoneer_team1):
        team_1_text = ""
        for character in decoded_dungeoneer_team1:
            team_1_text += "\n"
            team_1_text += character
        return team_1_text

    def display_team2(self, decoded_dungeoneer_team2):
        team_2_text = ""
        for character in decoded_dungeoneer_team2:
            team_2_text += "\n"
            team_2_text += character
        return team_2_text

    def display_team3(self, decoded_dungeoneer_team3):
        team_3_text = ""
        for character in decoded_dungeoneer_team3:
            team_3_text += "\n"
            team_3_text += character
        return team_3_text

    def team_1_button_message(self, decoded_dungeoneer_team1):
        text = ""
        for character in decoded_dungeoneer_team1:
            if character == "Empty":
                text = "Create"
                return text
            else:
                text = "Edit"
        return text

    def team_2_button_message(self, decoded_dungeoneer_team2):
        text = ""
        for character in decoded_dungeoneer_team2:
            if character == "Empty":
                text = "Create"
                return text
            else:
                text = "Edit"
        return text

    def team_3_button_message(self, decoded_dungeoneer_team3):
        text = ""
        for character in decoded_dungeoneer_team3:
            if character == "Empty":
                text = "Create"
                return text
            else:
                text = "Edit"
        return text

    def team_1_decode(self, team_1_data):
        decoded_dungeoneer_team1 = []
        if len(team_1_data) == 0:
            decoded_dungeoneer_team1.append("Empty")
            return decoded_dungeoneer_team1
        else:
            if len(team_1_data) < 5:
                for character in team_1_data:
                    if character == "C1":
                        decoded_dungeoneer_team1.append("Champion1")
                    if character == "C2":
                        decoded_dungeoneer_team1.append("Champion2")
                    if not character:
                        break
            else:
                for character in team_1_data:
                    if character == "C1":
                        decoded_dungeoneer_team1.append("Champion1")
                    if character == "C2":
                        decoded_dungeoneer_team1.append("Champion2")
        if len(decoded_dungeoneer_team1) < 5:
            while len(decoded_dungeoneer_team1) < 5:
                decoded_dungeoneer_team1.append(".")
            return decoded_dungeoneer_team1

    def team_2_decode(self, team_2_data):
        decoded_dungeoneer_team2 = []
        if team_2_data == "":
            decoded_dungeoneer_team2.append("Empty")
            return decoded_dungeoneer_team2
        else:
            if len(team_2_data) < 5:
                for character in team_2_data:
                    if character == "C1":
                        decoded_dungeoneer_team2.append("Champion1")
                    if character == "C2":
                        decoded_dungeoneer_team2.append("Champion2")
                    if not character:
                        break
            else:
                for character in team_2_data:
                    if character == "C1":
                        decoded_dungeoneer_team2.append("Champion1")
                    if character == "C2":
                        decoded_dungeoneer_team2.append("Champion2")
        if len(decoded_dungeoneer_team2) < 5:
            while len(decoded_dungeoneer_team2) < 5:
                decoded_dungeoneer_team2.append(".")
            return decoded_dungeoneer_team2

    def team_3_decode(self, team_3_data):
        decoded_dungeoneer_team3 = []
        if team_3_data == "":
            decoded_dungeoneer_team3.append("Empty")
            return decoded_dungeoneer_team3
        else:
            if len(team_3_data) < 5:
                for character in team_3_data:
                    if character == "C1":
                        decoded_dungeoneer_team3.append("Champion1")
                    if character == "C2":
                        decoded_dungeoneer_team3.append("Champion2")
                    if not character:
                        break
            else:
                for character in team_3_data:
                    if character == "C1":
                        decoded_dungeoneer_team3.append("Champion1")
                    if character == "C2":
                        decoded_dungeoneer_team3.append("Champion2")
        if len(decoded_dungeoneer_team3) < 5:
            while len(decoded_dungeoneer_team3) < 5:
                decoded_dungeoneer_team3.append(".")
            return decoded_dungeoneer_team3


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
