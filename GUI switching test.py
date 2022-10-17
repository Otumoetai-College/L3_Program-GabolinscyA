import os
import random
import math
import sys
from Champions import *
from Monsters import *

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


class ParentClass(tk.Tk):

    def __init__(self, *args, **kwargs):
        global computer_username
        tk.Tk.__init__(self, *args, **kwargs)
        self.problem = ttk.Label(self, text="")
        self.title_font = tkfont.Font(family='Times New Roman Baltic', size=120, weight="bold")
        self.small_title_font = tkfont.Font(family='Times New Roman Baltic', size=80, weight="bold")
        self.medium_text_font_bold = tkfont.Font(family='Times New ROman Baltic', size=50, weight="bold")
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
                LoginMenu, RegisterMenu, DungeonManagement, Team1SelectionPage, GameFrame):
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

    def cancel_new_team1(self):
        Team1SelectionPage.clear_temp_party1(self)
        self.show_frame("CreateTeamPage")

    def finalise_new_team1(self, root):
        Team1SelectionPage.save_new_team1(self, root)
        ParentClass.show_frame(app, "CreateTeamPage")

    def set_dungeon_team(self, decoded_dungeoneer_team1, root):
        current_team = open(
            "C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_dungeon_team.txt".format(computer_username), "w")
        current_team.write(str(decoded_dungeoneer_team1))
        current_team.close()
        root.destroy()
        ParentClass.show_frame(app, "GameFrame")


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
        ParentClass.user_account_set(self)
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
        play_button = tk.Button(self, text="Enter the Dungeon", font=controller.menu_button_font,
                                command=self.team_check)
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

    def team_check(self):
        user = ParentClass.get_user_encoded(self)
        team_line_1 = []
        team_line_1 = ParentClass.return_users_champion_team1(self, user)
        team_line_1 = team_line_1.replace(",", "")
        team_1_list_data = team_line_1.split()
        CTP = CreateTeamPage
        decoded_dungeoneer_team1 = CTP.team_1_decode(self, team_1_list_data)
        if "Empty" in decoded_dungeoneer_team1:
            root = tk.Tk()
            warning_label = tk.Label(root, text="You must have a full team before \n entering the dungeon")
            okButton = tk.Button(root, text="Ok", command=root.destroy)
            warning_label.grid(row=1, column=1)
            okButton.grid(row=3, column=1)
        else:
            self.enter_dungeon_confirmation()

    def enter_dungeon_confirmation(self):
        root = tk.Tk()
        user = ParentClass.get_user_encoded(self)
        team_line_1 = []
        team_line_1 = ParentClass.return_users_champion_team1(self, user)
        team_line_1 = team_line_1.replace(",", "")
        team_1_list_data = team_line_1.split()
        CTP = CreateTeamPage
        SA = ParentClass
        decoded_dungeoneer_team1 = CTP.team_1_decode(self, team_1_list_data)
        message_label = tk.Label(root, text=":Are you sure you want to delve into the dungeon with:")
        visual_team_label = tk.Label(root, text=self.display_team1(decoded_dungeoneer_team1))
        yesButton = tk.Button(root, text="Yes",
                              command=lambda: ParentClass.set_dungeon_team(self, decoded_dungeoneer_team1, root))
        noButton = tk.Button(root, text="No", command=root.destroy)
        message_label.grid(row=1, column=1)
        visual_team_label.grid(row=2, column=1)
        yesButton.grid(row=3, column=1, sticky="w", padx=100)
        noButton.grid(row=3, column=1, sticky="e", padx=100)

    def display_team1(self, decoded_dungeoneer_team1):
        team_1_text = ""
        i = 0
        for character in decoded_dungeoneer_team1:
            if i == 3:
                team_1_text += "\n"
            team_1_text += "["
            team_1_text += character
            team_1_text += "]"
            i += 1
        return team_1_text


class DungeonManagement(tk.Frame):
    def __init__(self, parent, controller):
        global current_selected_dungeon
        tk.Frame.__init__(self, parent)
        self.controller = controller
        smallish_text_font = tkfont.Font(size=12)
        title_label = tk.Label(self, text="Dungeon Settings", font=controller.small_title_font)
        invis_label1 = tk.Label(self)
        invis_label2 = tk.Label(self)
        easymode_label = tk.Label(self, text="The Catacombs", font=smallish_text_font)
        easymode_button = tk.Button(self, text="Easy Dungeon", font=controller.menu_button_font,
                                    command=lambda: self.set_new_dungeon_difficulty("easy"))
        normalmode_label = tk.Label(self, text="The Deep Dark", font=smallish_text_font)
        normalmode_button = tk.Button(self, text="Normal Dungeon", font=controller.menu_button_font,
                                      command=lambda: self.set_new_dungeon_difficulty("normal"))
        hardmode_label = tk.Label(self, text="The Abyss", font=smallish_text_font)
        hardmode_button = tk.Button(self, text="Hard Dungeon", font=controller.menu_button_font,
                                    command=lambda: self.set_new_dungeon_difficulty("hard"))
        buttonReturn = tk.Button(self, text="Return to Dungeon", font=controller.menu_button_font,
                                 command=lambda: controller.show_frame("DungeonDelve"))
        title_label.grid(row=1, column=2)
        invis_label1.grid(row=0, column=0, padx=80, pady=45)
        invis_label2.grid(row=5, column=2, pady=60)
        easymode_label.grid(row=3, column=2, sticky="w", padx=35)
        easymode_button.grid(row=4, column=2, sticky="w")
        normalmode_label.grid(row=3, column=2)
        normalmode_button.grid(row=4, column=2)
        hardmode_label.grid(row=3, column=2, sticky="e", padx=55)
        hardmode_button.grid(row=4, column=2, sticky="e")
        buttonReturn.grid(row=6, column=2)

    def set_new_dungeon_difficulty(self, difficulty):
        global dungeon_difficulty
        if difficulty == "easy":
            dungeon_difficulty_file = open(
                "C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_dungeon_difficulty.txt".format(computer_username),
                "w")
            dungeon_difficulty_file.write("easy")
            dungeon_difficulty_file.close()
        if difficulty == "normal":
            dungeon_difficulty_file = open(
                "C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_dungeon_difficulty.txt".format(computer_username),
                "w")
            dungeon_difficulty_file.write("normal")
            dungeon_difficulty_file.close()
        if difficulty == "hard":
            dungeon_difficulty_file = open(
                "C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_dungeon_difficulty.txt".format(computer_username),
                "w")
            dungeon_difficulty_file.write("hard")
            dungeon_difficulty_file.close()

    def get_easy_dungeon_modifiers(self):
        HEALTH_MODIFIER = 0.05
        ATTACKPOWER_MODIFIER = 0.05
        EASY_DUNGEON_MODIFIERS = []
        EASY_DUNGEON_MODIFIERS.append(HEALTH_MODIFIER)
        EASY_DUNGEON_MODIFIERS.append(ATTACKPOWER_MODIFIER)
        return EASY_DUNGEON_MODIFIERS

    def get_medium_dungeon_modifiers(self):
        HEALTH_MODIFIER = 0.1
        ATTACKPOWER_MODIFIER = 0.1
        MEDIUM_DUNGEON_MODIFIERS = []
        MEDIUM_DUNGEON_MODIFIERS.append(HEALTH_MODIFIER)
        MEDIUM_DUNGEON_MODIFIERS.append(ATTACKPOWER_MODIFIER)
        return MEDIUM_DUNGEON_MODIFIERS

    def get_hard_dungeon_modifiers(self):
        HEALTH_MODIFIER = 0.2
        ATTACKPOWER_MODIFIER = 0.25
        HARD_DUNGEON_MODIFIERS = []
        HARD_DUNGEON_MODIFIERS.append(HEALTH_MODIFIER)
        HARD_DUNGEON_MODIFIERS.append(ATTACKPOWER_MODIFIER)
        return HARD_DUNGEON_MODIFIERS


class GameFrame(tk.Frame):
    def __init__(self, parent, controller):
        global start_ok_button, remember_label, beginning_label, start_invis_label1, beginning_check_interger
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.title_font = tkfont.Font(family='Times New Roman Baltic', size=120, weight="bold")
        self.small_title_font = tkfont.Font(family='Times New Roman Baltic', size=80, weight="bold")
        self.medium_text_font_bold = tkfont.Font(family='Times New Roman Baltic', size=50, weight="bold")
        self.menu_button_font = tkfont.Font(family='Helvetica', size=18, weight="bold")
        self.small_text_font = tkfont.Font(family='Times New Roman Baltic', size=20)
        start_invis_label1 = tk.Label(self)
        start_ok_button = tk.Button(self, text="Ok", font=controller.small_title_font, command=self.begin_dungeon_run)
        remember_label = tk.Label(self, text=":REMEMBER:", font=controller.small_title_font)
        beginning_label = tk.Label(self, text="You cannot save your progress\n You must complete the run in one go",
                                   font=self.medium_text_font_bold)
        start_ok_button.grid(row=3, column=1)
        remember_label.grid(row=1, column=1)
        beginning_label.grid(row=2, column=1)
        start_invis_label1.grid(row=0, column=0, padx=20, pady=20)
        beginning_check_interger = 1

    def begin_dungeon_run(self):
        global beginning_check_interger, dungeon_name_label, delve_button, BDRinvisLabel1, BDR_check_interger, roomLevel, floorLevel, dungeon_settings, dungeon_name_text, permaHealthMod
        if beginning_check_interger == 1:
            start_ok_button.destroy()
            remember_label.destroy()
            beginning_label.destroy()
            start_invis_label1.destroy()
            beginning_check_interger = 0
        read_difficulty_file = open(
            "C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_dungeon_difficulty.txt".format(computer_username),
            "r")
        dungeon_settings = read_difficulty_file.readline()
        if dungeon_settings == "easy":
            dungeon_name_text = "The Catacombs (Easy)"
        if dungeon_settings == "normal":
            dungeon_name_text = "The Deep Dark (Normal)"
        if dungeon_settings == "hard":
            dungeon_name_text = "The Abyss (Hard)"
        read_difficulty_file.close()
        dungeon_name_label = tk.Label(self, text=dungeon_name_text, font=self.medium_text_font_bold)
        delve_button = tk.Button(self, text="Start Floor 1", font=self.medium_text_font_bold,
                                 command=self.set_dungeon_properties)
        BDRinvisLabel1 = tk.Label(self)
        dungeon_name_label.grid(row=1, column=1)
        BDRinvisLabel1.grid(row=2, column=0, padx=155, pady=120)
        delve_button.grid(row=3, column=1)
        BDR_check_interger = 1
        roomLevel = 1
        floorLevel = 1
        permaHealthMod = 0

    def set_dungeon_properties(self):
        global MODIFERS, dungeon_floor_frame, dungeon_game_frame, from_combat
        if dungeon_settings == "easy":
            MODIFERS = DungeonManagement.get_easy_dungeon_modifiers(self)
        elif dungeon_settings == "normal":
            MODIFERS = DungeonManagement.get_medium_dungeon_modifiers(self)
        elif dungeon_settings == "hard":
            MODIFERS = DungeonManagement.get_hard_dungeon_modifiers(self)
        dungeon_floor_frame = ttk.Frame(self)
        dungeon_floor_frame.grid(row=0, column=0, sticky="NSEW")
        dungeon_game_frame = ttk.Frame(dungeon_floor_frame)
        dungeon_game_frame.grid(row=3, column=0, sticky="NSEW")
        from_combat = 0
        self.dungeon_LabelFrame = tk.LabelFrame()
        self.dungeon_LabelFrame.grid(row=0, column=0)
        self.get_individual_champions()
        self.set_champions_stats()
        self.set_up_beginning_champion_stats()
        self.DungeonFloorProgress()

    def get_individual_champions(self):
        global CHAMPION_LIST
        current_team_file = open(
            "C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_dungeon_team.txt".format(computer_username), "r")
        team = current_team_file.readline()
        team = team.replace("[", "")
        team = team.replace("]", "")
        team = team.replace("'", "")
        dungeon_team = list(team.split(", "))
        current_team_file.close()
        counter = 1
        CHAMPION_LIST = []
        for character in dungeon_team:
            if character == MONK.title:
                CHAMPION_LIST.insert(counter, character)
            if character == BARBARIAN.title:
                CHAMPION_LIST.insert(counter, character)
            if character == VETERAN_BODYGUARD.title:
                CHAMPION_LIST.insert(counter, character)
            if character == MASTER_FENCER.title:
                CHAMPION_LIST.insert(counter, character)
            if character == BERSERKER.title:
                CHAMPION_LIST.insert(counter, character)
            if character == ROGUE.title:
                CHAMPION_LIST.insert(counter, character)
            if character == SURVIVALIST.title:
                CHAMPION_LIST.insert(counter, character)
            if character == BRAWLIST.title:
                CHAMPION_LIST.insert(counter, character)
            if character == ACADEMIC_MAGE.title:
                CHAMPION_LIST.insert(counter, character)
            if character == DRUID.title:
                CHAMPION_LIST.insert(counter, character)
            if character == WARLOCK.title:
                CHAMPION_LIST.insert(counter, character)
            if character == BLOODMANCER.title:
                CHAMPION_LIST.insert(counter, character)
            if character == PALADIN.title:
                CHAMPION_LIST.insert(counter, character)
            if character == CASTLE_RANGER.title:
                CHAMPION_LIST.insert(counter, character)
            if character == THUNDER_APPRENTICE.title:
                CHAMPION_LIST.insert(counter, character)
            if character == POWER_CONDUIT.title:
                CHAMPION_LIST.insert(counter, character)
            if character == EARTH_SPEAKER.title:
                CHAMPION_LIST.insert(counter, character)
            if character == PRIEST_OF_THE_DEVOTED.title:
                CHAMPION_LIST.insert(counter, character)
            if character == TIME_WALKER.title:
                CHAMPION_LIST.insert(counter, character)
            if character == CHILD_OF_MEDICINE.title:
                CHAMPION_LIST.insert(counter, character)
            counter += 1

    def set_champions_stats(self):
        global CHAMPION_1_HP, CHAMPION_1_RP, CHAMPION_1_AP, CHAMPION_1_RPNAME, CHAMPION_2_HP, CHAMPION_2_RP, CHAMPION_2_AP, CHAMPION_2_RPNAME, CHAMPION_3_HP, CHAMPION_3_RP, CHAMPION_3_AP, \
            CHAMPION_3_RPNAME, CHAMPION_4_HP, CHAMPION_4_RP, CHAMPION_4_AP, CHAMPION_4_RPNAME, CHAMPION_5_HP, CHAMPION_5_RP, CHAMPION_5_AP, CHAMPION_5_RPNAME, CHAMPION_1_ATTACKLIST, CHAMPION_1_SPECIALLIST \
            , CHAMPION_2_ATTACKLIST, CHAMPION_2_SPECIALLIST, CHAMPION_3_ATTACKLIST, CHAMPION_3_SPECIALLIST, CHAMPION_4_ATTACKLIST, CHAMPION_4_SPECIALLIST, CHAMPION_5_ATTACKLIST, CHAMPION_5_SPECIALLIST
        counter = 1
        champion_hp_list = []
        champion_rp_list = []
        champion_ap_list = []
        champion_rpName_list = []
        champion_attack_list = ""
        champion_specials_list = ""
        for character in CHAMPION_LIST:
            if character == MONK.title:
                champion_hp_list.append(MONK.hp)
                champion_rp_list.append(MONK.rp)
                champion_ap_list.append(MONK.ap)
                champion_rpName_list.append(MONK.rp_name)
                champion_attack_list = MONK.attack_list
                champion_specials_list = MONK.specials_list
            elif character == BARBARIAN.title:
                champion_hp_list.append(BARBARIAN.hp)
                champion_rp_list.append(BARBARIAN.rp)
                champion_ap_list.append(BARBARIAN.ap)
                champion_rpName_list.append(BARBARIAN.rp_name)
                champion_attack_list = BARBARIAN.attack_list
                champion_specials_list = BARBARIAN.specials_list
            elif character == VETERAN_BODYGUARD.title:
                champion_hp_list.append(VETERAN_BODYGUARD.hp)
                champion_rp_list.append(VETERAN_BODYGUARD.rp)
                champion_ap_list.append(VETERAN_BODYGUARD.ap)
                champion_rpName_list.append(VETERAN_BODYGUARD.rp_name)
                champion_attack_list = VETERAN_BODYGUARD.attack_list
                champion_specials_list = VETERAN_BODYGUARD.specials_list
            elif character == MASTER_FENCER.title:
                champion_hp_list.append(MASTER_FENCER.hp)
                champion_rp_list.append(MASTER_FENCER.rp)
                champion_ap_list.append(MASTER_FENCER.ap)
                champion_rpName_list.append(MASTER_FENCER.rp_name)
                champion_attack_list = MASTER_FENCER.attack_list
                champion_specials_list = MASTER_FENCER.specials_list
            elif character == BERSERKER.title:
                champion_hp_list.append(BERSERKER.hp)
                champion_rp_list.append(BERSERKER.rp)
                champion_ap_list.append(BERSERKER.ap)
                champion_rpName_list.append(BERSERKER.rp_name)
                champion_attack_list = BERSERKER.attack_list
                champion_specials_list = BERSERKER.specials_list
            elif character == ROGUE.title:
                champion_hp_list.append(ROGUE.hp)
                champion_rp_list.append(ROGUE.rp)
                champion_ap_list.append(ROGUE.ap)
                champion_rpName_list.append(ROGUE.rp_name)
                champion_attack_list = ROGUE.attack_list
                champion_specials_list = ROGUE.specials_list
            elif character == SURVIVALIST.title:
                champion_hp_list.append(SURVIVALIST.hp)
                champion_rp_list.append(SURVIVALIST.rp)
                champion_ap_list.append(SURVIVALIST.ap)
                champion_rpName_list.append(SURVIVALIST.rp_name)
                champion_attack_list = SURVIVALIST.attack_list
                champion_specials_list = SURVIVALIST.specials_list
            elif character == BRAWLIST.title:
                champion_hp_list.append(BRAWLIST.hp)
                champion_rp_list.append(BRAWLIST.rp)
                champion_ap_list.append(BRAWLIST.ap)
                champion_rpName_list.append(BRAWLIST.rp_name)
                champion_attack_list = BRAWLIST.attack_list
                champion_specials_list = BRAWLIST.specials_list
            elif character == ACADEMIC_MAGE.title:
                champion_hp_list.append(ACADEMIC_MAGE.hp)
                champion_rp_list.append(ACADEMIC_MAGE.rp)
                champion_ap_list.append(ACADEMIC_MAGE.ap)
                champion_rpName_list.append(ACADEMIC_MAGE.rp_name)
                champion_attack_list = ACADEMIC_MAGE.attack_list
                champion_specials_list = ACADEMIC_MAGE.specials_list
            elif character == DRUID.title:
                champion_hp_list.append(DRUID.hp)
                champion_rp_list.append(DRUID.rp)
                champion_ap_list.append(DRUID.ap)
                champion_rpName_list.append(DRUID.rp_name)
                champion_attack_list = DRUID.attack_list
                champion_specials_list = DRUID.specials_list
            elif character == WARLOCK.title:
                champion_hp_list.append(WARLOCK.hp)
                champion_rp_list.append(WARLOCK.rp)
                champion_ap_list.append(WARLOCK.ap)
                champion_rpName_list.append(WARLOCK.rp_name)
                champion_attack_list = WARLOCK.attack_list
                champion_specials_list = WARLOCK.specials_list
            elif character == BLOODMANCER.title:
                champion_hp_list.append(BLOODMANCER.hp)
                champion_rp_list.append(BLOODMANCER.rp)
                champion_ap_list.append(BLOODMANCER.ap)
                champion_rpName_list.append(BLOODMANCER.rp_name)
                champion_attack_list = BLOODMANCER.attack_list
                champion_specials_list = BLOODMANCER.specials_list
            elif character == PALADIN.title:
                champion_hp_list.append(PALADIN.hp)
                champion_rp_list.append(PALADIN.rp)
                champion_ap_list.append(PALADIN.ap)
                champion_rpName_list.append(PALADIN.rp_name)
                champion_attack_list = PALADIN.attack_list
                champion_specials_list = PALADIN.specials_list
            elif character == CASTLE_RANGER.title:
                champion_hp_list.append(CASTLE_RANGER.hp)
                champion_rp_list.append(CASTLE_RANGER.rp)
                champion_ap_list.append(CASTLE_RANGER.ap)
                champion_rpName_list.append(CASTLE_RANGER.rp_name)
                champion_attack_list = CASTLE_RANGER.attack_list
                champion_specials_list = CASTLE_RANGER.specials_list
            elif character == THUNDER_APPRENTICE.title:
                champion_hp_list.append(THUNDER_APPRENTICE.hp)
                champion_rp_list.append(THUNDER_APPRENTICE.rp)
                champion_ap_list.append(THUNDER_APPRENTICE.ap)
                champion_rpName_list.append(THUNDER_APPRENTICE.rp_name)
                champion_attack_list = THUNDER_APPRENTICE.attack_list
                champion_specials_list = THUNDER_APPRENTICE.specials_list
            elif character == POWER_CONDUIT.title:
                champion_hp_list.append(POWER_CONDUIT.hp)
                champion_rp_list.append(POWER_CONDUIT.rp)
                champion_ap_list.append(POWER_CONDUIT.ap)
                champion_rpName_list.append(POWER_CONDUIT.rp_name)
                champion_attack_list = POWER_CONDUIT.attack_list
                champion_specials_list = POWER_CONDUIT.specials_list
            elif character == EARTH_SPEAKER.title:
                champion_hp_list.append(EARTH_SPEAKER.hp)
                champion_rp_list.append(EARTH_SPEAKER.rp)
                champion_ap_list.append(EARTH_SPEAKER.ap)
                champion_rpName_list.append(EARTH_SPEAKER.rp_name)
                champion_attack_list = EARTH_SPEAKER.attack_list
                champion_specials_list = EARTH_SPEAKER.specials_list
            elif character == PRIEST_OF_THE_DEVOTED.title:
                champion_hp_list.append(PRIEST_OF_THE_DEVOTED.hp)
                champion_rp_list.append(PRIEST_OF_THE_DEVOTED.rp)
                champion_ap_list.append(PRIEST_OF_THE_DEVOTED.ap)
                champion_rpName_list.append(PRIEST_OF_THE_DEVOTED.rp_name)
                champion_attack_list = PRIEST_OF_THE_DEVOTED.attack_list
                champion_specials_list = PRIEST_OF_THE_DEVOTED.specials_list
            elif character == TIME_WALKER.title:
                champion_hp_list.append(TIME_WALKER.hp)
                champion_rp_list.append(TIME_WALKER.rp)
                champion_ap_list.append(TIME_WALKER.ap)
                champion_rpName_list.append(TIME_WALKER.rp_name)
                champion_attack_list = TIME_WALKER.attack_list
                champion_specials_list = TIME_WALKER.specials_list
            elif character == CHILD_OF_MEDICINE.title:
                champion_hp_list.append(CHILD_OF_MEDICINE.hp)
                champion_rp_list.append(CHILD_OF_MEDICINE.rp)
                champion_ap_list.append(CHILD_OF_MEDICINE.ap)
                champion_rpName_list.append(CHILD_OF_MEDICINE.rp_name)
                champion_attack_list = CHILD_OF_MEDICINE.attack_list
                champion_specials_list = CHILD_OF_MEDICINE.specials_list
            if counter == 1:
                CHAMPION_1_HP = champion_hp_list[0]
                CHAMPION_1_RP = champion_rp_list[0]
                CHAMPION_1_AP = champion_ap_list[0]
                CHAMPION_1_RPNAME = champion_rpName_list[0]
                CHAMPION_1_ATTACKLIST = champion_attack_list
                CHAMPION_1_SPECIALLIST = champion_specials_list
                champion_hp_list = []
                champion_rp_list = []
                champion_ap_list = []
                champion_rpName_list = []
                champion_attack_list = ""
                champion_specials_list = ""
            elif counter == 2:
                CHAMPION_2_HP = champion_hp_list[0]
                CHAMPION_2_RP = champion_rp_list[0]
                CHAMPION_2_AP = champion_ap_list[0]
                CHAMPION_2_RPNAME = champion_rpName_list[0]
                CHAMPION_2_ATTACKLIST = champion_attack_list
                CHAMPION_2_SPECIALLIST = champion_specials_list
                champion_hp_list = []
                champion_rp_list = []
                champion_ap_list = []
                champion_rpName_list = []
                champion_attack_list = ""
                champion_specials_list = ""
            elif counter == 3:
                CHAMPION_3_HP = champion_hp_list[0]
                CHAMPION_3_RP = champion_rp_list[0]
                CHAMPION_3_AP = champion_ap_list[0]
                CHAMPION_3_RPNAME = champion_rpName_list[0]
                CHAMPION_3_ATTACKLIST = champion_attack_list
                CHAMPION_3_SPECIALLIST = champion_specials_list
                champion_hp_list = []
                champion_rp_list = []
                champion_ap_list = []
                champion_rpName_list = []
                champion_attack_list = ""
                champion_specials_list = ""
            elif counter == 4:
                CHAMPION_4_HP = champion_hp_list[0]
                CHAMPION_4_RP = champion_rp_list[0]
                CHAMPION_4_AP = champion_ap_list[0]
                CHAMPION_4_RPNAME = champion_rpName_list[0]
                CHAMPION_4_ATTACKLIST = champion_attack_list
                CHAMPION_4_SPECIALLIST = champion_specials_list
                champion_hp_list = []
                champion_rp_list = []
                champion_ap_list = []
                champion_rpName_list = []
                champion_attack_list = ""
                champion_specials_list = ""
            elif counter == 5:
                CHAMPION_5_HP = champion_hp_list[0]
                CHAMPION_5_RP = champion_rp_list[0]
                CHAMPION_5_AP = champion_ap_list[0]
                CHAMPION_5_RPNAME = champion_rpName_list[0]
                CHAMPION_5_ATTACKLIST = champion_attack_list
                CHAMPION_5_SPECIALLIST = champion_specials_list
                champion_hp_list = []
                champion_rp_list = []
                champion_ap_list = []
                champion_rpName_list = []
                champion_attack_list = ""
                champion_specials_list = ""
            counter += 1

    def set_monster_encounter(self):
        global AI_ATTACKS, AI_GROUP_HP, AI_ATTACKPOWER, AI_SPAWNED, AI_ENTRY_WORD, AI_NICKNAME, \
            AI_NAME, AI_RESOURCE, AI_RESOURCE_NAME, ai1_hp, ai2_hp, ai3_hp, ai4_hp, ai5_hp, ai1_rp, ai2_rp, ai3_rp, \
            ai4_rp, ai5_rp, ai1_max_hp, ai2_max_hp, ai3_max_hp, ai4_max_hp, ai5_max_hp
        NUM_SPAWNED_MONSTERS = [1, 2, 3, 4, 5]
        random.shuffle(NUM_SPAWNED_MONSTERS)
        if NUM_SPAWNED_MONSTERS[0] == 1:
            ai_type = [GROTHAK_THE_DESTROYER.name]  # will create variety later
        elif NUM_SPAWNED_MONSTERS[0] == 2:
            ai_type = [WORMPULP_BROTHERS.name]  # will create variety later
        elif NUM_SPAWNED_MONSTERS[0] == 3:
            ai_type = [SIREN_TRIPLETS.name]  # will create variety later
        elif NUM_SPAWNED_MONSTERS[0] == 4:
            ai_type = [VEMONSKIN_TROGGIES.name]  # will create variety later
        elif NUM_SPAWNED_MONSTERS[0] == 5:
            ai_type = [GIANT_LOCUST_SWARM.name]  # will create variety later
        random.shuffle(ai_type)
        monster_ai = ai_type[0]
        if monster_ai == GROTHAK_THE_DESTROYER.name:
            AI_ATTACKS = GROTHAK_THE_DESTROYER.attack_list  # will add more later
            AI_GROUP_HP = GROTHAK_THE_DESTROYER.hp
            AI_ATTACKPOWER = GROTHAK_THE_DESTROYER.ap
            AI_SPAWNED = GROTHAK_THE_DESTROYER.ai_spawned
            AI_ENTRY_WORD = GROTHAK_THE_DESTROYER.enter_word
            AI_NICKNAME = GROTHAK_THE_DESTROYER.nickname
            AI_NAME = GROTHAK_THE_DESTROYER.name
            AI_RESOURCE = GROTHAK_THE_DESTROYER.rp
            AI_RESOURCE_NAME = GROTHAK_THE_DESTROYER.rp_name
        elif monster_ai == WORMPULP_BROTHERS.name:
            AI_ATTACKS = WORMPULP_BROTHERS.attack_list  # will add more later
            AI_GROUP_HP = WORMPULP_BROTHERS.hp
            AI_ATTACKPOWER = WORMPULP_BROTHERS.ap
            AI_SPAWNED = WORMPULP_BROTHERS.ai_spawned
            AI_ENTRY_WORD = WORMPULP_BROTHERS.enter_word
            AI_NICKNAME = WORMPULP_BROTHERS.nickname
            AI_NAME = WORMPULP_BROTHERS.name
            AI_RESOURCE = WORMPULP_BROTHERS.rp
            AI_RESOURCE_NAME = WORMPULP_BROTHERS.rp_name
        elif monster_ai == SIREN_TRIPLETS.name:
            AI_ATTACKS = SIREN_TRIPLETS.attack_list  # will add more later
            AI_GROUP_HP = SIREN_TRIPLETS.hp
            AI_ATTACKPOWER = SIREN_TRIPLETS.ap
            AI_SPAWNED = SIREN_TRIPLETS.ai_spawned
            AI_ENTRY_WORD = SIREN_TRIPLETS.enter_word
            AI_NICKNAME = SIREN_TRIPLETS.nickname
            AI_NAME = SIREN_TRIPLETS.name
            AI_RESOURCE = SIREN_TRIPLETS.rp
            AI_RESOURCE_NAME = SIREN_TRIPLETS.rp_name
        elif monster_ai == VEMONSKIN_TROGGIES.name:
            AI_ATTACKS = VEMONSKIN_TROGGIES.attack_list  # will add more later
            AI_GROUP_HP = VEMONSKIN_TROGGIES.hp
            AI_ATTACKPOWER = VEMONSKIN_TROGGIES.ap
            AI_SPAWNED = VEMONSKIN_TROGGIES.ai_spawned
            AI_ENTRY_WORD = VEMONSKIN_TROGGIES.enter_word
            AI_NICKNAME = VEMONSKIN_TROGGIES.nickname
            AI_NAME = VEMONSKIN_TROGGIES.name
            AI_RESOURCE = VEMONSKIN_TROGGIES.rp
            AI_RESOURCE_NAME = VEMONSKIN_TROGGIES.rp_name
        elif monster_ai == GIANT_LOCUST_SWARM.name:
            AI_ATTACKS = GIANT_LOCUST_SWARM.attack_list  # will add more later
            AI_GROUP_HP = GIANT_LOCUST_SWARM.hp
            AI_ATTACKPOWER = GIANT_LOCUST_SWARM.ap
            AI_SPAWNED = GIANT_LOCUST_SWARM.ai_spawned
            AI_ENTRY_WORD = GIANT_LOCUST_SWARM.enter_word
            AI_NICKNAME = GIANT_LOCUST_SWARM.nickname
            AI_NAME = GIANT_LOCUST_SWARM.name
            AI_RESOURCE = GIANT_LOCUST_SWARM.rp
            AI_RESOURCE_NAME = GIANT_LOCUST_SWARM.rp_name
        aiEnemyNA = 0
        if AI_SPAWNED == 1:
            ai1_hp = math.ceil(AI_GROUP_HP * (1 + health_modifier))
            ai2_hp = aiEnemyNA
            ai3_hp = aiEnemyNA
            ai4_hp = aiEnemyNA
            ai5_hp = aiEnemyNA
        if AI_SPAWNED == 2:
            ai1_hp = math.ceil(AI_GROUP_HP * (1 + health_modifier))
            ai2_hp = math.ceil(AI_GROUP_HP * (1 + health_modifier))
            ai3_hp = aiEnemyNA
            ai4_hp = aiEnemyNA
            ai5_hp = aiEnemyNA
        if AI_SPAWNED == 3:
            ai1_hp = math.ceil(AI_GROUP_HP * (1 + health_modifier))
            ai2_hp = math.ceil(AI_GROUP_HP * (1 + health_modifier))
            ai3_hp = math.ceil(AI_GROUP_HP * (1 + health_modifier))
            ai4_hp = aiEnemyNA
            ai5_hp = aiEnemyNA
        if AI_SPAWNED == 4:
            ai1_hp = math.ceil(AI_GROUP_HP * (1 + health_modifier))
            ai2_hp = math.ceil(AI_GROUP_HP * (1 + health_modifier))
            ai3_hp = math.ceil(AI_GROUP_HP * (1 + health_modifier))
            ai4_hp = math.ceil(AI_GROUP_HP * (1 + health_modifier))
            ai5_hp = aiEnemyNA
        if AI_SPAWNED == 5:
            ai1_hp = math.ceil(AI_GROUP_HP * (1 + health_modifier))
            ai2_hp = math.ceil(AI_GROUP_HP * (1 + health_modifier))
            ai3_hp = math.ceil(AI_GROUP_HP * (1 + health_modifier))
            ai4_hp = math.ceil(AI_GROUP_HP * (1 + health_modifier))
            ai5_hp = math.ceil(AI_GROUP_HP * (1 + health_modifier))
        if AI_RESOURCE_NAME == "null":
            ai1_rp = "null"
            ai2_rp = "null"
            ai3_rp = "null"
            ai4_rp = "null"
            ai5_rp = "null"
        else:
            ai1_rp = AI_RESOURCE
            ai2_rp = AI_RESOURCE
            ai3_rp = AI_RESOURCE
            ai4_rp = AI_RESOURCE
            ai5_rp = AI_RESOURCE
        ai1_max_hp = ai1_hp
        ai2_max_hp = ai2_hp
        ai3_max_hp = ai3_hp
        ai4_max_hp = ai4_hp
        ai5_max_hp = ai5_hp
        global club_slam_requirements, violent_thrash_requirements, twilight_beam_requirements, spear_stab_requirements, \
            bite_requirements
        if AI_NAME == "Grothak the Destroyer":
            club_slam_requirements = [0, 0, 0]
        if AI_NAME == "Wormpulp Brothers":
            violent_thrash_requirements = [0, 0, 0]
        if AI_NAME == "Siren Triplets":
            twilight_beam_requirements = [25, 0, 0]
        if AI_NAME == "Venomskin Troggies":
            spear_stab_requirements = [0, 0, 0]
        if AI_NAME == "Giant Locust Swarm":
            bite_requirements = [0, 0, 0]

    def set_up_beginning_champion_stats(self):
        global champion1_hp, champion1_ap, champion1_rp, champion1_rpName, champion2_hp, champion2_ap, champion2_rp, champion2_rpName, \
            champion3_hp, champion3_ap, champion3_rp, champion3_rpName, champion4_hp, champion4_ap, champion4_rp, champion4_rpName, \
            champion5_hp, champion5_ap, champion5_rp, champion5_rpName, champion1_small_external_buffs, champion1_big_external_buffs, \
            champion2_small_external_buffs, champion2_big_external_buffs, champion3_small_external_buffs, champion3_big_external_buffs, \
            champion4_small_external_buffs, champion4_big_external_buffs, champion5_small_external_buffs, champion5_big_external_buffs, \
        void_infusion_stacks, champion1_blessing, champion2_blessing, champion3_blessing, champion4_blessing, champion5_blessing
        champion1_hp = CHAMPION_1_HP
        champion1_ap = CHAMPION_1_AP
        void_infusion_stacks = 0
        champion1_blessing = [0, 0]
        champion2_blessing = [0, 0]
        champion3_blessing = [0, 0]
        champion4_blessing = [0, 0]
        champion5_blessing = [0, 0]
        if CHAMPION_1_RPNAME == "Mana":
            champion1_rp = CHAMPION_1_RP
        else:
            champion1_rp = 0
        champion1_rpName = CHAMPION_1_RPNAME
        champion1_small_external_buffs = [0]
        champion1_big_external_buffs = [0]
        champion2_hp = CHAMPION_2_HP
        champion2_ap = CHAMPION_2_AP
        if CHAMPION_2_RPNAME == "Mana":
            champion2_rp = CHAMPION_2_RP
        else:
            champion2_rp = 0
        champion2_rpName = CHAMPION_2_RPNAME
        champion2_small_external_buffs = [0]
        champion2_big_external_buffs = [0]
        champion3_hp = CHAMPION_3_HP
        champion3_ap = CHAMPION_3_AP
        if CHAMPION_3_RPNAME == "Mana":
            champion3_rp = CHAMPION_3_RP
        else:
            champion3_rp = 0
        champion3_rpName = CHAMPION_3_RPNAME
        champion3_small_external_buffs = [0]
        champion3_big_external_buffs = [0]
        champion4_hp = CHAMPION_4_HP
        champion4_ap = CHAMPION_4_AP
        if CHAMPION_4_RPNAME == "Mana":
            champion4_rp = CHAMPION_4_RP
        else:
            champion4_rp = 0
        champion4_rpName = CHAMPION_4_RPNAME
        champion4_small_external_buffs = [0]
        champion4_big_external_buffs = [0]
        champion5_hp = CHAMPION_5_HP
        champion5_ap = CHAMPION_5_AP
        if CHAMPION_5_RPNAME == "Mana":
            champion5_rp = CHAMPION_5_RP
        else:
            champion5_rp = 0
        champion5_rpName = CHAMPION_5_RPNAME
        champion5_small_external_buffs = [0]
        champion5_big_external_buffs = [0]
        global palm_strike_requirements, leg_sweep_requirements, harmonize_requirements, pressure_points_requirements, \
            bloodthirst_requirements, pulverize_requirements, challenging_shout_requirements, impactful_boast_requirements, \
            shield_bash_requirements, trainwreck_requirements, fortification_requirements, block_requirements, \
            pierce_requirements, disruptive_slash_requirements, parry_requirements, elusive_measures_requirements
        # Monk Abilities:
        palm_strike_requirements = [0, 0, 0, 20]
        leg_sweep_requirements = [30, 0, 2, 0]
        harmonize_requirements = [50, 0, 0, 0]
        pressure_points_requirements = [30, 0, 5, 0]
        # Barbarian Abiltities:
        bloodthirst_requirements = [0, 0, 0, 30]
        pulverize_requirements = [20, 0, 0, 0]
        challenging_shout_requirements = [40, 0, 2, 20]
        impactful_boast_requirements = [20, 0, 0, 0]
        # Veteran Bodyguard Abilities:
        shield_bash_requirements = [0, 0, 0, 0]
        trainwreck_requirements = [0, 0, 1, 0]
        fortification_requirements = [0, 0, 2, 0]
        block_requirements = [0, 0, 0, 0]
        # Master Fencer Abilities
        pierce_requirements = [0, 0, 0, 0]
        disruptive_slash_requirements = [0, 0, 2, 0]
        parry_requirements = [0, 0, 2, 0]
        elusive_measures_requirements = [0, 0, 1, 0]
        global raging_blow_requirements, rampage_requirements, enrage_requirements, reckless_flurry_requirements, \
            serrated_slash_requirements, eviscerate_requirements, garrote_requirements, exploit_weakness_requirements, \
            spear_thrust_requirements, scrap_bomb_requirements, play_dead_requirements, rushed_rest_requirements, \
            tactical_punch_requirements, uppercut_requirements, defensive_stance_requirements, rushdown_requirements
        # Berserker Abilities
        raging_blow_requirements = [0, 0, 0, 40]
        rampage_requirements = [80, 0, 0, 0]
        enrage_requirements = [0, 0, 0, 30]
        reckless_flurry_requirements = [40, 0, 2, 0]
        # Rogue Abilities
        serrated_slash_requirements = [0, 0, 0, 0]
        eviscerate_requirements = [0, 0, 2, 0]
        garrote_requirements = [0, 0, 0, 0]
        exploit_weakness_requirements = [0, 0, 4, 0]
        # Survivalist Abilities
        spear_thrust_requirements = [0, 0, 0, 0]
        scrap_bomb_requirements = [0, 0, 2, 0]
        play_dead_requirements = [0, 0, 3, 0]
        rushed_rest_requirements = [0, 0, 2, 0]
        # Brawlist Abilties
        tactical_punch_requirements = [0, 0, 0, 0]
        uppercut_requirements = [0, 0, 2, 0]
        defensive_stance_requirements = [0, 0, 2, 0]
        rushdown_requirements = [0, 0, 3, 0]
        global frost_bolt_requirements, fireball_requirements, arcane_brilliance_requirements, magical_barrier_requirements, \
            venusfly_snap_requirements, vine_swipe_requirements, thorns_requirements, prickle_arena_requirements, \
            black_bolt_requirements, void_infusion_requirements, wound_fissure_requirements, soul_tap_requirements, \
            drain_life_requirements, blood_spike_requirements, blood_boil_requirements, enharden_nerves_requirements
        # Academic Mage Abilities
        frost_bolt_requirements = [20, 0, 0, 0]
        fireball_requirements = [30, 0, 0, 0]
        arcane_brilliance_requirements = [100, 0, 5, 0]
        magical_barrier_requirements = [20, 0, 0, 0]
        # Druid Abilities
        venusfly_snap_requirements = [40, 0, 0, 0]
        vine_swipe_requirements = [20, 0, 1, 0]
        thorns_requirements = [10, 0, 0, 0]
        prickle_arena_requirements = [30, 0, 4, 0]
        # Warlock Abilities
        black_bolt_requirements = [25, 0, 0, 0]
        void_infusion_requirements = [100, 0, 0, 0]
        wound_fissure_requirements = [50, 0, 3, 0]
        soul_tap_requirements = [0, 0, 0, 0]
        # Bloodmancer Abilities
        drain_life_requirements = [0, 0, 0, 0]
        blood_spike_requirements = [200, 0, 0, 0]
        blood_boil_requirements = [0, 0, 3, 0]
        enharden_nerves_requirements = [0, 0, 2, 0]
        global overhand_justice_requirements, righteous_blow_requirements, aura_of_power_requirements, aura_of_protection_requirements, \
            steady_shot_requirements, power_opt_requirements, equip_iron_cast_arrows_requirements, equip_tracker_tipped_arrows_requirements, \
            lightning_bolt_requirements, chain_lightning_requirements, crashing_boom_requirements, thunderous_vigor_requirements, \
            muscle_enlarger_requirements, mistic_bloom_requirements, power_surge_requirements, full_potential_requirements
        # Paladin Abilities
        overhand_justice_requirements = [0, 0, 0, 0]
        righteous_blow_requirements = [0, 0, 2, 0]
        aura_of_power_requirements = [0, 0, 1, 0]
        aura_of_protection_requirements = [0, 0, 1, 0]
        # Castle Ranger Abilitites
        steady_shot_requirements = [0, 0, 0, 0]
        power_opt_requirements = [0, 0, 1, 0]
        equip_iron_cast_arrows_requirements = [0, 0, 1, 0]
        equip_tracker_tipped_arrows_requirements = [0, 0, 1, 0]
        # Thunder Apprentice Abilities
        lightning_bolt_requirements = [0, 0, 0, 0]
        chain_lightning_requirements = [0, 0, 0, 0]
        crashing_boom_requirements = [0, 0, 4, 0]
        thunderous_vigor_requirements = [0, 0, 6, 0]
        # Power Conduit Abilities
        muscle_enlarger_requirements = [0, 0, 0, 1]
        mistic_bloom_requirements = [0, 0, 0, 1]
        power_surge_requirements = [3, 0, 0, 0]
        full_potential_requirements = [3, 0, 0, 0]
        global rock_barrage_requirements, healing_surge_requirements, rejuvenating_whirlpool_requirements, boulder_cocoon_requirements, \
            shimmering_bolt_requirements, divine_smite_requirements, healing_light_requirements, diffracting_nova_requirements, \
            cybernetic_blast_requirements, nanoheal_bots_requirements, reverse_wounds_requirements, alter_time_requirements, \
            throw_scissors_requirements, bandage_wound_requirements, perfected_herbal_tea_requirements, g3t_jaxd_requirements
        # Earth Speaker Abilities
        rock_barrage_requirements = [0, 0, 0, 30]
        healing_surge_requirements = [40, 0, 0, 0]
        rejuvenating_whirlpool_requirements = [50, 0, 1, 0]
        boulder_cocoon_requirements = [100, 0, 0, 0]
        # Priest of the Devoted Abilities
        shimmering_bolt_requirements = [0, 0, 0, 30]
        divine_smite_requirements = [70, 0, 0, 0]
        healing_light_requirements = [20, 0, 0, 0]
        diffracting_nova_requirements = [30, 0, 0, 0]
        # Time Walker Abilities
        cybernetic_blast_requirements = [0, 0, 0, 30]
        nanoheal_bots_requirements = [20, 0, 0, 0]
        reverse_wounds_requirements = [50, 0, 0, 0]
        alter_time_requirements = [180, 0, 5, 0]
        # Child of Medicine Abilities
        throw_scissors_requirements = [0, 0, 0, 0]
        bandage_wound_requirements = [0, 0, 0, 0]
        perfected_herbal_tea_requirements = [0, 0, 1, 0]
        g3t_jaxd_requirements = [0, 0, 4, 0]

    def DungeonFloorProgress(self):
        global BDR_check_interger, teams_current_condition_label, current_floor_label, floor_room_modifiers_label, from_combat
        if BDR_check_interger == 1:
            dungeon_name_label.destroy()
            delve_button.destroy()
            BDRinvisLabel1.destroy()
            BDR_check_interger = 0
        if from_combat == 1:
            floor_room_modifiers_label.destroy()
            from_combat = 0
        current_dungeon_label = tk.Label(dungeon_floor_frame, text=dungeon_name_text, font=self.small_text_font)
        current_floor_label = tk.Label(dungeon_floor_frame, text="Floor {} : Room {}".format(floorLevel, roomLevel),
                                       font=self.medium_text_font_bold)
        teams_current_condition_label = tk.Label(dungeon_floor_frame, text=":Your Team's Current Condition:",
                                                 font=self.small_text_font)
        champion1_label = tk.Label(dungeon_game_frame, text=CHAMPION_LIST[0], font=self.small_text_font, width=16)
        champion2_label = tk.Label(dungeon_game_frame, text=CHAMPION_LIST[1], font=self.small_text_font, width=16)
        champion3_label = tk.Label(dungeon_game_frame, text=CHAMPION_LIST[2], font=self.small_text_font, width=16)
        champion4_label = tk.Label(dungeon_game_frame, text=CHAMPION_LIST[3], font=self.small_text_font, width=16)
        champion5_label = tk.Label(dungeon_game_frame, text=CHAMPION_LIST[4], font=self.small_text_font, width=16)
        champion1_status = tk.Label(dungeon_game_frame, text=self.champion_floorMenu_status_text(1), width=20)
        champion2_status = tk.Label(dungeon_game_frame, text=self.champion_floorMenu_status_text(2), width=20)
        champion3_status = tk.Label(dungeon_game_frame, text=self.champion_floorMenu_status_text(3), width=20)
        champion4_status = tk.Label(dungeon_game_frame, text=self.champion_floorMenu_status_text(4), width=20)
        champion5_status = tk.Label(dungeon_game_frame, text=self.champion_floorMenu_status_text(5), width=20)
        proceed_button = tk.Button(dungeon_game_frame, text="Proceed", font=self.menu_button_font,
                                   command=self.combat_monster_setup)
        CLFinvis_label = tk.Label(dungeon_game_frame)
        teams_current_condition_label.grid(row=2, column=0)
        champion1_label.grid(row=4, column=1)
        champion2_label.grid(row=4, column=2)
        champion3_label.grid(row=4, column=3)
        champion4_label.grid(row=4, column=4)
        champion5_label.grid(row=4, column=5)
        champion1_status.grid(row=5, column=1)
        champion2_status.grid(row=5, column=2)
        champion3_status.grid(row=5, column=3)
        champion4_status.grid(row=5, column=4)
        champion5_status.grid(row=5, column=5)
        CLFinvis_label.grid(row=6, column=3, pady=100)
        proceed_button.grid(row=7, column=3)
        current_dungeon_label.grid(row=0, column=0)
        current_floor_label.grid(row=1, column=0)

    def champion_floorMenu_status_text(self, champion_position):
        if champion_position == 1:
            if CHAMPION_1_RPNAME == "null":
                if champion1_hp == 0:
                    status_text = "*DEAD*\nHealth Points: {}/{}\n".format(champion1_hp, CHAMPION_1_HP)
                    return status_text
                else:
                    status_text = "\nHealth Points: {}/{}\n".format(champion1_hp, CHAMPION_1_HP)
                    return status_text
            else:
                if champion1_hp == 0:
                    status_text = "*DEAD*\nHealth Points: {}/{}\n{}: {}/{}".format(champion1_hp, CHAMPION_1_HP,
                                                                                   CHAMPION_1_RPNAME, champion1_rp,
                                                                                   CHAMPION_1_RP)
                    return status_text
                else:
                    status_text = "\nHealth Points: {}/{}\n{}: {}/{}".format(champion1_hp, CHAMPION_1_HP,
                                                                             CHAMPION_1_RPNAME, champion1_rp,
                                                                             CHAMPION_1_RP)
                    return status_text
        if champion_position == 2:
            if CHAMPION_2_RPNAME == "null":
                if champion2_hp == 0:
                    status_text = "*DEAD*\nHealth Points: {}/{}\n".format(champion2_hp, CHAMPION_2_HP)
                    return status_text
                else:
                    status_text = "\nHealth Points: {}/{}\n".format(champion2_hp, CHAMPION_2_HP)
                    return status_text
            else:
                if champion2_hp == 0:
                    status_text = "*DEAD*\nHealth Points: {}/{}\n{}: {}/{}".format(champion2_hp, CHAMPION_2_HP,
                                                                                   CHAMPION_2_RPNAME, champion2_rp,
                                                                                   CHAMPION_2_RP)
                    return status_text
                else:
                    status_text = "\nHealth Points: {}/{}\n{}: {}/{}".format(champion2_hp, CHAMPION_2_HP,
                                                                             CHAMPION_2_RPNAME, champion2_rp,
                                                                             CHAMPION_2_RP)
                    return status_text
        if champion_position == 3:
            if CHAMPION_3_RPNAME == "null":
                if champion3_hp == 0:
                    status_text = "*DEAD*\nHealth Points: {}/{}\n".format(champion3_hp, CHAMPION_3_HP)
                    return status_text
                else:
                    status_text = "\nHealth Points: {}/{}\n".format(champion3_hp, CHAMPION_3_HP)
                    return status_text
            else:
                if champion3_hp == 0:
                    status_text = "*DEAD*\nHealth Points: {}/{}\n{}: {}/{}".format(champion3_hp, CHAMPION_3_HP,
                                                                                   CHAMPION_3_RPNAME, champion3_rp,
                                                                                   CHAMPION_3_RP)
                    return status_text
                else:
                    status_text = "\nHealth Points: {}/{}\n{}: {}/{}".format(champion3_hp, CHAMPION_3_HP,
                                                                             CHAMPION_3_RPNAME, champion3_rp,
                                                                             CHAMPION_3_RP)
                    return status_text
        if champion_position == 4:
            if CHAMPION_4_RPNAME == "null":
                if champion4_hp == 0:
                    status_text = "*DEAD*\nHealth Points: {}/{}\n".format(champion4_hp, CHAMPION_4_HP)
                    return status_text
                else:
                    status_text = "\nHealth Points: {}/{}\n".format(champion4_hp, CHAMPION_4_HP)
                    return status_text
            else:
                if champion4_hp == 0:
                    status_text = "*DEAD*\nHealth Points: {}/{}\n{}: {}/{}".format(champion4_hp, CHAMPION_4_HP,
                                                                                   CHAMPION_4_RPNAME, champion4_rp,
                                                                                   CHAMPION_4_RP)
                    return status_text
                else:
                    status_text = "\nHealth Points: {}/{}\n{}: {}/{}".format(champion4_hp, CHAMPION_4_HP,
                                                                             CHAMPION_4_RPNAME, champion4_rp,
                                                                             CHAMPION_4_RP)
                    return status_text
        if champion_position == 5:
            if CHAMPION_5_RPNAME == "null":
                if champion5_hp == 0:
                    status_text = "*DEAD*\nHealth Points: {}/{}\n".format(champion5_hp, CHAMPION_5_HP)
                    return status_text
                else:
                    status_text = "\nHealth Points: {}/{}\n".format(champion5_hp, CHAMPION_5_HP)
                    return status_text
            else:
                if champion5_hp == 0:
                    status_text = "*DEAD*\nHealth Points: {}/{}\n{}: {}/{}".format(champion5_hp, CHAMPION_5_HP,
                                                                                   CHAMPION_5_RPNAME, champion5_rp,
                                                                                   CHAMPION_5_RP)
                    return status_text
                else:
                    status_text = "\nHealth Points: {}/{}\n{}: {}/{}".format(champion5_hp, CHAMPION_5_HP,
                                                                             CHAMPION_5_RPNAME, champion5_rp,
                                                                             CHAMPION_5_RP)
                    return status_text

    def combat_monster_setup(self):
        global new_round, from_attack_button, from_special_button, from_rest_button, combat_results, current_floor_label, teams_current_condition_label, floor_room_modifiers_label, \
            damage_modifier, health_modifier, current_turn, ai1_stun, ai2_stun, ai3_stun, ai4_stun, ai5_stun, ai1_taunt, ai2_taunt, ai3_taunt, ai4_taunt, ai5_taunt, \
            ai1_brittle, ai2_brittle, ai3_brittle, ai4_brittle, ai5_brittle, ai1_weakness, ai2_weakness, ai3_weakness, ai4_weakness, ai5_weakness, \
            ai1_burnDot, ai2_burnDot, ai3_burnDot, ai4_burnDot, ai5_burnDot, ai1_SerraSlashDot, ai2_SerraSlashDot, ai3_SerraSlashDot, \
            ai4_SerraSlashDot, ai5_SerraSlashDot, ai1_garroteDot, ai2_garroteDot, ai3_garroteDot, ai4_garroteDot, ai5_garroteDot, \
            ai1_EviscerDot, ai2_EviscerDot, ai3_EviscerDot, ai4_EviscerDot, ai5_EviscerDot, \
            ai1_statuses, ai2_statuses, ai3_statuses, ai4_statuses, ai5_statuses, \
            ai1_pricked, ai2_pricked, ai3_pricked, ai4_pricked, ai5_pricked
        new_round = 1
        damage_modifier = MODIFERS[1] * floorLevel
        health_modifier = MODIFERS[0] * (roomLevel + (permaHealthMod * 2))
        combat_results = ""
        from_attack_button = 0
        from_special_button = 0
        from_rest_button = 0
        ai1_brittle = 0
        ai2_brittle = 0
        ai3_brittle = 0
        ai4_brittle = 0
        ai5_brittle = 0
        ai1_weakness = 0
        ai2_weakness = 0
        ai3_weakness = 0
        ai4_weakness = 0
        ai5_weakness = 0
        ai1_stun = 0
        ai2_stun = 0
        ai3_stun = 0
        ai4_stun = 0
        ai5_stun = 0
        ai1_pricked = []
        ai2_pricked = []
        ai3_pricked = []
        ai4_pricked = []
        ai5_pricked = []
        ai1_taunt = ["", 0]
        ai2_taunt = ["", 0]
        ai3_taunt = ["", 0]
        ai4_taunt = ["", 0]
        ai5_taunt = ["", 0]
        ai1_burnDot = [0, 0]
        ai2_burnDot = [0, 0]
        ai3_burnDot = [0, 0]
        ai4_burnDot = [0, 0]
        ai5_burnDot = [0, 0]
        ai1_SerraSlashDot = [0, 0]
        ai2_SerraSlashDot = [0, 0]
        ai3_SerraSlashDot = [0, 0]
        ai4_SerraSlashDot = [0, 0]
        ai5_SerraSlashDot = [0, 0]
        ai1_EviscerDot = [0, 0]
        ai2_EviscerDot = [0, 0]
        ai3_EviscerDot = [0, 0]
        ai4_EviscerDot = [0, 0]
        ai5_EviscerDot = [0, 0]
        ai1_garroteDot = [0, 0]
        ai2_garroteDot = [0, 0]
        ai3_garroteDot = [0, 0]
        ai4_garroteDot = [0, 0]
        ai5_garroteDot = [0, 0]
        ai1_statuses = []
        ai2_statuses = []
        ai3_statuses = []
        ai4_statuses = []
        ai5_statuses = []
        current_turn = "C1"
        for widget in dungeon_game_frame.winfo_children():
            widget.destroy()
        teams_current_condition_label.destroy()
        current_floor_label.destroy()
        current_floor_label = tk.Label(dungeon_floor_frame, text="Floor {} : Room {}".format(floorLevel, roomLevel),
                                       font=self.small_text_font)
        current_floor_label.grid(row=1, column=0)
        floor_room_modifiers_label = tk.Label(dungeon_floor_frame,
                                              text="Enemy Damage Modifier: +{}% Enemy Health Modifier: +{}%".format(
                                                  (100 + (100 * damage_modifier)), (100 + (100 * health_modifier))))
        floor_room_modifiers_label.grid(row=2, column=0)
        self.set_monster_encounter()
        self.player_combat_champion1()

    def repeating_combatUI_refresh_function(self):
        self.combat_setup()

    def monster_attack_intentions(self):
        global ai1_attack, ai2_attack, ai3_attack, ai4_attack, ai5_attack
        attack = []
        if ai1_hp == 0:
            ai1_attacking = 0
        else:
            ai1_attacking = 1
        if ai2_hp == 0:
            ai2_attacking = 0
        elif ai2_hp == "out":
            ai2_attacking = 0
        else:
            ai2_attacking = 1
        if ai3_hp == 0:
            ai3_attacking = 0
        elif ai3_hp == "out":
            ai3_attacking = 0
        else:
            ai3_attacking = 1
        if ai4_hp == 0:
            ai4_attacking = 0
        elif ai4_hp == "out":
            ai4_attacking = 0
        else:
            ai4_attacking = 1
        if ai5_hp == 0:
            ai5_attacking = 0
        elif ai5_hp == "out":
            ai5_attacking = 0
        else:
            ai5_attacking = 1
        if ai1_attacking == 1:
            ai1_attack = self.select_ai_attacks()
        else:
            ai1_attack = "null"
        if ai2_attacking == 1:
            ai2_attack = self.select_ai_attacks()
        else:
            ai2_attack = "null"
        if ai3_attacking == 1:
            ai3_attack = self.select_ai_attacks()
        else:
            ai3_attack = "null"
        if ai4_attacking == 1:
            ai4_attack = self.select_ai_attacks()
        else:
            ai4_attack = "null"
        if ai5_attacking == 1:
            ai5_attack = self.select_ai_attacks()
        else:
            ai5_attack = "null"

    def select_ai_attacks(self):
        attack = []
        if AI_NAME == "Grothak the Destroyer":
            # Club_Slam
            club_slam_basenumber = [1, 1.3, 1.5]
            random.shuffle(club_slam_basenumber)
            club_slam_damage = (club_slam_basenumber[0] * AI_ATTACKPOWER * (1 + damage_modifier))
            if club_slam_requirements[1] == 0:
                if club_slam_requirements[0] <= AI_RESOURCE:
                    attack.append("Club Slam")
            random.shuffle(attack)
            if attack[0] == "Club Slam":
                attack = ["Club Slam", math.ceil(club_slam_damage), "1T"]
        if AI_NAME == "Wormpulp Brothers":
            # Violent Thrash
            violent_thrash_basenumber = [1, 1.1, 1.2]
            random.shuffle(violent_thrash_basenumber)
            violent_thrash_damage = (violent_thrash_basenumber[0] * AI_ATTACKPOWER * (1 + damage_modifier))
            if violent_thrash_requirements[1] == 0:
                if violent_thrash_requirements[0] <= AI_RESOURCE:
                    attack.append("Violent Thrash")
            random.shuffle(attack)
            if attack[0] == "Violent Thrash":
                attack = ["Violent Thrash", math.ceil(violent_thrash_damage), "2T"]
        if AI_NAME == "Siren Triplets":
            # Twilight Beam
            twilight_beam_basenumber = [1.2, 1.4, 1.6]
            random.shuffle(twilight_beam_basenumber)
            twilight_beam_damage = (twilight_beam_basenumber[0] * AI_ATTACKPOWER * (1 + damage_modifier))
            if twilight_beam_requirements[1] == 0:
                if twilight_beam_requirements[0] <= AI_RESOURCE:
                    attack.append("Twilight Beam")
            random.shuffle(attack)
            if attack[0] == "Twilight Beam":
                attack = ["Twilight Beam", math.ceil(twilight_beam_damage), "1T"]
        if AI_NAME == "Venomskin Troggies":
            # Spear Thrust
            spear_thrust_basenumber = [1.2, 1.4, 1.6]
            random.shuffle(spear_thrust_basenumber)
            spear_thrust_damage = (spear_thrust_basenumber[0] * AI_ATTACKPOWER * (1 + damage_modifier))
            if spear_stab_requirements[1] == 0:
                if spear_stab_requirements[0] <= AI_RESOURCE:
                    attack.append("Spear Thrust")
            random.shuffle(attack)
            if attack[0] == "Spear Thrust":
                attack = ["Spear Thrust", math.ceil(spear_thrust_damage), "1T"]
        if AI_NAME == "Giant Locust Swarm":
            # Bite
            bite_basenumber = [1.2, 1.4, 1.6]
            random.shuffle(bite_basenumber)
            bite_damage = (bite_basenumber[0] * AI_ATTACKPOWER * (1 + damage_modifier))
            if bite_requirements[1] == 0:
                if bite_requirements[0] <= AI_RESOURCE:
                    attack.append("Bite")
            random.shuffle(attack)
            if attack[0] == "Bite":
                attack = ["Bite", math.ceil(bite_damage), "1T"]
        return attack

    def combat_setup(self):
        global dungeon_game_frame, champion1_combatFrame_stats
        floor_information_dottedLine1 = tk.Label(dungeon_game_frame,
                                                 text="====================================================")
        floor_information_dottedLine2 = tk.Label(dungeon_game_frame,
                                                 text="====================================================")
        floor_information_dottedLine3 = tk.Label(dungeon_game_frame,
                                                 text="====================================================")
        floor_information_dottedLine1.grid(row=0, column=1, sticky="WE")
        floor_information_dottedLine2.grid(row=0, column=2, sticky="WE")
        floor_information_dottedLine3.grid(row=0, column=3, sticky="WE")
        champion1_combatFrame_name = tk.Label(dungeon_game_frame, text=self.champion_combat_name(1))
        champion1_combatFrame_stats = tk.Label(dungeon_game_frame, text=self.champion_combat_status_text(1))
        champion1_combatFrame_statusEffects = tk.Label(dungeon_game_frame, text="Status Effects")
        champion2_combatFrame_name = tk.Label(dungeon_game_frame, text=self.champion_combat_name(2))
        champion2_combatFrame_stats = tk.Label(dungeon_game_frame, text=self.champion_combat_status_text(2))
        champion2_combatFrame_statusEffects = tk.Label(dungeon_game_frame, text="Status Effects")
        champion3_combatFrame_name = tk.Label(dungeon_game_frame, text=self.champion_combat_name(3))
        champion3_combatFrame_stats = tk.Label(dungeon_game_frame, text=self.champion_combat_status_text(3))
        champion3_combatFrame_statusEffects = tk.Label(dungeon_game_frame, text="Status Effects")
        champion4_combatFrame_name = tk.Label(dungeon_game_frame, text=self.champion_combat_name(4))
        champion4_combatFrame_stats = tk.Label(dungeon_game_frame, text=self.champion_combat_status_text(4))
        champion4_combatFrame_statusEffects = tk.Label(dungeon_game_frame, text="Status Effects")
        champion5_combatFrame_name = tk.Label(dungeon_game_frame, text=self.champion_combat_name(5))
        champion5_combatFrame_stats = tk.Label(dungeon_game_frame, text=self.champion_combat_status_text(5))
        champion5_combatFrame_statusEffects = tk.Label(dungeon_game_frame, text="Status Effects")
        champion_CLF_dottedLine_label2 = tk.Label(dungeon_game_frame, text="----------------")
        champion_CLF_dottedLine_label3 = tk.Label(dungeon_game_frame, text="----------------")
        champion_CLF_dottedLine_label4 = tk.Label(dungeon_game_frame, text="----------------")
        champion_CLF_dottedLine_label5 = tk.Label(dungeon_game_frame, text="----------------")
        champion_CLF_dottedLine_label2.grid(row=3, column=1, sticky="w")
        champion_CLF_dottedLine_label3.grid(row=6, column=1, sticky="w")
        champion_CLF_dottedLine_label4.grid(row=9, column=1, sticky="w")
        champion_CLF_dottedLine_label5.grid(row=12, column=1, sticky="w")
        champion1_combatFrame_name.grid(row=1, column=1, sticky="w")
        champion1_combatFrame_stats.grid(row=2, column=1, sticky="w")
        champion1_combatFrame_statusEffects.grid(row=2, column=1)
        champion2_combatFrame_name.grid(row=4, column=1, sticky="w")
        champion2_combatFrame_stats.grid(row=5, column=1, sticky="w")
        champion2_combatFrame_statusEffects.grid(row=5, column=1)
        champion3_combatFrame_name.grid(row=7, column=1, sticky="w")
        champion3_combatFrame_stats.grid(row=8, column=1, sticky="w")
        champion3_combatFrame_statusEffects.grid(row=8, column=1)
        champion4_combatFrame_name.grid(row=10, column=1, sticky="w")
        champion4_combatFrame_stats.grid(row=11, column=1, sticky="w")
        champion4_combatFrame_statusEffects.grid(row=11, column=1)
        champion5_combatFrame_name.grid(row=13, column=1, sticky="w")
        champion5_combatFrame_stats.grid(row=14, column=1, sticky="w")
        champion5_combatFrame_statusEffects.grid(row=14, column=1)
        champion_interaction_dottedLine1 = tk.Label(dungeon_game_frame,
                                                    text="====================================================")
        champion_interaction_dottedLine2 = tk.Label(dungeon_game_frame,
                                                    text="====================================================")
        champion_interaction_dottedLine3 = tk.Label(dungeon_game_frame,
                                                    text="====================================================")
        champion_interaction_dottedLine1.grid(row=16, column=1, sticky="WE")
        champion_interaction_dottedLine2.grid(row=16, column=2, sticky="WE")
        champion_interaction_dottedLine3.grid(row=16, column=3, sticky="WE")
        champion_interaction_currentTurn_label = tk.Label(dungeon_game_frame, text=self.current_champions_turn_text())
        champion_interaction_currentTurn_label.grid(row=17, column=2)
        if AI_SPAWNED == 1:
            ai1_combatFrame_stats = tk.Label(dungeon_game_frame, text=self.ai_combat_status_text(1))
            ai1_combatFrame_name = tk.Label(dungeon_game_frame, text=self.ai_combat_name(1))
            ai1_combatFrame_statusEffects = tk.Label(dungeon_game_frame, text="status effects")
            AI_CLF_dottedLine_label2 = tk.Label(dungeon_game_frame, text="----------------")
            if ai1_hp != 0:
                ai1_intended_attack_label = tk.Label(dungeon_game_frame, text=ai1_attack_intention)
                ai1_intended_attack_label.grid(row=7, column=2, sticky="e")
            ai1_combatFrame_name.grid(row=7, column=3, sticky="e")
            ai1_combatFrame_stats.grid(row=8, column=3, sticky="e")
            ai1_combatFrame_statusEffects.grid(row=8, column=3)
            AI_CLF_dottedLine_label2.grid(row=9, column=3, sticky="e")
        elif AI_SPAWNED == 2:
            ai1_combatFrame_stats = tk.Label(dungeon_game_frame, text=self.ai_combat_status_text(1))
            ai1_combatFrame_name = tk.Label(dungeon_game_frame, text=self.ai_combat_name(1))
            ai1_combatFrame_statusEffects = tk.Label(dungeon_game_frame, text="status effects")
            ai1_combatFrame_name.grid(row=4, column=3, sticky="e")
            ai1_combatFrame_stats.grid(row=5, column=3, sticky="e")
            ai1_combatFrame_statusEffects.grid(row=5, column=3)
            ai2_combatFrame_stats = tk.Label(dungeon_game_frame, text=self.ai_combat_status_text(2))
            ai2_combatFrame_name = tk.Label(dungeon_game_frame, text=self.ai_combat_name(2))
            ai2_combatFrame_statusEffects = tk.Label(dungeon_game_frame, text="status effects")
            ai2_combatFrame_name.grid(row=7, column=3, sticky="e")
            ai2_combatFrame_stats.grid(row=8, column=3, sticky="e")
            ai2_combatFrame_statusEffects.grid(row=8, column=3)
            AI_CLF_dottedLine_label2 = tk.Label(dungeon_game_frame, text="----------------")
            AI_CLF_dottedLine_label3 = tk.Label(dungeon_game_frame, text="----------------")
            if ai1_hp != 0:
                ai1_intended_attack_label = tk.Label(dungeon_game_frame, text=ai1_attack_intention)
                ai1_intended_attack_label.grid(row=4, column=2, sticky="e")
            if ai2_hp != 0:
                ai2_intended_attack_label = tk.Label(dungeon_game_frame, text=ai2_attack_intention)
                ai2_intended_attack_label.grid(row=7, column=2, sticky="e")
            AI_CLF_dottedLine_label2.grid(row=6, column=3, sticky="e")
            AI_CLF_dottedLine_label3.grid(row=9, column=3, sticky="e")
        elif AI_SPAWNED == 3:
            ai1_combatFrame_stats = tk.Label(dungeon_game_frame, text=self.ai_combat_status_text(1))
            ai1_combatFrame_name = tk.Label(dungeon_game_frame, text=self.ai_combat_name(1))
            ai1_combatFrame_statusEffects = tk.Label(dungeon_game_frame, text="status effects")
            ai1_combatFrame_name.grid(row=4, column=3, sticky="e")
            ai1_combatFrame_stats.grid(row=5, column=3, sticky="e")
            ai1_combatFrame_statusEffects.grid(row=5, column=3)
            ai2_combatFrame_stats = tk.Label(dungeon_game_frame, text=self.ai_combat_status_text(2))
            ai2_combatFrame_name = tk.Label(dungeon_game_frame, text=self.ai_combat_name(2))
            ai2_combatFrame_statusEffects = tk.Label(dungeon_game_frame, text="status effects")
            ai2_combatFrame_name.grid(row=7, column=3, sticky="e")
            ai2_combatFrame_stats.grid(row=8, column=3, sticky="e")
            ai2_combatFrame_statusEffects.grid(row=8, column=3)
            ai3_combatFrame_stats = tk.Label(dungeon_game_frame, text=self.ai_combat_status_text(3))
            ai3_combatFrame_name = tk.Label(dungeon_game_frame, text=self.ai_combat_name(3))
            ai3_combatFrame_statusEffects = tk.Label(dungeon_game_frame, text="status effects")
            ai3_combatFrame_name.grid(row=10, column=3, sticky="e")
            ai3_combatFrame_stats.grid(row=11, column=3, sticky="e")
            ai3_combatFrame_statusEffects.grid(row=11, column=3)
            AI_CLF_dottedLine_label2 = tk.Label(dungeon_game_frame, text="----------------")
            AI_CLF_dottedLine_label3 = tk.Label(dungeon_game_frame, text="----------------")
            if ai1_hp != 0:
                ai1_intended_attack_label = tk.Label(dungeon_game_frame, text=ai1_attack_intention)
                ai1_intended_attack_label.grid(row=4, column=2, sticky="e")
            if ai2_hp != 0:
                ai2_intended_attack_label = tk.Label(dungeon_game_frame, text=ai2_attack_intention)
                ai2_intended_attack_label.grid(row=7, column=2, sticky="e")
            if ai3_hp != 0:
                ai3_intended_attack_label = tk.Label(dungeon_game_frame, text=ai3_attack_intention)
                ai3_intended_attack_label.grid(row=10, column=2, sticky="e")
            AI_CLF_dottedLine_label2.grid(row=6, column=3, sticky="e")
            AI_CLF_dottedLine_label3.grid(row=9, column=3, sticky="e")
        elif AI_SPAWNED == 4:
            ai1_combatFrame_stats = tk.Label(dungeon_game_frame, text=self.ai_combat_status_text(1))
            ai1_combatFrame_name = tk.Label(dungeon_game_frame, text=self.ai_combat_name(1))
            ai1_combatFrame_statusEffects = tk.Label(dungeon_game_frame, text="status effects")
            ai1_combatFrame_name.grid(row=1, column=3, sticky="e")
            ai1_combatFrame_stats.grid(row=2, column=3, sticky="e")
            ai1_combatFrame_statusEffects.grid(row=2, column=3)
            ai2_combatFrame_stats = tk.Label(dungeon_game_frame, text=self.ai_combat_status_text(2))
            ai2_combatFrame_name = tk.Label(dungeon_game_frame, text=self.ai_combat_name(2))
            ai2_combatFrame_statusEffects = tk.Label(dungeon_game_frame, text="status effects")
            ai2_combatFrame_name.grid(row=4, column=3, sticky="e")
            ai2_combatFrame_stats.grid(row=5, column=3, sticky="e")
            ai2_combatFrame_statusEffects.grid(row=5, column=3)
            ai3_combatFrame_stats = tk.Label(dungeon_game_frame, text=self.ai_combat_status_text(3))
            ai3_combatFrame_name = tk.Label(dungeon_game_frame, text=self.ai_combat_name(3))
            ai3_combatFrame_statusEffects = tk.Label(dungeon_game_frame, text="status effects")
            ai3_combatFrame_name.grid(row=7, column=3, sticky="e")
            ai3_combatFrame_stats.grid(row=8, column=3, sticky="e")
            ai3_combatFrame_statusEffects.grid(row=8, column=3)
            ai4_combatFrame_stats = tk.Label(dungeon_game_frame, text=self.ai_combat_status_text(4))
            ai4_combatFrame_name = tk.Label(dungeon_game_frame, text=self.ai_combat_name(4))
            ai4_combatFrame_statusEffects = tk.Label(dungeon_game_frame, text="status effects")
            ai4_combatFrame_name.grid(row=10, column=3, sticky="e")
            ai4_combatFrame_stats.grid(row=11, column=3, sticky="e")
            ai4_combatFrame_statusEffects.grid(row=11, column=3)
            AI_CLF_dottedLine_label2 = tk.Label(dungeon_game_frame, text="----------------")
            AI_CLF_dottedLine_label3 = tk.Label(dungeon_game_frame, text="----------------")
            AI_CLF_dottedLine_label4 = tk.Label(dungeon_game_frame, text="----------------")
            if ai1_hp != 0:
                ai1_intended_attack_label = tk.Label(dungeon_game_frame, text=ai1_attack_intention)
                ai1_intended_attack_label.grid(row=1, column=2, sticky="e")
            if ai2_hp != 0:
                ai2_intended_attack_label = tk.Label(dungeon_game_frame, text=ai2_attack_intention)
                ai2_intended_attack_label.grid(row=4, column=2, sticky="e")
            if ai3_hp != 0:
                ai3_intended_attack_label = tk.Label(dungeon_game_frame, text=ai3_attack_intention)
                ai3_intended_attack_label.grid(row=7, column=2, sticky="e")
            if ai4_hp != 0:
                ai4_intended_attack_label = tk.Label(dungeon_game_frame, text=ai4_attack_intention)
                ai4_intended_attack_label.grid(row=10, column=2, sticky="e")
            AI_CLF_dottedLine_label2.grid(row=3, column=3, sticky="e")
            AI_CLF_dottedLine_label3.grid(row=6, column=3, sticky="e")
            AI_CLF_dottedLine_label4.grid(row=9, column=3, sticky="e")
        elif AI_SPAWNED == 5:
            ai1_combatFrame_stats = tk.Label(dungeon_game_frame, text=self.ai_combat_status_text(1))
            ai1_combatFrame_name = tk.Label(dungeon_game_frame, text=self.ai_combat_name(1))
            ai1_combatFrame_statusEffects = tk.Label(dungeon_game_frame, text="status effects")
            ai1_combatFrame_name.grid(row=1, column=3, sticky="e")
            ai1_combatFrame_stats.grid(row=2, column=3, sticky="e")
            ai1_combatFrame_statusEffects.grid(row=2, column=3)
            ai2_combatFrame_stats = tk.Label(dungeon_game_frame, text=self.ai_combat_status_text(2))
            ai2_combatFrame_name = tk.Label(dungeon_game_frame, text=self.ai_combat_name(2))
            ai2_combatFrame_statusEffects = tk.Label(dungeon_game_frame, text="status effects")
            ai2_combatFrame_name.grid(row=4, column=3, sticky="e")
            ai2_combatFrame_stats.grid(row=5, column=3, sticky="e")
            ai2_combatFrame_statusEffects.grid(row=5, column=3)
            ai3_combatFrame_stats = tk.Label(dungeon_game_frame, text=self.ai_combat_status_text(3))
            ai3_combatFrame_name = tk.Label(dungeon_game_frame, text=self.ai_combat_name(3))
            ai3_combatFrame_statusEffects = tk.Label(dungeon_game_frame, text="status effects")
            ai3_combatFrame_name.grid(row=7, column=3, sticky="e")
            ai3_combatFrame_stats.grid(row=8, column=3, sticky="e")
            ai3_combatFrame_statusEffects.grid(row=8, column=3)
            ai4_combatFrame_stats = tk.Label(dungeon_game_frame, text=self.ai_combat_status_text(4))
            ai4_combatFrame_name = tk.Label(dungeon_game_frame, text=self.ai_combat_name(4))
            ai4_combatFrame_statusEffects = tk.Label(dungeon_game_frame, text="status effects")
            ai4_combatFrame_name.grid(row=10, column=3, sticky="e")
            ai4_combatFrame_stats.grid(row=11, column=3, sticky="e")
            ai4_combatFrame_statusEffects.grid(row=11, column=3)
            ai5_combatFrame_stats = tk.Label(dungeon_game_frame, text=self.ai_combat_status_text(5))
            ai5_combatFrame_name = tk.Label(dungeon_game_frame, text=self.ai_combat_name(5))
            ai5_combatFrame_statusEffects = tk.Label(dungeon_game_frame, text="status effects")
            ai5_combatFrame_name.grid(row=13, column=3, sticky="e")
            ai5_combatFrame_stats.grid(row=14, column=3, sticky="e")
            ai5_combatFrame_statusEffects.grid(row=14, column=3)
            AI_CLF_dottedLine_label2 = tk.Label(dungeon_game_frame, text="----------------")
            AI_CLF_dottedLine_label3 = tk.Label(dungeon_game_frame, text="----------------")
            AI_CLF_dottedLine_label4 = tk.Label(dungeon_game_frame, text="----------------")
            AI_CLF_dottedLine_label5 = tk.Label(dungeon_game_frame, text="----------------")
            if ai1_hp != 0:
                ai1_intended_attack_label = tk.Label(dungeon_game_frame, text=ai1_attack_intention)
                ai1_intended_attack_label.grid(row=1, column=2, sticky="e")
            if ai2_hp != 0:
                ai2_intended_attack_label = tk.Label(dungeon_game_frame, text=ai2_attack_intention)
                ai2_intended_attack_label.grid(row=4, column=2, sticky="e")
            if ai3_hp != 0:
                ai3_intended_attack_label = tk.Label(dungeon_game_frame, text=ai3_attack_intention)
                ai3_intended_attack_label.grid(row=7, column=2, sticky="e")
            if ai4_hp != 0:
                ai4_intended_attack_label = tk.Label(dungeon_game_frame, text=ai4_attack_intention)
                ai4_intended_attack_label.grid(row=10, column=2, sticky="e")
            if ai5_hp != 0:
                ai5_intended_attack_label = tk.Label(dungeon_game_frame, text=ai5_attack_intention)
                ai5_intended_attack_label.grid(row=13, column=2, sticky="e")
            AI_CLF_dottedLine_label2.grid(row=3, column=3, sticky="e")
            AI_CLF_dottedLine_label3.grid(row=6, column=3, sticky="e")
            AI_CLF_dottedLine_label4.grid(row=9, column=3, sticky="e")
            AI_CLF_dottedLine_label5.grid(row=12, column=3, sticky="e")

    def current_champions_turn_text(self):
        if current_turn == "C1":
            text = "<{}'s Turn>".format(CHAMPION_LIST[0])
            return text
        elif current_turn == "C2":
            text = "<{}'s Turn>".format(CHAMPION_LIST[1])
            return text
        elif current_turn == "C3":
            text = "<{}'s Turn>".format(CHAMPION_LIST[2])
            return text
        elif current_turn == "C4":
            text = "<{}'s Turn>".format(CHAMPION_LIST[3])
            return text
        elif current_turn == "C5":
            text = "<{}'s Turn>".format(CHAMPION_LIST[4])
            return text

    def ai_choose_attack_targets(self, ):
        global ai1_attack_intention, ai2_attack_intention, ai3_attack_intention, ai4_attack_intention, ai5_attack_intention
        ai_attack_options = []
        counter = 0
        if ai1_hp >= 0:
            if ai1_attack == "null":
                ai1_attack_intention = ""
            elif ai1_stun != 0:
                ai1_attack_intention = "STUNNED"
            elif len(ai1_taunt) != 0:
                for champions in CHAMPION_LIST:
                    counter += 1
                    if champions == ai1_taunt[0]:
                        if counter == 1:
                            ai_attack_target = CHAMPION_LIST[0]
                            ai1_attack_intention = "{} <<< {} ({} Damage)".format(ai_attack_target, ai1_attack[0],
                                                                                  ai1_attack[1])
                        elif counter == 2:
                            ai_attack_target = CHAMPION_LIST[1]
                            ai1_attack_intention = "{} <<< {} ({} Damage)".format(ai_attack_target, ai1_attack[0],
                                                                                  ai1_attack[1])
                        elif counter == 3:
                            ai_attack_target = CHAMPION_LIST[2]
                            ai1_attack_intention = "{} <<< {} ({} Damage)".format(ai_attack_target, ai1_attack[0],
                                                                                  ai1_attack[1])
                        elif counter == 4:
                            ai_attack_target = CHAMPION_LIST[3]
                            ai1_attack_intention = "{} <<< {} ({} Damage)".format(ai_attack_target, ai1_attack[0],
                                                                                  ai1_attack[1])
                        elif counter == 5:
                            ai_attack_target = CHAMPION_LIST[4]
                            ai1_attack_intention = "{} <<< {} ({} Damage)".format(ai_attack_target, ai1_attack[0],
                                                                                  ai1_attack[1])
            if new_round == 1:
                if ai1_attack[2] == "1T":
                    if champion1_hp != 0:
                        ai_attack_options.append("C1")
                    if champion2_hp != 0:
                        ai_attack_options.append("C2")
                    if champion3_hp != 0:
                        ai_attack_options.append("C3")
                    if champion4_hp != 0:
                        ai_attack_options.append("C4")
                    if champion5_hp != 0:
                        ai_attack_options.append("C5")
                    random.shuffle(ai_attack_options)
                    if ai_attack_options[0] == "C1":
                        ai_attack_target = CHAMPION_LIST[0]
                    if ai_attack_options[0] == "C2":
                        ai_attack_target = CHAMPION_LIST[1]
                    if ai_attack_options[0] == "C3":
                        ai_attack_target = CHAMPION_LIST[2]
                    if ai_attack_options[0] == "C4":
                        ai_attack_target = CHAMPION_LIST[3]
                    if ai_attack_options[0] == "C5":
                        ai_attack_target = CHAMPION_LIST[4]
                    ai1_attack_intention = "{} <<< {} ({} Damage)".format(ai_attack_target, ai1_attack[0],
                                                                          ai1_attack[1])
                elif ai1_attack[2] == "2T":
                    if champion1_hp != 0:
                        ai_attack_options.append("C1")
                    if champion2_hp != 0:
                        ai_attack_options.append("C2")
                    if champion3_hp != 0:
                        ai_attack_options.append("C3")
                    if champion4_hp != 0:
                        ai_attack_options.append("C4")
                    if champion5_hp != 0:
                        ai_attack_options.append("C5")
                    random.shuffle(ai_attack_options)
                    if ai_attack_options[0] == "C1":
                        ai_attack1_target = CHAMPION_LIST[0]
                        ai_attack_options.remove("C1")
                    if ai_attack_options[0] == "C2":
                        ai_attack1_target = CHAMPION_LIST[1]
                        ai_attack_options.remove("C2")
                    if ai_attack_options[0] == "C3":
                        ai_attack1_target = CHAMPION_LIST[2]
                        ai_attack_options.remove("C3")
                    if ai_attack_options[0] == "C4":
                        ai_attack1_target = CHAMPION_LIST[3]
                        ai_attack_options.remove("C4")
                    if ai_attack_options[0] == "C5":
                        ai_attack1_target = CHAMPION_LIST[4]
                        ai_attack_options.remove("C5")
                    random.shuffle(ai_attack_options)
                    if ai_attack_options[0] == "C1":
                        ai_attack2_target = CHAMPION_LIST[0]
                    if ai_attack_options[0] == "C2":
                        ai_attack2_target = CHAMPION_LIST[1]
                    if ai_attack_options[0] == "C3":
                        ai_attack2_target = CHAMPION_LIST[2]
                    if ai_attack_options[0] == "C4":
                        ai_attack2_target = CHAMPION_LIST[3]
                    if ai_attack_options[0] == "C5":
                        ai_attack2_target = CHAMPION_LIST[4]
                    ai1_attack_intention = "{} and {} <<< {} ({} Damage)".format(ai_attack1_target, ai_attack2_target,
                                                                                 ai1_attack[0], ai1_attack[1])
                if ai1_attack[2] == "AOE":
                    ai1_attack_intention = "Everyone <<< {} ({} Damage)".format(ai1_attack[0], ai1_attack[1])
        if ai2_hp >= 0:
            if ai2_attack == "null":
                ai2_attack_intention = ""
            elif ai2_stun != 0:
                ai2_attack_intention = "STUNNED"
            elif len(ai2_taunt) != 0:
                for champions in CHAMPION_LIST:
                    counter += 1
                    if champions == ai2_taunt[0]:
                        if counter == 1:
                            ai_attack_target = CHAMPION_LIST[0]
                            ai2_attack_intention = "{} <<< {} ({} Damage)".format(ai_attack_target, ai2_attack[0],
                                                                                  ai2_attack[1])
                        elif counter == 2:
                            ai_attack_target = CHAMPION_LIST[1]
                            ai2_attack_intention = "{} <<< {} ({} Damage)".format(ai_attack_target, ai2_attack[0],
                                                                                  ai2_attack[1])
                        elif counter == 3:
                            ai_attack_target = CHAMPION_LIST[2]
                            ai2_attack_intention = "{} <<< {} ({} Damage)".format(ai_attack_target, ai2_attack[0],
                                                                                  ai2_attack[1])
                        elif counter == 4:
                            ai_attack_target = CHAMPION_LIST[3]
                            ai2_attack_intention = "{} <<< {} ({} Damage)".format(ai_attack_target, ai2_attack[0],
                                                                                  ai2_attack[1])
                        elif counter == 5:
                            ai_attack_target = CHAMPION_LIST[4]
                            ai2_attack_intention = "{} <<< {} ({} Damage)".format(ai_attack_target, ai2_attack[0],
                                                                                  ai2_attack[1])
            if new_round == 1:
                if ai2_attack[2] == "1T":
                    if champion1_hp != 0:
                        ai_attack_options.append("C1")
                    if champion2_hp != 0:
                        ai_attack_options.append("C2")
                    if champion3_hp != 0:
                        ai_attack_options.append("C3")
                    if champion4_hp != 0:
                        ai_attack_options.append("C4")
                    if champion5_hp != 0:
                        ai_attack_options.append("C5")
                    random.shuffle(ai_attack_options)
                    if ai_attack_options[0] == "C1":
                        ai_attack_target = CHAMPION_LIST[0]
                    if ai_attack_options[0] == "C2":
                        ai_attack_target = CHAMPION_LIST[1]
                    if ai_attack_options[0] == "C3":
                        ai_attack_target = CHAMPION_LIST[2]
                    if ai_attack_options[0] == "C4":
                        ai_attack_target = CHAMPION_LIST[3]
                    if ai_attack_options[0] == "C5":
                        ai_attack_target = CHAMPION_LIST[4]
                    ai2_attack_intention = "{} <<< {} ({} Damage)".format(ai_attack_target, ai2_attack[0],
                                                                          ai2_attack[1])
                if ai2_attack[2] == "2T":
                    if champion1_hp != 0:
                        ai_attack_options.append("C1")
                    if champion2_hp != 0:
                        ai_attack_options.append("C2")
                    if champion3_hp != 0:
                        ai_attack_options.append("C3")
                    if champion4_hp != 0:
                        ai_attack_options.append("C4")
                    if champion5_hp != 0:
                        ai_attack_options.append("C5")
                    random.shuffle(ai_attack_options)
                    if ai_attack_options[0] == "C1":
                        ai_attack1_target = CHAMPION_LIST[0]
                        ai_attack_options.remove("C1")
                    if ai_attack_options[0] == "C2":
                        ai_attack1_target = CHAMPION_LIST[1]
                        ai_attack_options.remove("C2")
                    if ai_attack_options[0] == "C3":
                        ai_attack1_target = CHAMPION_LIST[2]
                        ai_attack_options.remove("C3")
                    if ai_attack_options[0] == "C4":
                        ai_attack1_target = CHAMPION_LIST[3]
                        ai_attack_options.remove("C4")
                    if ai_attack_options[0] == "C5":
                        ai_attack1_target = CHAMPION_LIST[4]
                        ai_attack_options.remove("C5")
                    random.shuffle(ai_attack_options)
                    if ai_attack_options[0] == "C1":
                        ai_attack2_target = CHAMPION_LIST[0]
                    if ai_attack_options[0] == "C2":
                        ai_attack2_target = CHAMPION_LIST[1]
                    if ai_attack_options[0] == "C3":
                        ai_attack2_target = CHAMPION_LIST[2]
                    if ai_attack_options[0] == "C4":
                        ai_attack2_target = CHAMPION_LIST[3]
                    if ai_attack_options[0] == "C5":
                        ai_attack2_target = CHAMPION_LIST[4]
                    ai2_attack_intention = "{} and {} <<< {} ({} Damage)".format(ai_attack1_target, ai_attack2_target,
                                                                                 ai2_attack[0],
                                                                                 ai2_attack[1])
                if ai2_attack[2] == "AOE":
                    ai2_attack_intention = "Everyone <<< {} ({} Damage)".format(ai2_attack[0], ai2_attack[1])
        if ai3_hp >= 0:
            if ai3_attack == "null":
                ai3_attack_intention = ""
            elif ai3_stun != 0:
                ai3_attack_intention = "STUNNED"
            elif len(ai3_taunt) != 0:
                for champions in CHAMPION_LIST:
                    counter += 1
                    if champions == ai3_taunt[0]:
                        if counter == 1:
                            ai_attack_target = CHAMPION_LIST[0]
                            ai3_attack_intention = "{} <<< {} ({} Damage)".format(ai_attack_target, ai3_attack[0],
                                                                                  ai3_attack[1])
                        elif counter == 2:
                            ai_attack_target = CHAMPION_LIST[1]
                            ai3_attack_intention = "{} <<< {} ({} Damage)".format(ai_attack_target, ai3_attack[0],
                                                                                  ai3_attack[1])
                        elif counter == 3:
                            ai_attack_target = CHAMPION_LIST[2]
                            ai3_attack_intention = "{} <<< {} ({} Damage)".format(ai_attack_target, ai3_attack[0],
                                                                                  ai3_attack[1])
                        elif counter == 4:
                            ai_attack_target = CHAMPION_LIST[3]
                            ai3_attack_intention = "{} <<< {} ({} Damage)".format(ai_attack_target, ai3_attack[0],
                                                                                  ai3_attack[1])
                        elif counter == 5:
                            ai_attack_target = CHAMPION_LIST[4]
                            ai3_attack_intention = "{} <<< {} ({} Damage)".format(ai_attack_target, ai3_attack[0],
                                                                                  ai3_attack[1])
            if new_round == 1:
                if ai3_attack[2] == "1T":
                    if champion1_hp != 0:
                        ai_attack_options.append("C1")
                    if champion2_hp != 0:
                        ai_attack_options.append("C2")
                    if champion3_hp != 0:
                        ai_attack_options.append("C3")
                    if champion4_hp != 0:
                        ai_attack_options.append("C4")
                    if champion5_hp != 0:
                        ai_attack_options.append("C5")
                    random.shuffle(ai_attack_options)
                    if ai_attack_options[0] == "C1":
                        ai_attack_target = CHAMPION_LIST[0]
                    if ai_attack_options[0] == "C2":
                        ai_attack_target = CHAMPION_LIST[1]
                    if ai_attack_options[0] == "C3":
                        ai_attack_target = CHAMPION_LIST[2]
                    if ai_attack_options[0] == "C4":
                        ai_attack_target = CHAMPION_LIST[3]
                    if ai_attack_options[0] == "C5":
                        ai_attack_target = CHAMPION_LIST[4]
                    ai3_attack_intention = "{} <<< {} ({} Damage)".format(ai_attack_target, ai3_attack[0],
                                                                          ai3_attack[1])
                if ai3_attack[2] == "2T":
                    if champion1_hp != 0:
                        ai_attack_options.append("C1")
                    if champion2_hp != 0:
                        ai_attack_options.append("C2")
                    if champion3_hp != 0:
                        ai_attack_options.append("C3")
                    if champion4_hp != 0:
                        ai_attack_options.append("C4")
                    if champion5_hp != 0:
                        ai_attack_options.append("C5")
                    random.shuffle(ai_attack_options)
                    if ai_attack_options[0] == "C1":
                        ai_attack1_target = CHAMPION_LIST[0]
                        ai_attack_options.remove("C1")
                    if ai_attack_options[0] == "C2":
                        ai_attack1_target = CHAMPION_LIST[1]
                        ai_attack_options.remove("C2")
                    if ai_attack_options[0] == "C3":
                        ai_attack1_target = CHAMPION_LIST[2]
                        ai_attack_options.remove("C3")
                    if ai_attack_options[0] == "C4":
                        ai_attack1_target = CHAMPION_LIST[3]
                        ai_attack_options.remove("C4")
                    if ai_attack_options[0] == "C5":
                        ai_attack1_target = CHAMPION_LIST[4]
                        ai_attack_options.remove("C5")
                    random.shuffle(ai_attack_options)
                    if ai_attack_options[0] == "C1":
                        ai_attack2_target = CHAMPION_LIST[0]
                    if ai_attack_options[0] == "C2":
                        ai_attack2_target = CHAMPION_LIST[1]
                    if ai_attack_options[0] == "C3":
                        ai_attack2_target = CHAMPION_LIST[2]
                    if ai_attack_options[0] == "C4":
                        ai_attack2_target = CHAMPION_LIST[3]
                    if ai_attack_options[0] == "C5":
                        ai_attack2_target = CHAMPION_LIST[4]
                    ai3_attack_intention = "{} and {} <<< {} ({} Damage)".format(ai_attack1_target, ai_attack2_target,
                                                                                 ai3_attack[0],
                                                                                 ai3_attack[1])
                if ai3_attack[2] == "AOE":
                    ai3_attack_intention = "Everyone <<< {} ({} Damage)".format(ai3_attack[0], ai3_attack[1])
        if ai4_hp >= 0:
            if ai4_attack == "null":
                ai4_attack_intention = ""
            elif ai4_stun != 0:
                ai4_attack_intention = "STUNNED"
            elif len(ai4_taunt) != 0:
                for champions in CHAMPION_LIST:
                    counter += 1
                    if champions == ai4_taunt[0]:
                        if counter == 1:
                            ai_attack_target = CHAMPION_LIST[0]
                            ai4_attack_intention = "{} <<< {} ({} Damage)".format(ai_attack_target, ai4_attack[0],
                                                                                  ai4_attack[1])
                        elif counter == 2:
                            ai_attack_target = CHAMPION_LIST[1]
                            ai4_attack_intention = "{} <<< {} ({} Damage)".format(ai_attack_target, ai4_attack[0],
                                                                                  ai4_attack[1])
                        elif counter == 3:
                            ai_attack_target = CHAMPION_LIST[2]
                            ai4_attack_intention = "{} <<< {} ({} Damage)".format(ai_attack_target, ai4_attack[0],
                                                                                  ai4_attack[1])
                        elif counter == 4:
                            ai_attack_target = CHAMPION_LIST[3]
                            ai4_attack_intention = "{} <<< {} ({} Damage)".format(ai_attack_target, ai4_attack[0],
                                                                                  ai4_attack[1])
                        elif counter == 5:
                            ai_attack_target = CHAMPION_LIST[4]
                            ai4_attack_intention = "{} <<< {} ({} Damage)".format(ai_attack_target, ai4_attack[0],
                                                                                  ai4_attack[1])
            if new_round == 1:
                if ai4_attack[2] == "1T":
                    if champion1_hp != 0:
                        ai_attack_options.append("C1")
                    if champion2_hp != 0:
                        ai_attack_options.append("C2")
                    if champion3_hp != 0:
                        ai_attack_options.append("C3")
                    if champion4_hp != 0:
                        ai_attack_options.append("C4")
                    if champion5_hp != 0:
                        ai_attack_options.append("C5")
                    random.shuffle(ai_attack_options)
                    if ai_attack_options[0] == "C1":
                        ai_attack_target = CHAMPION_LIST[0]
                    if ai_attack_options[0] == "C2":
                        ai_attack_target = CHAMPION_LIST[1]
                    if ai_attack_options[0] == "C3":
                        ai_attack_target = CHAMPION_LIST[2]
                    if ai_attack_options[0] == "C4":
                        ai_attack_target = CHAMPION_LIST[3]
                    if ai_attack_options[0] == "C5":
                        ai_attack_target = CHAMPION_LIST[4]
                    ai4_attack_intention = "{} <<< {} ({} Damage)".format(ai_attack_target, ai4_attack[0],
                                                                          ai4_attack[1])
                if ai4_attack[2] == "2T":
                    if champion1_hp != 0:
                        ai_attack_options.append("C1")
                    if champion2_hp != 0:
                        ai_attack_options.append("C2")
                    if champion3_hp != 0:
                        ai_attack_options.append("C3")
                    if champion4_hp != 0:
                        ai_attack_options.append("C4")
                    if champion5_hp != 0:
                        ai_attack_options.append("C5")
                    random.shuffle(ai_attack_options)
                    if ai_attack_options[0] == "C1":
                        ai_attack1_target = CHAMPION_LIST[0]
                        ai_attack_options.remove("C1")
                    if ai_attack_options[0] == "C2":
                        ai_attack1_target = CHAMPION_LIST[1]
                        ai_attack_options.remove("C2")
                    if ai_attack_options[0] == "C3":
                        ai_attack1_target = CHAMPION_LIST[2]
                        ai_attack_options.remove("C3")
                    if ai_attack_options[0] == "C4":
                        ai_attack1_target = CHAMPION_LIST[3]
                        ai_attack_options.remove("C4")
                    if ai_attack_options[0] == "C5":
                        ai_attack1_target = CHAMPION_LIST[4]
                        ai_attack_options.remove("C5")
                    random.shuffle(ai_attack_options)
                    if ai_attack_options[0] == "C1":
                        ai_attack2_target = CHAMPION_LIST[0]
                    if ai_attack_options[0] == "C2":
                        ai_attack2_target = CHAMPION_LIST[1]
                    if ai_attack_options[0] == "C3":
                        ai_attack2_target = CHAMPION_LIST[2]
                    if ai_attack_options[0] == "C4":
                        ai_attack2_target = CHAMPION_LIST[3]
                    if ai_attack_options[0] == "C5":
                        ai_attack2_target = CHAMPION_LIST[4]
                    ai4_attack_intention = "{} and {} <<< {} ({} Damage)".format(ai_attack1_target, ai_attack2_target,
                                                                                 ai4_attack[0],
                                                                                 ai4_attack[1])
                if ai4_attack[2] == "AOE":
                    ai4_attack_intention = "Everyone <<< {} ({} Damage)".format(ai4_attack[0], ai4_attack[1])
        if ai5_hp >= 0:
            if ai5_attack == "null":
                ai5_attack_intention = ""
            elif ai5_stun != 0:
                ai5_attack_intention = "STUNNED"
            elif len(ai5_taunt) != 0:
                for champions in CHAMPION_LIST:
                    counter += 1
                    if champions == ai5_taunt[0]:
                        if counter == 1:
                            ai_attack_target = CHAMPION_LIST[0]
                            ai5_attack_intention = "{} <<< {} ({} Damage)".format(ai_attack_target, ai5_attack[0],
                                                                                  ai5_attack[1])
                        elif counter == 2:
                            ai_attack_target = CHAMPION_LIST[1]
                            ai5_attack_intention = "{} <<< {} ({} Damage)".format(ai_attack_target, ai5_attack[0],
                                                                                  ai5_attack[1])
                        elif counter == 3:
                            ai_attack_target = CHAMPION_LIST[2]
                            ai5_attack_intention = "{} <<< {} ({} Damage)".format(ai_attack_target, ai5_attack[0],
                                                                                  ai5_attack[1])
                        elif counter == 4:
                            ai_attack_target = CHAMPION_LIST[3]
                            ai5_attack_intention = "{} <<< {} ({} Damage)".format(ai_attack_target, ai5_attack[0],
                                                                                  ai5_attack[1])
                        elif counter == 5:
                            ai_attack_target = CHAMPION_LIST[4]
                            ai5_attack_intention = "{} <<< {} ({} Damage)".format(ai_attack_target, ai5_attack[0],
                                                                                  ai5_attack[1])
            if new_round == 1:
                if ai5_attack[2] == "1T":
                    if champion1_hp != 0:
                        ai_attack_options.append("C1")
                    if champion2_hp != 0:
                        ai_attack_options.append("C2")
                    if champion3_hp != 0:
                        ai_attack_options.append("C3")
                    if champion4_hp != 0:
                        ai_attack_options.append("C4")
                    if champion5_hp != 0:
                        ai_attack_options.append("C5")
                    random.shuffle(ai_attack_options)
                    if ai_attack_options[0] == "C1":
                        ai_attack_target = CHAMPION_LIST[0]
                    if ai_attack_options[0] == "C2":
                        ai_attack_target = CHAMPION_LIST[1]
                    if ai_attack_options[0] == "C3":
                        ai_attack_target = CHAMPION_LIST[2]
                    if ai_attack_options[0] == "C4":
                        ai_attack_target = CHAMPION_LIST[3]
                    if ai_attack_options[0] == "C5":
                        ai_attack_target = CHAMPION_LIST[4]
                    ai5_attack_intention = "{} <<< {} ({} Damage)".format(ai_attack_target, ai5_attack[0],
                                                                          ai5_attack[1])
                if ai5_attack[2] == "2T":
                    if champion1_hp != 0:
                        ai_attack_options.append("C1")
                    if champion2_hp != 0:
                        ai_attack_options.append("C2")
                    if champion3_hp != 0:
                        ai_attack_options.append("C3")
                    if champion4_hp != 0:
                        ai_attack_options.append("C4")
                    if champion5_hp != 0:
                        ai_attack_options.append("C5")
                    random.shuffle(ai_attack_options)
                    if ai_attack_options[0] == "C1":
                        ai_attack1_target = CHAMPION_LIST[0]
                        ai_attack_options.remove("C1")
                    if ai_attack_options[0] == "C2":
                        ai_attack1_target = CHAMPION_LIST[1]
                        ai_attack_options.remove("C2")
                    if ai_attack_options[0] == "C3":
                        ai_attack1_target = CHAMPION_LIST[2]
                        ai_attack_options.remove("C3")
                    if ai_attack_options[0] == "C4":
                        ai_attack1_target = CHAMPION_LIST[3]
                        ai_attack_options.remove("C4")
                    if ai_attack_options[0] == "C5":
                        ai_attack1_target = CHAMPION_LIST[4]
                        ai_attack_options.remove("C5")
                    random.shuffle(ai_attack_options)
                    if ai_attack_options[0] == "C1":
                        ai_attack2_target = CHAMPION_LIST[0]
                    if ai_attack_options[0] == "C2":
                        ai_attack2_target = CHAMPION_LIST[1]
                    if ai_attack_options[0] == "C3":
                        ai_attack2_target = CHAMPION_LIST[2]
                    if ai_attack_options[0] == "C4":
                        ai_attack2_target = CHAMPION_LIST[3]
                    if ai_attack_options[0] == "C5":
                        ai_attack2_target = CHAMPION_LIST[4]
                    ai5_attack_intention = "{} and {} <<< {} ({} Damage)".format(ai_attack1_target, ai_attack2_target,
                                                                                 ai5_attack[0],
                                                                                 ai5_attack[1])
                if ai5_attack[2] == "AOE":
                    ai5_attack_intention = "Everyone <<< {} ({} Damage)".format(ai5_attack[0], ai5_attack[1])

    def champion_combat_name(self, champion_position):
        global champion1_hp, champion2_hp, champion3_hp, champion4_hp, champion5_hp
        name_text = ""
        if champion_position == 1:
            if champion1_hp < 0:
                champion1_hp = 0
            if champion1_hp == 0:
                name_text = "{} *DEAD*".format(CHAMPION_LIST[0])
                return name_text
            else:
                name_text = "{}".format(CHAMPION_LIST[0])
                return name_text
        if champion_position == 2:
            if champion2_hp < 0:
                champion2_hp = 0
            if champion2_hp == 0:
                name_text = "{} *DEAD*".format(CHAMPION_LIST[1])
                return name_text
            else:
                name_text = "{}".format(CHAMPION_LIST[1])
                return name_text
        if champion_position == 3:
            if champion3_hp < 0:
                champion3_hp = 0
            if champion3_hp == 0:
                name_text = "{} *DEAD*".format(CHAMPION_LIST[2])
                return name_text
            else:
                name_text = "{}".format(CHAMPION_LIST[2])
                return name_text
        if champion_position == 4:
            if champion4_hp < 0:
                champion4_hp = 0
            if champion4_hp == 0:
                name_text = "{} *DEAD*".format(CHAMPION_LIST[3])
                return name_text
            else:
                name_text = "{}".format(CHAMPION_LIST[3])
                return name_text
        if champion_position == 5:
            if champion5_hp < 0:
                champion5_hp = 0
            if champion5_hp == 0:
                name_text = "{} *DEAD*".format(CHAMPION_LIST[4])
                return name_text
            else:
                name_text = "{}".format(CHAMPION_LIST[4])
                return name_text

    def champion_combat_status_text(self, champion_position):
        global champion1_rp, champion2_rp, champion3_rp, champion4_rp, champion5_rp
        if champion_position == 1:
            if CHAMPION_1_RPNAME == "null":
                status_text = "Health Points: {}/{}".format(champion1_hp, CHAMPION_1_HP)
                return status_text
            else:
                if champion1_rp > CHAMPION_1_RP:
                    champion1_rp = CHAMPION_1_RP
                status_text = "Health Points: {}/{}\n{}: {}/{}".format(champion1_hp, CHAMPION_1_HP, CHAMPION_1_RPNAME,
                                                                       champion1_rp, CHAMPION_1_RP)
                return status_text
        if champion_position == 2:
            if CHAMPION_2_RPNAME == "null":
                status_text = "Health Points: {}/{}".format(champion2_hp, CHAMPION_2_HP)
                return status_text
            else:
                if champion2_rp > CHAMPION_2_RP:
                    champion2_rp = CHAMPION_2_RP
                status_text = "Health Points: {}/{}\n{}: {}/{}".format(champion2_hp, CHAMPION_2_HP, CHAMPION_2_RPNAME,
                                                                       champion2_rp, CHAMPION_2_RP)
                return status_text
        if champion_position == 3:
            if CHAMPION_3_RPNAME == "null":
                status_text = "Health Points: {}/{}".format(champion3_hp, CHAMPION_3_HP)
                return status_text
            else:
                if champion3_rp > CHAMPION_3_RP:
                    champion3_rp = CHAMPION_3_RP
                status_text = "Health Points: {}/{}\n{}: {}/{}".format(champion3_hp, CHAMPION_3_HP, CHAMPION_3_RPNAME,
                                                                       champion3_rp, CHAMPION_3_RP)
                return status_text
        if champion_position == 4:
            if CHAMPION_4_RPNAME == "null":
                status_text = "Health Points: {}/{}".format(champion4_hp, CHAMPION_4_HP)
                return status_text
            else:
                if champion4_rp > CHAMPION_4_RP:
                    champion4_rp = CHAMPION_4_RP
                status_text = "Health Points: {}/{}\n{}: {}/{}".format(champion4_hp, CHAMPION_4_HP, CHAMPION_4_RPNAME,
                                                                       champion4_rp, CHAMPION_4_RP)
                return status_text
        if champion_position == 5:
            if CHAMPION_5_RPNAME == "null":
                status_text = "Health Points: {}/{}".format(champion5_hp, CHAMPION_5_HP)
                return status_text
            else:
                if champion5_rp > CHAMPION_5_RP:
                    champion5_rp = CHAMPION_5_RP
                status_text = "Health Points: {}/{}\n{}: {}/{}".format(champion5_hp, CHAMPION_5_HP, CHAMPION_5_RPNAME,
                                                                       champion5_rp, CHAMPION_5_RP)
                return status_text

    def ai_combat_name(self, ai_postion):
        if ai_postion == 1:
            if AI_SPAWNED == 1:
                if ai1_hp == 0:
                    name_text = "*DEAD* {}".format(AI_NAME)
                    return name_text
                else:
                    name_text = "{}".format(AI_NAME)
                    return name_text
            else:
                if ai1_hp == 0:
                    name_text = "*DEAD* {}#1".format(AI_NICKNAME)
                    return name_text
                else:
                    name_text = "{}#1".format(AI_NICKNAME)
                    return name_text
        if ai_postion == 2:
            if ai2_hp == 0:
                name_text = "*DEAD* {}#2".format(AI_NICKNAME)
                return name_text
            else:
                name_text = "{}#2".format(AI_NICKNAME)
                return name_text
        if ai_postion == 3:
            if ai3_hp == 0:
                name_text = "*DEAD* {}#3".format(AI_NICKNAME)
                return name_text
            else:
                name_text = "{}#3".format(AI_NICKNAME)
                return name_text
        if ai_postion == 4:
            if ai4_hp == 0:
                name_text = "*DEAD* {}#4".format(AI_NICKNAME)
                return name_text
            else:
                name_text = "{}#4".format(AI_NICKNAME)
                return name_text
        if ai_postion == 5:
            if ai5_hp == 0:
                name_text = "*DEAD* {}#5".format(AI_NICKNAME)
                return name_text
            else:
                name_text = "{}#5".format(AI_NICKNAME)
                return name_text

    def ai_combat_status_text(self, ai_position):
        global ai1_hp, ai2_hp, ai3_hp, ai4_hp, ai5_hp
        if ai_position == 1:
            if ai1_hp <= 0:
                ai1_hp = 0
            if AI_RESOURCE_NAME == "null":
                status_text = "Health Points: {}/{}".format(ai1_hp, ai1_max_hp)
                return status_text
            else:
                status_text = "Health Points: {}/{}\n{}: {}/{}".format(ai1_hp, ai1_max_hp, AI_RESOURCE_NAME, ai1_rp,
                                                                       AI_RESOURCE)
                return status_text
        if ai_position == 2:
            if ai2_hp <= 0:
                ai2_hp = 0
            if AI_RESOURCE_NAME == "null":
                status_text = "Health Points: {}/{}".format(ai2_hp, ai2_max_hp)
                return status_text
            else:
                status_text = "Health Points: {}/{}\n{}: {}/{}".format(ai2_hp, ai2_max_hp, AI_RESOURCE_NAME, ai2_rp,
                                                                       AI_RESOURCE)
                return status_text
        if ai_position == 3:
            if ai3_hp <= 0:
                ai3_hp = 0
            if AI_RESOURCE_NAME == "null":
                status_text = "Health Points: {}/{}".format(ai3_hp, ai3_max_hp)
                return status_text
            else:
                status_text = "Health Points: {}/{}\n{}: {}/{}".format(ai3_hp, ai3_max_hp, AI_RESOURCE_NAME, ai3_rp,
                                                                       AI_RESOURCE)
                return status_text
        if ai_position == 4:
            if ai4_hp <= 0:
                ai4_hp = 0
            if AI_RESOURCE_NAME == "null":
                status_text = "Health Points: {}/{}".format(ai4_hp, ai4_max_hp)
                return status_text
            else:
                status_text = "Health Points: {}/{}\n{}: {}/{}".format(ai4_hp, ai4_max_hp, AI_RESOURCE_NAME, ai4_rp,
                                                                       AI_RESOURCE)
                return status_text
        if ai_position == 5:
            if ai5_hp <= 0:
                ai5_hp = 0
            if AI_RESOURCE_NAME == "null":
                status_text = "Health Points: {}/{}".format(ai5_hp, ai5_max_hp)
                return status_text
            else:
                status_text = "Health Points: {}/{}\n{}: {}/{}".format(ai5_hp, ai5_max_hp, AI_RESOURCE_NAME, ai5_rp,
                                                                       AI_RESOURCE)
                return status_text

    def player_combat_champion1(self):
        global attack_button_champion1, special_button_champion1, rest_button_champion1, current_turn, new_round, from_attack_button, from_special_button, \
            floorLevel, roomLevel, from_rest_button
        if new_round == 1:
            self.monster_attack_intentions()
            self.ai_choose_attack_targets()
            new_round = 0
        if from_attack_button == 1:
            attack1_button.destroy()
            attack1_button_details.destroy()
            attack2_button.destroy()
            attack2_button_details.destroy()
            attack3_button.destroy()
            attack3_button_details.destroy()
            attack4_button.destroy()
            attack4_button_details.destroy()
            back_button.destroy()
            from_attack_button = 0
        if from_special_button == 1:
            special1_button.destroy()
            special1_button_details.destroy()
            special2_button.destroy()
            special2_button_details.destroy()
            special3_button.destroy()
            special3_button_details.destroy()
            special4_button.destroy()
            special4_button_details.destroy()
            back_button.destroy()
            from_special_button = 0
        if from_rest_button == 1:
            rest_confirmation_label.destroy()
            rest_confirmation_button.destroy()
            back_button.destroy()
            from_rest_button = 0
        self.repeating_combatUI_refresh_function()
        if combat_results == "win":
            self.combat_to_progression()
        elif combat_results == "lost":
            i = 0
        else:
            self.get_champions_abiltity_button_data(1)
            attack_button_champion1 = tk.Button(dungeon_game_frame, text=self.check_if_power_conduit_text(), width=59,
                                                height=12, command=self.check_if_power_conduit_command)
            special_button_champion1 = tk.Button(dungeon_game_frame, text="Special Moves", width=59, height=12,
                                                 command=self.special_button)
            rest_button_champion1 = tk.Button(dungeon_game_frame, text="Rest", width=59, height=12,
                                              command=self.rest_button)
            attack_button_champion1.grid(row=18, column=1)
            special_button_champion1.grid(row=18, column=2)
            rest_button_champion1.grid(row=18, column=3)

    def next_turn(self):
        global combat_results, current_turn, new_round
        if AI_SPAWNED == 1:
            if ai1_hp <= 0:
                combat_results = "win"
        elif AI_SPAWNED == 2:
            if ai1_hp <= 0:
                if ai2_hp <= 0:
                    combat_results = "win"
        elif AI_SPAWNED == 3:
            if ai1_hp <= 0:
                if ai2_hp <= 0:
                    if ai3_hp <= 0:
                        combat_results = "win"
        elif AI_SPAWNED == 4:
            if ai1_hp <= 0:
                if ai2_hp <= 0:
                    if ai3_hp <= 0:
                        if ai4_hp <= 0:
                            combat_results = "win"
        elif AI_SPAWNED == 5:
            if ai1_hp <= 0:
                if ai2_hp <= 0:
                    if ai3_hp <= 0:
                        if ai4_hp <= 0:
                            if ai5_hp <= 0:
                                combat_results = "win"
        if champion1_hp == 0:
            if champion2_hp == 0:
                if champion3_hp == 0:
                    if champion4_hp == 0:
                        if champion5_hp == 0:
                            combat_results = "lost"
        if current_turn == "C1":
            current_turn = "C2"
            for widget in dungeon_game_frame.winfo_children():
                widget.destroy()
            self.ai_choose_attack_targets()
            self.repeating_combatUI_refresh_function()
            self.champion_turn_ticker(2)
            self.player_combat_champion2()
        elif current_turn == "C2":
            current_turn = "C3"
            for widget in dungeon_game_frame.winfo_children():
                widget.destroy()
            self.repeating_combatUI_refresh_function()
            self.champion_turn_ticker(3)
            self.player_combat_champion3()
        elif current_turn == "C3":
            current_turn = "C4"
            for widget in dungeon_game_frame.winfo_children():
                widget.destroy()
            self.ai_choose_attack_targets()
            self.repeating_combatUI_refresh_function()
            self.champion_turn_ticker(4)
            self.player_combat_champion4()
        elif current_turn == "C4":
            current_turn = "C5"
            for widget in dungeon_game_frame.winfo_children():
                widget.destroy()
            self.ai_choose_attack_targets()
            self.repeating_combatUI_refresh_function()
            self.champion_turn_ticker(5)
            self.player_combat_champion5()
        elif current_turn == "C5":
            current_turn = "MN"
            for widget in dungeon_game_frame.winfo_children():
                widget.destroy()
            self.repeating_combatUI_refresh_function()
            self.monsters_turn()
        elif current_turn == "MN":
            current_turn = "C1"
            for widget in dungeon_game_frame.winfo_children():
                widget.destroy()
            new_round = 1
            self.repeating_combatUI_refresh_function()
            self.champion_turn_ticker(1)
            self.player_combat_champion1()

    def player_combat_champion2(self):
        global attack_button_champion2, special_button_champion2, rest_button_champion2, current_turn, new_round, from_attack_button, from_special_button, \
            roomLevel, floorLevel, from_rest_button
        current_turn = "C2"
        if from_attack_button == 1:
            attack1_button.destroy()
            attack1_button_details.destroy()
            attack2_button.destroy()
            attack2_button_details.destroy()
            attack3_button.destroy()
            attack3_button_details.destroy()
            attack4_button.destroy()
            attack4_button_details.destroy()
            back_button.destroy()
            from_attack_button = 0
        if from_special_button == 1:
            special1_button.destroy()
            special1_button_details.destroy()
            special2_button.destroy()
            special2_button_details.destroy()
            special3_button.destroy()
            special3_button_details.destroy()
            special4_button.destroy()
            special4_button_details.destroy()
            back_button.destroy()
            from_special_button = 0
        if from_rest_button == 1:
            rest_confirmation_label.destroy()
            rest_confirmation_button.destroy()
            back_button.destroy()
            from_rest_button = 0
        if combat_results == "win":
            self.combat_to_progression()
        elif combat_results == "lost":
            i = 0
        else:
            self.get_champions_abiltity_button_data(2)
            attack_button_champion2 = tk.Button(dungeon_game_frame, text=self.check_if_power_conduit_text(), width=59,
                                                height=10, command=self.check_if_power_conduit_command)
            special_button_champion2 = tk.Button(dungeon_game_frame, text="Special Moves", width=59, height=10,
                                                 command=self.special_button)
            rest_button_champion2 = tk.Button(dungeon_game_frame, text="Rest", width=59, height=10,
                                              command=self.rest_button)
            attack_button_champion2.grid(row=18, column=1)
            special_button_champion2.grid(row=18, column=2)
            rest_button_champion2.grid(row=18, column=3)

    def player_combat_champion3(self):
        global attack_button_champion3, special_button_champion3, rest_button_champion3, current_turn, new_round, from_attack_button, from_special_button, \
            roomLevel, floorLevel, from_rest_button
        current_turn = "C3"
        if from_attack_button == 1:
            attack1_button.destroy()
            attack1_button_details.destroy()
            attack2_button.destroy()
            attack2_button_details.destroy()
            attack3_button.destroy()
            attack3_button_details.destroy()
            attack4_button.destroy()
            attack4_button_details.destroy()
            back_button.destroy()
            from_attack_button = 0
        if from_special_button == 1:
            special1_button.destroy()
            special1_button_details.destroy()
            special2_button.destroy()
            special2_button_details.destroy()
            special3_button.destroy()
            special3_button_details.destroy()
            special4_button.destroy()
            special4_button_details.destroy()
            back_button.destroy()
            from_special_button = 0
        if from_rest_button == 1:
            rest_confirmation_label.destroy()
            rest_confirmation_button.destroy()
            back_button.destroy()
            from_rest_button = 0
        if combat_results == "win":
            self.combat_to_progression()
        elif combat_results == "lost":
            i = 0
        else:
            self.get_champions_abiltity_button_data(3)
            attack_button_champion3 = tk.Button(dungeon_game_frame, text=self.check_if_power_conduit_text(), width=59,
                                                height=10, command=self.check_if_power_conduit_command)
            special_button_champion3 = tk.Button(dungeon_game_frame, text="Special Moves", width=59, height=10,
                                                 command=self.special_button)
            rest_button_champion3 = tk.Button(dungeon_game_frame, text="Rest", width=59, height=10,
                                              command=self.rest_button)
            attack_button_champion3.grid(row=18, column=1)
            special_button_champion3.grid(row=18, column=2)
            rest_button_champion3.grid(row=18, column=3)

    def player_combat_champion4(self):
        global attack_button_champion4, special_button_champion4, rest_button_champion4, current_turn, new_round, from_attack_button, from_special_button, \
            roomLevel, floorLevel, from_rest_button
        current_turn = "C4"
        if from_attack_button == 1:
            attack1_button.destroy()
            attack1_button_details.destroy()
            attack2_button.destroy()
            attack2_button_details.destroy()
            attack3_button.destroy()
            attack3_button_details.destroy()
            attack4_button.destroy()
            attack4_button_details.destroy()
            back_button.destroy()
            from_attack_button = 0
        if from_special_button == 1:
            special1_button.destroy()
            special1_button_details.destroy()
            special2_button.destroy()
            special2_button_details.destroy()
            special3_button.destroy()
            special3_button_details.destroy()
            special4_button.destroy()
            special4_button_details.destroy()
            back_button.destroy()
            from_special_button = 0
        if from_rest_button == 1:
            rest_confirmation_label.destroy()
            rest_confirmation_button.destroy()
            back_button.destroy()
            from_rest_button = 0
        if combat_results == "win":
            self.combat_to_progression()
        elif combat_results == "lost":
            i = 0
        else:
            self.get_champions_abiltity_button_data(4)
            attack_button_champion4 = tk.Button(dungeon_game_frame, text=self.check_if_power_conduit_text(), width=59,
                                                height=10, command=self.check_if_power_conduit_command)
            special_button_champion4 = tk.Button(dungeon_game_frame, text="Special Moves", width=59, height=10,
                                                 command=self.special_button)
            rest_button_champion4 = tk.Button(dungeon_game_frame, text="Rest", width=59, height=10,
                                              command=self.rest_button)
            attack_button_champion4.grid(row=18, column=1)
            special_button_champion4.grid(row=18, column=2)
            rest_button_champion4.grid(row=18, column=3)

    def player_combat_champion5(self):
        global attack_button_champion5, special_button_champion5, rest_button_champion5, current_turn, new_round, from_attack_button, from_special_button, \
            roomLevel, floorLevel, from_rest_button
        current_turn = "C5"
        if from_attack_button == 1:
            attack1_button.destroy()
            attack1_button_details.destroy()
            attack2_button.destroy()
            attack2_button_details.destroy()
            attack3_button.destroy()
            attack3_button_details.destroy()
            attack4_button.destroy()
            attack4_button_details.destroy()
            back_button.destroy()
            from_attack_button = 0
        if from_special_button == 1:
            special1_button.destroy()
            special1_button_details.destroy()
            special2_button.destroy()
            special2_button_details.destroy()
            special3_button.destroy()
            special3_button_details.destroy()
            special4_button.destroy()
            special4_button_details.destroy()
            back_button.destroy()
            from_special_button = 0
        if from_rest_button == 1:
            rest_confirmation_label.destroy()
            rest_confirmation_button.destroy()
            back_button.destroy()
            from_rest_button = 0
        if combat_results == "win":
            self.combat_to_progression()
        elif combat_results == "lost":
            i = 0
        else:
            self.get_champions_abiltity_button_data(5)
            attack_button_champion5 = tk.Button(dungeon_game_frame, text=self.check_if_power_conduit_text(), width=59,
                                                height=10, command=self.check_if_power_conduit_command)
            special_button_champion5 = tk.Button(dungeon_game_frame, text="Special Moves", width=59, height=10,
                                                 command=self.special_button)
            rest_button_champion5 = tk.Button(dungeon_game_frame, text="Rest", width=59, height=10,
                                              command=self.rest_button)
            attack_button_champion5.grid(row=18, column=1)
            special_button_champion5.grid(row=18, column=2)
            rest_button_champion5.grid(row=18, column=3)

    def monsters_turn(self):
        global combat_results, current_turn, ai1_stun, ai2_stun, ai3_stun, ai4_stun, ai5_stun, ai1_taunt, ai2_taunt, ai3_taunt, ai4_taunt, ai5_taunt, \
            ai1_brittle, ai2_brittle, ai3_brittle, ai4_brittle, ai5_brittle, ai1_weakness, ai2_weakness, ai3_weakness, ai4_weakness, ai5_weakness, \
            ai1_burnDot, ai2_burnDot, ai3_burnDot, ai4_burnDot, ai5_burnDot, ai1_SerraSlashDot, ai2_SerraSlashDot, ai3_SerraSlashDot, \
            ai4_SerraSlashDot, ai5_SerraSlashDot, ai1_garroteDot, ai2_garroteDot, ai3_garroteDot, ai4_garroteDot, ai5_garroteDot, \
            ai1_EviscerDot, ai2_EviscerDot, ai3_EviscerDot, ai4_EviscerDot, ai5_EviscerDot, \
            ai1_statuses, ai2_statuses, ai3_statuses, ai4_statuses, ai5_statuses, \
            ai1_hp, ai2_hp, ai3_hp, ai4_hp, ai5_hp, \
            champion1_hp, champion2_hp, champion3_hp,champion4_hp, champion5_hp

        if combat_results == "win":
            self.combat_to_progression()
        elif combat_results == "lost":
            i = 0
        else:
            if AI_SPAWNED == 1:
                monster_list = [1]
            elif AI_SPAWNED == 2:
                monster_list = [1,2]
            elif AI_SPAWNED == 3:
                monster_list = [1,2,3]
            elif AI_SPAWNED == 4:
                monster_list = [1,2,3,4]
            elif AI_SPAWNED == 5:
                monster_list = [1,2,3,4,5]
            for monster_var in monster_list:
                if monster_var == $:
                    if ai$_hp == 0:
                        continue
                    if len(ai$_pricked) != 0:
                        ai$_hp = ai$_hp - ai$_pricked[0]
                        if ai$_hp < 0:
                            ai$_hp = 0
                            continue
                    if ai$_burnDot[1] != 0:
                        ai$_hp = ai$_hp - ai$_burnDot[0]
                        ai$_burnDot[1] = ai$_burnDot[1] - 1
                        if ai$_hp < 0:
                            ai$_hp = 0
                            continue
                    if ai$_SerraSlashDot[1] != 0:
                        ai$_hp = ai$_hp - ai$_SerraSlashDot[0]
                        ai$_SerraSlashDot[1] = ai$_SerraSlashDot[1] - 1
                        if ai$_hp < 0:
                            ai$_hp = 0
                            continue
                    if ai$_EviscerDot[1] != 0:
                        ai$_hp = ai$_hp - ai$_EviscerDot[0]
                        ai$_EviscerDot[1] = ai$_EviscerDot[1] - 1
                        if ai$_hp < 0:
                            ai$_hp = 0
                            continue
                    if ai$_garroteDot[1] != 0:
                        ai$_hp = ai$_hp - ai$_garroteDot[0]
                        ai$_garroteDot[1] = ai$_garroteDot[1] - 1
                        if ai$_hp < 0:
                            ai$_hp = 0
                            continue
                    if ai$_stun != 0:
                        continue
                    if ai$_taunt[1] != 0:
                        taunter_counter = 1
                        for champion in CHAMPION_LIST:
                            if champion == ai$_taunt[0]:
                                break
                            taunter_counter += 1
                        if taunter_counter == 1:
                            if len(champion1_guarded) != 0:
                                guard_list = []
                                for guards in champion1_guarded:
                                    if guards == "Block":
                                        guard_list.append(99)
                                    if guards == "Parry":
                                        guard_list.append(101)
                                    if guards == "Boulder":
                                        guard_list.append(100)
                                    if guards == "Elusive Measures":
                                        guard_list.append(100)
                                    guard_list = sorted(guard_list, reverse=True)
                                    if guard_list[0] == 101:
                                        ai$_hp = ai$_hp - ai1_attack[1]
                                        if champion1_thorns[0] == 1:
                                            ai$_hp = ai$_hp - 200
                                        if ai$_hp < 0:
                                            ai$_hp = 0
                                    if guard_list[0] == 100:
                                        champion1_hp = champion1_hp
                                    if guard_list[0] == 99:
                                        bodyguard_counter = 1
                                        for champions in CHAMPION_LIST:
                                            if champions == VETERAN_BODYGUARD.name:
                                                break
                                            bodyguard_counter
                                        if bodyguard_counter == 1:
                                            champion1_hp = champion1_hp - (ai$_attack[1] * 0.4)
                                        if bodyguard_counter == 2:
                                            champion2_hp = champion2_hp - (ai$_attack[1] * 0.4)
                                        if bodyguard_counter == 3:
                                            champion3_hp = champion3_hp - (ai$_attack[1] * 0.4)
                                        if bodyguard_counter == 4:
                                            champion4_hp = champion4_hp - (ai$_attack[1] * 0.4)
                                        if bodyguard_counter == 5:
                                            champion5_hp = champion5_hp - (ai$_attack[1] * 0.4)
                            if CHAMPION_LIST[0] == MONK.name:
                                staggered_damage = ai$_attack[1] / 3
                                if len(monk_staggered_damage_list1) == 0:
                                    monk_staggered_damage_list1






            current_turn = "MN"
            self.next_turn()

    def combat_to_progression(self):
        global roomLevel, floorLevel, from_combat, permaHealthMod
        roomLevel += 1
        if roomLevel > 5:
            floorLevel += 1
            roomLevel = 1
            permaHealthMod += 1
        for widget in dungeon_game_frame.winfo_children():
            widget.destroy()
        from_combat = 1
        self.DungeonFloorProgress()

    def check_if_power_conduit_text(self):
        counter = 1
        for character in CHAMPION_LIST:
            if character == "Power Conduit":
                turn_check = "C{}".format(counter)
                if current_turn == turn_check:
                    attack_text = "Cannot Attack"
                    return attack_text
            counter += 1
        attack_text = "Attack"
        return attack_text

    def check_if_power_conduit_command(self):
        counter = 1
        for character in CHAMPION_LIST:
            if character == "Power Conduit":
                turn_check = "C{}".format(counter)
                if current_turn == turn_check:
                    break
            counter += 1
        self.attack_button()

    def champion_turn_ticker(self, champion_position):
        global leg_sweep_requirements, pressure_points_requirements, challenging_shout_requirements, trainwreck_requirements, \
            fortification_requirements, disruptive_slash_requirements, parry_requirements, elusive_measures_requirements, \
            reckless_flurry_requirements, eviscerate_requirements, exploit_weakness_requirements, scrap_bomb_requirements, \
            play_dead_requirements, rushed_rest_requirements, uppercut_requirements, defensive_stance_requirements, \
            rushdown_requirements, arcane_brilliance_requirements, vine_swipe_requirements, prickle_arena_requirements, \
            wound_fissure_requirements, blood_boil_requirements, enharden_nerves_requirements, righteous_blow_requirements, \
            aura_of_power_requirements, aura_of_protection_requirements, power_opt_requirements, equip_iron_cast_arrows_requirements, \
            equip_tracker_tipped_arrows_requirements, crashing_boom_requirements, thunderous_vigor_requirements, rejuvenating_whirlpool_requirements, \
            alter_time_requirements, perfected_herbal_tea_requirements, g3t_jaxd_requirements
        if champion_position == 1:
            if CHAMPION_LIST[0] == "Monk":
                if leg_sweep_requirements[1] > 0:
                    leg_sweep_requirements[1] = leg_sweep_requirements[1] - 1
                if pressure_points_requirements[1] > 0:
                    pressure_points_requirements[1] = pressure_points_requirements[1] - 1
            if CHAMPION_LIST[0] == "Barbarian":
                if challenging_shout_requirements[1] > 0:
                    challenging_shout_requirements[1] = challenging_shout_requirements[1] - 1
            if CHAMPION_LIST[0] == "Veteran Bodyguard":
                if trainwreck_requirements[1] > 0:
                    trainwreck_requirements[1] = trainwreck_requirements[1] - 1
                if fortification_requirements[1] > 0:
                    fortification_requirements[1] = fortification_requirements[1] - 1
            if CHAMPION_LIST[0] == "Fencer":
                if disruptive_slash_requirements[1] > 0:
                    disruptive_slash_requirements[1] = disruptive_slash_requirements[1] - 1
                if parry_requirements[1] > 0:
                    parry_requirements[1] = parry_requirements[1] - 1
                if elusive_measures_requirements[1] > 0:
                    elusive_measures_requirements[1] = elusive_measures_requirements[1] - 1
            if CHAMPION_LIST[0] == "Berserker":
                if reckless_flurry_requirements[1] > 0:
                    reckless_flurry_requirements[1] = reckless_flurry_requirements[1] - 1
            if CHAMPION_LIST[0] == "Rogue":
                if eviscerate_requirements[1] > 0:
                    eviscerate_requirements[1] = eviscerate_requirements[1] - 1
                if exploit_weakness_requirements[1] > 0:
                    exploit_weakness_requirements[1] = exploit_weakness_requirements[1] - 1
            if CHAMPION_LIST[0] == "Survivalist":
                if scrap_bomb_requirements[1] > 0:
                    scrap_bomb_requirements[1] = scrap_bomb_requirements[1] - 1
                if play_dead_requirements[1] > 0:
                    play_dead_requirements[1] = play_dead_requirements[1] - 1
                if rushed_rest_requirements[1] > 0:
                    rushed_rest_requirements[1] = rushed_rest_requirements[1] - 1
            if CHAMPION_LIST[0] == "Brawlist ":
                if uppercut_requirements[1] > 0:
                    uppercut_requirements[1] = uppercut_requirements[1] - 1
                if defensive_stance_requirements[1] > 0:
                    defensive_stance_requirements[1] = defensive_stance_requirements[1] - 1
                if rushdown_requirements[1] > 0:
                    rushdown_requirements[1] = rushdown_requirements[1] - 1
            if CHAMPION_LIST[0] == "Academics Mage":
                if arcane_brilliance_requirements[1] > 0:
                    arcane_brilliance_requirements[1] = arcane_brilliance_requirements[1] - 1
            if CHAMPION_LIST[0] == "Druid":
                if vine_swipe_requirements[1] > 0:
                    vine_swipe_requirements[1] = vine_swipe_requirements[1] - 1
                if prickle_arena_requirements[1] > 0:
                    prickle_arena_requirements[1] = prickle_arena_requirements[1] - 1
            if CHAMPION_LIST[0] == "Warlock":
                if wound_fissure_requirements[1] > 0:
                    wound_fissure_requirements[1] = wound_fissure_requirements[1] - 1
            if CHAMPION_LIST[0] == "Bloodmancer":
                if blood_boil_requirements[1] > 0:
                    blood_boil_requirements[1] = blood_boil_requirements[1] - 1
                if enharden_nerves_requirements[1] > 0:
                    enharden_nerves_requirements[1] = enharden_nerves_requirements[1] - 1
            if CHAMPION_LIST[0] == "Paladin":
                if righteous_blow_requirements[1] > 0:
                    righteous_blow_requirements[1] = righteous_blow_requirements[1] - 1
                if aura_of_power_requirements[1] > 0:
                    aura_of_power_requirements[1] = aura_of_power_requirements[1] - 1
                if aura_of_protection_requirements[1] > 0:
                    aura_of_protection_requirements[1] = aura_of_protection_requirements[1] - 1
            if CHAMPION_LIST[0] == "Ranger":
                if power_opt_requirements[1] > 0:
                    power_opt_requirements[1] = power_opt_requirements[1] - 1
                if equip_iron_cast_arrows_requirements[1] > 0:
                    equip_iron_cast_arrows_requirements[1] = equip_iron_cast_arrows_requirements[1] - 1
                if equip_tracker_tipped_arrows_requirements[1] > 0:
                    equip_tracker_tipped_arrows_requirements[1] = equip_tracker_tipped_arrows_requirements[1] - 1
            if CHAMPION_LIST[0] == "Thunderous Apprentice":
                if crashing_boom_requirements[1] > 0:
                    crashing_boom_requirements[1] = crashing_boom_requirements[1] - 1
                if thunderous_vigor_requirements[1] > 0:
                    thunderous_vigor_requirements[1] = thunderous_vigor_requirements[1] - 1
            if CHAMPION_LIST[0] == "Earth Speaker":
                if rejuvenating_whirlpool_requirements[1] > 0:
                    rejuvenating_whirlpool_requirements[1] = rejuvenating_whirlpool_requirements[1] - 1
            if CHAMPION_LIST[0] == "Time Walker":
                if alter_time_requirements[1] > 0:
                    alter_time_requirements[1] = alter_time_requirements[1] - 1
            if CHAMPION_LIST[0] == "Field Medic":
                if perfected_herbal_tea_requirements[1] > 0:
                    perfected_herbal_tea_requirements[1] = perfected_herbal_tea_requirements[1] - 1
                if g3t_jaxd_requirements[1] > 0:
                    g3t_jaxd_requirements[1] = g3t_jaxd_requirements[1] - 1
        if champion_position == 2:
            if CHAMPION_LIST[1] == "Monk":
                if leg_sweep_requirements[1] > 0:
                    leg_sweep_requirements[1] = leg_sweep_requirements[1] - 1
                if pressure_points_requirements[1] > 0:
                    pressure_points_requirements[1] = pressure_points_requirements[1] - 1
            if CHAMPION_LIST[1] == "Barbarian":
                if challenging_shout_requirements[1] > 0:
                    challenging_shout_requirements[1] = challenging_shout_requirements[1] - 1
            if CHAMPION_LIST[1] == "Veteran Bodyguard":
                if trainwreck_requirements[1] > 0:
                    trainwreck_requirements[1] = trainwreck_requirements[1] - 1
                if fortification_requirements[1] > 0:
                    fortification_requirements[1] = fortification_requirements[1] - 1
            if CHAMPION_LIST[1] == "Fencer":
                if disruptive_slash_requirements[1] > 0:
                    disruptive_slash_requirements[1] = disruptive_slash_requirements[1] - 1
                if parry_requirements[1] > 0:
                    parry_requirements[1] = parry_requirements[1] - 1
                if elusive_measures_requirements[1] > 0:
                    elusive_measures_requirements[1] = elusive_measures_requirements[1] - 1
            if CHAMPION_LIST[1] == "Berserker":
                if reckless_flurry_requirements[1] > 0:
                    reckless_flurry_requirements[1] = reckless_flurry_requirements[1] - 1
            if CHAMPION_LIST[1] == "Rogue":
                if eviscerate_requirements[1] > 0:
                    eviscerate_requirements[1] = eviscerate_requirements[1] - 1
                if exploit_weakness_requirements[1] > 0:
                    exploit_weakness_requirements[1] = exploit_weakness_requirements[1] - 1
            if CHAMPION_LIST[1] == "Survivalist":
                if scrap_bomb_requirements[1] > 0:
                    scrap_bomb_requirements[1] = scrap_bomb_requirements[1] - 1
                if play_dead_requirements[1] > 0:
                    play_dead_requirements[1] = play_dead_requirements[1] - 1
                if rushed_rest_requirements[1] > 0:
                    rushed_rest_requirements[1] = rushed_rest_requirements[1] - 1
            if CHAMPION_LIST[1] == "Brawlist ":
                if uppercut_requirements[1] > 0:
                    uppercut_requirements[1] = uppercut_requirements[1] - 1
                if defensive_stance_requirements[1] > 0:
                    defensive_stance_requirements[1] = defensive_stance_requirements[1] - 1
                if rushdown_requirements[1] > 0:
                    rushdown_requirements[1] = rushdown_requirements[1] - 1
            if CHAMPION_LIST[1] == "Academics Mage":
                if arcane_brilliance_requirements[1] > 0:
                    arcane_brilliance_requirements[1] = arcane_brilliance_requirements[1] - 1
            if CHAMPION_LIST[1] == "Druid":
                if vine_swipe_requirements[1] > 0:
                    vine_swipe_requirements[1] = vine_swipe_requirements[1] - 1
                if prickle_arena_requirements[1] > 0:
                    prickle_arena_requirements[1] = prickle_arena_requirements[1] - 1
            if CHAMPION_LIST[1] == "Warlock":
                if wound_fissure_requirements[1] > 0:
                    wound_fissure_requirements[1] = wound_fissure_requirements[1] - 1
            if CHAMPION_LIST[1] == "Bloodmancer":
                if blood_boil_requirements[1] > 0:
                    blood_boil_requirements[1] = blood_boil_requirements[1] - 1
                if enharden_nerves_requirements[1] > 0:
                    enharden_nerves_requirements[1] = enharden_nerves_requirements[1] - 1
            if CHAMPION_LIST[1] == "Paladin":
                if righteous_blow_requirements[1] > 0:
                    righteous_blow_requirements[1] = righteous_blow_requirements[1] - 1
                if aura_of_power_requirements[1] > 0:
                    aura_of_power_requirements[1] = aura_of_power_requirements[1] - 1
                if aura_of_protection_requirements[1] > 0:
                    aura_of_protection_requirements[1] = aura_of_protection_requirements[1] - 1
            if CHAMPION_LIST[1] == "Ranger":
                if power_opt_requirements[1] > 0:
                    power_opt_requirements[1] = power_opt_requirements[1] - 1
                if equip_iron_cast_arrows_requirements[1] > 0:
                    equip_iron_cast_arrows_requirements[1] = equip_iron_cast_arrows_requirements[1] - 1
                if equip_tracker_tipped_arrows_requirements[1] > 0:
                    equip_tracker_tipped_arrows_requirements[1] = equip_tracker_tipped_arrows_requirements[1] - 1
            if CHAMPION_LIST[1] == "Thunderous Apprentice":
                if crashing_boom_requirements[1] > 0:
                    crashing_boom_requirements[1] = crashing_boom_requirements[1] - 1
                if thunderous_vigor_requirements[1] > 0:
                    thunderous_vigor_requirements[1] = thunderous_vigor_requirements[1] - 1
            if CHAMPION_LIST[1] == "Earth Speaker":
                if rejuvenating_whirlpool_requirements[1] > 0:
                    rejuvenating_whirlpool_requirements[1] = rejuvenating_whirlpool_requirements[1] - 1
            if CHAMPION_LIST[1] == "Time Walker":
                if alter_time_requirements[1] > 0:
                    alter_time_requirements[1] = alter_time_requirements[1] - 1
            if CHAMPION_LIST[1] == "Field Medic":
                if perfected_herbal_tea_requirements[1] > 0:
                    perfected_herbal_tea_requirements[1] = perfected_herbal_tea_requirements[1] - 1
                if g3t_jaxd_requirements[1] > 0:
                    g3t_jaxd_requirements[1] = g3t_jaxd_requirements[1] - 1
        if champion_position == 3:
            if CHAMPION_LIST[2] == "Monk":
                if leg_sweep_requirements[1] > 0:
                    leg_sweep_requirements[1] = leg_sweep_requirements[1] - 1
                if pressure_points_requirements[1] > 0:
                    pressure_points_requirements[1] = pressure_points_requirements[1] - 1
            if CHAMPION_LIST[2] == "Barbarian":
                if challenging_shout_requirements[1] > 0:
                    challenging_shout_requirements[1] = challenging_shout_requirements[1] - 1
            if CHAMPION_LIST[2] == "Veteran Bodyguard":
                if trainwreck_requirements[1] > 0:
                    trainwreck_requirements[1] = trainwreck_requirements[1] - 1
                if fortification_requirements[1] > 0:
                    fortification_requirements[1] = fortification_requirements[1] - 1
            if CHAMPION_LIST[2] == "Fencer":
                if disruptive_slash_requirements[1] > 0:
                    disruptive_slash_requirements[1] = disruptive_slash_requirements[1] - 1
                if parry_requirements[1] > 0:
                    parry_requirements[1] = parry_requirements[1] - 1
                if elusive_measures_requirements[1] > 0:
                    elusive_measures_requirements[1] = elusive_measures_requirements[1] - 1
            if CHAMPION_LIST[2] == "Berserker":
                if reckless_flurry_requirements[1] > 0:
                    reckless_flurry_requirements[1] = reckless_flurry_requirements[1] - 1
            if CHAMPION_LIST[2] == "Rogue":
                if eviscerate_requirements[1] > 0:
                    eviscerate_requirements[1] = eviscerate_requirements[1] - 1
                if exploit_weakness_requirements[1] > 0:
                    exploit_weakness_requirements[1] = exploit_weakness_requirements[1] - 1
            if CHAMPION_LIST[2] == "Survivalist":
                if scrap_bomb_requirements[1] > 0:
                    scrap_bomb_requirements[1] = scrap_bomb_requirements[1] - 1
                if play_dead_requirements[1] > 0:
                    play_dead_requirements[1] = play_dead_requirements[1] - 1
                if rushed_rest_requirements[1] > 0:
                    rushed_rest_requirements[1] = rushed_rest_requirements[1] - 1
            if CHAMPION_LIST[2] == "Brawlist ":
                if uppercut_requirements[1] > 0:
                    uppercut_requirements[1] = uppercut_requirements[1] - 1
                if defensive_stance_requirements[1] > 0:
                    defensive_stance_requirements[1] = defensive_stance_requirements[1] - 1
                if rushdown_requirements[1] > 0:
                    rushdown_requirements[1] = rushdown_requirements[1] - 1
            if CHAMPION_LIST[2] == "Academics Mage":
                if arcane_brilliance_requirements[1] > 0:
                    arcane_brilliance_requirements[1] = arcane_brilliance_requirements[1] - 1
            if CHAMPION_LIST[2] == "Druid":
                if vine_swipe_requirements[1] > 0:
                    vine_swipe_requirements[1] = vine_swipe_requirements[1] - 1
                if prickle_arena_requirements[1] > 0:
                    prickle_arena_requirements[1] = prickle_arena_requirements[1] - 1
            if CHAMPION_LIST[2] == "Warlock":
                if wound_fissure_requirements[1] > 0:
                    wound_fissure_requirements[1] = wound_fissure_requirements[1] - 1
            if CHAMPION_LIST[2] == "Bloodmancer":
                if blood_boil_requirements[1] > 0:
                    blood_boil_requirements[1] = blood_boil_requirements[1] - 1
                if enharden_nerves_requirements[1] > 0:
                    enharden_nerves_requirements[1] = enharden_nerves_requirements[1] - 1
            if CHAMPION_LIST[2] == "Paladin":
                if righteous_blow_requirements[1] > 0:
                    righteous_blow_requirements[1] = righteous_blow_requirements[1] - 1
                if aura_of_power_requirements[1] > 0:
                    aura_of_power_requirements[1] = aura_of_power_requirements[1] - 1
                if aura_of_protection_requirements[1] > 0:
                    aura_of_protection_requirements[1] = aura_of_protection_requirements[1] - 1
            if CHAMPION_LIST[2] == "Ranger":
                if power_opt_requirements[1] > 0:
                    power_opt_requirements[1] = power_opt_requirements[1] - 1
                if equip_iron_cast_arrows_requirements[1] > 0:
                    equip_iron_cast_arrows_requirements[1] = equip_iron_cast_arrows_requirements[1] - 1
                if equip_tracker_tipped_arrows_requirements[1] > 0:
                    equip_tracker_tipped_arrows_requirements[1] = equip_tracker_tipped_arrows_requirements[1] - 1
            if CHAMPION_LIST[2] == "Thunderous Apprentice":
                if crashing_boom_requirements[1] > 0:
                    crashing_boom_requirements[1] = crashing_boom_requirements[1] - 1
                if thunderous_vigor_requirements[1] > 0:
                    thunderous_vigor_requirements[1] = thunderous_vigor_requirements[1] - 1
            if CHAMPION_LIST[2] == "Earth Speaker":
                if rejuvenating_whirlpool_requirements[1] > 0:
                    rejuvenating_whirlpool_requirements[1] = rejuvenating_whirlpool_requirements[1] - 1
            if CHAMPION_LIST[2] == "Time Walker":
                if alter_time_requirements[1] > 0:
                    alter_time_requirements[1] = alter_time_requirements[1] - 1
            if CHAMPION_LIST[2] == "Field Medic":
                if perfected_herbal_tea_requirements[1] > 0:
                    perfected_herbal_tea_requirements[1] = perfected_herbal_tea_requirements[1] - 1
                if g3t_jaxd_requirements[1] > 0:
                    g3t_jaxd_requirements[1] = g3t_jaxd_requirements[1] - 1
        if champion_position == 4:
            if CHAMPION_LIST[3] == "Monk":
                if leg_sweep_requirements[1] > 0:
                    leg_sweep_requirements[1] = leg_sweep_requirements[1] - 1
                if pressure_points_requirements[1] > 0:
                    pressure_points_requirements[1] = pressure_points_requirements[1] - 1
            if CHAMPION_LIST[3] == "Barbarian":
                if challenging_shout_requirements[1] > 0:
                    challenging_shout_requirements[1] = challenging_shout_requirements[1] - 1
            if CHAMPION_LIST[3] == "Veteran Bodyguard":
                if trainwreck_requirements[1] > 0:
                    trainwreck_requirements[1] = trainwreck_requirements[1] - 1
                if fortification_requirements[1] > 0:
                    fortification_requirements[1] = fortification_requirements[1] - 1
            if CHAMPION_LIST[3] == "Fencer":
                if disruptive_slash_requirements[1] > 0:
                    disruptive_slash_requirements[1] = disruptive_slash_requirements[1] - 1
                if parry_requirements[1] > 0:
                    parry_requirements[1] = parry_requirements[1] - 1
                if elusive_measures_requirements[1] > 0:
                    elusive_measures_requirements[1] = elusive_measures_requirements[1] - 1
            if CHAMPION_LIST[3] == "Berserker":
                if reckless_flurry_requirements[1] > 0:
                    reckless_flurry_requirements[1] = reckless_flurry_requirements[1] - 1
            if CHAMPION_LIST[3] == "Rogue":
                if eviscerate_requirements[1] > 0:
                    eviscerate_requirements[1] = eviscerate_requirements[1] - 1
                if exploit_weakness_requirements[1] > 0:
                    exploit_weakness_requirements[1] = exploit_weakness_requirements[1] - 1
            if CHAMPION_LIST[3] == "Survivalist":
                if scrap_bomb_requirements[1] > 0:
                    scrap_bomb_requirements[1] = scrap_bomb_requirements[1] - 1
                if play_dead_requirements[1] > 0:
                    play_dead_requirements[1] = play_dead_requirements[1] - 1
                if rushed_rest_requirements[1] > 0:
                    rushed_rest_requirements[1] = rushed_rest_requirements[1] - 1
            if CHAMPION_LIST[3] == "Brawlist ":
                if uppercut_requirements[1] > 0:
                    uppercut_requirements[1] = uppercut_requirements[1] - 1
                if defensive_stance_requirements[1] > 0:
                    defensive_stance_requirements[1] = defensive_stance_requirements[1] - 1
                if rushdown_requirements[1] > 0:
                    rushdown_requirements[1] = rushdown_requirements[1] - 1
            if CHAMPION_LIST[3] == "Academics Mage":
                if arcane_brilliance_requirements[1] > 0:
                    arcane_brilliance_requirements[1] = arcane_brilliance_requirements[1] - 1
            if CHAMPION_LIST[3] == "Druid":
                if vine_swipe_requirements[1] > 0:
                    vine_swipe_requirements[1] = vine_swipe_requirements[1] - 1
                if prickle_arena_requirements[1] > 0:
                    prickle_arena_requirements[1] = prickle_arena_requirements[1] - 1
            if CHAMPION_LIST[3] == "Warlock":
                if wound_fissure_requirements[1] > 0:
                    wound_fissure_requirements[1] = wound_fissure_requirements[1] - 1
            if CHAMPION_LIST[3] == "Bloodmancer":
                if blood_boil_requirements[1] > 0:
                    blood_boil_requirements[1] = blood_boil_requirements[1] - 1
                if enharden_nerves_requirements[1] > 0:
                    enharden_nerves_requirements[1] = enharden_nerves_requirements[1] - 1
            if CHAMPION_LIST[3] == "Paladin":
                if righteous_blow_requirements[1] > 0:
                    righteous_blow_requirements[1] = righteous_blow_requirements[1] - 1
                if aura_of_power_requirements[1] > 0:
                    aura_of_power_requirements[1] = aura_of_power_requirements[1] - 1
                if aura_of_protection_requirements[1] > 0:
                    aura_of_protection_requirements[1] = aura_of_protection_requirements[1] - 1
            if CHAMPION_LIST[3] == "Ranger":
                if power_opt_requirements[1] > 0:
                    power_opt_requirements[1] = power_opt_requirements[1] - 1
                if equip_iron_cast_arrows_requirements[1] > 0:
                    equip_iron_cast_arrows_requirements[1] = equip_iron_cast_arrows_requirements[1] - 1
                if equip_tracker_tipped_arrows_requirements[1] > 0:
                    equip_tracker_tipped_arrows_requirements[1] = equip_tracker_tipped_arrows_requirements[1] - 1
            if CHAMPION_LIST[3] == "Thunderous Apprentice":
                if crashing_boom_requirements[1] > 0:
                    crashing_boom_requirements[1] = crashing_boom_requirements[1] - 1
                if thunderous_vigor_requirements[1] > 0:
                    thunderous_vigor_requirements[1] = thunderous_vigor_requirements[1] - 1
            if CHAMPION_LIST[3] == "Earth Speaker":
                if rejuvenating_whirlpool_requirements[1] > 0:
                    rejuvenating_whirlpool_requirements[1] = rejuvenating_whirlpool_requirements[1] - 1
            if CHAMPION_LIST[3] == "Time Walker":
                if alter_time_requirements[1] > 0:
                    alter_time_requirements[1] = alter_time_requirements[1] - 1
            if CHAMPION_LIST[3] == "Field Medic":
                if perfected_herbal_tea_requirements[1] > 0:
                    perfected_herbal_tea_requirements[1] = perfected_herbal_tea_requirements[1] - 1
                if g3t_jaxd_requirements[1] > 0:
                    g3t_jaxd_requirements[1] = g3t_jaxd_requirements[1] - 1
        if champion_position == 5:
            if CHAMPION_LIST[4] == "Monk":
                if leg_sweep_requirements[1] > 0:
                    leg_sweep_requirements[1] = leg_sweep_requirements[1] - 1
                if pressure_points_requirements[1] > 0:
                    pressure_points_requirements[1] = pressure_points_requirements[1] - 1
            if CHAMPION_LIST[4] == "Barbarian":
                if challenging_shout_requirements[1] > 0:
                    challenging_shout_requirements[1] = challenging_shout_requirements[1] - 1
            if CHAMPION_LIST[4] == "Veteran Bodyguard":
                if trainwreck_requirements[1] > 0:
                    trainwreck_requirements[1] = trainwreck_requirements[1] - 1
                if fortification_requirements[1] > 0:
                    fortification_requirements[1] = fortification_requirements[1] - 1
            if CHAMPION_LIST[4] == "Fencer":
                if disruptive_slash_requirements[1] > 0:
                    disruptive_slash_requirements[1] = disruptive_slash_requirements[1] - 1
                if parry_requirements[1] > 0:
                    parry_requirements[1] = parry_requirements[1] - 1
                if elusive_measures_requirements[1] > 0:
                    elusive_measures_requirements[1] = elusive_measures_requirements[1] - 1
            if CHAMPION_LIST[4] == "Berserker":
                if reckless_flurry_requirements[1] > 0:
                    reckless_flurry_requirements[1] = reckless_flurry_requirements[1] - 1
            if CHAMPION_LIST[4] == "Rogue":
                if eviscerate_requirements[1] > 0:
                    eviscerate_requirements[1] = eviscerate_requirements[1] - 1
                if exploit_weakness_requirements[1] > 0:
                    exploit_weakness_requirements[1] = exploit_weakness_requirements[1] - 1
            if CHAMPION_LIST[4] == "Survivalist":
                if scrap_bomb_requirements[1] > 0:
                    scrap_bomb_requirements[1] = scrap_bomb_requirements[1] - 1
                if play_dead_requirements[1] > 0:
                    play_dead_requirements[1] = play_dead_requirements[1] - 1
                if rushed_rest_requirements[1] > 0:
                    rushed_rest_requirements[1] = rushed_rest_requirements[1] - 1
            if CHAMPION_LIST[4] == "Brawlist ":
                if uppercut_requirements[1] > 0:
                    uppercut_requirements[1] = uppercut_requirements[1] - 1
                if defensive_stance_requirements[1] > 0:
                    defensive_stance_requirements[1] = defensive_stance_requirements[1] - 1
                if rushdown_requirements[1] > 0:
                    rushdown_requirements[1] = rushdown_requirements[1] - 1
            if CHAMPION_LIST[4] == "Academics Mage":
                if arcane_brilliance_requirements[1] > 0:
                    arcane_brilliance_requirements[1] = arcane_brilliance_requirements[1] - 1
            if CHAMPION_LIST[4] == "Druid":
                if vine_swipe_requirements[1] > 0:
                    vine_swipe_requirements[1] = vine_swipe_requirements[1] - 1
                if prickle_arena_requirements[1] > 0:
                    prickle_arena_requirements[1] = prickle_arena_requirements[1] - 1
            if CHAMPION_LIST[4] == "Warlock":
                if wound_fissure_requirements[1] > 0:
                    wound_fissure_requirements[1] = wound_fissure_requirements[1] - 1
            if CHAMPION_LIST[4] == "Bloodmancer":
                if blood_boil_requirements[1] > 0:
                    blood_boil_requirements[1] = blood_boil_requirements[1] - 1
                if enharden_nerves_requirements[1] > 0:
                    enharden_nerves_requirements[1] = enharden_nerves_requirements[1] - 1
            if CHAMPION_LIST[4] == "Paladin":
                if righteous_blow_requirements[1] > 0:
                    righteous_blow_requirements[1] = righteous_blow_requirements[1] - 1
                if aura_of_power_requirements[1] > 0:
                    aura_of_power_requirements[1] = aura_of_power_requirements[1] - 1
                if aura_of_protection_requirements[1] > 0:
                    aura_of_protection_requirements[1] = aura_of_protection_requirements[1] - 1
            if CHAMPION_LIST[4] == "Ranger":
                if power_opt_requirements[1] > 0:
                    power_opt_requirements[1] = power_opt_requirements[1] - 1
                if equip_iron_cast_arrows_requirements[1] > 0:
                    equip_iron_cast_arrows_requirements[1] = equip_iron_cast_arrows_requirements[1] - 1
                if equip_tracker_tipped_arrows_requirements[1] > 0:
                    equip_tracker_tipped_arrows_requirements[1] = equip_tracker_tipped_arrows_requirements[1] - 1
            if CHAMPION_LIST[4] == "Thunderous Apprentice":
                if crashing_boom_requirements[1] > 0:
                    crashing_boom_requirements[1] = crashing_boom_requirements[1] - 1
                if thunderous_vigor_requirements[1] > 0:
                    thunderous_vigor_requirements[1] = thunderous_vigor_requirements[1] - 1
            if CHAMPION_LIST[4] == "Earth Speaker":
                if rejuvenating_whirlpool_requirements[1] > 0:
                    rejuvenating_whirlpool_requirements[1] = rejuvenating_whirlpool_requirements[1] - 1
            if CHAMPION_LIST[4] == "Time Walker":
                if alter_time_requirements[1] > 0:
                    alter_time_requirements[1] = alter_time_requirements[1] - 1
            if CHAMPION_LIST[4] == "Field Medic":
                if perfected_herbal_tea_requirements[1] > 0:
                    perfected_herbal_tea_requirements[1] = perfected_herbal_tea_requirements[1] - 1
                if g3t_jaxd_requirements[1] > 0:
                    g3t_jaxd_requirements[1] = g3t_jaxd_requirements[1] - 1

    def attack_button(self):
        global attack1_button, attack1_button_details, attack2_button, attack2_button_details, attack3_button, attack3_button_details, attack4_button, attack4_button_details, back_button, \
            from_attack_button
        if current_turn == "C1":
            attack_button_champion1.destroy()
            special_button_champion1.destroy()
            rest_button_champion1.destroy()
            attack1_button = tk.Button(dungeon_game_frame, text=attack_button_text_list[0], width=50, height=4,
                                       command=lambda: self.champion_attacks(attack_button_text_list_temp[0]))
            attack1_button_details = tk.Button(dungeon_game_frame,
                                               text="{} Details".format(attack_button_text_list_temp[0]), width=38,
                                               height=1)
            attack2_button = tk.Button(dungeon_game_frame, text=attack_button_text_list[1], width=50, height=4,
                                       command=lambda: self.champion_attacks(attack_button_text_list_temp[1]))
            attack2_button_details = tk.Button(dungeon_game_frame,
                                               text="{} Details".format(attack_button_text_list_temp[1]), width=38,
                                               height=1)
            attack3_button = tk.Button(dungeon_game_frame, text=attack_button_text_list[2], width=50, height=4,
                                       command=lambda: self.champion_attacks(attack_button_text_list_temp[2]))
            attack3_button_details = tk.Button(dungeon_game_frame,
                                               text="{} Details".format(attack_button_text_list_temp[2]), width=38,
                                               height=1)
            attack4_button = tk.Button(dungeon_game_frame, text=attack_button_text_list[3], width=50, height=4,
                                       command=lambda: self.champion_attacks(attack_button_text_list_temp[3]))
            attack4_button_details = tk.Button(dungeon_game_frame,
                                               text="{} Details".format(attack_button_text_list_temp[3]), width=38,
                                               height=1)
            back_button = tk.Button(dungeon_game_frame, text="Back", command=self.player_combat_champion1)
            back_button.grid(row=20, column=2, pady=20)
            attack1_button.grid(row=18, column=1)
            attack1_button_details.grid(row=19, column=1)
            attack2_button.grid(row=18, column=3)
            attack2_button_details.grid(row=19, column=3)
            attack3_button.grid(row=20, column=1)
            attack3_button_details.grid(row=21, column=1)
            attack4_button.grid(row=20, column=3)
            attack4_button_details.grid(row=21, column=3)
            from_attack_button = 1
        if current_turn == "C2":
            attack_button_champion2.destroy()
            special_button_champion2.destroy()
            rest_button_champion2.destroy()
            attack1_button = tk.Button(dungeon_game_frame, text=attack_button_text_list[0], width=50, height=4,
                                       command=lambda: self.champion_attacks(attack_button_text_list_temp[0]))
            attack1_button_details = tk.Button(dungeon_game_frame,
                                               text="{} Details".format(attack_button_text_list_temp[0]), width=38,
                                               height=1)
            attack2_button = tk.Button(dungeon_game_frame, text=attack_button_text_list[1], width=50, height=4,
                                       command=lambda: self.champion_attacks(attack_button_text_list_temp[1]))
            attack2_button_details = tk.Button(dungeon_game_frame,
                                               text="{} Details".format(attack_button_text_list_temp[1]), width=38,
                                               height=1)
            attack3_button = tk.Button(dungeon_game_frame, text=attack_button_text_list[2], width=50, height=4,
                                       command=lambda: self.champion_attacks(attack_button_text_list_temp[2]))
            attack3_button_details = tk.Button(dungeon_game_frame,
                                               text="{} Details".format(attack_button_text_list_temp[2]), width=38,
                                               height=1)
            attack4_button = tk.Button(dungeon_game_frame, text=attack_button_text_list[3], width=50, height=4,
                                       command=lambda: self.champion_attacks(attack_button_text_list_temp[3]))
            attack4_button_details = tk.Button(dungeon_game_frame,
                                               text="{} Details".format(attack_button_text_list_temp[3]), width=38,
                                               height=1)
            back_button = tk.Button(dungeon_game_frame, text="Back", command=self.player_combat_champion2)
            back_button.grid(row=20, column=2, pady=20)
            attack1_button.grid(row=18, column=1)
            attack1_button_details.grid(row=19, column=1)
            attack2_button.grid(row=18, column=3)
            attack2_button_details.grid(row=19, column=3)
            attack3_button.grid(row=20, column=1)
            attack3_button_details.grid(row=21, column=1)
            attack4_button.grid(row=20, column=3)
            attack4_button_details.grid(row=21, column=3)
            from_attack_button = 1
        if current_turn == "C3":
            attack_button_champion3.destroy()
            special_button_champion3.destroy()
            rest_button_champion3.destroy()
            attack1_button = tk.Button(dungeon_game_frame, text=attack_button_text_list[0], width=50, height=4,
                                       command=lambda: self.champion_attacks(attack_button_text_list_temp[0]))
            attack1_button_details = tk.Button(dungeon_game_frame,
                                               text="{} Details".format(attack_button_text_list_temp[0]), width=38,
                                               height=1)
            attack2_button = tk.Button(dungeon_game_frame, text=attack_button_text_list[1], width=50, height=4,
                                       command=lambda: self.champion_attacks(attack_button_text_list_temp[1]))
            attack2_button_details = tk.Button(dungeon_game_frame,
                                               text="{} Details".format(attack_button_text_list_temp[1]), width=38,
                                               height=1)
            attack3_button = tk.Button(dungeon_game_frame, text=attack_button_text_list[2], width=50, height=4,
                                       command=lambda: self.champion_attacks(attack_button_text_list_temp[2]))
            attack3_button_details = tk.Button(dungeon_game_frame,
                                               text="{} Details".format(attack_button_text_list_temp[2]), width=38,
                                               height=1)
            attack4_button = tk.Button(dungeon_game_frame, text=attack_button_text_list[3], width=50, height=4,
                                       command=lambda: self.champion_attacks(attack_button_text_list_temp[3]))
            attack4_button_details = tk.Button(dungeon_game_frame,
                                               text="{} Details".format(attack_button_text_list_temp[3]), width=38,
                                               height=1)
            back_button = tk.Button(dungeon_game_frame, text="Back", command=self.player_combat_champion3)
            back_button.grid(row=20, column=2, pady=20)
            attack1_button.grid(row=18, column=1)
            attack1_button_details.grid(row=19, column=1)
            attack2_button.grid(row=18, column=3)
            attack2_button_details.grid(row=19, column=3)
            attack3_button.grid(row=20, column=1)
            attack3_button_details.grid(row=21, column=1)
            attack4_button.grid(row=20, column=3)
            attack4_button_details.grid(row=21, column=3)
            from_attack_button = 1
        if current_turn == "C4":
            attack_button_champion4.destroy()
            special_button_champion4.destroy()
            rest_button_champion4.destroy()
            attack1_button = tk.Button(dungeon_game_frame, text=attack_button_text_list[0], width=50, height=4,
                                       command=lambda: self.champion_attacks(attack_button_text_list_temp[0]))
            attack1_button_details = tk.Button(dungeon_game_frame,
                                               text="{} Details".format(attack_button_text_list_temp[0]), width=38,
                                               height=1)
            attack2_button = tk.Button(dungeon_game_frame, text=attack_button_text_list[1], width=50, height=4,
                                       command=lambda: self.champion_attacks(attack_button_text_list_temp[1]))
            attack2_button_details = tk.Button(dungeon_game_frame,
                                               text="{} Details".format(attack_button_text_list_temp[1]), width=38,
                                               height=1)
            attack3_button = tk.Button(dungeon_game_frame, text=attack_button_text_list[2], width=50, height=4,
                                       command=lambda: self.champion_attacks(attack_button_text_list_temp[2]))
            attack3_button_details = tk.Button(dungeon_game_frame,
                                               text="{} Details".format(attack_button_text_list_temp[2]), width=38,
                                               height=1)
            attack4_button = tk.Button(dungeon_game_frame, text=attack_button_text_list[3], width=50, height=4,
                                       command=lambda: self.champion_attacks(attack_button_text_list_temp[3]))
            attack4_button_details = tk.Button(dungeon_game_frame,
                                               text="{} Details".format(attack_button_text_list_temp[3]), width=38,
                                               height=1)
            back_button = tk.Button(dungeon_game_frame, text="Back", command=self.player_combat_champion4)
            back_button.grid(row=20, column=2, pady=20)
            attack1_button.grid(row=18, column=1)
            attack1_button_details.grid(row=19, column=1)
            attack2_button.grid(row=18, column=3)
            attack2_button_details.grid(row=19, column=3)
            attack3_button.grid(row=20, column=1)
            attack3_button_details.grid(row=21, column=1)
            attack4_button.grid(row=20, column=3)
            attack4_button_details.grid(row=21, column=3)
            from_attack_button = 1
        if current_turn == "C5":
            attack_button_champion5.destroy()
            special_button_champion5.destroy()
            rest_button_champion5.destroy()
            attack1_button = tk.Button(dungeon_game_frame, text=attack_button_text_list[0], width=50, height=4,
                                       command=lambda: self.champion_attacks(attack_button_text_list_temp[0]))
            attack1_button_details = tk.Button(dungeon_game_frame,
                                               text="{} Details".format(attack_button_text_list_temp[0]), width=38,
                                               height=1)
            attack2_button = tk.Button(dungeon_game_frame, text=attack_button_text_list[1], width=50, height=4,
                                       command=lambda: self.champion_attacks(attack_button_text_list_temp[1]))
            attack2_button_details = tk.Button(dungeon_game_frame,
                                               text="{} Details".format(attack_button_text_list_temp[1]), width=38,
                                               height=1)
            attack3_button = tk.Button(dungeon_game_frame, text=attack_button_text_list[2], width=50, height=4,
                                       command=lambda: self.champion_attacks(attack_button_text_list_temp[2]))
            attack3_button_details = tk.Button(dungeon_game_frame,
                                               text="{} Details".format(attack_button_text_list_temp[2]), width=38,
                                               height=1)
            attack4_button = tk.Button(dungeon_game_frame, text=attack_button_text_list[3], width=50, height=4,
                                       command=lambda: self.champion_attacks(attack_button_text_list_temp[3]))
            attack4_button_details = tk.Button(dungeon_game_frame,
                                               text="{} Details".format(attack_button_text_list_temp[3]), width=38,
                                               height=1)
            back_button = tk.Button(dungeon_game_frame, text="Back", command=self.player_combat_champion5)
            back_button.grid(row=20, column=2, pady=20)
            attack1_button.grid(row=18, column=1)
            attack1_button_details.grid(row=19, column=1)
            attack2_button.grid(row=18, column=3)
            attack2_button_details.grid(row=19, column=3)
            attack3_button.grid(row=20, column=1)
            attack3_button_details.grid(row=21, column=1)
            attack4_button.grid(row=20, column=3)
            attack4_button_details.grid(row=21, column=3)
            from_attack_button = 1

    def champion_attacks(self, ability_name):
        global attack_to_target, special_to_target, ability_data, champion1_rp, champion2_rp, champion3_rp, champion4_rp, champion5_rp
        attack_to_target = 1
        special_to_target = 0
        counter = 1
        damage_done = 0
        if ability_name == "Empty":
            return
        if ability_name == "Palm Strike":
            global palm_strike_requirements
            if palm_strike_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == MONK.title:
                        if counter == 1:
                            if palm_strike_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - palm_strike_requirements[0]
                                palm_strike_requirements[1] = palm_strike_requirements[2]
                                champion1_rp = champion1_rp + palm_strike_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = math.ceil((MONK.ap + champion1_small_external_buffs[0]) * champion1_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(MONK.ap + champion1_small_external_buffs[0])
                                ability_data = ["Palm Strike", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if palm_strike_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - palm_strike_requirements[0]
                                palm_strike_requirements[1] = palm_strike_requirements[2]
                                champion2_rp = champion2_rp + palm_strike_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = math.ceil((MONK.ap + champion2_small_external_buffs[0]) * champion2_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(MONK.ap + champion2_small_external_buffs[0])
                                ability_data = ["Palm Strike", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if palm_strike_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - palm_strike_requirements[0]
                                palm_strike_requirements[1] = palm_strike_requirements[2]
                                champion3_rp = champion3_rp + palm_strike_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = math.ceil((MONK.ap + champion3_small_external_buffs[0]) * champion3_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(MONK.ap + champion3_small_external_buffs[0])
                                ability_data = ["Palm Strike", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if palm_strike_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - palm_strike_requirements[0]
                                palm_strike_requirements[1] = palm_strike_requirements[2]
                                champion4_rp = champion4_rp + palm_strike_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = math.ceil((MONK.ap + champion4_small_external_buffs[0]) * champion4_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(MONK.ap + champion4_small_external_buffs[0])
                                ability_data = ["Palm Strike", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if palm_strike_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - palm_strike_requirements[0]
                                palm_strike_requirements[1] = palm_strike_requirements[2]
                                champion5_rp = champion5_rp + palm_strike_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = math.ceil((MONK.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(MONK.ap + champion5_small_external_buffs[0])
                                ability_data = ["Palm Strike", "enemy", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Leg Sweep":
            global leg_sweep_requirements
            if leg_sweep_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == MONK.title:
                        if counter == 1:
                            if counter == 1:
                                if leg_sweep_requirements[0] <= champion1_rp:
                                    champion1_rp = champion1_rp - leg_sweep_requirements[0]
                                    leg_sweep_requirements[1] = leg_sweep_requirements[2]
                                    champion1_rp = champion1_rp + leg_sweep_requirements[3]
                                    if len(champion1_big_external_buffs) != 1:
                                        damage_done = math.ceil((MONK.ap + champion1_small_external_buffs[0]) *
                                                       champion1_big_external_buffs[0])
                                    else:
                                        damage_done = math.ceil(MONK.ap + champion1_small_external_buffs[0])
                                    ability_data = ["Leg Sweep", "enemy", "1T", damage_done]
                                else:
                                    return
                            if counter == 2:
                                if leg_sweep_requirements[0] <= champion2_rp:
                                    champion2_rp = champion2_rp - leg_sweep_requirements[0]
                                    leg_sweep_requirements[1] = leg_sweep_requirements[2]
                                    champion2_rp = champion2_rp + leg_sweep_requirements[3]
                                    if len(champion2_big_external_buffs) != 1:
                                        damage_done = math.ceil((MONK.ap + champion2_small_external_buffs[0]) *
                                                       champion2_big_external_buffs[0])
                                    else:
                                        damage_done = math.ceil(MONK.ap + champion2_small_external_buffs[0])
                                    ability_data = ["Leg Sweep", "enemy", "1T", damage_done]
                                else:
                                    return
                            if counter == 3:
                                if leg_sweep_requirements[0] <= champion3_rp:
                                    champion3_rp = champion3_rp - leg_sweep_requirements[0]
                                    leg_sweep_requirements[1] = leg_sweep_requirements[2]
                                    champion3_rp = champion3_rp + leg_sweep_requirements[3]
                                    if len(champion3_big_external_buffs) != 1:
                                        damage_done = math.ceil((MONK.ap + champion3_small_external_buffs[0]) *
                                                       champion3_big_external_buffs[0])
                                    else:
                                        damage_done = math.ceil(MONK.ap + champion3_small_external_buffs[0])
                                    ability_data = ["Leg Sweep", "enemy", "1T", damage_done]
                                else:
                                    return
                            if counter == 4:
                                if leg_sweep_requirements[0] <= champion4_rp:
                                    champion4_rp = champion4_rp - leg_sweep_requirements[0]
                                    leg_sweep_requirements[1] = leg_sweep_requirements[2]
                                    champion4_rp = champion4_rp + leg_sweep_requirements[3]
                                    if len(champion4_big_external_buffs) != 1:
                                        damage_done = math.ceil((MONK.ap + champion4_small_external_buffs[0]) *
                                                       champion4_big_external_buffs[0])
                                    else:
                                        damage_done = math.ceil(MONK.ap + champion4_small_external_buffs[0])
                                    ability_data = ["Leg Sweep", "enemy", "1T", damage_done]
                                else:
                                    return
                            if counter == 5:
                                if leg_sweep_requirements[0] <= champion5_rp:
                                    champion5_rp = champion5_rp - leg_sweep_requirements[0]
                                    leg_sweep_requirements[1] = leg_sweep_requirements[2]
                                    champion5_rp = champion5_rp + leg_sweep_requirements[3]
                                    if len(champion5_big_external_buffs) != 1:
                                        damage_done = math.ceil((MONK.ap + champion5_small_external_buffs[0]) *
                                                       champion5_big_external_buffs[0])
                                    else:
                                        damage_done = math.ceil(MONK.ap + champion5_small_external_buffs[0])
                                    ability_data = ["Leg Sweep", "enemy", "1T", damage_done]
                                else:
                                    return
                        counter += 1
            else:
                return
        elif ability_name == "Bloodthirst":
            global bloodthirst_requirements
            if bloodthirst_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == BARBARIAN.title:
                        if counter == 1:
                            if bloodthirst_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - bloodthirst_requirements[0]
                                bloodthirst_requirements[1] = bloodthirst_requirements[2]
                                champion1_rp = champion1_rp + bloodthirst_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = math.ceil((BARBARIAN.ap + champion1_small_external_buffs[0]) * champion1_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(BARBARIAN.ap + champion1_small_external_buffs[0])
                                ability_data = ["Bloodthirst", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if bloodthirst_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - bloodthirst_requirements[0]
                                bloodthirst_requirements[1] = bloodthirst_requirements[2]
                                champion2_rp = champion2_rp + bloodthirst_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = math.ceil((BARBARIAN.ap + champion2_small_external_buffs[0]) * champion2_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(BARBARIAN.ap + champion2_small_external_buffs[0])
                                ability_data = ["Bloodthirst", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if bloodthirst_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - bloodthirst_requirements[0]
                                bloodthirst_requirements[1] = bloodthirst_requirements[2]
                                champion3_rp = champion3_rp + bloodthirst_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = math.ceil((BARBARIAN.ap + champion3_small_external_buffs[0]) * champion3_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(BARBARIAN.ap + champion3_small_external_buffs[0])
                                ability_data = ["Bloodthirst", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if bloodthirst_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - bloodthirst_requirements[0]
                                bloodthirst_requirements[1] = bloodthirst_requirements[2]
                                champion4_rp = champion4_rp + bloodthirst_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = math.ceil((BARBARIAN.ap + champion4_small_external_buffs[0]) * champion4_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(BARBARIAN.ap + champion4_small_external_buffs[0])
                                ability_data = ["Bloodthirst", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if bloodthirst_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - bloodthirst_requirements[0]
                                bloodthirst_requirements[1] = bloodthirst_requirements[2]
                                champion5_rp = champion5_rp + bloodthirst_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = math.ceil((BARBARIAN.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(BARBARIAN.ap + champion5_small_external_buffs[0])
                                ability_data = ["Bloodthirst", "enemy", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Pulverize":
            global pulverize_requirements
            if pulverize_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == BARBARIAN.title:
                        if counter == 1:
                            if pulverize_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - pulverize_requirements[0]
                                pulverize_requirements[1] = pulverize_requirements[2]
                                champion1_rp = champion1_rp + pulverize_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = math.ceil((BARBARIAN.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(BARBARIAN.ap + champion1_small_external_buffs[0])
                                ability_data = ["Pulverize", "enemy", "2T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if pulverize_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - pulverize_requirements[0]
                                pulverize_requirements[1] = pulverize_requirements[2]
                                champion2_rp = champion2_rp + pulverize_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = math.ceil((BARBARIAN.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(BARBARIAN.ap + champion2_small_external_buffs[0])
                                ability_data = ["Pulverize", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if pulverize_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - pulverize_requirements[0]
                                pulverize_requirements[1] = pulverize_requirements[2]
                                champion3_rp = champion3_rp + pulverize_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = math.ceil((BARBARIAN.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(BARBARIAN.ap + champion3_small_external_buffs[0])
                                ability_data = ["Pulverize", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if pulverize_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - pulverize_requirements[0]
                                pulverize_requirements[1] = pulverize_requirements[2]
                                champion4_rp = champion4_rp + pulverize_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = math.ceil((BARBARIAN.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(BARBARIAN.ap + champion4_small_external_buffs[0])
                                ability_data = ["Pulverize", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if pulverize_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - pulverize_requirements[0]
                                pulverize_requirements[1] = pulverize_requirements[2]
                                champion5_rp = champion5_rp + pulverize_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = math.ceil((BARBARIAN.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(BARBARIAN.ap + champion5_small_external_buffs[0])
                                ability_data = ["Pulverize", "enemy", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Shield Bash":
            global shield_bash_requirements
            if shield_bash_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == VETERAN_BODYGUARD.title:
                        if counter == 1:
                            if shield_bash_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - shield_bash_requirements[0]
                                shield_bash_requirements[1] = shield_bash_requirements[2]
                                champion1_rp = champion1_rp + shield_bash_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = math.ceil((VETERAN_BODYGUARD.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(VETERAN_BODYGUARD.ap + champion1_small_external_buffs[0])
                                ability_data = ["Shield Bash", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if shield_bash_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - shield_bash_requirements[0]
                                shield_bash_requirements[1] = shield_bash_requirements[2]
                                champion2_rp = champion2_rp + shield_bash_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = math.ceil((VETERAN_BODYGUARD.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(VETERAN_BODYGUARD.ap + champion2_small_external_buffs[0])
                                ability_data = ["Shield Bash", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if shield_bash_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - shield_bash_requirements[0]
                                shield_bash_requirements[1] = shield_bash_requirements[2]
                                champion3_rp = champion3_rp + shield_bash_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = math.ceil((VETERAN_BODYGUARD.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(VETERAN_BODYGUARD.ap + champion3_small_external_buffs[0])
                                ability_data = ["Shield Bash", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if shield_bash_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - shield_bash_requirements[0]
                                shield_bash_requirements[1] = shield_bash_requirements[2]
                                champion4_rp = champion4_rp + shield_bash_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = math.ceil((VETERAN_BODYGUARD.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(VETERAN_BODYGUARD.ap + champion4_small_external_buffs[0])
                                ability_data = ["Shield Bash", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if shield_bash_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - shield_bash_requirements[0]
                                shield_bash_requirements[1] = shield_bash_requirements[2]
                                champion5_rp = champion5_rp + shield_bash_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = math.ceil((VETERAN_BODYGUARD.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(VETERAN_BODYGUARD.ap + champion5_small_external_buffs[0])
                                ability_data = ["Shield Bash", "enemy", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Trainwreck":
            global trainwreck_requirements
            if trainwreck_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == VETERAN_BODYGUARD.title:
                        if counter == 1:
                            if trainwreck_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - trainwreck_requirements[0]
                                trainwreck_requirements[1] = trainwreck_requirements[2]
                                champion1_rp = champion1_rp + trainwreck_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = math.ceil((VETERAN_BODYGUARD.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(VETERAN_BODYGUARD.ap + champion1_small_external_buffs[0])
                                ability_data = ["Trainwreck", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if trainwreck_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - trainwreck_requirements[0]
                                trainwreck_requirements[1] = trainwreck_requirements[2]
                                champion2_rp = champion2_rp + trainwreck_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = math.ceil((VETERAN_BODYGUARD.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(VETERAN_BODYGUARD.ap + champion2_small_external_buffs[0])
                                ability_data = ["Trainwreck", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if trainwreck_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - trainwreck_requirements[0]
                                trainwreck_requirements[1] = trainwreck_requirements[2]
                                champion3_rp = champion3_rp + trainwreck_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = math.ceil((VETERAN_BODYGUARD.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(VETERAN_BODYGUARD.ap + champion3_small_external_buffs[0])
                                ability_data = ["Trainwreck", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if trainwreck_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - trainwreck_requirements[0]
                                trainwreck_requirements[1] = trainwreck_requirements[2]
                                champion4_rp = champion4_rp + trainwreck_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = math.ceil((VETERAN_BODYGUARD.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(VETERAN_BODYGUARD.ap + champion4_small_external_buffs[0])
                                ability_data = ["Trainwreck", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if trainwreck_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - trainwreck_requirements[0]
                                trainwreck_requirements[1] = trainwreck_requirements[2]
                                champion5_rp = champion5_rp + trainwreck_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = math.ceil((VETERAN_BODYGUARD.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(VETERAN_BODYGUARD.ap + champion5_small_external_buffs[0])
                                ability_data = ["Trainwreck", "enemy", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Pierce":
            global pierce_requirements
            if pierce_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == MASTER_FENCER.title:
                        if counter == 1:
                            if pierce_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - pierce_requirements[0]
                                pierce_requirements[1] = pierce_requirements[2]
                                champion1_rp = champion1_rp + pierce_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = math.ceil((MASTER_FENCER.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(MASTER_FENCER.ap + champion1_small_external_buffs[0])
                                ability_data = ["Pierce", "enemy", "2T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if pierce_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - pierce_requirements[0]
                                pierce_requirements[1] = pierce_requirements[2]
                                champion2_rp = champion2_rp + pierce_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = math.ceil((MASTER_FENCER.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(MASTER_FENCER.ap + champion2_small_external_buffs[0])
                                ability_data = ["Pierce", "enemy", "2T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if pierce_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - pierce_requirements[0]
                                pierce_requirements[1] = pierce_requirements[2]
                                champion3_rp = champion3_rp + pierce_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = math.ceil((MASTER_FENCER.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(MASTER_FENCER.ap + champion3_small_external_buffs[0])
                                ability_data = ["Pierce", "enemy", "2T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if pierce_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - pierce_requirements[0]
                                pierce_requirements[1] = pierce_requirements[2]
                                champion4_rp = champion4_rp + pierce_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = math.ceil((MASTER_FENCER.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(MASTER_FENCER.ap + champion4_small_external_buffs[0])
                                ability_data = ["Pierce", "enemy", "2T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if pierce_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - pierce_requirements[0]
                                pierce_requirements[1] = pierce_requirements[2]
                                champion5_rp = champion5_rp + pierce_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = math.ceil((MASTER_FENCER.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(MASTER_FENCER.ap + champion5_small_external_buffs[0])
                                ability_data = ["Pierce", "enemy", "2T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Disruptive Slash":
            global disruptive_slash_requirements
            if disruptive_slash_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == MASTER_FENCER.title:
                        if counter == 1:
                            if disruptive_slash_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - disruptive_slash_requirements[0]
                                disruptive_slash_requirements[1] = disruptive_slash_requirements[2]
                                champion1_rp = champion1_rp + disruptive_slash_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = math.ceil((MASTER_FENCER.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(MASTER_FENCER.ap + champion1_small_external_buffs[0])
                                ability_data = ["Disruptive Slash", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if disruptive_slash_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - disruptive_slash_requirements[0]
                                disruptive_slash_requirements[1] = disruptive_slash_requirements[2]
                                champion2_rp = champion2_rp + disruptive_slash_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = math.ceil((MASTER_FENCER.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(MASTER_FENCER.ap + champion2_small_external_buffs[0])
                                ability_data = ["Disruptive Slash", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if disruptive_slash_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - disruptive_slash_requirements[0]
                                disruptive_slash_requirements[1] = disruptive_slash_requirements[2]
                                champion3_rp = champion3_rp + disruptive_slash_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = math.ceil((MASTER_FENCER.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(MASTER_FENCER.ap + champion3_small_external_buffs[0])
                                ability_data = ["Disruptive Slash", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if disruptive_slash_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - disruptive_slash_requirements[0]
                                disruptive_slash_requirements[1] = disruptive_slash_requirements[2]
                                champion4_rp = champion4_rp + disruptive_slash_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = math.ceil((MASTER_FENCER.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(MASTER_FENCER.ap + champion4_small_external_buffs[0])
                                ability_data = ["Disruptive Slash", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if disruptive_slash_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - disruptive_slash_requirements[0]
                                disruptive_slash_requirements[1] = disruptive_slash_requirements[2]
                                champion5_rp = champion5_rp + disruptive_slash_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = math.ceil((MASTER_FENCER.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(MASTER_FENCER.ap + champion5_small_external_buffs[0])
                                ability_data = ["Disruptive Slash", "enemy", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Raging Blow":
            global raging_blow_requirements
            if raging_blow_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == BERSERKER.title:
                        if counter == 1:
                            if raging_blow_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - raging_blow_requirements[0]
                                raging_blow_requirements[1] = raging_blow_requirements[2]
                                champion1_rp = champion1_rp + raging_blow_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = math.ceil((BERSERKER.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(BERSERKER.ap + champion1_small_external_buffs[0])
                                ability_data = ["Raging Blow", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if raging_blow_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - raging_blow_requirements[0]
                                raging_blow_requirements[1] = raging_blow_requirements[2]
                                champion2_rp = champion2_rp + raging_blow_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = math.ceil((BERSERKER.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(BERSERKER.ap + champion2_small_external_buffs[0])
                                ability_data = ["Raging Blow", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if raging_blow_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - raging_blow_requirements[0]
                                raging_blow_requirements[1] = raging_blow_requirements[2]
                                champion3_rp = champion3_rp + raging_blow_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = math.ceil((BERSERKER.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(BERSERKER.ap + champion3_small_external_buffs[0])
                                ability_data = ["Raging Blow", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if raging_blow_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - raging_blow_requirements[0]
                                raging_blow_requirements[1] = raging_blow_requirements[2]
                                champion4_rp = champion4_rp + raging_blow_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = math.ceil((BERSERKER.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(BERSERKER.ap + champion4_small_external_buffs[0])
                                ability_data = ["Raging Blow", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if raging_blow_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - raging_blow_requirements[0]
                                raging_blow_requirements[1] = raging_blow_requirements[2]
                                champion5_rp = champion5_rp + raging_blow_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = math.ceil((BERSERKER.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(BERSERKER.ap + champion5_small_external_buffs[0])
                                ability_data = ["Raging Blow", "enemy", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Rampage":
            global rampage_requirements
            if rampage_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == BERSERKER.title:
                        if counter == 1:
                            if rampage_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - rampage_requirements[0]
                                rampage_requirements[1] = rampage_requirements[2]
                                champion1_rp = champion1_rp + rampage_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = math.ceil((BERSERKER.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(BERSERKER.ap + champion1_small_external_buffs[0])
                                ability_data = ["Rampage", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if rampage_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - rampage_requirements[0]
                                rampage_requirements[1] = rampage_requirements[2]
                                champion2_rp = champion2_rp + rampage_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = math.ceil((BERSERKER.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(BERSERKER.ap + champion2_small_external_buffs[0])
                                ability_data = ["Rampage", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if rampage_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - rampage_requirements[0]
                                rampage_requirements[1] = rampage_requirements[2]
                                champion3_rp = champion3_rp + rampage_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = math.ceil((BERSERKER.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(BERSERKER.ap + champion3_small_external_buffs[0])
                                ability_data = ["Rampage", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if rampage_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - rampage_requirements[0]
                                rampage_requirements[1] = rampage_requirements[2]
                                champion4_rp = champion4_rp + rampage_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = math.ceil((BERSERKER.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(BERSERKER.ap + champion4_small_external_buffs[0])
                                ability_data = ["Rampage", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if rampage_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - rampage_requirements[0]
                                rampage_requirements[1] = rampage_requirements[2]
                                champion5_rp = champion5_rp + rampage_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = math.ceil((BERSERKER.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(BERSERKER.ap + champion5_small_external_buffs[0])
                                ability_data = ["Rampage", "enemy", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Serrated Slash":
            global serrated_slash_requirements
            if serrated_slash_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == ROGUE.title:
                        if counter == 1:
                            if serrated_slash_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - serrated_slash_requirements[0]
                                serrated_slash_requirements[1] = serrated_slash_requirements[2]
                                champion1_rp = champion1_rp + serrated_slash_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = math.ceil((ROGUE.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(ROGUE.ap + champion1_small_external_buffs[0])
                                ability_data = ["Serrated Slash", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if serrated_slash_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - serrated_slash_requirements[0]
                                serrated_slash_requirements[1] = serrated_slash_requirements[2]
                                champion2_rp = champion2_rp + serrated_slash_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = math.ceil((ROGUE.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(ROGUE.ap + champion2_small_external_buffs[0])
                                ability_data = ["Serrated Slash", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if serrated_slash_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - serrated_slash_requirements[0]
                                serrated_slash_requirements[1] = serrated_slash_requirements[2]
                                champion3_rp = champion3_rp + serrated_slash_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = math.ceil((ROGUE.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(ROGUE.ap + champion3_small_external_buffs[0])
                                ability_data = ["Serrated Slash", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if serrated_slash_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - serrated_slash_requirements[0]
                                serrated_slash_requirements[1] = serrated_slash_requirements[2]
                                champion4_rp = champion4_rp + serrated_slash_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = math.ceil((ROGUE.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil( ROGUE.ap + champion4_small_external_buffs[0])
                                ability_data = ["Serrated Slash", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if serrated_slash_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - serrated_slash_requirements[0]
                                serrated_slash_requirements[1] = serrated_slash_requirements[2]
                                champion5_rp = champion5_rp + serrated_slash_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = math.ceil((ROGUE.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     ROGUE.ap + champion5_small_external_buffs[0])
                                ability_data = ["Serrated Slash", "enemy", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Eviscerate":
            global eviscerate_requirements
            if eviscerate_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == ROGUE.title:
                        if counter == 1:
                            if eviscerate_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - eviscerate_requirements[0]
                                eviscerate_requirements[1] = eviscerate_requirements[2]
                                champion1_rp = champion1_rp + eviscerate_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = math.ceil((ROGUE.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     ROGUE.ap + champion1_small_external_buffs[0])
                                ability_data = ["Eviscerate", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if eviscerate_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - eviscerate_requirements[0]
                                eviscerate_requirements[1] = eviscerate_requirements[2]
                                champion2_rp = champion2_rp + eviscerate_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = math.ceil((ROGUE.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     ROGUE.ap + champion2_small_external_buffs[0])
                                ability_data = ["Eviscerate", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if eviscerate_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - eviscerate_requirements[0]
                                eviscerate_requirements[1] = eviscerate_requirements[2]
                                champion3_rp = champion3_rp + eviscerate_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = math.ceil((ROGUE.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     ROGUE.ap + champion3_small_external_buffs[0])
                                ability_data = ["Eviscerate", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if eviscerate_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - eviscerate_requirements[0]
                                eviscerate_requirements[1] = eviscerate_requirements[2]
                                champion4_rp = champion4_rp + eviscerate_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = math.ceil((ROGUE.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     ROGUE.ap + champion4_small_external_buffs[0])
                                ability_data = ["Eviscerate", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if eviscerate_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - eviscerate_requirements[0]
                                eviscerate_requirements[1] = eviscerate_requirements[2]
                                champion5_rp = champion5_rp + eviscerate_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = math.ceil((ROGUE.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     ROGUE.ap + champion5_small_external_buffs[0])
                                ability_data = ["Eviscerate", "enemy", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Spear Thrust":
            global spear_thrust_requirements
            if spear_thrust_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == SURVIVALIST.title:
                        if counter == 1:
                            if spear_thrust_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - spear_thrust_requirements[0]
                                spear_thrust_requirements[1] = spear_thrust_requirements[2]
                                champion1_rp = champion1_rp + spear_thrust_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = math.ceil((SURVIVALIST.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     SURVIVALIST.ap + champion1_small_external_buffs[0])
                                ability_data = ["Spear Thrust", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if spear_thrust_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - spear_thrust_requirements[0]
                                spear_thrust_requirements[1] = spear_thrust_requirements[2]
                                champion2_rp = champion2_rp + spear_thrust_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = math.ceil((SURVIVALIST.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     SURVIVALIST.ap + champion2_small_external_buffs[0])
                                ability_data = ["Spear Thrust", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if spear_thrust_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - spear_thrust_requirements[0]
                                spear_thrust_requirements[1] = spear_thrust_requirements[2]
                                champion3_rp = champion3_rp + spear_thrust_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = math.ceil((SURVIVALIST.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     SURVIVALIST.ap + champion3_small_external_buffs[0])
                                ability_data = ["Spear Thrust", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if spear_thrust_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - spear_thrust_requirements[0]
                                spear_thrust_requirements[1] = spear_thrust_requirements[2]
                                champion4_rp = champion4_rp + spear_thrust_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = math.ceil((SURVIVALIST.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     SURVIVALIST.ap + champion4_small_external_buffs[0])
                                ability_data = ["Spear Thrust", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if spear_thrust_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - spear_thrust_requirements[0]
                                spear_thrust_requirements[1] = spear_thrust_requirements[2]
                                champion5_rp = champion5_rp + spear_thrust_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = math.ceil((SURVIVALIST.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     SURVIVALIST.ap + champion5_small_external_buffs[0])
                                ability_data = ["Spear Thrust", "enemy", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Scrap Bomb":
            global scrap_bomb_requirements
            if scrap_bomb_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == SURVIVALIST.title:
                        if counter == 1:
                            if scrap_bomb_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - scrap_bomb_requirements[0]
                                scrap_bomb_requirements[1] = scrap_bomb_requirements[2]
                                champion1_rp = champion1_rp + scrap_bomb_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = math.ceil((SURVIVALIST.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     SURVIVALIST.ap + champion1_small_external_buffs[0])
                                ability_data = ["Scrap Bomb", "enemy", "AOE", damage_done]
                            else:
                                return
                        if counter == 2:
                            if scrap_bomb_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - scrap_bomb_requirements[0]
                                scrap_bomb_requirements[1] = scrap_bomb_requirements[2]
                                champion2_rp = champion2_rp + scrap_bomb_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = math.ceil((SURVIVALIST.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     SURVIVALIST.ap + champion2_small_external_buffs[0])
                                ability_data = ["Scrap Bomb", "enemy", "AOE", damage_done]
                            else:
                                return
                        if counter == 3:
                            if scrap_bomb_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - scrap_bomb_requirements[0]
                                scrap_bomb_requirements[1] = scrap_bomb_requirements[2]
                                champion3_rp = champion3_rp + scrap_bomb_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = math.ceil((SURVIVALIST.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     SURVIVALIST.ap + champion3_small_external_buffs[0])
                                ability_data = ["Scrap Bomb", "enemy", "AOE", damage_done]
                            else:
                                return
                        if counter == 4:
                            if scrap_bomb_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - scrap_bomb_requirements[0]
                                scrap_bomb_requirements[1] = scrap_bomb_requirements[2]
                                champion4_rp = champion4_rp + scrap_bomb_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = math.ceil((SURVIVALIST.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     SURVIVALIST.ap + champion4_small_external_buffs[0])
                                ability_data = ["Scrap Bomb", "enemy", "AOE", damage_done]
                            else:
                                return
                        if counter == 5:
                            if scrap_bomb_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - scrap_bomb_requirements[0]
                                scrap_bomb_requirements[1] = scrap_bomb_requirements[2]
                                champion5_rp = champion5_rp + scrap_bomb_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = math.ceil((SURVIVALIST.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     SURVIVALIST.ap + champion5_small_external_buffs[0])
                                ability_data = ["Scrap Bomb", "enemy", "AOE", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Tactical Punch":
            global tactical_punch_requirements
            if tactical_punch_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == BRAWLIST.title:
                        if counter == 1:
                            if tactical_punch_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - tactical_punch_requirements[0]
                                tactical_punch_requirements[1] = tactical_punch_requirements[2]
                                champion1_rp = champion1_rp + tactical_punch_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = math.ceil((BRAWLIST.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(BRAWLIST.ap + champion1_small_external_buffs[0])
                                ability_data = ["Tactical Punch", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if tactical_punch_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - tactical_punch_requirements[0]
                                tactical_punch_requirements[1] = tactical_punch_requirements[2]
                                champion2_rp = champion2_rp + tactical_punch_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = math.ceil((BRAWLIST.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     BRAWLIST.ap + champion2_small_external_buffs[0])
                                ability_data = ["Tactical Punch", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if tactical_punch_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - tactical_punch_requirements[0]
                                tactical_punch_requirements[1] = tactical_punch_requirements[2]
                                champion3_rp = champion3_rp + tactical_punch_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = math.ceil((BRAWLIST.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     BRAWLIST.ap + champion3_small_external_buffs[0])
                                ability_data = ["Tactical Punch", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if tactical_punch_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - tactical_punch_requirements[0]
                                tactical_punch_requirements[1] = tactical_punch_requirements[2]
                                champion4_rp = champion4_rp + tactical_punch_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = math.ceil((BRAWLIST.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     BRAWLIST.ap + champion4_small_external_buffs[0])
                                ability_data = ["Tactical Punch", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if tactical_punch_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - tactical_punch_requirements[0]
                                tactical_punch_requirements[1] = tactical_punch_requirements[2]
                                champion5_rp = champion5_rp + tactical_punch_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = math.ceil((BRAWLIST.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     BRAWLIST.ap + champion5_small_external_buffs[0])
                                ability_data = ["Tactical Punch", "enemy", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Uppercut":
            global uppercut_requirements
            if uppercut_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == BRAWLIST.title:
                        if counter == 1:
                            if uppercut_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - uppercut_requirements[0]
                                uppercut_requirements[1] = uppercut_requirements[2]
                                champion1_rp = champion1_rp + uppercut_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = math.ceil((BRAWLIST.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     BRAWLIST.ap + champion1_small_external_buffs[0])
                                ability_data = ["Uppercut", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if uppercut_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - uppercut_requirements[0]
                                uppercut_requirements[1] = uppercut_requirements[2]
                                champion2_rp = champion2_rp + uppercut_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = math.ceil((BRAWLIST.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     BRAWLIST.ap + champion2_small_external_buffs[0])
                                ability_data = ["Uppercut", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if uppercut_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - uppercut_requirements[0]
                                uppercut_requirements[1] = uppercut_requirements[2]
                                champion3_rp = champion3_rp + uppercut_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = math.ceil((BRAWLIST.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     BRAWLIST.ap + champion3_small_external_buffs[0])
                                ability_data = ["Uppercut", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if uppercut_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - uppercut_requirements[0]
                                uppercut_requirements[1] = uppercut_requirements[2]
                                champion4_rp = champion4_rp + uppercut_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = math.ceil((BRAWLIST.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     BRAWLIST.ap + champion4_small_external_buffs[0])
                                ability_data = ["Uppercut", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if uppercut_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - uppercut_requirements[0]
                                uppercut_requirements[1] = uppercut_requirements[2]
                                champion5_rp = champion5_rp + uppercut_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = math.ceil((BRAWLIST.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     BRAWLIST.ap + champion5_small_external_buffs[0])
                                ability_data = ["Uppercut", "enemy", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Frost Bolt":
            global frost_bolt_requirements
            if frost_bolt_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == ACADEMIC_MAGE.title:
                        if counter == 1:
                            if frost_bolt_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - frost_bolt_requirements[0]
                                frost_bolt_requirements[1] = frost_bolt_requirements[2]
                                champion1_rp = champion1_rp + frost_bolt_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = math.ceil((ACADEMIC_MAGE.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     ACADEMIC_MAGE.ap + champion1_small_external_buffs[0])
                                ability_data = ["Frost Bolt", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if frost_bolt_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - frost_bolt_requirements[0]
                                frost_bolt_requirements[1] = frost_bolt_requirements[2]
                                champion2_rp = champion2_rp + frost_bolt_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = math.ceil((ACADEMIC_MAGE.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     ACADEMIC_MAGE.ap + champion2_small_external_buffs[0])
                                ability_data = ["Frost Bolt", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if frost_bolt_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - frost_bolt_requirements[0]
                                frost_bolt_requirements[1] = frost_bolt_requirements[2]
                                champion3_rp = champion3_rp + frost_bolt_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = math.ceil((ACADEMIC_MAGE.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     ACADEMIC_MAGE.ap + champion3_small_external_buffs[0])
                                ability_data = ["Frost Bolt", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if frost_bolt_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - frost_bolt_requirements[0]
                                frost_bolt_requirements[1] = frost_bolt_requirements[2]
                                champion4_rp = champion4_rp + frost_bolt_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = math.ceil((ACADEMIC_MAGE.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     ACADEMIC_MAGE.ap + champion4_small_external_buffs[0])
                                ability_data = ["Frost Bolt", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if frost_bolt_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - frost_bolt_requirements[0]
                                frost_bolt_requirements[1] = frost_bolt_requirements[2]
                                champion5_rp = champion5_rp + frost_bolt_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = math.ceil((ACADEMIC_MAGE.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     ACADEMIC_MAGE.ap + champion5_small_external_buffs[0])
                                ability_data = ["Frost Bolt", "enemy", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Fireball":
            global fireball_requirements
            if fireball_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == ACADEMIC_MAGE.title:
                        if counter == 1:
                            if fireball_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - fireball_requirements[0]
                                fireball_requirements[1] = fireball_requirements[2]
                                champion1_rp = champion1_rp + fireball_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = math.ceil((ACADEMIC_MAGE.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     ACADEMIC_MAGE.ap + champion1_small_external_buffs[0])
                                ability_data = ["Fireball", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if fireball_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - fireball_requirements[0]
                                fireball_requirements[1] = fireball_requirements[2]
                                champion2_rp = champion2_rp + fireball_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = math.ceil((ACADEMIC_MAGE.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     ACADEMIC_MAGE.ap + champion2_small_external_buffs[0])
                                ability_data = ["Fireball", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if fireball_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - fireball_requirements[0]
                                fireball_requirements[1] = fireball_requirements[2]
                                champion3_rp = champion3_rp + fireball_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = math.ceil((ACADEMIC_MAGE.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     ACADEMIC_MAGE.ap + champion3_small_external_buffs[0])
                                ability_data = ["Fireball", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if fireball_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - fireball_requirements[0]
                                fireball_requirements[1] = fireball_requirements[2]
                                champion4_rp = champion4_rp + fireball_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = math.ceil((ACADEMIC_MAGE.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     ACADEMIC_MAGE.ap + champion4_small_external_buffs[0])
                                ability_data = ["Fireball", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if fireball_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - fireball_requirements[0]
                                fireball_requirements[1] = fireball_requirements[2]
                                champion5_rp = champion5_rp + fireball_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = math.ceil((ACADEMIC_MAGE.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     ACADEMIC_MAGE.ap + champion5_small_external_buffs[0])
                                ability_data = ["Fireball", "enemy", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Venus-fly Snap":
            global venusfly_snap_requirements
            if venusfly_snap_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == DRUID.title:
                        if counter == 1:
                            if venusfly_snap_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - venusfly_snap_requirements[0]
                                venusfly_snap_requirements[1] = venusfly_snap_requirements[2]
                                champion1_rp = champion1_rp + venusfly_snap_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = math.ceil((DRUID.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     DRUID.ap + champion1_small_external_buffs[0])
                                ability_data = ["Venus-fly Snap", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if venusfly_snap_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - venusfly_snap_requirements[0]
                                venusfly_snap_requirements[1] = venusfly_snap_requirements[2]
                                champion2_rp = champion2_rp + venusfly_snap_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = math.ceil((DRUID.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     DRUID.ap + champion2_small_external_buffs[0])
                                ability_data = ["Venus-fly Snap", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if venusfly_snap_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - venusfly_snap_requirements[0]
                                venusfly_snap_requirements[1] = venusfly_snap_requirements[2]
                                champion3_rp = champion3_rp + venusfly_snap_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = math.ceil((DRUID.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     DRUID.ap + champion3_small_external_buffs[0])
                                ability_data = ["Venus-fly Snap", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if venusfly_snap_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - venusfly_snap_requirements[0]
                                venusfly_snap_requirements[1] = venusfly_snap_requirements[2]
                                champion4_rp = champion4_rp + venusfly_snap_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = math.ceil((DRUID.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     DRUID.ap + champion4_small_external_buffs[0])
                                ability_data = ["Venus-fly Snap", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if venusfly_snap_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - venusfly_snap_requirements[0]
                                venusfly_snap_requirements[1] = venusfly_snap_requirements[2]
                                champion5_rp = champion5_rp + venusfly_snap_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = math.ceil((DRUID.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     DRUID.ap + champion5_small_external_buffs[0])
                                ability_data = ["Venus-fly Snap", "enemy", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Vine-Swipe":
            global vine_swipe_requirements
            if vine_swipe_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == DRUID.title:
                        if counter == 1:
                            if vine_swipe_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - vine_swipe_requirements[0]
                                vine_swipe_requirements[1] = vine_swipe_requirements[2]
                                champion1_rp = champion1_rp + vine_swipe_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = math.ceil((DRUID.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     DRUID.ap + champion1_small_external_buffs[0])
                                ability_data = ["Vine-Swipe", "enemy", "2T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if vine_swipe_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - vine_swipe_requirements[0]
                                vine_swipe_requirements[1] = vine_swipe_requirements[2]
                                champion2_rp = champion2_rp + vine_swipe_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = math.ceil((DRUID.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     DRUID.ap + champion2_small_external_buffs[0])
                                ability_data = ["Vine-Swipe", "enemy", "2T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if vine_swipe_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - vine_swipe_requirements[0]
                                vine_swipe_requirements[1] = vine_swipe_requirements[2]
                                champion3_rp = champion3_rp + vine_swipe_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = math.ceil((DRUID.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     DRUID.ap + champion3_small_external_buffs[0])
                                ability_data = ["Vine-Swipe", "enemy", "2T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if vine_swipe_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - vine_swipe_requirements[0]
                                vine_swipe_requirements[1] = vine_swipe_requirements[2]
                                champion4_rp = champion4_rp + vine_swipe_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = math.ceil((DRUID.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     DRUID.ap + champion4_small_external_buffs[0])
                                ability_data = ["Vine-Swipe", "enemy", "2T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if vine_swipe_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - vine_swipe_requirements[0]
                                vine_swipe_requirements[1] = vine_swipe_requirements[2]
                                champion5_rp = champion5_rp + vine_swipe_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = math.ceil((DRUID.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     DRUID.ap + champion5_small_external_buffs[0])
                                ability_data = ["Vine-Swipe", "enemy", "2T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Black Bolt":
            global black_bolt_requirements
            if black_bolt_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == WARLOCK.title:
                        if counter == 1:
                            if black_bolt_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - black_bolt_requirements[0]
                                black_bolt_requirements[1] = black_bolt_requirements[2]
                                champion1_rp = champion1_rp + black_bolt_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = math.ceil((WARLOCK.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     WARLOCK.ap + champion1_small_external_buffs[0])
                                ability_data = ["Black Bolt", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if black_bolt_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - black_bolt_requirements[0]
                                black_bolt_requirements[1] = black_bolt_requirements[2]
                                champion2_rp = champion2_rp + black_bolt_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = math.ceil((WARLOCK.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     WARLOCK.ap + champion2_small_external_buffs[0])
                                ability_data = ["Black Bolt", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if black_bolt_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - black_bolt_requirements[0]
                                black_bolt_requirements[1] = black_bolt_requirements[2]
                                champion3_rp = champion3_rp + black_bolt_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = math.ceil((WARLOCK.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     WARLOCK.ap + champion3_small_external_buffs[0])
                                ability_data = ["Black Bolt", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if black_bolt_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - black_bolt_requirements[0]
                                black_bolt_requirements[1] = black_bolt_requirements[2]
                                champion4_rp = champion4_rp + black_bolt_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = math.ceil((WARLOCK.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     WARLOCK.ap + champion4_small_external_buffs[0])
                                ability_data = ["Black Bolt", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if black_bolt_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - black_bolt_requirements[0]
                                black_bolt_requirements[1] = black_bolt_requirements[2]
                                champion5_rp = champion5_rp + black_bolt_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = math.ceil((WARLOCK.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     WARLOCK.ap + champion5_small_external_buffs[0])
                                ability_data = ["Black Bolt", "enemy", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Void Infusion":
            global void_infusion_requirements
            if void_infusion_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == WARLOCK.title:
                        if counter == 1:
                            if void_infusion_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - void_infusion_requirements[0]
                                void_infusion_requirements[1] = void_infusion_requirements[2]
                                champion1_rp = champion1_rp + void_infusion_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = math.ceil((WARLOCK.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     WARLOCK.ap + champion1_small_external_buffs[0])
                                ability_data = ["Void Infusion", "self", "1T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if void_infusion_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - void_infusion_requirements[0]
                                void_infusion_requirements[1] = void_infusion_requirements[2]
                                champion2_rp = champion2_rp + void_infusion_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = math.ceil((WARLOCK.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     WARLOCK.ap + champion2_small_external_buffs[0])
                                ability_data = ["Void Infusion", "self", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if void_infusion_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - void_infusion_requirements[0]
                                void_infusion_requirements[1] = void_infusion_requirements[2]
                                champion3_rp = champion3_rp + void_infusion_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = math.ceil((WARLOCK.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     WARLOCK.ap + champion3_small_external_buffs[0])
                                ability_data = ["Void Infusion", "self", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if void_infusion_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - void_infusion_requirements[0]
                                void_infusion_requirements[1] = void_infusion_requirements[2]
                                champion4_rp = champion4_rp + void_infusion_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = math.ceil((WARLOCK.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     WARLOCK.ap + champion4_small_external_buffs[0])
                                ability_data = ["Void Infusion", "self", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if void_infusion_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - void_infusion_requirements[0]
                                void_infusion_requirements[1] = void_infusion_requirements[2]
                                champion5_rp = champion5_rp + void_infusion_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = math.ceil((WARLOCK.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     WARLOCK.ap + champion5_small_external_buffs[0])
                                ability_data = ["Void Infusion", "self", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Drain Life":
            global drain_life_requirements
            if drain_life_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == BLOODMANCER.title:
                        if counter == 1:
                            if drain_life_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - drain_life_requirements[0]
                                drain_life_requirements[1] = drain_life_requirements[2]
                                champion1_rp = champion1_rp + drain_life_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = math.ceil((BLOODMANCER.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     BLOODMANCER.ap + champion1_small_external_buffs[0])
                                ability_data = ["Drain Life", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if drain_life_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - drain_life_requirements[0]
                                drain_life_requirements[1] = drain_life_requirements[2]
                                champion2_rp = champion2_rp + drain_life_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = math.ceil((BLOODMANCER.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     BLOODMANCER.ap + champion2_small_external_buffs[0])
                                ability_data = ["Drain Life", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if drain_life_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - drain_life_requirements[0]
                                drain_life_requirements[1] = drain_life_requirements[2]
                                champion3_rp = champion3_rp + drain_life_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = math.ceil((BLOODMANCER.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     BLOODMANCER.ap + champion3_small_external_buffs[0])
                                ability_data = ["Drain Life", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if drain_life_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - drain_life_requirements[0]
                                drain_life_requirements[1] = drain_life_requirements[2]
                                champion4_rp = champion4_rp + drain_life_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = math.ceil((BLOODMANCER.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     BLOODMANCER.ap + champion4_small_external_buffs[0])
                                ability_data = ["Drain Life", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if drain_life_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - drain_life_requirements[0]
                                drain_life_requirements[1] = drain_life_requirements[2]
                                champion5_rp = champion5_rp + drain_life_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = math.ceil((BLOODMANCER.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     BLOODMANCER.ap + champion5_small_external_buffs[0])
                                ability_data = ["Drain Life", "enemy", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Blood Spike":
            global blood_spike_requirements
            if blood_spike_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == BLOODMANCER.title:
                        if counter == 1:
                            if blood_spike_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - blood_spike_requirements[0]
                                blood_spike_requirements[1] = blood_spike_requirements[2]
                                champion1_rp = champion1_rp + blood_spike_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = math.ceil((BLOODMANCER.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     BLOODMANCER.ap + champion1_small_external_buffs[0])
                                ability_data = ["Blood Spike", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if blood_spike_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - blood_spike_requirements[0]
                                blood_spike_requirements[1] = blood_spike_requirements[2]
                                champion2_rp = champion2_rp + blood_spike_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = math.ceil((BLOODMANCER.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     BLOODMANCER.ap + champion2_small_external_buffs[0])
                                ability_data = ["Blood Spike", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if blood_spike_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - blood_spike_requirements[0]
                                blood_spike_requirements[1] = blood_spike_requirements[2]
                                champion3_rp = champion3_rp + blood_spike_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = math.ceil((BLOODMANCER.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     BLOODMANCER.ap + champion3_small_external_buffs[0])
                                ability_data = ["Blood Spike", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if blood_spike_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - blood_spike_requirements[0]
                                blood_spike_requirements[1] = blood_spike_requirements[2]
                                champion4_rp = champion4_rp + blood_spike_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = math.ceil((BLOODMANCER.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     BLOODMANCER.ap + champion4_small_external_buffs[0])
                                ability_data = ["Blood Spike", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if blood_spike_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - blood_spike_requirements[0]
                                blood_spike_requirements[1] = blood_spike_requirements[2]
                                champion5_rp = champion5_rp + blood_spike_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = math.ceil((BLOODMANCER.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     BLOODMANCER.ap + champion5_small_external_buffs[0])
                                ability_data = ["Blood Spike", "enemy", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Overhand Justice":
            global overhand_justice_requirements
            if overhand_justice_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == PALADIN.title:
                        if counter == 1:
                            if overhand_justice_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - overhand_justice_requirements[0]
                                overhand_justice_requirements[1] = overhand_justice_requirements[2]
                                champion1_rp = champion1_rp + overhand_justice_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = math.ceil((PALADIN.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     PALADIN.ap + champion1_small_external_buffs[0])
                                ability_data = ["Overhand Justice", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if overhand_justice_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - overhand_justice_requirements[0]
                                overhand_justice_requirements[1] = overhand_justice_requirements[2]
                                champion2_rp = champion2_rp + overhand_justice_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = math.ceil((PALADIN.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     PALADIN.ap + champion2_small_external_buffs[0])
                                ability_data = ["Overhand Justice", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if overhand_justice_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - overhand_justice_requirements[0]
                                overhand_justice_requirements[1] = overhand_justice_requirements[2]
                                champion3_rp = champion3_rp + overhand_justice_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = math.ceil((PALADIN.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     PALADIN.ap + champion3_small_external_buffs[0])
                                ability_data = ["Overhand Justice", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if overhand_justice_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - overhand_justice_requirements[0]
                                overhand_justice_requirements[1] = overhand_justice_requirements[2]
                                champion4_rp = champion4_rp + overhand_justice_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = math.ceil((PALADIN.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     PALADIN.ap + champion4_small_external_buffs[0])
                                ability_data = ["Overhand Justice", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if overhand_justice_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - overhand_justice_requirements[0]
                                overhand_justice_requirements[1] = overhand_justice_requirements[2]
                                champion5_rp = champion5_rp + overhand_justice_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = math.ceil((PALADIN.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     PALADIN.ap + champion5_small_external_buffs[0])
                                ability_data = ["Overhand Justice", "enemy", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Righteous Blow":
            global righteous_blow_requirements
            if righteous_blow_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == PALADIN.title:
                        if counter == 1:
                            if righteous_blow_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - righteous_blow_requirements[0]
                                righteous_blow_requirements[1] = righteous_blow_requirements[2]
                                champion1_rp = champion1_rp + righteous_blow_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = math.ceil((PALADIN.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     PALADIN.ap + champion1_small_external_buffs[0])
                                ability_data = ["Righteous Blow", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if righteous_blow_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - righteous_blow_requirements[0]
                                righteous_blow_requirements[1] = righteous_blow_requirements[2]
                                champion2_rp = champion2_rp + righteous_blow_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = math.ceil((PALADIN.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     PALADIN.ap + champion2_small_external_buffs[0])
                                ability_data = ["Righteous Blow", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if righteous_blow_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - righteous_blow_requirements[0]
                                righteous_blow_requirements[1] = righteous_blow_requirements[2]
                                champion3_rp = champion3_rp + righteous_blow_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = math.ceil((PALADIN.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     PALADIN.ap + champion3_small_external_buffs[0])
                                ability_data = ["Righteous Blow", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if righteous_blow_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - righteous_blow_requirements[0]
                                righteous_blow_requirements[1] = righteous_blow_requirements[2]
                                champion4_rp = champion4_rp + righteous_blow_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = math.ceil((PALADIN.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     PALADIN.ap + champion4_small_external_buffs[0])
                                ability_data = ["Righteous Blow", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if righteous_blow_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - righteous_blow_requirements[0]
                                righteous_blow_requirements[1] = righteous_blow_requirements[2]
                                champion5_rp = champion5_rp + righteous_blow_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = math.ceil((PALADIN.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     PALADIN.ap + champion5_small_external_buffs[0])
                                ability_data = ["Righteous Blow", "enemy", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Steady Shot":
            global steady_shot_requirements
            if steady_shot_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == CASTLE_RANGER.title:
                        if counter == 1:
                            if steady_shot_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - steady_shot_requirements[0]
                                steady_shot_requirements[1] = steady_shot_requirements[2]
                                champion1_rp = champion1_rp + steady_shot_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = math.ceil((CASTLE_RANGER.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     CASTLE_RANGER.ap + champion1_small_external_buffs[0])
                                ability_data = ["Steady Shot", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if steady_shot_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - steady_shot_requirements[0]
                                steady_shot_requirements[1] = steady_shot_requirements[2]
                                champion2_rp = champion2_rp + steady_shot_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = math.ceil((CASTLE_RANGER.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     CASTLE_RANGER.ap + champion2_small_external_buffs[0])
                                ability_data = ["Steady Shot", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if steady_shot_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - steady_shot_requirements[0]
                                steady_shot_requirements[1] = steady_shot_requirements[2]
                                champion3_rp = champion3_rp + steady_shot_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = math.ceil((CASTLE_RANGER.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     CASTLE_RANGER.ap + champion3_small_external_buffs[0])
                                ability_data = ["Steady Shot", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if steady_shot_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - steady_shot_requirements[0]
                                steady_shot_requirements[1] = steady_shot_requirements[2]
                                champion4_rp = champion4_rp + steady_shot_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = math.ceil((CASTLE_RANGER.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     CASTLE_RANGER.ap + champion4_small_external_buffs[0])
                                ability_data = ["Steady Shot", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if steady_shot_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - steady_shot_requirements[0]
                                steady_shot_requirements[1] = steady_shot_requirements[2]
                                champion5_rp = champion5_rp + steady_shot_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = math.ceil((CASTLE_RANGER.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     CASTLE_RANGER.ap + champion5_small_external_buffs[0])
                                ability_data = ["Steady Shot", "enemy", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Power Opt":
            global power_opt_requirements
            if power_opt_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == CASTLE_RANGER.title:
                        if counter == 1:
                            if power_opt_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - power_opt_requirements[0]
                                power_opt_requirements[1] = power_opt_requirements[2]
                                champion1_rp = champion1_rp + power_opt_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = math.ceil((CASTLE_RANGER.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     CASTLE_RANGER.ap + champion1_small_external_buffs[0])
                                ability_data = ["Power Opt", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if power_opt_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - power_opt_requirements[0]
                                power_opt_requirements[1] = power_opt_requirements[2]
                                champion2_rp = champion2_rp + power_opt_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = math.ceil((CASTLE_RANGER.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     CASTLE_RANGER.ap + champion2_small_external_buffs[0])
                                ability_data = ["Power Opt", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if power_opt_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - power_opt_requirements[0]
                                power_opt_requirements[1] = power_opt_requirements[2]
                                champion3_rp = champion3_rp + power_opt_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = math.ceil((CASTLE_RANGER.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     CASTLE_RANGER.ap + champion3_small_external_buffs[0])
                                ability_data = ["Power Opt", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if power_opt_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - power_opt_requirements[0]
                                power_opt_requirements[1] = power_opt_requirements[2]
                                champion4_rp = champion4_rp + power_opt_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = math.ceil((CASTLE_RANGER.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     CASTLE_RANGER.ap + champion4_small_external_buffs[0])
                                ability_data = ["Power Opt", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if power_opt_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - power_opt_requirements[0]
                                power_opt_requirements[1] = power_opt_requirements[2]
                                champion5_rp = champion5_rp + power_opt_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = math.ceil((CASTLE_RANGER.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     CASTLE_RANGER.ap + champion5_small_external_buffs[0])
                                ability_data = ["Power Opt", "enemy", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Lightning Bolt":
            global lightning_bolt_requirements
            if lightning_bolt_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == THUNDER_APPRENTICE.title:
                        if counter == 1:
                            if lightning_bolt_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - lightning_bolt_requirements[0]
                                lightning_bolt_requirements[1] = lightning_bolt_requirements[2]
                                champion1_rp = champion1_rp + lightning_bolt_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = math.ceil((THUNDER_APPRENTICE.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     THUNDER_APPRENTICE.ap + champion1_small_external_buffs[0])
                                ability_data = ["Lightning Bolt", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if lightning_bolt_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - lightning_bolt_requirements[0]
                                lightning_bolt_requirements[1] = lightning_bolt_requirements[2]
                                champion2_rp = champion2_rp + lightning_bolt_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = math.ceil((THUNDER_APPRENTICE.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     THUNDER_APPRENTICE.ap + champion2_small_external_buffs[0])
                                ability_data = ["Lightning Bolt", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if lightning_bolt_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - lightning_bolt_requirements[0]
                                lightning_bolt_requirements[1] = lightning_bolt_requirements[2]
                                champion3_rp = champion3_rp + lightning_bolt_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = math.ceil((THUNDER_APPRENTICE.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     THUNDER_APPRENTICE.ap + champion3_small_external_buffs[0])
                                ability_data = ["Lightning Bolt", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if lightning_bolt_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - lightning_bolt_requirements[0]
                                lightning_bolt_requirements[1] = lightning_bolt_requirements[2]
                                champion4_rp = champion4_rp + lightning_bolt_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = math.ceil((THUNDER_APPRENTICE.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     THUNDER_APPRENTICE.ap + champion4_small_external_buffs[0])
                                ability_data = ["Lightning Bolt", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if lightning_bolt_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - lightning_bolt_requirements[0]
                                lightning_bolt_requirements[1] = lightning_bolt_requirements[2]
                                champion5_rp = champion5_rp + lightning_bolt_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = math.ceil((THUNDER_APPRENTICE.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     THUNDER_APPRENTICE.ap + champion5_small_external_buffs[0])
                                ability_data = ["Lightning Bolt", "enemy", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Chain Lightning":
            global chain_lightning_requirements
            if chain_lightning_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == THUNDER_APPRENTICE.title:
                        if counter == 1:
                            if chain_lightning_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - chain_lightning_requirements[0]
                                chain_lightning_requirements[1] = chain_lightning_requirements[2]
                                champion1_rp = champion1_rp + chain_lightning_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = math.ceil((THUNDER_APPRENTICE.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     THUNDER_APPRENTICE.ap + champion1_small_external_buffs[0])
                                ability_data = ["Chain Lightning", "enemy", "AOE", damage_done]
                            else:
                                return
                        if counter == 2:
                            if chain_lightning_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - chain_lightning_requirements[0]
                                chain_lightning_requirements[1] = chain_lightning_requirements[2]
                                champion2_rp = champion2_rp + chain_lightning_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = math.ceil((THUNDER_APPRENTICE.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     THUNDER_APPRENTICE.ap + champion2_small_external_buffs[0])
                                ability_data = ["Chain Lightning", "enemy", "AOE", damage_done]
                            else:
                                return
                        if counter == 3:
                            if chain_lightning_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - chain_lightning_requirements[0]
                                chain_lightning_requirements[1] = chain_lightning_requirements[2]
                                champion3_rp = champion3_rp + chain_lightning_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = math.ceil((THUNDER_APPRENTICE.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     THUNDER_APPRENTICE.ap + champion3_small_external_buffs[0])
                                ability_data = ["Chain Lightning", "enemy", "AOE", damage_done]
                            else:
                                return
                        if counter == 4:
                            if chain_lightning_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - chain_lightning_requirements[0]
                                chain_lightning_requirements[1] = chain_lightning_requirements[2]
                                champion4_rp = champion4_rp + chain_lightning_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = math.ceil((THUNDER_APPRENTICE.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     THUNDER_APPRENTICE.ap + champion4_small_external_buffs[0])
                                ability_data = ["Chain Lightning", "enemy", "AOE", damage_done]
                            else:
                                return
                        if counter == 5:
                            if chain_lightning_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - chain_lightning_requirements[0]
                                chain_lightning_requirements[1] = chain_lightning_requirements[2]
                                champion5_rp = champion5_rp + chain_lightning_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = math.ceil((THUNDER_APPRENTICE.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     THUNDER_APPRENTICE.ap + champion5_small_external_buffs[0])
                                ability_data = ["Chain Lightning", "enemy", "AOE", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Rock Barrage":
            global rock_barrage_requirements
            if rock_barrage_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == EARTH_SPEAKER.title:
                        if counter == 1:
                            if rock_barrage_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - rock_barrage_requirements[0]
                                rock_barrage_requirements[1] = rock_barrage_requirements[2]
                                champion1_rp = champion1_rp + rock_barrage_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = math.ceil((EARTH_SPEAKER.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     EARTH_SPEAKER.ap + champion1_small_external_buffs[0])
                                ability_data = ["Rock Barrage", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if rock_barrage_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - rock_barrage_requirements[0]
                                rock_barrage_requirements[1] = rock_barrage_requirements[2]
                                champion2_rp = champion2_rp + rock_barrage_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = math.ceil((EARTH_SPEAKER.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     EARTH_SPEAKER.ap + champion2_small_external_buffs[0])
                                ability_data = ["Rock Barrage", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if rock_barrage_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - rock_barrage_requirements[0]
                                rock_barrage_requirements[1] = rock_barrage_requirements[2]
                                champion3_rp = champion3_rp + rock_barrage_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = math.ceil((EARTH_SPEAKER.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     EARTH_SPEAKER.ap + champion3_small_external_buffs[0])
                                ability_data = ["Rock Barrage", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if rock_barrage_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - rock_barrage_requirements[0]
                                rock_barrage_requirements[1] = rock_barrage_requirements[2]
                                champion4_rp = champion4_rp + rock_barrage_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = math.ceil((EARTH_SPEAKER.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     EARTH_SPEAKER.ap + champion4_small_external_buffs[0])
                                ability_data = ["Rock Barrage", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if rock_barrage_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - rock_barrage_requirements[0]
                                rock_barrage_requirements[1] = rock_barrage_requirements[2]
                                champion5_rp = champion5_rp + rock_barrage_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = math.ceil((EARTH_SPEAKER.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     EARTH_SPEAKER.ap + champion5_small_external_buffs[0])
                                ability_data = ["Rock Barrage", "enemy", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Shimmering Bolt":
            global shimmering_bolt_requirements
            if shimmering_bolt_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == PRIEST_OF_THE_DEVOTED.title:
                        if counter == 1:
                            if shimmering_bolt_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - shimmering_bolt_requirements[0]
                                shimmering_bolt_requirements[1] = shimmering_bolt_requirements[2]
                                champion1_rp = champion1_rp + shimmering_bolt_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = math.ceil((PRIEST_OF_THE_DEVOTED.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     PRIEST_OF_THE_DEVOTED.ap + champion1_small_external_buffs[0])
                                ability_data = ["Shimmering Bolt", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if shimmering_bolt_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - shimmering_bolt_requirements[0]
                                shimmering_bolt_requirements[1] = shimmering_bolt_requirements[2]
                                champion2_rp = champion2_rp + shimmering_bolt_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = math.ceil((PRIEST_OF_THE_DEVOTED.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     PRIEST_OF_THE_DEVOTED.ap + champion2_small_external_buffs[0])
                                ability_data = ["Shimmering Bolt", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if shimmering_bolt_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - shimmering_bolt_requirements[0]
                                shimmering_bolt_requirements[1] = shimmering_bolt_requirements[2]
                                champion3_rp = champion3_rp + shimmering_bolt_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = math.ceil((PRIEST_OF_THE_DEVOTED.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     PRIEST_OF_THE_DEVOTED.ap + champion3_small_external_buffs[0])
                                ability_data = ["Shimmering Bolt", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if shimmering_bolt_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - shimmering_bolt_requirements[0]
                                shimmering_bolt_requirements[1] = shimmering_bolt_requirements[2]
                                champion4_rp = champion4_rp + shimmering_bolt_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = math.ceil((PRIEST_OF_THE_DEVOTED.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     PRIEST_OF_THE_DEVOTED.ap + champion4_small_external_buffs[0])
                                ability_data = ["Shimmering Bolt", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if shimmering_bolt_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - shimmering_bolt_requirements[0]
                                shimmering_bolt_requirements[1] = shimmering_bolt_requirements[2]
                                champion5_rp = champion5_rp + shimmering_bolt_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = math.ceil((PRIEST_OF_THE_DEVOTED.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     PRIEST_OF_THE_DEVOTED.ap + champion5_small_external_buffs[0])
                                ability_data = ["Shimmering Bolt", "enemy", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Divine Smite":
            global divine_smite_requirements
            if divine_smite_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == PRIEST_OF_THE_DEVOTED.title:
                        if counter == 1:
                            if divine_smite_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - divine_smite_requirements[0]
                                divine_smite_requirements[1] = divine_smite_requirements[2]
                                champion1_rp = champion1_rp + divine_smite_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = math.ceil((PRIEST_OF_THE_DEVOTED.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     PRIEST_OF_THE_DEVOTED.ap + champion1_small_external_buffs[0])
                                ability_data = ["Divine Smite", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if divine_smite_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - divine_smite_requirements[0]
                                divine_smite_requirements[1] = divine_smite_requirements[2]
                                champion2_rp = champion2_rp + divine_smite_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = math.ceil((PRIEST_OF_THE_DEVOTED.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     PRIEST_OF_THE_DEVOTED.ap + champion2_small_external_buffs[0])
                                ability_data = ["Divine Smite", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if divine_smite_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - divine_smite_requirements[0]
                                divine_smite_requirements[1] = divine_smite_requirements[2]
                                champion3_rp = champion3_rp + divine_smite_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = math.ceil((PRIEST_OF_THE_DEVOTED.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     PRIEST_OF_THE_DEVOTED.ap + champion3_small_external_buffs[0])
                                ability_data = ["Divine Smite", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if divine_smite_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - divine_smite_requirements[0]
                                divine_smite_requirements[1] = divine_smite_requirements[2]
                                champion4_rp = champion4_rp + divine_smite_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = math.ceil((PRIEST_OF_THE_DEVOTED.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     PRIEST_OF_THE_DEVOTED.ap + champion4_small_external_buffs[0])
                                ability_data = ["Divine Smite", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if divine_smite_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - divine_smite_requirements[0]
                                divine_smite_requirements[1] = divine_smite_requirements[2]
                                champion5_rp = champion5_rp + divine_smite_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = math.ceil((PRIEST_OF_THE_DEVOTED.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     PRIEST_OF_THE_DEVOTED.ap + champion5_small_external_buffs[0])
                                ability_data = ["Divine Smite", "enemy", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Cybernetic Blast":
            global cybernetic_blast_requirements
            if cybernetic_blast_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == TIME_WALKER.title:
                        if counter == 1:
                            if cybernetic_blast_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - cybernetic_blast_requirements[0]
                                cybernetic_blast_requirements[1] = cybernetic_blast_requirements[2]
                                champion1_rp = champion1_rp + cybernetic_blast_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = math.ceil((TIME_WALKER.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     TIME_WALKER.ap + champion1_small_external_buffs[0])
                                ability_data = ["Cybernetic Blast", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if cybernetic_blast_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - cybernetic_blast_requirements[0]
                                cybernetic_blast_requirements[1] = cybernetic_blast_requirements[2]
                                champion2_rp = champion2_rp + cybernetic_blast_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = math.ceil((TIME_WALKER.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     TIME_WALKER.ap + champion2_small_external_buffs[0])
                                ability_data = ["Cybernetic Blast", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if cybernetic_blast_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - cybernetic_blast_requirements[0]
                                cybernetic_blast_requirements[1] = cybernetic_blast_requirements[2]
                                champion3_rp = champion3_rp + cybernetic_blast_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = math.ceil((TIME_WALKER.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     TIME_WALKER.ap + champion3_small_external_buffs[0])
                                ability_data = ["Cybernetic Blast", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if cybernetic_blast_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - cybernetic_blast_requirements[0]
                                cybernetic_blast_requirements[1] = cybernetic_blast_requirements[2]
                                champion4_rp = champion4_rp + cybernetic_blast_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = math.ceil((TIME_WALKER.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(     TIME_WALKER.ap + champion4_small_external_buffs[0])
                                ability_data = ["Cybernetic Blast", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if cybernetic_blast_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - cybernetic_blast_requirements[0]
                                cybernetic_blast_requirements[1] = cybernetic_blast_requirements[2]
                                champion5_rp = champion5_rp + cybernetic_blast_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = math.ceil((TIME_WALKER.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(TIME_WALKER.ap + champion5_small_external_buffs[0])
                                ability_data = ["Cybernetic Blast", "enemy", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Throw Scissors":
            global throw_scissors_requirements
            if throw_scissors_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == CHILD_OF_MEDICINE.title:
                        if counter == 1:
                            if throw_scissors_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - throw_scissors_requirements[0]
                                throw_scissors_requirements[1] = throw_scissors_requirements[2]
                                champion1_rp = champion1_rp + throw_scissors_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = math.ceil(     CHILD_OF_MEDICINE.ap + champion1_small_external_buffs[0])
                                else:
                                    damage_done = math.ceil(CHILD_OF_MEDICINE.ap + champion1_small_external_buffs[0])
                                ability_data = ["Throw Scissors", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if throw_scissors_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - throw_scissors_requirements[0]
                                throw_scissors_requirements[1] = throw_scissors_requirements[2]
                                champion2_rp = champion2_rp + throw_scissors_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = math.ceil((CHILD_OF_MEDICINE.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(CHILD_OF_MEDICINE.ap + champion2_small_external_buffs[0])
                                ability_data = ["Throw Scissors", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if throw_scissors_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - throw_scissors_requirements[0]
                                throw_scissors_requirements[1] = throw_scissors_requirements[2]
                                champion3_rp = champion3_rp + throw_scissors_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = math.ceil((CHILD_OF_MEDICINE.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(CHILD_OF_MEDICINE.ap + champion3_small_external_buffs[0])
                                ability_data = ["Throw Scissors", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if throw_scissors_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - throw_scissors_requirements[0]
                                throw_scissors_requirements[1] = throw_scissors_requirements[2]
                                champion4_rp = champion4_rp + throw_scissors_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = math.ceil((CHILD_OF_MEDICINE.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(CHILD_OF_MEDICINE.ap + champion4_small_external_buffs[0])
                                ability_data = ["Throw Scissors", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if throw_scissors_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - throw_scissors_requirements[0]
                                throw_scissors_requirements[1] = throw_scissors_requirements[2]
                                champion5_rp = champion5_rp + throw_scissors_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = math.ceil((CHILD_OF_MEDICINE.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = math.ceil(CHILD_OF_MEDICINE.ap + champion5_small_external_buffs[0])
                                ability_data = ["Throw Scissors", "enemy", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        self.player_targetting_AI()

    def special_button(self):
        global special1_button, special1_button_details, special2_button, special2_button_details, special3_button, special3_button_details, special4_button, special4_button_details, back_button, \
            from_special_button
        if current_turn == "C1":
            attack_button_champion1.destroy()
            special_button_champion1.destroy()
            rest_button_champion1.destroy()
            special1_button = tk.Button(dungeon_game_frame, text=special_button_text_list[0], width=50, height=4,
                                       command=lambda: self.champion_specials(special_button_text_list_temp[0]))
            special1_button_details = tk.Button(dungeon_game_frame,
                                                text="{} Details".format(special_button_text_list_temp[0]), width=38,
                                                height=1)
            special2_button = tk.Button(dungeon_game_frame, text=special_button_text_list[1], width=50, height=4,
                                       command=lambda: self.champion_specials(special_button_text_list_temp[1]))
            special2_button_details = tk.Button(dungeon_game_frame,
                                                text="{} Details".format(special_button_text_list_temp[1]), width=38,
                                                height=1)
            special3_button = tk.Button(dungeon_game_frame, text=special_button_text_list[2], width=50, height=4,
                                       command=lambda: self.champion_specials(special_button_text_list_temp[2]))
            special3_button_details = tk.Button(dungeon_game_frame,
                                                text="{} Details".format(special_button_text_list_temp[2]), width=38,
                                                height=1)
            special4_button = tk.Button(dungeon_game_frame, text=special_button_text_list[3], width=50, height=4,
                                       command=lambda: self.champion_specials(special_button_text_list_temp[3]))
            special4_button_details = tk.Button(dungeon_game_frame,
                                                text="{} Details".format(special_button_text_list_temp[3]), width=38,
                                                height=1)
            back_button = tk.Button(dungeon_game_frame, text="Back", command=self.player_combat_champion1)
            back_button.grid(row=20, column=2, pady=20)
            special1_button.grid(row=18, column=1)
            special1_button_details.grid(row=19, column=1)
            special2_button.grid(row=18, column=3)
            special2_button_details.grid(row=19, column=3)
            special3_button.grid(row=20, column=1)
            special3_button_details.grid(row=21, column=1)
            special4_button.grid(row=20, column=3)
            special4_button_details.grid(row=21, column=3)
            from_special_button = 1
        if current_turn == "C2":
            attack_button_champion2.destroy()
            special_button_champion2.destroy()
            rest_button_champion2.destroy()
            special1_button = tk.Button(dungeon_game_frame, text=special_button_text_list[0], width=50, height=4,
                                       command=lambda: self.champion_specials(special_button_text_list_temp[0]))
            special1_button_details = tk.Button(dungeon_game_frame,
                                                text="{} Details".format(special_button_text_list_temp[0]), width=38,
                                                height=1)
            special2_button = tk.Button(dungeon_game_frame, text=special_button_text_list[1], width=50, height=4,
                                       command=lambda: self.champion_specials(special_button_text_list_temp[1]))
            special2_button_details = tk.Button(dungeon_game_frame,
                                                text="{} Details".format(special_button_text_list_temp[1]), width=38,
                                                height=1)
            special3_button = tk.Button(dungeon_game_frame, text=special_button_text_list[2], width=50, height=4,
                                       command=lambda: self.champion_specials(special_button_text_list_temp[2]))
            special3_button_details = tk.Button(dungeon_game_frame,
                                                text="{} Details".format(special_button_text_list_temp[2]), width=38,
                                                height=1)
            special4_button = tk.Button(dungeon_game_frame, text=special_button_text_list[3], width=50, height=4,
                                       command=lambda: self.champion_specials(special_button_text_list_temp[3]))
            special4_button_details = tk.Button(dungeon_game_frame,
                                                text="{} Details".format(special_button_text_list_temp[3]), width=38,
                                                height=1)
            back_button = tk.Button(dungeon_game_frame, text="Back", command=self.player_combat_champion2)
            back_button.grid(row=20, column=2, pady=20)
            special1_button.grid(row=18, column=1)
            special1_button_details.grid(row=19, column=1)
            special2_button.grid(row=18, column=3)
            special2_button_details.grid(row=19, column=3)
            special3_button.grid(row=20, column=1)
            special3_button_details.grid(row=21, column=1)
            special4_button.grid(row=20, column=3)
            special4_button_details.grid(row=21, column=3)
            from_special_button = 1
        if current_turn == "C3":
            attack_button_champion3.destroy()
            special_button_champion3.destroy()
            rest_button_champion3.destroy()
            special1_button = tk.Button(dungeon_game_frame, text=special_button_text_list[0], width=50, height=4,
                                       command=lambda: self.champion_specials(special_button_text_list_temp[0]))
            special1_button_details = tk.Button(dungeon_game_frame,
                                                text="{} Details".format(special_button_text_list_temp[0]), width=38,
                                                height=1)
            special2_button = tk.Button(dungeon_game_frame, text=special_button_text_list[1], width=50, height=4,
                                       command=lambda: self.champion_specials(special_button_text_list_temp[1]))
            special2_button_details = tk.Button(dungeon_game_frame,
                                                text="{} Details".format(special_button_text_list_temp[1]), width=38,
                                                height=1)
            special3_button = tk.Button(dungeon_game_frame, text=special_button_text_list[2], width=50, height=4,
                                       command=lambda: self.champion_specials(special_button_text_list_temp[2]))
            special3_button_details = tk.Button(dungeon_game_frame,
                                                text="{} Details".format(special_button_text_list_temp[2]), width=38,
                                                height=1)
            special4_button = tk.Button(dungeon_game_frame, text=special_button_text_list[3], width=50, height=4,
                                       command=lambda: self.champion_specials(special_button_text_list_temp[3]))
            special4_button_details = tk.Button(dungeon_game_frame,
                                                text="{} Details".format(special_button_text_list_temp[3]), width=38,
                                                height=1)
            back_button = tk.Button(dungeon_game_frame, text="Back", command=self.player_combat_champion3)
            back_button.grid(row=20, column=2, pady=20)
            special1_button.grid(row=18, column=1)
            special1_button_details.grid(row=19, column=1)
            special2_button.grid(row=18, column=3)
            special2_button_details.grid(row=19, column=3)
            special3_button.grid(row=20, column=1)
            special3_button_details.grid(row=21, column=1)
            special4_button.grid(row=20, column=3)
            special4_button_details.grid(row=21, column=3)
            from_special_button = 1
        if current_turn == "C4":
            attack_button_champion4.destroy()
            special_button_champion4.destroy()
            rest_button_champion4.destroy()
            special1_button = tk.Button(dungeon_game_frame, text=special_button_text_list[0], width=50, height=4,
                                       command=lambda: self.champion_specials(special_button_text_list_temp[0]))
            special1_button_details = tk.Button(dungeon_game_frame,
                                                text="{} Details".format(special_button_text_list_temp[0]), width=38,
                                                height=1)
            special2_button = tk.Button(dungeon_game_frame, text=special_button_text_list[1], width=50, height=4,
                                       command=lambda: self.champion_specials(special_button_text_list_temp[1]))
            special2_button_details = tk.Button(dungeon_game_frame,
                                                text="{} Details".format(special_button_text_list_temp[1]), width=38,
                                                height=1)
            special3_button = tk.Button(dungeon_game_frame, text=special_button_text_list[2], width=50, height=4,
                                       command=lambda: self.champion_specials(special_button_text_list_temp[2]))
            special3_button_details = tk.Button(dungeon_game_frame,
                                                text="{} Details".format(special_button_text_list_temp[2]), width=38,
                                                height=1)
            special4_button = tk.Button(dungeon_game_frame, text=special_button_text_list[3], width=50, height=4,
                                       command=lambda: self.champion_specials(special_button_text_list_temp[3]))
            special4_button_details = tk.Button(dungeon_game_frame,
                                                text="{} Details".format(special_button_text_list_temp[3]), width=38,
                                                height=1)
            back_button = tk.Button(dungeon_game_frame, text="Back", command=self.player_combat_champion4)
            back_button.grid(row=20, column=2, pady=20)
            special1_button.grid(row=18, column=1)
            special1_button_details.grid(row=19, column=1)
            special2_button.grid(row=18, column=3)
            special2_button_details.grid(row=19, column=3)
            special3_button.grid(row=20, column=1)
            special3_button_details.grid(row=21, column=1)
            special4_button.grid(row=20, column=3)
            special4_button_details.grid(row=21, column=3)
            from_special_button = 1
        if current_turn == "C5":
            attack_button_champion5.destroy()
            special_button_champion5.destroy()
            rest_button_champion5.destroy()
            special1_button = tk.Button(dungeon_game_frame, text=special_button_text_list[0], width=50, height=4,
                                       command=lambda: self.champion_specials(special_button_text_list_temp[0]))
            special1_button_details = tk.Button(dungeon_game_frame,
                                                text="{} Details".format(special_button_text_list_temp[0]), width=38,
                                                height=1)
            special2_button = tk.Button(dungeon_game_frame, text=special_button_text_list[1], width=50, height=4,
                                       command=lambda: self.champion_specials(special_button_text_list_temp[1]))
            special2_button_details = tk.Button(dungeon_game_frame,
                                                text="{} Details".format(special_button_text_list_temp[1]), width=38,
                                                height=1)
            special3_button = tk.Button(dungeon_game_frame, text=special_button_text_list[2], width=50, height=4,
                                       command=lambda: self.champion_specials(special_button_text_list_temp[2]))
            special3_button_details = tk.Button(dungeon_game_frame,
                                                text="{} Details".format(special_button_text_list_temp[2]), width=38,
                                                height=1)
            special4_button = tk.Button(dungeon_game_frame, text=special_button_text_list[3], width=50, height=4,
                                       command=lambda: self.champion_specials(special_button_text_list_temp[3]))
            special4_button_details = tk.Button(dungeon_game_frame,
                                                text="{} Details".format(special_button_text_list_temp[3]), width=38,
                                                height=1)
            back_button = tk.Button(dungeon_game_frame, text="Back", command=self.player_combat_champion5)
            back_button.grid(row=20, column=2, pady=20)
            special1_button.grid(row=18, column=1)
            special1_button_details.grid(row=19, column=1)
            special2_button.grid(row=18, column=3)
            special2_button_details.grid(row=19, column=3)
            special3_button.grid(row=20, column=1)
            special3_button_details.grid(row=21, column=1)
            special4_button.grid(row=20, column=3)
            special4_button_details.grid(row=21, column=3)
            from_special_button = 1

    def champion_specials(self, ability_name):
        global attack_to_target, special_to_target, ability_data, champion1_rp, champion2_rp, champion3_rp, champion4_rp, champion5_rp
        attack_to_target = 0
        special_to_target = 1
        counter = 1
        damage_done = 0
        healing_done = 0
        if ability_name == "Empty":
            return
        elif ability_name == "Harmonize":
            global harmonize_requirements
            if harmonize_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == MONK.title:
                        if counter == 1:
                            if harmonize_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - harmonize_requirements[0]
                                harmonize_requirements[1] = harmonize_requirements[2]
                                champion1_rp = champion1_rp + harmonize_requirements[3]
                                ability_data =["Harmonize", "self", "1T"]
                            else:
                                return
                        if counter == 2:
                            if harmonize_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - harmonize_requirements[0]
                                harmonize_requirements[1] = harmonize_requirements[2]
                                champion2_rp = champion2_rp + harmonize_requirements[3]
                                ability_data =["Harmonize", "self", "1T"]
                            else:
                                return
                        if counter == 3:
                            if harmonize_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - harmonize_requirements[0]
                                harmonize_requirements[1] = harmonize_requirements[2]
                                champion3_rp = champion3_rp + harmonize_requirements[3]
                                ability_data =["Harmonize", "self", "1T"]
                            else:
                                return
                        if counter == 4:
                            if harmonize_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - harmonize_requirements[0]
                                harmonize_requirements[1] = harmonize_requirements[2]
                                champion4_rp = champion4_rp + harmonize_requirements[3]
                                ability_data =["Harmonize", "self", "1T"]
                            else:
                                return
                        if counter == 5:
                            if harmonize_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - harmonize_requirements[0]
                                harmonize_requirements[1] = harmonize_requirements[2]
                                champion5_rp = champion5_rp + harmonize_requirements[3]
                                ability_data =["Harmonize", "self", "1T"]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Pressure Points":
            global pressure_points_requirements
            if pressure_points_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == MONK.title:
                        if counter == 1:
                            if pressure_points_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - pressure_points_requirements[0]
                                pressure_points_requirements[1] = pressure_points_requirements[2]
                                champion1_rp = champion1_rp + pressure_points_requirements[3]
                                ability_data = ["Pressure Points", "enemy", "1T"]
                            else:
                                return
                        if counter == 2:
                            if pressure_points_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - pressure_points_requirements[0]
                                pressure_points_requirements[1] = pressure_points_requirements[2]
                                champion2_rp = champion2_rp + pressure_points_requirements[3]
                                ability_data = ["Pressure Points", "enemy", "1T"]
                            else:
                                return
                        if counter == 3:
                            if pressure_points_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - pressure_points_requirements[0]
                                pressure_points_requirements[1] = pressure_points_requirements[2]
                                champion3_rp = champion3_rp + pressure_points_requirements[3]
                                ability_data = ["Pressure Points", "enemy", "1T"]
                            else:
                                return
                        if counter == 4:
                            if pressure_points_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - pressure_points_requirements[0]
                                pressure_points_requirements[1] = pressure_points_requirements[2]
                                champion4_rp = champion4_rp + pressure_points_requirements[3]
                                ability_data = ["Pressure Points", "enemy", "1T"]
                            else:
                                return
                        if counter == 5:
                            if pressure_points_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - pressure_points_requirements[0]
                                pressure_points_requirements[1] = pressure_points_requirements[2]
                                champion5_rp = champion5_rp + pressure_points_requirements[3]
                                ability_data = ["Pressure Points", "enemy", "1T"]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Challenging Shout":
            global challenging_shout_requirements
            if challenging_shout_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == BARBARIAN.title:
                        if counter == 1:
                            if challenging_shout_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - challenging_shout_requirements[0]
                                challenging_shout_requirements[1] = challenging_shout_requirements[2]
                                champion1_rp = champion1_rp + challenging_shout_requirements[3]
                                ability_data = ["Challenging Shout", "self", "AOE"]
                            else:
                                return
                        if counter == 2:
                            if challenging_shout_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - challenging_shout_requirements[0]
                                challenging_shout_requirements[1] = challenging_shout_requirements[2]
                                champion2_rp = champion2_rp + challenging_shout_requirements[3]
                                ability_data = ["Challenging Shout", "self", "AOE"]
                            else:
                                return
                        if counter == 3:
                            if challenging_shout_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - challenging_shout_requirements[0]
                                challenging_shout_requirements[1] = challenging_shout_requirements[2]
                                champion3_rp = champion3_rp + challenging_shout_requirements[3]
                                ability_data = ["Challenging Shout", "self", "AOE"]
                            else:
                                return
                        if counter == 4:
                            if challenging_shout_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - challenging_shout_requirements[0]
                                challenging_shout_requirements[1] = challenging_shout_requirements[2]
                                champion4_rp = champion4_rp + challenging_shout_requirements[3]
                                ability_data = ["Challenging Shout", "self", "AOE"]
                            else:
                                return
                        if counter == 5:
                            if challenging_shout_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - challenging_shout_requirements[0]
                                challenging_shout_requirements[1] = challenging_shout_requirements[2]
                                champion5_rp = champion5_rp + challenging_shout_requirements[3]
                                ability_data = ["Challenging Shout", "self", "AOE"]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Impactful Boast":
            global impactful_boast_requirements
            if impactful_boast_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == BARBARIAN.title:
                        if counter == 1:
                            if impactful_boast_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - impactful_boast_requirements[0]
                                impactful_boast_requirements[1] = impactful_boast_requirements[2]
                                champion1_rp = champion1_rp + impactful_boast_requirements[3]
                                ability_data = ["Impactful Boast", "self"]
                            else:
                                return
                        if counter == 2:
                            if impactful_boast_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - impactful_boast_requirements[0]
                                impactful_boast_requirements[1] = impactful_boast_requirements[2]
                                champion2_rp = champion2_rp + impactful_boast_requirements[3]
                                ability_data = ["Impactful Boast", "self"]
                            else:
                                return
                        if counter == 3:
                            if impactful_boast_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - impactful_boast_requirements[0]
                                impactful_boast_requirements[1] = impactful_boast_requirements[2]
                                champion3_rp = champion3_rp + impactful_boast_requirements[3]
                                ability_data = ["Impactful Boast", "self"]
                            else:
                                return
                        if counter == 4:
                            if impactful_boast_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - impactful_boast_requirements[0]
                                impactful_boast_requirements[1] = impactful_boast_requirements[2]
                                champion4_rp = champion4_rp + impactful_boast_requirements[3]
                                ability_data = ["Impactful Boast", "self"]
                            else:
                                return
                        if counter == 5:
                            if impactful_boast_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - impactful_boast_requirements[0]
                                impactful_boast_requirements[1] = impactful_boast_requirements[2]
                                champion5_rp = champion5_rp + impactful_boast_requirements[3]
                                ability_data = ["Impactful Boast", "self"]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Fortification":
            global fortification_requirements
            if fortification_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == VETERAN_BODYGUARD.title:
                        if counter == 1:
                            if fortification_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - fortification_requirements[0]
                                fortification_requirements[1] = fortification_requirements[2]
                                champion1_rp = champion1_rp + fortification_requirements[3]
                                ability_data = ["Fortification", "ally", "AOE"]
                            else:
                                return
                        if counter == 2:
                            if fortification_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - fortification_requirements[0]
                                fortification_requirements[1] = fortification_requirements[2]
                                champion2_rp = champion2_rp + fortification_requirements[3]
                                ability_data = ["Fortification", "ally", "AOE"]
                            else:
                                return
                        if counter == 3:
                            if fortification_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - fortification_requirements[0]
                                fortification_requirements[1] = fortification_requirements[2]
                                champion3_rp = champion3_rp + fortification_requirements[3]
                                ability_data = ["Fortification", "ally", "AOE"]
                            else:
                                return
                        if counter == 4:
                            if fortification_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - fortification_requirements[0]
                                fortification_requirements[1] = fortification_requirements[2]
                                champion4_rp = champion4_rp + fortification_requirements[3]
                                ability_data = ["Fortification", "ally", "AOE"]
                            else:
                                return
                        if counter == 5:
                            if fortification_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - fortification_requirements[0]
                                fortification_requirements[1] = fortification_requirements[2]
                                champion5_rp = champion5_rp + fortification_requirements[3]
                                ability_data = ["Fortification", "ally", "AOE"]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Block":
            global block_requirements
            if block_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == VETERAN_BODYGUARD.title:
                        if counter == 1:
                            if block_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - block_requirements[0]
                                block_requirements[1] = block_requirements[2]
                                champion1_rp = champion1_rp + block_requirements[3]
                                ability_data = ["Block", "ally", "1T"]
                            else:
                                return
                        if counter == 2:
                            if block_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - block_requirements[0]
                                block_requirements[1] = block_requirements[2]
                                champion2_rp = champion2_rp + block_requirements[3]
                                ability_data = ["Block", "ally", "1T"]
                            else:
                                return
                        if counter == 3:
                            if block_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - block_requirements[0]
                                block_requirements[1] = block_requirements[2]
                                champion3_rp = champion3_rp + block_requirements[3]
                                ability_data = ["Block", "ally", "1T"]
                            else:
                                return
                        if counter == 4:
                            if block_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - block_requirements[0]
                                block_requirements[1] = block_requirements[2]
                                champion4_rp = champion4_rp + block_requirements[3]
                                ability_data = ["Block", "ally", "1T"]
                            else:
                                return
                        if counter == 5:
                            if block_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - block_requirements[0]
                                block_requirements[1] = block_requirements[2]
                                champion5_rp = champion5_rp + block_requirements[3]
                                ability_data = ["Block", "ally", "1T"]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Parry":
            global parry_requirements
            if parry_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == MASTER_FENCER.title:
                        if counter == 1:
                            if parry_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - parry_requirements[0]
                                parry_requirements[1] = parry_requirements[2]
                                champion1_rp = champion1_rp + parry_requirements[3]
                                ability_data = ["Parry", "ally", "1T"]
                            else:
                                return
                        if counter == 2:
                            if parry_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - parry_requirements[0]
                                parry_requirements[1] = parry_requirements[2]
                                champion2_rp = champion2_rp + parry_requirements[3]
                                ability_data = ["Parry", "ally", "1T"]
                            else:
                                return
                        if counter == 3:
                            if parry_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - parry_requirements[0]
                                parry_requirements[1] = parry_requirements[2]
                                champion3_rp = champion3_rp + parry_requirements[3]
                                ability_data = ["Parry", "ally", "1T"]
                            else:
                                return
                        if counter == 4:
                            if parry_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - parry_requirements[0]
                                parry_requirements[1] = parry_requirements[2]
                                champion4_rp = champion4_rp + parry_requirements[3]
                                ability_data = ["Parry", "ally", "1T"]
                            else:
                                return
                        if counter == 5:
                            if parry_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - parry_requirements[0]
                                parry_requirements[1] = parry_requirements[2]
                                champion5_rp = champion5_rp + parry_requirements[3]
                                ability_data = ["Parry", "ally", "1T"]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Elusive Measures":
            global elusive_measures_requirements
            if elusive_measures_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == MASTER_FENCER.title:
                        if counter == 1:
                            if elusive_measures_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - elusive_measures_requirements[0]
                                elusive_measures_requirements[1] = elusive_measures_requirements[2]
                                champion1_rp = champion1_rp + elusive_measures_requirements[3]
                                ability_data = ["Elusive Measures", "self"]
                            else:
                                return
                        if counter == 2:
                            if elusive_measures_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - elusive_measures_requirements[0]
                                elusive_measures_requirements[1] = elusive_measures_requirements[2]
                                champion2_rp = champion2_rp + elusive_measures_requirements[3]
                                ability_data = ["Elusive Measures", "self"]
                            else:
                                return
                        if counter == 3:
                            if elusive_measures_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - elusive_measures_requirements[0]
                                elusive_measures_requirements[1] = elusive_measures_requirements[2]
                                champion3_rp = champion3_rp + elusive_measures_requirements[3]
                                ability_data = ["Elusive Measures", "self"]
                            else:
                                return
                        if counter == 4:
                            if elusive_measures_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - elusive_measures_requirements[0]
                                elusive_measures_requirements[1] = elusive_measures_requirements[2]
                                champion4_rp = champion4_rp + elusive_measures_requirements[3]
                                ability_data = ["Elusive Measures", "self"]
                            else:
                                return
                        if counter == 5:
                            if elusive_measures_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - elusive_measures_requirements[0]
                                elusive_measures_requirements[1] = elusive_measures_requirements[2]
                                champion5_rp = champion5_rp + elusive_measures_requirements[3]
                                ability_data = ["Elusive Measures", "self"]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Enrage":
            global enrage_requirements
            if enrage_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == BERSERKER.title:
                        if counter == 1:
                            if enrage_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - enrage_requirements[0]
                                enrage_requirements[1] = enrage_requirements[2]
                                champion1_rp = champion1_rp + enrage_requirements[3]
                                ability_data = ["Enrage", "self"]
                            else:
                                return
                        if counter == 2:
                            if enrage_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - enrage_requirements[0]
                                enrage_requirements[1] = enrage_requirements[2]
                                champion2_rp = champion2_rp + enrage_requirements[3]
                                ability_data = ["Enrage", "self"]
                            else:
                                return
                        if counter == 3:
                            if enrage_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - enrage_requirements[0]
                                enrage_requirements[1] = enrage_requirements[2]
                                champion3_rp = champion3_rp + enrage_requirements[3]
                                ability_data = ["Enrage", "self"]
                            else:
                                return
                        if counter == 4:
                            if enrage_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - enrage_requirements[0]
                                enrage_requirements[1] = enrage_requirements[2]
                                champion4_rp = champion4_rp + enrage_requirements[3]
                                ability_data = ["Enrage", "self"]
                            else:
                                return
                        if counter == 5:
                            if enrage_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - enrage_requirements[0]
                                enrage_requirements[1] = enrage_requirements[2]
                                champion5_rp = champion5_rp + enrage_requirements[3]
                                ability_data = ["Enrage", "self"]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Reckless Flurry":
            global reckless_flurry_requirements
            if reckless_flurry_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == BERSERKER.title:
                        if counter == 1:
                            if reckless_flurry_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - reckless_flurry_requirements[0]
                                reckless_flurry_requirements[1] = reckless_flurry_requirements[2]
                                champion1_rp = champion1_rp + reckless_flurry_requirements[3]
                                ability_data = ["Reckless Flurry", "self"]
                            else:
                                return
                        if counter == 2:
                            if reckless_flurry_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - reckless_flurry_requirements[0]
                                reckless_flurry_requirements[1] = reckless_flurry_requirements[2]
                                champion2_rp = champion2_rp + reckless_flurry_requirements[3]
                                ability_data = ["Reckless Flurry", "self"]
                            else:
                                return
                        if counter == 3:
                            if reckless_flurry_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - reckless_flurry_requirements[0]
                                reckless_flurry_requirements[1] = reckless_flurry_requirements[2]
                                champion3_rp = champion3_rp + reckless_flurry_requirements[3]
                                ability_data = ["Reckless Flurry", "self"]
                            else:
                                return
                        if counter == 4:
                            if reckless_flurry_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - reckless_flurry_requirements[0]
                                reckless_flurry_requirements[1] = reckless_flurry_requirements[2]
                                champion4_rp = champion4_rp + reckless_flurry_requirements[3]
                                ability_data = ["Reckless Flurry", "self"]
                            else:
                                return
                        if counter == 5:
                            if reckless_flurry_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - reckless_flurry_requirements[0]
                                reckless_flurry_requirements[1] = reckless_flurry_requirements[2]
                                champion5_rp = champion5_rp + reckless_flurry_requirements[3]
                                ability_data = ["Reckless Flurry", "self"]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Garrote":
            global garrote_requirements
            if garrote_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == ROGUE.title:
                        if counter == 1:
                            if garrote_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - garrote_requirements[0]
                                garrote_requirements[1] = garrote_requirements[2]
                                champion1_rp = champion1_rp + garrote_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = ((ROGUE.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = (ROGUE.ap + champion1_small_external_buffs[0])
                                ability_data = ["Garrote", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if garrote_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - garrote_requirements[0]
                                garrote_requirements[1] = garrote_requirements[2]
                                champion2_rp = champion2_rp + garrote_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = ((ROGUE.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = (ROGUE.ap + champion2_small_external_buffs[0])
                                ability_data = ["Garrote", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if garrote_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - garrote_requirements[0]
                                garrote_requirements[1] = garrote_requirements[2]
                                champion3_rp = champion3_rp + garrote_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = ((ROGUE.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = (ROGUE.ap + champion3_small_external_buffs[0])
                                ability_data = ["Garrote", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if garrote_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - garrote_requirements[0]
                                garrote_requirements[1] = garrote_requirements[2]
                                champion4_rp = champion4_rp + garrote_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = ((ROGUE.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = (ROGUE.ap + champion4_small_external_buffs[0])
                                ability_data = ["Garrote", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if garrote_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - garrote_requirements[0]
                                garrote_requirements[1] = garrote_requirements[2]
                                champion5_rp = champion5_rp + garrote_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = ((ROGUE.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = (ROGUE.ap + champion5_small_external_buffs[0])
                                ability_data = ["Garrote", "enemy", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Exploit Weakness":
            global exploit_weakness_requirements
            if exploit_weakness_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == ROGUE.title:
                        if counter == 1:
                            if exploit_weakness_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - exploit_weakness_requirements[0]
                                exploit_weakness_requirements[1] = exploit_weakness_requirements[2]
                                champion1_rp = champion1_rp + exploit_weakness_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = ((ROGUE.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = (ROGUE.ap + champion1_small_external_buffs[0])
                                ability_data = ["Exploit Weakness", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if exploit_weakness_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - exploit_weakness_requirements[0]
                                exploit_weakness_requirements[1] = exploit_weakness_requirements[2]
                                champion2_rp = champion2_rp + exploit_weakness_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = ((ROGUE.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = (ROGUE.ap + champion2_small_external_buffs[0])
                                ability_data = ["Exploit Weakness", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if exploit_weakness_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - exploit_weakness_requirements[0]
                                exploit_weakness_requirements[1] = exploit_weakness_requirements[2]
                                champion3_rp = champion3_rp + exploit_weakness_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = ((ROGUE.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = (ROGUE.ap + champion3_small_external_buffs[0])
                                ability_data = ["Exploit Weakness", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if exploit_weakness_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - exploit_weakness_requirements[0]
                                exploit_weakness_requirements[1] = exploit_weakness_requirements[2]
                                champion4_rp = champion4_rp + exploit_weakness_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = ((ROGUE.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = (ROGUE.ap + champion4_small_external_buffs[0])
                                ability_data = ["Exploit Weakness", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if exploit_weakness_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - exploit_weakness_requirements[0]
                                exploit_weakness_requirements[1] = exploit_weakness_requirements[2]
                                champion5_rp = champion5_rp + exploit_weakness_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = ((ROGUE.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = (ROGUE.ap + champion5_small_external_buffs[0])
                                ability_data = ["Exploit Weakness", "enemy", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Play Dead":
            global play_dead_requirements
            if play_dead_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == SURVIVALIST.title:
                        if counter == 1:
                            if play_dead_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - play_dead_requirements[0]
                                play_dead_requirements[1] = play_dead_requirements[2]
                                champion1_rp = champion1_rp + play_dead_requirements[3]
                                ability_data = ["Play Dead", "self"]
                            else:
                                return
                        if counter == 2:
                            if play_dead_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - play_dead_requirements[0]
                                play_dead_requirements[1] = play_dead_requirements[2]
                                champion2_rp = champion2_rp + play_dead_requirements[3]
                                ability_data = ["Play Dead", "self"]
                            else:
                                return
                        if counter == 3:
                            if play_dead_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - play_dead_requirements[0]
                                play_dead_requirements[1] = play_dead_requirements[2]
                                champion3_rp = champion3_rp + play_dead_requirements[3]
                                ability_data = ["Play Dead", "self"]
                            else:
                                return
                        if counter == 4:
                            if play_dead_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - play_dead_requirements[0]
                                play_dead_requirements[1] = play_dead_requirements[2]
                                champion4_rp = champion4_rp + play_dead_requirements[3]
                                ability_data = ["Play Dead", "self"]
                            else:
                                return
                        if counter == 5:
                            if play_dead_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - play_dead_requirements[0]
                                play_dead_requirements[1] = play_dead_requirements[2]
                                champion5_rp = champion5_rp + play_dead_requirements[3]
                                ability_data = ["Play Dead", "self"]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Rushed Rest":
            global rushed_rest_requirements
            if rushed_rest_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == SURVIVALIST.title:
                        if counter == 1:
                            if rushed_rest_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - rushed_rest_requirements[0]
                                rushed_rest_requirements[1] = rushed_rest_requirements[2]
                                champion1_rp = champion1_rp + rushed_rest_requirements[3]
                                ability_data = ["Rushed Rest", "self"]
                            else:
                                return
                        if counter == 2:
                            if rushed_rest_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - rushed_rest_requirements[0]
                                rushed_rest_requirements[1] = rushed_rest_requirements[2]
                                champion2_rp = champion2_rp + rushed_rest_requirements[3]
                                ability_data = ["Rushed Rest", "self"]
                            else:
                                return
                        if counter == 3:
                            if rushed_rest_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - rushed_rest_requirements[0]
                                rushed_rest_requirements[1] = rushed_rest_requirements[2]
                                champion3_rp = champion3_rp + rushed_rest_requirements[3]
                                ability_data = ["Rushed Rest", "self"]
                            else:
                                return
                        if counter == 4:
                            if rushed_rest_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - rushed_rest_requirements[0]
                                rushed_rest_requirements[1] = rushed_rest_requirements[2]
                                champion4_rp = champion4_rp + rushed_rest_requirements[3]
                                ability_data = ["Rushed Rest", "self"]
                            else:
                                return
                        if counter == 5:
                            if rushed_rest_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - rushed_rest_requirements[0]
                                rushed_rest_requirements[1] = rushed_rest_requirements[2]
                                champion5_rp = champion5_rp + rushed_rest_requirements[3]
                                ability_data = ["Rushed Rest", "self"]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Defensive Stance":
            global denfensive_stance_requirements
            if denfensive_stance_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == BRAWLIST.title:
                        if counter == 1:
                            if denfensive_stance_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - denfensive_stance_requirements[0]
                                denfensive_stance_requirements[1] = denfensive_stance_requirements[2]
                                champion1_rp = champion1_rp + denfensive_stance_requirements[3]
                                ability_data = ["Defensive Stance", "self"]
                            else:
                                return
                        if counter == 2:
                            if denfensive_stance_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - denfensive_stance_requirements[0]
                                denfensive_stance_requirements[1] = denfensive_stance_requirements[2]
                                champion2_rp = champion2_rp + denfensive_stance_requirements[3]
                                ability_data = ["Defensive Stance", "self"]
                            else:
                                return
                        if counter == 3:
                            if denfensive_stance_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - denfensive_stance_requirements[0]
                                denfensive_stance_requirements[1] = denfensive_stance_requirements[2]
                                champion3_rp = champion3_rp + denfensive_stance_requirements[3]
                                ability_data = ["Defensive Stance", "self"]
                            else:
                                return
                        if counter == 4:
                            if denfensive_stance_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - denfensive_stance_requirements[0]
                                denfensive_stance_requirements[1] = denfensive_stance_requirements[2]
                                champion4_rp = champion4_rp + denfensive_stance_requirements[3]
                                ability_data = ["Defensive Stance", "self"]
                            else:
                                return
                        if counter == 5:
                            if denfensive_stance_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - denfensive_stance_requirements[0]
                                denfensive_stance_requirements[1] = denfensive_stance_requirements[2]
                                champion5_rp = champion5_rp + denfensive_stance_requirements[3]
                                ability_data = ["Defensive Stance", "self"]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Rushdown":
            global rushdown_requirements
            if rushdown_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == BRAWLIST.title:
                        if counter == 1:
                            if rushdown_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - rushdown_requirements[0]
                                rushdown_requirements[1] = rushdown_requirements[2]
                                champion1_rp = champion1_rp + rushdown_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = ((BRAWLIST.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = (BRAWLIST.ap + champion1_small_external_buffs[0])
                                ability_data = ["Rushdown", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if rushdown_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - rushdown_requirements[0]
                                rushdown_requirements[1] = rushdown_requirements[2]
                                champion2_rp = champion2_rp + rushdown_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = ((BRAWLIST.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = (BRAWLIST.ap + champion2_small_external_buffs[0])
                                ability_data = ["Rushdown", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if rushdown_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - rushdown_requirements[0]
                                rushdown_requirements[1] = rushdown_requirements[2]
                                champion3_rp = champion3_rp + rushdown_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = ((BRAWLIST.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = (BRAWLIST.ap + champion3_small_external_buffs[0])
                                ability_data = ["Rushdown", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if rushdown_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - rushdown_requirements[0]
                                rushdown_requirements[1] = rushdown_requirements[2]
                                champion4_rp = champion4_rp + rushdown_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = ((BRAWLIST.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = (BRAWLIST.ap + champion4_small_external_buffs[0])
                                ability_data = ["Rushdown", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if rushdown_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - rushdown_requirements[0]
                                rushdown_requirements[1] = rushdown_requirements[2]
                                champion5_rp = champion5_rp + rushdown_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = ((BRAWLIST.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = (BRAWLIST.ap + champion5_small_external_buffs[0])
                                ability_data = ["Rushdown", "enemy", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Arcane Brilliance":
            global arcane_brilliance_requirements
            if arcane_brilliance_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == ACADEMIC_MAGE.title:
                        if counter == 1:
                            if arcane_brilliance_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - arcane_brilliance_requirements[0]
                                arcane_brilliance_requirements[1] = arcane_brilliance_requirements[2]
                                champion1_rp = champion1_rp + arcane_brilliance_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = ((ACADEMIC_MAGE.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = (ACADEMIC_MAGE.ap + champion1_small_external_buffs[0])
                                ability_data = ["Arcane Brilliance", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if arcane_brilliance_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - arcane_brilliance_requirements[0]
                                arcane_brilliance_requirements[1] = arcane_brilliance_requirements[2]
                                champion2_rp = champion2_rp + arcane_brilliance_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = ((ACADEMIC_MAGE.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = (ACADEMIC_MAGE.ap + champion2_small_external_buffs[0])
                                ability_data = ["Arcane Brilliance", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if arcane_brilliance_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - arcane_brilliance_requirements[0]
                                arcane_brilliance_requirements[1] = arcane_brilliance_requirements[2]
                                champion3_rp = champion3_rp + arcane_brilliance_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = ((ACADEMIC_MAGE.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = (ACADEMIC_MAGE.ap + champion3_small_external_buffs[0])
                                ability_data = ["Arcane Brilliance", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if arcane_brilliance_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - arcane_brilliance_requirements[0]
                                arcane_brilliance_requirements[1] = arcane_brilliance_requirements[2]
                                champion4_rp = champion4_rp + arcane_brilliance_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = ((ACADEMIC_MAGE.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = (ACADEMIC_MAGE.ap + champion4_small_external_buffs[0])
                                ability_data = ["Arcane Brilliance", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if arcane_brilliance_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - arcane_brilliance_requirements[0]
                                arcane_brilliance_requirements[1] = arcane_brilliance_requirements[2]
                                champion5_rp = champion5_rp + arcane_brilliance_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = ((ACADEMIC_MAGE.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = (ACADEMIC_MAGE.ap + champion5_small_external_buffs[0])
                                ability_data = ["Arcane Brilliance", "enemy", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Magical Barrier":
            global magical_barrier_requirements
            if magical_barrier_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == ACADEMIC_MAGE.title:
                        if counter == 1:
                            if magical_barrier_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - magical_barrier_requirements[0]
                                magical_barrier_requirements[1] = magical_barrier_requirements[2]
                                champion1_rp = champion1_rp + magical_barrier_requirements[3]
                                ability_data = ["Magical Barrier", "self"]
                            else:
                                return
                        if counter == 2:
                            if magical_barrier_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - magical_barrier_requirements[0]
                                magical_barrier_requirements[1] = magical_barrier_requirements[2]
                                champion2_rp = champion2_rp + magical_barrier_requirements[3]
                                ability_data = ["Magical Barrier", "self"]
                            else:
                                return
                        if counter == 3:
                            if magical_barrier_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - magical_barrier_requirements[0]
                                magical_barrier_requirements[1] = magical_barrier_requirements[2]
                                champion3_rp = champion3_rp + magical_barrier_requirements[3]
                                ability_data = ["Magical Barrier", "self"]
                            else:
                                return
                        if counter == 4:
                            if magical_barrier_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - magical_barrier_requirements[0]
                                magical_barrier_requirements[1] = magical_barrier_requirements[2]
                                champion4_rp = champion4_rp + magical_barrier_requirements[3]
                                ability_data = ["Magical Barrier", "self"]
                            else:
                                return
                        if counter == 5:
                            if magical_barrier_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - magical_barrier_requirements[0]
                                magical_barrier_requirements[1] = magical_barrier_requirements[2]
                                champion5_rp = champion5_rp + magical_barrier_requirements[3]
                                ability_data = ["Magical Barrier", "self"]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Thorns":
            global thorns_requirements
            if thorns_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == DRUID.title:
                        if counter == 1:
                            if thorns_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - thorns_requirements[0]
                                thorns_requirements[1] = thorns_requirements[2]
                                champion1_rp = champion1_rp + thorns_requirements[3]
                                ability_data = ["Thorns", "ally", "1T"]
                            else:
                                return
                        if counter == 2:
                            if thorns_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - thorns_requirements[0]
                                thorns_requirements[1] = thorns_requirements[2]
                                champion2_rp = champion2_rp + thorns_requirements[3]
                                ability_data = ["Thorns", "ally", "1T"]
                            else:
                                return
                        if counter == 3:
                            if thorns_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - thorns_requirements[0]
                                thorns_requirements[1] = thorns_requirements[2]
                                champion3_rp = champion3_rp + thorns_requirements[3]
                                ability_data = ["Thorns", "ally", "1T"]
                            else:
                                return
                        if counter == 4:
                            if thorns_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - thorns_requirements[0]
                                thorns_requirements[1] = thorns_requirements[2]
                                champion4_rp = champion4_rp + thorns_requirements[3]
                                ability_data = ["Thorns", "ally", "1T"]
                            else:
                                return
                        if counter == 5:
                            if thorns_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - thorns_requirements[0]
                                thorns_requirements[1] = thorns_requirements[2]
                                champion5_rp = champion5_rp + thorns_requirements[3]
                                ability_data = ["Thorns", "ally", "1T"]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Prickle Arena":
            global prickle_arena_requirements
            if prickle_arena_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == DRUID.title:
                        if counter == 1:
                            if prickle_arena_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - prickle_arena_requirements[0]
                                prickle_arena_requirements[1] = prickle_arena_requirements[2]
                                champion1_rp = champion1_rp + prickle_arena_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = ((DRUID.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = (DRUID.ap + champion1_small_external_buffs[0])
                                ability_data = ["Prickle Arena", "enemy", "AOE", damage_done]
                            else:
                                return
                        if counter == 2:
                            if prickle_arena_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - prickle_arena_requirements[0]
                                prickle_arena_requirements[1] = prickle_arena_requirements[2]
                                champion2_rp = champion2_rp + prickle_arena_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = ((DRUID.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = (DRUID.ap + champion2_small_external_buffs[0])
                                ability_data = ["Prickle Arena", "enemy", "AOE", damage_done]
                            else:
                                return
                        if counter == 3:
                            if prickle_arena_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - prickle_arena_requirements[0]
                                prickle_arena_requirements[1] = prickle_arena_requirements[2]
                                champion3_rp = champion3_rp + prickle_arena_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = ((DRUID.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = (DRUID.ap + champion3_small_external_buffs[0])
                                ability_data = ["Prickle Arena", "enemy", "AOE", damage_done]
                            else:
                                return
                        if counter == 4:
                            if prickle_arena_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - prickle_arena_requirements[0]
                                prickle_arena_requirements[1] = prickle_arena_requirements[2]
                                champion4_rp = champion4_rp + prickle_arena_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = ((DRUID.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = (DRUID.ap + champion4_small_external_buffs[0])
                                ability_data = ["Prickle Arena", "enemy", "AOE", damage_done]
                            else:
                                return
                        if counter == 5:
                            if prickle_arena_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - prickle_arena_requirements[0]
                                prickle_arena_requirements[1] = prickle_arena_requirements[2]
                                champion5_rp = champion5_rp + prickle_arena_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = ((DRUID.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = (DRUID.ap + champion5_small_external_buffs[0])
                                ability_data = ["Prickle Arena", "enemy", "AOE", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Wound Fissure":
            global wound_fissure_requirements
            if wound_fissure_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == WARLOCK.title:
                        if counter == 1:
                            if wound_fissure_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - wound_fissure_requirements[0]
                                wound_fissure_requirements[1] = wound_fissure_requirements[2]
                                champion1_rp = champion1_rp + wound_fissure_requirements[3]
                                ability_data = ["Wound Fissure", "enemy", "1T"]
                            else:
                                return
                        if counter == 2:
                            if wound_fissure_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - wound_fissure_requirements[0]
                                wound_fissure_requirements[1] = wound_fissure_requirements[2]
                                champion2_rp = champion2_rp + wound_fissure_requirements[3]
                                ability_data = ["Wound Fissure", "enemy", "1T"]
                            else:
                                return
                        if counter == 3:
                            if wound_fissure_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - wound_fissure_requirements[0]
                                wound_fissure_requirements[1] = wound_fissure_requirements[2]
                                champion3_rp = champion3_rp + wound_fissure_requirements[3]
                                ability_data = ["Wound Fissure", "enemy", "1T"]
                            else:
                                return
                        if counter == 4:
                            if wound_fissure_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - wound_fissure_requirements[0]
                                wound_fissure_requirements[1] = wound_fissure_requirements[2]
                                champion4_rp = champion4_rp + wound_fissure_requirements[3]
                                ability_data = ["Wound Fissure", "enemy", "1T"]
                            else:
                                return
                        if counter == 5:
                            if wound_fissure_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - wound_fissure_requirements[0]
                                wound_fissure_requirements[1] = wound_fissure_requirements[2]
                                champion5_rp = champion5_rp + wound_fissure_requirements[3]
                                ability_data = ["Wound Fissure", "enemy", "1T"]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Soul Tap":
            global soul_tap_requirements
            if soul_tap_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == WARLOCK.title:
                        if counter == 1:
                            if soul_tap_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - soul_tap_requirements[0]
                                soul_tap_requirements[1] = soul_tap_requirements[2]
                                champion1_rp = champion1_rp + soul_tap_requirements[3]
                                ability_data = ["Soul Tap", "self"]
                            else:
                                return
                        if counter == 2:
                            if soul_tap_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - soul_tap_requirements[0]
                                soul_tap_requirements[1] = soul_tap_requirements[2]
                                champion2_rp = champion2_rp + soul_tap_requirements[3]
                                ability_data = ["Soul Tap", "self"]
                            else:
                                return
                        if counter == 3:
                            if soul_tap_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - soul_tap_requirements[0]
                                soul_tap_requirements[1] = soul_tap_requirements[2]
                                champion3_rp = champion3_rp + soul_tap_requirements[3]
                                ability_data = ["Soul Tap", "self"]
                            else:
                                return
                        if counter == 4:
                            if soul_tap_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - soul_tap_requirements[0]
                                soul_tap_requirements[1] = soul_tap_requirements[2]
                                champion4_rp = champion4_rp + soul_tap_requirements[3]
                                ability_data = ["Soul Tap", "self"]
                            else:
                                return
                        if counter == 5:
                            if soul_tap_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - soul_tap_requirements[0]
                                soul_tap_requirements[1] = soul_tap_requirements[2]
                                champion5_rp = champion5_rp + soul_tap_requirements[3]
                                ability_data = ["Soul Tap", "self"]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Blood Boil":
            global blood_boil_requirements
            if blood_boil_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == BLOODMANCER.title:
                        if counter == 1:
                            if blood_boil_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - blood_boil_requirements[0]
                                blood_boil_requirements[1] = blood_boil_requirements[2]
                                champion1_rp = champion1_rp + blood_boil_requirements[3]
                                ability_data = ["Blood Boil", "self"]
                            else:
                                return
                        if counter == 2:
                            if blood_boil_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - blood_boil_requirements[0]
                                blood_boil_requirements[1] = blood_boil_requirements[2]
                                champion2_rp = champion2_rp + blood_boil_requirements[3]
                                ability_data = ["Blood Boil", "self"]
                            else:
                                return
                        if counter == 3:
                            if blood_boil_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - blood_boil_requirements[0]
                                blood_boil_requirements[1] = blood_boil_requirements[2]
                                champion3_rp = champion3_rp + blood_boil_requirements[3]
                                ability_data = ["Blood Boil", "self"]
                            else:
                                return
                        if counter == 4:
                            if blood_boil_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - blood_boil_requirements[0]
                                blood_boil_requirements[1] = blood_boil_requirements[2]
                                champion4_rp = champion4_rp + blood_boil_requirements[3]
                                ability_data = ["Blood Boil", "self"]
                            else:
                                return
                        if counter == 5:
                            if blood_boil_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - blood_boil_requirements[0]
                                blood_boil_requirements[1] = blood_boil_requirements[2]
                                champion5_rp = champion5_rp + blood_boil_requirements[3]
                                ability_data = ["Blood Boil", "self"]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Enharden Nerves":
            global enharden_nerves_requirements
            if enharden_nerves_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == BLOODMANCER.title:
                        if counter == 1:
                            if enharden_nerves_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - enharden_nerves_requirements[0]
                                enharden_nerves_requirements[1] = enharden_nerves_requirements[2]
                                champion1_rp = champion1_rp + enharden_nerves_requirements[3]
                                ability_data = ["Enharden Nerves", "self"]
                            else:
                                return
                        if counter == 2:
                            if enharden_nerves_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - enharden_nerves_requirements[0]
                                enharden_nerves_requirements[1] = enharden_nerves_requirements[2]
                                champion2_rp = champion2_rp + enharden_nerves_requirements[3]
                                ability_data = ["Enharden Nerves", "self"]
                            else:
                                return
                        if counter == 3:
                            if enharden_nerves_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - enharden_nerves_requirements[0]
                                enharden_nerves_requirements[1] = enharden_nerves_requirements[2]
                                champion3_rp = champion3_rp + enharden_nerves_requirements[3]
                                ability_data = ["Enharden Nerves", "self"]
                            else:
                                return
                        if counter == 4:
                            if enharden_nerves_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - enharden_nerves_requirements[0]
                                enharden_nerves_requirements[1] = enharden_nerves_requirements[2]
                                champion4_rp = champion4_rp + enharden_nerves_requirements[3]
                                ability_data = ["Enharden Nerves", "self"]
                            else:
                                return
                        if counter == 5:
                            if enharden_nerves_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - enharden_nerves_requirements[0]
                                enharden_nerves_requirements[1] = enharden_nerves_requirements[2]
                                champion5_rp = champion5_rp + enharden_nerves_requirements[3]
                                ability_data = ["Enharden Nerves", "self"]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Aura of Power":
            if aura_of_power_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == PALADIN.title:
                        if counter == 1:
                            if aura_of_power_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - aura_of_power_requirements[0]
                                aura_of_power_requirements[1] = aura_of_power_requirements[2]
                                aura_of_protection_requirements[1] = aura_of_power_requirements[2]
                                champion1_rp = champion1_rp + aura_of_power_requirements[3]
                                ability_data = ["Aura of Power", "ally", "AOE"]
                            else:
                                return
                        if counter == 2:
                            if aura_of_power_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - aura_of_power_requirements[0]
                                aura_of_power_requirements[1] = aura_of_power_requirements[2]
                                aura_of_protection_requirements[1] = aura_of_power_requirements[2]
                                champion2_rp = champion2_rp + aura_of_power_requirements[3]
                                ability_data = ["Aura of Power", "ally", "AOE"]
                            else:
                                return
                        if counter == 3:
                            if aura_of_power_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - aura_of_power_requirements[0]
                                aura_of_power_requirements[1] = aura_of_power_requirements[2]
                                aura_of_protection_requirements[1] = aura_of_power_requirements[2]
                                champion3_rp = champion3_rp + aura_of_power_requirements[3]
                                ability_data = ["Aura of Power", "ally", "AOE"]
                            else:
                                return
                        if counter == 4:
                            if aura_of_power_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - aura_of_power_requirements[0]
                                aura_of_power_requirements[1] = aura_of_power_requirements[2]
                                aura_of_protection_requirements[1] = aura_of_power_requirements[2]
                                champion4_rp = champion4_rp + aura_of_power_requirements[3]
                                ability_data = ["Aura of Power", "ally", "AOE"]
                            else:
                                return
                        if counter == 5:
                            if aura_of_power_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - aura_of_power_requirements[0]
                                aura_of_power_requirements[1] = aura_of_power_requirements[2]
                                aura_of_protection_requirements[1] = aura_of_power_requirements[2]
                                champion5_rp = champion5_rp + aura_of_power_requirements[3]
                                ability_data = ["Aura of Power", "ally", "AOE"]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Aura of Protection":
            if aura_of_protection_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == PALADIN.title:
                        if counter == 1:
                            if aura_of_protection_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - aura_of_protection_requirements[0]
                                aura_of_protection_requirements[1] = aura_of_protection_requirements[2]
                                aura_of_power_requirements[1] = aura_of_protection_requirements[2]
                                champion1_rp = champion1_rp + aura_of_protection_requirements[3]
                                ability_data = ["Aura of Protection", "ally", "AOE"]
                            else:
                                return
                        if counter == 2:
                            if aura_of_protection_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - aura_of_protection_requirements[0]
                                aura_of_protection_requirements[1] = aura_of_protection_requirements[2]
                                aura_of_power_requirements[1] = aura_of_protection_requirements[2]
                                champion2_rp = champion2_rp + aura_of_protection_requirements[3]
                                ability_data = ["Aura of Protection", "ally", "AOE"]
                            else:
                                return
                        if counter == 3:
                            if aura_of_protection_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - aura_of_protection_requirements[0]
                                aura_of_protection_requirements[1] = aura_of_protection_requirements[2]
                                aura_of_power_requirements[1] = aura_of_protection_requirements[2]
                                champion3_rp = champion3_rp + aura_of_protection_requirements[3]
                                ability_data = ["Aura of Protection", "ally", "AOE"]
                            else:
                                return
                        if counter == 4:
                            if aura_of_protection_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - aura_of_protection_requirements[0]
                                aura_of_protection_requirements[1] = aura_of_protection_requirements[2]
                                aura_of_power_requirements[1] = aura_of_protection_requirements[2]
                                champion4_rp = champion4_rp + aura_of_protection_requirements[3]
                                ability_data = ["Aura of Protection", "ally", "AOE"]
                            else:
                                return
                        if counter == 5:
                            if aura_of_protection_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - aura_of_protection_requirements[0]
                                aura_of_protection_requirements[1] = aura_of_protection_requirements[2]
                                aura_of_power_requirements[1] = aura_of_protection_requirements[2]
                                champion5_rp = champion5_rp + aura_of_protection_requirements[3]
                                ability_data = ["Aura of Protection", "ally", "AOE"]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Muscle Enlarger":
            global muscle_enlarger_requirements
            if muscle_enlarger_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == POWER_CONDUIT.title:
                        if counter == 1:
                            if muscle_enlarger_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - muscle_enlarger_requirements[0]
                                muscle_enlarger_requirements[1] = muscle_enlarger_requirements[2]
                                champion1_rp = champion1_rp + muscle_enlarger_requirements[3]
                                ability_data = ["Muscle Enlarger", "ally", "1T"]
                            else:
                                return
                        if counter == 2:
                            if muscle_enlarger_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - muscle_enlarger_requirements[0]
                                muscle_enlarger_requirements[1] = muscle_enlarger_requirements[2]
                                champion2_rp = champion2_rp + muscle_enlarger_requirements[3]
                                ability_data = ["Muscle Enlarger", "ally", "1T"]
                            else:
                                return
                        if counter == 3:
                            if muscle_enlarger_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - muscle_enlarger_requirements[0]
                                muscle_enlarger_requirements[1] = muscle_enlarger_requirements[2]
                                champion3_rp = champion3_rp + muscle_enlarger_requirements[3]
                                ability_data = ["Muscle Enlarger", "ally", "1T"]
                            else:
                                return
                        if counter == 4:
                            if muscle_enlarger_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - muscle_enlarger_requirements[0]
                                muscle_enlarger_requirements[1] = muscle_enlarger_requirements[2]
                                champion4_rp = champion4_rp + muscle_enlarger_requirements[3]
                                ability_data = ["Muscle Enlarger", "ally", "1T"]
                            else:
                                return
                        if counter == 5:
                            if muscle_enlarger_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - muscle_enlarger_requirements[0]
                                muscle_enlarger_requirements[1] = muscle_enlarger_requirements[2]
                                champion5_rp = champion5_rp + muscle_enlarger_requirements[3]
                                ability_data = ["Muscle Enlarger", "ally", "1T"]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Mistic Bloom":
            global mistic_bloom_requirements
            if mistic_bloom_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == POWER_CONDUIT.title:
                        if counter == 1:
                            if mistic_bloom_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - mistic_bloom_requirements[0]
                                mistic_bloom_requirements[1] = mistic_bloom_requirements[2]
                                champion1_rp = champion1_rp + mistic_bloom_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    healing_done = ((500 + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    healing_done = (500 + champion1_small_external_buffs[0])
                                ability_data = ["Mistic Bloom", "ally", "1T", healing_done]
                            else:
                                return
                        if counter == 2:
                            if mistic_bloom_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - mistic_bloom_requirements[0]
                                mistic_bloom_requirements[1] = mistic_bloom_requirements[2]
                                champion2_rp = champion2_rp + mistic_bloom_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    healing_done = ((500 + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    healing_done = (500 + champion2_small_external_buffs[0])
                                ability_data = ["Mistic Bloom", "ally", "1T", healing_done]
                            else:
                                return
                        if counter == 3:
                            if mistic_bloom_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - mistic_bloom_requirements[0]
                                mistic_bloom_requirements[1] = mistic_bloom_requirements[2]
                                champion3_rp = champion3_rp + mistic_bloom_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    healing_done = ((500 + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    healing_done = (500 + champion3_small_external_buffs[0])
                                ability_data = ["Mistic Bloom", "ally", "1T", healing_done]
                            else:
                                return
                        if counter == 4:
                            if mistic_bloom_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - mistic_bloom_requirements[0]
                                mistic_bloom_requirements[1] = mistic_bloom_requirements[2]
                                champion4_rp = champion4_rp + mistic_bloom_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    healing_done = ((500 + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    healing_done = (500 + champion4_small_external_buffs[0])
                                ability_data = ["Mistic Bloom", "ally", "1T", healing_done]
                            else:
                                return
                        if counter == 5:
                            if mistic_bloom_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - mistic_bloom_requirements[0]
                                mistic_bloom_requirements[1] = mistic_bloom_requirements[2]
                                champion5_rp = champion5_rp + mistic_bloom_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    healing_done = ((500 + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    healing_done = (500 + champion5_small_external_buffs[0])
                                ability_data = ["Mistic Bloom", "ally", "1T", healing_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Power Surge":
            global power_surge_requirements
            if power_surge_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == POWER_CONDUIT.title:
                        if counter == 1:
                            if power_surge_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - power_surge_requirements[0]
                                power_surge_requirements[1] = power_surge_requirements[2]
                                champion1_rp = champion1_rp + power_surge_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = ((500 + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = (500 + champion1_small_external_buffs[0])
                                ability_data = ["Power Surge", "enemy", "AOE", damage_done]
                            else:
                                return
                        if counter == 2:
                            if power_surge_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - power_surge_requirements[0]
                                power_surge_requirements[1] = power_surge_requirements[2]
                                champion2_rp = champion2_rp + power_surge_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = ((500 + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = (500 + champion2_small_external_buffs[0])
                                ability_data = ["Power Surge", "enemy", "AOE", damage_done]
                            else:
                                return
                        if counter == 3:
                            if power_surge_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - power_surge_requirements[0]
                                power_surge_requirements[1] = power_surge_requirements[2]
                                champion3_rp = champion3_rp + power_surge_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = ((500 + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = (500 + champion3_small_external_buffs[0])
                                ability_data = ["Power Surge", "enemy", "AOE", damage_done]
                            else:
                                return
                        if counter == 4:
                            if power_surge_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - power_surge_requirements[0]
                                power_surge_requirements[1] = power_surge_requirements[2]
                                champion4_rp = champion4_rp + power_surge_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = ((500 + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = (500 + champion4_small_external_buffs[0])
                                ability_data = ["Power Surge", "enemy", "AOE", damage_done]
                            else:
                                return
                        if counter == 5:
                            if power_surge_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - power_surge_requirements[0]
                                power_surge_requirements[1] = power_surge_requirements[2]
                                champion5_rp = champion5_rp + power_surge_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = ((500 + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = (500 + champion5_small_external_buffs[0])
                                ability_data = ["Power Surge", "enemy", "AOE", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Full Potential":
            global full_potential_requirements
            if full_potential_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == POWER_CONDUIT.title:
                        if counter == 1:
                            if full_potential_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - full_potential_requirements[0]
                                full_potential_requirements[1] = full_potential_requirements[2]
                                champion1_rp = champion1_rp + full_potential_requirements[3]
                                ability_data = ["Full Potential", "ally", "1T"]
                            else:
                                return
                        if counter == 2:
                            if full_potential_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - full_potential_requirements[0]
                                full_potential_requirements[1] = full_potential_requirements[2]
                                champion2_rp = champion2_rp + full_potential_requirements[3]
                                ability_data = ["Full Potential", "ally", "1T"]
                            else:
                                return
                        if counter == 3:
                            if full_potential_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - full_potential_requirements[0]
                                full_potential_requirements[1] = full_potential_requirements[2]
                                champion3_rp = champion3_rp + full_potential_requirements[3]
                                ability_data = ["Full Potential", "ally", "1T"]
                            else:
                                return
                        if counter == 4:
                            if full_potential_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - full_potential_requirements[0]
                                full_potential_requirements[1] = full_potential_requirements[2]
                                champion4_rp = champion4_rp + full_potential_requirements[3]
                                ability_data = ["Full Potential", "ally", "1T"]
                            else:
                                return
                        if counter == 5:
                            if full_potential_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - full_potential_requirements[0]
                                full_potential_requirements[1] = full_potential_requirements[2]
                                champion5_rp = champion5_rp + full_potential_requirements[3]
                                ability_data = ["Full Potential", "ally", "1T"]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Healing Surge":
            global healing_surge_requirements
            if healing_surge_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == EARTH_SPEAKER.title:
                        if counter == 1:
                            if healing_surge_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - healing_surge_requirements[0]
                                healing_surge_requirements[1] = healing_surge_requirements[2]
                                champion1_rp = champion1_rp + healing_surge_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    healing_done = ((300 + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    healing_done = (300 + champion1_small_external_buffs[0])
                                ability_data = ["Healing Surge", "ally", "1T", healing_done]
                            else:
                                return
                        if counter == 2:
                            if healing_surge_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - healing_surge_requirements[0]
                                healing_surge_requirements[1] = healing_surge_requirements[2]
                                champion2_rp = champion2_rp + healing_surge_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    healing_done = ((300 + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    healing_done = (300 + champion2_small_external_buffs[0])
                                ability_data = ["Healing Surge", "ally", "1T", healing_done]
                            else:
                                return
                        if counter == 3:
                            if healing_surge_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - healing_surge_requirements[0]
                                healing_surge_requirements[1] = healing_surge_requirements[2]
                                champion3_rp = champion3_rp + healing_surge_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    healing_done = ((300 + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    healing_done = (300 + champion3_small_external_buffs[0])
                                ability_data = ["Healing Surge", "ally", "1T", healing_done]
                            else:
                                return
                        if counter == 4:
                            if healing_surge_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - healing_surge_requirements[0]
                                healing_surge_requirements[1] = healing_surge_requirements[2]
                                champion4_rp = champion4_rp + healing_surge_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    healing_done = ((300 + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    healing_done = (300 + champion4_small_external_buffs[0])
                                ability_data = ["Healing Surge", "ally", "1T", healing_done]
                            else:
                                return
                        if counter == 5:
                            if healing_surge_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - healing_surge_requirements[0]
                                healing_surge_requirements[1] = healing_surge_requirements[2]
                                champion5_rp = champion5_rp + healing_surge_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    healing_done = ((300 + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    healing_done = (300 + champion5_small_external_buffs[0])
                                ability_data = ["Healing Surge", "ally", "1T", healing_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Rejuvenating Whirlpool":
            global rejuvenating_whirlpool_requirements
            if rejuvenating_whirlpool_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == EARTH_SPEAKER.title:
                        if counter == 1:
                            if rejuvenating_whirlpool_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - rejuvenating_whirlpool_requirements[0]
                                rejuvenating_whirlpool_requirements[1] = rejuvenating_whirlpool_requirements[2]
                                champion1_rp = champion1_rp + rejuvenating_whirlpool_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    healing_done = ((300 + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    healing_done = (300 + champion1_small_external_buffs[0])
                                ability_data = ["Rejuvenating Whirlpool", "ally", "AOE", healing_done]
                            else:
                                return
                        if counter == 2:
                            if rejuvenating_whirlpool_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - rejuvenating_whirlpool_requirements[0]
                                rejuvenating_whirlpool_requirements[1] = rejuvenating_whirlpool_requirements[2]
                                champion2_rp = champion2_rp + rejuvenating_whirlpool_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    healing_done = ((300 + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    healing_done = (300 + champion2_small_external_buffs[0])
                                ability_data = ["Rejuvenating Whirlpool", "ally", "AOE", healing_done]
                            else:
                                return
                        if counter == 3:
                            if rejuvenating_whirlpool_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - rejuvenating_whirlpool_requirements[0]
                                rejuvenating_whirlpool_requirements[1] = rejuvenating_whirlpool_requirements[2]
                                champion3_rp = champion3_rp + rejuvenating_whirlpool_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    healing_done = ((300 + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    healing_done = (300 + champion3_small_external_buffs[0])
                                ability_data = ["Rejuvenating Whirlpool", "ally", "AOE", healing_done]
                            else:
                                return
                        if counter == 4:
                            if rejuvenating_whirlpool_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - rejuvenating_whirlpool_requirements[0]
                                rejuvenating_whirlpool_requirements[1] = rejuvenating_whirlpool_requirements[2]
                                champion4_rp = champion4_rp + rejuvenating_whirlpool_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    healing_done = ((300 + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    healing_done = (300 + champion4_small_external_buffs[0])
                                ability_data = ["Rejuvenating Whirlpool", "ally", "AOE", healing_done]
                            else:
                                return
                        if counter == 5:
                            if rejuvenating_whirlpool_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - rejuvenating_whirlpool_requirements[0]
                                rejuvenating_whirlpool_requirements[1] = rejuvenating_whirlpool_requirements[2]
                                champion5_rp = champion5_rp + rejuvenating_whirlpool_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    healing_done = ((300 + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    healing_done = (300 + champion5_small_external_buffs[0])
                                ability_data = ["Rejuvenating Whirlpool", "ally", "AOE", healing_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Boulder Cocoon":
            global boulder_cocoon_requirements
            if boulder_cocoon_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == EARTH_SPEAKER.title:
                        if counter == 1:
                            if boulder_cocoon_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - boulder_cocoon_requirements[0]
                                boulder_cocoon_requirements[1] = boulder_cocoon_requirements[2]
                                champion1_rp = champion1_rp + boulder_cocoon_requirements[3]
                                ability_data = ["Boulder Cocoon", "ally", "1T"]
                            else:
                                return
                        if counter == 2:
                            if boulder_cocoon_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - boulder_cocoon_requirements[0]
                                boulder_cocoon_requirements[1] = boulder_cocoon_requirements[2]
                                champion2_rp = champion2_rp + boulder_cocoon_requirements[3]
                                ability_data = ["Boulder Cocoon", "ally", "1T"]
                            else:
                                return
                        if counter == 3:
                            if boulder_cocoon_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - boulder_cocoon_requirements[0]
                                boulder_cocoon_requirements[1] = boulder_cocoon_requirements[2]
                                champion3_rp = champion3_rp + boulder_cocoon_requirements[3]
                                ability_data = ["Boulder Cocoon", "ally", "1T"]
                            else:
                                return
                        if counter == 4:
                            if boulder_cocoon_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - boulder_cocoon_requirements[0]
                                boulder_cocoon_requirements[1] = boulder_cocoon_requirements[2]
                                champion4_rp = champion4_rp + boulder_cocoon_requirements[3]
                                ability_data = ["Boulder Cocoon", "ally", "1T"]
                            else:
                                return
                        if counter == 5:
                            if boulder_cocoon_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - boulder_cocoon_requirements[0]
                                boulder_cocoon_requirements[1] = boulder_cocoon_requirements[2]
                                champion5_rp = champion5_rp + boulder_cocoon_requirements[3]
                                ability_data = ["Boulder Cocoon", "ally", "1T"]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Healing Light":
            global healing_light_requirements
            if healing_light_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == PRIEST_OF_THE_DEVOTED.title:
                        if counter == 1:
                            if healing_light_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - healing_light_requirements[0]
                                healing_light_requirements[1] = healing_light_requirements[2]
                                champion1_rp = champion1_rp + healing_light_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    healing_done = ((300 + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    healing_done = (300 + champion1_small_external_buffs[0])
                                ability_data = ["Healing Light", "ally", "1T", healing_done]
                            else:
                                return
                        if counter == 2:
                            if healing_light_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - healing_light_requirements[0]
                                healing_light_requirements[1] = healing_light_requirements[2]
                                champion2_rp = champion2_rp + healing_light_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    healing_done = ((300 + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    healing_done = (300 + champion2_small_external_buffs[0])
                                ability_data = ["Healing Light", "ally", "1T", healing_done]
                            else:
                                return
                        if counter == 3:
                            if healing_light_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - healing_light_requirements[0]
                                healing_light_requirements[1] = healing_light_requirements[2]
                                champion3_rp = champion3_rp + healing_light_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    healing_done = ((300 + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    healing_done = (300 + champion3_small_external_buffs[0])
                                ability_data = ["Healing Light", "ally", "1T", healing_done]
                            else:
                                return
                        if counter == 4:
                            if healing_light_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - healing_light_requirements[0]
                                healing_light_requirements[1] = healing_light_requirements[2]
                                champion4_rp = champion4_rp + healing_light_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    healing_done = ((300 + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    healing_done = (300 + champion4_small_external_buffs[0])
                                ability_data = ["Healing Light", "ally", "1T", healing_done]
                            else:
                                return
                        if counter == 5:
                            if healing_light_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - healing_light_requirements[0]
                                healing_light_requirements[1] = healing_light_requirements[2]
                                champion5_rp = champion5_rp + healing_light_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    healing_done = ((300 + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    healing_done = (300 + champion5_small_external_buffs[0])
                                ability_data = ["Healing Light", "ally", "1T", healing_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Diffracting Nova":
            global diffracting_nova_requirements
            if diffracting_nova_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == PRIEST_OF_THE_DEVOTED.title:
                        if counter == 1:
                            if diffracting_nova_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - diffracting_nova_requirements[0]
                                diffracting_nova_requirements[1] = diffracting_nova_requirements[2]
                                champion1_rp = champion1_rp + diffracting_nova_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = ((300 + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    damage_done = (300 + champion1_small_external_buffs[0])
                                ability_data = ["Diffracting Nova", "enemy", "AOE", damage_done]
                            else:
                                return
                        if counter == 2:
                            if diffracting_nova_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - diffracting_nova_requirements[0]
                                diffracting_nova_requirements[1] = diffracting_nova_requirements[2]
                                champion2_rp = champion2_rp + diffracting_nova_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = ((300 + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = (300 + champion2_small_external_buffs[0])
                                ability_data = ["Diffracting Nova", "enemy", "AOE", damage_done]
                            else:
                                return
                        if counter == 3:
                            if diffracting_nova_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - diffracting_nova_requirements[0]
                                diffracting_nova_requirements[1] = diffracting_nova_requirements[2]
                                champion3_rp = champion3_rp + diffracting_nova_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = ((300 + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = (300 + champion3_small_external_buffs[0])
                                ability_data = ["Diffracting Nova", "enemy", "AOE", damage_done]
                            else:
                                return
                        if counter == 4:
                            if diffracting_nova_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - diffracting_nova_requirements[0]
                                diffracting_nova_requirements[1] = diffracting_nova_requirements[2]
                                champion4_rp = champion4_rp + diffracting_nova_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = ((300 + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = (300 + champion4_small_external_buffs[0])
                                ability_data = ["Diffracting Nova", "enemy", "AOE", damage_done]
                            else:
                                return
                        if counter == 5:
                            if diffracting_nova_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - diffracting_nova_requirements[0]
                                diffracting_nova_requirements[1] = diffracting_nova_requirements[2]
                                champion5_rp = champion5_rp + diffracting_nova_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = ((300 + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = (300 + champion5_small_external_buffs[0])
                                ability_data = ["Diffracting Nova", "enemy", "AOE", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Nanoheal Bots":
            global nanoheal_bots_requirements
            if nanoheal_bots_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == TIME_WALKER.title:
                        if counter == 1:
                            if nanoheal_bots_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - nanoheal_bots_requirements[0]
                                nanoheal_bots_requirements[1] = nanoheal_bots_requirements[2]
                                champion1_rp = champion1_rp + nanoheal_bots_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    healing_done = ((300 + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    healing_done = (300 + champion1_small_external_buffs[0])
                                ability_data = ["Nanoheal Bots", "ally", "AOE", healing_done]
                            else:
                                return
                        if counter == 2:
                            if nanoheal_bots_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - nanoheal_bots_requirements[0]
                                nanoheal_bots_requirements[1] = nanoheal_bots_requirements[2]
                                champion2_rp = champion2_rp + nanoheal_bots_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    healing_done = ((300 + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    healing_done = (300 + champion2_small_external_buffs[0])
                                ability_data = ["Nanoheal Bots", "ally", "AOE", healing_done]
                            else:
                                return
                        if counter == 3:
                            if nanoheal_bots_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - nanoheal_bots_requirements[0]
                                nanoheal_bots_requirements[1] = nanoheal_bots_requirements[2]
                                champion3_rp = champion3_rp + nanoheal_bots_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    healing_done = ((300 + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    healing_done = (300 + champion3_small_external_buffs[0])
                                ability_data = ["Nanoheal Bots", "ally", "AOE", healing_done]
                            else:
                                return
                        if counter == 4:
                            if nanoheal_bots_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - nanoheal_bots_requirements[0]
                                nanoheal_bots_requirements[1] = nanoheal_bots_requirements[2]
                                champion4_rp = champion4_rp + nanoheal_bots_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    healing_done = ((300 + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    healing_done = (300 + champion4_small_external_buffs[0])
                                ability_data = ["Nanoheal Bots", "ally", "AOE", healing_done]
                            else:
                                return
                        if counter == 5:
                            if nanoheal_bots_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - nanoheal_bots_requirements[0]
                                nanoheal_bots_requirements[1] = nanoheal_bots_requirements[2]
                                champion5_rp = champion5_rp + nanoheal_bots_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    healing_done = ((300 + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    healing_done = (300 + champion5_small_external_buffs[0])
                                ability_data = ["Nanoheal Bots", "ally", "AOE", healing_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Reverse Wounds":
            global reverse_wounds_requirements
            if reverse_wounds_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == TIME_WALKER.title:
                        if counter == 1:
                            if reverse_wounds_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - reverse_wounds_requirements[0]
                                reverse_wounds_requirements[1] = reverse_wounds_requirements[2]
                                champion1_rp = champion1_rp + reverse_wounds_requirements[3]
                                ability_data = ["Reverse Wounds", "ally", "1T"]
                            else:
                                return
                        if counter == 2:
                            if reverse_wounds_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - reverse_wounds_requirements[0]
                                reverse_wounds_requirements[1] = reverse_wounds_requirements[2]
                                champion2_rp = champion2_rp + reverse_wounds_requirements[3]
                                ability_data = ["Reverse Wounds", "ally", "1T"]
                            else:
                                return
                        if counter == 3:
                            if reverse_wounds_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - reverse_wounds_requirements[0]
                                reverse_wounds_requirements[1] = reverse_wounds_requirements[2]
                                champion3_rp = champion3_rp + reverse_wounds_requirements[3]
                                ability_data = ["Reverse Wounds", "ally", "1T"]
                            else:
                                return
                        if counter == 4:
                            if reverse_wounds_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - reverse_wounds_requirements[0]
                                reverse_wounds_requirements[1] = reverse_wounds_requirements[2]
                                champion4_rp = champion4_rp + reverse_wounds_requirements[3]
                                ability_data = ["Reverse Wounds", "ally", "1T"]
                            else:
                                return
                        if counter == 5:
                            if reverse_wounds_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - reverse_wounds_requirements[0]
                                reverse_wounds_requirements[1] = reverse_wounds_requirements[2]
                                champion5_rp = champion5_rp + reverse_wounds_requirements[3]
                                ability_data = ["Reverse Wounds", "ally", "1T"]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Alter Time":
            global alter_time_requirements
            if alter_time_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == TIME_WALKER.title:
                        if counter == 1:
                            if alter_time_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - alter_time_requirements[0]
                                alter_time_requirements[1] = alter_time_requirements[2]
                                champion1_rp = champion1_rp + alter_time_requirements[3]
                                ability_data = ["Alter Time", "ally", "AOE"]
                            else:
                                return
                        if counter == 2:
                            if alter_time_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - alter_time_requirements[0]
                                alter_time_requirements[1] = alter_time_requirements[2]
                                champion2_rp = champion2_rp + alter_time_requirements[3]
                                ability_data = ["Alter Time", "ally", "AOE"]
                            else:
                                return
                        if counter == 3:
                            if alter_time_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - alter_time_requirements[0]
                                alter_time_requirements[1] = alter_time_requirements[2]
                                champion3_rp = champion3_rp + alter_time_requirements[3]
                                ability_data = ["Alter Time", "ally", "AOE"]
                            else:
                                return
                        if counter == 4:
                            if alter_time_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - alter_time_requirements[0]
                                alter_time_requirements[1] = alter_time_requirements[2]
                                champion4_rp = champion4_rp + alter_time_requirements[3]
                                ability_data = ["Alter Time", "ally", "AOE"]
                            else:
                                return
                        if counter == 5:
                            if alter_time_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - alter_time_requirements[0]
                                alter_time_requirements[1] = alter_time_requirements[2]
                                champion5_rp = champion5_rp + alter_time_requirements[3]
                                ability_data = ["Alter Time", "ally", "AOE"]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Bandage Wound":
            global bandage_wound_requirements
            if bandage_wound_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == CHILD_OF_MEDICINE.title:
                        if counter == 1:
                            if bandage_wound_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - bandage_wound_requirements[0]
                                bandage_wound_requirements[1] = bandage_wound_requirements[2]
                                champion1_rp = champion1_rp + bandage_wound_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    healing_done = ((CHILD_OF_MEDICINE.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    healing_done = (CHILD_OF_MEDICINE.ap + champion1_small_external_buffs[0])
                                ability_data = ["Bandage Wound", "ally", "1T", healing_done]
                            else:
                                return
                        if counter == 2:
                            if bandage_wound_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - bandage_wound_requirements[0]
                                bandage_wound_requirements[1] = bandage_wound_requirements[2]
                                champion2_rp = champion2_rp + bandage_wound_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    healing_done = ((CHILD_OF_MEDICINE.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    healing_done = (CHILD_OF_MEDICINE.ap + champion2_small_external_buffs[0])
                                ability_data = ["Bandage Wound", "ally", "1T", healing_done]
                            else:
                                return
                        if counter == 3:
                            if bandage_wound_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - bandage_wound_requirements[0]
                                bandage_wound_requirements[1] = bandage_wound_requirements[2]
                                champion3_rp = champion3_rp + bandage_wound_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    healing_done = ((CHILD_OF_MEDICINE.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    healing_done = (CHILD_OF_MEDICINE.ap + champion3_small_external_buffs[0])
                                ability_data = ["Bandage Wound", "ally", "1T", healing_done]
                            else:
                                return
                        if counter == 4:
                            if bandage_wound_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - bandage_wound_requirements[0]
                                bandage_wound_requirements[1] = bandage_wound_requirements[2]
                                champion4_rp = champion4_rp + bandage_wound_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    healing_done = ((CHILD_OF_MEDICINE.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    healing_done = (CHILD_OF_MEDICINE.ap + champion4_small_external_buffs[0])
                                ability_data = ["Bandage Wound", "ally", "1T", healing_done]
                            else:
                                return
                        if counter == 5:
                            if bandage_wound_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - bandage_wound_requirements[0]
                                bandage_wound_requirements[1] = bandage_wound_requirements[2]
                                champion5_rp = champion5_rp + bandage_wound_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    healing_done = ((CHILD_OF_MEDICINE.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    healing_done = (CHILD_OF_MEDICINE.ap + champion5_small_external_buffs[0])
                                ability_data = ["Bandage Wound", "ally", "1T", healing_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Perfected Herbal Tea":
            global Perfected_herbal_tea_requirements
            if Perfected_herbal_tea_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == CHILD_OF_MEDICINE.title:
                        if counter == 1:
                            if Perfected_herbal_tea_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - Perfected_herbal_tea_requirements[0]
                                Perfected_herbal_tea_requirements[1] = Perfected_herbal_tea_requirements[2]
                                champion1_rp = champion1_rp + Perfected_herbal_tea_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    healing_done = ((CHILD_OF_MEDICINE.ap + champion1_small_external_buffs[0]) *
                                                   champion1_big_external_buffs[0])
                                else:
                                    healing_done = (CHILD_OF_MEDICINE.ap + champion1_small_external_buffs[0])
                                ability_data = ["Perfected Herbal Tea", "ally", "1T", healing_done]
                            else:
                                return
                        if counter == 2:
                            if Perfected_herbal_tea_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - Perfected_herbal_tea_requirements[0]
                                Perfected_herbal_tea_requirements[1] = Perfected_herbal_tea_requirements[2]
                                champion2_rp = champion2_rp + Perfected_herbal_tea_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    healing_done = ((CHILD_OF_MEDICINE.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    healing_done = (CHILD_OF_MEDICINE.ap + champion2_small_external_buffs[0])
                                ability_data = ["Perfected Herbal Tea", "ally", "1T", healing_done]
                            else:
                                return
                        if counter == 3:
                            if Perfected_herbal_tea_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - Perfected_herbal_tea_requirements[0]
                                Perfected_herbal_tea_requirements[1] = Perfected_herbal_tea_requirements[2]
                                champion3_rp = champion3_rp + Perfected_herbal_tea_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    healing_done = ((CHILD_OF_MEDICINE.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    healing_done = (CHILD_OF_MEDICINE.ap + champion3_small_external_buffs[0])
                                ability_data = ["Perfected Herbal Tea", "ally", "1T", healing_done]
                            else:
                                return
                        if counter == 4:
                            if Perfected_herbal_tea_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - Perfected_herbal_tea_requirements[0]
                                Perfected_herbal_tea_requirements[1] = Perfected_herbal_tea_requirements[2]
                                champion4_rp = champion4_rp + Perfected_herbal_tea_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    healing_done = ((CHILD_OF_MEDICINE.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    healing_done = (CHILD_OF_MEDICINE.ap + champion4_small_external_buffs[0])
                                ability_data = ["Perfected Herbal Tea", "ally", "1T", healing_done]
                            else:
                                return
                        if counter == 5:
                            if Perfected_herbal_tea_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - Perfected_herbal_tea_requirements[0]
                                Perfected_herbal_tea_requirements[1] = Perfected_herbal_tea_requirements[2]
                                champion5_rp = champion5_rp + Perfected_herbal_tea_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    healing_done = ((CHILD_OF_MEDICINE.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    healing_done = (CHILD_OF_MEDICINE.ap + champion5_small_external_buffs[0])
                                ability_data = ["Perfected Herbal Tea", "ally", "1T", healing_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "G.3.T J.A.X.D":
            global g3t_jaxd_requirements
            if g3t_jaxd_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == CHILD_OF_MEDICINE.title:
                        if counter == 1:
                            if g3t_jaxd_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - g3t_jaxd_requirements[0]
                                g3t_jaxd_requirements[1] = g3t_jaxd_requirements[2]
                                champion1_rp = champion1_rp + g3t_jaxd_requirements[3]
                                ability_data = ["G.3.T J.A.X.D", "ally", "1T"]
                            else:
                                return
                        if counter == 2:
                            if g3t_jaxd_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - g3t_jaxd_requirements[0]
                                g3t_jaxd_requirements[1] = g3t_jaxd_requirements[2]
                                champion2_rp = champion2_rp + g3t_jaxd_requirements[3]
                                ability_data = ["G.3.T J.A.X.D", "ally", "1T"]
                            else:
                                return
                        if counter == 3:
                            if g3t_jaxd_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - g3t_jaxd_requirements[0]
                                g3t_jaxd_requirements[1] = g3t_jaxd_requirements[2]
                                champion3_rp = champion3_rp + g3t_jaxd_requirements[3]
                                ability_data = ["G.3.T J.A.X.D", "ally", "1T"]
                            else:
                                return
                        if counter == 4:
                            if g3t_jaxd_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - g3t_jaxd_requirements[0]
                                g3t_jaxd_requirements[1] = g3t_jaxd_requirements[2]
                                champion4_rp = champion4_rp + g3t_jaxd_requirements[3]
                                ability_data = ["G.3.T J.A.X.D", "ally", "1T"]
                            else:
                                return
                        if counter == 5:
                            if g3t_jaxd_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - g3t_jaxd_requirements[0]
                                g3t_jaxd_requirements[1] = g3t_jaxd_requirements[2]
                                champion5_rp = champion5_rp + g3t_jaxd_requirements[3]
                                ability_data = ["G.3.T J.A.X.D", "ally", "1T"]
                            else:
                                return
                    counter += 1
            else:
                return
        self.player_targetting_AI()
    def rest_button(self):
        global from_rest_button, rest_confirmation_label, rest_confirmation_button, back_button
        if current_turn == "C1":
            attack_button_champion1.destroy()
            special_button_champion1.destroy()
            rest_button_champion1.destroy()
            rest_confirmation_label = tk.Label(dungeon_game_frame,
                                               text="Are you sure you want this champion to rest for their turn?")
            rest_confirmation_label.grid(row=20, column=2, pady=10)
            rest_confirmation_button = tk.Button(dungeon_game_frame, text="Yes", command=lambda: self.champion_rest(1),
                                                 font=self.medium_text_font_bold)
            rest_confirmation_button.grid(row=20, column=1, pady=12)
            back_button = tk.Button(dungeon_game_frame, text="No", command=self.player_combat_champion1,
                                    font=self.medium_text_font_bold)
            back_button.grid(row=20, column=3, pady=12)
            from_rest_button = 1
        if current_turn == "C2":
            attack_button_champion2.destroy()
            special_button_champion2.destroy()
            rest_button_champion2.destroy()
            rest_confirmation_label = tk.Label(dungeon_game_frame,
                                               text="Are you sure you want this champion to rest for their turn?")
            rest_confirmation_label.grid(row=20, column=2, pady=10)
            rest_confirmation_button = tk.Button(dungeon_game_frame, text="Yes", command=lambda: self.champion_rest(2),
                                                 font=self.medium_text_font_bold)
            rest_confirmation_button.grid(row=20, column=1, pady=12)
            back_button = tk.Button(dungeon_game_frame, text="No", command=self.player_combat_champion2,
                                    font=self.medium_text_font_bold)
            back_button.grid(row=20, column=3, pady=12)
            from_rest_button = 1
        if current_turn == "C3":
            attack_button_champion3.destroy()
            special_button_champion3.destroy()
            rest_button_champion3.destroy()
            rest_confirmation_label = tk.Label(dungeon_game_frame,
                                               text="Are you sure you want this champion to rest for their turn?")
            rest_confirmation_label.grid(row=20, column=2, pady=10)
            rest_confirmation_button = tk.Button(dungeon_game_frame, text="Yes", command=lambda: self.champion_rest(3),
                                                 font=self.medium_text_font_bold)
            rest_confirmation_button.grid(row=20, column=1, pady=12)
            back_button = tk.Button(dungeon_game_frame, text="No", command=self.player_combat_champion3,
                                    font=self.medium_text_font_bold)
            back_button.grid(row=20, column=3, pady=12)
            from_rest_button = 1
        if current_turn == "C4":
            attack_button_champion4.destroy()
            special_button_champion4.destroy()
            rest_button_champion4.destroy()
            rest_confirmation_label = tk.Label(dungeon_game_frame,
                                               text="Are you sure you want this champion to rest for their turn?")
            rest_confirmation_label.grid(row=20, column=2, pady=10)
            rest_confirmation_button = tk.Button(dungeon_game_frame, text="Yes", command=lambda: self.champion_rest(4),
                                                 font=self.medium_text_font_bold)
            rest_confirmation_button.grid(row=20, column=1, pady=12)
            back_button = tk.Button(dungeon_game_frame, text="No", command=self.player_combat_champion4,
                                    font=self.medium_text_font_bold)
            back_button.grid(row=20, column=3, pady=12)
            from_rest_button = 1
        if current_turn == "C5":
            attack_button_champion5.destroy()
            special_button_champion5.destroy()
            rest_button_champion5.destroy()
            rest_confirmation_label = tk.Label(dungeon_game_frame,
                                               text="Are you sure you want this champion to rest for their turn?")
            rest_confirmation_label.grid(row=20, column=2, pady=10)
            rest_confirmation_button = tk.Button(dungeon_game_frame, text="Yes", command=lambda: self.champion_rest(5),
                                                 font=self.medium_text_font_bold)
            rest_confirmation_button.grid(row=20, column=1, pady=12)
            back_button = tk.Button(dungeon_game_frame, text="No", command=self.player_combat_champion5,
                                    font=self.medium_text_font_bold)
            back_button.grid(row=20, column=3, pady=12)
            from_rest_button = 1

    def champion_rest(self, champion_position):
        global champion1_hp, champion2_hp, champion3_hp, champion4_hp, champion5_hp, champion1_rp, champion2_rp, champion3_rp, champion4_rp, champion5_rp, from_rest_button, \
            rest_confirmation_label, rest_confirmation_button, back_button
        if champion_position == 1:
            if CHAMPION_1_RPNAME == "Mana":
                champion1_rp += math.ceil(CHAMPION_1_RP * 0.5)
                if champion1_rp > CHAMPION_1_RP:
                    champion1_rp = CHAMPION_1_RP
            champion1_hp += math.ceil(CHAMPION_1_HP * 0.33)
            if champion1_hp > CHAMPION_1_HP:
                champion1_hp = CHAMPION_1_HP
        if champion_position == 2:
            if CHAMPION_2_RPNAME == "Mana":
                champion2_rp += math.ceil(CHAMPION_2_RP * 0.5)
                if champion2_rp > CHAMPION_2_RP:
                    champion2_rp = CHAMPION_2_RP
            champion2_hp += math.ceil(CHAMPION_2_HP * 0.33)
            if champion2_hp > CHAMPION_2_HP:
                champion2_hp = CHAMPION_2_HP
        if champion_position == 3:
            if CHAMPION_3_RPNAME == "Mana":
                champion3_rp += math.ceil(CHAMPION_3_RP * 0.5)
                if champion3_rp > CHAMPION_3_RP:
                    champion3_rp = CHAMPION_3_RP
            champion3_hp += math.ceil(CHAMPION_3_HP * 0.33)
            if champion3_hp > CHAMPION_3_HP:
                champion3_hp = CHAMPION_3_HP
        if champion_position == 4:
            if CHAMPION_4_RPNAME == "Mana":
                champion4_rp += math.ceil(CHAMPION_4_RP * 0.5)
                if champion4_rp > CHAMPION_4_RP:
                    champion4_rp = CHAMPION_4_RP
            champion4_hp += math.ceil(CHAMPION_4_HP * 0.33)
            if champion4_hp > CHAMPION_4_HP:
                champion4_hp = CHAMPION_4_HP
        if champion_position == 5:
            if CHAMPION_5_RPNAME == "Mana":
                champion5_rp += math.ceil(CHAMPION_5_RP * 0.5)
                if champion5_rp > CHAMPION_5_RP:
                    champion5_rp = CHAMPION_5_RP
            champion5_hp += math.ceil(CHAMPION_5_HP * 0.33)
            if champion5_hp > CHAMPION_5_HP:
                champion5_hp = CHAMPION_5_HP
        rest_confirmation_label.destroy()
        rest_confirmation_button.destroy()
        back_button.destroy()
        from_rest_button = 0
        self.next_turn()

    def player_targetting_AI(self):
        global attack_to_target, special_to_target, ai1_attacktarget_frame, ai2_attacktarget_frame, ai3_attacktarget_frame, \
            ai4_attacktarget_frame, ai5_attacktarget_frame, champion1_supporttarget_frame, champion2_supporttarget_frame, \
            champion3_supporttarget_frame, champion4_supporttarget_frame, champion5_supporttarget_frame
        if attack_to_target == 1:
            attack1_button.destroy()
            attack1_button_details.destroy()
            attack2_button.destroy()
            attack2_button_details.destroy()
            attack3_button.destroy()
            attack3_button_details.destroy()
            attack4_button.destroy()
            attack4_button_details.destroy()
            back_button.destroy()
            attack_to_target = 0
        if special_to_target == 1:
            special1_button.destroy()
            special1_button_details.destroy()
            special2_button.destroy()
            special2_button_details.destroy()
            special3_button.destroy()
            special3_button_details.destroy()
            special4_button.destroy()
            special4_button_details.destroy()
            back_button.destroy()
            special_to_target = 0
        if ability_data[1] == "enemy":
            if ability_data[2] == "AOE":
                self.complete_turn()
            else:
                if AI_SPAWNED == 1:
                    ai1_attacktarget_frame = tk.Button(dungeon_game_frame, text=self.target_frame_ai_champion_text("ai", 1),
                                                       command=lambda: self.multi_target_check(1))
                    ai1_attacktarget_frame.grid(row=19, column=2)
                elif AI_SPAWNED == 2:
                    ai1_attacktarget_frame = tk.Button(dungeon_game_frame, text=self.target_frame_ai_champion_text("ai", 1),
                                                       command=lambda: self.multi_target_check(1))
                    ai1_attacktarget_frame.grid(row=19, column=2, sticky="w")
                    ai2_attacktarget_frame = tk.Button(dungeon_game_frame, text=self.target_frame_ai_champion_text("ai", 2),
                                                       command=lambda: self.multi_target_check(2))
                    ai2_attacktarget_frame.grid(row=19, column=2, sticky="e")
                    if ai1_hp == 0:
                        ai1_attacktarget_frame["state"] = 'disable'
                    if ai2_hp == 0:
                        ai2_attacktarget_frame["state"] = 'disable'
                elif AI_SPAWNED == 3:
                    ai1_attacktarget_frame = tk.Button(dungeon_game_frame, text=self.target_frame_ai_champion_text("ai", 1),
                                                       command=lambda: self.multi_target_check(1))
                    ai1_attacktarget_frame.grid(row=19, column=1)
                    ai2_attacktarget_frame = tk.Button(dungeon_game_frame, text=self.target_frame_ai_champion_text("ai", 2),
                                                       command=lambda: self.multi_target_check(2))
                    ai2_attacktarget_frame.grid(row=19, column=2)
                    ai3_attacktarget_frame = tk.Button(dungeon_game_frame, text=self.target_frame_ai_champion_text("ai", 3),
                                                       command=lambda: self.multi_target_check(3))
                    ai3_attacktarget_frame.grid(row=19, column=3)
                    if ai1_hp == 0:
                        ai1_attacktarget_frame["state"] = 'disable'
                    if ai2_hp == 0:
                        ai2_attacktarget_frame["state"] = 'disable'
                    if ai3_hp == 0:
                        ai3_attacktarget_frame["state"] = 'disable'
                elif AI_SPAWNED == 4:
                    ai1_attacktarget_frame = tk.Button(dungeon_game_frame, text=self.target_frame_ai_champion_text("ai", 1),
                                                       command=lambda: self.multi_target_check(1))
                    ai1_attacktarget_frame.grid(row=19, column=1, sticky="e")
                    ai2_attacktarget_frame = tk.Button(dungeon_game_frame, text=self.target_frame_ai_champion_text("ai", 2),
                                                       command=lambda: self.multi_target_check(2))
                    ai2_attacktarget_frame.grid(row=19, column=3, sticky="w")
                    ai3_attacktarget_frame = tk.Button(dungeon_game_frame, text=self.target_frame_ai_champion_text("ai", 3),
                                                       command=lambda: self.multi_target_check(3))
                    ai3_attacktarget_frame.grid(row=20, column=1, sticky="e")
                    ai4_attacktarget_frame = tk.Button(dungeon_game_frame, text=self.target_frame_ai_champion_text("ai", 4),
                                                       command=lambda: self.multi_target_check(4))
                    ai4_attacktarget_frame.grid(row=20, column=3, sticky="w")
                    if ai1_hp == 0:
                        ai1_attacktarget_frame["state"] = 'disable'
                    if ai2_hp == 0:
                        ai2_attacktarget_frame["state"] = 'disable'
                    if ai3_hp == 0:
                        ai3_attacktarget_frame["state"] = 'disable'
                    if ai4_hp == 0:
                        ai4_attacktarget_frame["state"] = 'disable'
                elif AI_SPAWNED == 5:
                    ai1_attacktarget_frame = tk.Button(dungeon_game_frame, text=self.target_frame_ai_champion_text("ai", 1),
                                                       command=lambda: self.multi_target_check(1))
                    ai1_attacktarget_frame.grid(row=19, column=1)
                    ai2_attacktarget_frame = tk.Button(dungeon_game_frame, text=self.target_frame_ai_champion_text("ai", 2),
                                                       command=lambda: self.multi_target_check(2))
                    ai2_attacktarget_frame.grid(row=19, column=1, sticky="e")
                    ai3_attacktarget_frame = tk.Button(dungeon_game_frame, text=self.target_frame_ai_champion_text("ai", 3),
                                                       command=lambda: self.multi_target_check(3))
                    ai3_attacktarget_frame.grid(row=19, column=2)
                    ai4_attacktarget_frame = tk.Button(dungeon_game_frame, text=self.target_frame_ai_champion_text("ai", 4),
                                                       command=lambda: self.multi_target_check(4))
                    ai4_attacktarget_frame.grid(row=19, column=3, sticky="w")
                    ai5_attacktarget_frame = tk.Button(dungeon_game_frame, text=self.target_frame_ai_champion_text("ai", 5),
                                                       command=lambda: self.multi_target_check(5))
                    ai5_attacktarget_frame.grid(row=19, column=3)
                    if ai1_hp == 0:
                        ai1_attacktarget_frame["state"] = 'disable'
                    if ai2_hp == 0:
                        ai2_attacktarget_frame["state"] = 'disable'
                    if ai3_hp == 0:
                        ai3_attacktarget_frame["state"] = 'disable'
                    if ai4_hp == 0:
                        ai4_attacktarget_frame["state"] = 'disable'
                    if ai5_hp == 0:
                        ai5_attacktarget_frame["state"] = 'disable'
        if ability_data[1] == "ally":
            if ability_data[2] == "AOE":
                self.complete_turn()
            else:
                champion1_supporttarget_frame = tk.Button(dungeon_game_frame,
                                                          text=self.target_frame_ai_champion_text("champion", 1))
                champion1_supporttarget_frame.grid(row=19, column=1)
                champion2_supporttarget_frame = tk.Button(dungeon_game_frame,
                                                          text=self.target_frame_ai_champion_text("champion", 2))
                champion2_supporttarget_frame.grid(row=19, column=2)
                champion3_supporttarget_frame = tk.Button(dungeon_game_frame,
                                                          text=self.target_frame_ai_champion_text("champion", 3))
                champion3_supporttarget_frame.grid(row=19, column=3)
                champion4_supporttarget_frame = tk.Button(dungeon_game_frame,
                                                          text=self.target_frame_ai_champion_text("champion", 4))
                champion4_supporttarget_frame.grid(row=19, column=1, sticky="e")
                champion5_supporttarget_frame = tk.Button(dungeon_game_frame,
                                                          text=self.target_frame_ai_champion_text("champion", 5))
                champion5_supporttarget_frame.grid(row=19, column=3, sticky="w")
                if champion1_hp == 0:
                    champion1_supporttarget_frame["state"] = 'disable'
                if champion2_hp == 0:
                    champion2_supporttarget_frame["state"] = 'disable'
                if champion3_hp == 0:
                    champion3_supporttarget_frame["state"] = 'disable'
                if champion4_hp == 0:
                    champion4_supporttarget_frame["state"] = 'disable'
                if champion5_hp == 0:
                    champion5_supporttarget_frame["state"] = 'disable'
        if ability_data[1] == "self":
            self.complete_turn()

    def multi_target_check(self, target):
        global ai1_attacktarget_frame, ai2_attacktarget_frame, ai3_attacktarget_frame, \
        ai4_attacktarget_frame, ai5_attacktarget_frame, target_list
        target_list = []
        target_list.append(target)
        if ability_data[2] == "1T":
            self.complete_turn()
        if ability_data[2] == "2T":
            self.clean_up()
            if AI_SPAWNED == 1:
                self.complete_turn()
            elif AI_SPAWNED == 2:
                ai1_attacktarget_frame = tk.Button(dungeon_game_frame, text=self.target_frame_ai_champion_text("ai", 1),
                                                   command=lambda: self.put_2nd_target_in_list(1))
                ai1_attacktarget_frame.grid(row=19, column=2, sticky="w")
                ai2_attacktarget_frame = tk.Button(dungeon_game_frame, text=self.target_frame_ai_champion_text("ai", 2),
                                                   command=lambda: self.put_2nd_target_in_list(2))
                ai2_attacktarget_frame.grid(row=19, column=2, sticky="e")
                if ai1_hp == 0:
                    ai1_attacktarget_frame["state"] = 'disable'
                if ai2_hp == 0:
                    ai2_attacktarget_frame["state"] = 'disable'
                if target == 1:
                    ai1_attacktarget_frame["state"] = 'disable'
                elif target == 2:
                    ai2_attacktarget_frame["state"] = 'disable'
            elif AI_SPAWNED == 3:
                ai1_attacktarget_frame = tk.Button(dungeon_game_frame, text=self.target_frame_ai_champion_text("ai", 1),
                                                   command=lambda: self.put_2nd_target_in_list(1))
                ai1_attacktarget_frame.grid(row=19, column=1)
                ai2_attacktarget_frame = tk.Button(dungeon_game_frame, text=self.target_frame_ai_champion_text("ai", 2),
                                                   command=lambda: self.put_2nd_target_in_list(2))
                ai2_attacktarget_frame.grid(row=19, column=2)
                ai3_attacktarget_frame = tk.Button(dungeon_game_frame, text=self.target_frame_ai_champion_text("ai", 3),
                                                   command=lambda: self.put_2nd_target_in_list(3))
                ai3_attacktarget_frame.grid(row=19, column=3)
                if ai1_hp == 0:
                    ai1_attacktarget_frame["state"] = 'disable'
                if ai2_hp == 0:
                    ai2_attacktarget_frame["state"] = 'disable'
                if ai3_hp == 0:
                    ai3_attacktarget_frame["state"] = 'disable'
                if target == 1:
                    ai1_attacktarget_frame["state"] = 'disable'
                elif target == 2:
                    ai2_attacktarget_frame["state"] = 'disable'
                elif target == 3:
                    ai3_attacktarget_frame["state"] = 'disable'
            elif AI_SPAWNED == 4:
                ai1_attacktarget_frame = tk.Button(dungeon_game_frame, text=self.target_frame_ai_champion_text("ai", 1),
                                                   command=lambda: self.put_2nd_target_in_list(1))
                ai1_attacktarget_frame.grid(row=19, column=1, sticky="e")
                ai2_attacktarget_frame = tk.Button(dungeon_game_frame, text=self.target_frame_ai_champion_text("ai", 2),
                                                   command=lambda: self.put_2nd_target_in_list(2))
                ai2_attacktarget_frame.grid(row=19, column=3, sticky="w")
                ai3_attacktarget_frame = tk.Button(dungeon_game_frame, text=self.target_frame_ai_champion_text("ai", 3),
                                                   command=lambda: self.put_2nd_target_in_list(3))
                ai3_attacktarget_frame.grid(row=20, column=1, sticky="e")
                ai4_attacktarget_frame = tk.Button(dungeon_game_frame, text=self.target_frame_ai_champion_text("ai", 4),
                                                   command=lambda: self.put_2nd_target_in_list(4))
                ai4_attacktarget_frame.grid(row=20, column=3, sticky="w")
                if ai1_hp == 0:
                    ai1_attacktarget_frame["state"] = 'disable'
                if ai2_hp == 0:
                    ai2_attacktarget_frame["state"] = 'disable'
                if ai3_hp == 0:
                    ai3_attacktarget_frame["state"] = 'disable'
                if ai4_hp == 0:
                    ai4_attacktarget_frame["state"] = 'disable'
                if target == 1:
                    ai1_attacktarget_frame["state"] = 'disable'
                elif target == 2:
                    ai2_attacktarget_frame["state"] = 'disable'
                elif target == 3:
                    ai3_attacktarget_frame["state"] = 'disable'
                elif target == 4:
                    ai4_attacktarget_frame["state"] = 'disable'
            elif AI_SPAWNED == 5:
                ai1_attacktarget_frame = tk.Button(dungeon_game_frame, text=self.target_frame_ai_champion_text("ai", 1),
                                                   command=lambda: self.put_2nd_target_in_list(1))
                ai1_attacktarget_frame.grid(row=19, column=1)
                ai2_attacktarget_frame = tk.Button(dungeon_game_frame, text=self.target_frame_ai_champion_text("ai", 2),
                                                   command=lambda: self.put_2nd_target_in_list(2))
                ai2_attacktarget_frame.grid(row=19, column=1, sticky="e")
                ai3_attacktarget_frame = tk.Button(dungeon_game_frame, text=self.target_frame_ai_champion_text("ai", 3),
                                                   command=lambda: self.put_2nd_target_in_list(3))
                ai3_attacktarget_frame.grid(row=19, column=2)
                ai4_attacktarget_frame = tk.Button(dungeon_game_frame, text=self.target_frame_ai_champion_text("ai", 4),
                                                   command=lambda: self.put_2nd_target_in_list(4))
                ai4_attacktarget_frame.grid(row=19, column=3, sticky="w")
                ai5_attacktarget_frame = tk.Button(dungeon_game_frame, text=self.target_frame_ai_champion_text("ai", 5),
                                                   command=lambda: self.put_2nd_target_in_list(5))
                ai5_attacktarget_frame.grid(row=19, column=3)
                if ai1_hp == 0:
                    ai1_attacktarget_frame["state"] = 'disable'
                if ai2_hp == 0:
                    ai2_attacktarget_frame["state"] = 'disable'
                if ai3_hp == 0:
                    ai3_attacktarget_frame["state"] = 'disable'
                if ai4_hp == 0:
                    ai4_attacktarget_frame["state"] = 'disable'
                if ai5_hp == 0:
                    ai5_attacktarget_frame["state"] = 'disable'
                if target == 1:
                    ai1_attacktarget_frame["state"] = 'disable'
                elif target == 2:
                    ai2_attacktarget_frame["state"] = 'disable'
                elif target == 3:
                    ai3_attacktarget_frame["state"] = 'disable'
                elif target == 4:
                    ai4_attacktarget_frame["state"] = 'disable'
                elif target == 5:
                    ai5_attacktarget_frame["state"] = 'disable'

    def put_2nd_target_in_list(self, target2):
        global target_list
        target_list.append(target2)
        self.complete_turn()
    def complete_turn(self):
        if ability_data[1] == "enemy":
            self.finalise_damage_dealt()
        if ability_data[1] == "ally":
            self.finalise_healing_done()
        if ability_data[1] == "self":
            self.finalise_self_buff()
        self.clean_up()
        self.next_turn()

    def finalise_damage_dealt(self):
        global ai1_hp, ai2_hp, ai3_hp, ai4_hp, ai5_hp, champion1_hp, champion2_hp, champion3_hp, champion4_hp, champion5_hp
        counter = 0
        if ability_data[0] == "Palm Strike":
            if 1 in target_list:
                ai1_hp = ai1_hp - ability_data[3]
                self.apply_taunt(1, MONK.title, 2)
            if 2 in target_list:
                ai2_hp = ai2_hp - ability_data[3]
                self.apply_taunt(2, MONK.title, 2)
            if 3 in target_list:
                ai3_hp = ai3_hp - ability_data[3]
                self.apply_taunt(3, MONK.title, 2)
            if 4 in target_list:
                ai4_hp = ai4_hp - ability_data[3]
                self.apply_taunt(4, MONK.title, 2)
            if 5 in target_list:
                ai5_hp = ai5_hp - ability_data[3]
                self.apply_taunt(5, MONK.title, 2)
        elif ability_data[0] == "Leg Sweep":
            if 1 in target_list:
                ai1_hp = ai1_hp - ability_data[3]
                self.apply_stun(1, 1)
            if 2 in target_list:
                ai2_hp = ai2_hp - ability_data[3]
                self.apply_stun(2, 1)
            if 3 in target_list:
                ai3_hp = ai3_hp - ability_data[3]
                self.apply_stun(3, 1)
            if 4 in target_list:
                ai4_hp = ai4_hp - ability_data[3]
                self.apply_stun(4, 1)
            if 5 in target_list:
                ai5_hp = ai5_hp - ability_data[3]
                self.apply_stun(5, 1)
        elif ability_data[0] == "Pressure Points":
            if 1 in target_list:
                if ai1_hp < AI_GROUP_HP * 0.2:
                    ai1_hp = 0
                else:
                    self.apply_stun(1, 3)
            if 2 in target_list:
                if ai2_hp < AI_GROUP_HP * 0.2:
                    ai2_hp = 0
                else:
                    self.apply_stun(2, 3)
            if 3 in target_list:
                if ai3_hp < AI_GROUP_HP * 0.2:
                    ai3_hp = 0
                else:
                    self.apply_stun(3, 3)
            if 4 in target_list:
                if ai4_hp < AI_GROUP_HP * 0.2:
                    ai4_hp = 0
                else:
                    self.apply_stun(4, 3)
            if 5 in target_list:
                if ai5_hp < AI_GROUP_HP * 0.2:
                    ai5_hp = 0
                else:
                    self.apply_stun(5, 3)
        elif ability_data[0] == "Bloodthirst":
            if 1 in target_list:
                ai1_hp = ai1_hp - ability_data[3]
                for champions in CHAMPION_LIST:
                    counter += 1
                    if champions == BARBARIAN.title:
                        if counter == 1:
                            champion1_hp = champion1_hp + math.ceil(ability_data[3] / 2)
                            if champion1_hp > CHAMPION_1_HP:
                                 champion1_hp = CHAMPION_1_HP
                        elif counter == 2:
                            champion2_hp = champion2_hp + math.ceil(ability_data[3] / 2)
                            if champion2_hp > CHAMPION_2_HP:
                                 champion2_hp = CHAMPION_2_HP
                        elif counter == 3:
                            champion3_hp = champion3_hp + math.ceil(ability_data[3] / 2)
                            if champion3_hp > CHAMPION_3_HP:
                                 champion3_hp = CHAMPION_3_HP
                        elif counter == 4:
                            champion4_hp = champion4_hp + math.ceil(ability_data[3] / 2)
                            if champion4_hp > CHAMPION_4_HP:
                                 champion4_hp = CHAMPION_4_HP
                        elif counter == 5:
                            champion5_hp = champion5_hp + math.ceil(ability_data[3] / 2)
                            if champion5_hp > CHAMPION_5_HP:
                                champion5_hp = CHAMPION_5_HP
            if 2 in target_list:
                ai2_hp = ai2_hp - ability_data[3]
                for champions in CHAMPION_LIST:
                    counter += 1
                    if champions == BARBARIAN.title:
                        if counter == 1:
                            champion1_hp = champion1_hp + math.ceil(ability_data[3] / 2)
                            if champion1_hp > CHAMPION_1_HP:
                                champion1_hp = CHAMPION_1_HP
                        elif counter == 2:
                            champion2_hp = champion2_hp + math.ceil(ability_data[3] / 2)
                            if champion2_hp > CHAMPION_2_HP:
                                champion2_hp = CHAMPION_2_HP
                        elif counter == 3:
                            champion3_hp = champion3_hp + math.ceil(ability_data[3] / 2)
                            if champion3_hp > CHAMPION_3_HP:
                                champion3_hp = CHAMPION_3_HP
                        elif counter == 4:
                            champion4_hp = champion4_hp + math.ceil(ability_data[3] / 2)
                            if champion4_hp > CHAMPION_4_HP:
                                champion4_hp = CHAMPION_4_HP
                        elif counter == 5:
                            champion5_hp = champion5_hp + math.ceil(ability_data[3] / 2)
                            if champion5_hp > CHAMPION_5_HP:
                                champion5_hp = CHAMPION_5_HP
            if 3 in target_list:
                ai3_hp = ai3_hp - ability_data[3]
                for champions in CHAMPION_LIST:
                    counter += 1
                    if champions == BARBARIAN.title:
                        if counter == 1:
                            champion1_hp = champion1_hp + math.ceil(ability_data[3] / 2)
                            if champion1_hp > CHAMPION_1_HP:
                                champion1_hp = CHAMPION_1_HP
                        elif counter == 2:
                            champion2_hp = champion2_hp + math.ceil(ability_data[3] / 2)
                            if champion2_hp > CHAMPION_2_HP:
                                champion2_hp = CHAMPION_2_HP
                        elif counter == 3:
                            champion3_hp = champion3_hp + math.ceil(ability_data[3] / 2)
                            if champion3_hp > CHAMPION_3_HP:
                                champion3_hp = CHAMPION_3_HP
                        elif counter == 4:
                            champion4_hp = champion4_hp + math.ceil(ability_data[3] / 2)
                            if champion4_hp > CHAMPION_4_HP:
                                champion4_hp = CHAMPION_4_HP
                        elif counter == 5:
                            champion5_hp = champion5_hp + math.ceil(ability_data[3] / 2)
                            if champion5_hp > CHAMPION_5_HP:
                                champion5_hp = CHAMPION_5_HP
            if 4 in target_list:
                ai4_hp = ai4_hp - ability_data[3]
                for champions in CHAMPION_LIST:
                    counter += 1
                    if champions == BARBARIAN.title:
                        if counter == 1:
                            champion1_hp = champion1_hp + math.ceil(ability_data[3] / 2)
                            if champion1_hp > CHAMPION_1_HP:
                                champion1_hp = CHAMPION_1_HP
                        elif counter == 2:
                            champion2_hp = champion2_hp + math.ceil(ability_data[3] / 2)
                            if champion2_hp > CHAMPION_2_HP:
                                champion2_hp = CHAMPION_2_HP
                        elif counter == 3:
                            champion3_hp = champion3_hp + math.ceil(ability_data[3] / 2)
                            if champion3_hp > CHAMPION_3_HP:
                                champion3_hp = CHAMPION_3_HP
                        elif counter == 4:
                            champion4_hp = champion4_hp + math.ceil(ability_data[3] / 2)
                            if champion4_hp > CHAMPION_4_HP:
                                champion4_hp = CHAMPION_4_HP
                        elif counter == 5:
                            champion5_hp = champion5_hp + math.ceil(ability_data[3] / 2)
                            if champion5_hp > CHAMPION_5_HP:
                                champion5_hp = CHAMPION_5_HP
            if 5 in target_list:
                ai5_hp = ai5_hp - ability_data[3]
                for champions in CHAMPION_LIST:
                    counter += 1
                    if champions == BARBARIAN.title:
                        if counter == 1:
                            champion1_hp = champion1_hp + math.ceil(ability_data[3] / 2)
                            if champion1_hp > CHAMPION_1_HP:
                                champion1_hp = CHAMPION_1_HP
                        elif counter == 2:
                            champion2_hp = champion2_hp + math.ceil(ability_data[3] / 2)
                            if champion2_hp > CHAMPION_2_HP:
                                champion2_hp = CHAMPION_2_HP
                        elif counter == 3:
                            champion3_hp = champion3_hp + math.ceil(ability_data[3] / 2)
                            if champion3_hp > CHAMPION_3_HP:
                                champion3_hp = CHAMPION_3_HP
                        elif counter == 4:
                            champion4_hp = champion4_hp + math.ceil(ability_data[3] / 2)
                            if champion4_hp > CHAMPION_4_HP:
                                champion4_hp = CHAMPION_4_HP
                        elif counter == 5:
                            champion5_hp = champion5_hp + math.ceil(ability_data[3] / 2)
                            if champion5_hp > CHAMPION_5_HP:
                                champion5_hp = CHAMPION_5_HP
        elif ability_data[0] == "Pulverize":
            if 1 in target_list:
                ai1_hp = ai1_hp - ability_data[3]
                self.apply_taunt(1,BARBARIAN.title, 2)
            if 2 in target_list:
                ai2_hp = ai2_hp - ability_data[3]
                self.apply_taunt(2, BARBARIAN.title, 2)
            if 3 in target_list:
                ai3_hp = ai3_hp - ability_data[3]
                self.apply_taunt(3, BARBARIAN.title, 2)
            if 4 in target_list:
                ai4_hp = ai4_hp - ability_data[3]
                self.apply_taunt(4, BARBARIAN.title, 2)
            if 5 in target_list:
                ai5_hp = ai5_hp - ability_data[3]
                self.apply_taunt(5, BARBARIAN.title, 2)
        elif ability_data[0] == "Shield Bash":
            if 1 in target_list:
                ai1_hp = ai1_hp - ability_data[3]
                self.apply_weakness(1, 2)
            if 2 in target_list:
                ai2_hp = ai2_hp - ability_data[3]
                self.apply_weakness(2, 2)
            if 3 in target_list:
                ai3_hp = ai3_hp - ability_data[3]
                self.apply_weakness(3, 2)
            if 4 in target_list:
                ai4_hp = ai4_hp - ability_data[3]
                self.apply_weakness(4, 2)
            if 5 in target_list:
                ai5_hp = ai5_hp - ability_data[3]
                self.apply_weakness(5, 2)
        elif ability_data[0] == "Trainwreck":
            if 1 in target_list:
                ai1_hp = ai1_hp - ability_data[3]
            if 2 in target_list:
                ai2_hp = ai2_hp - ability_data[3]
            if 3 in target_list:
                ai3_hp = ai3_hp - ability_data[3]
            if 4 in target_list:
                ai4_hp = ai4_hp - ability_data[3]
            if 5 in target_list:
                ai5_hp = ai5_hp - ability_data[3]
        elif ability_data[0] == "Pierce":
            if 1 in target_list:
                ai1_hp = ai1_hp - ability_data[3]
            if 2 in target_list:
                ai2_hp = ai2_hp - ability_data[3]
            if 3 in target_list:
                ai3_hp = ai3_hp - ability_data[3]
            if 4 in target_list:
                ai4_hp = ai4_hp - ability_data[3]
            if 5 in target_list:
                ai5_hp = ai5_hp - ability_data[3]
        elif ability_data[0] == "Disruptive Slash":
            if 1 in target_list:
                ai1_hp = ai1_hp - ability_data[3]
                self.apply_stun(1, 1)
            if 2 in target_list:
                ai2_hp = ai2_hp - ability_data[3]
                self.apply_stun(2, 1)
            if 3 in target_list:
                ai3_hp = ai3_hp - ability_data[3]
                self.apply_stun(3, 1)
            if 4 in target_list:
                ai4_hp = ai4_hp - ability_data[3]
                self.apply_stun(4, 1)
            if 5 in target_list:
                ai5_hp = ai5_hp - ability_data[3]
                self.apply_stun(5, 1)
        elif ability_data[0] == "Raging Blow":
            if reckless_flurry_requirements[1] != 0:
                if AI_SPAWNED == 1:
                    ai1_hp = ai1_hp - ability_data[3]
                if AI_SPAWNED == 2:
                    ai1_hp = ai1_hp - ability_data[3]
                    ai2_hp = ai2_hp - ability_data[3]
                if AI_SPAWNED == 3:
                    ai1_hp = ai1_hp - ability_data[3]
                    ai2_hp = ai2_hp - ability_data[3]
                    ai3_hp = ai3_hp - ability_data[3]
                if AI_SPAWNED == 4:
                    ai1_hp = ai1_hp - ability_data[3]
                    ai2_hp = ai2_hp - ability_data[3]
                    ai3_hp = ai3_hp - ability_data[3]
                    ai4_hp = ai4_hp - ability_data[3]
                if AI_SPAWNED == 5:
                    ai1_hp = ai1_hp - ability_data[3]
                    ai2_hp = ai2_hp - ability_data[3]
                    ai3_hp = ai3_hp - ability_data[3]
                    ai4_hp = ai4_hp - ability_data[3]
                    ai5_hp = ai5_hp - ability_data[3]
            else:
                if 1 in target_list:
                    ai1_hp = ai1_hp - ability_data[3]
                if 2 in target_list:
                    ai2_hp = ai2_hp - ability_data[3]
                if 3 in target_list:
                    ai3_hp = ai3_hp - ability_data[3]
                if 4 in target_list:
                    ai4_hp = ai4_hp - ability_data[3]
                if 5 in target_list:
                    ai5_hp = ai5_hp - ability_data[3]
        elif ability_data[0] == "Rampage":
            if reckless_flurry_requirements[1] != 0:
                if AI_SPAWNED == 1:
                    ai1_hp = ai1_hp - ability_data[3]
                if AI_SPAWNED == 2:
                    ai1_hp = ai1_hp - ability_data[3]
                    ai2_hp = ai2_hp - ability_data[3]
                if AI_SPAWNED == 3:
                    ai1_hp = ai1_hp - ability_data[3]
                    ai2_hp = ai2_hp - ability_data[3]
                    ai3_hp = ai3_hp - ability_data[3]
                if AI_SPAWNED == 4:
                    ai1_hp = ai1_hp - ability_data[3]
                    ai2_hp = ai2_hp - ability_data[3]
                    ai3_hp = ai3_hp - ability_data[3]
                    ai4_hp = ai4_hp - ability_data[3]
                if AI_SPAWNED == 5:
                    ai1_hp = ai1_hp - ability_data[3]
                    ai2_hp = ai2_hp - ability_data[3]
                    ai3_hp = ai3_hp - ability_data[3]
                    ai4_hp = ai4_hp - ability_data[3]
                    ai5_hp = ai5_hp - ability_data[3]
            else:
                if 1 in target_list:
                    ai1_hp = ai1_hp - ability_data[3]
                if 2 in target_list:
                    ai2_hp = ai2_hp - ability_data[3]
                if 3 in target_list:
                    ai3_hp = ai3_hp - ability_data[3]
                if 4 in target_list:
                    ai4_hp = ai4_hp - ability_data[3]
                if 5 in target_list:
                    ai5_hp = ai5_hp - ability_data[3]
        elif ability_data[0] == "Serrated Slash":
            if 1 in target_list:
                ai1_hp = ai1_hp - ability_data[3]
                self.serrated_slash_dot(1, 1)
            if 2 in target_list:
                ai2_hp = ai2_hp - ability_data[3]
                self.serrated_slash_dot(1, 1)
            if 3 in target_list:
                ai3_hp = ai3_hp - ability_data[3]
                self.serrated_slash_dot(1, 1)
            if 4 in target_list:
                ai4_hp = ai4_hp - ability_data[3]
                self.serrated_slash_dot(1, 1)
            if 5 in target_list:
                ai5_hp = ai5_hp - ability_data[3]
                self.serrated_slash_dot(1, 1)
        elif ability_data[0] == "Eviscerate":
            if 1 in target_list:
                ai1_hp = ai1_hp - ability_data[3]
                self.eviscerate_dot(1, 3)
            if 2 in target_list:
                ai2_hp = ai2_hp - ability_data[3]
                self.eviscerate_dot(2, 3)
            if 3 in target_list:
                ai3_hp = ai3_hp - ability_data[3]
                self.eviscerate_dot(3, 3)
            if 4 in target_list:
                ai4_hp = ai4_hp - ability_data[3]
                self.eviscerate_dot(4, 3)
            if 5 in target_list:
                ai5_hp = ai5_hp - ability_data[3]
                self.eviscerate_dot(5, 3)
        elif ability_data[0] == "Garrote":
            if 1 in target_list:
                ai1_hp = ai1_hp - ability_data[3]
                self.garrote_dot(1, 2)
            if 2 in target_list:
                ai2_hp = ai2_hp - ability_data[3]
                self.garrote_dot(2, 2)
            if 3 in target_list:
                ai3_hp = ai3_hp - ability_data[3]
                self.garrote_dot(3, 2)
            if 4 in target_list:
                ai4_hp = ai4_hp - ability_data[3]
                self.garrote_dot(4, 2)
            if 5 in target_list:
                ai5_hp = ai5_hp - ability_data[3]
                self.garrote_dot(5, 2)
        elif ability_data[0] == "Exploit Weakness":
            damage_multipler = 0
            if 1 in target_list:
                if len(ai1_statuses) != 0:
                    for status_effect in ai1_statuses:
                        damage_multipler += 1
                ai1_hp = ai1_hp - (ability_data[3] * (1 + (damage_multipler * 0.3)))
            if 2 in target_list:
                for status_effect in ai2_statuses:
                    damage_multipler += 1
                ai2_hp = ai2_hp - (ability_data[3] * (1 + (damage_multipler * 0.3)))
            if 3 in target_list:
                for status_effect in ai3_statuses:
                    damage_multipler += 1
                ai3_hp = ai3_hp - (ability_data[3] * (1 + (damage_multipler * 0.3)))
            if 4 in target_list:
                for status_effect in ai4_statuses:
                    damage_multipler += 1
                ai4_hp = ai4_hp - (ability_data[3] * (1 + (damage_multipler * 0.3)))
            if 5 in target_list:
                for status_effect in ai5_statuses:
                    damage_multipler += 1
                ai5_hp = ai5_hp - (ability_data[3] * (1 + (damage_multipler * 0.3)))
        elif ability_data[0] == "Spear Thrust":
            if 1 in target_list:
                ai1_hp = ai1_hp - ability_data[3]
            if 2 in target_list:
                ai2_hp = ai2_hp - ability_data[3]
            if 3 in target_list:
                ai3_hp = ai3_hp - ability_data[3]
            if 4 in target_list:
                ai4_hp = ai4_hp - ability_data[3]
            if 5 in target_list:
                ai5_hp = ai5_hp - ability_data[3]
        elif ability_data[0] == "Scrap Bomb":
            if AI_SPAWNED == 1:
                ai1_hp = ai1_hp - ability_data[3]
                self.apply_weakness(1, 2)
            if AI_SPAWNED == 3:
                ai1_hp = ai1_hp - ability_data[3]
                ai2_hp = ai2_hp - ability_data[3]
                self.apply_weakness(1, 2)
                self.apply_weakness(2, 2)
            if AI_SPAWNED == 3:
                ai1_hp = ai1_hp - ability_data[3]
                ai2_hp = ai2_hp - ability_data[3]
                ai3_hp = ai3_hp - ability_data[3]
                self.apply_weakness(1, 2)
                self.apply_weakness(2, 2)
                self.apply_weakness(3, 2)
            if AI_SPAWNED == 4:
                ai1_hp = ai1_hp - ability_data[3]
                ai2_hp = ai2_hp - ability_data[3]
                ai3_hp = ai3_hp - ability_data[3]
                ai4_hp = ai4_hp - ability_data[3]
                self.apply_weakness(1, 2)
                self.apply_weakness(2, 2)
                self.apply_weakness(3, 2)
                self.apply_weakness(4, 2)
            if AI_SPAWNED == 5:
                ai1_hp = ai1_hp - ability_data[3]
                ai2_hp = ai2_hp - ability_data[3]
                ai3_hp = ai3_hp - ability_data[3]
                ai4_hp = ai4_hp - ability_data[3]
                ai5_hp = ai5_hp - ability_data[3]
                self.apply_weakness(1, 2)
                self.apply_weakness(2, 2)
                self.apply_weakness(3, 2)
                self.apply_weakness(4, 2)
                self.apply_weakness(5, 2)
        elif ability_data[0] == "Tactical Punch":
            if 1 in target_list:
                if ai1_hp > AI_GROUP_HP * 0.66:
                    ai1_hp = ai1_hp - ability_data[3]
                    self.apply_weakness(1, 1)
                elif ai1_hp < AI_GROUP_HP * 0.66:
                    if ai1_hp > AI_GROUP_HP * 0.33:
                        ai1_hp = ai1_hp - ability_data[3]
                        self.apply_brittle(1, 1)
                    elif ai1_hp < AI_GROUP_HP * 0.33:
                        ai1_hp = ai1_hp - ability_data[3] * 1.5
            if 2 in target_list:
                if ai2_hp > AI_GROUP_HP * 0.66:
                    ai2_hp = ai2_hp - ability_data[3]
                    self.apply_weakness(2, 1)
                elif ai2_hp < AI_GROUP_HP * 0.66:
                    if ai2_hp > AI_GROUP_HP * 0.33:
                        ai2hp = ai2_hp - ability_data[3]
                        self.apply_brittle(2, 1)
                    elif ai2_hp < AI_GROUP_HP * 0.33:
                        ai2_hp = ai2_hp - ability_data[3] * 1.5
            if 3 in target_list:
                if ai3_hp > AI_GROUP_HP * 0.66:
                    ai3_hp = ai3_hp - ability_data[3]
                    self.apply_weakness(3, 1)
                elif ai3_hp < AI_GROUP_HP * 0.66:
                    if ai3_hp > AI_GROUP_HP * 0.33:
                        ai3hp = ai3_hp - ability_data[3]
                        self.apply_brittle(3, 1)
                    elif ai3_hp < AI_GROUP_HP * 0.33:
                        ai3_hp = ai3_hp - ability_data[3] * 1.5
            if 4 in target_list:
                if ai4_hp > AI_GROUP_HP * 0.66:
                    ai4_hp = ai4_hp - ability_data[3]
                    self.apply_weakness(4, 1)
                elif ai4_hp < AI_GROUP_HP * 0.66:
                        if ai4_hp > AI_GROUP_HP * 0.33:
                            ai4hp = ai4_hp - ability_data[3]
                            self.apply_brittle(4, 1)
                        elif ai4_hp < AI_GROUP_HP * 0.33:
                            ai4_hp = ai4_hp - ability_data[3] * 1.5
            if 5 in target_list:
                if ai5_hp > AI_GROUP_HP * 0.66:
                    ai5_hp = ai5_hp - ability_data[3]
                    self.apply_weakness(5, 1)
                elif ai5_hp < AI_GROUP_HP * 0.66:
                    if ai5_hp > AI_GROUP_HP * 0.33:
                        ai5hp = ai5_hp - ability_data[3]
                        self.apply_brittle(5, 1)
                    elif ai5_hp < AI_GROUP_HP * 0.33:
                        ai5_hp = ai5_hp - ability_data[3] * 1.5
        elif ability_data[0] == "Uppercut":
            if 1 in target_list:
                ai1_hp = ai1_hp - ability_data[3] * 1.5
            if 2 in target_list:
                ai2_hp = ai2_hp - ability_data[3] * 1.5
            if 3 in target_list:
                ai3_hp = ai3_hp - ability_data[3] * 1.5
            if 4 in target_list:
                ai4_hp = ai4_hp - ability_data[3] * 1.5
            if 5 in target_list:
                ai5_hp = ai5_hp - ability_data[3] * 1.5
        elif ability_data[0] == "Rushdown":
            ai_list = []
            attacks = ["Tactical Punch", "Uppercut"]
            if AI_SPAWNED == 1:
                ai_list.append(1)
            elif AI_SPAWNED == 2:
                if ai1_hp != 0:
                    ai_list.append(1)
                if ai2_hp != 0:
                    ai_list.append(2)
            elif AI_SPAWNED == 2:
                if ai1_hp != 0:
                    ai_list.append(1)
                if ai2_hp != 0:
                    ai_list.append(2)
            elif AI_SPAWNED == 3:
                if ai1_hp != 0:
                    ai_list.append(1)
                if ai2_hp != 0:
                    ai_list.append(2)
                if ai3_hp != 0:
                    ai_list.append(3)
            elif AI_SPAWNED == 4:
                if ai1_hp != 0:
                    ai_list.append(1)
                if ai2_hp != 0:
                    ai_list.append(2)
                if ai3_hp != 0:
                    ai_list.append(3)
                if ai4_hp != 0:
                    ai_list.append(4)
            elif AI_SPAWNED == 5:
                if ai1_hp != 0:
                    ai_list.append(1)
                if ai2_hp != 0:
                    ai_list.append(2)
                if ai3_hp != 0:
                    ai_list.append(3)
                if ai4_hp != 0:
                    ai_list.append(4)
                if ai5_hp != 0:
                    ai_list.append(5)
            for i in range(5):
                random.shuffle(ai_list)
                random.shuffle(attacks)
                if ai_list[0] == 1:
                    if attacks[0] == "Tactical Punch":
                        if ai1_hp > AI_GROUP_HP * 0.66:
                            ai1_hp = ai1_hp - ability_data[3]
                            self.apply_weakness(1, 1)
                        elif ai1_hp < AI_GROUP_HP * 0.66:
                            if ai1_hp > AI_GROUP_HP * 0.33:
                                ai1_hp = ai1_hp - ability_data[3]
                                self.apply_brittle(1, 1)
                            elif ai1_hp < AI_GROUP_HP * 0.33:
                                ai1_hp = ai1_hp - ability_data[3] * 1.5
                    if attacks[0] == "Uppercut":
                        ai1_hp = ai1_hp - ability_data[3] * 1.5
                if ai_list[0] == 2:
                    if attacks[0] == "Tactical Punch":
                        if ai2_hp > AI_GROUP_HP * 0.66:
                            ai2_hp = ai2_hp - ability_data[3]
                            self.apply_weakness(2, 1)
                        elif ai2_hp < AI_GROUP_HP * 0.66:
                            if ai2_hp > AI_GROUP_HP * 0.33:
                                ai2_hp = ai2_hp - ability_data[3]
                                self.apply_brittle(2, 1)
                            elif ai2_hp < AI_GROUP_HP * 0.33:
                                ai2_hp = ai2_hp - ability_data[3] * 1.5
                    if attacks[0] == "Uppercut":
                        ai2_hp = ai2_hp - ability_data[3] * 1.5
                if ai_list[0] == 3:
                    if attacks[0] == "Tactical Punch":
                        if ai3_hp > AI_GROUP_HP * 0.66:
                            ai3_hp = ai3_hp - ability_data[3]
                            self.apply_weakness(3, 1)
                        elif ai3_hp < AI_GROUP_HP * 0.66:
                            if ai3_hp > AI_GROUP_HP * 0.33:
                                ai3_hp = ai3_hp - ability_data[3]
                                self.apply_brittle(3, 1)
                            elif ai3_hp < AI_GROUP_HP * 0.33:
                                ai3_hp = ai3_hp - ability_data[3] * 1.5
                    if attacks[0] == "Uppercut":
                        ai3_hp = ai3_hp - ability_data[3] * 1.5
                if ai_list[0] == 4:
                    if attacks[0] == "Tactical Punch":
                        if ai4_hp > AI_GROUP_HP * 0.66:
                            ai4_hp = ai4_hp - ability_data[3]
                            self.apply_weakness(4, 1)
                        elif ai4_hp < AI_GROUP_HP * 0.66:
                            if ai4_hp > AI_GROUP_HP * 0.33:
                                ai4_hp = ai4_hp - ability_data[3]
                                self.apply_brittle(4, 1)
                            elif ai4_hp < AI_GROUP_HP * 0.33:
                                ai4_hp = ai4_hp - ability_data[3] * 1.5
                    if attacks[0] == "Uppercut":
                        ai4_hp = ai4_hp - ability_data[3] * 1.5
                if ai_list[0] == 5:
                    if attacks[0] == "Tactical Punch":
                        if ai5_hp > AI_GROUP_HP * 0.66:
                            ai5_hp = ai5_hp - ability_data[3]
                            self.apply_weakness(5, 1)
                        elif ai5_hp < AI_GROUP_HP * 0.66:
                            if ai5_hp > AI_GROUP_HP * 0.33:
                                ai5_hp = ai5_hp - ability_data[3]
                                self.apply_brittle(5, 1)
                            elif ai5_hp < AI_GROUP_HP * 0.33:
                                ai5_hp = ai5_hp - ability_data[3] * 1.5
                    if attacks[0] == "Uppercut":
                        ai5_hp = ai5_hp - ability_data[3] * 1.5
        elif ability_data[0] == "Frost Bolt":
            if 1 in target_list:
                ai1_hp = ai1_hp - ability_data[3]
                self.apply_brittle(1, 2)
            if 2 in target_list:
                ai2_hp = ai2_hp - ability_data[3]
                self.apply_brittle(2, 2)
            if 3 in target_list:
                ai3_hp = ai3_hp - ability_data[3]
                self.apply_brittle(3, 2)
            if 4 in target_list:
                ai4_hp = ai4_hp - ability_data[3]
                self.apply_brittle(4, 2)
            if 5 in target_list:
                ai5_hp = ai5_hp - ability_data[3]
                self.apply_brittle(5, 2)
        elif ability_data[0] == "Fireball":
            if 1 in target_list:
                ai1_hp = ai1_hp - ability_data[3]
                self.apply_burn(1, 2)
            if 2 in target_list:
                ai2_hp = ai2_hp - ability_data[3]
                self.apply_burn(2, 2)
            if 3 in target_list:
                ai3_hp = ai3_hp - ability_data[3]
                self.apply_burn(3, 2)
            if 4 in target_list:
                ai4_hp = ai4_hp - ability_data[3]
                self.apply_burn(4, 2)
            if 5 in target_list:
                ai5_hp = ai5_hp - ability_data[3]
                self.apply_burn(5, 2)
        elif ability_data[0] == "Arcane Brilliance":
            ai_list = []
            attacks = ["Frost Bolt", "Fireball"]
            if AI_SPAWNED == 1:
                ai_list.append(1)
            elif AI_SPAWNED == 2:
                if ai1_hp != 0:
                    ai_list.append(1)
                if ai2_hp != 0:
                    ai_list.append(2)
            elif AI_SPAWNED == 2:
                if ai1_hp != 0:
                    ai_list.append(1)
                if ai2_hp != 0:
                    ai_list.append(2)
            elif AI_SPAWNED == 3:
                if ai1_hp != 0:
                    ai_list.append(1)
                if ai2_hp != 0:
                    ai_list.append(2)
                if ai3_hp != 0:
                    ai_list.append(3)
            elif AI_SPAWNED == 4:
                if ai1_hp != 0:
                    ai_list.append(1)
                if ai2_hp != 0:
                    ai_list.append(2)
                if ai3_hp != 0:
                    ai_list.append(3)
                if ai4_hp != 0:
                    ai_list.append(4)
            elif AI_SPAWNED == 5:
                if ai1_hp != 0:
                    ai_list.append(1)
                if ai2_hp != 0:
                    ai_list.append(2)
                if ai3_hp != 0:
                    ai_list.append(3)
                if ai4_hp != 0:
                    ai_list.append(4)
                if ai5_hp != 0:
                    ai_list.append(5)
            for i in range(5):
                random.shuffle(ai_list)
                random.shuffle(attacks)
                if ai_list[0] == 1:
                    if attacks[0] == "Frost Bolt":
                        ai1_hp = ai1_hp - ability_data[3]
                        self.apply_brittle(1, 2)
                    if attacks[0] == "Fireball":
                        self.apply_burn(1, 2)
                        ai1_hp = ai1_hp - ability_data[3]
                if ai_list[0] == 2:
                    if attacks[0] == "Frost Bolt":
                        ai2_hp = ai2_hp - ability_data[3]
                        self.apply_brittle(2, 2)
                    if attacks[0] == "Fireball":
                        ai2_hp = ai2_hp - ability_data[3]
                        self.apply_burn(2, 2)
                if ai_list[0] == 3:
                    if attacks[0] == "Frost Bolt":
                        ai3_hp = ai3_hp - ability_data[3]
                        self.apply_brittle(3, 2)
                        if attacks[0] == "Fireball":
                            ai3_hp = ai3_hp - ability_data[3]
                            self.apply_burn(3, 2)
                if ai_list[0] == 4:
                    if attacks[0] == "Frost Bolt":
                        ai4_hp = ai4_hp - ability_data[3]
                        self.apply_brittle(4, 2)
                        if attacks[0] == "Fireball":
                            ai4_hp = ai4_hp - ability_data[3]
                            self.apply_burn(4, 2)
                if ai_list[0] == 5:
                    if attacks[0] == "Frost Bolt":
                        ai5_hp = ai5_hp - ability_data[3]
                        self.apply_brittle(5, 2)
                        if attacks[0] == "Fireball":
                            ai5_hp = ai5_hp - ability_data[3]
                            self.apply_burn(5, 2)
        elif ability_data[0] == "Venus-fly Snap":
            if 1 in target_list:
                ai1_hp = ai1_hp - ability_data[3]
            if 2 in target_list:
                ai2_hp = ai2_hp - ability_data[3]
            if 3 in target_list:
                ai3_hp = ai3_hp - ability_data[3]
            if 4 in target_list:
                ai4_hp = ai4_hp - ability_data[3]
            if 5 in target_list:
                ai5_hp = ai5_hp - ability_data[3]
        elif ability_data[0] == "Vine-Swipe":
            if 1 in target_list:
                ai1_hp = ai1_hp - ability_data[3]
            if 2 in target_list:
                ai2_hp = ai2_hp - ability_data[3]
            if 3 in target_list:
                ai3_hp = ai3_hp - ability_data[3]
            if 4 in target_list:
                ai4_hp = ai4_hp - ability_data[3]
            if 5 in target_list:
                ai5_hp = ai5_hp - ability_data[3]
        elif ability_data[0] == "Prickle Arena":
            if AI_SPAWNED == 1:
                self.apply_pricked(1)
            if AI_SPAWNED == 2:
                self.apply_pricked(1)
                self.apply_pricked(2)
            if AI_SPAWNED == 3:
                self.apply_pricked(1)
                self.apply_pricked(2)
                self.apply_pricked(3)
            if AI_SPAWNED == 4:
                self.apply_pricked(1)
                self.apply_pricked(2)
                self.apply_pricked(3)
                self.apply_pricked(4)
            if AI_SPAWNED == 5:
                self.apply_pricked(1)
                self.apply_pricked(2)
                self.apply_pricked(3)
                self.apply_pricked(4)
                self.apply_pricked(5)
        elif ability_data[0] == "Black Bolt":
            global void_infusion_stacks
            if 1 in target_list:
                ai1_hp = ai1_hp - (ability_data[3] + (ability_data[3] * (1 + (void_infusion_stacks * 0.2))))
                void_infusion_stacks = 0
            if 2 in target_list:
                ai2_hp = ai2_hp - (ability_data[3] + (ability_data[3] * (1 + (void_infusion_stacks * 0.2))))
                void_infusion_stacks = 0
            if 3 in target_list:
                ai3_hp = ai3_hp - (ability_data[3] + (ability_data[3] * (1 + (void_infusion_stacks * 0.2))))
                void_infusion_stacks = 0
            if 4 in target_list:
                ai4_hp = ai4_hp - (ability_data[3] + (ability_data[3] * (1 + (void_infusion_stacks * 0.2))))
                void_infusion_stacks = 0
            if 5 in target_list:
                ai5_hp = ai5_hp - (ability_data[3] + (ability_data[3] * (1 + (void_infusion_stacks * 0.2))))
                void_infusion_stacks = 0
        elif ability_data[0] == "Wound Fissure":
            global ai1_burnDot, ai2_burnDot, ai3_burnDot, ai4_burnDot, ai5_burnDot, \
                ai1_SerraSlashDot, ai2_SerraSlashDot, ai3_SerraSlashDot, ai4_SerraSlashDot, ai5_SerraSlashDot, \
                ai1_EviscerDot, ai2_EviscerDot, ai3_EviscerDot, ai4_EviscerDot, ai5_EviscerDot, \
                ai1_garroteDot, ai2_garroteDot, ai3_garroteDot, ai4_garroteDot, ai5_garroteDot
            counter = 0
            if 1 in target_list:
                if ai1_burnDot[1] > 0:
                    while ai1_burnDot[1] > 0:
                        if ai1_hp <= 0:
                            break
                        if counter == 2:
                            break
                        ai1_hp = ai1_hp - ai1_burnDot[0]
                        ai1_burnDot[1] = ai1_burnDot[1] - 1
                        counter += 1
                    counter = 0
                if ai1_SerraSlashDot[1] > 0:
                    while ai1_SerraSlashDot[1] > 0:
                        if ai1_hp <= 0:
                            break
                        if counter == 2:
                            break
                        ai1_hp = ai1_hp - ai1_SerraSlashDot[0]
                        ai1_SerraSlashDot[1] = ai1_SerraSlashDot[1] - 1
                        counter += 1
                    counter = 0
                if ai1_EviscerDot[1] > 0:
                    while ai1_EviscerDot[1] > 0:
                        if ai1_hp <= 0:
                            break
                        if counter == 2:
                            break
                        ai1_hp = ai1_hp - ai1_EviscerDot[0]
                        ai1_EviscerDot[1] = ai1_EviscerDot[1] - 1
                        counter += 1
                    counter = 0
                if ai1_garroteDot[1] > 0:
                    while ai1_garroteDot[1] > 0:
                        if ai1_hp <= 0:
                            break
                        if counter == 2:
                            break
                        ai1_hp = ai1_hp - ai1_garroteDot[0]
                        ai1_garroteDot[1] = ai1_garroteDot[1] - 1
                        counter += 1
                    counter = 0
            if 2 in target_list:
                if ai2_burnDot[1] > 0:
                    while ai2_burnDot[1] > 0:
                        if ai2_hp <= 0:
                            break
                        if counter == 2:
                            break
                        ai2_hp = ai2_hp - ai2_burnDot[0]
                        ai2_burnDot[1] = ai2_burnDot[1] - 1
                        counter += 1
                    counter = 0
                if ai2_SerraSlashDot[1] > 0:
                    while ai2_SerraSlashDot[1] > 0:
                        if ai2_hp <= 0:
                            break
                        if counter == 2:
                            break
                        ai2_hp = ai1_hp - ai2_SerraSlashDot[0]
                        ai2_SerraSlashDot[1] = ai2_SerraSlashDot[1] - 1
                        counter += 1
                    counter = 0
                if ai2_EviscerDot[1] > 0:
                    while ai2_EviscerDot[1] > 0:
                        if ai2_hp <= 0:
                            break
                        if counter == 2:
                            break
                        ai2_hp = ai2_hp - ai2_EviscerDot[0]
                        ai2_EviscerDot[1] = ai2_EviscerDot[1] - 1
                        counter += 1
                    counter = 0
                if ai2_garroteDot[1] > 0:
                    while ai2_garroteDot[1] > 0:
                        if ai2_hp <= 0:
                            break
                        if counter == 2:
                            break
                        ai2_hp = ai1_hp - ai2_garroteDot[0]
                        ai2_garroteDot[1] = ai2_garroteDot[1] - 1
                        counter += 1
                    counter = 0
            if 3 in target_list:
                if ai3_burnDot[1] > 0:
                    while ai3_burnDot[1] > 0:
                        if ai3_hp <= 0:
                            break
                        if counter == 2:
                            break
                        ai3_hp = ai3_hp - ai3_burnDot[0]
                        ai3_burnDot[1] = ai3_burnDot[1] - 1
                        counter += 1
                    counter = 0
                if ai3_SerraSlashDot[1] > 0:
                    while ai3_SerraSlashDot[1] > 0:
                        if ai3_hp <= 0:
                            break
                        if counter == 2:
                            break
                        ai3_hp = ai1_hp - ai3_SerraSlashDot[0]
                        ai3_SerraSlashDot[1] = ai3_SerraSlashDot[1] - 1
                        counter += 1
                    counter = 0
                if ai3_EviscerDot[1] > 0:
                    while ai3_EviscerDot[1] > 0:
                        if ai3_hp <= 0:
                            break
                        if counter == 2:
                            break
                        ai3_hp = ai3_hp - ai3_EviscerDot[0]
                        ai3_EviscerDot[1] = ai3_EviscerDot[1] - 1
                        counter += 1
                    counter = 0
                if ai3_garroteDot[1] > 0:
                    while ai3_garroteDot[1] > 0:
                        if ai3_hp <= 0:
                            break
                        if counter == 2:
                            break
                        ai3_hp = ai1_hp - ai3_garroteDot[0]
                        ai3_garroteDot[1] = ai3_garroteDot[1] - 1
                        counter += 1
                    counter = 0
            if 4 in target_list:
                if ai4_burnDot[1] > 0:
                    while ai4_burnDot[1] > 0:
                        if ai4_hp <= 0:
                            break
                        if counter == 2:
                            break
                        ai4_hp = ai4_hp - ai4_burnDot[0]
                        ai4_burnDot[1] = ai4_burnDot[1] - 1
                        counter += 1
                    counter = 0
                if ai4_SerraSlashDot[1] > 0:
                    while ai4_SerraSlashDot[1] > 0:
                        if ai4_hp <= 0:
                            break
                        if counter == 2:
                            break
                        ai4_hp = ai1_hp - ai4_SerraSlashDot[0]
                        ai4_SerraSlashDot[1] = ai4_SerraSlashDot[1] - 1
                        counter += 1
                    counter = 0
                if ai4_EviscerDot[1] > 0:
                    while ai4_EviscerDot[1] > 0:
                        if ai4_hp <= 0:
                            break
                        if counter == 2:
                            break
                        ai4_hp = ai4_hp - ai4_EviscerDot[0]
                        ai4_EviscerDot[1] = ai4_EviscerDot[1] - 1
                        counter += 1
                    counter = 0
                if ai4_garroteDot[1] > 0:
                    while ai4_garroteDot[1] > 0:
                        if ai4_hp <= 0:
                            break
                        if counter == 2:
                            break
                        ai4_hp = ai1_hp - ai4_garroteDot[0]
                        ai4_garroteDot[1] = ai4_garroteDot[1] - 1
                        counter += 1
                    counter = 0
            if 5 in target_list:
                if ai5_burnDot[1] > 0:
                    while ai5_burnDot[1] > 0:
                        if ai5_hp <= 0:
                            break
                        if counter == 2:
                            break
                        ai5_hp = ai5_hp - ai5_burnDot[0]
                        ai5_burnDot[1] = ai5_burnDot[1] - 1
                        counter += 1
                    counter = 0
                if ai5_SerraSlashDot[1] > 0:
                    while ai5_SerraSlashDot[1] > 0:
                        if ai5_hp <= 0:
                            break
                        if counter == 2:
                            break
                        ai5_hp = ai1_hp - ai5_SerraSlashDot[0]
                        ai5_SerraSlashDot[1] = ai5_SerraSlashDot[1] - 1
                        counter += 1
                    counter = 0
                if ai5_EviscerDot[1] > 0:
                    while ai5_EviscerDot[1] > 0:
                        if ai5_hp <= 0:
                            break
                        if counter == 2:
                            break
                        ai5_hp = ai5_hp - ai5_EviscerDot[0]
                        ai5_EviscerDot[1] = ai5_EviscerDot[1] - 1
                        counter += 1
                    counter = 0
                if ai5_garroteDot[1] > 0:
                    while ai5_garroteDot[1] > 0:
                        if ai5_hp <= 0:
                            break
                        if counter == 2:
                            break
                        ai5_hp = ai1_hp - ai5_garroteDot[0]
                        ai5_garroteDot[1] = ai5_garroteDot[1] - 1
                        counter += 1
                    counter = 0
        elif ability_data[0] == "Drain Life":
            if 1 in target_list:
                ai1_hp = ai1_hp - ability_data[3]
                for champions in CHAMPION_LIST:
                    counter += 1
                    if champions == BLOODMANCER.title:
                        if counter == 1:
                            champion1_hp = champion1_hp + math.ceil(ability_data[3] * 1.5)
                            if champion1_hp > CHAMPION_1_HP:
                                 champion1_hp = CHAMPION_1_HP
                        elif counter == 2:
                            champion2_hp = champion2_hp + math.ceil(ability_data[3] * 1.5)
                            if champion2_hp > CHAMPION_2_HP:
                                 champion2_hp = CHAMPION_2_HP
                        elif counter == 3:
                            champion3_hp = champion3_hp + math.ceil(ability_data[3] * 1.5)
                            if champion3_hp > CHAMPION_3_HP:
                                 champion3_hp = CHAMPION_3_HP
                        elif counter == 4:
                            champion4_hp = champion4_hp + math.ceil(ability_data[3] * 1.5)
                            if champion4_hp > CHAMPION_4_HP:
                                 champion4_hp = CHAMPION_4_HP
                        elif counter == 5:
                            champion5_hp = champion5_hp + math.ceil(ability_data[3] * 1.5)
                            if champion5_hp > CHAMPION_5_HP:
                                champion5_hp = CHAMPION_5_HP
            if 2 in target_list:
                ai2_hp = ai2_hp - ability_data[3]
                for champions in CHAMPION_LIST:
                    counter += 1
                    if champions == BLOODMANCER.title:
                        if counter == 1:
                            champion1_hp = champion1_hp + math.ceil(ability_data[3] * 1.5)
                            if champion1_hp > CHAMPION_1_HP:
                                champion1_hp = CHAMPION_1_HP
                        elif counter == 2:
                            champion2_hp = champion2_hp + math.ceil(ability_data[3] * 1.5)
                            if champion2_hp > CHAMPION_2_HP:
                                champion2_hp = CHAMPION_2_HP
                        elif counter == 3:
                            champion3_hp = champion3_hp + math.ceil(ability_data[3] * 1.5)
                            if champion3_hp > CHAMPION_3_HP:
                                champion3_hp = CHAMPION_3_HP
                        elif counter == 4:
                            champion4_hp = champion4_hp + math.ceil(ability_data[3] * 1.5)
                            if champion4_hp > CHAMPION_4_HP:
                                champion4_hp = CHAMPION_4_HP
                        elif counter == 5:
                            champion5_hp = champion5_hp + math.ceil(ability_data[3] * 1.5)
                            if champion5_hp > CHAMPION_5_HP:
                                champion5_hp = CHAMPION_5_HP
            if 3 in target_list:
                ai3_hp = ai3_hp - ability_data[3]
                for champions in CHAMPION_LIST:
                    counter += 1
                    if champions == BLOODMANCER.title:
                        if counter == 1:
                            champion1_hp = champion1_hp + math.ceil(ability_data[3] * 1.5)
                            if champion1_hp > CHAMPION_1_HP:
                                champion1_hp = CHAMPION_1_HP
                        elif counter == 2:
                            champion2_hp = champion2_hp + math.ceil(ability_data[3] * 1.5)
                            if champion2_hp > CHAMPION_2_HP:
                                champion2_hp = CHAMPION_2_HP
                        elif counter == 3:
                            champion3_hp = champion3_hp + math.ceil(ability_data[3] * 1.5)
                            if champion3_hp > CHAMPION_3_HP:
                                champion3_hp = CHAMPION_3_HP
                        elif counter == 4:
                            champion4_hp = champion4_hp + math.ceil(ability_data[3] * 1.5)
                            if champion4_hp > CHAMPION_4_HP:
                                champion4_hp = CHAMPION_4_HP
                        elif counter == 5:
                            champion5_hp = champion5_hp + math.ceil(ability_data[3] * 1.5)
                            if champion5_hp > CHAMPION_5_HP:
                                champion5_hp = CHAMPION_5_HP
            if 4 in target_list:
                ai4_hp = ai4_hp - ability_data[3]
                for champions in CHAMPION_LIST:
                    counter += 1
                    if champions == BLOODMANCER.title:
                        if counter == 1:
                            champion1_hp = champion1_hp + math.ceil(ability_data[3] * 1.5)
                            if champion1_hp > CHAMPION_1_HP:
                                champion1_hp = CHAMPION_1_HP
                        elif counter == 2:
                            champion2_hp = champion2_hp + math.ceil(ability_data[3] * 1.5)
                            if champion2_hp > CHAMPION_2_HP:
                                champion2_hp = CHAMPION_2_HP
                        elif counter == 3:
                            champion3_hp = champion3_hp + math.ceil(ability_data[3] * 1.5)
                            if champion3_hp > CHAMPION_3_HP:
                                champion3_hp = CHAMPION_3_HP
                        elif counter == 4:
                            champion4_hp = champion4_hp + math.ceil(ability_data[3] * 1.5)
                            if champion4_hp > CHAMPION_4_HP:
                                champion4_hp = CHAMPION_4_HP
                        elif counter == 5:
                            champion5_hp = champion5_hp + math.ceil(ability_data[3] * 1.5)
                            if champion5_hp > CHAMPION_5_HP:
                                champion5_hp = CHAMPION_5_HP
            if 5 in target_list:
                ai5_hp = ai5_hp - ability_data[3]
                for champions in CHAMPION_LIST:
                    counter += 1
                    if champions == BLOODMANCER.title:
                        if counter == 1:
                            champion1_hp = champion1_hp + math.ceil(ability_data[3] * 1.5)
                            if champion1_hp > CHAMPION_1_HP:
                                champion1_hp = CHAMPION_1_HP
                        elif counter == 2:
                            champion2_hp = champion2_hp + math.ceil(ability_data[3] * 1.5)
                            if champion2_hp > CHAMPION_2_HP:
                                champion2_hp = CHAMPION_2_HP
                        elif counter == 3:
                            champion3_hp = champion3_hp + math.ceil(ability_data[3] * 1.5)
                            if champion3_hp > CHAMPION_3_HP:
                                champion3_hp = CHAMPION_3_HP
                        elif counter == 4:
                            champion4_hp = champion4_hp + math.ceil(ability_data[3] * 1.5)
                            if champion4_hp > CHAMPION_4_HP:
                                champion4_hp = CHAMPION_4_HP
                        elif counter == 5:
                            champion5_hp = champion5_hp + math.ceil(ability_data[3] * 1.5)
                            if champion5_hp > CHAMPION_5_HP:
                                champion5_hp = CHAMPION_5_HP
        elif ability_data[0] == "Blood Spike":
            global blood_boil_buff
            if 1 in target_list:
                ai1_hp = ai1_hp - (ability_data[3] + (blood_boil_buff * ability_data[3]))
            if 2 in target_list:
                ai2_hp = ai2_hp - ability_data[3]
            if 3 in target_list:
                ai3_hp = ai3_hp - ability_data[3]
            if 4 in target_list:
                ai4_hp = ai4_hp - ability_data[3]
            if 5 in target_list:
                ai5_hp = ai5_hp - ability_data[3]
            for champions in CHAMPION_LIST:
                counter += 1
                if champions == BLOODMANCER.title:
                    if counter == 1:
                        champion1_hp = champion1_hp - ability_data[3]
                        if champion1_hp > CHAMPION_1_HP:
                            champion1_hp = CHAMPION_1_HP
                    elif counter == 2:
                        champion2_hp = champion2_hp - ability_data[3]
                        if champion2_hp > CHAMPION_2_HP:
                            champion2_hp = CHAMPION_2_HP
                    elif counter == 3:
                        champion3_hp = champion3_hp - ability_data[3]
                        if champion3_hp > CHAMPION_3_HP:
                            champion3_hp = CHAMPION_3_HP
                    elif counter == 4:
                        champion4_hp = champion4_hp - ability_data[3]
                        if champion4_hp > CHAMPION_4_HP:
                            champion4_hp = CHAMPION_4_HP
                    elif counter == 5:
                        champion5_hp = champion5_hp - ability_data[3]
                        if champion5_hp > CHAMPION_5_HP:
                            champion5_hp = CHAMPION_5_HP
            blood_boil_buff = 0
        elif ability_data[0] == "Overhand Justice":
            if 1 in target_list:
                ai1_hp = ai1_hp - ability_data[3]
            if 2 in target_list:
                ai2_hp = ai2_hp - ability_data[3]
            if 3 in target_list:
                ai3_hp = ai3_hp - ability_data[3]
            if 4 in target_list:
                ai4_hp = ai4_hp - ability_data[3]
            if 5 in target_list:
                ai5_hp = ai5_hp - ability_data[3]
        elif ability_data[0] == "Righteous Blow":
            if 1 in target_list:
                ai1_hp = ai1_hp - ability_data[3]
                self.apply_stun(1, 2)
            if 2 in target_list:
                ai2_hp = ai2_hp - ability_data[3]
                self.apply_stun(2, 2)
            if 3 in target_list:
                ai3_hp = ai3_hp - ability_data[3]
                self.apply_stun(3, 2)
            if 4 in target_list:
                ai4_hp = ai4_hp - ability_data[3]
                self.apply_stun(4, 2)
            if 5 in target_list:
                ai5_hp = ai5_hp - ability_data[3]
                self.apply_stun(5, 2)
        elif ability_data[0] == "Steady Shot":
            if current_arrow_type == "Iron-cast":
                if 1 in target_list:
                    ai1_hp = ai1_hp - ability_data[3]
                if 2 in target_list:
                    ai2_hp = ai2_hp - ability_data[3]
                if 3 in target_list:
                    ai3_hp = ai3_hp - ability_data[3]
                if 4 in target_list:
                    ai4_hp = ai4_hp - ability_data[3]
                if 5 in target_list:
                    ai5_hp = ai5_hp - ability_data[3]
            if current_arrow_type == "Tracker-tipped":
                if AI_SPAWNED == 1:
                    ai1_hp = ai1_hp - math.ceil(ability_data[3] * 0.75)
                if AI_SPAWNED == 3:
                    ai1_hp = ai1_hp - math.ceil(ability_data[3] * 0.75)
                    ai2_hp = ai2_hp - math.ceil(ability_data[3] * 0.75)
                if AI_SPAWNED == 3:
                    ai1_hp = ai1_hp - math.ceil(ability_data[3] * 0.75)
                    ai2_hp = ai2_hp - math.ceil(ability_data[3] * 0.75)
                    ai3_hp = ai3_hp - math.ceil(ability_data[3] * 0.75)
                if AI_SPAWNED == 4:
                    ai1_hp = ai1_hp - math.ceil(ability_data[3] * 0.75)
                    ai2_hp = ai2_hp - math.ceil(ability_data[3] * 0.75)
                    ai3_hp = ai3_hp - math.ceil(ability_data[3] * 0.75)
                    ai4_hp = ai4_hp - math.ceil(ability_data[3] * 0.75)
                if AI_SPAWNED == 5:
                    ai1_hp = ai1_hp - math.ceil(ability_data[3] * 0.75)
                    ai2_hp = ai2_hp - math.ceil(ability_data[3] * 0.75)
                    ai3_hp = ai3_hp - math.ceil(ability_data[3] * 0.75)
                    ai4_hp = ai4_hp - math.ceil(ability_data[3] * 0.75)
                    ai5_hp = ai5_hp - math.ceil(ability_data[3] * 0.75)
        elif ability_data[0] == "Power Opt":
            if current_arrow_type == "Iron-cast":
                if 1 in target_list:
                    ai1_hp = ai1_hp - ability_data[3] * 2
                if 2 in target_list:
                    ai2_hp = ai2_hp - ability_data[3] * 2
                if 3 in target_list:
                    ai3_hp = ai3_hp - ability_data[3] * 2
                if 4 in target_list:
                    ai4_hp = ai4_hp - ability_data[3] * 2
                if 5 in target_list:
                    ai5_hp = ai5_hp - ability_data[3] * 2
            if current_arrow_type == "Tracker-tipped":
                if AI_SPAWNED == 1:
                    ai1_hp = ai1_hp - math.ceil(ability_data[3] * 1.25)
                if AI_SPAWNED == 3:
                    ai1_hp = ai1_hp - math.ceil(ability_data[3] * 1.25)
                    ai2_hp = ai2_hp - math.ceil(ability_data[3] * 1.25)
                if AI_SPAWNED == 3:
                    ai1_hp = ai1_hp - math.ceil(ability_data[3] * 1.25)
                    ai2_hp = ai2_hp - math.ceil(ability_data[3] * 1.25)
                    ai3_hp = ai3_hp - math.ceil(ability_data[3] * 1.25)
                if AI_SPAWNED == 4:
                    ai1_hp = ai1_hp - math.ceil(ability_data[3] * 1.25)
                    ai2_hp = ai2_hp - math.ceil(ability_data[3] * 1.25)
                    ai3_hp = ai3_hp - math.ceil(ability_data[3] * 1.25)
                    ai4_hp = ai4_hp - math.ceil(ability_data[3] * 1.25)
                if AI_SPAWNED == 5:
                    ai1_hp = ai1_hp - math.ceil(ability_data[3] * 1.25)
                    ai2_hp = ai2_hp - math.ceil(ability_data[3] * 1.25)
                    ai3_hp = ai3_hp - math.ceil(ability_data[3] * 1.25)
                    ai4_hp = ai4_hp - math.ceil(ability_data[3] * 1.25)
                    ai5_hp = ai5_hp - math.ceil(ability_data[3] * 1.25)
        elif ability_data[0] == "Lightning Bolt":
            if 1 in target_list:
                ai1_hp = ai1_hp - ability_data[3]
            if 2 in target_list:
                ai2_hp = ai2_hp - ability_data[3]
            if 3 in target_list:
                ai3_hp = ai3_hp - ability_data[3]
            if 4 in target_list:
                ai4_hp = ai4_hp - ability_data[3]
            if 5 in target_list:
                ai5_hp = ai5_hp - ability_data[3]
        elif ability_data[0] == "Chain Lightning":
            if AI_SPAWNED == 1:
                ai1_hp = ai1_hp - math.ceil(ability_data[3] * 0.75)
            if AI_SPAWNED == 3:
                ai1_hp = ai1_hp - math.ceil(ability_data[3] * 0.75)
                ai2_hp = ai2_hp - math.ceil(ability_data[3] * 0.75)
            if AI_SPAWNED == 3:
                ai1_hp = ai1_hp - math.ceil(ability_data[3] * 0.75)
                ai2_hp = ai2_hp - math.ceil(ability_data[3] * 0.75)
                ai3_hp = ai3_hp - math.ceil(ability_data[3] * 0.75)
            if AI_SPAWNED == 4:
                ai1_hp = ai1_hp - math.ceil(ability_data[3] * 0.75)
                ai2_hp = ai2_hp - math.ceil(ability_data[3] * 0.75)
                ai3_hp = ai3_hp - math.ceil(ability_data[3] * 0.75)
                ai4_hp = ai4_hp - math.ceil(ability_data[3] * 0.75)
            if AI_SPAWNED == 5:
                ai1_hp = ai1_hp - math.ceil(ability_data[3] * 0.75)
                ai2_hp = ai2_hp - math.ceil(ability_data[3] * 0.75)
                ai3_hp = ai3_hp - math.ceil(ability_data[3] * 0.75)
                ai4_hp = ai4_hp - math.ceil(ability_data[3] * 0.75)
                ai5_hp = ai5_hp - math.ceil(ability_data[3] * 0.75)
        elif ability_data[0] == "Crashing Boom":
            if AI_SPAWNED == 1:
                self.apply_stun(1, 1)
            if AI_SPAWNED == 3:
                self.apply_stun(1, 1)
                self.apply_stun(2, 1)
            if AI_SPAWNED == 3:
                self.apply_stun(1, 1)
                self.apply_stun(2, 1)
                self.apply_stun(3, 1)
            if AI_SPAWNED == 4:
                self.apply_stun(1, 1)
                self.apply_stun(2, 1)
                self.apply_stun(3, 1)
                self.apply_stun(4, 1)
            if AI_SPAWNED == 5:
                self.apply_stun(1, 1)
                self.apply_stun(2, 1)
                self.apply_stun(3, 1)
                self.apply_stun(4, 1)
                self.apply_stun(5, 1)
        elif ability_data[0] == "Power Surge":
            if AI_SPAWNED == 1:
                ai1_hp = ai1_hp - math.ceil(ability_data[3])
                self.apply_weakness(1, 2)
            if AI_SPAWNED == 3:
                ai1_hp = ai1_hp - math.ceil(ability_data[3])
                ai2_hp = ai2_hp - math.ceil(ability_data[3])
                self.apply_weakness(1, 2)
                self.apply_weakness(2, 2)
            if AI_SPAWNED == 3:
                ai1_hp = ai1_hp - math.ceil(ability_data[3])
                ai2_hp = ai2_hp - math.ceil(ability_data[3])
                ai3_hp = ai3_hp - math.ceil(ability_data[3])
                self.apply_weakness(1, 2)
                self.apply_weakness(2, 2)
                self.apply_weakness(3, 2)
            if AI_SPAWNED == 4:
                ai1_hp = ai1_hp - math.ceil(ability_data[3])
                ai2_hp = ai2_hp - math.ceil(ability_data[3])
                ai3_hp = ai3_hp - math.ceil(ability_data[3])
                ai4_hp = ai4_hp - math.ceil(ability_data[3])
                self.apply_weakness(1, 2)
                self.apply_weakness(2, 2)
                self.apply_weakness(3, 2)
                self.apply_weakness(4, 2)
            if AI_SPAWNED == 5:
                ai1_hp = ai1_hp - math.ceil(ability_data[3])
                ai2_hp = ai2_hp - math.ceil(ability_data[3])
                ai3_hp = ai3_hp - math.ceil(ability_data[3])
                ai4_hp = ai4_hp - math.ceil(ability_data[3])
                ai5_hp = ai5_hp - math.ceil(ability_data[3])
                self.apply_weakness(1, 2)
                self.apply_weakness(2, 2)
                self.apply_weakness(3, 2)
                self.apply_weakness(4, 2)
                self.apply_weakness(5, 2)
        elif ability_data[0] == "Rock Barrage":
            if 1 in target_list:
                ai1_hp = ai1_hp - ability_data[3]
            if 2 in target_list:
                ai2_hp = ai2_hp - ability_data[3]
            if 3 in target_list:
                ai3_hp = ai3_hp - ability_data[3]
            if 4 in target_list:
                ai4_hp = ai4_hp - ability_data[3]
            if 5 in target_list:
                ai5_hp = ai5_hp - ability_data[3]
        elif ability_data[0] == "Shimmering Bolt":
            if 1 in target_list:
                ai1_hp = ai1_hp - ability_data[3]
                if champion1_hp != 0:
                    self.check_champion_blessing(1)
                if champion2_hp != 0:
                    self.check_champion_blessing(2)
                if champion3_hp != 0:
                    self.check_champion_blessing(3)
                if champion4_hp != 0:
                    self.check_champion_blessing(4)
                if champion5_hp != 0:
                    self.check_champion_blessing(5)
            if 2 in target_list:
                ai2_hp = ai2_hp - ability_data[3]
                if champion1_hp != 0:
                    self.check_champion_blessing(1)
                if champion2_hp != 0:
                    self.check_champion_blessing(2)
                if champion3_hp != 0:
                    self.check_champion_blessing(3)
                if champion4_hp != 0:
                    self.check_champion_blessing(4)
                if champion5_hp != 0:
                    self.check_champion_blessing(5)
            if 3 in target_list:
                ai3_hp = ai3_hp - ability_data[3]
                if champion1_hp != 0:
                    self.check_champion_blessing(1)
                if champion2_hp != 0:
                    self.check_champion_blessing(2)
                if champion3_hp != 0:
                    self.check_champion_blessing(3)
                if champion4_hp != 0:
                    self.check_champion_blessing(4)
                if champion5_hp != 0:
                    self.check_champion_blessing(5)
            if 4 in target_list:
                ai4_hp = ai4_hp - ability_data[3]
                if champion1_hp != 0:
                    self.check_champion_blessing(1)
                if champion2_hp != 0:
                    self.check_champion_blessing(2)
                if champion3_hp != 0:
                    self.check_champion_blessing(3)
                if champion4_hp != 0:
                    self.check_champion_blessing(4)
                if champion5_hp != 0:
                    self.check_champion_blessing(5)
            if 5 in target_list:
                ai5_hp = ai5_hp - ability_data[3]
                if champion1_hp != 0:
                    self.check_champion_blessing(1)
                if champion2_hp != 0:
                    self.check_champion_blessing(2)
                if champion3_hp != 0:
                    self.check_champion_blessing(3)
                if champion4_hp != 0:
                    self.check_champion_blessing(4)
                if champion5_hp != 0:
                    self.check_champion_blessing(5)
        elif ability_data[0] == "Divine Smite":
            if 1 in target_list:
                ai1_hp = ai1_hp - ability_data[3]
                if champion1_hp != 0:
                    self.check_champion_blessing(1)
                if champion2_hp != 0:
                    self.check_champion_blessing(2)
                if champion3_hp != 0:
                    self.check_champion_blessing(3)
                if champion4_hp != 0:
                    self.check_champion_blessing(4)
                if champion5_hp != 0:
                    self.check_champion_blessing(5)
            if 2 in target_list:
                ai2_hp = ai2_hp - ability_data[3]
                if champion1_hp != 0:
                    self.check_champion_blessing(1)
                if champion2_hp != 0:
                    self.check_champion_blessing(2)
                if champion3_hp != 0:
                    self.check_champion_blessing(3)
                if champion4_hp != 0:
                    self.check_champion_blessing(4)
                if champion5_hp != 0:
                    self.check_champion_blessing(5)
            if 3 in target_list:
                ai3_hp = ai3_hp - ability_data[3]
                if champion1_hp != 0:
                    self.check_champion_blessing(1)
                if champion2_hp != 0:
                    self.check_champion_blessing(2)
                if champion3_hp != 0:
                    self.check_champion_blessing(3)
                if champion4_hp != 0:
                    self.check_champion_blessing(4)
                if champion5_hp != 0:
                    self.check_champion_blessing(5)
            if 4 in target_list:
                ai4_hp = ai4_hp - ability_data[3]
                if champion1_hp != 0:
                    self.check_champion_blessing(1)
                if champion2_hp != 0:
                    self.check_champion_blessing(2)
                if champion3_hp != 0:
                    self.check_champion_blessing(3)
                if champion4_hp != 0:
                    self.check_champion_blessing(4)
                if champion5_hp != 0:
                    self.check_champion_blessing(5)
            if 5 in target_list:
                ai5_hp = ai5_hp - ability_data[3]
                if champion1_hp != 0:
                    self.check_champion_blessing(1)
                if champion2_hp != 0:
                    self.check_champion_blessing(2)
                if champion3_hp != 0:
                    self.check_champion_blessing(3)
                if champion4_hp != 0:
                    self.check_champion_blessing(4)
                if champion5_hp != 0:
                    self.check_champion_blessing(5)
        elif ability_data[0] == "Diffracting Nova":
            if champion1_hp != 0:
                self.grant_champion_blessing(1)
            if champion2_hp != 0:
                self.grant_champion_blessing(2)
            if champion3_hp != 0:
                self.grant_champion_blessing(3)
            if champion4_hp != 0:
                self.grant_champion_blessing(4)
            if champion5_hp != 0:
                self.grant_champion_blessing(5)
            if AI_SPAWNED == 1:
                ai1_hp = ai1_hp - ability_data[3]
                if champion1_hp != 0:
                    self.check_champion_blessing(1)
                if champion2_hp != 0:
                    self.check_champion_blessing(2)
                if champion3_hp != 0:
                    self.check_champion_blessing(3)
                if champion4_hp != 0:
                    self.check_champion_blessing(4)
                if champion5_hp != 0:
                    self.check_champion_blessing(5)
            if AI_SPAWNED == 2:
                ai1_hp = ai1_hp - ability_data[3]
                ai2_hp = ai2_hp - ability_data[3]
                if champion1_hp != 0:
                    self.check_champion_blessing(1)
                if champion2_hp != 0:
                    self.check_champion_blessing(2)
                if champion3_hp != 0:
                    self.check_champion_blessing(3)
                if champion4_hp != 0:
                    self.check_champion_blessing(4)
                if champion5_hp != 0:
                    self.check_champion_blessing(5)
            if AI_SPAWNED == 3:
                ai1_hp = ai1_hp - ability_data[3]
                ai2_hp = ai2_hp - ability_data[3]
                ai3_hp = ai3_hp - ability_data[3]
                if champion1_hp != 0:
                    self.check_champion_blessing(1)
                if champion2_hp != 0:
                    self.check_champion_blessing(2)
                if champion3_hp != 0:
                    self.check_champion_blessing(3)
                if champion4_hp != 0:
                    self.check_champion_blessing(4)
                if champion5_hp != 0:
                    self.check_champion_blessing(5)
            if AI_SPAWNED == 4:
                ai1_hp = ai1_hp - ability_data[3]
                ai2_hp = ai2_hp - ability_data[3]
                ai3_hp = ai3_hp - ability_data[3]
                ai4_hp = ai4_hp - ability_data[3]
                if champion1_hp != 0:
                    self.check_champion_blessing(1)
                if champion2_hp != 0:
                    self.check_champion_blessing(2)
                if champion3_hp != 0:
                    self.check_champion_blessing(3)
                if champion4_hp != 0:
                    self.check_champion_blessing(4)
                if champion5_hp != 0:
                    self.check_champion_blessing(5)
            if AI_SPAWNED == 5:
                ai1_hp = ai1_hp - ability_data[3]
                ai2_hp = ai2_hp - ability_data[3]
                ai3_hp = ai3_hp - ability_data[3]
                ai4_hp = ai4_hp - ability_data[3]
                ai5_hp = ai5_hp - ability_data[3]
                if champion1_hp != 0:
                    self.check_champion_blessing(1)
                if champion2_hp != 0:
                    self.check_champion_blessing(2)
                if champion3_hp != 0:
                    self.check_champion_blessing(3)
                if champion4_hp != 0:
                    self.check_champion_blessing(4)
                if champion5_hp != 0:
                    self.check_champion_blessing(5)
        elif ability_data[0] == "Cybernetic Blast":
            if 1 in target_list:
                ai1_hp = ai1_hp - ability_data[3]
            if 2 in target_list:
                ai2_hp = ai2_hp - ability_data[3]
            if 3 in target_list:
                ai3_hp = ai3_hp - ability_data[3]
            if 4 in target_list:
                ai4_hp = ai4_hp - ability_data[3]
            if 5 in target_list:
                ai5_hp = ai5_hp - ability_data[3]
        elif ability_data[0] == "Throw Scissors":
            if 1 in target_list:
                ai1_hp = ai1_hp - ability_data[3]
            if 2 in target_list:
                ai2_hp = ai2_hp - ability_data[3]
            if 3 in target_list:
                ai3_hp = ai3_hp - ability_data[3]
            if 4 in target_list:
                ai4_hp = ai4_hp - ability_data[3]
            if 5 in target_list:
                ai5_hp = ai5_hp - ability_data[3]

    def finalise_healing_done(self):
        global champion1_hp, champion2_hp, champion3_hp, champion4_hp, champion5_hp
        global champion1_guarded, champion2_guarded, champion3_guarded, champion4_guarded, champion5_guarded
        counter = 0
        if ability_data[0] == "Fortification":
            global champion1_fortification, champion2_fortification, champion3_fortification, \
                champion4_fortification, champion5_fortification
            if champion1_hp != 0:
                champion1_fortification = [1, 2]
            if champion2_hp != 0:
                champion2_fortification = [1, 2]
            if champion3_hp != 0:
                champion3_fortification = [1, 2]
            if champion4_hp != 0:
                champion4_fortification = [1, 2]
            if champion5_hp != 0:
                champion5_fortification = [1, 2]
        elif ability_data[0] == "Block":
            if 1 in target_list:
                champion1_guarded.append("Block")
            if 2 in target_list:
                champion2_guarded.append("Block")
            if 3 in target_list:
                champion3_guarded.append("Block")
            if 4 in target_list:
                champion4_guarded.append("Block")
            if 5 in target_list:
                champion5_guarded.append("Block")
        elif ability_data[0] == "Parry":
            if 1 in target_list:
                champion1_guarded.append("Parry")
            if 2 in target_list:
                champion2_guarded.append("Parry")
            if 3 in target_list:
                champion3_guarded.append("Parry")
            if 4 in target_list:
                champion4_guarded.append("Parry")
            if 5 in target_list:
                champion5_guarded.append("Parry")
        elif ability_data[0] == "Thorns":
            global champion1_thorns, champion2_thorns, champion3_thorns, champion4_thorns, champion5_thorns
            if 1 in target_list:
                champion1_thorns = [1, 5]
            if 2 in target_list:
                champion2_thorns = [1, 5]
            if 3 in target_list:
                champion3_thorns = [1, 5]
            if 4 in target_list:
                champion4_thorns = [1, 5]
            if 5 in target_list:
                champion5_thorns = [1, 5]
        elif ability_data[0] == "Aura of Power":
            global champion1_aura, champion2_aura, champion3_aura, champion4_aura, champion5_aura
            champion1_aura = [1]
            champion2_aura = [1]
            champion3_aura = [1]
            champion4_aura = [1]
            champion5_aura = [1]
        elif ability_data[0] == "Aura of Protection":
            champion1_aura = [2]
            champion2_aura = [2]
            champion3_aura = [2]
            champion4_aura = [2]
            champion5_aura = [2]
        elif ability_data[0] == "Muscle Enlarger":
            global champion1_enlarged_muscles, champion2_enlarged_muscles, champion3_enlarged_muscles, \
                champion4_enlarged_muscles, champion5_enlarged_muscles
            if 1 in target_list:
                champion1_enlarged_muscles = [1, 3]
            if 2 in target_list:
                champion2_enlarged_muscles = [1, 3]
            if 3 in target_list:
                champion3_enlarged_muscles = [1, 3]
            if 4 in target_list:
                champion4_enlarged_muscles = [1, 3]
            if 5 in target_list:
                champion5_enlarged_muscles = [1, 3]
        elif ability_data[0] == "Mistic Bloom":
            if 1 in target_list:
                champion1_hp = champion1_hp + ability_data[3]
                champion1_hp > CHAMPION_1_HP
                champion1_hp = CHAMPION_1_HP
            if 2 in target_list:
                champion2_hp = champion2_hp + ability_data[3]
                champion2_hp > CHAMPION_2_HP
                champion2_hp = CHAMPION_2_HP
            if 3 in target_list:
                champion3_hp = champion3_hp + ability_data[3]
                champion3_hp > CHAMPION_3_HP
                champion3_hp = CHAMPION_3_HP
            if 4 in target_list:
                champion4_hp = champion4_hp + ability_data[3]
                champion4_hp > CHAMPION_4_HP
                champion4_hp = CHAMPION_4_HP
            if 5 in target_list:
                champion5_hp = champion5_hp + ability_data[3]
                champion5_hp > CHAMPION_5_HP
                champion5_hp = CHAMPION_5_HP
        elif ability_data[0] == "Full Potential":
            global champion1_full_potential, champion2_full_potential, champion3_full_potential, \
                champion4_full_potential, champion5_full_potential
            if 1 in target_list:
                champion1_full_potential = [1, 2]
            if 2 in target_list:
                champion2_full_potential = [1, 2]
            if 3 in target_list:
                champion3_full_potential = [1, 2]
            if 4 in target_list:
                champion4_full_potential = [1, 2]
            if 5 in target_list:
                champion5_full_potential = [1, 2]
        elif ability_data[0] == "Healing Surge":
            if 1 in target_list:
                champion1_hp = champion1_hp + ability_data[3]
                champion1_hp > CHAMPION_1_HP
                champion1_hp = CHAMPION_1_HP
            if 2 in target_list:
                champion2_hp = champion2_hp + ability_data[3]
                champion2_hp > CHAMPION_2_HP
                champion2_hp = CHAMPION_2_HP
            if 3 in target_list:
                champion3_hp = champion3_hp + ability_data[3]
                champion3_hp > CHAMPION_3_HP
                champion3_hp = CHAMPION_3_HP
            if 4 in target_list:
                champion4_hp = champion4_hp + ability_data[3]
                champion4_hp > CHAMPION_4_HP
                champion4_hp = CHAMPION_4_HP
            if 5 in target_list:
                champion5_hp = champion5_hp + ability_data[3]
                champion5_hp > CHAMPION_5_HP
                champion5_hp = CHAMPION_5_HP
        elif ability_data[0] == "Rejuvenating Whirlpool":
            if champion1_hp != 0:
                champion1_hp = champion1_hp + ability_data[3]
                champion1_hp > CHAMPION_1_HP
                champion1_hp = CHAMPION_1_HP
            if champion2_hp != 0:
                champion2_hp = champion2_hp + ability_data[3]
                champion2_hp > CHAMPION_2_HP
                champion2_hp = CHAMPION_2_HP
            if champion3_hp != 0:
                champion3_hp = champion3_hp + ability_data[3]
                champion3_hp > CHAMPION_3_HP
                champion3_hp = CHAMPION_3_HP
            if champion4_hp != 0:
                champion4_hp = champion4_hp + ability_data[3]
                champion4_hp > CHAMPION_4_HP
                champion4_hp = CHAMPION_4_HP
            if champion5_hp != 0:
                champion5_hp = champion5_hp + ability_data[3]
                champion5_hp > CHAMPION_5_HP
                champion5_hp = CHAMPION_5_HP
        elif ability_data[0] == "Boulder Cocoon":
            if 1 in target_list:
                champion1_guarded.append("Boulder")
            if 2 in target_list:
                champion1_guarded.append("Boulder")
            if 3 in target_list:
                champion1_guarded.append("Boulder")
            if 4 in target_list:
                champion1_guarded.append("Boulder")
            if 5 in target_list:
                champion1_guarded.append("Boulder")
        elif ability_data[0] == "Healing Light":
            if 1 in target_list:
                champion1_hp = champion1_hp + ability_data[3]
                champion1_hp > CHAMPION_1_HP
                champion1_hp = CHAMPION_1_HP
                self.grant_champion_blessing(1)
            if 2 in target_list:
                champion2_hp = champion2_hp + ability_data[3]
                champion2_hp > CHAMPION_2_HP
                champion2_hp = CHAMPION_2_HP
                self.grant_champion_blessing(2)
            if 3 in target_list:
                champion3_hp = champion3_hp + ability_data[3]
                champion3_hp > CHAMPION_3_HP
                champion3_hp = CHAMPION_3_HP
                self.grant_champion_blessing(3)
            if 4 in target_list:
                champion4_hp = champion4_hp + ability_data[3]
                champion4_hp > CHAMPION_4_HP
                champion4_hp = CHAMPION_4_HP
                self.grant_champion_blessing(4)
            if 5 in target_list:
                champion5_hp = champion5_hp + ability_data[3]
                champion5_hp > CHAMPION_5_HP
                champion5_hp = CHAMPION_5_HP
                self.grant_champion_blessing(5)
        elif ability_data[0] == "Nanoheal Bots":
            if champion1_hp != 0:
                champion1_hp = champion1_hp + ability_data[3]
                champion1_hp > CHAMPION_1_HP
                champion1_hp = CHAMPION_1_HP
            if champion2_hp != 0:
                champion2_hp = champion2_hp + ability_data[3]
                champion2_hp > CHAMPION_2_HP
                champion2_hp = CHAMPION_2_HP
            if champion3_hp != 0:
                champion3_hp = champion3_hp + ability_data[3]
                champion3_hp > CHAMPION_3_HP
                champion3_hp = CHAMPION_3_HP
            if champion4_hp != 0:
                champion4_hp = champion4_hp + ability_data[3]
                champion4_hp > CHAMPION_4_HP
                champion4_hp = CHAMPION_4_HP
            if champion5_hp != 0:
                champion5_hp = champion5_hp + ability_data[3]
                champion5_hp > CHAMPION_5_HP
                champion5_hp = CHAMPION_5_HP
            self.apply_nanoheal_bots(3)
        elif ability_data[0] == "Reverse Wounds":
            if 1 in target_list:
                champion1_hp = champion1_hp + champion1_lastRound_damageTaken
            if 2 in target_list:
                champion2_hp = champion2_hp + champion2_lastRound_damageTaken
            if 3 in target_list:
                champion3_hp = champion3_hp + champion3_lastRound_damageTaken
            if 4 in target_list:
                champion4_hp = champion4_hp + champion4_lastRound_damageTaken
            if 5 in target_list:
                champion5_hp = champion5_hp + champion5_lastRound_damageTaken
        elif ability_data[0] == "Alter Time":
            if champion1_hp != 0:
                champion1_hp = CHAMPION_1_HP
            if champion2_hp != 0:
                champion2_hp = CHAMPION_2_HP
            if champion3_hp != 0:
                champion3_hp = CHAMPION_3_HP
            if champion4_hp != 0:
                champion4_hp = CHAMPION_4_HP
            if champion5_hp != 0:
                champion5_hp = CHAMPION_5_HP
        elif ability_data[0] == "Bandage Wound":
            if 1 in target_list:
                champion1_hp = champion1_hp + ability_data[3]
                champion1_hp > CHAMPION_1_HP
                champion1_hp = CHAMPION_1_HP
            if 2 in target_list:
                champion2_hp = champion2_hp + ability_data[3]
                champion2_hp > CHAMPION_2_HP
                champion2_hp = CHAMPION_2_HP
            if 3 in target_list:
                champion3_hp = champion3_hp + ability_data[3]
                champion3_hp > CHAMPION_3_HP
                champion3_hp = CHAMPION_3_HP
            if 4 in target_list:
                champion4_hp = champion4_hp + ability_data[3]
                champion4_hp > CHAMPION_4_HP
                champion4_hp = CHAMPION_4_HP
            if 5 in target_list:
                champion5_hp = champion5_hp + ability_data[3]
                champion5_hp > CHAMPION_5_HP
                champion5_hp = CHAMPION_5_HP
        elif ability_data[0] == "Perfected Herbal Tea":
            if 1 in target_list:
                champion1_hp = champion1_hp + ability_data[3]
                champion1_hp > CHAMPION_1_HP
                champion1_hp = CHAMPION_1_HP
                self.apply_herbal_tea(1, 2)
            if 2 in target_list:
                champion2_hp = champion2_hp + ability_data[3]
                champion2_hp > CHAMPION_2_HP
                champion2_hp = CHAMPION_2_HP
                self.apply_herbal_tea(2, 2)
            if 3 in target_list:
                champion3_hp = champion3_hp + ability_data[3]
                champion3_hp > CHAMPION_3_HP
                champion3_hp = CHAMPION_3_HP
                self.apply_herbal_tea(3, 2)
            if 4 in target_list:
                champion4_hp = champion4_hp + ability_data[3]
                champion4_hp > CHAMPION_4_HP
                champion4_hp = CHAMPION_4_HP
                self.apply_herbal_tea(4, 2)
            if 5 in target_list:
                champion5_hp = champion5_hp + ability_data[3]
                champion5_hp > CHAMPION_5_HP
                champion5_hp = CHAMPION_5_HP
                self.apply_herbal_tea(5, 2)
        elif ability_data[0] == "G.3.T J.A.X.D":
            global champion1_JAXD, champion2_JAXD, champion3_JAXD, \
                champion4_JAXD, champion5_JAXD
            if 1 in target_list:
                champion1_JAXD = [1, 2]
            if 2 in target_list:
                champion2_JAXD = [1, 2]
            if 3 in target_list:
                champion3_JAXD = [1, 2]
            if 4 in target_list:
                champion4_JAXD = [1, 2]
            if 5 in target_list:
                champion5_JAXD = [1, 2]

    def finalise_self_buff(self):
        global ai1_hp, ai2_hp,ai3_hp,ai4_hp,ai5_hp, champion1_hp, champion2_hp, champion3_hp, champion4_hp, champion5_hp
        global champion1_guarded, champion2_guarded, chmapion3_guarded, champion4_guarded, \
            champion5_guarded, current_arrow_type
        counter = 0
        if ability_data[0] == "Harmonize":
            global monk_staggered_damage_list
            if monk_staggered_damage_list[0] != 0:
                monk_staggered_damage_list[0] = monk_staggered_damage_list[0] / 2
            if monk_staggered_damage_list[1] != 0:
                monk_staggered_damage_list[1] = monk_staggered_damage_list[1] - 1
        elif ability_data[0] == "Challenging Shout":
            if AI_SPAWNED == 1:
                self.apply_taunt(1, BARBARIAN.title, 2)
            elif AI_SPAWNED == 2:
                if ai1_hp != 0:
                    self.apply_taunt(1, BARBARIAN.title, 2)
                if ai2_hp != 0:
                    self.apply_taunt(2, BARBARIAN.title, 2)
            elif AI_SPAWNED == 3:
                if ai1_hp != 0:
                    self.apply_taunt(1, BARBARIAN.title, 2)
                if ai2_hp != 0:
                    self.apply_taunt(2, BARBARIAN.title, 2)
                if ai3_hp != 0:
                    self.apply_taunt(3, BARBARIAN.title, 2)
            elif AI_SPAWNED == 4:
                if ai1_hp != 0:
                    self.apply_taunt(1, BARBARIAN.title, 2)
                if ai2_hp != 0:
                    self.apply_taunt(2, BARBARIAN.title, 2)
                if ai3_hp != 0:
                    self.apply_taunt(3, BARBARIAN.title, 2)
                if ai4_hp != 0:
                    self.apply_taunt(4, BARBARIAN.title, 2)
            elif AI_SPAWNED == 5:
                if ai1_hp != 0:
                    self.apply_taunt(1, BARBARIAN.title, 2)
                if ai2_hp != 0:
                    self.apply_taunt(2, BARBARIAN.title, 2)
                if ai3_hp != 0:
                    self.apply_taunt(3, BARBARIAN.title, 2)
                if ai4_hp != 0:
                    self.apply_taunt(4, BARBARIAN.title, 2)
                if ai5_hp != 0:
                    self.apply_taunt(5, BARBARIAN.title, 2)
        elif ability_data[0] == "Impactful Boast":
            point = 0
            if ai1_taunt[0] == BARBARIAN.title:
                point += 1
            if ai2_taunt[0] == BARBARIAN.title:
                point += 1
            if ai3_taunt[0] == BARBARIAN.title:
                point += 1
            if ai4_taunt[0] == BARBARIAN.title:
                point += 1
            if ai5_taunt[0] == BARBARIAN.title:
                point += 1
            for character in CHAMPION_LIST:
                counter += 1
                if character == BARBARIAN.title:
                    if counter == 1:
                        champion1_hp = champion1_hp + (300 * point)
                        break
                    if counter == 2:
                        champion2_hp = champion2_hp + (300 * point)
                        break
                    if counter == 3:
                        champion3_hp = champion3_hp + (300 * point)
                        break
                    if counter == 4:
                        champion4_hp = champion4_hp + (300 * point)
                        break
                    if counter == 5:
                        champion5_hp = champion5_hp + (300 * point)
                        break
        elif ability_data[0] == "Elusive Measures":
            for character in CHAMPION_LIST:
                counter += 1
                if character == MASTER_FENCER.title:
                    if counter == 1:
                        champion1_guarded.append("Elusive Measures")
                        break
                    if counter == 2:
                        champion2_guarded.append("Elusive Measures")
                        break
                    if counter == 3:
                        champion3_guarded.append("Elusive Measures")
                        break
                    if counter == 4:
                        champion4_guarded.append("Elusive Measures")
                        break
                    if counter == 5:
                        champion5_guarded.append("Elusive Measures")
                        break
        elif ability_data[0] == "Enrage":
            global champion1_enrage, champion2_enrage, champion3_enrage, champion4_enrage, champion5_enrage
            for character in CHAMPION_LIST:
                counter += 1
                if character == BERSERKER.title:
                    if counter == 1:
                        champion1_enrage = [1]
                        break
                    if counter == 2:
                        champion2_enrage = [1]
                        break
                    if counter == 3:
                        champion3_enrage = [1]
                        break
                    if counter == 4:
                        champion4_enrage = [1]
                        break
                    if counter == 5:
                        champion5_enrage = [1]
                        break
        elif ability_data[0] == "Reckless Flurry":
            global champion1_reckless_flurry,champion2_reckless_flurry,champion3_reckless_flurry, \
                champion4_reckless_flurry,champion5_reckless_flurry
            for character in CHAMPION_LIST:
                counter += 1
                if character == BERSERKER.title:
                    if counter == 1:
                        champion1_reckless_flurry = [1, 3]
                        break
                    if counter == 2:
                        champion2_reckless_flurry = [1, 3]
                        break
                    if counter == 3:
                        champion3_reckless_flurry = [1, 3]
                        break
                    if counter == 4:
                        champion4_reckless_flurry = [1, 3]
                        break
                    if counter == 5:
                        champion5_reckless_flurry = [1, 3]
                        break
        elif ability_data[0] == "Play Dead":
            global champion1_play_dead, champion2_play_dead, champion3_play_dead , \
                champion4_play_dead, champion5_play_dead
            for character in CHAMPION_LIST:
                counter += 1
                if character == SURVIVALIST.title:
                    if counter == 1:
                        champion1_play_dead = [1]
                        break
                    if counter == 2:
                        champion2_play_dead = [1]
                        break
                    if counter == 3:
                        champion3_play_dead = [1]
                        break
                    if counter == 4:
                        champion4_play_dead = [1]
                        break
                    if counter == 5:
                        champion5_play_dead = [1]
                        break
        elif ability_data[0] == "Rushed Rest":
            global rushed_rest_used
            rushed_rest_used = 1
            for character in CHAMPION_LIST:
                counter += 1
                if character == SURVIVALIST.title:
                    if counter == 1:
                        champion1_hp = champion1_hp + (CHAMPION_1_HP * 0.6)
                        if champion1_hp > CHAMPION_1_HP:
                            champion1_hp = CHAMPION_1_HP
                        break
                    if counter == 2:
                        champion2_hp = champion2_hp + (CHAMPION_2_HP * 0.6)
                        if champion2_hp > CHAMPION_2_HP:
                            champion2_hp = CHAMPION_2_HP
                        break
                    if counter == 3:
                        champion3_hp = champion3_hp + (CHAMPION_3_HP * 0.6)
                        if champion3_hp > CHAMPION_3_HP:
                            champion3_hp = CHAMPION_3_HP
                        break
                    if counter == 4:
                        champion4_hp = champion4_hp + (CHAMPION_4_HP * 0.6)
                        if champion4_hp > CHAMPION_4_HP:
                            champion4_hp = CHAMPION_4_HP
                        break
                    if counter == 5:
                        champion5_hp = champion5_hp + (CHAMPION_5_HP * 0.6)
                        if champion5_hp > CHAMPION_5_HP:
                            champion5_hp = CHAMPION_5_HP
                        break
        elif ability_data[0] == "Defensive Stance":
            for character in CHAMPION_LIST:
                counter += 1
                if character == BRAWLIST.title:
                    if counter == 1:
                        champion1_guarded.append("Defensive Stance")
                        break
                    if counter == 2:
                        champion2_guarded.append("Defensive Stance")
                        break
                    if counter == 3:
                        champion3_guarded.append("Defensive Stance")
                        break
                    if counter == 4:
                        champion4_guarded.append("Defensive Stance")
                        break
                    if counter == 5:
                        champion5_guarded.append("Defensive Stance")
                        break
        elif ability_data[0] == "Magical Barrier":
            for character in CHAMPION_LIST:
                counter += 1
                if character == ACADEMIC_MAGE.title:
                    if counter == 1:
                        champion1_guarded.append("Magical Barrier")
                        break
                    if counter == 2:
                        champion2_guarded.append("Magical Barrier")
                        break
                    if counter == 3:
                        champion3_guarded.append("Magical Barrier")
                        break
                    if counter == 4:
                        champion4_guarded.append("Magical Barrier")
                        break
                    if counter == 5:
                        champion5_guarded.append("Magical Barrier")
                        break
        elif ability_data[0] == "Void Infusion":
            global void_infusion_stacks
            void_infusion_stacks += 1
        elif ability_data[0] == "Soul Tap":
            global champion1_rp, champion2_rp, champion3_rp, champion4_rp, champion5_rp
            for character in CHAMPION_LIST:
                counter += 1
                if character == WARLOCK.title:
                    if counter == 1:
                        hp_sacrifice_amount = CHAMPION_1_RP - champion1_rp
                        if hp_sacrifice_amount < champion1_hp:
                            champion1_hp = champion1_hp - hp_sacrifice_amount
                            champion1_rp = CHAMPION_1_RP
                        break
                    elif counter == 2:
                        hp_sacrifice_amount = CHAMPION_2_RP - champion2_rp
                        if hp_sacrifice_amount < champion2_hp:
                            champion2_hp = champion2_hp - hp_sacrifice_amount
                            champion2_rp = CHAMPION_2_RP
                        break
                    elif counter == 3:
                        hp_sacrifice_amount = CHAMPION_3_RP - champion3_rp
                        if hp_sacrifice_amount < champion3_hp:
                            champion3_hp = champion3_hp - hp_sacrifice_amount
                            champion3_rp = CHAMPION_3_RP
                        break
                    elif counter == 4:
                        hp_sacrifice_amount = CHAMPION_4_RP - champion4_rp
                        if hp_sacrifice_amount < champion4_hp:
                            champion4_hp = champion4_hp - hp_sacrifice_amount
                            champion4_rp = CHAMPION_4_RP
                        break
                    elif counter == 5:
                        hp_sacrifice_amount = CHAMPION_5_RP - champion5_rp
                        if hp_sacrifice_amount < champion5_hp:
                            champion5_hp = champion5_hp - hp_sacrifice_amount
                            champion5_rp = CHAMPION_5_RP
                        break
        elif ability_data[0] == "Blood Boil":
            global blood_boil_buff
            blood_boil_buff = 1
        elif ability_data[0] == "Enharden Nerves":
            for character in CHAMPION_LIST:
                counter += 1
                if character == BLOODMANCER.title:
                    if counter == 1:
                        champion1_guarded.append("Enharden Nerves")
                        break
                    if counter == 2:
                        champion2_guarded.append("Enharden Nerves")
                        break
                    if counter == 3:
                        champion3_guarded.append("Enharden Nerves")
                        break
                    if counter == 4:
                        champion4_guarded.append("Enharden Nerves")
                        break
                    if counter == 5:
                        champion5_guarded.append("Enharden Nerves")
                        break
        elif ability_data[0] == "Equip Iron-cast Arrows":
            current_arrow_type = "Iron-cast"
        elif ability_data[0] == "Equip Tracker-tipped Arrows":
            current_arrow_type = "Tracker-tipped"
        elif ability_data[0] == "Thunderous Vigor":
            global crashing_boom_requirements
            crashing_boom_requirements[1] = 0

    def grant_champion_blessing(self, champion_position):
        global champion1_blessing, champion2_blessing, champion3_blessing, champion4_blessing, champion5_blessing
        if champion_position == 1:
            champion1_blessing = [1, 5]
        if champion_position == 2:
            champion2_blessing = [1, 5]
        if champion_position == 3:
            champion3_blessing = [1, 5]
        if champion_position == 4:
            champion4_blessing = [1, 5]
        if champion_position == 5:
            champion5_blessing = [1, 5]

    def check_champion_blessing(self, champion_position):
        global champion1_hp, champion2_hp, champion3_hp, champion4_hp, champion5_hp
        if champion_position == 1:
            if champion1_blessing[0] != 0:
                champion1_hp = champion1_hp + ability_data[3]
                if champion1_hp > CHAMPION_1_HP:
                    champion1_hp = CHAMPION_1_HP
        if champion_position == 2:
            if champion2_blessing[0] != 0:
                champion2_hp = champion2_hp + ability_data[3]
                if champion2_hp > CHAMPION_2_HP:
                    champion2_hp = CHAMPION_2_HP
        if champion_position == 3:
            if champion3_blessing[0] != 0:
                champion3_hp = champion3_hp + ability_data[3]
                if champion3_hp > CHAMPION_3_HP:
                    champion3_hp = CHAMPION_3_HP
        if champion_position == 4:
            if champion4_blessing[0] != 0:
                champion4_hp = champion4_hp + ability_data[3]
                if champion4_hp > CHAMPION_4_HP:
                    champion4_hp = CHAMPION_4_HP
        if champion_position == 5:
            if champion5_blessing[0] != 0:
                champion5_hp = champion5_hp + ability_data[3]
                if champion5_hp > CHAMPION_5_HP:
                    champion5_hp = CHAMPION_5_HP

    def apply_nanoheal_bots(self, length):
        global champion1_nanobot, champion2_nanobot, champion3_nanobot, champion4_nanobot, champion5_nanobot
        nanobotHealHOT = math.ceil(ability_data[3] * 0.66)
        if champion1_hp != 0:
            champion1_nanobot = [nanobotHealHOT, length]
        if champion2_hp != 0:
            champion2_nanobot = [nanobotHealHOT, length]
        if champion3_hp != 0:
            champion3_nanobot = [nanobotHealHOT, length]
        if champion4_hp != 0:
            champion4_nanobot = [nanobotHealHOT, length]
        if champion5_hp != 0:
            champion5_nanobot = [nanobotHealHOT, length]

    def apply_herbal_tea(self, length):
        global champion1_herb_tea, champion2_herb_tea, champion3_herb_tea, champion4_herb_tea, champion5_herb_tea
        herbal_tea_HealHOT = ability_data[3]
        if 1 in target_list:
            champion1_herb_tea = [herbal_tea_HealHOT, length]
        if 2 in target_list:
            champion2_herb_tea = [herbal_tea_HealHOT, length]
        if 3 in target_list:
            champion3_herb_tea = [herbal_tea_HealHOT, length]
        if 4 in target_list:
            champion4_herb_tea = [herbal_tea_HealHOT, length]
        if 5 in target_list:
            champion5_herb_tea = [herbal_tea_HealHOT, length]

    def apply_weakness(self, ai_target, length):
        global ai1_weakness, ai2_weakness, ai3_weakness, ai4_weakness, ai5_weakness
        if ai_target == 1:
            if length > ai1_weakness:
                ai1_weakness = length
            else:
                return
        if ai_target == 2:
            if length > ai2_weakness:
                ai2_weakness = length
            else:
                return
        if ai_target == 3:
            if length > ai3_weakness:
                ai3_weakness = length
            else:
                return
        if ai_target == 4:
            if length > ai4_weakness:
                ai4_weakness = length
            else:
                return
        if ai_target == 5:
            if length > ai5_weakness:
                ai5_weakness = length
            else:
                return
    def apply_taunt(self, ai_target, tauntie, length):
        global ai1_taunt, ai2_taunt, ai3_taunt, ai4_taunt, ai5_taunt
        if ai_target == 1:
            if length > ai1_taunt[1]:
                ai1_taunt = [tauntie ,length]
            else:
                return
        if ai_target == 2:
            if length > ai2_taunt[1]:
                ai2_taunt = [tauntie ,length]
            else:
                return
        if ai_target == 3:
            if length > ai3_taunt[1]:
                ai3_taunt = [tauntie ,length]
            else:
                return
        if ai_target == 4:
            if length > ai4_taunt[1]:
                ai4_taunt = [tauntie ,length]
            else:
                return
        if ai_target == 5:
            if length > ai5_taunt[1]:
                ai5_taunt = [tauntie ,length]
            else:
                return
    def apply_stun(self, ai_target, length):
        global ai1_stun, ai2_stun, ai3_stun, ai4_stun, ai5_stun
        if ai_target == 1:
            if length > ai1_stun:
                ai1_stun = length
            else:
                return
        if ai_target == 2:
            if length > ai2_stun:
                ai2_stun = length
            else:
                return
        if ai_target == 3:
            if length > ai3_stun:
                ai3_stun = length
            else:
                return
        if ai_target == 4:
            if length > ai4_stun:
                ai4_stun = length
            else:
                return
        if ai_target == 5:
            if length > ai5_stun:
                ai5_stun = length
            else:
                return

    def apply_brittle(self, ai_target, length):
        global ai1_brittle, ai2_brittle, ai3_brittle, ai4_brittle, ai5_brittle
        if ai_target == 1:
            if length > ai1_brittle:
                ai1_brittle = length
            else:
                return
        if ai_target == 2:
            if length > ai2_brittle:
                ai2_brittle = length
            else:
                return
        if ai_target == 3:
            if length > ai3_brittle:
                ai3_brittle = length
            else:
                return
        if ai_target == 4:
            if length > ai4_brittle:
                ai4_brittle = length
            else:
                return
        if ai_target == 5:
            if length > ai5_brittle:
                ai5_brittle = length
            else:
                return
    def apply_burn(self, ai_target, length):
        global ai1_burnDot, ai2_burnDot, ai3_burnDot, ai4_burnDot, ai5_burnDot
        burnDot = math.ceil(ability_data[3] * 0.5)
        if ai_target == 1:
            if length > ai1_burnDot[1]:
                ai1_burnDot = [burnDot, length]
            else:
                return
        if ai_target == 2:
            if length > ai2_burnDot[1]:
                ai2_burnDot = [burnDot, length]
            else:
                return
        if ai_target == 3:
            if length > ai3_burnDot[1]:
                ai3_burnDot = [burnDot, length]
            else:
                return
        if ai_target == 4:
            if length > ai4_burnDot[1]:
                ai4_burnDot = [burnDot, length]
            else:
                return
        if ai_target == 5:
            if length > ai5_burnDot[1]:
                ai5_burnDot = [burnDot, length]
            else:
                return
    def apply_pricked(self, ai_target):
        global ai1_pricked, ai2_pricked, ai3_pricked, ai4_pricked, ai5_pricked
        prick_dot = math.ceil(ability_data[3] * 0.25)
        if ai_target == 1:
            ai1_pricked = [prick_dot]
        if ai_target == 2:
            ai2_pricked = [prick_dot]
        if ai_target == 3:
            ai3_pricked = [prick_dot]
        if ai_target == 4:
            ai4_pricked = [prick_dot]
        if ai_target == 5:
            ai5_pricked = [prick_dot]
    def serrated_slash_dot(self, ai_target, length):
        global ai1_SerraSlashDot, ai2_SerraSlashDot, ai3_SerraSlashDot, ai4_SerraSlashDot, ai5_SerraSlashDot
        SerraSlashDotDamage = math.ceil(ability_data[3] * 0.5)
        if ai_target == 1:
            if length > ai1_SerraSlashDot[1]:
                ai1_SerraSlashDot = [SerraSlashDotDamage, length]
            else:
                return
        if ai_target == 2:
            if length > ai2_SerraSlashDot[1]:
                ai2_SerraSlashDot = [SerraSlashDotDamage, length]
            else:
                return
        if ai_target == 3:
            if length > ai3_SerraSlashDot[1]:
                ai3_SerraSlashDot = [SerraSlashDotDamage, length]
            else:
                return
        if ai_target == 4:
            if length > ai4_SerraSlashDot[1]:
                ai4_SerraSlashDot = [SerraSlashDotDamage, length]
            else:
                return
        if ai_target == 5:
            if length > ai5_SerraSlashDot[1]:
                ai5_SerraSlashDot = [SerraSlashDotDamage, length]
            else:
                return
    def eviscerate_dot(self, ai_target, length):
        global ai1_EviscerDot, ai2_EviscerDot, ai3_EviscerDot, ai4_EviscerDot, ai5_EviscerDot
        EviscerDotDamage = math.ceil(ability_data[3])
        if ai_target == 1:
            if length > ai1_EviscerDot[1]:
                ai1_EviscerDot = [EviscerDotDamage, length]
            else:
                return
        if ai_target == 2:
            if length > ai2_EviscerDot[1]:
                ai2_EviscerDot = [EviscerDotDamage, length]
            else:
                return
        if ai_target == 3:
            if length > ai3_EviscerDot[1]:
                ai3_EviscerDot = [EviscerDotDamage, length]
            else:
                return
        if ai_target == 4:
            if length > ai4_EviscerDot[1]:
                ai4_EviscerDot = [EviscerDotDamage, length]
            else:
                return
        if ai_target == 5:
            if length > ai5_EviscerDot[1]:
                ai5_EviscerDot = [EviscerDotDamage, length]
            else:
                return
    def garrote_dot(self, ai_target, length):
        global ai1_garroteDot, ai2_garroteDot, ai3_garroteDot, ai4_garroteDot, ai5_garroteDot
        garroteDotDamage = math.ceil(ability_data[3] * 0.75)
        if ai_target == 1:
            if length > ai1_garroteDot[1]:
                ai1_garroteDot = [garroteDotDamage, length]
            else:
                return
        if ai_target == 2:
            if length > ai2_garroteDot[1]:
                ai2_garroteDot = [garroteDotDamage, length]
            else:
                return
        if ai_target == 3:
            if length > ai3_garroteDot[1]:
                ai3_garroteDot = [garroteDotDamage, length]
            else:
                return
        if ai_target == 4:
            if length > ai4_garroteDot[1]:
                ai4_garroteDot = [garroteDotDamage, length]
            else:
                return
        if ai_target == 5:
            if length > ai5_garroteDot[1]:
                ai5_garroteDot = [garroteDotDamage, length]
            else:
                return
    def clean_up(self):
        if ability_data[1] == "ally":
            champion1_supporttarget_frame.destroy()
            champion2_supporttarget_frame.destroy()
            champion3_supporttarget_frame.destroy()
            champion4_supporttarget_frame.destroy()
            champion5_supporttarget_frame.destroy()
        if ability_data[1] == "enemy":
            if AI_SPAWNED == 1:
                ai1_attacktarget_frame.destroy()
            if AI_SPAWNED == 2:
                ai1_attacktarget_frame.destroy()
                ai2_attacktarget_frame.destroy()
            if AI_SPAWNED == 3:
                ai1_attacktarget_frame.destroy()
                ai2_attacktarget_frame.destroy()
                ai3_attacktarget_frame.destroy()
            if AI_SPAWNED == 4:
                ai1_attacktarget_frame.destroy()
                ai2_attacktarget_frame.destroy()
                ai3_attacktarget_frame.destroy()
                ai4_attacktarget_frame.destroy()
            if AI_SPAWNED == 5:
                ai1_attacktarget_frame.destroy()
                ai2_attacktarget_frame.destroy()
                ai3_attacktarget_frame.destroy()
                ai4_attacktarget_frame.destroy()
                ai5_attacktarget_frame.destroy()

    def target_frame_ai_champion_text(self, ai_or_champion, character_position):
        if ai_or_champion == "champion":
            if character_position == 1:
                if champion1_hp == 0:
                    status_text = "{}\n*DEAD*\nHealth Points: {}/{}".format(CHAMPION_LIST[0], champion1_hp,
                                                                            CHAMPION_1_HP)
                    return status_text
                else:
                    status_text = "{}\nHealth Points: {}/{}".format(CHAMPION_LIST[0], champion1_hp, CHAMPION_1_HP)
                    return status_text
            if character_position == 2:
                if champion2_hp == 0:
                    status_text = "{}\n*DEAD*\nHealth Points: {}/{}".format(CHAMPION_LIST[1], champion2_hp,
                                                                            CHAMPION_2_HP)
                    return status_text
                else:
                    status_text = "{}\nHealth Points: {}/{}".format(CHAMPION_LIST[1], champion2_hp, CHAMPION_2_HP)
                    return status_text
            if character_position == 3:
                if champion3_hp == 0:
                    status_text = "{}\n*DEAD*\nHealth Points: {}/{}".format(CHAMPION_LIST[2], champion3_hp,
                                                                            CHAMPION_3_HP)
                    return status_text
                else:
                    status_text = "{}\nHealth Points: {}/{}".format(CHAMPION_LIST[2], champion3_hp, CHAMPION_3_HP)
                    return status_text
            if character_position == 4:
                if champion4_hp == 0:
                    status_text = "{}\n*DEAD*\nHealth Points: {}/{}".format(CHAMPION_LIST[3], champion4_hp,
                                                                            CHAMPION_4_HP)
                    return status_text
                else:
                    status_text = "{}\nHealth Points: {}/{}".format(CHAMPION_LIST[3], champion4_hp, CHAMPION_4_HP)
                    return status_text
            if character_position == 5:
                if champion5_hp == 0:
                    status_text = "{}\n*DEAD*\nHealth Points: {}/{}".format(CHAMPION_LIST[4], champion5_hp,
                                                                            CHAMPION_5_HP)
                    return status_text
                else:
                    status_text = "{}\nHealth Points: {}/{}".format(CHAMPION_LIST[4], champion5_hp, CHAMPION_5_HP)
                    return status_text
        if ai_or_champion == "ai":
            if character_position == 1:
                if AI_SPAWNED == 1:
                    status_text = "{}\nHealth Points: {}/{}".format(AI_NAME, ai1_hp, ai1_max_hp)
                    return status_text
                if ai1_hp == 0:
                    status_text = "{}#1\n*DEAD*\nHealth Points: {}/{}".format(AI_NAME, ai1_hp,
                                                                              ai1_max_hp)
                    return status_text
                else:
                    status_text = "{}#1\nHealth Points: {}/{}".format(AI_NAME, ai1_hp, ai1_max_hp)
                    return status_text
            if character_position == 2:
                if ai2_hp == 0:
                    status_text = "{}#2\n*DEAD*\nHealth Points: {}/{}".format(AI_NAME, ai2_hp,
                                                                              ai2_max_hp)
                    return status_text
                else:
                    status_text = "{}#2\nHealth Points: {}/{}".format(AI_NAME, ai2_hp, ai2_max_hp)
                    return status_text
            if character_position == 3:
                if ai3_hp == 0:
                    status_text = "{}#3\n*DEAD*\nHealth Points: {}/{}".format(AI_NAME, ai3_hp,
                                                                              ai3_max_hp)
                    return status_text
                else:
                    status_text = "{}#3\nHealth Points: {}/{}".format(AI_NAME, ai3_hp, ai3_max_hp)
                    return status_text
            if character_position == 4:
                if ai4_hp == 0:
                    status_text = "{}#4\n*DEAD*\nHealth Points: {}/{}".format(AI_NAME, ai4_hp,
                                                                              ai4_max_hp)
                    return status_text
                else:
                    status_text = "{}#4\nHealth Points: {}/{}".format(AI_NAME, ai4_hp, ai4_max_hp)
                    return status_text
            if character_position == 5:
                if ai5_hp == 0:
                    status_text = "{}#5\n*DEAD*\nHealth Points: {}/{}".format(AI_NAME, ai5_hp,
                                                                              ai5_max_hp)
                    return status_text
                else:
                    status_text = "{}#5\nHealth Points: {}/{}".format(AI_NAME, ai5_hp, ai5_max_hp)
                    return status_text

    def get_champions_abiltity_button_data(self, champion_position):
        global attack_button_text_list_temp, special_button_text_list_temp
        attack_button_text_list_temp = []
        special_button_text_list_temp = []
        if champion_position == 1:
            for abilities in CHAMPION_1_ATTACKLIST:
                attack_button_text_list_temp.append(abilities)
            while len(attack_button_text_list_temp) < 4:
                attack_button_text_list_temp.append("Empty")
            for abiltities in CHAMPION_1_SPECIALLIST:
                special_button_text_list_temp.append(abiltities)
            while len(special_button_text_list_temp) < 4:
                special_button_text_list_temp.append("Empty")
        if champion_position == 2:
            for abilities in CHAMPION_2_ATTACKLIST:
                attack_button_text_list_temp.append(abilities)
            while len(attack_button_text_list_temp) < 4:
                attack_button_text_list_temp.append("Empty")
            for abiltities in CHAMPION_2_SPECIALLIST:
                special_button_text_list_temp.append(abiltities)
            while len(special_button_text_list_temp) < 4:
                special_button_text_list_temp.append("Empty")
        if champion_position == 3:
            for abilities in CHAMPION_3_ATTACKLIST:
                attack_button_text_list_temp.append(abilities)
            while len(attack_button_text_list_temp) < 4:
                attack_button_text_list_temp.append("Empty")
            for abiltities in CHAMPION_3_SPECIALLIST:
                special_button_text_list_temp.append(abiltities)
            while len(special_button_text_list_temp) < 4:
                special_button_text_list_temp.append("Empty")
        if champion_position == 4:
            for abilities in CHAMPION_4_ATTACKLIST:
                attack_button_text_list_temp.append(abilities)
            while len(attack_button_text_list_temp) < 4:
                attack_button_text_list_temp.append("Empty")
            for abiltities in CHAMPION_4_SPECIALLIST:
                special_button_text_list_temp.append(abiltities)
            while len(special_button_text_list_temp) < 4:
                special_button_text_list_temp.append("Empty")
        if champion_position == 5:
            for abilities in CHAMPION_5_ATTACKLIST:
                attack_button_text_list_temp.append(abilities)
            while len(attack_button_text_list_temp) < 4:
                attack_button_text_list_temp.append("Empty")
            for abiltities in CHAMPION_5_SPECIALLIST:
                special_button_text_list_temp.append(abiltities)
            while len(special_button_text_list_temp) < 4:
                special_button_text_list_temp.append("Empty")
        self.champions_ability_button_text()

    def champions_ability_button_text(self):
        global attack_button_text_list, special_button_text_list
        attack_button_text_list = []
        special_button_text_list = []
        for attack_name in attack_button_text_list_temp:
            if attack_name == "Leg Sweep":
                if leg_sweep_requirements[0] > 0:
                    if leg_sweep_requirements[1] > 0:
                        attack_text = "Leg Sweep ({})\n{} {}".format(leg_sweep_requirements[1], MONK.rp_name,
                                                                     leg_sweep_requirements[0])
                        attack_button_text_list.append(attack_text)
                    else:
                        attack_text = "Leg Sweep\n{} {}".format(MONK.rp_name, leg_sweep_requirements[0])
                        attack_button_text_list.append(attack_text)
                elif leg_sweep_requirements[1] > 0:
                    attack_text = "Leg Sweep ({})".format(leg_sweep_requirements[1])
                    attack_button_text_list.append(attack_text)
                else:
                    attack_button_text_list.append(attack_name)
            elif attack_name == "Pulverize":
                if pulverize_requirements[0] > 0:
                    if pulverize_requirements[1] > 0:
                        attack_text = "Pulverize ({})\n{} {}".format(pulverize_requirements[1], BARBARIAN.rp_name,
                                                                     pulverize_requirements[0])
                        attack_button_text_list.append(attack_text)
                    else:
                        attack_text = "Pulverize\n{} {}".format(BARBARIAN.rp_name, pulverize_requirements[0])
                        attack_button_text_list.append(attack_text)
                elif pulverize_requirements[1] > 0:
                    attack_text = "Pulverize ({})".format(pulverize_requirements[1])
                    attack_button_text_list.append(attack_text)
                else:
                    attack_button_text_list.append(attack_name)
            elif attack_name == "Trainwreck":
                if trainwreck_requirements[0] > 0:
                    if trainwreck_requirements[1] > 0:
                        attack_text = "Trainwreck ({})\n{} {}".format(trainwreck_requirements[1],
                                                                      VETERAN_BODYGUARD.rp_name,
                                                                      trainwreck_requirements[0])
                        attack_button_text_list.append(attack_text)
                    else:
                        attack_text = "Trainwreck\n{} {}".format(VETERAN_BODYGUARD.rp_name, trainwreck_requirements[0])
                        attack_button_text_list.append(attack_text)
                elif trainwreck_requirements[1] > 0:
                    attack_text = "Trainwreck ({})".format(trainwreck_requirements[1])
                    attack_button_text_list.append(attack_text)
                else:
                    attack_button_text_list.append(attack_name)
            elif attack_name == "Disruptive Slash":
                if disruptive_slash_requirements[0] > 0:
                    if disruptive_slash_requirements[1] > 0:
                        attack_text = "Disruptive Slash ({})\n{} {}".format(disruptive_slash_requirements[1],
                                                                            MASTER_FENCER.rp_name,
                                                                            disruptive_slash_requirements[0])
                        attack_button_text_list.append(attack_text)
                    else:
                        attack_text = "Disruptive Slash\n{} {}".format(MASTER_FENCER.rp_name,
                                                                       disruptive_slash_requirements[0])
                        attack_button_text_list.append(attack_text)
                elif disruptive_slash_requirements[1] > 0:
                    attack_text = "Disruptive Slash ({})".format(disruptive_slash_requirements[1])
                    attack_button_text_list.append(attack_text)
                else:
                    attack_button_text_list.append(attack_name)
            elif attack_name == "Rampage":
                if rampage_requirements[0] > 0:
                    if rampage_requirements[1] > 0:
                        attack_text = "Rampage ({})\n{} {}".format(rampage_requirements[1], BERSERKER.rp_name,
                                                                   rampage_requirements[0])
                        attack_button_text_list.append(attack_text)
                    else:
                        attack_text = "Rampage\n{} {}".format(BERSERKER.rp_name, rampage_requirements[0])
                        attack_button_text_list.append(attack_text)
                elif rampage_requirements[1] > 0:
                    attack_text = "Rampage ({})".format(rampage_requirements[1])
                    attack_button_text_list.append(attack_text)
                else:
                    attack_button_text_list.append(attack_name)
            elif attack_name == "Eviscerate":
                if eviscerate_requirements[0] > 0:
                    if eviscerate_requirements[1] > 0:
                        attack_text = "Eviscerate ({})\n{} {}".format(eviscerate_requirements[1], ROGUE.rp_name,
                                                                      eviscerate_requirements[0])
                        attack_button_text_list.append(attack_text)
                    else:
                        attack_text = "Eviscerate\n{} {}".format(ROGUE.rp_name, eviscerate_requirements[0])
                        attack_button_text_list.append(attack_text)
                elif eviscerate_requirements[1] > 0:
                    attack_text = "Eviscerate ({})".format(eviscerate_requirements[1])
                    attack_button_text_list.append(attack_text)
                else:
                    attack_button_text_list.append(attack_name)
            elif attack_name == "Scrap Bomb":
                if scrap_bomb_requirements[0] > 0:
                    if scrap_bomb_requirements[1] > 0:
                        attack_text = "Scrap Bomb ({})\n{} {}".format(scrap_bomb_requirements[1], SURVIVALIST.rp_name,
                                                                      scrap_bomb_requirements[
                                                                          0])
                        attack_button_text_list.append(attack_text)
                    else:
                        attack_text = "Scrap Bomb\n{} {}".format(SURVIVALIST.rp_name, scrap_bomb_requirements[0])
                        attack_button_text_list.append(attack_text)
                elif scrap_bomb_requirements[1] > 0:
                    attack_text = "Scrap Bomb ({})".format(scrap_bomb_requirements[1])
                    attack_button_text_list.append(attack_text)
                else:
                    attack_button_text_list.append(attack_name)
            elif attack_name == "Uppercut":
                if uppercut_requirements[0] > 0:
                    if uppercut_requirements[1] > 0:
                        attack_text = "Uppercut ({})\n{} {}".format(uppercut_requirements[1], BRAWLIST.rp_name,
                                                                    uppercut_requirements[
                                                                        0])
                        attack_button_text_list.append(attack_text)
                    else:
                        attack_text = "Uppercut\n{} {}".format(BRAWLIST.rp_name, uppercut_requirements[0])
                        attack_button_text_list.append(attack_text)
                elif uppercut_requirements[1] > 0:
                    attack_text = "Uppercut ({})".format(uppercut_requirements[1])
                    attack_button_text_list.append(attack_text)
                else:
                    attack_button_text_list.append(attack_name)
            elif attack_name == "Frost Bolt":
                if frost_bolt_requirements[0] > 0:
                    if frost_bolt_requirements[1] > 0:
                        attack_text = "Frost Bolt ({})\n{} {}".format(frost_bolt_requirements[1], ACADEMIC_MAGE.rp_name,
                                                                      frost_bolt_requirements[
                                                                          0])
                        attack_button_text_list.append(attack_text)
                    else:
                        attack_text = "Frost Bolt\n{} {}".format(ACADEMIC_MAGE.rp_name, frost_bolt_requirements[0])
                        attack_button_text_list.append(attack_text)
                elif frost_bolt_requirements[1] > 0:

                    attack_text = "Frost Bolt ({})".format(frost_bolt_requirements[1])
                    attack_button_text_list.append(attack_text)
                else:
                    attack_button_text_list.append(attack_name)
            elif attack_name == "Fireball":
                if fireball_requirements[0] > 0:
                    if fireball_requirements[1] > 0:
                        attack_text = "Fireball ({})\n{} {}".format(fireball_requirements[1], ACADEMIC_MAGE.rp_name,
                                                                    fireball_requirements[
                                                                        0])
                        attack_button_text_list.append(attack_text)
                    else:
                        attack_text = "Fireball\n{} {}".format(ACADEMIC_MAGE.rp_name, fireball_requirements[0])
                        attack_button_text_list.append(attack_text)
                elif fireball_requirements[1] > 0:
                    attack_text = "Fireball ({})".format(fireball_requirements[1])
                    attack_button_text_list.append(attack_text)
                else:
                    attack_button_text_list.append(attack_name)
            elif attack_name == "Venus-fly Snap":
                if venusfly_snap_requirements[0] > 0:
                    if venusfly_snap_requirements[1] > 0:
                        attack_text = "Venus-fly Snap ({})\n{} {}".format(venusfly_snap_requirements[1], DRUID.rp_name,
                                                                          venusfly_snap_requirements[
                                                                              0])
                        attack_button_text_list.append(attack_text)
                    else:
                        attack_text = "Venus-fly Snap\n{} {}".format(DRUID.rp_name, venusfly_snap_requirements[0])
                        attack_button_text_list.append(attack_text)
                elif venusfly_snap_requirements[1] > 0:

                    attack_text = "Venus-fly Snap ({})".format(venusfly_snap_requirements[1])
                    attack_button_text_list.append(attack_text)
                else:
                    attack_button_text_list.append(attack_name)
            elif attack_name == "Vine-Swipe":
                if vine_swipe_requirements[0] > 0:
                    if vine_swipe_requirements[1] > 0:
                        attack_text = "Vine-Swipe ({})\n{} {}".format(vine_swipe_requirements[1], DRUID.rp_name,
                                                                      vine_swipe_requirements[
                                                                          0])
                        attack_button_text_list.append(attack_text)
                    else:
                        attack_text = "Vine-Swipe\n{} {}".format(DRUID.rp_name, vine_swipe_requirements[0])
                        attack_button_text_list.append(attack_text)
                elif vine_swipe_requirements[1] > 0:

                    attack_text = "Vine-Swipe ({})".format(vine_swipe_requirements[1])
                    attack_button_text_list.append(attack_text)
                else:
                    attack_button_text_list.append(attack_name)
            elif attack_name == "Black Bolt":
                if black_bolt_requirements[0] > 0:
                    if black_bolt_requirements[1] > 0:
                        attack_text = "Black Bolt ({})\n{} {}".format(black_bolt_requirements[1], WARLOCK.rp_name,
                                                                      black_bolt_requirements[
                                                                          0])
                        attack_button_text_list.append(attack_text)
                    else:
                        attack_text = "Black Bolt\n{} {}".format(WARLOCK.rp_name, black_bolt_requirements[0])
                        attack_button_text_list.append(attack_text)
                elif black_bolt_requirements[1] > 0:
                    attack_text = "Black Bolt ({})".format(black_bolt_requirements[1])
                    attack_button_text_list.append(attack_text)
                else:
                    attack_button_text_list.append(attack_name)
            elif attack_name == "Blood Spike":
                if blood_spike_requirements[0] > 0:
                    if blood_spike_requirements[1] > 0:
                        attack_text = "Blood Spike ({})\n{} {}".format(blood_spike_requirements[1], BLOODMANCER.rp_name,
                                                                       blood_spike_requirements[
                                                                           0])
                        attack_button_text_list.append(attack_text)
                    else:
                        attack_text = "Blood Spike\n{} {}".format(BLOODMANCER.rp_name, blood_spike_requirements[0])
                        attack_button_text_list.append(attack_text)
                elif blood_spike_requirements[1] > 0:

                    attack_text = "Blood Spike ({})".format(blood_spike_requirements[1])
                    attack_button_text_list.append(attack_text)
                else:
                    attack_button_text_list.append(attack_name)
            elif attack_name == "Rightous Blow":
                if righteous_blow_requirements[0] > 0:
                    if righteous_blow_requirements[1] > 0:
                        attack_text = "Rightous Blow ({})\n{} {}".format(righteous_blow_requirements[1], PALADIN.rp_name,
                                                                         righteous_blow_requirements[
                                                                             0])
                        attack_button_text_list.append(attack_text)
                    else:
                        attack_text = "Rightous Blow\n{} {}".format(PALADIN.rp_name, righteous_blow_requirements[0])
                        attack_button_text_list.append(attack_text)
                elif righteous_blow_requirements[1] > 0:

                    attack_text = "Rightous Blow ({})".format(righteous_blow_requirements[1])
                    attack_button_text_list.append(attack_text)
                else:
                    attack_button_text_list.append(attack_name)
            elif attack_name == "Power Opt":
                if power_opt_requirements[0] > 0:
                    if power_opt_requirements[1] > 0:
                        attack_text = "Power Opt ({})\n{} {}".format(power_opt_requirements[1], CASTLE_RANGER.rp_name,
                                                                     power_opt_requirements[
                                                                         0])
                        attack_button_text_list.append(attack_text)
                    else:
                        attack_text = "Power Opt\n{} {}".format(CASTLE_RANGER.rp_name, power_opt_requirements[0])
                        attack_button_text_list.append(attack_text)
                elif power_opt_requirements[1] > 0:
                    attack_text = "Power Opt ({})".format(power_opt_requirements[1])
                    attack_button_text_list.append(attack_text)
                else:
                    attack_button_text_list.append(attack_name)
            elif attack_name == "Divine Smite":
                if divine_smite_requirements[0] > 0:
                    if divine_smite_requirements[1] > 0:
                        attack_text = "Divine Smite ({})\n{} {}".format(divine_smite_requirements[1],
                                                                        PRIEST_OF_THE_DEVOTED.rp_name,
                                                                        divine_smite_requirements[
                                                                            0])
                        attack_button_text_list.append(attack_text)
                    else:
                        attack_text = "Divine Smite\n{} {}".format(PRIEST_OF_THE_DEVOTED.rp_name,
                                                                   divine_smite_requirements[0])
                        attack_button_text_list.append(attack_text)
                elif divine_smite_requirements[1] > 0:
                    attack_text = "Divine Smite ({})".format(divine_smite_requirements[1])
                    attack_button_text_list.append(attack_text)
                else:
                    attack_button_text_list.append(attack_name)
            else:
                attack_button_text_list.append(attack_name)
        for special_name in special_button_text_list_temp:
            if special_name == "Harmonize":
                if harmonize_requirements[0] > 0:
                    if harmonize_requirements[1] > 0:
                        special_text = "Harmonize ({})\n{} {}".format(harmonize_requirements[1], MONK.rp_name,
                                                                      harmonize_requirements[0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Harmonize\n{} {}".format(MONK.rp_name, harmonize_requirements[0])
                        special_button_text_list.append(special_text)
                elif harmonize_requirements[1] > 0:
                    special_text = "Harmonize ({})".format(harmonize_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Pressure Points":
                if pressure_points_requirements[0] > 0:
                    if pressure_points_requirements[1] > 0:
                        special_text = "Pressure Points ({})\n{} {}".format(pressure_points_requirements[1],
                                                                            MONK.rp_name,
                                                                            pressure_points_requirements[0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Pressure Points\n{} {}".format(MONK.rp_name, pressure_points_requirements[0])
                        special_button_text_list.append(special_text)
                elif pressure_points_requirements[1] > 0:
                    special_text = "Pressure Points ({})".format(pressure_points_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Challenging Shout":
                if challenging_shout_requirements[0] > 0:
                    if challenging_shout_requirements[1] > 0:
                        special_text = "Challenging Shout", "Challenging Shout ({})\n{} {}".format(
                            challenging_shout_requirements[1], BARBARIAN.rp_name, challenging_shout_requirements[0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Challenging Shout", "Challenging Shout\n{} {}".format(BARBARIAN.rp_name,
                                                                                              challenging_shout_requirements[
                                                                                                  0])
                        special_button_text_list.append(special_text)
                elif challenging_shout_requirements[1] > 0:
                    special_text = "Challenging Shout ({})".format(challenging_shout_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Impactful Boast":
                if impactful_boast_requirements[0] > 0:
                    if impactful_boast_requirements[1] > 0:
                        special_text = "Impactful Boast ({})\n{} {}".format(impactful_boast_requirements[1],
                                                                            BARBARIAN.rp_name,
                                                                            impactful_boast_requirements[0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Impactful Boast\n{} {}".format(BARBARIAN.rp_name,
                                                                       impactful_boast_requirements[0])
                        special_button_text_list.append(special_text)
                elif impactful_boast_requirements[1] > 0:
                    special_text = "Impactful Boast ({})".format(impactful_boast_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Fortification":
                if fortification_requirements[0] > 0:
                    if fortification_requirements[1] > 0:
                        special_text = "Fortification", "Fortification ({})\n{} {}".format(
                            fortification_requirements[1], VETERAN_BODYGUARD.rp_name, fortification_requirements[0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Fortification", "Fortification\n{} {}".format(VETERAN_BODYGUARD.rp_name,
                                                                                      fortification_requirements[0])
                        special_button_text_list.append(special_text)
                elif fortification_requirements[1] > 0:
                    special_text = "Fortification ({})".format(fortification_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Parry":
                if parry_requirements[0] > 0:
                    if parry_requirements[1] > 0:
                        special_text = "Parry ({})\n{} {}".format(parry_requirements[1], MASTER_FENCER.rp_name,
                                                                  parry_requirements[0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Parry\n{} {}".format(MASTER_FENCER.rp_name, parry_requirements[0])
                        special_button_text_list.append(special_text)
                elif parry_requirements[1] > 0:
                    special_text = "Parry ({})".format(parry_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Elusive Measures":
                if elusive_measures_requirements[0] > 0:
                    if elusive_measures_requirements[1] > 0:
                        special_text = "Elusive Measures ({})\n{} {}".format(elusive_measures_requirements[1],
                                                                             MASTER_FENCER.rp_name,
                                                                             elusive_measures_requirements[0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Elusive Measures\n{} {}".format(MASTER_FENCER.rp_name,
                                                                        elusive_measures_requirements[0])
                        special_button_text_list.append(special_text)
                elif elusive_measures_requirements[1] > 0:
                    special_text = "Elusive Measures ({})".format(elusive_measures_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Reckless Flurry":
                if reckless_flurry_requirements[0] > 0:
                    if reckless_flurry_requirements[1] > 0:
                        special_text = "Reckless Flurry ({})\n{} {}".format(reckless_flurry_requirements[1],
                                                                            BERSERKER.rp_name,
                                                                            reckless_flurry_requirements[0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Reckless Flurry\n{} {}".format(BERSERKER.rp_name,
                                                                       reckless_flurry_requirements[0])
                        special_button_text_list.append(special_text)
                elif reckless_flurry_requirements[1] > 0:
                    special_text = "Reckless Flurry ({})".format(reckless_flurry_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Exploit Weakness":
                if exploit_weakness_requirements[0] > 0:
                    if exploit_weakness_requirements[1] > 0:
                        special_text = "Exploit Weakness ({})\n{} {}".format(exploit_weakness_requirements[1],
                                                                             ROGUE.rp_name,
                                                                             exploit_weakness_requirements[
                                                                                 0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Exploit Weakness\n{} {}".format(ROGUE.rp_name, exploit_weakness_requirements[0])
                        special_button_text_list.append(special_text)
                elif exploit_weakness_requirements[1] > 0:
                    special_text = "Exploit Weakness ({})".format(exploit_weakness_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Play Dead":
                if play_dead_requirements[0] > 0:
                    if play_dead_requirements[1] > 0:
                        special_text = "Play Dead ({})\n{} {}".format(play_dead_requirements[1], SURVIVALIST.rp_name,
                                                                      play_dead_requirements[
                                                                          0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Play Dead\n{} {}".format(SURVIVALIST.rp_name, play_dead_requirements[0])
                        special_button_text_list.append(special_text)
                elif play_dead_requirements[1] > 0:
                    special_text = "Play Dead ({})".format(play_dead_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Rushed Rest":
                if rushed_rest_requirements[0] > 0:
                    if rushed_rest_requirements[1] > 0:
                        special_text = "Rushed Rest ({})\n{} {}".format(rushed_rest_requirements[1],
                                                                        SURVIVALIST.rp_name, rushed_rest_requirements[
                                                                            0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Rushed Rest\n{} {}".format(SURVIVALIST.rp_name, rushed_rest_requirements[0])
                        special_button_text_list.append(special_text)
                elif rushed_rest_requirements[1] > 0:
                    special_text = "Rushed Rest ({})".format(rushed_rest_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Defensive Stance":
                if defensive_stance_requirements[0] > 0:
                    if defensive_stance_requirements[1] > 0:
                        special_text = "Defensive Stance ({})\n{} {}".format(defensive_stance_requirements[1],
                                                                             BRAWLIST.rp_name,
                                                                             defensive_stance_requirements[
                                                                                 0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Defensive Stance\n{} {}".format(BRAWLIST.rp_name,
                                                                        defensive_stance_requirements[0])
                        special_button_text_list.append(special_text)
                elif defensive_stance_requirements[1] > 0:
                    special_text = "Defensive Stance ({})".format(defensive_stance_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Rushdown":
                if rushdown_requirements[0] > 0:
                    if rushdown_requirements[1] > 0:
                        special_text = "Rushdown ({})\n{} {}".format(rushdown_requirements[1], BRAWLIST.rp_name,
                                                                     rushdown_requirements[
                                                                         0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Rushdown\n{} {}".format(BRAWLIST.rp_name, rushdown_requirements[0])
                        special_button_text_list.append(special_text)
                elif rushdown_requirements[1] > 0:
                    special_text = "Rushdown ({})".format(rushdown_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Arcane Brilliance":
                if arcane_brilliance_requirements[0] > 0:
                    if arcane_brilliance_requirements[1] > 0:
                        special_text = "Arcane Brilliance ({})\n{} {}".format(arcane_brilliance_requirements[1],
                                                                              ACADEMIC_MAGE.rp_name,
                                                                              arcane_brilliance_requirements[
                                                                                  0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Arcane Brilliance\n{} {}".format(ACADEMIC_MAGE.rp_name,
                                                                         arcane_brilliance_requirements[0])
                        special_button_text_list.append(special_text)
                elif arcane_brilliance_requirements[1] > 0:
                    special_text = "Arcane Brilliance ({})".format(arcane_brilliance_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Magical Barrier":
                if magical_barrier_requirements[0] > 0:
                    if magical_barrier_requirements[1] > 0:
                        special_text = "Magical Barrier ({})\n{} {}".format(magical_barrier_requirements[1],
                                                                            ACADEMIC_MAGE.rp_name,
                                                                            magical_barrier_requirements[
                                                                                0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Magical Barrier\n{} {}".format(ACADEMIC_MAGE.rp_name,
                                                                       magical_barrier_requirements[0])
                        special_button_text_list.append(special_text)
                elif magical_barrier_requirements[1] > 0:
                    special_text = "Magical Barrier ({})".format(magical_barrier_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Thorns":
                if thorns_requirements[0] > 0:
                    if thorns_requirements[1] > 0:
                        special_text = "Thorns ({})\n{} {}".format(thorns_requirements[1], DRUID.rp_name,
                                                                   thorns_requirements[
                                                                       0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Thorns\n{} {}".format(DRUID.rp_name, thorns_requirements[0])
                        special_button_text_list.append(special_text)
                elif thorns_requirements[1] > 0:
                    special_text = "Thorns ({})".format(thorns_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Prickle Arena":
                if prickle_arena_requirements[0] > 0:
                    if prickle_arena_requirements[1] > 0:
                        special_text = "Prickle Arena ({})\n{} {}".format(prickle_arena_requirements[1], DRUID.rp_name,
                                                                          prickle_arena_requirements[
                                                                              0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Prickle Arena\n{} {}".format(DRUID.rp_name, prickle_arena_requirements[0])
                        special_button_text_list.append(special_text)
                elif prickle_arena_requirements[1] > 0:
                    special_text = "Prickle Arena ({})".format(prickle_arena_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Void Infusion":
                if void_infusion_requirements[0] > 0:
                    if void_infusion_requirements[1] > 0:
                        special_text = "Void Infusion ({})\n{} {}".format(void_infusion_requirements[1],
                                                                          WARLOCK.rp_name, void_infusion_requirements[
                                                                              0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Void Infusion\n{} {}".format(WARLOCK.rp_name, void_infusion_requirements[0])
                        special_button_text_list.append(special_text)
                elif void_infusion_requirements[1] > 0:
                    special_text = "Void Infusion ({})".format(void_infusion_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Wound Fissure":
                if wound_fissure_requirements[0] > 0:
                    if wound_fissure_requirements[1] > 0:
                        special_text = "Wound Fissure ({})\n{} {}".format(wound_fissure_requirements[1],
                                                                          WARLOCK.rp_name, wound_fissure_requirements[
                                                                              0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Wound Fissure\n{} {}".format(WARLOCK.rp_name, wound_fissure_requirements[0])
                        special_button_text_list.append(special_text)
                elif wound_fissure_requirements[1] > 0:
                    special_text = "Wound Fissure ({})".format(wound_fissure_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Blood Boil":
                if blood_boil_requirements[0] > 0:
                    if blood_boil_requirements[1] > 0:
                        special_text = "Blood Boil ({})\n{} {}".format(blood_boil_requirements[1], BLOODMANCER.rp_name,
                                                                       blood_boil_requirements[
                                                                           0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Blood Boil\n{} {}".format(BLOODMANCER.rp_name, blood_boil_requirements[0])
                        special_button_text_list.append(special_text)
                elif blood_boil_requirements[1] > 0:
                    special_text = "Blood Boil ({})".format(blood_boil_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Enharden Nerves":
                if enharden_nerves_requirements[0] > 0:
                    if enharden_nerves_requirements[1] > 0:
                        special_text = "Enharden Nerves ({})\n{} {}".format(enharden_nerves_requirements[1],
                                                                            BLOODMANCER.rp_name,
                                                                            enharden_nerves_requirements[
                                                                                0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Enharden Nerves\n{} {}".format(BLOODMANCER.rp_name,
                                                                       enharden_nerves_requirements[0])
                        special_button_text_list.append(special_text)
                elif enharden_nerves_requirements[1] > 0:
                    special_text = "Enharden Nerves ({})".format(enharden_nerves_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Aura of Power":
                if aura_of_power_requirements[0] > 0:
                    if aura_of_power_requirements[1] > 0:
                        special_text = "Aura of Power ({})\n{} {}".format(aura_of_power_requirements[1],
                                                                          PALADIN.rp_name, aura_of_power_requirements[
                                                                              0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Aura of Power\n{} {}".format(PALADIN.rp_name, aura_of_power_requirements[0])
                        special_button_text_list.append(special_text)
                elif aura_of_power_requirements[1] > 0:
                    special_text = "Aura of Power ({})".format(aura_of_power_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Aura of Protection":
                if aura_of_protection_requirements[0] > 0:
                    if aura_of_protection_requirements[1] > 0:
                        special_text = "Aura of Protection ({})\n{} {}".format(aura_of_protection_requirements[1],
                                                                               PALADIN.rp_name,
                                                                               aura_of_protection_requirements[
                                                                                   0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Aura of Protection\n{} {}".format(PALADIN.rp_name,
                                                                          aura_of_protection_requirements[0])
                        special_button_text_list.append(special_text)
                elif aura_of_protection_requirements[1] > 0:
                    special_text = "Aura of Protection ({})".format(aura_of_protection_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Equip Iron-cast Arrows":
                if equip_iron_cast_arrows_requirements[0] > 0:
                    if equip_iron_cast_arrows_requirements[1] > 0:
                        special_text = "Equip Iron-cast Arrows ({})\n{} {}".format(
                            equip_iron_cast_arrows_requirements[1], CASTLE_RANGER.rp_name,
                            equip_iron_cast_arrows_requirements[
                                0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Equip Iron-cast Arrows\n{} {}".format(CASTLE_RANGER.rp_name,
                                                                              equip_iron_cast_arrows_requirements[0])
                        special_button_text_list.append(special_text)
                elif equip_iron_cast_arrows_requirements[1] > 0:
                    special_text = "Equip Iron-cast Arrows ({})".format(equip_iron_cast_arrows_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Equip Tracker-tipped Arrows":
                if equip_tracker_tipped_arrows_requirements[0] > 0:
                    if equip_tracker_tipped_arrows_requirements[1] > 0:
                        special_text = "Equip Tracker-tipped Arrows ({})\n{} {}".format(
                            equip_tracker_tipped_arrows_requirements[1], CASTLE_RANGER.rp_name,
                            equip_tracker_tipped_arrows_requirements[
                                0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Equip Tracker-tipped Arrows\n{} {}".format(CASTLE_RANGER.rp_name,
                                                                                   equip_tracker_tipped_arrows_requirements[
                                                                                       0])
                        special_button_text_list.append(special_text)
                elif equip_tracker_tipped_arrows_requirements[1] > 0:
                    special_text = "Equip Tracker-tipped Arrows ({})".format(
                        equip_tracker_tipped_arrows_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Crashing Boom":
                if crashing_boom_requirements[0] > 0:
                    if crashing_boom_requirements[1] > 0:
                        special_text = "Crashing Boom ({})\n{} {}".format(crashing_boom_requirements[1],
                                                                          THUNDER_APPRENTICE.rp_name,
                                                                          crashing_boom_requirements[
                                                                              0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Crashing Boom\n{} {}".format(THUNDER_APPRENTICE.rp_name,
                                                                     crashing_boom_requirements[0])
                        special_button_text_list.append(special_text)
                elif crashing_boom_requirements[1] > 0:
                    special_text = "Crashing Boom ({})".format(crashing_boom_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Power Surge":
                if power_surge_requirements[0] > 0:
                    if power_surge_requirements[1] > 0:
                        special_text = "Power Surge ({})\n{} {}".format(power_surge_requirements[1],
                                                                        POWER_CONDUIT.rp_name, power_surge_requirements[
                                                                            0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Power Surge\n{} {}".format(POWER_CONDUIT.rp_name, power_surge_requirements[0])
                        special_button_text_list.append(special_text)
                elif power_surge_requirements[1] > 0:
                    special_text = "Power Surge ({})".format(power_surge_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Full Potential":
                if full_potential_requirements[0] > 0:
                    if full_potential_requirements[1] > 0:
                        special_text = "Full Potential ({})\n{} {}".format(full_potential_requirements[1],
                                                                           POWER_CONDUIT.rp_name,
                                                                           full_potential_requirements[
                                                                               0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Full Potential\n{} {}".format(POWER_CONDUIT.rp_name,
                                                                      full_potential_requirements[0])
                        special_button_text_list.append(special_text)
                elif full_potential_requirements[1] > 0:
                    special_text = "Full Potential ({})".format(full_potential_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Healing Surge":
                if healing_surge_requirements[0] > 0:
                    if healing_surge_requirements[1] > 0:
                        special_text = "Healing Surge ({})\n{} {}".format(healing_surge_requirements[1],
                                                                          EARTH_SPEAKER.rp_name,
                                                                          healing_surge_requirements[
                                                                              0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Healing Surge\n{} {}".format(EARTH_SPEAKER.rp_name,
                                                                     healing_surge_requirements[0])
                        special_button_text_list.append(special_text)
                elif healing_surge_requirements[1] > 0:
                    special_text = "Healing Surge ({})".format(healing_surge_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Rejuvenating Whirlpool":
                if rejuvenating_whirlpool_requirements[0] > 0:
                    if rejuvenating_whirlpool_requirements[1] > 0:
                        special_text = "Rejuvenating Whirlpool ({})\n{} {}".format(
                            rejuvenating_whirlpool_requirements[1], EARTH_SPEAKER.rp_name,
                            rejuvenating_whirlpool_requirements[
                                0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Rejuvenating Whirlpool\n{} {}".format(EARTH_SPEAKER.rp_name,
                                                                              rejuvenating_whirlpool_requirements[0])
                        special_button_text_list.append(special_text)
                elif rejuvenating_whirlpool_requirements[1] > 0:
                    special_text = "Rejuvenating Whirlpool ({})".format(rejuvenating_whirlpool_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Boulder Cocoon":
                if boulder_cocoon_requirements[0] > 0:
                    if boulder_cocoon_requirements[1] > 0:
                        special_text = "Boulder Cocoon ({})\n{} {}".format(boulder_cocoon_requirements[1],
                                                                           EARTH_SPEAKER.rp_name,
                                                                           boulder_cocoon_requirements[
                                                                               0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Boulder Cocoon\n{} {}".format(EARTH_SPEAKER.rp_name,
                                                                      boulder_cocoon_requirements[0])
                        special_button_text_list.append(special_text)
                elif boulder_cocoon_requirements[1] > 0:
                    special_text = "Boulder Cocoon ({})".format(boulder_cocoon_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Healing Light":
                if healing_light_requirements[0] > 0:
                    if healing_light_requirements[1] > 0:
                        special_text = "Healing Light ({})\n{} {}".format(healing_light_requirements[1],
                                                                          PRIEST_OF_THE_DEVOTED.rp_name,
                                                                          healing_light_requirements[
                                                                              0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Healing Light\n{} {}".format(PRIEST_OF_THE_DEVOTED.rp_name,
                                                                     healing_light_requirements[0])
                        special_button_text_list.append(special_text)
                elif healing_light_requirements[1] > 0:
                    special_text = "Healing Light ({})".format(healing_light_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Diffracting Nova":
                if diffracting_nova_requirements[0] > 0:
                    if diffracting_nova_requirements[1] > 0:
                        special_text = "Diffracting Nova ({})\n{} {}".format(diffracting_nova_requirements[1],
                                                                             PRIEST_OF_THE_DEVOTED.rp_name,
                                                                             diffracting_nova_requirements[
                                                                                 0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Diffracting Nova\n{} {}".format(PRIEST_OF_THE_DEVOTED.rp_name,
                                                                        diffracting_nova_requirements[0])
                        special_button_text_list.append(special_text)
                elif diffracting_nova_requirements[1] > 0:
                    special_text = "Diffracting Nova ({})".format(diffracting_nova_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Nanoheal Bots":
                if nanoheal_bots_requirements[0] > 0:
                    if nanoheal_bots_requirements[1] > 0:
                        special_text = "Nanoheal Bots ({})\n{} {}".format(nanoheal_bots_requirements[1],
                                                                          TIME_WALKER.rp_name,
                                                                          nanoheal_bots_requirements[
                                                                              0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Nanoheal Bots\n{} {}".format(TIME_WALKER.rp_name, nanoheal_bots_requirements[0])
                        special_button_text_list.append(special_text)
                elif nanoheal_bots_requirements[1] > 0:
                    special_text = "Nanoheal Bots ({})".format(nanoheal_bots_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Reverse Wounds":
                if reverse_wounds_requirements[0] > 0:
                    if reverse_wounds_requirements[1] > 0:
                        special_text = "Reverse Wounds ({})\n{} {}".format(reverse_wounds_requirements[1],
                                                                           TIME_WALKER.rp_name,
                                                                           reverse_wounds_requirements[
                                                                               0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Reverse Wounds\n{} {}".format(TIME_WALKER.rp_name,
                                                                      reverse_wounds_requirements[0])
                        special_button_text_list.append(special_text)
                elif reverse_wounds_requirements[1] > 0:
                    special_text = "Reverse Wounds ({})".format(reverse_wounds_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Alter Time":
                if alter_time_requirements[0] > 0:
                    if alter_time_requirements[1] > 0:
                        special_text = "Alter Time ({})\n{} {}".format(alter_time_requirements[1], TIME_WALKER.rp_name,
                                                                       alter_time_requirements[
                                                                           0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Alter Time\n{} {}".format(TIME_WALKER.rp_name, alter_time_requirements[0])
                        special_button_text_list.append(special_text)
                elif alter_time_requirements[1] > 0:
                    special_text = "Alter Time ({})".format(alter_time_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "Perfected Herbal Tea":
                if perfected_herbal_tea_requirements[0] > 0:
                    if perfected_herbal_tea_requirements[1] > 0:
                        special_text = "Perfected Herbal Tea ({})\n{} {}".format(perfected_herbal_tea_requirements[1],
                                                                                 CHILD_OF_MEDICINE.rp_name,
                                                                                 perfected_herbal_tea_requirements[
                                                                                     0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "Perfected Herbal Tea\n{} {}".format(CHILD_OF_MEDICINE.rp_name,
                                                                            perfected_herbal_tea_requirements[0])
                        special_button_text_list.append(special_text)
                elif perfected_herbal_tea_requirements[1] > 0:
                    special_text = "Perfected Herbal Tea ({})".format(perfected_herbal_tea_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            elif special_name == "G.3.T J.A.X.D":
                if g3t_jaxd_requirements[0] > 0:
                    if g3t_jaxd_requirements[1] > 0:
                        special_text = "G.3.T J.A.X.D ({})\n{} {}".format(g3t_jaxd_requirements[1],
                                                                          CHILD_OF_MEDICINE.rp_name,
                                                                          g3t_jaxd_requirements[
                                                                              0])
                        special_button_text_list.append(special_text)
                    else:
                        special_text = "G.3.T J.A.X.D\n{} {}".format(CHILD_OF_MEDICINE.rp_name,
                                                                     g3t_jaxd_requirements[0])
                        special_button_text_list.append(special_text)
                elif g3t_jaxd_requirements[1] > 0:
                    special_text = "G.3.T J.A.X.D ({})".format(g3t_jaxd_requirements[1])
                    special_button_text_list.append(special_text)
                else:
                    special_button_text_list.append(special_name)
            else:
                special_button_text_list.append(special_name)


class CreateTeamPage(tk.Frame):
    def __init__(self, parent, controller):
        global update_page_button
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.update_variables()
        label = tk.Label(self, text="Champion Camp", font=controller.title_font)
        team_1_button = tk.Button(self, text=team_1_button_text,
                                  command=lambda: controller.show_frame("Team1SelectionPage"))
        team_2_button = tk.Button(self, text=team_2_button_text,
                                  command=lambda: controller.show_frame("Team2SelectionPage"))
        team_3_button = tk.Button(self, text=team_3_button_text,
                                  command=lambda: controller.show_frame("Team3SelectionPage"))
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
        global decoded_dungeoneer_team1, decoded_dungeoneer_team2, decoded_dungeoneer_team3, team_1_button_text, team_2_button_text, team_3_button_text
        user = self.get_user()
        team_1_list_data = []
        team_2_list_data = []
        team_3_list_data = []
        team_line_1 = ParentClass.return_users_champion_team1(self, user)
        team_line_1 = team_line_1.replace(",", "")
        team_1_list_data = team_line_1.split()
        team_line_2 = ParentClass.return_users_champion_team2(self, user)
        team_line_2 = team_line_2.replace(",", "")
        team_2_list_data = team_line_2.split()
        team_line_3 = ParentClass.return_users_champion_team3(self, user)
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
        user = ParentClass.get_user_encoded(self)
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
                    if character == MONK.code:
                        decoded_dungeoneer_team1.append(MONK.title)
                    if character == BARBARIAN.code:
                        decoded_dungeoneer_team1.append(BARBARIAN.title)
                    if character == VETERAN_BODYGUARD.code:
                        decoded_dungeoneer_team1.append(VETERAN_BODYGUARD.title)
                    if character == MASTER_FENCER.code:
                        decoded_dungeoneer_team1.append(MASTER_FENCER.title)
                    if character == BERSERKER.code:
                        decoded_dungeoneer_team1.append(BERSERKER.title)
                    if character == ROGUE.code:
                        decoded_dungeoneer_team1.append(ROGUE.title)
                    if character == SURVIVALIST.code:
                        decoded_dungeoneer_team1.append(SURVIVALIST.title)
                    if character == BRAWLIST.code:
                        decoded_dungeoneer_team1.append(BRAWLIST.title)
                    if character == ACADEMIC_MAGE.code:
                        decoded_dungeoneer_team1.append(ACADEMIC_MAGE.title)
                    if character == DRUID.code:
                        decoded_dungeoneer_team1.append(DRUID.title)
                    if character == WARLOCK.code:
                        decoded_dungeoneer_team1.append(WARLOCK.title)
                    if character == BLOODMANCER.code:
                        decoded_dungeoneer_team1.append(BLOODMANCER.title)
                    if character == PALADIN.code:
                        decoded_dungeoneer_team1.append(PALADIN.title)
                    if character == CASTLE_RANGER.code:
                        decoded_dungeoneer_team1.append(CASTLE_RANGER.title)
                    if character == THUNDER_APPRENTICE.code:
                        decoded_dungeoneer_team1.append(THUNDER_APPRENTICE.title)
                    if character == POWER_CONDUIT.code:
                        decoded_dungeoneer_team1.append(POWER_CONDUIT.title)
                    if character == EARTH_SPEAKER.code:
                        decoded_dungeoneer_team1.append(EARTH_SPEAKER.title)
                    if character == PRIEST_OF_THE_DEVOTED.code:
                        decoded_dungeoneer_team1.append(PRIEST_OF_THE_DEVOTED.title)
                    if character == TIME_WALKER.code:
                        decoded_dungeoneer_team1.append(TIME_WALKER.title)
                    if character == CHILD_OF_MEDICINE.code:
                        decoded_dungeoneer_team1.append(CHILD_OF_MEDICINE.title)
                    if not character:
                        break
            else:
                for character in team_1_list_data:
                    if character == MONK.code:
                        decoded_dungeoneer_team1.append(MONK.title)
                    if character == BARBARIAN.code:
                        decoded_dungeoneer_team1.append(BARBARIAN.title)
                    if character == VETERAN_BODYGUARD.code:
                        decoded_dungeoneer_team1.append(VETERAN_BODYGUARD.title)
                    if character == MASTER_FENCER.code:
                        decoded_dungeoneer_team1.append(MASTER_FENCER.title)
                    if character == BERSERKER.code:
                        decoded_dungeoneer_team1.append(BERSERKER.title)
                    if character == ROGUE.code:
                        decoded_dungeoneer_team1.append(ROGUE.title)
                    if character == SURVIVALIST.code:
                        decoded_dungeoneer_team1.append(SURVIVALIST.title)
                    if character == BRAWLIST.code:
                        decoded_dungeoneer_team1.append(BRAWLIST.title)
                    if character == ACADEMIC_MAGE.code:
                        decoded_dungeoneer_team1.append(ACADEMIC_MAGE.title)
                    if character == DRUID.code:
                        decoded_dungeoneer_team1.append(DRUID.title)
                    if character == WARLOCK.code:
                        decoded_dungeoneer_team1.append(WARLOCK.title)
                    if character == BLOODMANCER.code:
                        decoded_dungeoneer_team1.append(BLOODMANCER.title)
                    if character == PALADIN.code:
                        decoded_dungeoneer_team1.append(PALADIN.title)
                    if character == CASTLE_RANGER.code:
                        decoded_dungeoneer_team1.append(CASTLE_RANGER.title)
                    if character == THUNDER_APPRENTICE.code:
                        decoded_dungeoneer_team1.append(THUNDER_APPRENTICE.title)
                    if character == POWER_CONDUIT.code:
                        decoded_dungeoneer_team1.append(POWER_CONDUIT.title)
                    if character == EARTH_SPEAKER.code:
                        decoded_dungeoneer_team1.append(EARTH_SPEAKER.title)
                    if character == PRIEST_OF_THE_DEVOTED.code:
                        decoded_dungeoneer_team1.append(PRIEST_OF_THE_DEVOTED.title)
                    if character == TIME_WALKER.code:
                        decoded_dungeoneer_team1.append(TIME_WALKER.title)
                    if character == CHILD_OF_MEDICINE.code:
                        decoded_dungeoneer_team1.append(CHILD_OF_MEDICINE.title)
                return decoded_dungeoneer_team1
        if len(decoded_dungeoneer_team1) < 5:
            while len(decoded_dungeoneer_team1) < 5:
                decoded_dungeoneer_team1.append("Empty")
            return decoded_dungeoneer_team1

    def team_2_decode(self, team_2_list_data):
        decoded_dungeoneer_team2 = []
        if len(team_2_list_data) == 0:
            decoded_dungeoneer_team2.append("Empty")
            return decoded_dungeoneer_team2
        else:
            if len(team_2_list_data) < 5:
                for character in team_2_list_data:
                    if character == MONK.code:
                        decoded_dungeoneer_team2.append(MONK.title)
                    if character == BARBARIAN.code:
                        decoded_dungeoneer_team2.append(BARBARIAN.title)
                    if character == VETERAN_BODYGUARD.code:
                        decoded_dungeoneer_team2.append(VETERAN_BODYGUARD.title)
                    if character == MASTER_FENCER.code:
                        decoded_dungeoneer_team2.append(MASTER_FENCER.title)
                    if character == BERSERKER.code:
                        decoded_dungeoneer_team2.append(BERSERKER.title)
                    if character == ROGUE.code:
                        decoded_dungeoneer_team2.append(ROGUE.title)
                    if character == SURVIVALIST.code:
                        decoded_dungeoneer_team2.append(SURVIVALIST.title)
                    if character == BRAWLIST.code:
                        decoded_dungeoneer_team2.append(BRAWLIST.title)
                    if character == ACADEMIC_MAGE.code:
                        decoded_dungeoneer_team2.append(ACADEMIC_MAGE.title)
                    if character == DRUID.code:
                        decoded_dungeoneer_team2.append(DRUID.title)
                    if character == WARLOCK.code:
                        decoded_dungeoneer_team2.append(WARLOCK.title)
                    if character == BLOODMANCER.code:
                        decoded_dungeoneer_team2.append(BLOODMANCER.title)
                    if character == PALADIN.code:
                        decoded_dungeoneer_team2.append(PALADIN.title)
                    if character == CASTLE_RANGER.code:
                        decoded_dungeoneer_team2.append(CASTLE_RANGER.title)
                    if character == THUNDER_APPRENTICE.code:
                        decoded_dungeoneer_team2.append(THUNDER_APPRENTICE.title)
                    if character == POWER_CONDUIT.code:
                        decoded_dungeoneer_team2.append(POWER_CONDUIT.title)
                    if character == EARTH_SPEAKER.code:
                        decoded_dungeoneer_team2.append(EARTH_SPEAKER.title)
                    if character == PRIEST_OF_THE_DEVOTED.code:
                        decoded_dungeoneer_team2.append(PRIEST_OF_THE_DEVOTED.title)
                    if character == TIME_WALKER.code:
                        decoded_dungeoneer_team2.append(TIME_WALKER.title)
                    if character == CHILD_OF_MEDICINE.code:
                        decoded_dungeoneer_team2.append(CHILD_OF_MEDICINE.title)
                    if not character:
                        break
            else:
                for character in team_2_list_data:
                    if character == MONK.code:
                        decoded_dungeoneer_team2.append(MONK.title)
                    if character == BARBARIAN.code:
                        decoded_dungeoneer_team2.append(BARBARIAN.title)
                    if character == VETERAN_BODYGUARD.code:
                        decoded_dungeoneer_team2.append(VETERAN_BODYGUARD.title)
                    if character == MASTER_FENCER.code:
                        decoded_dungeoneer_team2.append(MASTER_FENCER.title)
                    if character == BERSERKER.code:
                        decoded_dungeoneer_team2.append(BERSERKER.title)
                    if character == ROGUE.code:
                        decoded_dungeoneer_team2.append(ROGUE.title)
                    if character == SURVIVALIST.code:
                        decoded_dungeoneer_team2.append(SURVIVALIST.title)
                    if character == BRAWLIST.code:
                        decoded_dungeoneer_team2.append(BRAWLIST.title)
                    if character == ACADEMIC_MAGE.code:
                        decoded_dungeoneer_team2.append(ACADEMIC_MAGE.title)
                    if character == DRUID.code:
                        decoded_dungeoneer_team2.append(DRUID.title)
                    if character == WARLOCK.code:
                        decoded_dungeoneer_team2.append(WARLOCK.title)
                    if character == BLOODMANCER.code:
                        decoded_dungeoneer_team2.append(BLOODMANCER.title)
                    if character == PALADIN.code:
                        decoded_dungeoneer_team2.append(PALADIN.title)
                    if character == CASTLE_RANGER.code:
                        decoded_dungeoneer_team2.append(CASTLE_RANGER.title)
                    if character == THUNDER_APPRENTICE.code:
                        decoded_dungeoneer_team2.append(THUNDER_APPRENTICE.title)
                    if character == POWER_CONDUIT.code:
                        decoded_dungeoneer_team2.append(POWER_CONDUIT.title)
                    if character == EARTH_SPEAKER.code:
                        decoded_dungeoneer_team2.append(EARTH_SPEAKER.title)
                    if character == PRIEST_OF_THE_DEVOTED.code:
                        decoded_dungeoneer_team2.append(PRIEST_OF_THE_DEVOTED.title)
                    if character == TIME_WALKER.code:
                        decoded_dungeoneer_team2.append(TIME_WALKER.title)
                    if character == CHILD_OF_MEDICINE.code:
                        decoded_dungeoneer_team2.append(CHILD_OF_MEDICINE.title)
                return decoded_dungeoneer_team2
        if len(decoded_dungeoneer_team2) < 5:
            while len(decoded_dungeoneer_team2) < 5:
                decoded_dungeoneer_team2.append("Empty")
            return decoded_dungeoneer_team2

    def team_3_decode(self, team_3_list_data):
        decoded_dungeoneer_team3 = []
        if len(team_3_list_data) == 0:
            decoded_dungeoneer_team3.append("Empty")
            return decoded_dungeoneer_team3
        else:
            if len(team_3_list_data) < 5:
                for character in team_3_list_data:
                    if character == MONK.code:
                        decoded_dungeoneer_team3.append(MONK.title)
                    if character == BARBARIAN.code:
                        decoded_dungeoneer_team3.append(BARBARIAN.title)
                    if character == VETERAN_BODYGUARD.code:
                        decoded_dungeoneer_team3.append(VETERAN_BODYGUARD.title)
                    if character == MASTER_FENCER.code:
                        decoded_dungeoneer_team3.append(MASTER_FENCER.title)
                    if character == BERSERKER.code:
                        decoded_dungeoneer_team3.append(BERSERKER.title)
                    if character == ROGUE.code:
                        decoded_dungeoneer_team3.append(ROGUE.title)
                    if character == SURVIVALIST.code:
                        decoded_dungeoneer_team3.append(SURVIVALIST.title)
                    if character == BRAWLIST.code:
                        decoded_dungeoneer_team3.append(BRAWLIST.title)
                    if character == ACADEMIC_MAGE.code:
                        decoded_dungeoneer_team3.append(ACADEMIC_MAGE.title)
                    if character == DRUID.code:
                        decoded_dungeoneer_team3.append(DRUID.title)
                    if character == WARLOCK.code:
                        decoded_dungeoneer_team3.append(WARLOCK.title)
                    if character == BLOODMANCER.code:
                        decoded_dungeoneer_team3.append(BLOODMANCER.title)
                    if character == PALADIN.code:
                        decoded_dungeoneer_team3.append(PALADIN.title)
                    if character == CASTLE_RANGER.code:
                        decoded_dungeoneer_team3.append(CASTLE_RANGER.title)
                    if character == THUNDER_APPRENTICE.code:
                        decoded_dungeoneer_team3.append(THUNDER_APPRENTICE.title)
                    if character == POWER_CONDUIT.code:
                        decoded_dungeoneer_team3.append(POWER_CONDUIT.title)
                    if character == EARTH_SPEAKER.code:
                        decoded_dungeoneer_team3.append(EARTH_SPEAKER.title)
                    if character == PRIEST_OF_THE_DEVOTED.code:
                        decoded_dungeoneer_team3.append(PRIEST_OF_THE_DEVOTED.title)
                    if character == TIME_WALKER.code:
                        decoded_dungeoneer_team3.append(TIME_WALKER.title)
                    if character == CHILD_OF_MEDICINE.code:
                        decoded_dungeoneer_team3.append(CHILD_OF_MEDICINE.title)
                    if not character:
                        break
            else:
                for character in team_3_list_data:
                    if character == MONK.code:
                        decoded_dungeoneer_team3.append(MONK.title)
                    if character == BARBARIAN.code:
                        decoded_dungeoneer_team3.append(BARBARIAN.title)
                    if character == VETERAN_BODYGUARD.code:
                        decoded_dungeoneer_team3.append(VETERAN_BODYGUARD.title)
                    if character == MASTER_FENCER.code:
                        decoded_dungeoneer_team3.append(MASTER_FENCER.title)
                    if character == BERSERKER.code:
                        decoded_dungeoneer_team3.append(BERSERKER.title)
                    if character == ROGUE.code:
                        decoded_dungeoneer_team3.append(ROGUE.title)
                    if character == SURVIVALIST.code:
                        decoded_dungeoneer_team3.append(SURVIVALIST.title)
                    if character == BRAWLIST.code:
                        decoded_dungeoneer_team3.append(BRAWLIST.title)
                    if character == ACADEMIC_MAGE.code:
                        decoded_dungeoneer_team3.append(ACADEMIC_MAGE.title)
                    if character == DRUID.code:
                        decoded_dungeoneer_team3.append(DRUID.title)
                    if character == WARLOCK.code:
                        decoded_dungeoneer_team3.append(WARLOCK.title)
                    if character == BLOODMANCER.code:
                        decoded_dungeoneer_team3.append(BLOODMANCER.title)
                    if character == PALADIN.code:
                        decoded_dungeoneer_team3.append(PALADIN.title)
                    if character == CASTLE_RANGER.code:
                        decoded_dungeoneer_team3.append(CASTLE_RANGER.title)
                    if character == THUNDER_APPRENTICE.code:
                        decoded_dungeoneer_team3.append(THUNDER_APPRENTICE.title)
                    if character == POWER_CONDUIT.code:
                        decoded_dungeoneer_team3.append(POWER_CONDUIT.title)
                    if character == EARTH_SPEAKER.code:
                        decoded_dungeoneer_team3.append(EARTH_SPEAKER.title)
                    if character == PRIEST_OF_THE_DEVOTED.code:
                        decoded_dungeoneer_team3.append(PRIEST_OF_THE_DEVOTED.title)
                    if character == TIME_WALKER.code:
                        decoded_dungeoneer_team3.append(TIME_WALKER.title)
                    if character == CHILD_OF_MEDICINE.code:
                        decoded_dungeoneer_team3.append(CHILD_OF_MEDICINE.title)
                return decoded_dungeoneer_team3
        if len(decoded_dungeoneer_team3) < 5:
            while len(decoded_dungeoneer_team3) < 5:
                decoded_dungeoneer_team3.append("Empty")
            return decoded_dungeoneer_team3


class Team1SelectionPage(tk.Frame):
    def __init__(self, parent, controller):
        global update_pageTSP
        global returnButtonTSP, invis_label1, invis_label2
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.menu_button_font = tkfont.Font(family='Helvetica', size=18, weight="bold")
        self.title_label_font = tkfont.Font(family='Helvetica', size=30, weight="bold")
        self.small_label_font = tkfont.Font(family='Helvetica', size=12, weight="bold")
        title = tk.Label(self, text="Champion Camp", font=self.title_label_font)
        update_pageTSP = tk.Button(self, text="Begin Recruiting for Team 1", command=lambda: self.pitstop1(),
                                   font=controller.menu_button_font)
        returnButtonTSP = tk.Button(self, text="Cancel", command=lambda: controller.cancel_new_team1())
        invis_label1 = tk.Label(self)
        invis_label2 = tk.Label(self)
        update_pageTSP.grid(row=2, column=2, pady=50)
        title.grid(row=1, column=2)
        returnButtonTSP.grid(row=13, column=2)
        invis_label1.grid(row=1, column=1, rowspan=4, pady=50, ipadx=240, ipady=100)
        invis_label2.grid(row=1, column=2, pady=100)

    def pitstop1(self):
        global visual_team_label, temp_party
        user = ParentClass.get_user_encoded(self)
        team_line_1 = []
        team_line_1 = ParentClass.return_users_champion_team1(self, user)
        team_line_1 = team_line_1.replace(",", "")
        team_1_list_data = team_line_1.split()
        CTP = CreateTeamPage
        decoded_dungeoneer_team1CTP = CTP.team_1_decode(self, team_1_list_data)
        temp_party = decoded_dungeoneer_team1CTP
        visual_team_label = tk.Label(self, text=self.display_team1(temp_party))
        visual_team_label.grid(row=11, column=2)
        self.team_creation1()

    def team_creation1(self):
        global tank, dps, healer, tank_section_button, dps_section_button, healer_section_button, decoded_dungeoneer_team1CTP
        tank = False
        dps = False
        healer = False
        invis_label3 = tk.Label(self)
        invis_label4 = tk.Label(self)
        tank_section_button = tk.Button(self, text="Tanks", font=self.menu_button_font, width=26,
                                        command=self.view_tanks1)
        dps_section_button = tk.Button(self, text="Damage Dealers", font=self.menu_button_font, width=26,
                                       command=self.view_dps1)
        healer_section_button = tk.Button(self, text="Healers", font=self.menu_button_font, width=26,
                                          command=self.view_healer1)
        your_team_label = tk.Label(self, text=":Your Team:", font=self.small_label_font)
        confirm_changes_button = tk.Button(self, text="Confirm Changes", command=self.confirm_new_team1)
        tank_section_button.grid(row=2, column=1)
        dps_section_button.grid(row=2, column=2, padx=25)
        healer_section_button.grid(row=2, column=3)
        invis_label3.grid(row=2, column=0, padx=6)
        invis_label4.grid(row=9, column=2, pady=45)
        your_team_label.grid(row=10, column=2)
        confirm_changes_button.grid(row=12, column=2)
        invis_label1.grid_forget()
        invis_label2.grid_forget()
        update_pageTSP.grid_forget()

    def display_team1(self, temp_party):
        team_1_text = ""
        i = 0
        for character in temp_party:
            if i == 3:
                team_1_text += "\n"
            team_1_text += "["
            team_1_text += character
            team_1_text += "]"
            i += 1
        if i != 5:
            while i < 5:
                team_1_text += "["
                team_1_text += "Empty"
                team_1_text += "]"
                i += 1
        return team_1_text

    def view_tanks1(self):
        global MONK_label, MONK_button_add, MONK_button_details, BARBARIAN_label, BARBARIAN_button_add, \
            BARBARIAN_button_details, bodyguard_label, bodyguard_button_add, bodyguard_button_details, \
            fencer_label, fencer_button_add, fencer_button_details, invis_label3, invis_label4, tank, dps, healer
        if tank == True:
            return
        else:
            if dps == True:
                BERSERKER_label.destroy()
                BERSERKER_button_add.destroy()
                BERSERKER_button_details.destroy()
                ROGUE_label.destroy()
                ROGUE_button_add.destroy()
                ROGUE_button_details.destroy()
                SURVIVALIST_label.destroy()
                SURVIVALIST_button_add.destroy()
                SURVIVALIST_button_details.destroy()
                BRAWLIST_label.destroy()
                BRAWLIST_button_add.destroy()
                BRAWLIST_button_details.destroy()
                ACADEMIC_MAGE_label.destroy()
                ACADEMIC_MAGE_button_add.destroy()
                ACADEMIC_MAGE_button_details.destroy()
                jungle_DRUID_label.destroy()
                jungle_DRUID_button_add.destroy()
                jungle_DRUID_button_details.destroy()
                WARLOCK_label.destroy()
                WARLOCK_button_add.destroy()
                WARLOCK_button_details.destroy()
                BLOODMANCER_label.destroy()
                BLOODMANCER_button_add.destroy()
                BLOODMANCER_button_details.destroy()
                PALADIN_label.destroy()
                PALADIN_button_add.destroy()
                PALADIN_button_details.destroy()
                CASTLE_RANGER_label.destroy()
                CASTLE_RANGER_button_add.destroy()
                CASTLE_RANGER_button_details.destroy()
                THUNDER_APPRENTICE_label.destroy()
                THUNDER_APPRENTICE_button_add.destroy()
                THUNDER_APPRENTICE_button_details.destroy()
                POWER_CONDUIT_label.destroy()
                POWER_CONDUIT_button_add.destroy()
                POWER_CONDUIT_button_details.destroy()
                melee_label.destroy()
                magic_label.destroy()
                mix_label.destroy()
                dps = False
            else:
                dps = False
            if healer == True:
                EARTH_SPEAKER_label.destroy()
                EARTH_SPEAKER_button_add.destroy()
                EARTH_SPEAKER_button_details.destroy()
                PRIEST_OF_THE_DEVOTED_label.destroy()
                PRIEST_OF_THE_DEVOTED_button_add.destroy()
                PRIEST_OF_THE_DEVOTED_button_details.destroy()
                TIME_WALKER_label.destroy()
                TIME_WALKER_button_add.destroy()
                TIME_WALKER_button_details.destroy()
                CHILD_OF_MEDICINE_label.destroy()
                CHILD_OF_MEDICINE_button_add.destroy()
                CHILD_OF_MEDICINE_button_details.destroy()
                invis_label3.destroy()
                invis_label4.destroy()
                healer = False
            else:
                healer = False
            tank = True
            invis_label3 = tk.Label(self)
            invis_label4 = tk.Label(self)
            MONK_label = tk.Label(self, text=MONK.name, font=self.menu_button_font)
            MONK_button_add = tk.Button(self, text="Add to Team",
                                        command=lambda: self.check_temp_party1(MONK.title, "tank"))
            MONK_button_details = tk.Button(self, text="View Details")
            BARBARIAN_label = tk.Label(self, text=BARBARIAN.name, font=self.menu_button_font)
            BARBARIAN_button_add = tk.Button(self, text="Add to Team",
                                             command=lambda: self.check_temp_party1(BARBARIAN.title, "tank"))
            BARBARIAN_button_details = tk.Button(self, text="View Details")
            bodyguard_label = tk.Label(self, text=VETERAN_BODYGUARD.name, font=self.menu_button_font)
            bodyguard_button_add = tk.Button(self, text="Add to Team",
                                             command=lambda: self.check_temp_party1(VETERAN_BODYGUARD.title, "tank"))
            bodyguard_button_details = tk.Button(self, text="View Details")
            fencer_label = tk.Label(self, text=MASTER_FENCER.name, font=self.menu_button_font)
            fencer_button_add = tk.Button(self, text="Add to Team",
                                          command=lambda: self.check_temp_party1(MASTER_FENCER.title, "tank"))
            fencer_button_details = tk.Button(self, text="View Details")
            MONK_label.grid(row=4, column=1, sticky="e")
            MONK_button_add.grid(row=5, column=1, sticky="e", padx=75)
            MONK_button_details.grid(row=5, column=1, sticky="e")
            BARBARIAN_label.grid(row=4, column=3, sticky="w")
            BARBARIAN_button_add.grid(row=5, column=3, sticky="w")
            BARBARIAN_button_details.grid(row=5, column=3, sticky="w", padx=80)
            bodyguard_label.grid(row=7, column=1, sticky="e")
            bodyguard_button_add.grid(row=8, column=1, sticky="e", padx=75)
            bodyguard_button_details.grid(row=8, column=1, sticky="e")
            fencer_label.grid(row=7, column=3, sticky="w")
            fencer_button_add.grid(row=8, column=3, sticky="w")
            fencer_button_details.grid(row=8, column=3, sticky="w", padx=80)
            invis_label3.grid(row=3, column=1, columnspan=3, pady=50)
            invis_label4.grid(row=6, column=1, columnspan=3, pady=50)

    def view_dps1(self):
        global melee_label, magic_label, mix_label, BERSERKER_label, BERSERKER_button_add, BERSERKER_button_details, \
            ROGUE_label, ROGUE_button_add, ROGUE_button_details, SURVIVALIST_label, SURVIVALIST_button_add, SURVIVALIST_button_details, \
            BRAWLIST_label, BRAWLIST_button_add, BRAWLIST_button_details, ACADEMIC_MAGE_label, ACADEMIC_MAGE_button_add, ACADEMIC_MAGE_button_details, \
            jungle_DRUID_label, jungle_DRUID_button_add, jungle_DRUID_button_details, WARLOCK_label, WARLOCK_button_add, WARLOCK_button_details, \
            BLOODMANCER_label, BLOODMANCER_button_add, BLOODMANCER_button_details, PALADIN_label, PALADIN_button_add, PALADIN_button_details, \
            CASTLE_RANGER_label, CASTLE_RANGER_button_add, CASTLE_RANGER_button_details, THUNDER_APPRENTICE_label, THUNDER_APPRENTICE_button_add, THUNDER_APPRENTICE_button_details, \
            POWER_CONDUIT_label, POWER_CONDUIT_button_add, POWER_CONDUIT_button_details, tank, dps, healer
        if dps == True:
            return
        else:
            if tank == True:
                MONK_label.destroy()
                MONK_button_add.destroy()
                MONK_button_details.destroy()
                BARBARIAN_label.destroy()
                BARBARIAN_button_add.destroy()
                BARBARIAN_button_details.destroy()
                bodyguard_label.destroy()
                bodyguard_button_add.destroy()
                bodyguard_button_details.destroy()
                fencer_label.destroy()
                fencer_button_add.destroy()
                fencer_button_details.destroy()
                invis_label3.destroy()
                invis_label4.destroy()
                tank = False
            else:
                tank = False
            if healer == True:
                EARTH_SPEAKER_label.destroy()
                EARTH_SPEAKER_button_add.destroy()
                EARTH_SPEAKER_button_details.destroy()
                PRIEST_OF_THE_DEVOTED_label.destroy()
                PRIEST_OF_THE_DEVOTED_button_add.destroy()
                PRIEST_OF_THE_DEVOTED_button_details.destroy()
                TIME_WALKER_label.destroy()
                TIME_WALKER_button_add.destroy()
                TIME_WALKER_button_details.destroy()
                CHILD_OF_MEDICINE_label.destroy()
                CHILD_OF_MEDICINE_button_add.destroy()
                CHILD_OF_MEDICINE_button_details.destroy()
                invis_label3.destroy()
                invis_label4.destroy()
                healer = False
            else:
                healer = False
            dps = True
            melee_label = tk.Label(self, text=":Melee:", font=self.menu_button_font)
            magic_label = tk.Label(self, text=":Magic:", font=self.menu_button_font)
            mix_label = tk.Label(self, text=":Other:", font=self.menu_button_font)
            BERSERKER_label = tk.Label(self, text=BERSERKER.name)
            BERSERKER_button_add = tk.Button(self, text="Add to Team",
                                             command=lambda: self.check_temp_party1(BERSERKER.title, "melee"))
            BERSERKER_button_details = tk.Button(self, text="View Details")
            ROGUE_label = tk.Label(self, text=ROGUE.name)
            ROGUE_button_add = tk.Button(self, text="Add to Team",
                                         command=lambda: self.check_temp_party1(ROGUE.title, "melee"))
            ROGUE_button_details = tk.Button(self, text="View Details")
            SURVIVALIST_label = tk.Label(self, text=SURVIVALIST.name)
            SURVIVALIST_button_add = tk.Button(self, text="Add to Team",
                                               command=lambda: self.check_temp_party1(SURVIVALIST.title, "melee"))
            SURVIVALIST_button_details = tk.Button(self, text="View Details")
            BRAWLIST_label = tk.Label(self, text=BRAWLIST.name)
            BRAWLIST_button_add = tk.Button(self, text="Add to Team",
                                            command=lambda: self.check_temp_party1(BRAWLIST.title, "melee"))
            BRAWLIST_button_details = tk.Button(self, text="View Details")
            ACADEMIC_MAGE_label = tk.Label(self, text=ACADEMIC_MAGE.name)
            ACADEMIC_MAGE_button_add = tk.Button(self, text="Add to Team",
                                                 command=lambda: self.check_temp_party1(ACADEMIC_MAGE.title, "magic"))
            ACADEMIC_MAGE_button_details = tk.Button(self, text="View Details")
            jungle_DRUID_label = tk.Label(self, text=DRUID.name)
            jungle_DRUID_button_add = tk.Button(self, text="Add to Team",
                                                command=lambda: self.check_temp_party1(DRUID.title, "magic"))
            jungle_DRUID_button_details = tk.Button(self, text="View Details")
            WARLOCK_label = tk.Label(self, text=WARLOCK.name)
            WARLOCK_button_add = tk.Button(self, text="Add to Team",
                                           command=lambda: self.check_temp_party1(WARLOCK.title, "magic"))
            WARLOCK_button_details = tk.Button(self, text="View Details")
            BLOODMANCER_label = tk.Label(self, text=BLOODMANCER.name)
            BLOODMANCER_button_add = tk.Button(self, text="Add to Team",
                                               command=lambda: self.check_temp_party1(BLOODMANCER.title, "magic"))
            BLOODMANCER_button_details = tk.Button(self, text="View Details")
            PALADIN_label = tk.Label(self, text=PALADIN.name)
            PALADIN_button_add = tk.Button(self, text="Add to Team",
                                           command=lambda: self.check_temp_party1(PALADIN.title, "mixed"))
            PALADIN_button_details = tk.Button(self, text="View Details")
            CASTLE_RANGER_label = tk.Label(self, text=CASTLE_RANGER.name)
            CASTLE_RANGER_button_add = tk.Button(self, text="Add to Team",
                                                 command=lambda: self.check_temp_party1(CASTLE_RANGER.title, "mixed"))
            CASTLE_RANGER_button_details = tk.Button(self, text="View Details")
            THUNDER_APPRENTICE_label = tk.Label(self, text=THUNDER_APPRENTICE.name)
            THUNDER_APPRENTICE_button_add = tk.Button(self, text="Add to Team",
                                                      command=lambda: self.check_temp_party1(THUNDER_APPRENTICE.title,
                                                                                             "mixed"))
            THUNDER_APPRENTICE_button_details = tk.Button(self, text="View Details")
            POWER_CONDUIT_label = tk.Label(self, text=POWER_CONDUIT.name)
            POWER_CONDUIT_button_add = tk.Button(self, text="Add to Team",
                                                 command=lambda: self.check_temp_party1(POWER_CONDUIT.title, "mixed"))
            POWER_CONDUIT_button_details = tk.Button(self, text="View Details")
            melee_label.grid(row=3, column=1)
            magic_label.grid(row=3, column=2)
            mix_label.grid(row=3, column=3)
            BERSERKER_label.grid(row=5, column=1, sticky="w")
            BERSERKER_button_add.grid(row=6, column=1, sticky="w")
            BERSERKER_button_details.grid(row=6, column=1, sticky="w", padx=80)
            ROGUE_label.grid(row=8, column=1, sticky="w")
            ROGUE_button_add.grid(row=9, column=1, sticky="w")
            ROGUE_button_details.grid(row=9, column=1, sticky="w", padx=80)
            SURVIVALIST_label.grid(row=5, column=1, sticky="e", padx=10)
            SURVIVALIST_button_add.grid(row=6, column=1, sticky="e", padx=85)
            SURVIVALIST_button_details.grid(row=6, column=1, sticky="e", padx=10)
            BRAWLIST_label.grid(row=8, column=1, sticky="e", padx=10)
            BRAWLIST_button_add.grid(row=9, column=1, sticky="e", padx=85)
            BRAWLIST_button_details.grid(row=9, column=1, sticky="e", padx=10)
            ACADEMIC_MAGE_label.grid(row=5, column=2, sticky="w", padx=10)
            ACADEMIC_MAGE_button_add.grid(row=6, column=2, sticky="w", padx=10)
            ACADEMIC_MAGE_button_details.grid(row=6, column=2, sticky="w", padx=90)
            jungle_DRUID_label.grid(row=8, column=2, sticky="w", padx=10)
            jungle_DRUID_button_add.grid(row=9, column=2, sticky="w", padx=10)
            jungle_DRUID_button_details.grid(row=9, column=2, sticky="w", padx=90)
            WARLOCK_label.grid(row=5, column=2, sticky="e", padx=10)
            WARLOCK_button_add.grid(row=6, column=2, sticky="e", padx=85)
            WARLOCK_button_details.grid(row=6, column=2, sticky="e", padx=10)
            BLOODMANCER_label.grid(row=8, column=2, sticky="e", padx=10)
            BLOODMANCER_button_add.grid(row=9, column=2, sticky="e", padx=85)
            BLOODMANCER_button_details.grid(row=9, column=2, sticky="e", padx=10)
            PALADIN_label.grid(row=5, column=3, sticky="w", padx=10)
            PALADIN_button_add.grid(row=6, column=3, sticky="w", padx=10)
            PALADIN_button_details.grid(row=6, column=3, sticky="w", padx=90)
            CASTLE_RANGER_label.grid(row=8, column=3, sticky="w", padx=10)
            CASTLE_RANGER_button_add.grid(row=9, column=3, sticky="w", padx=10)
            CASTLE_RANGER_button_details.grid(row=9, column=3, sticky="w", padx=90)
            THUNDER_APPRENTICE_label.grid(row=5, column=3, sticky="e")
            THUNDER_APPRENTICE_button_add.grid(row=6, column=3, sticky="e", padx=75)
            THUNDER_APPRENTICE_button_details.grid(row=6, column=3, sticky="e")
            POWER_CONDUIT_label.grid(row=8, column=3, sticky="e")
            POWER_CONDUIT_button_add.grid(row=9, column=3, sticky="e", padx=75)
            POWER_CONDUIT_button_details.grid(row=9, column=3, sticky="e")

    def view_healer1(self):
        global EARTH_SPEAKER_label, EARTH_SPEAKER_button_add, EARTH_SPEAKER_button_details, PRIEST_OF_THE_DEVOTED_label, PRIEST_OF_THE_DEVOTED_button_add, \
            PRIEST_OF_THE_DEVOTED_button_details, TIME_WALKER_label, TIME_WALKER_button_add, TIME_WALKER_button_details, \
            CHILD_OF_MEDICINE_label, CHILD_OF_MEDICINE_button_add, CHILD_OF_MEDICINE_button_details, invis_label3, invis_label4, tank, dps, healer
        if healer == True:
            return
        else:
            invis_label3 = tk.Label(self)
            invis_label4 = tk.Label(self)
            if tank == True:
                MONK_label.destroy()
                MONK_button_add.destroy()
                MONK_button_details.destroy()
                BARBARIAN_label.destroy()
                BARBARIAN_button_add.destroy()
                BARBARIAN_button_details.destroy()
                bodyguard_label.destroy()
                bodyguard_button_add.destroy()
                bodyguard_button_details.destroy()
                fencer_label.destroy()
                fencer_button_add.destroy()
                fencer_button_details.destroy()
                invis_label3.destroy()
                invis_label4.destroy()
                tank = False
            else:
                tank = False
            if dps == True:
                BERSERKER_label.destroy()
                BERSERKER_button_add.destroy()
                BERSERKER_button_details.destroy()
                ROGUE_label.destroy()
                ROGUE_button_add.destroy()
                ROGUE_button_details.destroy()
                SURVIVALIST_label.destroy()
                SURVIVALIST_button_add.destroy()
                SURVIVALIST_button_details.destroy()
                BRAWLIST_label.destroy()
                BRAWLIST_button_add.destroy()
                BRAWLIST_button_details.destroy()
                ACADEMIC_MAGE_label.destroy()
                ACADEMIC_MAGE_button_add.destroy()
                ACADEMIC_MAGE_button_details.destroy()
                jungle_DRUID_label.destroy()
                jungle_DRUID_button_add.destroy()
                jungle_DRUID_button_details.destroy()
                WARLOCK_label.destroy()
                WARLOCK_button_add.destroy()
                WARLOCK_button_details.destroy()
                BLOODMANCER_label.destroy()
                BLOODMANCER_button_add.destroy()
                BLOODMANCER_button_details.destroy()
                PALADIN_label.destroy()
                PALADIN_button_add.destroy()
                PALADIN_button_details.destroy()
                CASTLE_RANGER_label.destroy()
                CASTLE_RANGER_button_add.destroy()
                CASTLE_RANGER_button_details.destroy()
                THUNDER_APPRENTICE_label.destroy()
                THUNDER_APPRENTICE_button_add.destroy()
                THUNDER_APPRENTICE_button_details.destroy()
                POWER_CONDUIT_label.destroy()
                POWER_CONDUIT_button_add.destroy()
                POWER_CONDUIT_button_details.destroy()
                melee_label.destroy()
                magic_label.destroy()
                mix_label.destroy()
                dps = False
            else:
                dps = False
            healer = True
            EARTH_SPEAKER_label = tk.Label(self, text=EARTH_SPEAKER.name, font=self.menu_button_font)
            EARTH_SPEAKER_button_add = tk.Button(self, text="Add to Team",
                                                 command=lambda: self.check_temp_party1(EARTH_SPEAKER.title, "healer"))
            EARTH_SPEAKER_button_details = tk.Button(self, text="View Details")
            PRIEST_OF_THE_DEVOTED_label = tk.Label(self, text=PRIEST_OF_THE_DEVOTED.name, font=self.menu_button_font)
            PRIEST_OF_THE_DEVOTED_button_add = tk.Button(self, text="Add to Team",
                                                         command=lambda: self.check_temp_party1(
                                                             PRIEST_OF_THE_DEVOTED.title, "healer"))
            PRIEST_OF_THE_DEVOTED_button_details = tk.Button(self, text="View Details")
            TIME_WALKER_label = tk.Label(self, text=TIME_WALKER.name, font=self.menu_button_font)
            TIME_WALKER_button_add = tk.Button(self, text="Add to Team",
                                               command=lambda: self.check_temp_party1(TIME_WALKER.title, "healer"))
            TIME_WALKER_button_details = tk.Button(self, text="View Details")
            CHILD_OF_MEDICINE_label = tk.Label(self, text=CHILD_OF_MEDICINE.name, font=self.menu_button_font)
            CHILD_OF_MEDICINE_button_add = tk.Button(self, text="Add to Team",
                                                     command=lambda: self.check_temp_party1(CHILD_OF_MEDICINE.title,
                                                                                            "healer"))
            CHILD_OF_MEDICINE_button_details = tk.Button(self, text="View Details")
            EARTH_SPEAKER_label.grid(row=4, column=1, sticky="e")
            EARTH_SPEAKER_button_add.grid(row=5, column=1, sticky="e", padx=75)
            EARTH_SPEAKER_button_details.grid(row=5, column=1, sticky="e")
            PRIEST_OF_THE_DEVOTED_label.grid(row=4, column=3, sticky="w")
            PRIEST_OF_THE_DEVOTED_button_add.grid(row=5, column=3, sticky="w")
            PRIEST_OF_THE_DEVOTED_button_details.grid(row=5, column=3, sticky="w", padx=80)
            TIME_WALKER_label.grid(row=7, column=1, sticky="e")
            TIME_WALKER_button_add.grid(row=8, column=1, sticky="e", padx=75)
            TIME_WALKER_button_details.grid(row=8, column=1, sticky="e")
            CHILD_OF_MEDICINE_label.grid(row=7, column=3, sticky="w")
            CHILD_OF_MEDICINE_button_add.grid(row=8, column=3, sticky="w")
            CHILD_OF_MEDICINE_button_details.grid(row=8, column=3, sticky="w", padx=80)
            invis_label3.grid(row=3, column=1, columnspan=3, pady=50)
            invis_label4.grid(row=6, column=1, columnspan=3, pady=50)

    def check_temp_party1(self, champion, type):
        global temp_party, yes_buttonCTP, no_buttonCTP, warning_label1CTP, warning_label2CTP, tank, dps, healer, visual_team_label
        tank_temp_party = []
        melee_temp_party = []
        magic_temp_party = []
        mixed_temp_party = []
        healer_temp_party = []
        if "Empty" in temp_party:
            temp_party.remove("Empty")
        if champion in temp_party:
            root = tk.Tk()
            warning_label = tk.Label(root, text="Sorry, but this character is already assigned in the party")
            ok_button = tk.Button(root, text="Ok", command=root.destroy)
            ok_button.grid(row=2, column=1)
            warning_label.grid(row=1, column=1)
            visual_team_label.destroy()
            visual_team_label = tk.Label(self, text=self.display_team1(temp_party))
            visual_team_label.grid(row=11, column=2)
        else:
            if len(temp_party) < 5:
                for character in temp_party:
                    if character == MONK.title:
                        tank_temp_party.append(character)
                    if character == BARBARIAN.title:
                        tank_temp_party.append(character)
                    if character == VETERAN_BODYGUARD.title:
                        tank_temp_party.append(character)
                    if character == MASTER_FENCER.title:
                        tank_temp_party.append(character)
                    if character == BERSERKER.title:
                        melee_temp_party.append(character)
                    if character == ROGUE.title:
                        melee_temp_party.append(character)
                    if character == SURVIVALIST.title:
                        melee_temp_party.append(character)
                    if character == BRAWLIST.title:
                        melee_temp_party.append(character)
                    if character == ACADEMIC_MAGE.title:
                        magic_temp_party.append(character)
                    if character == DRUID.title:
                        magic_temp_party.append(character)
                    if character == WARLOCK.title:
                        magic_temp_party.append(character)
                    if character == BLOODMANCER.title:
                        magic_temp_party.append(character)
                    if character == PALADIN.title:
                        mixed_temp_party.append(character)
                    if character == CASTLE_RANGER.title:
                        mixed_temp_party.append(character)
                    if character == THUNDER_APPRENTICE.title:
                        mixed_temp_party.append(character)
                    if character == POWER_CONDUIT.title:
                        mixed_temp_party.append(character)
                    if character == EARTH_SPEAKER.title:
                        healer_temp_party.append(character)
                    if character == PRIEST_OF_THE_DEVOTED.title:
                        healer_temp_party.append(character)
                    if character == TIME_WALKER.title:
                        healer_temp_party.append(character)
                    if character == CHILD_OF_MEDICINE.title:
                        healer_temp_party.append(character)
                    if character == "Empty":
                        p = 0
                if type == "tank":
                    tank_temp_party.append(champion)
                    tank_temp_party = sorted(tank_temp_party)
                elif type == "melee":
                    melee_temp_party.append(champion)
                    melee_temp_party = sorted(melee_temp_party)
                elif type == "magic":
                    magic_temp_party.append(champion)
                    magic_temp_party = sorted(magic_temp_party)
                elif type == "mixed":
                    mixed_temp_party.append(champion)
                    mixed_temp_party = sorted(mixed_temp_party)
                elif type == "healer":
                    healer_temp_party.append(champion)
                    healer_temp_party = sorted(healer_temp_party)
                temp_party = []
                if tank_temp_party == []:
                    p = 0
                else:
                    for character in tank_temp_party:
                        temp_party.append(character)
                if melee_temp_party == []:
                    p = 0
                else:
                    for character in melee_temp_party:
                        temp_party.append(character)
                if magic_temp_party == []:
                    p = 0
                else:
                    for character in magic_temp_party:
                        temp_party.append(character)
                if mixed_temp_party == []:
                    p = 0
                else:
                    for character in mixed_temp_party:
                        temp_party.append(character)
                if healer_temp_party == []:
                    p = 0
                else:
                    for character in healer_temp_party:
                        temp_party.append(character)
                visual_team_label.destroy()
                visual_team_label = tk.Label(self, text=self.display_team1(temp_party))
                visual_team_label.grid(row=11, column=2)
            elif len(temp_party) == 5:
                root = tk.Tk()
                warning_label1CTP = tk.Label(root, text="The party is currently full!")
                warning_label2CTP = tk.Label(root, text="Would you like to remove a current party member to make room?")
                yes_buttonCTP = tk.Button(root, text="Yes",
                                          command=lambda: self.adding_champions_tempParty1(root, champion))
                no_buttonCTP = tk.Button(root, text="No", command=lambda: root.destroy())
                warning_label1CTP.grid(row=1, column=1)
                warning_label2CTP.grid(row=2, column=1)
                yes_buttonCTP.grid(row=3, column=1, sticky="w", padx=140)
                no_buttonCTP.grid(row=3, column=1, sticky="e", padx=140)

    def adding_champions_tempParty1(self, root, champion):
        global champion1CTP, champion2CTP, champion3CTP, champion4CTP, champion5CTP, cancel_buttonCTP, window_labelCTP
        yes_buttonCTP.grid_forget()
        no_buttonCTP.grid_forget()
        warning_label1CTP.grid_forget()
        warning_label2CTP.grid_forget()
        window_labelCTP = tk.Label(root, text="Please choose which champion will be replaced for '{}'".format(champion))
        champion1CTP = tk.Button(root, text=temp_party[0],
                                 command=lambda: self.replace_champion1(root, champion, temp_party[0]))
        champion2CTP = tk.Button(root, text=temp_party[1],
                                 command=lambda: self.replace_champion1(root, champion, temp_party[1]))
        champion3CTP = tk.Button(root, text=temp_party[2],
                                 command=lambda: self.replace_champion1(root, champion, temp_party[2]))
        champion4CTP = tk.Button(root, text=temp_party[3],
                                 command=lambda: self.replace_champion1(root, champion, temp_party[3]))
        champion5CTP = tk.Button(root, text=temp_party[4],
                                 command=lambda: self.replace_champion1(root, champion, temp_party[4]))
        cancel_buttonCTP = tk.Button(root, text="Cancel", command=root.destroy, font="bold")
        window_labelCTP.grid(row=1, column=3)
        champion1CTP.grid(row=2, column=3)
        champion2CTP.grid(row=3, column=3)
        champion3CTP.grid(row=4, column=3)
        champion4CTP.grid(row=5, column=3)
        champion5CTP.grid(row=6, column=3)
        cancel_buttonCTP.grid(row=7, column=3)

    def replace_champion1(self, root, champion, selected):
        global temp_party, visual_team_label
        pos = temp_party.index(selected)
        temp_pos = temp_party[pos]
        temp_party[pos] = champion
        champion1CTP.grid_forget()
        champion2CTP.grid_forget()
        champion3CTP.grid_forget()
        champion4CTP.grid_forget()
        champion5CTP.grid_forget()
        cancel_buttonCTP.grid_forget()
        window_labelCTP.grid_forget()
        window_labelCTP2 = tk.Label(root, text="'{}' has been replaced by '{}'!".format(temp_pos, champion))
        ok_button = tk.Button(root, text="Ok", command=root.destroy)
        window_labelCTP2.grid(row=1, column=1)
        ok_button.grid(row=2, column=1)
        tank_temp_party = []
        melee_temp_party = []
        magic_temp_party = []
        mixed_temp_party = []
        healer_temp_party = []
        for character in temp_party:
            if character == MONK.title:
                tank_temp_party.append(character)
            if character == BARBARIAN.title:
                tank_temp_party.append(character)
            if character == VETERAN_BODYGUARD.title:
                tank_temp_party.append(character)
            if character == MASTER_FENCER.title:
                tank_temp_party.append(character)
            if character == BERSERKER.title:
                melee_temp_party.append(character)
            if character == ROGUE.title:
                melee_temp_party.append(character)
            if character == SURVIVALIST.title:
                melee_temp_party.append(character)
            if character == BRAWLIST.title:
                melee_temp_party.append(character)
            if character == ACADEMIC_MAGE.title:
                magic_temp_party.append(character)
            if character == DRUID.title:
                magic_temp_party.append(character)
            if character == WARLOCK.title:
                magic_temp_party.append(character)
            if character == BLOODMANCER.title:
                magic_temp_party.append(character)
            if character == PALADIN.title:
                mixed_temp_party.append(character)
            if character == CASTLE_RANGER.title:
                mixed_temp_party.append(character)
            if character == THUNDER_APPRENTICE.title:
                mixed_temp_party.append(character)
            if character == POWER_CONDUIT.title:
                mixed_temp_party.append(character)
            if character == EARTH_SPEAKER.title:
                healer_temp_party.append(character)
            if character == PRIEST_OF_THE_DEVOTED.title:
                healer_temp_party.append(character)
            if character == TIME_WALKER.title:
                healer_temp_party.append(character)
            if character == CHILD_OF_MEDICINE.title:
                healer_temp_party.append(character)
        temp_party = []
        if tank_temp_party == []:
            p = 0
        else:
            tank_temp_party = sorted(tank_temp_party)
            for character in tank_temp_party:
                temp_party.append(character)
        if melee_temp_party == []:
            p = 0
        else:
            melee_temp_party = sorted(melee_temp_party)
            for character in melee_temp_party:
                temp_party.append(character)
        if magic_temp_party == []:
            p = 0
        else:
            magic_temp_party = sorted(magic_temp_party)
            for character in magic_temp_party:
                temp_party.append(character)
        if mixed_temp_party == []:
            p = 0
        else:
            mixed_temp_party = sorted(mixed_temp_party)
            for character in mixed_temp_party:
                temp_party.append(character)
        if healer_temp_party == []:
            p = 0
        else:
            healer_temp_party = sorted(healer_temp_party)
            for character in healer_temp_party:
                temp_party.append(character)
        visual_team_label.destroy()
        visual_team_label = tk.Label(self, text=self.display_team1(temp_party))
        visual_team_label.grid(row=11, column=2)

    def confirm_new_team1(self):
        root = tk.Tk()
        confirmation_label = tk.Label(root, text="Are you sure you want save this group?")
        yes_buttonCNT = tk.Button(root, text="Yes", command=lambda: ParentClass.finalise_new_team1(self, root))
        no_buttonCNT = tk.Button(root, text="No", command=lambda: root.destroy())
        confirmation_label.grid(row=2, column=1)
        yes_buttonCNT.grid(row=3, column=1, sticky="w", padx=70)
        no_buttonCNT.grid(row=3, column=1, sticky="e", padx=70)

    def save_new_team1(self, root):
        i = -1
        file = open("C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_championTeam_1.txt".format(computer_username),
                    "r")
        file_allLines = file.readlines()
        user = ParentClass.get_user_encoded(self)
        user = str(user)
        for line in file_allLines:
            i += 1
            if user in line:
                coded_temp_party = self.code_party()
                new_line = "{}, {}\n".format(user, coded_temp_party)
                file_allLines[i] = new_line
                file_write = open(
                    "C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_championTeam_1.txt".format(computer_username),
                    "w")
                file_write.writelines(file_allLines)
                file.close()
                file_write.close()
                root.destroy()
                break

    def code_party(self):
        coded_temp_party = ""
        i = 0
        for character in temp_party:
            if character == MONK.title:
                coded_temp_party += MONK.code
            if character == BARBARIAN.title:
                coded_temp_party += BARBARIAN.code
            if character == VETERAN_BODYGUARD.title:
                coded_temp_party += VETERAN_BODYGUARD.code
            if character == MASTER_FENCER.title:
                coded_temp_party += MASTER_FENCER.code
            if character == BERSERKER.title:
                coded_temp_party += BERSERKER.code
            if character == ROGUE.title:
                coded_temp_party += ROGUE.code
            if character == SURVIVALIST.title:
                coded_temp_party += SURVIVALIST.code
            if character == BRAWLIST.title:
                coded_temp_party += BRAWLIST.code
            if character == ACADEMIC_MAGE.title:
                coded_temp_party += ACADEMIC_MAGE.code
            if character == DRUID.title:
                coded_temp_party += DRUID.code
            if character == WARLOCK.title:
                coded_temp_party += WARLOCK.code
            if character == BLOODMANCER.title:
                coded_temp_party += BLOODMANCER.code
            if character == PALADIN.title:
                coded_temp_party += PALADIN.code
            if character == CASTLE_RANGER.title:
                coded_temp_party += CASTLE_RANGER.code
            if character == THUNDER_APPRENTICE.title:
                coded_temp_party += THUNDER_APPRENTICE.code
            if character == POWER_CONDUIT.title:
                coded_temp_party += POWER_CONDUIT.code
            if character == EARTH_SPEAKER.title:
                coded_temp_party += EARTH_SPEAKER.code
            if character == PRIEST_OF_THE_DEVOTED.title:
                coded_temp_party += PRIEST_OF_THE_DEVOTED.code
            if character == TIME_WALKER.title:
                coded_temp_party += TIME_WALKER.code
            if character == CHILD_OF_MEDICINE.title:
                coded_temp_party += CHILD_OF_MEDICINE.code
            if character == "Empty":
                break
            i += 1
            if i <= 4:
                coded_temp_party += ", "
        return coded_temp_party

    def clear_temp_party1(self):
        global temp_party
        temp_party = []


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
    app = ParentClass()
    app.mainloop()
