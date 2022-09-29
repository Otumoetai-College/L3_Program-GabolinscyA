import os
import random
import math
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
        current_team = open("C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_dungeon_team.txt".format(computer_username), "w")
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
        play_button = tk.Button(self, text="Enter the Dungeon", font=controller.menu_button_font, command=self.team_check)
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
        yesButton = tk.Button(root, text="Yes", command=lambda: ParentClass.set_dungeon_team(self, decoded_dungeoneer_team1, root))
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
        easymode_button = tk.Button(self, text="Easy Dungeon", font=controller.menu_button_font, command=lambda:self.set_new_dungeon_difficulty("easy"))
        normalmode_label = tk.Label(self, text="The Deep Dark", font=smallish_text_font)
        normalmode_button = tk.Button(self, text="Normal Dungeon", font=controller.menu_button_font, command=lambda:self.set_new_dungeon_difficulty("normal"))
        hardmode_label = tk.Label(self, text="The Abyss", font=smallish_text_font)
        hardmode_button = tk.Button(self, text="Hard Dungeon", font=controller.menu_button_font, command=lambda:self.set_new_dungeon_difficulty("hard"))
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
            dungeon_difficulty_file = open("C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_dungeon_difficulty.txt".format(computer_username), "w")
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
        HEALTH_MODIFIER = 5
        ATTACKPOWER_MODIFIER = 10
        EASY_DUNGEON_MODIFIERS = []
        EASY_DUNGEON_MODIFIERS.append(HEALTH_MODIFIER)
        EASY_DUNGEON_MODIFIERS.append(ATTACKPOWER_MODIFIER)
        return EASY_DUNGEON_MODIFIERS
    def get_medium_dungeon_modifiers(self):
        HEALTH_MODIFIER = 10
        ATTACKPOWER_MODIFIER = 15
        MEDIUM_DUNGEON_MODIFIERS = []
        MEDIUM_DUNGEON_MODIFIERS.append(HEALTH_MODIFIER)
        MEDIUM_DUNGEON_MODIFIERS.append(ATTACKPOWER_MODIFIER)
        return MEDIUM_DUNGEON_MODIFIERS
    def get_hard_dungeon_modifiers(self):
        HEALTH_MODIFIER = 20
        ATTACKPOWER_MODIFIER = 20
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
        beginning_label = tk.Label(self, text="You cannot save your progress\n You must complete the run in one go", font=self.medium_text_font_bold)
        start_ok_button.grid(row=3, column=1)
        remember_label.grid(row=1, column=1)
        beginning_label.grid(row=2, column=1)
        start_invis_label1.grid(row=0, column=0, padx=20, pady=20)
        beginning_check_interger = 1
    def begin_dungeon_run(self):
        global beginning_check_interger, dungeon_name_label, delve_button, BDRinvisLabel1, BDR_check_interger, roomLevel, floorLevel, dungeon_settings, dungeon_name_text
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
        delve_button = tk.Button(self, text="Start Floor 1", font=self.medium_text_font_bold, command=self.set_dungeon_properties)
        BDRinvisLabel1 = tk.Label(self)
        dungeon_name_label.grid(row=1, column=1)
        BDRinvisLabel1.grid(row=2, column=0, padx=155, pady=120)
        delve_button.grid(row=3, column=1)
        BDR_check_interger = 1
        roomLevel = 1
        floorLevel = 1

    def set_dungeon_properties(self):
        global MODIFERS
        if dungeon_settings == "easy":
            MODIFERS = DungeonManagement.get_easy_dungeon_modifiers(self)
        elif dungeon_settings == "normal":
            MODIFERS = DungeonManagement.get_medium_dungeon_modifiers(self)
        elif dungeon_settings == "hard":
            MODIFERS = DungeonManagement.get_hard_dungeon_modifiers(self)
        self.get_individual_champions()
        self.set_champions_stats()
        self.set_up_beginning_champion_stats()
        self.DungeonFloorProgress()

    def get_individual_champions(self):
        global CHAMPION_LIST
        current_team_file = open("C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_dungeon_team.txt".format(computer_username), "r")
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
        aiEnemyNA = "out"
        if AI_SPAWNED == 1:
            ai1_hp = AI_GROUP_HP + MODIFERS[0] * roomLevel
            ai2_hp = aiEnemyNA
            ai3_hp = aiEnemyNA
            ai4_hp = aiEnemyNA
            ai5_hp = aiEnemyNA
        if AI_SPAWNED == 2:
            ai1_hp = AI_GROUP_HP + MODIFERS[0] * roomLevel
            ai2_hp = AI_GROUP_HP + MODIFERS[0] * roomLevel
            ai3_hp = aiEnemyNA
            ai4_hp = aiEnemyNA
            ai5_hp = aiEnemyNA
        if AI_SPAWNED == 3:
            ai1_hp = AI_GROUP_HP + MODIFERS[0] * roomLevel
            ai2_hp = AI_GROUP_HP + MODIFERS[0] * roomLevel
            ai3_hp = AI_GROUP_HP + MODIFERS[0] * roomLevel
            ai4_hp = aiEnemyNA
            ai5_hp = aiEnemyNA
        if AI_SPAWNED == 4:
            ai1_hp = AI_GROUP_HP + MODIFERS[0] * roomLevel
            ai2_hp = AI_GROUP_HP + MODIFERS[0] * roomLevel
            ai3_hp = AI_GROUP_HP + MODIFERS[0] * roomLevel
            ai4_hp = AI_GROUP_HP + MODIFERS[0] * roomLevel
            ai5_hp = aiEnemyNA
        if AI_SPAWNED == 5:
            ai1_hp = AI_GROUP_HP + MODIFERS[0] * roomLevel
            ai2_hp = AI_GROUP_HP + MODIFERS[0] * roomLevel
            ai3_hp = AI_GROUP_HP + MODIFERS[0] * roomLevel
            ai4_hp = AI_GROUP_HP + MODIFERS[0] * roomLevel
            ai5_hp = AI_GROUP_HP + MODIFERS[0] * roomLevel
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
        global club_slam_requirements, violent_thrash_requirements, twilight_beam_requirements, spear_thrust_requirements, \
        bite_requirements
        if AI_NAME == "Grothak the Destroyer":
            club_slam_requirements = [0, 0, 0]
        if AI_NAME == "Wormpulp Brothers":
            violent_thrash_requirements = [0, 0, 0]
        if AI_NAME == "Siren Triplets":
            twilight_beam_requirements = [25, 0, 0]
        if AI_NAME == "Venomskin Troggies":
            spear_thrust_requirements = [0, 0, 0]
        if AI_NAME == "Giant Locust Swarm":
            bite_requirements = [0, 0, 0]
    def set_up_beginning_champion_stats(self):
        global champion1_hp, champion1_ap, champion1_rp, champion1_rpName, champion2_hp, champion2_ap, champion2_rp, champion2_rpName, \
        champion3_hp, champion3_ap, champion3_rp, champion3_rpName, champion4_hp, champion4_ap, champion4_rp, champion4_rpName, \
        champion5_hp, champion5_ap, champion5_rp, champion5_rpName, champion1_small_external_buffs, champion1_big_external_buffs, \
        champion2_small_external_buffs, champion2_big_external_buffs, champion3_small_external_buffs, champion3_big_external_buffs, \
        champion4_small_external_buffs, champion4_big_external_buffs, champion5_small_external_buffs, champion5_big_external_buffs
        champion1_hp = CHAMPION_1_HP
        champion1_ap = CHAMPION_1_AP
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
        #Monk Abilities:
        palm_strike_requirements = [0, 0, 0, 20]
        leg_sweep_requirements = [30, 0, 2, 0]
        harmonize_requirements = [50, 0, 0, 0]
        pressure_points_requirements = [30, 0, 5, 0]
        #Barbarian Abiltities:
        bloodthirst_requirements = [0, 0, 0, 30]
        pulverize_requirements = [20, 0, 0, 0]
        challenging_shout_requirements = [40, 0, 2, 20]
        impactful_boast_requirements = [20, 0, 0, 0]
        #Veteran Bodyguard Abilities:
        shield_bash_requirements = [0, 0, 0, 0]
        trainwreck_requirements = [0, 0, 1, 0]
        fortification_requirements = [0, 0, 2, 0]
        block_requirements = [0, 0, 0, 0]
        #Master Fencer Abilities
        pierce_requirements = [0, 0, 0, 0]
        disruptive_slash_requirements = [0, 0, 2, 0]
        parry_requirements = [0, 0, 2, 0]
        elusive_measures_requirements = [0, 0, 1, 0]
        global raging_blow_requirements, rampage_requirements, enrage_requirements, reckless_flurry_requirements
        #Berserker Abilities
        raging_blow_requirements = [0, 0, 0, 20]
        rampage_requirements = [80, 0, 0, 0]
        enrage_requirements = [0, 0, 0, 30]
        reckless_flurry_requirements = [30, 0, 2, 0]

    def DungeonFloorProgress(self):
        global BDR_check_interger, dungeon_floor
        if BDR_check_interger == 1:
            dungeon_name_label.destroy()
            delve_button.destroy()
            BDRinvisLabel1.destroy()
            BDR_check_interger = 0
        dungeon_floor = ttk.LabelFrame(self)
        dungeon_floor.grid(row=0, column=0)
        champion_labelframe = ttk.LabelFrame(dungeon_floor)
        champion_labelframe.grid(row=4, column=3)
        current_dungeon_label = tk.Label(dungeon_floor, text=dungeon_name_text, font=self.small_text_font)
        current_floor_label = tk.Label(dungeon_floor, text="Floor {} : Room {}".format(floorLevel, roomLevel), font=self.medium_text_font_bold)
        teams_current_condition_label = tk.Label(dungeon_floor, text=":Your Team's Current Condition:", font=self.small_text_font)
        champion1_label = tk.Label(champion_labelframe, text=CHAMPION_LIST[0], font=self.small_text_font, width=15)
        champion2_label = tk.Label(champion_labelframe, text=CHAMPION_LIST[1], font=self.small_text_font, width=15)
        champion3_label = tk.Label(champion_labelframe, text=CHAMPION_LIST[2], font=self.small_text_font, width=15)
        champion4_label = tk.Label(champion_labelframe, text=CHAMPION_LIST[3], font=self.small_text_font, width=15)
        champion5_label = tk.Label(champion_labelframe, text=CHAMPION_LIST[4], font=self.small_text_font, width=15)
        champion1_status = tk.Label(champion_labelframe, text=self.champion_floorMenu_status_text(1), width=20)
        champion2_status = tk.Label(champion_labelframe, text=self.champion_floorMenu_status_text(2), width=20)
        champion3_status = tk.Label(champion_labelframe, text=self.champion_floorMenu_status_text(3), width=20)
        champion4_status = tk.Label(champion_labelframe, text=self.champion_floorMenu_status_text(4), width=20)
        champion5_status = tk.Label(champion_labelframe, text=self.champion_floorMenu_status_text(5), width=20)
        proceed_button = tk.Button(champion_labelframe, text="Proceed", font=self.menu_button_font, command=self.combat_monster_setup)
        CLFinvis_label = tk.Label(champion_labelframe)
        teams_current_condition_label.grid(row=3, column=3)
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
        current_dungeon_label.grid(row=0, column=3)
        current_floor_label.grid(row=1, column=3)

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
                    status_text = "*DEAD*\nHealth Points: {}/{}\n{}: {}/{}".format(champion1_hp, CHAMPION_1_HP,CHAMPION_1_RPNAME, champion1_rp, CHAMPION_1_RP)
                    return status_text
                else:
                    status_text = "\nHealth Points: {}/{}\n{}: {}/{}".format(champion1_hp, CHAMPION_1_HP, CHAMPION_1_RPNAME, champion1_rp, CHAMPION_1_RP)
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
                    status_text = "*DEAD*\nHealth Points: {}/{}\n{}: {}/{}".format(champion2_hp, CHAMPION_2_HP,CHAMPION_2_RPNAME, champion2_rp, CHAMPION_2_RP)
                    return status_text
                else:
                    status_text = "\nHealth Points: {}/{}\n{}: {}/{}".format(champion2_hp, CHAMPION_2_HP, CHAMPION_2_RPNAME, champion2_rp, CHAMPION_2_RP)
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
                    status_text = "*DEAD*\nHealth Points: {}/{}\n{}: {}/{}".format(champion3_hp, CHAMPION_3_HP,CHAMPION_3_RPNAME, champion3_rp, CHAMPION_3_RP)
                    return status_text
                else:
                    status_text = "\nHealth Points: {}/{}\n{}: {}/{}".format(champion3_hp, CHAMPION_3_HP, CHAMPION_3_RPNAME, champion3_rp, CHAMPION_3_RP)
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
                    status_text = "*DEAD*\nHealth Points: {}/{}\n{}: {}/{}".format(champion4_hp, CHAMPION_4_HP,CHAMPION_4_RPNAME, champion4_rp, CHAMPION_4_RP)
                    return status_text
                else:
                    status_text = "\nHealth Points: {}/{}\n{}: {}/{}".format(champion4_hp, CHAMPION_4_HP, CHAMPION_4_RPNAME, champion4_rp, CHAMPION_4_RP)
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
                    status_text = "*DEAD*\nHealth Points: {}/{}\n{}: {}/{}".format(champion5_hp, CHAMPION_5_HP,CHAMPION_5_RPNAME, champion5_rp, CHAMPION_5_RP)
                    return status_text
                else:
                    status_text = "\nHealth Points: {}/{}\n{}: {}/{}".format(champion5_hp, CHAMPION_5_HP, CHAMPION_5_RPNAME, champion5_rp, CHAMPION_5_RP)
                    return status_text

    def combat_monster_setup(self):
        global new_round, from_attack_button, from_special_button
        new_round = 1
        from_attack_button = 0
        from_special_button = 0
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
            #Club_Slam
            club_slam_basenumber = [1, 1.3, 1.5]
            random.shuffle(club_slam_basenumber)
            club_slam_damage = (club_slam_basenumber[0] * AI_ATTACKPOWER + (MODIFERS[1] * floorLevel))
            if club_slam_requirements[1] == 0:
                if club_slam_requirements[0] <= AI_RESOURCE:
                    attack.append("Club Slam")
            random.shuffle(attack)
            if attack[0] == "Club Slam":
                attack = ["Club Slam", math.ceil(club_slam_damage), "1T"]
        if AI_NAME == "Wormpulp Brothers":
            #Violent Thrash
            violent_thrash_basenumber = [1,1.1,1.2]
            random.shuffle(violent_thrash_basenumber)
            violent_thrash_damage = (violent_thrash_basenumber[0] * AI_ATTACKPOWER + (MODIFERS[1] * floorLevel))
            if violent_thrash_requirements[1] == 0:
                if violent_thrash_requirements[0] <= AI_RESOURCE:
                    attack.append("Violent Thrash")
            random.shuffle(attack)
            if attack[0] == "Violent Thrash":
                attack = ["Violent Thrash", math.ceil(violent_thrash_damage), "2T"]
        if AI_NAME == "Siren Triplets":
            #Twilight Beam
            twilight_beam_basenumber = [1.2, 1.4, 1.6]
            random.shuffle(twilight_beam_basenumber)
            twilight_beam_damage = (twilight_beam_basenumber[0] * AI_ATTACKPOWER + (MODIFERS[1] * floorLevel))
            if twilight_beam_requirements[1] == 0:
                if twilight_beam_requirements[0] <= AI_RESOURCE:
                    attack.append("Twilight Beam")
            random.shuffle(attack)
            if attack[0] == "Twilight Beam":
                attack = ["Twilight Beam", math.ceil(twilight_beam_damage), "1T"]
        if AI_NAME == "Venomskin Troggies":
            #Spear Thrust
            spear_thrust_basenumber = [1.2, 1.4, 1.6]
            random.shuffle(spear_thrust_basenumber)
            spear_thrust_damage = (spear_thrust_basenumber[0] * AI_ATTACKPOWER + (MODIFERS[1] * floorLevel))
            if spear_thrust_requirements[1] == 0:
                if spear_thrust_requirements[0] <= AI_RESOURCE:
                    attack.append("Spear Thrust")
            random.shuffle(attack)
            if attack[0] == "Spear Thrust":
                attack = ["Spear Thrust", math.ceil(spear_thrust_damage), "1T"]
        if AI_NAME == "Giant Locust Swarm":
            #Bite
            bite_basenumber = [1.2, 1.4, 1.6]
            random.shuffle(bite_basenumber)
            bite_damage = (bite_basenumber[0] * AI_ATTACKPOWER + (MODIFERS[1] * floorLevel))
            if bite_requirements[1] == 0:
                if bite_requirements[0] <= AI_RESOURCE:
                    attack.append("Bite")
            random.shuffle(attack)
            if attack[0] == "Bite":
                attack = ["Bite", math.ceil(bite_damage), "1T"]
        return attack
    def combat_setup(self):
        global combat_labelframe, combat_UI_labelframe
        dungeon_floor.destroy()
        combat_labelframe = ttk.LabelFrame(self)
        combat_labelframe.grid(row=0, column=0, sticky="NSEW")
        combat_UI_labelframe = ttk.LabelFrame(self)
        combat_UI_labelframe.grid(row=1, column=0, sticky="NSEW")
        current_dungeon_label = tk.Label(combat_labelframe, text=dungeon_name_text, font=self.small_text_font)
        CLFinvis_label1 = tk.Label(combat_labelframe, width=72)
        CLFinvis_label2 = tk.Label(combat_labelframe, width=72)
        champion1_combatFrame_name = tk.LabelFrame(combat_UI_labelframe, text=self.champion_combat_name(1), font=self.title_font)
        champion1_combatFrame_stats = tk.Label(combat_UI_labelframe, text=self.champion_combat_status_text(1))
        champion1_combatFrame_statusEffects = tk.Label(combat_UI_labelframe, text="Status Effects")
        champion2_combatFrame_name = tk.LabelFrame(combat_UI_labelframe, text=self.champion_combat_name(2),
                                                   font=self.small_text_font)
        champion2_combatFrame_stats = tk.Label(combat_UI_labelframe, text=self.champion_combat_status_text(2))
        champion2_combatFrame_statusEffects = tk.Label(combat_UI_labelframe, text="Status Effects")
        champion3_combatFrame_name = tk.LabelFrame(combat_UI_labelframe, text=self.champion_combat_name(3),
                                                   font=self.small_text_font)
        champion3_combatFrame_stats = tk.Label(combat_UI_labelframe, text=self.champion_combat_status_text(3))
        champion3_combatFrame_statusEffects = tk.Label(combat_UI_labelframe, text="Status Effects")
        champion4_combatFrame_name = tk.LabelFrame(combat_UI_labelframe, text=self.champion_combat_name(4),
        font = self.small_text_font)
        champion4_combatFrame_stats = tk.Label(combat_UI_labelframe, text=self.champion_combat_status_text(4))
        champion4_combatFrame_statusEffects = tk.Label(combat_UI_labelframe, text="Status Effects")
        champion5_combatFrame_name = tk.LabelFrame(combat_UI_labelframe, text=self.champion_combat_name(5),
        font = self.small_text_font)
        champion5_combatFrame_stats = tk.Label(combat_UI_labelframe, text=self.champion_combat_status_text(5))
        champion5_combatFrame_statusEffects = tk.Label(combat_UI_labelframe, text="Status Effects")
        champion_CLF_dottedLine_label1 = tk.Label(combat_UI_labelframe, text="----------------")
        champion_CLF_dottedLine_label2 = tk.Label(combat_UI_labelframe, text="----------------")
        champion_CLF_dottedLine_label3 = tk.Label(combat_UI_labelframe, text="----------------")
        champion_CLF_dottedLine_label4 = tk.Label(combat_UI_labelframe, text="----------------")
        champion_CLF_dottedLine_label5 = tk.Label(combat_UI_labelframe, text="----------------")
        champion_CLF_dottedLine_label1.grid(row=0, column=1, sticky="w")
        champion_CLF_dottedLine_label2.grid(row=3, column=1, sticky="w")
        champion_CLF_dottedLine_label3.grid(row=6, column=1, sticky="w")
        champion_CLF_dottedLine_label4.grid(row=9, column=1, sticky="w")
        champion_CLF_dottedLine_label5.grid(row=12, column=1, sticky="w")
        current_dungeon_label.grid(row=0, column=1)
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
        champion_interaction_dottedLine1 = tk.Label(combat_UI_labelframe, text="====================================================")
        champion_interaction_dottedLine2 = tk.Label(combat_UI_labelframe, text="====================================================")
        champion_interaction_dottedLine3 = tk.Label(combat_UI_labelframe, text="====================================================")
        champion_interaction_dottedLine1.grid(row=16, column=1, sticky="WE")
        champion_interaction_dottedLine2.grid(row=16, column=2, sticky="WE")
        champion_interaction_dottedLine3.grid(row=16, column=3, sticky="WE")
        CLFinvis_label1.grid(row=0, column=0)
        CLFinvis_label2.grid(row=0, column=2)
        if AI_SPAWNED == 1:
            ai1_combatFrame_name = tk.Label(combat_UI_labelframe, text=self.ai_combat_name(1))
            ai1_combatFrame_stats = tk.Label(combat_UI_labelframe, text=self.ai_combat_status_text(1))
            ai1_combatFrame_statusEffects = tk.Label(combat_UI_labelframe, text="status effects")
            AI_CLF_dottedLine_label1 = tk.Label(combat_UI_labelframe, text="----------------")
            AI_CLF_dottedLine_label2 = tk.Label(combat_UI_labelframe, text="----------------")
            ai1_intented_attack_label = tk.Label(combat_UI_labelframe, text=ai1_attack_intention)
            ai1_intented_attack_label.grid(row=7, column=2, sticky="e")
            ai1_combatFrame_name.grid(row=7, column=3, sticky="e")
            ai1_combatFrame_stats.grid(row=8, column=3, sticky="e")
            ai1_combatFrame_statusEffects.grid(row=8, column=3)
            AI_CLF_dottedLine_label1.grid(row=6, column=3, sticky="e")
            AI_CLF_dottedLine_label2.grid(row=9, column=3, sticky="e")
        elif AI_SPAWNED == 2:
            ai1_combatFrame_name = tk.Label(combat_UI_labelframe, text=self.ai_combat_name(1))
            ai1_combatFrame_stats = tk.Label(combat_UI_labelframe, text=self.ai_combat_status_text(1))
            ai1_combatFrame_statusEffects = tk.Label(combat_UI_labelframe, text="status effects")
            ai1_combatFrame_name.grid(row=4, column=3, sticky="e")
            ai1_combatFrame_stats.grid(row=5, column=3, sticky="e")
            ai1_combatFrame_statusEffects.grid(row=5, column=3)
            ai2_combatFrame_name = tk.Label(combat_UI_labelframe, text=self.ai_combat_name(2))
            ai2_combatFrame_stats = tk.Label(combat_UI_labelframe, text=self.ai_combat_status_text(2))
            ai2_combatFrame_statusEffects = tk.Label(combat_UI_labelframe, text="status effects")
            ai2_combatFrame_name.grid(row=7, column=3, sticky="e")
            ai2_combatFrame_stats.grid(row=8, column=3, sticky="e")
            ai2_combatFrame_statusEffects.grid(row=8, column=3)
            AI_CLF_dottedLine_label1 = tk.Label(combat_UI_labelframe, text="----------------")
            AI_CLF_dottedLine_label2 = tk.Label(combat_UI_labelframe, text="----------------")
            AI_CLF_dottedLine_label3 = tk.Label(combat_UI_labelframe, text="----------------")
            ai1_intented_attack_label = tk.Label(combat_UI_labelframe, text=ai1_attack_intention)
            ai2_intented_attack_label = tk.Label(combat_UI_labelframe, text=ai2_attack_intention)
            ai1_intented_attack_label.grid(row=4, column=2, sticky="e")
            ai2_intented_attack_label.grid(row=7, column=2, sticky="e")
            AI_CLF_dottedLine_label1.grid(row=3, column=3, sticky="e")
            AI_CLF_dottedLine_label2.grid(row=6, column=3, sticky="e")
            AI_CLF_dottedLine_label3.grid(row=9, column=3, sticky="e")
        elif AI_SPAWNED == 3:
            ai1_combatFrame_name = tk.Label(combat_UI_labelframe, text=self.ai_combat_name(1))
            ai1_combatFrame_stats = tk.Label(combat_UI_labelframe, text=self.ai_combat_status_text(1))
            ai1_combatFrame_statusEffects = tk.Label(combat_UI_labelframe, text="status effects")
            ai1_combatFrame_name.grid(row=4, column=3, sticky="e")
            ai1_combatFrame_stats.grid(row=5, column=3, sticky="e")
            ai1_combatFrame_statusEffects.grid(row=5, column=3)
            ai2_combatFrame_name = tk.Label(combat_UI_labelframe, text=self.ai_combat_name(2))
            ai2_combatFrame_stats = tk.Label(combat_UI_labelframe, text=self.ai_combat_status_text(2))
            ai2_combatFrame_statusEffects = tk.Label(combat_UI_labelframe, text="status effects")
            ai2_combatFrame_name.grid(row=7, column=3, sticky="e")
            ai2_combatFrame_stats.grid(row=8, column=3, sticky="e")
            ai2_combatFrame_statusEffects.grid(row=8, column=3)
            ai3_combatFrame_name = tk.Label(combat_UI_labelframe, text=self.ai_combat_name(3))
            ai3_combatFrame_stats = tk.Label(combat_UI_labelframe, text=self.ai_combat_status_text(3))
            ai3_combatFrame_statusEffects = tk.Label(combat_UI_labelframe, text="status effects")
            ai3_combatFrame_name.grid(row=10, column=3, sticky="e")
            ai3_combatFrame_stats.grid(row=11, column=3, sticky="e")
            ai3_combatFrame_statusEffects.grid(row=11, column=3)
            AI_CLF_dottedLine_label1 = tk.Label(combat_UI_labelframe, text="----------------")
            AI_CLF_dottedLine_label2 = tk.Label(combat_UI_labelframe, text="----------------")
            AI_CLF_dottedLine_label3 = tk.Label(combat_UI_labelframe, text="----------------")
            ai1_intented_attack_label = tk.Label(combat_UI_labelframe, text=ai1_attack_intention)
            ai2_intented_attack_label = tk.Label(combat_UI_labelframe, text=ai2_attack_intention)
            ai3_intented_attack_label = tk.Label(combat_UI_labelframe, text=ai3_attack_intention)
            ai1_intented_attack_label.grid(row=4, column=2, sticky="e")
            ai2_intented_attack_label.grid(row=7, column=2, sticky="e")
            ai3_intented_attack_label.grid(row=10, column=2, sticky="e")
            AI_CLF_dottedLine_label1.grid(row=3, column=3, sticky="e")
            AI_CLF_dottedLine_label2.grid(row=6, column=3, sticky="e")
            AI_CLF_dottedLine_label3.grid(row=9, column=3, sticky="e")
        elif AI_SPAWNED == 4:
            ai1_combatFrame_name = tk.Label(combat_UI_labelframe, text=self.ai_combat_name(1))
            ai1_combatFrame_stats = tk.Label(combat_UI_labelframe, text=self.ai_combat_status_text(1))
            ai1_combatFrame_statusEffects = tk.Label(combat_UI_labelframe, text="status effects")
            ai1_combatFrame_name.grid(row=1, column=3, sticky="e")
            ai1_combatFrame_stats.grid(row=2, column=3, sticky="e")
            ai1_combatFrame_statusEffects.grid(row=2, column=3)
            ai2_combatFrame_name = tk.Label(combat_UI_labelframe, text=self.ai_combat_name(2))
            ai2_combatFrame_stats = tk.Label(combat_UI_labelframe, text=self.ai_combat_status_text(2))
            ai2_combatFrame_statusEffects = tk.Label(combat_UI_labelframe, text="status effects")
            ai2_combatFrame_name.grid(row=4, column=3, sticky="e")
            ai2_combatFrame_stats.grid(row=5, column=3, sticky="e")
            ai2_combatFrame_statusEffects.grid(row=5, column=3)
            ai3_combatFrame_name = tk.Label(combat_UI_labelframe, text=self.ai_combat_name(3))
            ai3_combatFrame_stats = tk.Label(combat_UI_labelframe, text=self.ai_combat_status_text(3))
            ai3_combatFrame_statusEffects = tk.Label(combat_UI_labelframe, text="status effects")
            ai3_combatFrame_name.grid(row=7, column=3, sticky="e")
            ai3_combatFrame_stats.grid(row=8, column=3, sticky="e")
            ai3_combatFrame_statusEffects.grid(row=8, column=3)
            ai4_combatFrame_name = tk.Label(combat_UI_labelframe, text=self.ai_combat_name(4))
            ai4_combatFrame_stats = tk.Label(combat_UI_labelframe, text=self.ai_combat_status_text(4))
            ai4_combatFrame_statusEffects = tk.Label(combat_UI_labelframe, text="status effects")
            ai4_combatFrame_name.grid(row=10, column=3, sticky="e")
            ai4_combatFrame_stats.grid(row=11, column=3, sticky="e")
            ai4_combatFrame_statusEffects.grid(row=11, column=3)
            AI_CLF_dottedLine_label1 = tk.Label(combat_UI_labelframe, text="----------------")
            AI_CLF_dottedLine_label2 = tk.Label(combat_UI_labelframe, text="----------------")
            AI_CLF_dottedLine_label3 = tk.Label(combat_UI_labelframe, text="----------------")
            AI_CLF_dottedLine_label4 = tk.Label(combat_UI_labelframe, text="----------------")
            ai1_intented_attack_label = tk.Label(combat_UI_labelframe, text=ai1_attack_intention)
            ai2_intented_attack_label = tk.Label(combat_UI_labelframe, text=ai2_attack_intention)
            ai3_intented_attack_label = tk.Label(combat_UI_labelframe, text=ai3_attack_intention)
            ai4_intented_attack_label = tk.Label(combat_UI_labelframe, text=ai4_attack_intention)
            ai1_intented_attack_label.grid(row=1, column=2, sticky="e")
            ai2_intented_attack_label.grid(row=4, column=2, sticky="e")
            ai3_intented_attack_label.grid(row=7, column=2, sticky="e")
            ai4_intented_attack_label.grid(row=10, column=2, sticky="e")
            AI_CLF_dottedLine_label1.grid(row=0, column=3, sticky="e")
            AI_CLF_dottedLine_label2.grid(row=3, column=3, sticky="e")
            AI_CLF_dottedLine_label3.grid(row=6, column=3, sticky="e")
            AI_CLF_dottedLine_label4.grid(row=9, column=3, sticky="e")
        elif AI_SPAWNED == 5:
            ai1_combatFrame_name = tk.Label(combat_UI_labelframe, text=self.ai_combat_name(1))
            ai1_combatFrame_stats = tk.Label(combat_UI_labelframe, text=self.ai_combat_status_text(1))
            ai1_combatFrame_statusEffects = tk.Label(combat_UI_labelframe, text="status effects")
            ai1_combatFrame_name.grid(row=1, column=3, sticky="e")
            ai1_combatFrame_stats.grid(row=2, column=3, sticky="e")
            ai1_combatFrame_statusEffects.grid(row=2, column=3)
            ai2_combatFrame_name = tk.Label(combat_UI_labelframe, text=self.ai_combat_name(2))
            ai2_combatFrame_stats = tk.Label(combat_UI_labelframe, text=self.ai_combat_status_text(2))
            ai2_combatFrame_statusEffects = tk.Label(combat_UI_labelframe, text="status effects")
            ai2_combatFrame_name.grid(row=4, column=3, sticky="e")
            ai2_combatFrame_stats.grid(row=5, column=3, sticky="e")
            ai2_combatFrame_statusEffects.grid(row=5, column=3)
            ai3_combatFrame_name = tk.Label(combat_UI_labelframe, text=self.ai_combat_name(3))
            ai3_combatFrame_stats = tk.Label(combat_UI_labelframe, text=self.ai_combat_status_text(3))
            ai3_combatFrame_statusEffects = tk.Label(combat_UI_labelframe, text="status effects")
            ai3_combatFrame_name.grid(row=7, column=3, sticky="e")
            ai3_combatFrame_stats.grid(row=8, column=3, sticky="e")
            ai3_combatFrame_statusEffects.grid(row=8, column=3)
            ai4_combatFrame_name = tk.Label(combat_UI_labelframe, text=self.ai_combat_name(4))
            ai4_combatFrame_stats = tk.Label(combat_UI_labelframe, text=self.ai_combat_status_text(4))
            ai4_combatFrame_statusEffects = tk.Label(combat_UI_labelframe, text="status effects")
            ai4_combatFrame_name.grid(row=10, column=3, sticky="e")
            ai4_combatFrame_stats.grid(row=11, column=3, sticky="e")
            ai4_combatFrame_statusEffects.grid(row=11, column=3)
            ai5_combatFrame_name = tk.Label(combat_UI_labelframe, text=self.ai_combat_name(5))
            ai5_combatFrame_stats = tk.Label(combat_UI_labelframe, text=self.ai_combat_status_text(5))
            ai5_combatFrame_statusEffects = tk.Label(combat_UI_labelframe, text="status effects")
            ai5_combatFrame_name.grid(row=13, column=3, sticky="e")
            ai5_combatFrame_stats.grid(row=14, column=3, sticky="e")
            ai5_combatFrame_statusEffects.grid(row=14, column=3)
            AI_CLF_dottedLine_label1 = tk.Label(combat_UI_labelframe, text="----------------")
            AI_CLF_dottedLine_label2 = tk.Label(combat_UI_labelframe, text="----------------")
            AI_CLF_dottedLine_label3 = tk.Label(combat_UI_labelframe, text="----------------")
            AI_CLF_dottedLine_label4 = tk.Label(combat_UI_labelframe, text="----------------")
            AI_CLF_dottedLine_label5 = tk.Label(combat_UI_labelframe, text="----------------")
            ai1_intented_attack_label = tk.Label(combat_UI_labelframe, text=ai1_attack_intention)
            ai2_intented_attack_label = tk.Label(combat_UI_labelframe, text=ai2_attack_intention)
            ai3_intented_attack_label = tk.Label(combat_UI_labelframe, text=ai3_attack_intention)
            ai4_intented_attack_label = tk.Label(combat_UI_labelframe, text=ai4_attack_intention)
            ai5_intented_attack_label = tk.Label(combat_UI_labelframe, text=ai5_attack_intention)
            ai1_intented_attack_label.grid(row=1, column=2, sticky="e")
            ai2_intented_attack_label.grid(row=4, column=2, sticky="e")
            ai3_intented_attack_label.grid(row=7, column=2, sticky="e")
            ai4_intented_attack_label.grid(row=10, column=2, sticky="e")
            ai5_intented_attack_label.grid(row=13, column=2, sticky="e")
            AI_CLF_dottedLine_label1.grid(row=0, column=3, sticky="e")
            AI_CLF_dottedLine_label2.grid(row=3, column=3, sticky="e")
            AI_CLF_dottedLine_label3.grid(row=6, column=3, sticky="e")
            AI_CLF_dottedLine_label4.grid(row=9, column=3, sticky="e")
            AI_CLF_dottedLine_label5.grid(row=12, column=3, sticky="e")

    def ai_chose_attack_targets(self,):
        global ai1_attack_intention, ai2_attack_intention, ai3_attack_intention, ai4_attack_intention, ai5_attack_intention
        ai_attack_options = []
        if ai1_hp > 0:
            if ai1_attack == "null":
                ai1_attack_intention = ""
            else:
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
                    ai1_attack_intention = "{} <<< {}\n({} Damage)".format(ai_attack_target, ai1_attack[0], ai1_attack[1])
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
                    ai1_attack_intention = "{} and {} <<< {}\n({} Damage)".format(ai_attack1_target, ai_attack2_target, ai1_attack[0], ai1_attack[1])
                if ai1_attack[2] == "AOE":
                    ai1_attack_intention = "Everyone <<< {}\n({} Damage)".format(ai1_attack[0], ai1_attack[1])
        if ai2_hp > 0:
            if ai2_attack == "null":
                ai2_attack_intention = ""
            else:
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
                    ai2_attack_intention = "{} <<< {}\n({} Damage)".format(ai_attack_target, ai2_attack[0], ai2_attack[1])
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
                    ai2_attack_intention = "{} and {} <<< {}\n({} Damage)".format(ai_attack1_target, ai_attack2_target, ai2_attack[0],
                                                                  ai2_attack[1])
                if ai2_attack[2] == "AOE":
                    ai2_attack_intention = "Everyone <<< {}\n({} Damage)".format(ai2_attack[0], ai2_attack[1])
        if ai3_hp > 0:
            if ai3_attack == "null":
                ai3_attack_intention = ""
            else:
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
                    ai3_attack_intention = "{} <<< {}\n({} Damage)".format(ai_attack_target, ai3_attack[0], ai3_attack[1])
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
                    ai3_attack_intention = "{} and {} <<< {}\n({} Damage)".format(ai_attack1_target, ai_attack2_target, ai3_attack[0],
                                                                  ai3_attack[1])
                if ai3_attack[2] == "AOE":
                    ai3_attack_intention = "Everyone <<< {}\n({} Damage)".format(ai3_attack[0], ai3_attack[1])
        if ai4_hp > 0:
            if ai4_attack == "null":
                ai4_attack_intention = ""
            else:
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
                    ai4_attack_intention = "{} <<< {}\n({} Damage)".format(ai_attack_target, ai4_attack[0], ai4_attack[1])
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
                    ai4_attack_intention = "{} and {} <<< {}\n({} Damage)".format(ai_attack1_target, ai_attack2_target, ai4_attack[0],
                                                                  ai4_attack[1])
                if ai4_attack[2] == "AOE":
                    ai4_attack_intention = "Everyone <<< {}\n({} Damage)".format(ai4_attack[0], ai4_attack[1])
        if ai5_hp > 0:
            if ai5_attack == "null":
                ai5_attack_intention = ""
            else:
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
                    ai5_attack_intention = "{} <<< {}\n({} Damage)".format(ai_attack_target, ai5_attack[0], ai5_attack[1])
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
                    ai5_attack_intention = "{} and {} <<< {}\n({} Damage)".format(ai_attack1_target, ai_attack2_target, ai5_attack[0],
                                                                  ai5_attack[1])
                if ai5_attack[2] == "AOE":
                    ai5_attack_intention = "Everyone <<< {}\n({} Damage)".format(ai5_attack[0], ai5_attack[1])

    def champion_combat_name(self, champion_position):
        global champion1_hp, champion2_hp, champion3_hp, champion4_hp, champion5_hp
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
                status_text = "Health Points: {}/{}\n{}: {}/{}".format(champion1_hp, CHAMPION_1_HP, CHAMPION_1_RPNAME, champion1_rp, CHAMPION_1_RP)
                return status_text
        if champion_position == 2:
            if CHAMPION_2_RPNAME == "null":
                status_text = "Health Points: {}/{}".format(champion2_hp, CHAMPION_2_HP)
                return status_text
            else:
                if champion2_rp > CHAMPION_2_RP:
                    champion2_rp = CHAMPION_2_RP
                status_text = "Health Points: {}/{}\n{}: {}/{}".format(champion2_hp, CHAMPION_2_HP, CHAMPION_2_RPNAME, champion2_rp, CHAMPION_2_RP)
                return status_text
        if champion_position == 3:
            if CHAMPION_3_RPNAME == "null":
                status_text = "Health Points: {}/{}".format(champion3_hp, CHAMPION_3_HP)
                return status_text
            else:
                if champion3_rp > CHAMPION_3_RP:
                    champion3_rp = CHAMPION_3_RP
                status_text = "Health Points: {}/{}\n{}: {}/{}".format(champion3_hp, CHAMPION_3_HP, CHAMPION_3_RPNAME, champion3_rp, CHAMPION_3_RP)
                return status_text
        if champion_position == 4:
            if CHAMPION_4_RPNAME == "null":
                status_text = "Health Points: {}/{}".format(champion4_hp, CHAMPION_4_HP)
                return status_text
            else:
                if champion4_rp > CHAMPION_4_RP:
                    champion4_rp = CHAMPION_4_RP
                status_text = "Health Points: {}/{}\n{}: {}/{}".format(champion4_hp, CHAMPION_4_HP, CHAMPION_4_RPNAME, champion4_rp, CHAMPION_4_RP)
                return status_text
        if champion_position == 5:
            if CHAMPION_5_RPNAME == "null":
                status_text = "Health Points: {}/{}".format(champion5_hp, CHAMPION_5_HP)
                return status_text
            else:
                if champion5_rp > CHAMPION_5_RP:
                    champion5_rp = CHAMPION_5_RP
                status_text = "Health Points: {}/{}\n{}: {}/{}".format(champion5_hp, CHAMPION_5_HP, CHAMPION_5_RPNAME, champion5_rp, CHAMPION_5_RP)
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
            if AI_RESOURCE_NAME == "null":
                status_text = "\nHealth Points: {}/{}".format(ai1_hp, ai1_max_hp)
                return status_text
            else:
                status_text = "\nHealth Points: {}/{}\n{}: {}/{}".format(ai1_hp, ai1_max_hp, AI_RESOURCE_NAME, ai1_rp, AI_RESOURCE)
                return status_text
        if ai_position == 2:
            if AI_RESOURCE_NAME == "null":
                status_text = "\nHealth Points: {}/{}".format(ai2_hp, ai2_max_hp)
                return status_text
            else:
                status_text = "\nHealth Points: {}/{}\n{}: {}/{}".format(ai2_hp, ai2_max_hp, AI_RESOURCE_NAME, ai2_rp, AI_RESOURCE)
                return status_text
        if ai_position == 3:
            if AI_RESOURCE_NAME == "null":
                status_text = "\nHealth Points: {}/{}".format(ai3_hp, ai3_max_hp)
                return status_text
            else:
                status_text = "\nHealth Points: {}/{}\n{}: {}/{}".format(ai3_hp, ai3_max_hp, AI_RESOURCE_NAME, ai3_rp, AI_RESOURCE)
                return status_text
        if ai_position == 4:
            if AI_RESOURCE_NAME == "null":
                status_text = "\nHealth Points: {}/{}".format(ai4_hp, ai4_max_hp)
                return status_text
            else:
                status_text = "\nHealth Points: {}/{}\n{}: {}/{}".format(ai4_hp, ai4_max_hp, AI_RESOURCE_NAME, ai4_rp, AI_RESOURCE)
                return status_text
        if ai_position == 5:
            if AI_RESOURCE_NAME == "null":
                status_text = "\nHealth Points: {}/{}".format(ai5_hp, ai5_max_hp)
                return status_text
            else:
                status_text = "\nHealth Points: {}/{}\n{}: {}/{}".format(ai5_hp, ai5_max_hp, AI_RESOURCE_NAME, ai5_rp, AI_RESOURCE)
                return status_text

    def player_combat_champion1(self):
        global attack_button_champion1, special_button_champion1, rest_button_champion1, current_turn, new_round, from_attack_button, from_special_button
        current_turn = "C1"
        if new_round == 1:
            self.monster_attack_intentions()
            self.ai_chose_attack_targets()
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
        self.repeating_combatUI_refresh_function()
        self.get_champions_abiltity_button_data(1)
        attack_button_champion1 = tk.Button(combat_UI_labelframe, text=self.check_if_power_conduit_text(), width=59, height=10, command=self.check_if_power_conduit_command)
        special_button_champion1 = tk.Button(combat_UI_labelframe, text="Special Moves", width=59, height=10, command=self.special_button)
        rest_button_champion1 = tk.Button(combat_UI_labelframe, text="Rest", width=59, height=10)
        attack_button_champion1.grid(row=17, column=1)
        special_button_champion1.grid(row=17, column=2)
        rest_button_champion1.grid(row=17, column=3)
        
    def next_turn(self):
        if current_turn == "C1":
            self.player_combat_champion2()
        elif current_turn == "C2":
            self.player_combat_champion3()
        elif current_turn == "C3":
            self.player_combat_champion4()
        elif current_turn == "C4":
            self.player_combat_champion5()
        elif current_turn == "C5":
            self.monsters_turn()
        elif current_turn == "MN":
            self.player_combat_champion1()
    
    def player_combat_champion2(self):
        global attack_button_champion2, special_button_champion2, rest_button_champion2, current_turn, new_round, from_attack_button, from_special_button
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
        self.repeating_combatUI_refresh_function()
        self.get_champions_abiltity_button_data(2)
        attack_button_champion2 = tk.Button(combat_UI_labelframe, text=self.check_if_power_conduit_text(), width=59, height=10, command=self.check_if_power_conduit_command)
        special_button_champion2 = tk.Button(combat_UI_labelframe, text="Special Moves", width=59, height=10, command=self.special_button)
        rest_button_champion2 = tk.Button(combat_UI_labelframe, text="Rest", width=59, height=10)
        attack_button_champion2.grid(row=17, column=1)
        special_button_champion2.grid(row=17, column=2)
        rest_button_champion2.grid(row=17, column=3)
    
    def player_combat_champion3(self):
        global attack_button_champion3, special_button_champion3, rest_button_champion3, current_turn, new_round, from_attack_button, from_special_button
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
        self.repeating_combatUI_refresh_function()
        self.get_champions_abiltity_button_data(3)
        attack_button_champion3 = tk.Button(combat_UI_labelframe, text=self.check_if_power_conduit_text(), width=59, height=10, command=self.check_if_power_conduit_command)
        special_button_champion3 = tk.Button(combat_UI_labelframe, text="Special Moves", width=59, height=10, command=self.special_button)
        rest_button_champion3 = tk.Button(combat_UI_labelframe, text="Rest", width=59, height=10)
        attack_button_champion3.grid(row=17, column=1)
        special_button_champion3.grid(row=17, column=2)
        rest_button_champion3.grid(row=17, column=3)
    
    def player_combat_champion4(self):
        global attack_button_champion4, special_button_champion4, rest_button_champion4, current_turn, new_round, from_attack_button, from_special_button
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
        self.repeating_combatUI_refresh_function()
        self.get_champions_abiltity_button_data(4)
        attack_button_champion4 = tk.Button(combat_UI_labelframe, text=self.check_if_power_conduit_text(), width=59, height=10, command=self.check_if_power_conduit_command)
        special_button_champion4 = tk.Button(combat_UI_labelframe, text="Special Moves", width=59, height=10, command=self.special_button)
        rest_button_champion4 = tk.Button(combat_UI_labelframe, text="Rest", width=59, height=10)
        attack_button_champion4.grid(row=17, column=1)
        special_button_champion4.grid(row=17, column=2)
        rest_button_champion4.grid(row=17, column=3)
    
    def player_combat_champion5(self):
        global attack_button_champion5, special_button_champion5, rest_button_champion5, current_turn, new_round, from_attack_button, from_special_button
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
        self.repeating_combatUI_refresh_function()
        self.get_champions_abiltity_button_data(5)
        attack_button_champion5 = tk.Button(combat_UI_labelframe, text=self.check_if_power_conduit_text(), width=59, height=10, command=self.check_if_power_conduit_command)
        special_button_champion5 = tk.Button(combat_UI_labelframe, text="Special Moves", width=59, height=10, command=self.special_button)
        rest_button_champion5 = tk.Button(combat_UI_labelframe, text="Rest", width=59, height=10)
        attack_button_champion5.grid(row=17, column=1)
        special_button_champion5.grid(row=17, column=2)
        rest_button_champion5.grid(row=17, column=3)
        
    def monsters_turn(self):
        current_turn = "MN"
        self.next_turn()

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

    def attack_button(self):
        global attack1_button, attack1_button_details, attack2_button, attack2_button_details, attack3_button, attack3_button_details, attack4_button, attack4_button_details, back_button, \
            from_attack_button
        if current_turn == "C1":
            attack_button_champion1.destroy()
            special_button_champion1.destroy()
            rest_button_champion1.destroy()
            attack1_button = tk.Button(combat_UI_labelframe, text=attack_button_text_list[0], width=50, height=4, command=lambda: self.champion_attacks(attack_button_text_list[0]))
            attack1_button_details = tk.Button(combat_UI_labelframe, text="{} Details".format(attack_button_text_list[0]), width=38, height=1)
            attack2_button = tk.Button(combat_UI_labelframe, text=attack_button_text_list[1], width=50, height=4, command=lambda: self.champion_attacks(attack_button_text_list[1]))
            attack2_button_details = tk.Button(combat_UI_labelframe,
                                              text="{} Details".format(attack_button_text_list[1]), width=38, height=1)
            attack3_button = tk.Button(combat_UI_labelframe, text=attack_button_text_list[2], width=50, height=4, command=lambda: self.champion_attacks(attack_button_text_list[2]))
            attack3_button_details = tk.Button(combat_UI_labelframe,
                                              text="{} Details".format(attack_button_text_list[2]), width=38, height=1)
            attack4_button = tk.Button(combat_UI_labelframe, text=attack_button_text_list[3], width=50, height=4, command=lambda: self.champion_attacks(attack_button_text_list[3]))
            attack4_button_details = tk.Button(combat_UI_labelframe,
                                              text="{} Details".format(attack_button_text_list[3]), width=38, height=1)
            back_button = tk.Button(combat_UI_labelframe, text="Back", command=self.player_combat_champion1)
            back_button.grid(row=19, column=2,pady=20)
            attack1_button.grid(row=17, column=1)
            attack1_button_details.grid(row=18, column=1)
            attack2_button.grid(row=17, column=3)
            attack2_button_details.grid(row=18, column=3)
            attack3_button.grid(row=19, column=1)
            attack3_button_details.grid(row=20, column=1)
            attack4_button.grid(row=19, column=3)
            attack4_button_details.grid(row=20, column=3)
            from_attack_button = 1
        if current_turn == "C2":
            attack_button_champion2.destroy()
            special_button_champion2.destroy()
            rest_button_champion2.destroy()
            attack1_button = tk.Button(combat_UI_labelframe, text=attack_button_text_list[0], width=50, height=4, command=lambda: self.champion_attacks(attack_button_text_list[0]))
            attack1_button_details = tk.Button(combat_UI_labelframe,
                                               text="{} Details".format(attack_button_text_list[0]), width=38, height=1)
            attack2_button = tk.Button(combat_UI_labelframe, text=attack_button_text_list[1], width=50, height=4, command=lambda: self.champion_attacks(attack_button_text_list[1]))
            attack2_button_details = tk.Button(combat_UI_labelframe,
                                               text="{} Details".format(attack_button_text_list[1]), width=38, height=1)
            attack3_button = tk.Button(combat_UI_labelframe, text=attack_button_text_list[2], width=50, height=4, command=lambda: self.champion_attacks(attack_button_text_list[2]))
            attack3_button_details = tk.Button(combat_UI_labelframe,
                                               text="{} Details".format(attack_button_text_list[2]), width=38, height=1)
            attack4_button = tk.Button(combat_UI_labelframe, text=attack_button_text_list[3], width=50, height=4, command=lambda: self.champion_attacks(attack_button_text_list[3]))
            attack4_button_details = tk.Button(combat_UI_labelframe,
                                               text="{} Details".format(attack_button_text_list[3]), width=38, height=1)
            back_button = tk.Button(combat_UI_labelframe, text="Back", command=self.player_combat_champion2)
            back_button.grid(row=19, column=2, pady=20)
            attack1_button.grid(row=17, column=1)
            attack1_button_details.grid(row=18, column=1)
            attack2_button.grid(row=17, column=3)
            attack2_button_details.grid(row=18, column=3)
            attack3_button.grid(row=19, column=1)
            attack3_button_details.grid(row=20, column=1)
            attack4_button.grid(row=19, column=3)
            attack4_button_details.grid(row=20, column=3)
            from_attack_button = 1
        if current_turn == "C3":
            attack_button_champion3.destroy()
            special_button_champion3.destroy()
            rest_button_champion3.destroy()
            attack1_button = tk.Button(combat_UI_labelframe, text=attack_button_text_list[0], width=50, height=4, command=lambda: self.champion_attacks(attack_button_text_list[0]))
            attack1_button_details = tk.Button(combat_UI_labelframe,
                                               text="{} Details".format(attack_button_text_list[0]), width=38, height=1)
            attack2_button = tk.Button(combat_UI_labelframe, text=attack_button_text_list[1], width=50, height=4, command=lambda: self.champion_attacks(attack_button_text_list[1]))
            attack2_button_details = tk.Button(combat_UI_labelframe,
                                               text="{} Details".format(attack_button_text_list[1]), width=38, height=1)
            attack3_button = tk.Button(combat_UI_labelframe, text=attack_button_text_list[2], width=50, height=4, command=lambda: self.champion_attacks(attack_button_text_list[2]))
            attack3_button_details = tk.Button(combat_UI_labelframe,
                                               text="{} Details".format(attack_button_text_list[2]), width=38, height=1)
            attack4_button = tk.Button(combat_UI_labelframe, text=attack_button_text_list[3], width=50, height=4, command=lambda: self.champion_attacks(attack_button_text_list[3]))
            attack4_button_details = tk.Button(combat_UI_labelframe,
                                               text="{} Details".format(attack_button_text_list[3]), width=38, height=1)
            back_button = tk.Button(combat_UI_labelframe, text="Back", command=self.player_combat_champion3)
            back_button.grid(row=19, column=2, pady=20)
            attack1_button.grid(row=17, column=1)
            attack1_button_details.grid(row=18, column=1)
            attack2_button.grid(row=17, column=3)
            attack2_button_details.grid(row=18, column=3)
            attack3_button.grid(row=19, column=1)
            attack3_button_details.grid(row=20, column=1)
            attack4_button.grid(row=19, column=3)
            attack4_button_details.grid(row=20, column=3)
            from_attack_button = 1
        if current_turn == "C4":
            attack_button_champion4.destroy()
            special_button_champion4.destroy()
            rest_button_champion4.destroy()
            attack1_button = tk.Button(combat_UI_labelframe, text=attack_button_text_list[0], width=50, height=4, command=lambda: self.champion_attacks(attack_button_text_list[0]))
            attack1_button_details = tk.Button(combat_UI_labelframe,
                                               text="{} Details".format(attack_button_text_list[0]), width=38, height=1)
            attack2_button = tk.Button(combat_UI_labelframe, text=attack_button_text_list[1], width=50, height=4, command=lambda: self.champion_attacks(attack_button_text_list[1]))
            attack2_button_details = tk.Button(combat_UI_labelframe,
                                               text="{} Details".format(attack_button_text_list[1]), width=38, height=1)
            attack3_button = tk.Button(combat_UI_labelframe, text=attack_button_text_list[2], width=50, height=4, command=lambda: self.champion_attacks(attack_button_text_list[2]))
            attack3_button_details = tk.Button(combat_UI_labelframe,
                                               text="{} Details".format(attack_button_text_list[2]), width=38, height=1)
            attack4_button = tk.Button(combat_UI_labelframe, text=attack_button_text_list[3], width=50, height=4, command=lambda: self.champion_attacks(attack_button_text_list[3]))
            attack4_button_details = tk.Button(combat_UI_labelframe,
                                               text="{} Details".format(attack_button_text_list[3]), width=38, height=1)
            back_button = tk.Button(combat_UI_labelframe, text="Back", command=self.player_combat_champion4)
            back_button.grid(row=19, column=2, pady=20)
            attack1_button.grid(row=17, column=1)
            attack1_button_details.grid(row=18, column=1)
            attack2_button.grid(row=17, column=3)
            attack2_button_details.grid(row=18, column=3)
            attack3_button.grid(row=19, column=1)
            attack3_button_details.grid(row=20, column=1)
            attack4_button.grid(row=19, column=3)
            attack4_button_details.grid(row=20, column=3)
            from_attack_button = 1
        if current_turn == "C5":
            attack_button_champion5.destroy()
            special_button_champion5.destroy()
            rest_button_champion5.destroy()
            attack1_button = tk.Button(combat_UI_labelframe, text=attack_button_text_list[0], width=50, height=4, command=lambda: self.champion_attacks(attack_button_text_list[0]))
            attack1_button_details = tk.Button(combat_UI_labelframe,
                                               text="{} Details".format(attack_button_text_list[0]), width=38, height=1)
            attack2_button = tk.Button(combat_UI_labelframe, text=attack_button_text_list[1], width=50, height=4, command=lambda: self.champion_attacks(attack_button_text_list[1]))
            attack2_button_details = tk.Button(combat_UI_labelframe,
                                               text="{} Details".format(attack_button_text_list[1]), width=38, height=1)
            attack3_button = tk.Button(combat_UI_labelframe, text=attack_button_text_list[2], width=50, height=4, command=lambda: self.champion_attacks(attack_button_text_list[2]))
            attack3_button_details = tk.Button(combat_UI_labelframe,
                                               text="{} Details".format(attack_button_text_list[2]), width=38, height=1)
            attack4_button = tk.Button(combat_UI_labelframe, text=attack_button_text_list[3], width=50, height=4, command=lambda: self.champion_attacks(attack_button_text_list[3]))
            attack4_button_details = tk.Button(combat_UI_labelframe,
                                               text="{} Details".format(attack_button_text_list[3]), width=38, height=1)
            back_button = tk.Button(combat_UI_labelframe, text="Back", command=self.player_combat_champion5)
            back_button.grid(row=19, column=2, pady=20)
            attack1_button.grid(row=17, column=1)
            attack1_button_details.grid(row=18, column=1)
            attack2_button.grid(row=17, column=3)
            attack2_button_details.grid(row=18, column=3)
            attack3_button.grid(row=19, column=1)
            attack3_button_details.grid(row=20, column=1)
            attack4_button.grid(row=19, column=3)
            attack4_button_details.grid(row=20, column=3)
            from_attack_button = 1
    def champion_attacks(self, ability_name):
        global attack_to_target, special_to_target, ability_data, champion1_rp, champion2_rp, champion3_rp, champion4_rp, champion5_rp, palm_strike_requirements
        attack_to_target = 1
        special_to_target = 0
        counter = 1
        damage_done = 0
        if ability_name == "Empty":
            return
        if ability_name == "Palm Strike":
            if palm_strike_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == "Monk":
                        if counter == 1:
                            if palm_strike_requirements[0] <= champion1_rp:
                                champion1_rp = champion1_rp - palm_strike_requirements[0]
                                ability_data = ["Palm Strike", "enemy", "1T"]
                                palm_strike_requirements[1] = palm_strike_requirements[2]
                                champion1_rp = champion1_rp + palm_strike_requirements[3]
                                if len(champion1_big_external_buffs) != 1:
                                    damage_done = ((MONK.ap + champion1_small_external_buffs[0]) * champion1_big_external_buffs[0])
                                else:
                                    damage_done = (MONK.ap + champion1_small_external_buffs[0])
                                ability_data = ["Palm Strike", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 2:
                            if palm_strike_requirements[0] <= champion2_rp:
                                champion2_rp = champion2_rp - palm_strike_requirements[0]
                                palm_strike_requirements[1] = palm_strike_requirements[2]
                                champion2_rp = champion2_rp + palm_strike_requirements[3]
                                if len(champion2_big_external_buffs) != 1:
                                    damage_done = ((MONK.ap + champion2_small_external_buffs[0]) *
                                                   champion2_big_external_buffs[0])
                                else:
                                    damage_done = (MONK.ap + champion2_small_external_buffs[0])
                                ability_data = ["Palm Strike", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 3:
                            if palm_strike_requirements[0] <= champion3_rp:
                                champion3_rp = champion3_rp - palm_strike_requirements[0]
                                palm_strike_requirements[1] = palm_strike_requirements[2]
                                champion3_rp = champion3_rp + palm_strike_requirements[3]
                                if len(champion3_big_external_buffs) != 1:
                                    damage_done = ((MONK.ap + champion3_small_external_buffs[0]) *
                                                   champion3_big_external_buffs[0])
                                else:
                                    damage_done = (MONK.ap + champion3_small_external_buffs[0])
                                ability_data = ["Palm Strike", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 4:
                            if palm_strike_requirements[0] <= champion4_rp:
                                champion4_rp = champion4_rp - palm_strike_requirements[0]
                                palm_strike_requirements[1] = palm_strike_requirements[2]
                                champion4_rp = champion4_rp + palm_strike_requirements[3]
                                if len(champion4_big_external_buffs) != 1:
                                    damage_done = ((MONK.ap + champion4_small_external_buffs[0]) *
                                                   champion4_big_external_buffs[0])
                                else:
                                    damage_done = (MONK.ap + champion4_small_external_buffs[0])
                                ability_data = ["Palm Strike", "enemy", "1T", damage_done]
                            else:
                                return
                        if counter == 5:
                            if palm_strike_requirements[0] <= champion5_rp:
                                champion5_rp = champion5_rp - palm_strike_requirements[0]
                                palm_strike_requirements[1] = palm_strike_requirements[2]
                                champion5_rp = champion5_rp + palm_strike_requirements[3]
                                if len(champion5_big_external_buffs) != 1:
                                    damage_done = ((MONK.ap + champion5_small_external_buffs[0]) *
                                                   champion5_big_external_buffs[0])
                                else:
                                    damage_done = (MONK.ap + champion5_small_external_buffs[0])
                                ability_data = ["Palm Strike", "enemy", "1T", damage_done]
                            else:
                                return
                    counter += 1
            else:
                return
        elif ability_name == "Leg Sweep":
            if leg_sweep_requirements[1] == 0:
                for character in CHAMPION_LIST:
                    if character == "Monk":
                        if counter == 1:
                            if counter == 1:
                                if leg_sweep_requirements[0] <= champion1_rp:
                                    champion1_rp = champion1_rp - leg_sweep_requirements[0]
                                    ability_data = ["Palm Strike", "enemy", "1T"]
                                    leg_sweep_requirements[1] = leg_sweep_requirements[2]
                                    champion1_rp = champion1_rp + leg_sweep_requirements[3]
                                    if len(champion1_big_external_buffs) != 1:
                                        damage_done = ((MONK.ap + champion1_small_external_buffs[0]) *
                                                       champion1_big_external_buffs[0])
                                    else:
                                        damage_done = (MONK.ap + champion1_small_external_buffs[0])
                                    ability_data = ["Palm Strike", "enemy", "1T", damage_done]
                                else:
                                    return
                            if counter == 2:
                                if leg_sweep_requirements[0] <= champion2_rp:
                                    champion2_rp = champion2_rp - leg_sweep_requirements[0]
                                    leg_sweep_requirements[1] = leg_sweep_requirements[2]
                                    champion2_rp = champion2_rp + leg_sweep_requirements[3]
                                    if len(champion2_big_external_buffs) != 1:
                                        damage_done = ((MONK.ap + champion2_small_external_buffs[0]) *
                                                       champion2_big_external_buffs[0])
                                    else:
                                        damage_done = (MONK.ap + champion2_small_external_buffs[0])
                                    ability_data = ["Palm Strike", "enemy", "1T", damage_done]
                                else:
                                    return
                            if counter == 3:
                                if leg_sweep_requirements[0] <= champion3_rp:
                                    champion3_rp = champion3_rp - leg_sweep_requirements[0]
                                    leg_sweep_requirements[1] = leg_sweep_requirements[2]
                                    champion3_rp = champion3_rp + leg_sweep_requirements[3]
                                    if len(champion3_big_external_buffs) != 1:
                                        damage_done = ((MONK.ap + champion3_small_external_buffs[0]) *
                                                       champion3_big_external_buffs[0])
                                    else:
                                        damage_done = (MONK.ap + champion3_small_external_buffs[0])
                                    ability_data = ["Palm Strike", "enemy", "1T", damage_done]
                                else:
                                    return
                            if counter == 4:
                                if leg_sweep_requirements[0] <= champion4_rp:
                                    champion4_rp = champion4_rp - leg_sweep_requirements[0]
                                    leg_sweep_requirements[1] = leg_sweep_requirements[2]
                                    champion4_rp = champion4_rp + leg_sweep_requirements[3]
                                    if len(champion4_big_external_buffs) != 1:
                                        damage_done = ((MONK.ap + champion4_small_external_buffs[0]) *
                                                       champion4_big_external_buffs[0])
                                    else:
                                        damage_done = (MONK.ap + champion4_small_external_buffs[0])
                                    ability_data = ["Palm Strike", "enemy", "1T", damage_done]
                                else:
                                    return
                            if counter == 5:
                                if leg_sweep_requirements[0] <= champion5_rp:
                                    champion5_rp = champion5_rp - leg_sweep_requirements[0]
                                    leg_sweep_requirements[1] = leg_sweep_requirements[2]
                                    champion5_rp = champion5_rp + leg_sweep_requirements[3]
                                    if len(champion5_big_external_buffs) != 1:
                                        damage_done = ((MONK.ap + champion5_small_external_buffs[0]) *
                                                       champion5_big_external_buffs[0])
                                    else:
                                        damage_done = (MONK.ap + champion5_small_external_buffs[0])
                                    ability_data = ["Palm Strike", "enemy", "1T", damage_done]
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
            special1_button = tk.Button(combat_UI_labelframe, text=specials_button_text_list[0], width=50, height=4)
            special1_button_details = tk.Button(combat_UI_labelframe, text="{} Details".format(specials_button_text_list[0]), width=38, height=1)
            special2_button = tk.Button(combat_UI_labelframe, text=specials_button_text_list[1], width=50, height=4)
            special2_button_details = tk.Button(combat_UI_labelframe,
                                              text="{} Details".format(specials_button_text_list[1]), width=38, height=1)
            special3_button = tk.Button(combat_UI_labelframe, text=specials_button_text_list[2], width=50, height=4)
            special3_button_details = tk.Button(combat_UI_labelframe,
                                              text="{} Details".format(specials_button_text_list[2]), width=38, height=1)
            special4_button = tk.Button(combat_UI_labelframe, text=specials_button_text_list[3], width=50, height=4)
            special4_button_details = tk.Button(combat_UI_labelframe,
                                              text="{} Details".format(specials_button_text_list[3]), width=38, height=1)
            back_button = tk.Button(combat_UI_labelframe, text="Back", command=self.player_combat_champion1)
            back_button.grid(row=19, column=2,pady=20)
            special1_button.grid(row=17, column=1)
            special1_button_details.grid(row=18, column=1)
            special2_button.grid(row=17, column=3)
            special2_button_details.grid(row=18, column=3)
            special3_button.grid(row=19, column=1)
            special3_button_details.grid(row=20, column=1)
            special4_button.grid(row=19, column=3)
            special4_button_details.grid(row=20, column=3)
            from_special_button = 1
        if current_turn == "C2":
            attack_button_champion2.destroy()
            special_button_champion2.destroy()
            rest_button_champion2.destroy()
            special1_button = tk.Button(combat_UI_labelframe, text=specials_button_text_list[0], width=50, height=4)
            special1_button_details = tk.Button(combat_UI_labelframe,
                                               text="{} Details".format(specials_button_text_list[0]), width=38, height=1)
            special2_button = tk.Button(combat_UI_labelframe, text=specials_button_text_list[1], width=50, height=4)
            special2_button_details = tk.Button(combat_UI_labelframe,
                                               text="{} Details".format(specials_button_text_list[1]), width=38, height=1)
            special3_button = tk.Button(combat_UI_labelframe, text=specials_button_text_list[2], width=50, height=4)
            special3_button_details = tk.Button(combat_UI_labelframe,
                                               text="{} Details".format(specials_button_text_list[2]), width=38, height=1)
            special4_button = tk.Button(combat_UI_labelframe, text=specials_button_text_list[3], width=50, height=4)
            special4_button_details = tk.Button(combat_UI_labelframe,
                                               text="{} Details".format(specials_button_text_list[3]), width=38, height=1)
            back_button = tk.Button(combat_UI_labelframe, text="Back", command=self.player_combat_champion2)
            back_button.grid(row=19, column=2, pady=20)
            special1_button.grid(row=17, column=1)
            special1_button_details.grid(row=18, column=1)
            special2_button.grid(row=17, column=3)
            special2_button_details.grid(row=18, column=3)
            special3_button.grid(row=19, column=1)
            special3_button_details.grid(row=20, column=1)
            special4_button.grid(row=19, column=3)
            special4_button_details.grid(row=20, column=3)
            from_special_button = 1
        if current_turn == "C3":
            attack_button_champion3.destroy()
            special_button_champion3.destroy()
            rest_button_champion3.destroy()
            special1_button = tk.Button(combat_UI_labelframe, text=specials_button_text_list[0], width=50, height=4)
            special1_button_details = tk.Button(combat_UI_labelframe,
                                               text="{} Details".format(specials_button_text_list[0]), width=38, height=1)
            special2_button = tk.Button(combat_UI_labelframe, text=specials_button_text_list[1], width=50, height=4)
            special2_button_details = tk.Button(combat_UI_labelframe,
                                               text="{} Details".format(specials_button_text_list[1]), width=38, height=1)
            special3_button = tk.Button(combat_UI_labelframe, text=specials_button_text_list[2], width=50, height=4)
            special3_button_details = tk.Button(combat_UI_labelframe,
                                               text="{} Details".format(specials_button_text_list[2]), width=38, height=1)
            special4_button = tk.Button(combat_UI_labelframe, text=specials_button_text_list[3], width=50, height=4)
            special4_button_details = tk.Button(combat_UI_labelframe,
                                               text="{} Details".format(specials_button_text_list[3]), width=38, height=1)
            back_button = tk.Button(combat_UI_labelframe, text="Back", command=self.player_combat_champion3)
            back_button.grid(row=19, column=2, pady=20)
            special1_button.grid(row=17, column=1)
            special1_button_details.grid(row=18, column=1)
            special2_button.grid(row=17, column=3)
            special2_button_details.grid(row=18, column=3)
            special3_button.grid(row=19, column=1)
            special3_button_details.grid(row=20, column=1)
            special4_button.grid(row=19, column=3)
            special4_button_details.grid(row=20, column=3)
            from_special_button = 1
        if current_turn == "C4":
            attack_button_champion4.destroy()
            special_button_champion4.destroy()
            rest_button_champion4.destroy()
            special1_button = tk.Button(combat_UI_labelframe, text=specials_button_text_list[0], width=50, height=4)
            special1_button_details = tk.Button(combat_UI_labelframe,
                                               text="{} Details".format(specials_button_text_list[0]), width=38, height=1)
            special2_button = tk.Button(combat_UI_labelframe, text=specials_button_text_list[1], width=50, height=4)
            special2_button_details = tk.Button(combat_UI_labelframe,
                                               text="{} Details".format(specials_button_text_list[1]), width=38, height=1)
            special3_button = tk.Button(combat_UI_labelframe, text=specials_button_text_list[2], width=50, height=4)
            special3_button_details = tk.Button(combat_UI_labelframe,
                                               text="{} Details".format(specials_button_text_list[2]), width=38, height=1)
            special4_button = tk.Button(combat_UI_labelframe, text=specials_button_text_list[3], width=50, height=4)
            special4_button_details = tk.Button(combat_UI_labelframe,
                                               text="{} Details".format(specials_button_text_list[3]), width=38, height=1)
            back_button = tk.Button(combat_UI_labelframe, text="Back", command=self.player_combat_champion4)
            back_button.grid(row=19, column=2, pady=20)
            special1_button.grid(row=17, column=1)
            special1_button_details.grid(row=18, column=1)
            special2_button.grid(row=17, column=3)
            special2_button_details.grid(row=18, column=3)
            special3_button.grid(row=19, column=1)
            special3_button_details.grid(row=20, column=1)
            special4_button.grid(row=19, column=3)
            special4_button_details.grid(row=20, column=3)
            from_special_button = 1
        if current_turn == "C5":
            attack_button_champion5.destroy()
            special_button_champion5.destroy()
            rest_button_champion5.destroy()
            special1_button = tk.Button(combat_UI_labelframe, text=specials_button_text_list[0], width=50, height=4)
            special1_button_details = tk.Button(combat_UI_labelframe,
                                               text="{} Details".format(specials_button_text_list[0]), width=38, height=1)
            special2_button = tk.Button(combat_UI_labelframe, text=specials_button_text_list[1], width=50, height=4)
            special2_button_details = tk.Button(combat_UI_labelframe,
                                               text="{} Details".format(specials_button_text_list[1]), width=38, height=1)
            special3_button = tk.Button(combat_UI_labelframe, text=specials_button_text_list[2], width=50, height=4)
            special3_button_details = tk.Button(combat_UI_labelframe,
                                               text="{} Details".format(specials_button_text_list[2]), width=38, height=1)
            special4_button = tk.Button(combat_UI_labelframe, text=specials_button_text_list[3], width=50, height=4)
            special4_button_details = tk.Button(combat_UI_labelframe,
                                               text="{} Details".format(specials_button_text_list[3]), width=38, height=1)
            back_button = tk.Button(combat_UI_labelframe, text="Back", command=self.player_combat_champion5)
            back_button.grid(row=19, column=2, pady=20)
            special1_button.grid(row=17, column=1)
            special1_button_details.grid(row=18, column=1)
            special2_button.grid(row=17, column=3)
            special2_button_details.grid(row=18, column=3)
            special3_button.grid(row=19, column=1)
            special3_button_details.grid(row=20, column=1)
            special4_button.grid(row=19, column=3)
            special4_button_details.grid(row=20, column=3)
            from_special_button = 1

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
            if AI_SPAWNED == 1:
                ai1_attacktarget_frame = tk.Button(combat_UI_labelframe, text=self.target_frame_ai_champion_text("ai", 1), command=lambda: self.complete_turn(1))
                ai1_attacktarget_frame.grid(row=17, column=2)
            elif AI_SPAWNED == 2:
                ai1_attacktarget_frame = tk.Button(combat_UI_labelframe, text=self.target_frame_ai_champion_text("ai", 1), command=lambda: self.complete_turn(1))
                ai1_attacktarget_frame.grid(row=17, column=2, sticky="w")
                ai2_attacktarget_frame = tk.Button(combat_UI_labelframe, text=self.target_frame_ai_champion_text("ai", 2), command=lambda: self.complete_turn(2))
                ai2_attacktarget_frame.grid(row=17, column=2, sticky="e")
                if ai1_hp == 0:
                    ai1_attacktarget_frame["state"] = 'disable'
                if ai2_hp == 0:
                    ai2_attacktarget_frame["state"] = 'disable'
            elif AI_SPAWNED == 3:
                ai1_attacktarget_frame = tk.Button(combat_UI_labelframe, text=self.target_frame_ai_champion_text("ai", 1), command=lambda: self.complete_turn(1))
                ai1_attacktarget_frame.grid(row=17, column=1)
                ai2_attacktarget_frame = tk.Button(combat_UI_labelframe, text=self.target_frame_ai_champion_text("ai", 2), command=lambda: self.complete_turn(2))
                ai2_attacktarget_frame.grid(row=17, column=2)
                ai3_attacktarget_frame = tk.Button(combat_UI_labelframe, text=self.target_frame_ai_champion_text("ai", 3), command=lambda: self.complete_turn(3))
                ai3_attacktarget_frame.grid(row=17, column=3)
                if ai1_hp == 0:
                    ai1_attacktarget_frame["state"] = 'disable'
                if ai2_hp == 0:
                    ai2_attacktarget_frame["state"] = 'disable'
                if ai3_hp == 0:
                    ai3_attacktarget_frame["state"] = 'disable'
            elif AI_SPAWNED == 4:
                ai1_attacktarget_frame = tk.Button(combat_UI_labelframe, text=self.target_frame_ai_champion_text("ai", 1), command=lambda: self.complete_turn(1))
                ai1_attacktarget_frame.grid(row=17, column=1, sticky="e")
                ai2_attacktarget_frame = tk.Button(combat_UI_labelframe, text=self.target_frame_ai_champion_text("ai", 2), command=lambda: self.complete_turn(2))
                ai2_attacktarget_frame.grid(row=17, column=3, sticky="w")
                ai3_attacktarget_frame = tk.Button(combat_UI_labelframe, text=self.target_frame_ai_champion_text("ai", 3), command=lambda: self.complete_turn(3))
                ai3_attacktarget_frame.grid(row=18, column=1, sticky="e")
                ai4_attacktarget_frame = tk.Button(combat_UI_labelframe, text=self.target_frame_ai_champion_text("ai", 4), command=lambda: self.complete_turn(4))
                ai4_attacktarget_frame.grid(row=18, column=3, sticky="w")
                if ai1_hp == 0:
                    ai1_attacktarget_frame["state"] = 'disable'
                if ai2_hp == 0:
                    ai2_attacktarget_frame["state"] = 'disable'
                if ai3_hp == 0:
                    ai3_attacktarget_frame["state"] = 'disable'
                if ai4_hp == 0:
                    ai4_attacktarget_frame["state"] = 'disable'
            elif AI_SPAWNED == 5:
                ai1_attacktarget_frame = tk.Button(combat_UI_labelframe, text=self.target_frame_ai_champion_text("ai", 1), command=lambda: self.complete_turn(1))
                ai1_attacktarget_frame.grid(row=17, column=1)
                ai2_attacktarget_frame = tk.Button(combat_UI_labelframe, text=self.target_frame_ai_champion_text("ai", 2), command=lambda: self.complete_turn(2))
                ai2_attacktarget_frame.grid(row=17, column=1, sticky="e")
                ai3_attacktarget_frame = tk.Button(combat_UI_labelframe, text=self.target_frame_ai_champion_text("ai", 3), command=lambda: self.complete_turn(3))
                ai3_attacktarget_frame.grid(row=17, column=2)
                ai4_attacktarget_frame = tk.Button(combat_UI_labelframe, text=self.target_frame_ai_champion_text("ai", 4), command=lambda: self.complete_turn(4))
                ai4_attacktarget_frame.grid(row=17, column=3, sticky="w")
                ai5_attacktarget_frame = tk.Button(combat_UI_labelframe, text=self.target_frame_ai_champion_text("ai", 5), command=lambda: self.complete_turn(5))
                ai5_attacktarget_frame.grid(row=17, column=3)
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
            champion1_supporttarget_frame = tk.Button(combat_UI_labelframe, text=self.target_frame_ai_champion_text("champion", 1))
            champion1_supporttarget_frame.grid(row=17, column=1)
            champion2_supporttarget_frame = tk.Button(combat_UI_labelframe, text=self.target_frame_ai_champion_text("champion", 2))
            champion2_supporttarget_frame.grid(row=17, column=2)
            champion3_supporttarget_frame = tk.Button(combat_UI_labelframe, text=self.target_frame_ai_champion_text("champion", 3))
            champion3_supporttarget_frame.grid(row=17, column=3)
            champion4_supporttarget_frame = tk.Button(combat_UI_labelframe, text=self.target_frame_ai_champion_text("champion", 4))
            champion4_supporttarget_frame.grid(row=18, column=1, sticky="e")
            champion5_supporttarget_frame = tk.Button(combat_UI_labelframe, text=self.target_frame_ai_champion_text("champion", 5))
            champion5_supporttarget_frame.grid(row=18, column=3, sticky="w")
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

    def complete_turn(self, target):
        if ability_data[1] == "enemy":
            self.finalise_damage_dealt(target)
        if ability_data[1] == "ally":
            self.finalise_healing_done(target)
        self.clean_up()
        self.next_turn()
    def finalise_damage_dealt(self, target):
        global ai1_hp, ai2_hp, ai3_hp, ai4_hp, ai5_hp
        if ability_data[0] == "Palm Strike":
            if target == 1:
                ai1_hp = ai1_hp - ability_data[3]
            if target == 2:
                ai2_hp = ai2_hp - ability_data[3]
            if target == 3:
                ai3_hp = ai3_hp - ability_data[3]
            if target == 4:
                ai4_hp = ai4_hp - ability_data[3]
            if target == 5:
                ai5_hp = ai5_hp - ability_data[3]

    def finalise_healing_done(self, target):
        global champion1_hp, champion2_hp, champion3_hp, champion4_hp, champion5_hp

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
                    status_text = "{}\n*DEAD*\nHealth Points: {}/{}".format(CHAMPION_LIST[0], champion1_hp, CHAMPION_1_HP)
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
        global attack_button_text_list, specials_button_text_list
        attack_button_text_list = []
        specials_button_text_list = []
        if champion_position == 1:
            for abilities in CHAMPION_1_ATTACKLIST:
                attack_button_text_list.append(abilities)
            while len(attack_button_text_list) < 4:
                attack_button_text_list.append("Empty")
            for abiltities in CHAMPION_1_SPECIALLIST:
                specials_button_text_list.append(abiltities)
            while len(specials_button_text_list) < 4:
                specials_button_text_list.append("Empty")
        if champion_position == 2:
            for abilities in CHAMPION_2_ATTACKLIST:
                attack_button_text_list.append(abilities)
            while len(attack_button_text_list) < 4:
                attack_button_text_list.append("Empty")
            for abiltities in CHAMPION_2_SPECIALLIST:
                specials_button_text_list.append(abiltities)
            while len(specials_button_text_list) < 4:
                specials_button_text_list.append("Empty")
        if champion_position == 3:
            for abilities in CHAMPION_3_ATTACKLIST:
                attack_button_text_list.append(abilities)
            while len(attack_button_text_list) < 4:
                attack_button_text_list.append("Empty")
            for abiltities in CHAMPION_3_SPECIALLIST:
                specials_button_text_list.append(abiltities)
            while len(specials_button_text_list) < 4:
                specials_button_text_list.append("Empty")
        if champion_position == 4:
            for abilities in CHAMPION_4_ATTACKLIST:
                attack_button_text_list.append(abilities)
            while len(attack_button_text_list) < 4:
                attack_button_text_list.append("Empty")
            for abiltities in CHAMPION_4_SPECIALLIST:
                specials_button_text_list.append(abiltities)
            while len(specials_button_text_list) < 4:
                specials_button_text_list.append("Empty")
        if champion_position == 5:
            for abilities in CHAMPION_5_ATTACKLIST:
                attack_button_text_list.append(abilities)
            while len(attack_button_text_list) < 4:
                attack_button_text_list.append("Empty")
            for abiltities in CHAMPION_5_SPECIALLIST:
                specials_button_text_list.append(abiltities)
            while len(specials_button_text_list) < 4:
                specials_button_text_list.append("Empty")

   # def button_details(self, attack_or_special):
  #      if attack_or_special == "attack":


  #  def champion_turn_tick(self, champion_position):



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
        yes_buttonCNT = tk.Button(root, text="Yes", command=lambda: ParentClass.finalise_new_team1(self ,root))
        no_buttonCNT = tk.Button(root, text="No", command=lambda: root.destroy())
        confirmation_label.grid(row=2, column=1)
        yes_buttonCNT.grid(row=3, column=1, sticky="w", padx=70)
        no_buttonCNT.grid(row=3, column=1, sticky="e", padx=70)

    def save_new_team1(self, root):
        i = -1
        file = open("C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_championTeam_1.txt".format(computer_username),"r")
        file_allLines = file.readlines()
        user = ParentClass.get_user_encoded(self)
        user = str(user)
        for line in file_allLines:
            i += 1
            if user in line:
                coded_temp_party = self.code_party()
                new_line = "{}, {}\n".format(user, coded_temp_party)
                file_allLines[i] = new_line
                file_write = open("C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_championTeam_1.txt".format(computer_username),"w")
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
            if i <=4:
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
