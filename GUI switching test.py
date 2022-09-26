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
                LoginMenu, RegisterMenu, DungeonManagement, Team1SelectionPage, Team2SelectionPage, Team3SelectionPage):
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
        self.show_frame("CreateTeamPage")

    def cancel_new_team2(self):
        Team2SelectionPage.clear_temp_party2(self)
        self.show_frame("CreateTeamPage")

    def finalise_new_team2(self, root):
        Team2SelectionPage.save_new_team2(self, root)
        self.show_frame("CreateTeamPage")

    def cancel_new_team3(self):
        Team3SelectionPage.clear_temp_party3(self)
        self.show_frame("CreateTeamPage")

    def finalise_new_team3(self, root):
        Team3SelectionPage.save_new_team3(self, root)
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
                    if character == Monk.code:
                        decoded_dungeoneer_team1.append(Monk.title)
                    if character == Barbarian.code:
                        decoded_dungeoneer_team1.append(Barbarian.title)
                    if character == Veteran_Bodyguard.code:
                        decoded_dungeoneer_team1.append(Veteran_Bodyguard.title)
                    if character == Master_Fencer.code:
                        decoded_dungeoneer_team1.append(Master_Fencer.title)
                    if character == Berserker.code:
                        decoded_dungeoneer_team1.append(Berserker.title)
                    if character == Rogue.code:
                        decoded_dungeoneer_team1.append(Rogue.title)
                    if character == Survivalist.code:
                        decoded_dungeoneer_team1.append(Survivalist.title)
                    if character == Brawlist.code:
                        decoded_dungeoneer_team1.append(Brawlist.title)
                    if character == Academic_Mage.code:
                        decoded_dungeoneer_team1.append(Academic_Mage.title)
                    if character == Druid.code:
                        decoded_dungeoneer_team1.append(Druid.title)
                    if character == Warlock.code:
                        decoded_dungeoneer_team1.append(Warlock.title)
                    if character == Bloodmancer.code:
                        decoded_dungeoneer_team1.append(Bloodmancer.title)
                    if character == Paladin.code:
                        decoded_dungeoneer_team1.append(Paladin.title)
                    if character == Castle_Ranger.code:
                        decoded_dungeoneer_team1.append(Castle_Ranger.title)
                    if character == Thunder_Apprentice.code:
                        decoded_dungeoneer_team1.append(Thunder_Apprentice.title)
                    if character == Power_Conduit.code:
                        decoded_dungeoneer_team1.append(Power_Conduit.title)
                    if character == Earth_Speaker.code:
                        decoded_dungeoneer_team1.append(Earth_Speaker.title)
                    if character == Priest_of_the_Devoted.code:
                        decoded_dungeoneer_team1.append(Priest_of_the_Devoted.title)
                    if character == Time_Walker.code:
                        decoded_dungeoneer_team1.append(Time_Walker.title)
                    if character == Child_of_Medicine.code:
                        decoded_dungeoneer_team1.append(Child_of_Medicine.title)
                    if not character:
                        break
            else:
                for character in team_1_list_data:
                    if character == Monk.code:
                        decoded_dungeoneer_team1.append(Monk.title)
                    if character == Barbarian.code:
                        decoded_dungeoneer_team1.append(Barbarian.title)
                    if character == Veteran_Bodyguard.code:
                        decoded_dungeoneer_team1.append(Veteran_Bodyguard.title)
                    if character == Master_Fencer.code:
                        decoded_dungeoneer_team1.append(Master_Fencer.title)
                    if character == Berserker.code:
                        decoded_dungeoneer_team1.append(Berserker.title)
                    if character == Rogue.code:
                        decoded_dungeoneer_team1.append(Rogue.title)
                    if character == Survivalist.code:
                        decoded_dungeoneer_team1.append(Survivalist.title)
                    if character == Brawlist.code:
                        decoded_dungeoneer_team1.append(Brawlist.title)
                    if character == Academic_Mage.code:
                        decoded_dungeoneer_team1.append(Academic_Mage.title)
                    if character == Druid.code:
                        decoded_dungeoneer_team1.append(Druid.title)
                    if character == Warlock.code:
                        decoded_dungeoneer_team1.append(Warlock.title)
                    if character == Bloodmancer.code:
                        decoded_dungeoneer_team1.append(Bloodmancer.title)
                    if character == Paladin.code:
                        decoded_dungeoneer_team1.append(Paladin.title)
                    if character == Castle_Ranger.code:
                        decoded_dungeoneer_team1.append(Castle_Ranger.title)
                    if character == Thunder_Apprentice.code:
                        decoded_dungeoneer_team1.append(Thunder_Apprentice.title)
                    if character == Power_Conduit.code:
                        decoded_dungeoneer_team1.append(Power_Conduit.title)
                    if character == Earth_Speaker.code:
                        decoded_dungeoneer_team1.append(Earth_Speaker.title)
                    if character == Priest_of_the_Devoted.code:
                        decoded_dungeoneer_team1.append(Priest_of_the_Devoted.title)
                    if character == Time_Walker.code:
                        decoded_dungeoneer_team1.append(Time_Walker.title)
                    if character == Child_of_Medicine.code:
                        decoded_dungeoneer_team1.append(Child_of_Medicine.title)
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
                    if character == Monk.code:
                        decoded_dungeoneer_team2.append(Monk.title)
                    if character == Barbarian.code:
                        decoded_dungeoneer_team2.append(Barbarian.title)
                    if character == Veteran_Bodyguard.code:
                        decoded_dungeoneer_team2.append(Veteran_Bodyguard.title)
                    if character == Master_Fencer.code:
                        decoded_dungeoneer_team2.append(Master_Fencer.title)
                    if character == Berserker.code:
                        decoded_dungeoneer_team2.append(Berserker.title)
                    if character == Rogue.code:
                        decoded_dungeoneer_team2.append(Rogue.title)
                    if character == Survivalist.code:
                        decoded_dungeoneer_team2.append(Survivalist.title)
                    if character == Brawlist.code:
                        decoded_dungeoneer_team2.append(Brawlist.title)
                    if character == Academic_Mage.code:
                        decoded_dungeoneer_team2.append(Academic_Mage.title)
                    if character == Druid.code:
                        decoded_dungeoneer_team2.append(Druid.title)
                    if character == Warlock.code:
                        decoded_dungeoneer_team2.append(Warlock.title)
                    if character == Bloodmancer.code:
                        decoded_dungeoneer_team2.append(Bloodmancer.title)
                    if character == Paladin.code:
                        decoded_dungeoneer_team2.append(Paladin.title)
                    if character == Castle_Ranger.code:
                        decoded_dungeoneer_team2.append(Castle_Ranger.title)
                    if character == Thunder_Apprentice.code:
                        decoded_dungeoneer_team2.append(Thunder_Apprentice.title)
                    if character == Power_Conduit.code:
                        decoded_dungeoneer_team2.append(Power_Conduit.title)
                    if character == Earth_Speaker.code:
                        decoded_dungeoneer_team2.append(Earth_Speaker.title)
                    if character == Priest_of_the_Devoted.code:
                        decoded_dungeoneer_team2.append(Priest_of_the_Devoted.title)
                    if character == Time_Walker.code:
                        decoded_dungeoneer_team2.append(Time_Walker.title)
                    if character == Child_of_Medicine.code:
                        decoded_dungeoneer_team2.append(Child_of_Medicine.title)
                    if not character:
                        break
            else:
                for character in team_2_list_data:
                    if character == Monk.code:
                        decoded_dungeoneer_team2.append(Monk.title)
                    if character == Barbarian.code:
                        decoded_dungeoneer_team2.append(Barbarian.title)
                    if character == Veteran_Bodyguard.code:
                        decoded_dungeoneer_team2.append(Veteran_Bodyguard.title)
                    if character == Master_Fencer.code:
                        decoded_dungeoneer_team2.append(Master_Fencer.title)
                    if character == Berserker.code:
                        decoded_dungeoneer_team2.append(Berserker.title)
                    if character == Rogue.code:
                        decoded_dungeoneer_team2.append(Rogue.title)
                    if character == Survivalist.code:
                        decoded_dungeoneer_team2.append(Survivalist.title)
                    if character == Brawlist.code:
                        decoded_dungeoneer_team2.append(Brawlist.title)
                    if character == Academic_Mage.code:
                        decoded_dungeoneer_team2.append(Academic_Mage.title)
                    if character == Druid.code:
                        decoded_dungeoneer_team2.append(Druid.title)
                    if character == Warlock.code:
                        decoded_dungeoneer_team2.append(Warlock.title)
                    if character == Bloodmancer.code:
                        decoded_dungeoneer_team2.append(Bloodmancer.title)
                    if character == Paladin.code:
                        decoded_dungeoneer_team2.append(Paladin.title)
                    if character == Castle_Ranger.code:
                        decoded_dungeoneer_team2.append(Castle_Ranger.title)
                    if character == Thunder_Apprentice.code:
                        decoded_dungeoneer_team2.append(Thunder_Apprentice.title)
                    if character == Power_Conduit.code:
                        decoded_dungeoneer_team2.append(Power_Conduit.title)
                    if character == Earth_Speaker.code:
                        decoded_dungeoneer_team2.append(Earth_Speaker.title)
                    if character == Priest_of_the_Devoted.code:
                        decoded_dungeoneer_team2.append(Priest_of_the_Devoted.title)
                    if character == Time_Walker.code:
                        decoded_dungeoneer_team2.append(Time_Walker.title)
                    if character == Child_of_Medicine.code:
                        decoded_dungeoneer_team2.append(Child_of_Medicine.title)
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
                    if character == Monk.code:
                        decoded_dungeoneer_team3.append(Monk.title)
                    if character == Barbarian.code:
                        decoded_dungeoneer_team3.append(Barbarian.title)
                    if character == Veteran_Bodyguard.code:
                        decoded_dungeoneer_team3.append(Veteran_Bodyguard.title)
                    if character == Master_Fencer.code:
                        decoded_dungeoneer_team3.append(Master_Fencer.title)
                    if character == Berserker.code:
                        decoded_dungeoneer_team3.append(Berserker.title)
                    if character == Rogue.code:
                        decoded_dungeoneer_team3.append(Rogue.title)
                    if character == Survivalist.code:
                        decoded_dungeoneer_team3.append(Survivalist.title)
                    if character == Brawlist.code:
                        decoded_dungeoneer_team3.append(Brawlist.title)
                    if character == Academic_Mage.code:
                        decoded_dungeoneer_team3.append(Academic_Mage.title)
                    if character == Druid.code:
                        decoded_dungeoneer_team3.append(Druid.title)
                    if character == Warlock.code:
                        decoded_dungeoneer_team3.append(Warlock.title)
                    if character == Bloodmancer.code:
                        decoded_dungeoneer_team3.append(Bloodmancer.title)
                    if character == Paladin.code:
                        decoded_dungeoneer_team3.append(Paladin.title)
                    if character == Castle_Ranger.code:
                        decoded_dungeoneer_team3.append(Castle_Ranger.title)
                    if character == Thunder_Apprentice.code:
                        decoded_dungeoneer_team3.append(Thunder_Apprentice.title)
                    if character == Power_Conduit.code:
                        decoded_dungeoneer_team3.append(Power_Conduit.title)
                    if character == Earth_Speaker.code:
                        decoded_dungeoneer_team3.append(Earth_Speaker.title)
                    if character == Priest_of_the_Devoted.code:
                        decoded_dungeoneer_team3.append(Priest_of_the_Devoted.title)
                    if character == Time_Walker.code:
                        decoded_dungeoneer_team3.append(Time_Walker.title)
                    if character == Child_of_Medicine.code:
                        decoded_dungeoneer_team3.append(Child_of_Medicine.title)
                    if not character:
                        break
            else:
                for character in team_3_list_data:
                    if character == Monk.code:
                        decoded_dungeoneer_team3.append(Monk.title)
                    if character == Barbarian.code:
                        decoded_dungeoneer_team3.append(Barbarian.title)
                    if character == Veteran_Bodyguard.code:
                        decoded_dungeoneer_team3.append(Veteran_Bodyguard.title)
                    if character == Master_Fencer.code:
                        decoded_dungeoneer_team3.append(Master_Fencer.title)
                    if character == Berserker.code:
                        decoded_dungeoneer_team3.append(Berserker.title)
                    if character == Rogue.code:
                        decoded_dungeoneer_team3.append(Rogue.title)
                    if character == Survivalist.code:
                        decoded_dungeoneer_team3.append(Survivalist.title)
                    if character == Brawlist.code:
                        decoded_dungeoneer_team3.append(Brawlist.title)
                    if character == Academic_Mage.code:
                        decoded_dungeoneer_team3.append(Academic_Mage.title)
                    if character == Druid.code:
                        decoded_dungeoneer_team3.append(Druid.title)
                    if character == Warlock.code:
                        decoded_dungeoneer_team3.append(Warlock.title)
                    if character == Bloodmancer.code:
                        decoded_dungeoneer_team3.append(Bloodmancer.title)
                    if character == Paladin.code:
                        decoded_dungeoneer_team3.append(Paladin.title)
                    if character == Castle_Ranger.code:
                        decoded_dungeoneer_team3.append(Castle_Ranger.title)
                    if character == Thunder_Apprentice.code:
                        decoded_dungeoneer_team3.append(Thunder_Apprentice.title)
                    if character == Power_Conduit.code:
                        decoded_dungeoneer_team3.append(Power_Conduit.title)
                    if character == Earth_Speaker.code:
                        decoded_dungeoneer_team3.append(Earth_Speaker.title)
                    if character == Priest_of_the_Devoted.code:
                        decoded_dungeoneer_team3.append(Priest_of_the_Devoted.title)
                    if character == Time_Walker.code:
                        decoded_dungeoneer_team3.append(Time_Walker.title)
                    if character == Child_of_Medicine.code:
                        decoded_dungeoneer_team3.append(Child_of_Medicine.title)
                return decoded_dungeoneer_team3
        if len(decoded_dungeoneer_team3) < 5:
            while len(decoded_dungeoneer_team3) < 5:
                decoded_dungeoneer_team3.append(".")
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
        user = SampleApp.get_user_encoded(self)
        team_line_1 = []
        team_line_1 = SampleApp.return_users_champion_team1(self, user)
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
        global monk_label, monk_button_add, monk_button_details, barbarian_label, barbarian_button_add, \
            barbarian_button_details, bodyguard_label, bodyguard_button_add, bodyguard_button_details, \
            fencer_label, fencer_button_add, fencer_button_details, invis_label3, invis_label4, tank, dps, healer
        if tank == True:
            return
        else:
            if dps == True:
                berserker_label.destroy()
                berserker_button_add.destroy()
                berserker_button_details.destroy()
                rogue_label.destroy()
                rogue_button_add.destroy()
                rogue_button_details.destroy()
                survivalist_label.destroy()
                survivalist_button_add.destroy()
                survivalist_button_details.destroy()
                brawlist_label.destroy()
                brawlist_button_add.destroy()
                brawlist_button_details.destroy()
                academic_mage_label.destroy()
                academic_mage_button_add.destroy()
                academic_mage_button_details.destroy()
                jungle_druid_label.destroy()
                jungle_druid_button_add.destroy()
                jungle_druid_button_details.destroy()
                warlock_label.destroy()
                warlock_button_add.destroy()
                warlock_button_details.destroy()
                bloodmancer_label.destroy()
                bloodmancer_button_add.destroy()
                bloodmancer_button_details.destroy()
                paladin_label.destroy()
                paladin_button_add.destroy()
                paladin_button_details.destroy()
                castle_ranger_label.destroy()
                castle_ranger_button_add.destroy()
                castle_ranger_button_details.destroy()
                thunder_apprentice_label.destroy()
                thunder_apprentice_button_add.destroy()
                thunder_apprentice_button_details.destroy()
                power_conduit_label.destroy()
                power_conduit_button_add.destroy()
                power_conduit_button_details.destroy()
                melee_label.destroy()
                magic_label.destroy()
                mix_label.destroy()
                dps = False
            else:
                dps = False
            if healer == True:
                earth_speaker_label.destroy()
                earth_speaker_button_add.destroy()
                earth_speaker_button_details.destroy()
                priest_of_the_devoted_label.destroy()
                priest_of_the_devoted_button_add.destroy()
                priest_of_the_devoted_button_details.destroy()
                time_walker_label.destroy()
                time_walker_button_add.destroy()
                time_walker_button_details.destroy()
                child_of_medicine_label.destroy()
                child_of_medicine_button_add.destroy()
                child_of_medicine_button_details.destroy()
                invis_label3.destroy()
                invis_label4.destroy()
                healer = False
            else:
                healer = False
            tank = True
            invis_label3 = tk.Label(self)
            invis_label4 = tk.Label(self)
            monk_label = tk.Label(self, text=Monk.name, font=self.menu_button_font)
            monk_button_add = tk.Button(self, text="Add to Team",
                                        command=lambda: self.check_temp_party1(Monk.title, "tank"))
            monk_button_details = tk.Button(self, text="View Details")
            barbarian_label = tk.Label(self, text=Barbarian.name, font=self.menu_button_font)
            barbarian_button_add = tk.Button(self, text="Add to Team",
                                             command=lambda: self.check_temp_party1(Barbarian.title, "tank"))
            barbarian_button_details = tk.Button(self, text="View Details")
            bodyguard_label = tk.Label(self, text=Veteran_Bodyguard.name, font=self.menu_button_font)
            bodyguard_button_add = tk.Button(self, text="Add to Team",
                                             command=lambda: self.check_temp_party1(Veteran_Bodyguard.title, "tank"))
            bodyguard_button_details = tk.Button(self, text="View Details")
            fencer_label = tk.Label(self, text=Master_Fencer.name, font=self.menu_button_font)
            fencer_button_add = tk.Button(self, text="Add to Team",
                                          command=lambda: self.check_temp_party1(Master_Fencer.title, "tank"))
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

    def view_dps1(self):
        global melee_label, magic_label, mix_label, berserker_label, berserker_button_add, berserker_button_details, \
            rogue_label, rogue_button_add, rogue_button_details, survivalist_label, survivalist_button_add, survivalist_button_details, \
            brawlist_label, brawlist_button_add, brawlist_button_details, academic_mage_label, academic_mage_button_add, academic_mage_button_details, \
            jungle_druid_label, jungle_druid_button_add, jungle_druid_button_details, warlock_label, warlock_button_add, warlock_button_details, \
            bloodmancer_label, bloodmancer_button_add, bloodmancer_button_details, paladin_label, paladin_button_add, paladin_button_details, \
            castle_ranger_label, castle_ranger_button_add, castle_ranger_button_details, thunder_apprentice_label, thunder_apprentice_button_add, thunder_apprentice_button_details, \
            power_conduit_label, power_conduit_button_add, power_conduit_button_details, tank, dps, healer
        if dps == True:
            return
        else:
            if tank == True:
                monk_label.destroy()
                monk_button_add.destroy()
                monk_button_details.destroy()
                barbarian_label.destroy()
                barbarian_button_add.destroy()
                barbarian_button_details.destroy()
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
                earth_speaker_label.destroy()
                earth_speaker_button_add.destroy()
                earth_speaker_button_details.destroy()
                priest_of_the_devoted_label.destroy()
                priest_of_the_devoted_button_add.destroy()
                priest_of_the_devoted_button_details.destroy()
                time_walker_label.destroy()
                time_walker_button_add.destroy()
                time_walker_button_details.destroy()
                child_of_medicine_label.destroy()
                child_of_medicine_button_add.destroy()
                child_of_medicine_button_details.destroy()
                invis_label3.destroy()
                invis_label4.destroy()
                healer = False
            else:
                healer = False
            dps = True
            melee_label = tk.Label(self, text=":Melee:", font=self.menu_button_font)
            magic_label = tk.Label(self, text=":Magic:", font=self.menu_button_font)
            mix_label = tk.Label(self, text=":Other:", font=self.menu_button_font)
            berserker_label = tk.Label(self, text=Berserker.name)
            berserker_button_add = tk.Button(self, text="Add to Team",
                                             command=lambda: self.check_temp_party1(Berserker.title, "melee"))
            berserker_button_details = tk.Button(self, text="View Details")
            rogue_label = tk.Label(self, text=Rogue.name)
            rogue_button_add = tk.Button(self, text="Add to Team",
                                         command=lambda: self.check_temp_party1(Rogue.title, "melee"))
            rogue_button_details = tk.Button(self, text="View Details")
            survivalist_label = tk.Label(self, text=Survivalist.name)
            survivalist_button_add = tk.Button(self, text="Add to Team",
                                               command=lambda: self.check_temp_party1(Survivalist.title, "melee"))
            survivalist_button_details = tk.Button(self, text="View Details")
            brawlist_label = tk.Label(self, text=Brawlist.name)
            brawlist_button_add = tk.Button(self, text="Add to Team",
                                            command=lambda: self.check_temp_party1(Brawlist.title, "melee"))
            brawlist_button_details = tk.Button(self, text="View Details")
            academic_mage_label = tk.Label(self, text=Academic_Mage.name)
            academic_mage_button_add = tk.Button(self, text="Add to Team",
                                                 command=lambda: self.check_temp_party1(Academic_Mage.title, "magic"))
            academic_mage_button_details = tk.Button(self, text="View Details")
            jungle_druid_label = tk.Label(self, text=Druid.name)
            jungle_druid_button_add = tk.Button(self, text="Add to Team",
                                                command=lambda: self.check_temp_party1(Druid.title, "magic"))
            jungle_druid_button_details = tk.Button(self, text="View Details")
            warlock_label = tk.Label(self, text=Warlock.name)
            warlock_button_add = tk.Button(self, text="Add to Team",
                                           command=lambda: self.check_temp_party1(Warlock.title, "magic"))
            warlock_button_details = tk.Button(self, text="View Details")
            bloodmancer_label = tk.Label(self, text=Bloodmancer.name)
            bloodmancer_button_add = tk.Button(self, text="Add to Team",
                                               command=lambda: self.check_temp_party1(Bloodmancer.title, "magic"))
            bloodmancer_button_details = tk.Button(self, text="View Details")
            paladin_label = tk.Label(self, text=Paladin.name)
            paladin_button_add = tk.Button(self, text="Add to Team",
                                           command=lambda: self.check_temp_party1(Paladin.title, "mixed"))
            paladin_button_details = tk.Button(self, text="View Details")
            castle_ranger_label = tk.Label(self, text=Castle_Ranger.name)
            castle_ranger_button_add = tk.Button(self, text="Add to Team",
                                                 command=lambda: self.check_temp_party1(Castle_Ranger.title, "mixed"))
            castle_ranger_button_details = tk.Button(self, text="View Details")
            thunder_apprentice_label = tk.Label(self, text=Thunder_Apprentice.name)
            thunder_apprentice_button_add = tk.Button(self, text="Add to Team",
                                                      command=lambda: self.check_temp_party1(Thunder_Apprentice.title,
                                                                                            "mixed"))
            thunder_apprentice_button_details = tk.Button(self, text="View Details")
            power_conduit_label = tk.Label(self, text=Power_Conduit.name)
            power_conduit_button_add = tk.Button(self, text="Add to Team",
                                                 command=lambda: self.check_temp_party1(Power_Conduit.title, "mixed"))
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

    def view_healer1(self):
        global earth_speaker_label, earth_speaker_button_add, earth_speaker_button_details, priest_of_the_devoted_label, priest_of_the_devoted_button_add, \
            priest_of_the_devoted_button_details, time_walker_label, time_walker_button_add, time_walker_button_details, \
            child_of_medicine_label, child_of_medicine_button_add, child_of_medicine_button_details, invis_label3, invis_label4, tank, dps, healer
        if healer == True:
            return
        else:
            invis_label3 = tk.Label(self)
            invis_label4 = tk.Label(self)
            if tank == True:
                monk_label.destroy()
                monk_button_add.destroy()
                monk_button_details.destroy()
                barbarian_label.destroy()
                barbarian_button_add.destroy()
                barbarian_button_details.destroy()
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
                berserker_label.destroy()
                berserker_button_add.destroy()
                berserker_button_details.destroy()
                rogue_label.destroy()
                rogue_button_add.destroy()
                rogue_button_details.destroy()
                survivalist_label.destroy()
                survivalist_button_add.destroy()
                survivalist_button_details.destroy()
                brawlist_label.destroy()
                brawlist_button_add.destroy()
                brawlist_button_details.destroy()
                academic_mage_label.destroy()
                academic_mage_button_add.destroy()
                academic_mage_button_details.destroy()
                jungle_druid_label.destroy()
                jungle_druid_button_add.destroy()
                jungle_druid_button_details.destroy()
                warlock_label.destroy()
                warlock_button_add.destroy()
                warlock_button_details.destroy()
                bloodmancer_label.destroy()
                bloodmancer_button_add.destroy()
                bloodmancer_button_details.destroy()
                paladin_label.destroy()
                paladin_button_add.destroy()
                paladin_button_details.destroy()
                castle_ranger_label.destroy()
                castle_ranger_button_add.destroy()
                castle_ranger_button_details.destroy()
                thunder_apprentice_label.destroy()
                thunder_apprentice_button_add.destroy()
                thunder_apprentice_button_details.destroy()
                power_conduit_label.destroy()
                power_conduit_button_add.destroy()
                power_conduit_button_details.destroy()
                melee_label.destroy()
                magic_label.destroy()
                mix_label.destroy()
                dps = False
            else:
                dps = False
            healer = True
            earth_speaker_label = tk.Label(self, text=Earth_Speaker.name, font=self.menu_button_font)
            earth_speaker_button_add = tk.Button(self, text="Add to Team",
                                                 command=lambda: self.check_temp_party1(Earth_Speaker.title, "healer"))
            earth_speaker_button_details = tk.Button(self, text="View Details")
            priest_of_the_devoted_label = tk.Label(self, text=Priest_of_the_Devoted.name, font=self.menu_button_font)
            priest_of_the_devoted_button_add = tk.Button(self, text="Add to Team",
                                                         command=lambda: self.check_temp_party1(
                                                             Priest_of_the_Devoted.title, "healer"))
            priest_of_the_devoted_button_details = tk.Button(self, text="View Details")
            time_walker_label = tk.Label(self, text=Time_Walker.name, font=self.menu_button_font)
            time_walker_button_add = tk.Button(self, text="Add to Team",
                                               command=lambda: self.check_temp_party1(Time_Walker.title, "healer"))
            time_walker_button_details = tk.Button(self, text="View Details")
            child_of_medicine_label = tk.Label(self, text=Child_of_Medicine.name, font=self.menu_button_font)
            child_of_medicine_button_add = tk.Button(self, text="Add to Team",
                                                     command=lambda: self.check_temp_party1(Child_of_Medicine.title,
                                                                                           "healer"))
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

    def check_temp_party1(self, champion, type):
        global temp_party, yes_buttonCTP, no_buttonCTP, warning_label1CTP, warning_label2CTP, tank, dps, healer, visual_team_label
        tank_temp_party = []
        melee_temp_party = []
        magic_temp_party = []
        mixed_temp_party = []
        healer_temp_party = []
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
                    if character == Monk.title:
                        tank_temp_party.append(character)
                    if character == Barbarian.title:
                        tank_temp_party.append(character)
                    if character == Veteran_Bodyguard.title:
                        tank_temp_party.append(character)
                    if character == Master_Fencer.title:
                        tank_temp_party.append(character)
                    if character == Berserker.title:
                        melee_temp_party.append(character)
                    if character == Rogue.title:
                        melee_temp_party.append(character)
                    if character == Survivalist.title:
                        melee_temp_party.append(character)
                    if character == Brawlist.title:
                        melee_temp_party.append(character)
                    if character == Academic_Mage.title:
                        magic_temp_party.append(character)
                    if character == Druid.title:
                        magic_temp_party.append(character)
                    if character == Warlock.title:
                        magic_temp_party.append(character)
                    if character == Bloodmancer.title:
                        magic_temp_party.append(character)
                    if character == Paladin.title:
                        mixed_temp_party.append(character)
                    if character == Castle_Ranger.title:
                        mixed_temp_party.append(character)
                    if character == Thunder_Apprentice.title:
                        mixed_temp_party.append(character)
                    if character == Power_Conduit.title:
                        mixed_temp_party.append(character)
                    if character == Earth_Speaker.title:
                        healer_temp_party.append(character)
                    if character == Priest_of_the_Devoted.title:
                        healer_temp_party.append(character)
                    if character == Time_Walker.title:
                        healer_temp_party.append(character)
                    if character == Child_of_Medicine.title:
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
            if character == Monk.title:
                tank_temp_party.append(character)
            if character == Barbarian.title:
                tank_temp_party.append(character)
            if character == Veteran_Bodyguard.title:
                tank_temp_party.append(character)
            if character == Master_Fencer.title:
                tank_temp_party.append(character)
            if character == Berserker.title:
                melee_temp_party.append(character)
            if character == Rogue.title:
                melee_temp_party.append(character)
            if character == Survivalist.title:
                melee_temp_party.append(character)
            if character == Brawlist.title:
                melee_temp_party.append(character)
            if character == Academic_Mage.title:
                magic_temp_party.append(character)
            if character == Druid.title:
                magic_temp_party.append(character)
            if character == Warlock.title:
                magic_temp_party.append(character)
            if character == Bloodmancer.title:
                magic_temp_party.append(character)
            if character == Paladin.title:
                mixed_temp_party.append(character)
            if character == Castle_Ranger.title:
                mixed_temp_party.append(character)
            if character == Thunder_Apprentice.title:
                mixed_temp_party.append(character)
            if character == Power_Conduit.title:
                mixed_temp_party.append(character)
            if character == Earth_Speaker.title:
                healer_temp_party.append(character)
            if character == Priest_of_the_Devoted.title:
                healer_temp_party.append(character)
            if character == Time_Walker.title:
                healer_temp_party.append(character)
            if character == Child_of_Medicine.title:
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
        yes_buttonCNT = tk.Button(root, text="Yes", command=lambda: SampleApp.finalise_new_team1(self, root))
        no_buttonCNT = tk.Button(root, text="No", command=lambda: root.destroy())
        confirmation_label.grid(row=2, column=1)
        yes_buttonCNT.grid(row=3, column=1, sticky="w", padx=70)
        no_buttonCNT.grid(row=3, column=1, sticky="e", padx=70)

    def save_new_team1(self, root):
        i = -1
        file = open("C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_championTeam_1.txt".format(computer_username),"r")
        file_allLines = file.readlines()
        user = SampleApp.get_user_encoded(self)
        user = str(user)
        for line in file_allLines:
            i += 1
            if user in line:
                coded_temp_party = self.code_party()
                new_line = "{} {}".format(line, coded_temp_party)
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
            if character == Monk.title:
                coded_temp_party += Monk.code
            if character == Barbarian.title:
                coded_temp_party += Barbarian.code
            if character == Veteran_Bodyguard.title:
                coded_temp_party += Veteran_Bodyguard.code
            if character == Master_Fencer.title:
                coded_temp_party += Master_Fencer.code
            if character == Berserker.title:
                coded_temp_party += Berserker.code
            if character == Rogue.title:
                coded_temp_party += Rogue.code
            if character == Survivalist.title:
                coded_temp_party += Survivalist.code
            if character == Brawlist.title:
                coded_temp_party += Brawlist.code
            if character == Academic_Mage.title:
                coded_temp_party += Academic_Mage.code
            if character == Druid.title:
                coded_temp_party += Druid.code
            if character == Warlock.title:
                coded_temp_party += Warlock.code
            if character == Bloodmancer.title:
                coded_temp_party += Bloodmancer.code
            if character == Paladin.title:
                coded_temp_party += Paladin.code
            if character == Castle_Ranger.title:
                coded_temp_party += Castle_Ranger.code
            if character == Thunder_Apprentice.title:
                coded_temp_party += Thunder_Apprentice.code
            if character == Power_Conduit.title:
                coded_temp_party += Power_Conduit.code
            if character == Earth_Speaker.title:
                coded_temp_party += Earth_Speaker.code
            if character == Priest_of_the_Devoted.title:
                coded_temp_party += Priest_of_the_Devoted.code
            if character == Time_Walker.title:
                coded_temp_party += Time_Walker.code
            if character == Child_of_Medicine.title:
                coded_temp_party += Child_of_Medicine.code
            if character == "Empty":
                break
            i += 1
            if i <=4:
                coded_temp_party += ", "
        return coded_temp_party


    def clear_temp_party1(self):
        global temp_party
        temp_party = []


