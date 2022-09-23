import os
from Champions import *

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
                LoginMenu, RegisterMenu, DungeonManagement, Team1SelectionPage):
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
        global user
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
        self.problem.destroy()
        self.problem = tk.Label(self, text="")
        self.problem.grid(row=7, column=2, padx=10, pady=10)
        username_file_r = username_file.read()
        username_file.close()
        password_encoder = "{}{}".format(inputted_username, inputted_password)
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
                while True:
                    password_file_r = password_file.readline()
                    if not password_file_r:
                        break
                    password_file_r = password_file_r.replace("\n", "")
                    try:
                        if bcrypt.check_password_hash(password_file_r, password_encoder):
                            self.problem.destroy()
                            user = User(inputted_username)
                            self.set_current_user(inputted_username)
                            self.login_to_main_menu(username_entry, password_entry)
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
        user = current_user_r
        current_user.close()
        return user

    def get_user_encoded(self):
        current_user = open(
            "C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_current_username.txt".format(computer_username), "r")
        current_user_r = current_user.readline()
        user = current_user_r
        user = user.encode("utf-8")
        current_user.close()
        return user

    def register_check_password(self, username_entry, password_entry, confirm_password_entry):
        global problem
        global encode_username
        global encode_password
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
            password_encoder = "{}{}".format(inputted_username, inputted_password)
            username_encoder = inputted_username
            encode_username = username_encoder.encode("utf-8")
            encode_password = bcrypt.generate_password_hash(password_encoder).decode("utf-8")
            if inputted_username == "":
                self.problem.destroy()
                self.problem = ttk.Label(self, text="")
                self.problem.configure(text=no_us_warning)
                self.problem.grid(row=3, column=0, padx=10, pady=10)
            else:
                if str(encode_username) in username_file_r:
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
        file.write(str(encode_username))
        file.close()
        file = open("C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_championTeam_1.txt".format(computer_username),
                    "a")
        file.write("\n")
        file.write(str(encode_username) + ", ")
        file.close()
        file = open("C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_championTeam_2.txt".format(computer_username),
                    "a")
        file.write("\n")
        file.write(str(encode_username) + ", ")
        file.close()
        file = open("C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_championTeam_3.txt".format(computer_username),
                    "a")
        file.write("\n")
        file.write(str(encode_username) + ", ")
        file.close()
        file = open("C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_password.txt".format(computer_username), "a")
        file.write("\n")
        file.write(str(encode_password))
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
        for line in champion_file_1:
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
        for line in champion_file_2:
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
        for line in champion_file_3:
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

    def teamcreation_to_camp(self):
        CreateTeamPage.update_variables()
        self.show_frame("CreateTeamPage")


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


