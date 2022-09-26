class Champions:
    def __init__(self, hp, rp, ap, name, title, code):
        #Health Point
        self.hp = hp
        #Resource Point
        self.rp = rp
        #Attack Power
        self.ap = ap
        #Set name
        self.name = name
        #Set Title
        self.title = title
        #Set Code
        self.code = code
#Tanks:
#MNK
Monk = Champions(1000, 100, 50, 'Feramon, the Monk', "Monk", "MNK")
#BBR
Barbarian = Champions(1000, 100, 50, 'Baralor, the Barbarian', "Barbarian", "BBR")
#VBG
Veteran_Bodyguard = Champions(1000, 0, 50, 'Hecutis, the Veteran Bodyguard', "Veteran Bodyguard", "VBG")
#MTF
Master_Fencer = Champions(1000, 0, 50, 'Lorelai, the Master Fencer', "Fencer", "MTF")

#DPS:

#Melee
#BKR
Berserker = Champions(500, 100, 100, 'Kelzarg, the Berserker', "Berserkser", "BKR")
#RGE
Rogue = Champions(500, 0, 100, 'Ryker, the Rogue', "Rogue", "RGE")
#SRV
Survivalist = Champions(500, 0, 100, 'Mally, the Survivalist', "Survivalist", "SRV")
#BST
Brawlist = Champions(500, 0, 100, 'George, the Brawlist', "Brawlist", "BST")

#Magic
#ADM
Academic_Mage = Champions(500, 200, 100, 'Tulip, the Academic Mage', "Academics Mage", "ADM")
#DRD
Druid = Champions(500, 200, 100, 'Fuds, the Druid', "Druid", "DRD")
#WRK
Warlock = Champions(500, 200, 100, "Sol'ghar, the Warlock", "Warlock", "WRK")
#BDM
Bloodmancer = Champions(500, 0, 100, 'Flynn, the Bloodmancer', "Bloodmancer", "BDM")

#Mixed
#PLD
Paladin = Champions(500, 0, 100, 'Olig, the Paladin', "Paladin", "PLD")
#CLR
Castle_Ranger = Champions(500, 0, 100, 'Brad, the Castle Ranger', "Ranger", "CLR")
#THD
Thunder_Apprentice = Champions(500, 0, 100, "Kel'ther, the Thunders Apprentice", "Thunderous Apprentice", "THD")
#PWC
Power_Conduit = Champions(500, 0, 0, 'Power Conduit', "Power Conduit", "PWC")

#Healers:
#ESP
Earth_Speaker = Champions(500, 200, 50, "Delmanar, the Earth's Speaker", "Earth Speaker", "ESP")
#PRS
Priest_of_the_Devoted = Champions(500, 200, 50, 'Sethuk, Priest of the Devoted', "Priest", "PRS")
#TWK
Time_Walker = Champions(500, 200, 50, 'Zaqner, the Time Walker', "Time Walker", "TWK")
#FDM
Child_of_Medicine = Champions(500, 200, 50, 'Curie, a Child of Medicine', "Field Medic", "FDM")