class Team2SelectionPage(tk.Frame):
    def __init__(self, parent, controller):
        global update_pageTSP
        global returnButtonTSP, invis_label1, invis_label2
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.menu_button_font = tkfont.Font(family='Helvetica', size=18, weight="bold")
        self.title_label_font = tkfont.Font(family='Helvetica', size=30, weight="bold")
        self.small_label_font = tkfont.Font(family='Helvetica', size=12, weight="bold")
        title = tk.Label(self, text="Champion Camp", font=self.title_label_font)
        update_pageTSP = tk.Button(self, text="Begin Recruiting for Team 2", command=lambda: self.pitstop2(),
                                   font=controller.menu_button_font)
        returnButtonTSP = tk.Button(self, text="Cancel", command=lambda: controller.cancel_new_team2())
        invis_label1 = tk.Label(self)
        invis_label2 = tk.Label(self)
        update_pageTSP.grid(row=2, column=2, pady=50)
        title.grid(row=1, column=2)
        returnButtonTSP.grid(row=13, column=2)
        invis_label1.grid(row=1, column=1, rowspan=4, pady=50, ipadx=240, ipady=100)
        invis_label2.grid(row=1, column=2, pady=100)

    def pitstop2(self):
        global visual_team_label, temp_party
        user = SampleApp.get_user_encoded(self)
        team_line_2 = []
        team_line_2 = SampleApp.return_users_champion_team2(self, user)
        team_line_2 = team_line_2.replace(",", "")
        team_2_list_data = team_line_2.split()
        CTP = CreateTeamPage
        decoded_dungeoneer_team2CTP = CTP.team_2_decode(self, team_2_list_data)
        temp_party = decoded_dungeoneer_team2CTP
        visual_team_label = tk.Label(self, text=self.display_team2(temp_party))
        visual_team_label.grid(row=11, column=2)
        self.team_creation2()

    def team_creation2(self):
        global tank, dps, healer, tank_section_button, dps_section_button, healer_section_button, decoded_dungeoneer_team2CTP
        tank = False
        dps = False
        healer = False
        invis_label3 = tk.Label(self)
        invis_label4 = tk.Label(self)
        tank_section_button = tk.Button(self, text="Tanks", font=self.menu_button_font, width=26,
                                        command=self.view_tanks2)
        dps_section_button = tk.Button(self, text="Damage Dealers", font=self.menu_button_font, width=26,
                                       command=self.view_dps2)
        healer_section_button = tk.Button(self, text="Healers", font=self.menu_button_font, width=26,
                                          command=self.view_healer2)
        your_team_label = tk.Label(self, text=":Your Team:", font=self.small_label_font)
        confirm_changes_button = tk.Button(self, text="Confirm Changes", command=self.confirm_new_team2)
        tank_section_button.grid(row=2, column=2)
        dps_section_button.grid(row=2, column=1, padx=25)
        healer_section_button.grid(row=2, column=3)
        invis_label3.grid(row=2, column=0, padx=6)
        invis_label4.grid(row=9, column=2, pady=45)
        your_team_label.grid(row=10, column=2)
        confirm_changes_button.grid(row=12, column=2)
        invis_label1.grid_forget()
        invis_label2.grid_forget()
        update_pageTSP.grid_forget()

    def display_team2(self, temp_party):
        team_2_text = ""
        i = 0
        for character in temp_party:
            if i == 3:
                team_2_text += "\n"
            team_2_text += "["
            team_2_text += character
            team_2_text += "]"
            i += 1
        if i != 5:
            while i < 5:
                team_2_text += "["
                team_2_text += "Empty"
                team_2_text += "]"
                i += 1
        return team_2_text

    def view_tanks2(self):
        global monk_label, monk_button_add, monk_button_details, barbarian_label, barbarian_button_add, \
            barbarian_button_details, bodyguard_label, bodyguard_button_add, bodyguard_button_details, \
            fencer_label, fencer_button_add, fencer_button_details, invis_label3, invis_label4, tank, dps, healer
        if tank == True:
            return
        else:
            if dps == True:
                berserker_label.destroy()
                berserker_button_add.destroy()
                berserker_button_details.destroy()
                rogue_label.destroy()
                rogue_button_add.destroy()
                rogue_button_details.destroy()
                survivalist_label.destroy()
                survivalist_button_add.destroy()
                survivalist_button_details.destroy()
                brawlist_label.destroy()
                brawlist_button_add.destroy()
                brawlist_button_details.destroy()
                academic_mage_label.destroy()
                academic_mage_button_add.destroy()
                academic_mage_button_details.destroy()
                jungle_druid_label.destroy()
                jungle_druid_button_add.destroy()
                jungle_druid_button_details.destroy()
                warlock_label.destroy()
                warlock_button_add.destroy()
                warlock_button_details.destroy()
                bloodmancer_label.destroy()
                bloodmancer_button_add.destroy()
                bloodmancer_button_details.destroy()
                paladin_label.destroy()
                paladin_button_add.destroy()
                paladin_button_details.destroy()
                castle_ranger_label.destroy()
                castle_ranger_button_add.destroy()
                castle_ranger_button_details.destroy()
                thunder_apprentice_label.destroy()
                thunder_apprentice_button_add.destroy()
                thunder_apprentice_button_details.destroy()
                power_conduit_label.destroy()
                power_conduit_button_add.destroy()
                power_conduit_button_details.destroy()
                melee_label.destroy()
                magic_label.destroy()
                mix_label.destroy()
                dps = False
            else:
                dps = False
            if healer == True:
                earth_speaker_label.destroy()
                earth_speaker_button_add.destroy()
                earth_speaker_button_details.destroy()
                priest_of_the_devoted_label.destroy()
                priest_of_the_devoted_button_add.destroy()
                priest_of_the_devoted_button_details.destroy()
                time_walker_label.destroy()
                time_walker_button_add.destroy()
                time_walker_button_details.destroy()
                child_of_medicine_label.destroy()
                child_of_medicine_button_add.destroy()
                child_of_medicine_button_details.destroy()
                invis_label3.destroy()
                invis_label4.destroy()
                healer = False
            else:
                healer = False
            tank = True
            invis_label3 = tk.Label(self)
            invis_label4 = tk.Label(self)
            monk_label = tk.Label(self, text=Monk.name, font=self.menu_button_font)
            monk_button_add = tk.Button(self, text="Add to Team",
                                        command=lambda: self.check_temp_party2(Monk.title, "tank"))
            monk_button_details = tk.Button(self, text="View Details")
            barbarian_label = tk.Label(self, text=Barbarian.name, font=self.menu_button_font)
            barbarian_button_add = tk.Button(self, text="Add to Team",
                                             command=lambda: self.check_temp_party2(Barbarian.title, "tank"))
            barbarian_button_details = tk.Button(self, text="View Details")
            bodyguard_label = tk.Label(self, text=Veteran_Bodyguard.name, font=self.menu_button_font)
            bodyguard_button_add = tk.Button(self, text="Add to Team",
                                             command=lambda: self.check_temp_party2(Veteran_Bodyguard.title, "tank"))
            bodyguard_button_details = tk.Button(self, text="View Details")
            fencer_label = tk.Label(self, text=Master_Fencer.name, font=self.menu_button_font)
            fencer_button_add = tk.Button(self, text="Add to Team",
                                          command=lambda: self.check_temp_party2(Master_Fencer.title, "tank"))
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

    def view_dps2(self):
        global melee_label, magic_label, mix_label, berserker_label, berserker_button_add, berserker_button_details, \
            rogue_label, rogue_button_add, rogue_button_details, survivalist_label, survivalist_button_add, survivalist_button_details, \
            brawlist_label, brawlist_button_add, brawlist_button_details, academic_mage_label, academic_mage_button_add, academic_mage_button_details, \
            jungle_druid_label, jungle_druid_button_add, jungle_druid_button_details, warlock_label, warlock_button_add, warlock_button_details, \
            bloodmancer_label, bloodmancer_button_add, bloodmancer_button_details, paladin_label, paladin_button_add, paladin_button_details, \
            castle_ranger_label, castle_ranger_button_add, castle_ranger_button_details, thunder_apprentice_label, thunder_apprentice_button_add, thunder_apprentice_button_details, \
            power_conduit_label, power_conduit_button_add, power_conduit_button_details, tank, dps, healer
        if dps == True:
            return
        else:
            if tank == True:
                monk_label.destroy()
                monk_button_add.destroy()
                monk_button_details.destroy()
                barbarian_label.destroy()
                barbarian_button_add.destroy()
                barbarian_button_details.destroy()
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
                earth_speaker_label.destroy()
                earth_speaker_button_add.destroy()
                earth_speaker_button_details.destroy()
                priest_of_the_devoted_label.destroy()
                priest_of_the_devoted_button_add.destroy()
                priest_of_the_devoted_button_details.destroy()
                time_walker_label.destroy()
                time_walker_button_add.destroy()
                time_walker_button_details.destroy()
                child_of_medicine_label.destroy()
                child_of_medicine_button_add.destroy()
                child_of_medicine_button_details.destroy()
                invis_label3.destroy()
                invis_label4.destroy()
                healer = False
            else:
                healer = False
            dps = True
            melee_label = tk.Label(self, text=":Melee:", font=self.menu_button_font)
            magic_label = tk.Label(self, text=":Magic:", font=self.menu_button_font)
            mix_label = tk.Label(self, text=":Other:", font=self.menu_button_font)
            berserker_label = tk.Label(self, text=Berserker.name)
            berserker_button_add = tk.Button(self, text="Add to Team",
                                             command=lambda: self.check_temp_party2(Berserker.title, "melee"))
            berserker_button_details = tk.Button(self, text="View Details")
            rogue_label = tk.Label(self, text=Rogue.name)
            rogue_button_add = tk.Button(self, text="Add to Team",
                                         command=lambda: self.check_temp_party2(Rogue.title, "melee"))
            rogue_button_details = tk.Button(self, text="View Details")
            survivalist_label = tk.Label(self, text=Survivalist.name)
            survivalist_button_add = tk.Button(self, text="Add to Team",
                                               command=lambda: self.check_temp_party2(Survivalist.title, "melee"))
            survivalist_button_details = tk.Button(self, text="View Details")
            brawlist_label = tk.Label(self, text=Brawlist.name)
            brawlist_button_add = tk.Button(self, text="Add to Team",
                                            command=lambda: self.check_temp_party2(Brawlist.title, "melee"))
            brawlist_button_details = tk.Button(self, text="View Details")
            academic_mage_label = tk.Label(self, text=Academic_Mage.name)
            academic_mage_button_add = tk.Button(self, text="Add to Team",
                                                 command=lambda: self.check_temp_party2(Academic_Mage.title, "magic"))
            academic_mage_button_details = tk.Button(self, text="View Details")
            jungle_druid_label = tk.Label(self, text=Druid.name)
            jungle_druid_button_add = tk.Button(self, text="Add to Team",
                                                command=lambda: self.check_temp_party2(Druid.title, "magic"))
            jungle_druid_button_details = tk.Button(self, text="View Details")
            warlock_label = tk.Label(self, text=Warlock.name)
            warlock_button_add = tk.Button(self, text="Add to Team",
                                           command=lambda: self.check_temp_party2(Warlock.title, "magic"))
            warlock_button_details = tk.Button(self, text="View Details")
            bloodmancer_label = tk.Label(self, text=Bloodmancer.name)
            bloodmancer_button_add = tk.Button(self, text="Add to Team",
                                               command=lambda: self.check_temp_party2(Bloodmancer.title, "magic"))
            bloodmancer_button_details = tk.Button(self, text="View Details")
            paladin_label = tk.Label(self, text=Paladin.name)
            paladin_button_add = tk.Button(self, text="Add to Team",
                                           command=lambda: self.check_temp_party2(Paladin.title, "mixed"))
            paladin_button_details = tk.Button(self, text="View Details")
            castle_ranger_label = tk.Label(self, text=Castle_Ranger.name)
            castle_ranger_button_add = tk.Button(self, text="Add to Team",
                                                 command=lambda: self.check_temp_party2(Castle_Ranger.title, "mixed"))
            castle_ranger_button_details = tk.Button(self, text="View Details")
            thunder_apprentice_label = tk.Label(self, text=Thunder_Apprentice.name)
            thunder_apprentice_button_add = tk.Button(self, text="Add to Team",
                                                      command=lambda: self.check_temp_party2(Thunder_Apprentice.title,
                                                                                            "mixed"))
            thunder_apprentice_button_details = tk.Button(self, text="View Details")
            power_conduit_label = tk.Label(self, text=Power_Conduit.name)
            power_conduit_button_add = tk.Button(self, text="Add to Team",
                                                 command=lambda: self.check_temp_party2(Power_Conduit.title, "mixed"))
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

    def view_healer2(self):
        global earth_speaker_label, earth_speaker_button_add, earth_speaker_button_details, priest_of_the_devoted_label, priest_of_the_devoted_button_add, \
            priest_of_the_devoted_button_details, time_walker_label, time_walker_button_add, time_walker_button_details, \
            child_of_medicine_label, child_of_medicine_button_add, child_of_medicine_button_details, invis_label3, invis_label4, tank, dps, healer
        if healer == True:
            return
        else:
            invis_label3 = tk.Label(self)
            invis_label4 = tk.Label(self)
            if tank == True:
                monk_label.destroy()
                monk_button_add.destroy()
                monk_button_details.destroy()
                barbarian_label.destroy()
                barbarian_button_add.destroy()
                barbarian_button_details.destroy()
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
                berserker_label.destroy()
                berserker_button_add.destroy()
                berserker_button_details.destroy()
                rogue_label.destroy()
                rogue_button_add.destroy()
                rogue_button_details.destroy()
                survivalist_label.destroy()
                survivalist_button_add.destroy()
                survivalist_button_details.destroy()
                brawlist_label.destroy()
                brawlist_button_add.destroy()
                brawlist_button_details.destroy()
                academic_mage_label.destroy()
                academic_mage_button_add.destroy()
                academic_mage_button_details.destroy()
                jungle_druid_label.destroy()
                jungle_druid_button_add.destroy()
                jungle_druid_button_details.destroy()
                warlock_label.destroy()
                warlock_button_add.destroy()
                warlock_button_details.destroy()
                bloodmancer_label.destroy()
                bloodmancer_button_add.destroy()
                bloodmancer_button_details.destroy()
                paladin_label.destroy()
                paladin_button_add.destroy()
                paladin_button_details.destroy()
                castle_ranger_label.destroy()
                castle_ranger_button_add.destroy()
                castle_ranger_button_details.destroy()
                thunder_apprentice_label.destroy()
                thunder_apprentice_button_add.destroy()
                thunder_apprentice_button_details.destroy()
                power_conduit_label.destroy()
                power_conduit_button_add.destroy()
                power_conduit_button_details.destroy()
                melee_label.destroy()
                magic_label.destroy()
                mix_label.destroy()
                dps = False
            else:
                dps = False
            healer = True
            earth_speaker_label = tk.Label(self, text=Earth_Speaker.name, font=self.menu_button_font)
            earth_speaker_button_add = tk.Button(self, text="Add to Team",
                                                 command=lambda: self.check_temp_party2(Earth_Speaker.title, "healer"))
            earth_speaker_button_details = tk.Button(self, text="View Details")
            priest_of_the_devoted_label = tk.Label(self, text=Priest_of_the_Devoted.name, font=self.menu_button_font)
            priest_of_the_devoted_button_add = tk.Button(self, text="Add to Team",
                                                         command=lambda: self.check_temp_party2(
                                                             Priest_of_the_Devoted.title, "healer"))
            priest_of_the_devoted_button_details = tk.Button(self, text="View Details")
            time_walker_label = tk.Label(self, text=Time_Walker.name, font=self.menu_button_font)
            time_walker_button_add = tk.Button(self, text="Add to Team",
                                               command=lambda: self.check_temp_party2(Time_Walker.title, "healer"))
            time_walker_button_details = tk.Button(self, text="View Details")
            child_of_medicine_label = tk.Label(self, text=Child_of_Medicine.name, font=self.menu_button_font)
            child_of_medicine_button_add = tk.Button(self, text="Add to Team",
                                                     command=lambda: self.check_temp_party2(Child_of_Medicine.title,
                                                                                           "healer"))
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

    def check_temp_party2(self, champion, type):
        global temp_party, yes_buttonCTP, no_buttonCTP, warning_label1CTP, warning_label2CTP, tank, dps, healer, visual_team_label
        tank_temp_party = []
        melee_temp_party = []
        magic_temp_party = []
        mixed_temp_party = []
        healer_temp_party = []
        if champion in temp_party:
            root = tk.Tk()
            warning_label = tk.Label(root, text="Sorry, but this character is already assigned in the party")
            ok_button = tk.Button(root, text="Ok", command=root.destroy)
            ok_button.grid(row=2, column=1)
            warning_label.grid(row=1, column=1)
            visual_team_label.destroy()
            visual_team_label = tk.Label(self, text=self.display_team2(temp_party))
            visual_team_label.grid(row=11, column=2)
        else:
            if len(temp_party) < 5:
                for character in temp_party:
                    if character == Monk.title:
                        tank_temp_party.append(character)
                    if character == Barbarian.title:
                        tank_temp_party.append(character)
                    if character == Veteran_Bodyguard.title:
                        tank_temp_party.append(character)
                    if character == Master_Fencer.title:
                        tank_temp_party.append(character)
                    if character == Berserker.title:
                        melee_temp_party.append(character)
                    if character == Rogue.title:
                        melee_temp_party.append(character)
                    if character == Survivalist.title:
                        melee_temp_party.append(character)
                    if character == Brawlist.title:
                        melee_temp_party.append(character)
                    if character == Academic_Mage.title:
                        magic_temp_party.append(character)
                    if character == Druid.title:
                        magic_temp_party.append(character)
                    if character == Warlock.title:
                        magic_temp_party.append(character)
                    if character == Bloodmancer.title:
                        magic_temp_party.append(character)
                    if character == Paladin.title:
                        mixed_temp_party.append(character)
                    if character == Castle_Ranger.title:
                        mixed_temp_party.append(character)
                    if character == Thunder_Apprentice.title:
                        mixed_temp_party.append(character)
                    if character == Power_Conduit.title:
                        mixed_temp_party.append(character)
                    if character == Earth_Speaker.title:
                        healer_temp_party.append(character)
                    if character == Priest_of_the_Devoted.title:
                        healer_temp_party.append(character)
                    if character == Time_Walker.title:
                        healer_temp_party.append(character)
                    if character == Child_of_Medicine.title:
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
                visual_team_label = tk.Label(self, text=self.display_team2(temp_party))
                visual_team_label.grid(row=11, column=2)
            elif len(temp_party) == 5:
                root = tk.Tk()
                warning_label1CTP = tk.Label(root, text="The party is currently full!")
                warning_label2CTP = tk.Label(root, text="Would you like to remove a current party member to make room?")
                yes_buttonCTP = tk.Button(root, text="Yes",
                                          command=lambda: self.adding_champions_tempParty2(root, champion))
                no_buttonCTP = tk.Button(root, text="No", command=lambda: root.destroy())
                warning_label1CTP.grid(row=1, column=1)
                warning_label2CTP.grid(row=2, column=1)
                yes_buttonCTP.grid(row=3, column=1, sticky="w", padx=140)
                no_buttonCTP.grid(row=3, column=1, sticky="e", padx=140)

    def adding_champions_tempParty2(self, root, champion):
        global champion1CTP, champion2CTP, champion3CTP, champion4CTP, champion5CTP, cancel_buttonCTP, window_labelCTP
        yes_buttonCTP.grid_forget()
        no_buttonCTP.grid_forget()
        warning_label1CTP.grid_forget()
        warning_label2CTP.grid_forget()
        window_labelCTP = tk.Label(root, text="Please choose which champion will be replaced for '{}'".format(champion))
        champion1CTP = tk.Button(root, text=temp_party[0],
                                 command=lambda: self.replace_champion2(root, champion, temp_party[0]))
        champion2CTP = tk.Button(root, text=temp_party[1],
                                 command=lambda: self.replace_champion2(root, champion, temp_party[1]))
        champion3CTP = tk.Button(root, text=temp_party[2],
                                 command=lambda: self.replace_champion2(root, champion, temp_party[2]))
        champion4CTP = tk.Button(root, text=temp_party[3],
                                 command=lambda: self.replace_champion2(root, champion, temp_party[3]))
        champion5CTP = tk.Button(root, text=temp_party[4],
                                 command=lambda: self.replace_champion2(root, champion, temp_party[4]))
        cancel_buttonCTP = tk.Button(root, text="Cancel", command=root.destroy, font="bold")
        window_labelCTP.grid(row=1, column=3)
        champion1CTP.grid(row=2, column=3)
        champion2CTP.grid(row=3, column=3)
        champion3CTP.grid(row=4, column=3)
        champion4CTP.grid(row=5, column=3)
        champion5CTP.grid(row=6, column=3)
        cancel_buttonCTP.grid(row=7, column=3)

    def replace_champion2(self, root, champion, selected):
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
            if character == Monk.title:
                tank_temp_party.append(character)
            if character == Barbarian.title:
                tank_temp_party.append(character)
            if character == Veteran_Bodyguard.title:
                tank_temp_party.append(character)
            if character == Master_Fencer.title:
                tank_temp_party.append(character)
            if character == Berserker.title:
                melee_temp_party.append(character)
            if character == Rogue.title:
                melee_temp_party.append(character)
            if character == Survivalist.title:
                melee_temp_party.append(character)
            if character == Brawlist.title:
                melee_temp_party.append(character)
            if character == Academic_Mage.title:
                magic_temp_party.append(character)
            if character == Druid.title:
                magic_temp_party.append(character)
            if character == Warlock.title:
                magic_temp_party.append(character)
            if character == Bloodmancer.title:
                magic_temp_party.append(character)
            if character == Paladin.title:
                mixed_temp_party.append(character)
            if character == Castle_Ranger.title:
                mixed_temp_party.append(character)
            if character == Thunder_Apprentice.title:
                mixed_temp_party.append(character)
            if character == Power_Conduit.title:
                mixed_temp_party.append(character)
            if character == Earth_Speaker.title:
                healer_temp_party.append(character)
            if character == Priest_of_the_Devoted.title:
                healer_temp_party.append(character)
            if character == Time_Walker.title:
                healer_temp_party.append(character)
            if character == Child_of_Medicine.title:
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
        visual_team_label = tk.Label(self, text=self.display_team2(temp_party))
        visual_team_label.grid(row=11, column=2)

    def confirm_new_team2(self):
        root = tk.Tk()
        confirmation_label = tk.Label(root, text="Are you sure you want save this group?")
        yes_buttonCNT = tk.Button(root, text="Yes", command=lambda: SampleApp.finalise_new_team2(self, root))
        no_buttonCNT = tk.Button(root, text="No", command=lambda: root.destroy())
        confirmation_label.grid(row=2, column=1)
        yes_buttonCNT.grid(row=3, column=1, sticky="w", padx=70)
        no_buttonCNT.grid(row=3, column=1, sticky="e", padx=70)

    def save_new_team2(self, root):
        i = -1
        file = open("C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_championTeam_2.txt".format(computer_username),"r")
        file_allLines = file.readlines()
        user = SampleApp.get_user_encoded(self)
        user = str(user)
        for line in file_allLines:
            i += 1
            if user in line:
                coded_temp_party = self.code_party()
                new_line = "{} {}".format(line, coded_temp_party)
                file_allLines[i] = new_line
                file_write = open("C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_championTeam_2.txt".format(computer_username),"w")
                file_write.writelines(file_allLines)
                file.close()
                file_write.close()
                root.destroy()
                break
    def code_party(self):
        coded_temp_party = ""
        i = 0
        for character in temp_party:
            if character == Monk.title:
                coded_temp_party += Monk.code
            if character == Barbarian.title:
                coded_temp_party += Barbarian.code
            if character == Veteran_Bodyguard.title:
                coded_temp_party += Veteran_Bodyguard.code
            if character == Master_Fencer.title:
                coded_temp_party += Master_Fencer.code
            if character == Berserker.title:
                coded_temp_party += Berserker.code
            if character == Rogue.title:
                coded_temp_party += Rogue.code
            if character == Survivalist.title:
                coded_temp_party += Survivalist.code
            if character == Brawlist.title:
                coded_temp_party += Brawlist.code
            if character == Academic_Mage.title:
                coded_temp_party += Academic_Mage.code
            if character == Druid.title:
                coded_temp_party += Druid.code
            if character == Warlock.title:
                coded_temp_party += Warlock.code
            if character == Bloodmancer.title:
                coded_temp_party += Bloodmancer.code
            if character == Paladin.title:
                coded_temp_party += Paladin.code
            if character == Castle_Ranger.title:
                coded_temp_party += Castle_Ranger.code
            if character == Thunder_Apprentice.title:
                coded_temp_party += Thunder_Apprentice.code
            if character == Power_Conduit.title:
                coded_temp_party += Power_Conduit.code
            if character == Earth_Speaker.title:
                coded_temp_party += Earth_Speaker.code
            if character == Priest_of_the_Devoted.title:
                coded_temp_party += Priest_of_the_Devoted.code
            if character == Time_Walker.title:
                coded_temp_party += Time_Walker.code
            if character == Child_of_Medicine.title:
                coded_temp_party += Child_of_Medicine.code
            if character == "Empty":
                break
            i += 1
            if i <=4:
                coded_temp_party += ", "
        return coded_temp_party


    def clear_temp_party2(self):
        global temp_party
        temp_party = []