class User():
    def __init__(self, username):
        self.username = username


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
        global update_page_button
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.update_variables()
        label = tk.Label(self, text="Champion Camp", font=controller.title_font)
        team_1_button = tk.Button(self, text=team_1_button_text, command=lambda: controller.show_frame("Team1SelectionPage"))
        team_2_button = tk.Button(self, text=team_2_button_text, command=lambda: controller.show_frame("Team2SelectionPage"))
        team_3_button = tk.Button(self, text=team_3_button_text, command=lambda: controller.show_frame("Team3SelectionPage"))
        update_page_button_2 = tk.Button(self, text="Refresh Team Page", command=self.update_variables)
        update_page_button_2.grid(row=8, column=2)
        buttonReturn = tk.Button(self, text="Return to Menu",
                                 command=lambda: controller.show_frame("MainMenu"))
        label.grid(row=1, column=2, sticky="nsew", pady=10)
        buttonReturn.grid(row=9, column=2)
        team_1_button.grid(row=3, column=2)
        team_2_button.grid(row=5, column=2)
        team_3_button.grid(row=7, column=2)

    def update_variables(self):
        global decoded_dungeoneer_team1,decoded_dungeoneer_team2,decoded_dungeoneer_team3,team_1_button_text,team_2_button_text,team_3_button_text
        user = self.get_user()
        team_1_list_data = []
        team_2_list_data = []
        team_3_list_data = []
        team_line_1 = SampleApp.return_users_champion_team1(self, user)
        team_line_1 = team_line_1.replace(",", "")
        team_1_list_data = team_line_1.split()
        team_line_2 = SampleApp.return_users_champion_team2(self, user)
        team_line_2 = team_line_2.replace(",", "")
        team_2_list_data = team_line_2.split()
        team_line_3 = SampleApp.return_users_champion_team3(self, user)
        team_line_3 = team_line_3.replace(",", "")
        team_3_list_data = team_line_3.split()
        decoded_dungeoneer_team1 = self.team_1_decode(team_1_list_data)
        decoded_dungeoneer_team2 = self.team_2_decode(team_2_list_data)
        decoded_dungeoneer_team3 = self.team_3_decode(team_3_list_data)
        team_1_text = self.display_team1(decoded_dungeoneer_team1)
        team_2_text = self.display_team2(decoded_dungeoneer_team2)
        team_3_text = self.display_team3(decoded_dungeoneer_team3)
        team_1_button_text = self.team_1_button_message(decoded_dungeoneer_team1)
        team_2_button_text = self.team_2_button_message(decoded_dungeoneer_team2)
        team_3_button_text = self.team_3_button_message(decoded_dungeoneer_team3)
        team_1_label = tk.Label(self, text=team_1_text)
        team_2_label = tk.Label(self, text=team_2_text)
        team_3_label = tk.Label(self, text=team_3_text)
        team_1_label.grid(row=2, column=2)
        team_2_label.grid(row=4, column=2)
        team_3_label.grid(row=6, column=2)



    def display_team1(self, decoded_dungeoneer_team1):
        team_1_text = ""
        for character in decoded_dungeoneer_team1:
            team_1_text += "\n"
            team_1_text += character
        return team_1_text

    def get_user(self):
        user = SampleApp.get_user_encoded(self)
        return user

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

    def team_1_decode(self, team_1_list_data):
        decoded_dungeoneer_team1 = []
        if len(team_1_list_data) == 0:
            decoded_dungeoneer_team1.append("Empty")
            return decoded_dungeoneer_team1
        else:
            if len(team_1_list_data) < 5:
                for character in team_1_list_data:
                    if character == "C1":
                        decoded_dungeoneer_team1.append("Champion1")
                    if character == "C2":
                        decoded_dungeoneer_team1.append("Champion2")
                    if character == "C3":
                        decoded_dungeoneer_team1.append("Champion3")
                    if character == "C4":
                        decoded_dungeoneer_team1.append("Champion4")
                    if character == "C5":
                        decoded_dungeoneer_team1.append("Champion5")
                    if not character:
                        break
            else:
                for character in team_1_list_data:
                    if character == "C1":
                        decoded_dungeoneer_team1.append("Champion1")
                    if character == "C2":
                        decoded_dungeoneer_team1.append("Champion2")
                    if character == "C3":
                        decoded_dungeoneer_team1.append("Champion3")
                    if character == "C4":
                        decoded_dungeoneer_team1.append("Champion4")
                    if character == "C5":
                        decoded_dungeoneer_team1.append("Champion5")
                return decoded_dungeoneer_team1
        if len(decoded_dungeoneer_team1) < 5:
            while len(decoded_dungeoneer_team1) < 5:
                decoded_dungeoneer_team1.append(".")
            return decoded_dungeoneer_team1

    def team_2_decode(self, team_2_list_data):
        decoded_dungeoneer_team2 = []
        if len(team_2_list_data) == 0:
            decoded_dungeoneer_team2.append("Empty")
            return decoded_dungeoneer_team2
        else:
            if len(team_2_list_data) < 5:
                for character in team_2_list_data:
                    if character == "C1":
                        decoded_dungeoneer_team2.append("Champion1")
                    if character == "C2":
                        decoded_dungeoneer_team2.append("Champion2")
                    if character == "C3":
                        decoded_dungeoneer_team2.append("Champion3")
                    if character == "C4":
                        decoded_dungeoneer_team2.append("Champion4")
                    if character == "C5":
                        decoded_dungeoneer_team2.append("Champion5")
                    if not character:
                        break
            else:
                for character in team_2_list_data:
                    if character == "C1":
                        decoded_dungeoneer_team2.append("Champion1")
                    if character == "C2":
                        decoded_dungeoneer_team2.append("Champion2")
                    if character == "C3":
                        decoded_dungeoneer_team2.append("Champion3")
                    if character == "C4":
                        decoded_dungeoneer_team2.append("Champion4")
                    if character == "C5":
                        decoded_dungeoneer_team2.append("Champion5")
                return decoded_dungeoneer_team2
        if len(decoded_dungeoneer_team2) < 5:
            while len(decoded_dungeoneer_team2) < 5:
                decoded_dungeoneer_team2.append(".")
            return decoded_dungeoneer_team2

    def team_3_decode(self, team_3_list_data):
        decoded_dungeoneer_team3 = []
        if len(team_3_list_data) == 0:
            decoded_dungeoneer_team3.append("Empty")
            return decoded_dungeoneer_team3
        else:
            if len(team_3_list_data) < 5:
                for character in team_3_list_data:
                    if character == "C1":
                        decoded_dungeoneer_team3.append("Champion1")
                    if character == "C2":
                        decoded_dungeoneer_team3.append("Champion2")
                    if character == "C3":
                        decoded_dungeoneer_team3.append("Champion3")
                    if character == "C4":
                        decoded_dungeoneer_team3.append("Champion4")
                    if character == "C5":
                        decoded_dungeoneer_team3.append("Champion5")
                    if not character:
                        break
            else:
                for character in team_3_list_data:
                    if character == "C1":
                        decoded_dungeoneer_team3.append("Champion1")
                    if character == "C2":
                        decoded_dungeoneer_team3.append("Champion2")
                    if character == "C3":
                        decoded_dungeoneer_team3.append("Champion3")
                    if character == "C4":
                        decoded_dungeoneer_team3.append("Champion4")
                    if character == "C5":
                        decoded_dungeoneer_team3.append("Champion5")
                return decoded_dungeoneer_team3
        if len(decoded_dungeoneer_team3) < 5:
            while len(decoded_dungeoneer_team3) < 5:
                decoded_dungeoneer_team3.append(".")
            return decoded_dungeoneer_team3


