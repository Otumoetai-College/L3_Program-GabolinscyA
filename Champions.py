class Champions:
    def __init__(self, hp, rp, ap, name):
        #Health Point
        self.hp = hp
        #Resource Point
        self.rp = rp
        #Attack Power
        self.ap = ap
        #Set name
        self.name = name
#Tanks:
#MNK
Monk = Champions(1000, 100, 50, 'Feramon, the Monk')
#BBR
Barbarian = Champions(1000, 100, 50, 'Baralor, the Barbarian')
#VBG
Veteran_Bodyguard = Champions(1000, 0, 50, 'Hecutis, the Veteran Bodyguard')
#MTF
Master_Fencer = Champions(1000, 0, 50, 'Lorelai, the Master Fencer')

#DPS:

#Melee
#BSR
Berserker = Champions(500, 100, 100, 'Kelzarg, the Berserker')
#RGE
Rogue = Champions(500, 0, 100, 'Ryker, the Rogue')
#SRV
Survivalist = Champions(500, 0, 100, 'Mally, the Survivalist')
#BST
Brawlist = Champions(500, 0, 100, 'George, the Brawlist')

#Magic
#ADM
Academic_Mage = Champions(500, 200, 100, 'Tulip, the Academics Mage')
#JDR
Jungle_Druid = Champions(500, 200, 100, 'Fuds, the Jungle Druid')
#WRK
Warlock = Champions(500, 200, 100, "Sol'ghar, the Warlock")
#BDM
Bloodmancer = Champions(500, 0, 100, 'Flynn, the Bloodmancer')

#Mixed
#PLD
Paladin = Champions(500, 0, 100, 'Olig, the Paladin')
#CLR
Castle_Ranger = Champions(500, 0, 100, 'Brad, the Castle Ranger')
#THD
Thunder_Apprentice = Champions(500, 0, 100, "Kel'ther, the Thunders Apprentice")
#PWC
Power_Conduit = Champions(500, 0, 0, 'Power Conduit')

#Healers:
#ESP
Earth_Speaker = Champions(500, 200, 50, "Delmanar, the Earth's Speaker")
#POD
Priest_of_the_Devoted = Champions(500, 200, 50, 'Sethuk, Priest of the Devoted')
#TWK
Time_Walker = Champions(500, 200, 50, 'Zaqner, the Time Walker')
#COM
Child_of_Medicine = Champions(500, 200, 50, 'Curie, a Child of Medicine')