class Team3SelectionPage(tk.Frame):
    def __init__(self, parent, controller):
        global update_pageTSP
        global returnButtonTSP, invis_label1, invis_label2
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.menu_button_font = tkfont.Font(family='Helvetica', size=18, weight="bold")
        self.title_label_font = tkfont.Font(family='Helvetica', size=30, weight="bold")
        self.small_label_font = tkfont.Font(family='Helvetica', size=12, weight="bold")
        title = tk.Label(self, text="Champion Camp", font=self.title_label_font)
        update_pageTSP = tk.Button(self, text="Begin Recruiting for Team 3", command=lambda: self.pitstop3(),
                                   font=controller.menu_button_font)
        returnButtonTSP = tk.Button(self, text="Cancel", command=lambda: controller.cancel_new_team3())
        invis_label1 = tk.Label(self)
        invis_label2 = tk.Label(self)
        update_pageTSP.grid(row=2, column=2, pady=50)
        title.grid(row=1, column=2)
        returnButtonTSP.grid(row=13, column=2)
        invis_label1.grid(row=1, column=1, rowspan=4, pady=50, ipadx=240, ipady=100)
        invis_label2.grid(row=1, column=2, pady=100)

    def pitstop3(self):
        global visual_team_label, temp_party
        user = SampleApp.get_user_encoded(self)
        team_line_3 = []
        team_line_3 = SampleApp.return_users_champion_team3(self, user)
        team_line_3 = team_line_3.replace(",", "")
        team_3_list_data = team_line_3.split()
        CTP = CreateTeamPage
        decoded_dungeoneer_team3CTP = CTP.team_3_decode(self, team_3_list_data)
        temp_party = decoded_dungeoneer_team3CTP
        visual_team_label = tk.Label(self, text=self.display_team3(temp_party))
        visual_team_label.grid(row=11, column=2)
        self.team_creation3()

    def team_creation3(self):
        global tank, dps, healer, tank_section_button, dps_section_button, healer_section_button, decoded_dungeoneer_team3CTP
        tank = False
        dps = False
        healer = False
        invis_label3 = tk.Label(self)
        invis_label4 = tk.Label(self)
        tank_section_button = tk.Button(self, text="Tanks", font=self.menu_button_font, width=26,
                                        command=self.view_tanks3)
        dps_section_button = tk.Button(self, text="Damage Dealers", font=self.menu_button_font, width=26,
                                       command=self.view_dps3)
        healer_section_button = tk.Button(self, text="Healers", font=self.menu_button_font, width=26,
                                          command=self.view_healer3)
        your_team_label = tk.Label(self, text=":Your Team:", font=self.small_label_font)
        confirm_changes_button = tk.Button(self, text="Confirm Changes", command=self.confirm_new_team3)
        tank_section_button.grid(row=2, column=2)
        dps_section_button.grid(row=2, column=1, padx=25)
        healer_section_button.grid(row=2, column=3)
        invis_label3.grid(row=2, column=0, padx=6)
        invis_label4.grid(row=9, column=2, pady=45)
        your_team_label.grid(row=10, column=2)
        confirm_changes_button.grid(row=12, column=2)
        invis_label1.grid_forget()
        invis_label2.grid_forget()
        update_pageTSP.grid_forget()

    def display_team3(self, temp_party):
        team_3_text = ""
        i = 0
        for character in temp_party:
            if i == 3:
                team_3_text += "\n"
            team_3_text += "["
            team_3_text += character
            team_3_text += "]"
            i += 1
        if i != 5:
            while i < 5:
                team_3_text += "["
                team_3_text += "Empty"
                team_3_text += "]"
                i += 1
        return team_3_text

    def view_tanks3(self):
        global monk_label, monk_button_add, monk_button_details, barbarian_label, barbarian_button_add, \
            barbarian_button_details, bodyguard_label, bodyguard_button_add, bodyguard_button_details, \
            fencer_label, fencer_button_add, fencer_button_details, invis_label3, invis_label4, tank, dps, healer
        if tank == True:
            return
        else:
            if dps == True:
                berserker_label.destroy()
                berserker_button_add.destroy()
                berserker_button_details.destroy()
                rogue_label.destroy()
                rogue_button_add.destroy()
                rogue_button_details.destroy()
                survivalist_label.destroy()
                survivalist_button_add.destroy()
                survivalist_button_details.destroy()
                brawlist_label.destroy()
                brawlist_button_add.destroy()
                brawlist_button_details.destroy()
                academic_mage_label.destroy()
                academic_mage_button_add.destroy()
                academic_mage_button_details.destroy()
                jungle_druid_label.destroy()
                jungle_druid_button_add.destroy()
                jungle_druid_button_details.destroy()
                warlock_label.destroy()
                warlock_button_add.destroy()
                warlock_button_details.destroy()
                bloodmancer_label.destroy()
                bloodmancer_button_add.destroy()
                bloodmancer_button_details.destroy()
                paladin_label.destroy()
                paladin_button_add.destroy()
                paladin_button_details.destroy()
                castle_ranger_label.destroy()
                castle_ranger_button_add.destroy()
                castle_ranger_button_details.destroy()
                thunder_apprentice_label.destroy()
                thunder_apprentice_button_add.destroy()
                thunder_apprentice_button_details.destroy()
                power_conduit_label.destroy()
                power_conduit_button_add.destroy()
                power_conduit_button_details.destroy()
                melee_label.destroy()
                magic_label.destroy()
                mix_label.destroy()
                dps = False
            else:
                dps = False
            if healer == True:
                earth_speaker_label.destroy()
                earth_speaker_button_add.destroy()
                earth_speaker_button_details.destroy()
                priest_of_the_devoted_label.destroy()
                priest_of_the_devoted_button_add.destroy()
                priest_of_the_devoted_button_details.destroy()
                time_walker_label.destroy()
                time_walker_button_add.destroy()
                time_walker_button_details.destroy()
                child_of_medicine_label.destroy()
                child_of_medicine_button_add.destroy()
                child_of_medicine_button_details.destroy()
                invis_label3.destroy()
                invis_label4.destroy()
                healer = False
            else:
                healer = False
            tank = True
            invis_label3 = tk.Label(self)
            invis_label4 = tk.Label(self)
            monk_label = tk.Label(self, text=Monk.name, font=self.menu_button_font)
            monk_button_add = tk.Button(self, text="Add to Team",
                                        command=lambda: self.check_temp_party3(Monk.title, "tank"))
            monk_button_details = tk.Button(self, text="View Details")
            barbarian_label = tk.Label(self, text=Barbarian.name, font=self.menu_button_font)
            barbarian_button_add = tk.Button(self, text="Add to Team",
                                             command=lambda: self.check_temp_party3(Barbarian.title, "tank"))
            barbarian_button_details = tk.Button(self, text="View Details")
            bodyguard_label = tk.Label(self, text=Veteran_Bodyguard.name, font=self.menu_button_font)
            bodyguard_button_add = tk.Button(self, text="Add to Team",
                                             command=lambda: self.check_temp_party3(Veteran_Bodyguard.title, "tank"))
            bodyguard_button_details = tk.Button(self, text="View Details")
            fencer_label = tk.Label(self, text=Master_Fencer.name, font=self.menu_button_font)
            fencer_button_add = tk.Button(self, text="Add to Team",
                                          command=lambda: self.check_temp_party3(Master_Fencer.title, "tank"))
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

    def view_dps3(self):
        global melee_label, magic_label, mix_label, berserker_label, berserker_button_add, berserker_button_details, \
            rogue_label, rogue_button_add, rogue_button_details, survivalist_label, survivalist_button_add, survivalist_button_details, \
            brawlist_label, brawlist_button_add, brawlist_button_details, academic_mage_label, academic_mage_button_add, academic_mage_button_details, \
            jungle_druid_label, jungle_druid_button_add, jungle_druid_button_details, warlock_label, warlock_button_add, warlock_button_details, \
            bloodmancer_label, bloodmancer_button_add, bloodmancer_button_details, paladin_label, paladin_button_add, paladin_button_details, \
            castle_ranger_label, castle_ranger_button_add, castle_ranger_button_details, thunder_apprentice_label, thunder_apprentice_button_add, thunder_apprentice_button_details, \
            power_conduit_label, power_conduit_button_add, power_conduit_button_details, tank, dps, healer
        if dps == True:
            return
        else:
            if tank == True:
                monk_label.destroy()
                monk_button_add.destroy()
                monk_button_details.destroy()
                barbarian_label.destroy()
                barbarian_button_add.destroy()
                barbarian_button_details.destroy()
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
                earth_speaker_label.destroy()
                earth_speaker_button_add.destroy()
                earth_speaker_button_details.destroy()
                priest_of_the_devoted_label.destroy()
                priest_of_the_devoted_button_add.destroy()
                priest_of_the_devoted_button_details.destroy()
                time_walker_label.destroy()
                time_walker_button_add.destroy()
                time_walker_button_details.destroy()
                child_of_medicine_label.destroy()
                child_of_medicine_button_add.destroy()
                child_of_medicine_button_details.destroy()
                invis_label3.destroy()
                invis_label4.destroy()
                healer = False
            else:
                healer = False
            dps = True
            melee_label = tk.Label(self, text=":Melee:", font=self.menu_button_font)
            magic_label = tk.Label(self, text=":Magic:", font=self.menu_button_font)
            mix_label = tk.Label(self, text=":Other:", font=self.menu_button_font)
            berserker_label = tk.Label(self, text=Berserker.name)
            berserker_button_add = tk.Button(self, text="Add to Team",
                                             command=lambda: self.check_temp_party3(Berserker.title, "melee"))
            berserker_button_details = tk.Button(self, text="View Details")
            rogue_label = tk.Label(self, text=Rogue.name)
            rogue_button_add = tk.Button(self, text="Add to Team",
                                         command=lambda: self.check_temp_party3(Rogue.title, "melee"))
            rogue_button_details = tk.Button(self, text="View Details")
            survivalist_label = tk.Label(self, text=Survivalist.name)
            survivalist_button_add = tk.Button(self, text="Add to Team",
                                               command=lambda: self.check_temp_party3(Survivalist.title, "melee"))
            survivalist_button_details = tk.Button(self, text="View Details")
            brawlist_label = tk.Label(self, text=Brawlist.name)
            brawlist_button_add = tk.Button(self, text="Add to Team",
                                            command=lambda: self.check_temp_party3(Brawlist.title, "melee"))
            brawlist_button_details = tk.Button(self, text="View Details")
            academic_mage_label = tk.Label(self, text=Academic_Mage.name)
            academic_mage_button_add = tk.Button(self, text="Add to Team",
                                                 command=lambda: self.check_temp_party3(Academic_Mage.title, "magic"))
            academic_mage_button_details = tk.Button(self, text="View Details")
            jungle_druid_label = tk.Label(self, text=Druid.name)
            jungle_druid_button_add = tk.Button(self, text="Add to Team",
                                                command=lambda: self.check_temp_party3(Druid.title, "magic"))
            jungle_druid_button_details = tk.Button(self, text="View Details")
            warlock_label = tk.Label(self, text=Warlock.name)
            warlock_button_add = tk.Button(self, text="Add to Team",
                                           command=lambda: self.check_temp_party3(Warlock.title, "magic"))
            warlock_button_details = tk.Button(self, text="View Details")
            bloodmancer_label = tk.Label(self, text=Bloodmancer.name)
            bloodmancer_button_add = tk.Button(self, text="Add to Team",
                                               command=lambda: self.check_temp_party3(Bloodmancer.title, "magic"))
            bloodmancer_button_details = tk.Button(self, text="View Details")
            paladin_label = tk.Label(self, text=Paladin.name)
            paladin_button_add = tk.Button(self, text="Add to Team",
                                           command=lambda: self.check_temp_party3(Paladin.title, "mixed"))
            paladin_button_details = tk.Button(self, text="View Details")
            castle_ranger_label = tk.Label(self, text=Castle_Ranger.name)
            castle_ranger_button_add = tk.Button(self, text="Add to Team",
                                                 command=lambda: self.check_temp_party3(Castle_Ranger.title, "mixed"))
            castle_ranger_button_details = tk.Button(self, text="View Details")
            thunder_apprentice_label = tk.Label(self, text=Thunder_Apprentice.name)
            thunder_apprentice_button_add = tk.Button(self, text="Add to Team",
                                                      command=lambda: self.check_temp_party3(Thunder_Apprentice.title,
                                                                                            "mixed"))
            thunder_apprentice_button_details = tk.Button(self, text="View Details")
            power_conduit_label = tk.Label(self, text=Power_Conduit.name)
            power_conduit_button_add = tk.Button(self, text="Add to Team",
                                                 command=lambda: self.check_temp_party3(Power_Conduit.title, "mixed"))
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

    def view_healer3(self):
        global earth_speaker_label, earth_speaker_button_add, earth_speaker_button_details, priest_of_the_devoted_label, priest_of_the_devoted_button_add, \
            priest_of_the_devoted_button_details, time_walker_label, time_walker_button_add, time_walker_button_details, \
            child_of_medicine_label, child_of_medicine_button_add, child_of_medicine_button_details, invis_label3, invis_label4, tank, dps, healer
        if healer == True:
            return
        else:
            invis_label3 = tk.Label(self)
            invis_label4 = tk.Label(self)
            if tank == True:
                monk_label.destroy()
                monk_button_add.destroy()
                monk_button_details.destroy()
                barbarian_label.destroy()
                barbarian_button_add.destroy()
                barbarian_button_details.destroy()
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
                berserker_label.destroy()
                berserker_button_add.destroy()
                berserker_button_details.destroy()
                rogue_label.destroy()
                rogue_button_add.destroy()
                rogue_button_details.destroy()
                survivalist_label.destroy()
                survivalist_button_add.destroy()
                survivalist_button_details.destroy()
                brawlist_label.destroy()
                brawlist_button_add.destroy()
                brawlist_button_details.destroy()
                academic_mage_label.destroy()
                academic_mage_button_add.destroy()
                academic_mage_button_details.destroy()
                jungle_druid_label.destroy()
                jungle_druid_button_add.destroy()
                jungle_druid_button_details.destroy()
                warlock_label.destroy()
                warlock_button_add.destroy()
                warlock_button_details.destroy()
                bloodmancer_label.destroy()
                bloodmancer_button_add.destroy()
                bloodmancer_button_details.destroy()
                paladin_label.destroy()
                paladin_button_add.destroy()
                paladin_button_details.destroy()
                castle_ranger_label.destroy()
                castle_ranger_button_add.destroy()
                castle_ranger_button_details.destroy()
                thunder_apprentice_label.destroy()
                thunder_apprentice_button_add.destroy()
                thunder_apprentice_button_details.destroy()
                power_conduit_label.destroy()
                power_conduit_button_add.destroy()
                power_conduit_button_details.destroy()
                melee_label.destroy()
                magic_label.destroy()
                mix_label.destroy()
                dps = False
            else:
                dps = False
            healer = True
            earth_speaker_label = tk.Label(self, text=Earth_Speaker.name, font=self.menu_button_font)
            earth_speaker_button_add = tk.Button(self, text="Add to Team",
                                                 command=lambda: self.check_temp_party3(Earth_Speaker.title, "healer"))
            earth_speaker_button_details = tk.Button(self, text="View Details")
            priest_of_the_devoted_label = tk.Label(self, text=Priest_of_the_Devoted.name, font=self.menu_button_font)
            priest_of_the_devoted_button_add = tk.Button(self, text="Add to Team",
                                                         command=lambda: self.check_temp_party3(
                                                             Priest_of_the_Devoted.title, "healer"))
            priest_of_the_devoted_button_details = tk.Button(self, text="View Details")
            time_walker_label = tk.Label(self, text=Time_Walker.name, font=self.menu_button_font)
            time_walker_button_add = tk.Button(self, text="Add to Team",
                                               command=lambda: self.check_temp_party3(Time_Walker.title, "healer"))
            time_walker_button_details = tk.Button(self, text="View Details")
            child_of_medicine_label = tk.Label(self, text=Child_of_Medicine.name, font=self.menu_button_font)
            child_of_medicine_button_add = tk.Button(self, text="Add to Team",
                                                     command=lambda: self.check_temp_party3(Child_of_Medicine.title,
                                                                                           "healer"))
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

    def check_temp_party3(self, champion, type):
        global temp_party, yes_buttonCTP, no_buttonCTP, warning_label1CTP, warning_label2CTP, tank, dps, healer, visual_team_label
        tank_temp_party = []
        melee_temp_party = []
        magic_temp_party = []
        mixed_temp_party = []
        healer_temp_party = []
        if champion in temp_party:
            root = tk.Tk()
            warning_label = tk.Label(root, text="Sorry, but this character is already assigned in the party")
            ok_button = tk.Button(root, text="Ok", command=root.destroy)
            ok_button.grid(row=2, column=1)
            warning_label.grid(row=1, column=1)
            visual_team_label.destroy()
            visual_team_label = tk.Label(self, text=self.display_team3(temp_party))
            visual_team_label.grid(row=11, column=2)
        else:
            if len(temp_party) < 5:
                for character in temp_party:
                    if character == Monk.title:
                        tank_temp_party.append(character)
                    if character == Barbarian.title:
                        tank_temp_party.append(character)
                    if character == Veteran_Bodyguard.title:
                        tank_temp_party.append(character)
                    if character == Master_Fencer.title:
                        tank_temp_party.append(character)
                    if character == Berserker.title:
                        melee_temp_party.append(character)
                    if character == Rogue.title:
                        melee_temp_party.append(character)
                    if character == Survivalist.title:
                        melee_temp_party.append(character)
                    if character == Brawlist.title:
                        melee_temp_party.append(character)
                    if character == Academic_Mage.title:
                        magic_temp_party.append(character)
                    if character == Druid.title:
                        magic_temp_party.append(character)
                    if character == Warlock.title:
                        magic_temp_party.append(character)
                    if character == Bloodmancer.title:
                        magic_temp_party.append(character)
                    if character == Paladin.title:
                        mixed_temp_party.append(character)
                    if character == Castle_Ranger.title:
                        mixed_temp_party.append(character)
                    if character == Thunder_Apprentice.title:
                        mixed_temp_party.append(character)
                    if character == Power_Conduit.title:
                        mixed_temp_party.append(character)
                    if character == Earth_Speaker.title:
                        healer_temp_party.append(character)
                    if character == Priest_of_the_Devoted.title:
                        healer_temp_party.append(character)
                    if character == Time_Walker.title:
                        healer_temp_party.append(character)
                    if character == Child_of_Medicine.title:
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
                visual_team_label = tk.Label(self, text=self.display_team3(temp_party))
                visual_team_label.grid(row=11, column=2)
            elif len(temp_party) == 5:
                root = tk.Tk()
                warning_label1CTP = tk.Label(root, text="The party is currently full!")
                warning_label2CTP = tk.Label(root, text="Would you like to remove a current party member to make room?")
                yes_buttonCTP = tk.Button(root, text="Yes",
                                          command=lambda: self.adding_champions_tempParty3(root, champion))
                no_buttonCTP = tk.Button(root, text="No", command=lambda: root.destroy())
                warning_label1CTP.grid(row=1, column=1)
                warning_label2CTP.grid(row=2, column=1)
                yes_buttonCTP.grid(row=3, column=1, sticky="w", padx=140)
                no_buttonCTP.grid(row=3, column=1, sticky="e", padx=140)

    def adding_champions_tempParty3(self, root, champion):
        global champion1CTP, champion2CTP, champion3CTP, champion4CTP, champion5CTP, cancel_buttonCTP, window_labelCTP
        yes_buttonCTP.grid_forget()
        no_buttonCTP.grid_forget()
        warning_label1CTP.grid_forget()
        warning_label2CTP.grid_forget()
        window_labelCTP = tk.Label(root, text="Please choose which champion will be replaced for '{}'".format(champion))
        champion1CTP = tk.Button(root, text=temp_party[0],
                                 command=lambda: self.replace_champion3(root, champion, temp_party[0]))
        champion2CTP = tk.Button(root, text=temp_party[1],
                                 command=lambda: self.replace_champion3(root, champion, temp_party[1]))
        champion3CTP = tk.Button(root, text=temp_party[2],
                                 command=lambda: self.replace_champion3(root, champion, temp_party[2]))
        champion4CTP = tk.Button(root, text=temp_party[3],
                                 command=lambda: self.replace_champion3(root, champion, temp_party[3]))
        champion5CTP = tk.Button(root, text=temp_party[4],
                                 command=lambda: self.replace_champion3(root, champion, temp_party[4]))
        cancel_buttonCTP = tk.Button(root, text="Cancel", command=root.destroy, font="bold")
        window_labelCTP.grid(row=1, column=3)
        champion1CTP.grid(row=2, column=3)
        champion2CTP.grid(row=3, column=3)
        champion3CTP.grid(row=4, column=3)
        champion4CTP.grid(row=5, column=3)
        champion5CTP.grid(row=6, column=3)
        cancel_buttonCTP.grid(row=7, column=3)

    def replace_champion3(self, root, champion, selected):
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
            if character == Monk.title:
                tank_temp_party.append(character)
            if character == Barbarian.title:
                tank_temp_party.append(character)
            if character == Veteran_Bodyguard.title:
                tank_temp_party.append(character)
            if character == Master_Fencer.title:
                tank_temp_party.append(character)
            if character == Berserker.title:
                melee_temp_party.append(character)
            if character == Rogue.title:
                melee_temp_party.append(character)
            if character == Survivalist.title:
                melee_temp_party.append(character)
            if character == Brawlist.title:
                melee_temp_party.append(character)
            if character == Academic_Mage.title:
                magic_temp_party.append(character)
            if character == Druid.title:
                magic_temp_party.append(character)
            if character == Warlock.title:
                magic_temp_party.append(character)
            if character == Bloodmancer.title:
                magic_temp_party.append(character)
            if character == Paladin.title:
                mixed_temp_party.append(character)
            if character == Castle_Ranger.title:
                mixed_temp_party.append(character)
            if character == Thunder_Apprentice.title:
                mixed_temp_party.append(character)
            if character == Power_Conduit.title:
                mixed_temp_party.append(character)
            if character == Earth_Speaker.title:
                healer_temp_party.append(character)
            if character == Priest_of_the_Devoted.title:
                healer_temp_party.append(character)
            if character == Time_Walker.title:
                healer_temp_party.append(character)
            if character == Child_of_Medicine.title:
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
        visual_team_label = tk.Label(self, text=self.display_team3(temp_party))
        visual_team_label.grid(row=11, column=2)

    def confirm_new_team3(self):
        root = tk.Tk()
        confirmation_label = tk.Label(root, text="Are you sure you want save this group?")
        yes_buttonCNT = tk.Button(root, text="Yes", command=lambda: SampleApp.finalise_new_team3(self, root))
        no_buttonCNT = tk.Button(root, text="No", command=lambda: root.destroy())
        confirmation_label.grid(row=2, column=1)
        yes_buttonCNT.grid(row=3, column=1, sticky="w", padx=70)
        no_buttonCNT.grid(row=3, column=1, sticky="e", padx=70)

    def save_new_team3(self, root):
        i = -1
        file = open("C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_championTeam_3.txt".format(computer_username),"r")
        file_allLines = file.readlines()
        user = SampleApp.get_user_encoded(self)
        user = str(user)
        for line in file_allLines:
            i += 1
            if user in line:
                coded_temp_party = self.code_party()
                new_line = "{} {}".format(line, coded_temp_party)
                file_allLines[i] = new_line
                file_write = open("C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_championTeam_3.txt".format(computer_username),"w")
                file_write.writelines(file_allLines)
                file.close()
                file_write.close()
                root.destroy()
                break
    def code_party(self):
        coded_temp_party = ""
        i = 0
        for character in temp_party:
            if character == Monk.title:
                coded_temp_party += Monk.code
            if character == Barbarian.title:
                coded_temp_party += Barbarian.code
            if character == Veteran_Bodyguard.title:
                coded_temp_party += Veteran_Bodyguard.code
            if character == Master_Fencer.title:
                coded_temp_party += Master_Fencer.code
            if character == Berserker.title:
                coded_temp_party += Berserker.code
            if character == Rogue.title:
                coded_temp_party += Rogue.code
            if character == Survivalist.title:
                coded_temp_party += Survivalist.code
            if character == Brawlist.title:
                coded_temp_party += Brawlist.code
            if character == Academic_Mage.title:
                coded_temp_party += Academic_Mage.code
            if character == Druid.title:
                coded_temp_party += Druid.code
            if character == Warlock.title:
                coded_temp_party += Warlock.code
            if character == Bloodmancer.title:
                coded_temp_party += Bloodmancer.code
            if character == Paladin.title:
                coded_temp_party += Paladin.code
            if character == Castle_Ranger.title:
                coded_temp_party += Castle_Ranger.code
            if character == Thunder_Apprentice.title:
                coded_temp_party += Thunder_Apprentice.code
            if character == Power_Conduit.title:
                coded_temp_party += Power_Conduit.code
            if character == Earth_Speaker.title:
                coded_temp_party += Earth_Speaker.code
            if character == Priest_of_the_Devoted.title:
                coded_temp_party += Priest_of_the_Devoted.code
            if character == Time_Walker.title:
                coded_temp_party += Time_Walker.code
            if character == Child_of_Medicine.title:
                coded_temp_party += Child_of_Medicine.code
            if character == "Empty":
                break
            i += 1
            if i <=4:
                coded_temp_party += ", "
        return coded_temp_party


    def clear_temp_party3(self):
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
    app = SampleApp()
    app.mainloop()