class Team1SelectionPage(tk.Frame):
    def __init__(self, parent, controller):
        global update_pageTSP
        global returnButtonTSP
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.menu_button_font = tkfont.Font(family='Helvetica', size=18, weight="bold")
        self.title_label_font = tkfont.Font(family='Helvetica', size=30, weight="bold")
        self.small_label_font = tkfont.Font(family='Helvetica', size=12, weight="bold")
        title = tk.Label(self, text="Champion Camp", font=self.title_label_font)
        update_pageTSP = tk.Button(self, text="Begin Recruiting for Team 1", command=lambda: self.team_creation(invis_label1, invis_label2), font=controller.menu_button_font)
        returnButtonTSP = tk.Button(self, text="Cancel", command=lambda: controller.show_frame("CreateTeamPage"))
        invis_label1 = tk.Label(self)
        invis_label2 = tk.Label(self)
        update_pageTSP.grid(row=2, column=2, pady=50)
        title.grid(row=1, column=2)
        returnButtonTSP.grid(row=13, column=2)
        invis_label1.grid(row=1, column=1, rowspan=4, pady=50, ipadx=240, ipady=100)
        invis_label2.grid(row=1, column=2, pady=100)

    def team_creation(self, invis_label1, invis_label2):
        user = SampleApp.get_user_encoded(self)
        team_line_1 = []
        team_line_1 = SampleApp.return_users_champion_team1(self, user)
        team_line_1 = team_line_1.replace(",", "")
        team_1_list_data = team_line_1.split()
        invis_label3 = tk.Label(self)
        invis_label4= tk.Label(self)
        CTP = CreateTeamPage
        decoded_dungeoneer_team1 = CTP.team_1_decode(self, team_1_list_data)
        tank_section_button = tk.Button(self, text="Tanks", font=self.menu_button_font, width=26, command=self.view_tanks)
        dps_section_button = tk.Button(self, text="Damage Dealers", font=self.menu_button_font, width=26, command=self.view_dps)
        healer_section_button = tk.Button(self, text="Healers", font=self.menu_button_font, width=26, command=self.view_healer)
        your_team_label = tk.Label(self, text=":Your Team:", font=self.small_label_font)
        visual_team_label = tk.Label(self, text=self.display_team1(decoded_dungeoneer_team1))
        confirm_changes_button = tk.Button(self, text="Confirm Changes")
        tank_section_button.grid(row=2, column=1)
        dps_section_button.grid(row=2, column=2, padx=25)
        healer_section_button.grid(row=2, column=3)
        invis_label3.grid(row=2, column=0, padx=6)
        invis_label4.grid(row=9, column=2, pady=45)
        your_team_label.grid(row=10, column=2)
        visual_team_label.grid(row=11, column=2)
        confirm_changes_button.grid(row=12, column=2)
        invis_label1.grid_forget()
        invis_label2.grid_forget()
        update_pageTSP.grid_forget()

    def display_team1(self, decoded_dungeoneer_team1):
        team_1_text = ""
        for character in decoded_dungeoneer_team1:
            team_1_text += character
            team_1_text += ", "
        return team_1_text

    def view_tanks(self):
        global monk_label, monk_button_add, monk_button_details, barbarian_label, barbarian_button_add,\
            barbarian_button_details, bodyguard_label, bodyguard_button_add, bodyguard_button_details, \
            fencer_label, fencer_button_add, fencer_button_details, invis_label3, invis_label4
        invis_label3 = tk.Label(self)
        invis_label4 = tk.Label(self)
        monk_label = tk.Label(self, text=Monk.name, font=self.menu_button_font)
        monk_button_add = tk.Button(self, text="Add to Team")
        monk_button_details = tk.Button(self, text="View Details")
        barbarian_label = tk.Label(self, text=Barbarian.name, font=self.menu_button_font)
        barbarian_button_add = tk.Button(self, text="Add to Team")
        barbarian_button_details = tk.Button(self, text="View Details")
        bodyguard_label = tk.Label(self, text=Veteran_Bodyguard.name, font=self.menu_button_font)
        bodyguard_button_add = tk.Button(self, text="Add to Team")
        bodyguard_button_details = tk.Button(self, text="View Details")
        fencer_label = tk.Label(self, text=Master_Fencer.name, font=self.menu_button_font)
        fencer_button_add = tk.Button(self, text="Add to Team")
        fencer_button_details = tk.Button(self, text="View Details")
        monk_label.grid(row=4, column=1, sticky="e")
        monk_button_add.grid(row=5, column=1, sticky="e", padx=75)
        monk_button_details.grid(row=5, column=1, sticky="e")
        barbarian_label.grid(row=4, column=3, sticky="w")
        barbarian_button_add.grid(row=5, column=3, sticky="w")
        barbarian_button_details.grid(row=5, column=3, sticky="w", padx=80)
        bodyguard_label.grid(row=7, column=1, sticky="e")
        bodyguard_button_add.grid(row=8, column=1, sticky="e", padx=75)
        bodyguard_button_details.grid(row=8, column=1, sticky="e")
        fencer_label.grid(row=7, column=3, sticky="w")
        fencer_button_add.grid(row=8, column=3, sticky="w")
        fencer_button_details.grid(row=8, column=3, sticky="w", padx=80)
        invis_label3.grid(row=3, column=1, columnspan=3, pady=50)
        invis_label4.grid(row=6, column=1, columnspan=3, pady=50)

    def view_dps(self):
        global melee_label, magic_label, mix_label, berserker_label, berserker_button_add, berserker_button_details,\
            rogue_label, rogue_button_add, rogue_button_details, survivalist_label, survivalist_button_add, survivalist_button_details,\
            brawlist_label, brawlist_button_add, brawlist_button_details, academic_mage_label, academic_mage_button_add, academic_mage_button_details,\
            jungle_druid_label, jungle_druid_button_add, jungle_druid_button_details, warlock_label, warlock_button_add, warlock_button_details,\
            bloodmancer_label, bloodmancer_button_add, bloodmancer_button_details, paladin_label, paladin_button_add, paladin_button_details,\
            castle_ranger_label, castle_ranger_button_add, castle_ranger_button_details, thunder_apprentice_label, thunder_apprentice_button_add, thunder_apprentice_button_details,\
            power_conduit_label, power_conduit_button_add, power_conduit_button_details
        monk_label.grid_forget()
        monk_button_add.grid_forget()
        monk_button_details.grid_forget()
        barbarian_label.grid_forget()
        barbarian_button_add.grid_forget()
        barbarian_button_details.grid_forget()
        bodyguard_label.grid_forget()
        bodyguard_button_add.grid_forget()
        bodyguard_button_details.grid_forget()
        fencer_label.grid_forget()
        fencer_button_add.grid_forget()
        fencer_button_details.grid_forget()
        earth_speaker_label.grid_forget()
        earth_speaker_button_add.grid_forget()
        earth_speaker_button_details.grid_forget()
        priest_of_the_devoted_label.grid_forget()
        priest_of_the_devoted_button_add.grid_forget()
        priest_of_the_devoted_button_details.grid_forget()
        time_walker_label.grid_forget()
        time_walker_button_add.grid_forget()
        time_walker_button_details.grid_forget()
        child_of_medicine_label.grid_forget()
        child_of_medicine_button_add.grid_forget()
        child_of_medicine_button_details.grid_forget()
        invis_label3.grid_forget()
        invis_label4.grid_forget()
        melee_label = tk.Label(self, text=":Melee:", font=self.menu_button_font)
        magic_label = tk.Label(self, text=":Magic:", font=self.menu_button_font)
        mix_label = tk.Label(self, text=":Other:", font=self.menu_button_font)
        berserker_label = tk.Label(self, text=Berserker.name)
        berserker_button_add = tk.Button(self, text="Add to Team")
        berserker_button_details = tk.Button(self, text="View Details")
        rogue_label = tk.Label(self, text=Rogue.name)
        rogue_button_add = tk.Button(self, text="Add to Team")
        rogue_button_details = tk.Button(self, text="View Details")
        survivalist_label = tk.Label(self, text=Survivalist.name)
        survivalist_button_add = tk.Button(self, text="Add to Team")
        survivalist_button_details = tk.Button(self, text="View Details")
        brawlist_label = tk.Label(self, text=Brawlist.name)
        brawlist_button_add = tk.Button(self, text="Add to Team")
        brawlist_button_details = tk.Button(self, text="View Details")
        academic_mage_label = tk.Label(self, text=Academic_Mage.name)
        academic_mage_button_add = tk.Button(self, text="Add to Team")
        academic_mage_button_details = tk.Button(self, text="View Details")
        jungle_druid_label = tk.Label(self, text=Jungle_Druid.name)
        jungle_druid_button_add = tk.Button(self, text="Add to Team")
        jungle_druid_button_details = tk.Button(self, text="View Details")
        warlock_label = tk.Label(self, text=Warlock.name)
        warlock_button_add = tk.Button(self, text="Add to Team")
        warlock_button_details = tk.Button(self, text="View Details")
        bloodmancer_label = tk.Label(self, text=Bloodmancer.name)
        bloodmancer_button_add = tk.Button(self, text="Add to Team")
        bloodmancer_button_details = tk.Button(self, text="View Details")
        paladin_label = tk.Label(self, text=Paladin.name)
        paladin_button_add = tk.Button(self, text="Add to Team")
        paladin_button_details = tk.Button(self, text="View Details")
        castle_ranger_label = tk.Label(self, text=Castle_Ranger.name)
        castle_ranger_button_add = tk.Button(self, text="Add to Team")
        castle_ranger_button_details = tk.Button(self, text="View Details")
        thunder_apprentice_label = tk.Label(self, text=Thunder_Apprentice.name)
        thunder_apprentice_button_add = tk.Button(self, text="Add to Team")
        thunder_apprentice_button_details = tk.Button(self, text="View Details")
        power_conduit_label = tk.Label(self, text=Power_Conduit.name)
        power_conduit_button_add = tk.Button(self, text="Add to Team")
        power_conduit_button_details = tk.Button(self, text="View Details")
        melee_label.grid(row=3, column=1)
        magic_label.grid(row=3, column=2)
        mix_label.grid(row=3, column=3)
        berserker_label.grid(row=5, column=1, sticky="w")
        berserker_button_add.grid(row=6, column=1, sticky="w")
        berserker_button_details.grid(row=6, column=1, sticky="w", padx=80)
        rogue_label.grid(row=8, column=1, sticky="w")
        rogue_button_add.grid(row=9, column=1, sticky="w")
        rogue_button_details.grid(row=9, column=1, sticky="w", padx=80)
        survivalist_label.grid(row=5, column=1, sticky="e", padx=10)
        survivalist_button_add.grid(row=6, column=1, sticky="e", padx=85)
        survivalist_button_details.grid(row=6, column=1, sticky="e", padx=10)
        brawlist_label.grid(row=8, column=1, sticky="e", padx=10)
        brawlist_button_add.grid(row=9, column=1, sticky="e", padx=85)
        brawlist_button_details.grid(row=9, column=1, sticky="e", padx=10)
        academic_mage_label.grid(row=5, column=2, sticky="w", padx=10)
        academic_mage_button_add.grid(row=6, column=2, sticky="w", padx=10)
        academic_mage_button_details.grid(row=6, column=2, sticky="w", padx=90)
        jungle_druid_label.grid(row=8, column=2, sticky="w", padx=10)
        jungle_druid_button_add.grid(row=9, column=2, sticky="w", padx=10)
        jungle_druid_button_details.grid(row=9, column=2, sticky="w", padx=90)
        warlock_label.grid(row=5, column=2, sticky="e", padx=10)
        warlock_button_add.grid(row=6, column=2, sticky="e", padx=85)
        warlock_button_details.grid(row=6, column=2, sticky="e", padx=10)
        bloodmancer_label.grid(row=8, column=2, sticky="e", padx=10)
        bloodmancer_button_add.grid(row=9, column=2, sticky="e", padx=85)
        bloodmancer_button_details.grid(row=9, column=2, sticky="e", padx=10)
        paladin_label.grid(row=5, column=3, sticky="w", padx=10)
        paladin_button_add.grid(row=6, column=3, sticky="w", padx=10)
        paladin_button_details.grid(row=6, column=3, sticky="w", padx=90)
        castle_ranger_label.grid(row=8, column=3, sticky="w", padx=10)
        castle_ranger_button_add.grid(row=9, column=3, sticky="w", padx=10)
        castle_ranger_button_details.grid(row=9, column=3, sticky="w", padx=90)
        thunder_apprentice_label.grid(row=5, column=3, sticky="e")
        thunder_apprentice_button_add.grid(row=6, column=3, sticky="e", padx=75)
        thunder_apprentice_button_details.grid(row=6, column=3, sticky="e")
        power_conduit_label.grid(row=8, column=3, sticky="e")
        power_conduit_button_add.grid(row=9, column=3, sticky="e", padx=75)
        power_conduit_button_details.grid(row=9, column=3, sticky="e")
        
    def view_healer(self):
        global earth_speaker_label, earth_speaker_button_add, earth_speaker_button_details, priest_of_the_devoted_label, priest_of_the_devoted_button_add,\
            priest_of_the_devoted_button_details, time_walker_label, time_walker_button_add, time_walker_button_details, \
            child_of_medicine_label, child_of_medicine_button_add, child_of_medicine_button_details, invis_label3, invis_label4
        invis_label3 = tk.Label(self)
        invis_label4 = tk.Label(self)
        earth_speaker_label = tk.Label(self, text=Earth_Speaker.name, font=self.menu_button_font)
        earth_speaker_button_add = tk.Button(self, text="Add to Team")
        earth_speaker_button_details = tk.Button(self, text="View Details")
        priest_of_the_devoted_label = tk.Label(self, text=Priest_of_the_Devoted.name, font=self.menu_button_font)
        priest_of_the_devoted_button_add = tk.Button(self, text="Add to Team")
        priest_of_the_devoted_button_details = tk.Button(self, text="View Details")
        time_walker_label = tk.Label(self, text=Time_Walker.name, font=self.menu_button_font)
        time_walker_button_add = tk.Button(self, text="Add to Team")
        time_walker_button_details = tk.Button(self, text="View Details")
        child_of_medicine_label = tk.Label(self, text=Child_of_Medicine.name, font=self.menu_button_font)
        child_of_medicine_button_add = tk.Button(self, text="Add to Team")
        child_of_medicine_button_details = tk.Button(self, text="View Details")
        earth_speaker_label.grid(row=4, column=1, sticky="e")
        earth_speaker_button_add.grid(row=5, column=1, sticky="e", padx=75)
        earth_speaker_button_details.grid(row=5, column=1, sticky="e")
        priest_of_the_devoted_label.grid(row=4, column=3, sticky="w")
        priest_of_the_devoted_button_add.grid(row=5, column=3, sticky="w")
        priest_of_the_devoted_button_details.grid(row=5, column=3, sticky="w", padx=80)
        time_walker_label.grid(row=7, column=1, sticky="e")
        time_walker_button_add.grid(row=8, column=1, sticky="e", padx=75)
        time_walker_button_details.grid(row=8, column=1, sticky="e")
        child_of_medicine_label.grid(row=7, column=3, sticky="w")
        child_of_medicine_button_add.grid(row=8, column=3, sticky="w")
        child_of_medicine_button_details.grid(row=8, column=3, sticky="w", padx=80)
        invis_label3.grid(row=3, column=1, columnspan=3, pady=50)
        invis_label4.grid(row=6, column=1, columnspan=3, pady=50)


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
