class Champions:
    def __init__(self, hp, rp, ap, name, title, code, rp_name, attack_list, specials_list):
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
        #Resource Power Name
        self.rp_name = rp_name
        #Possible attacks List
        self.attack_list = attack_list
        #Possible Special Abilities List
        self.specials_list = specials_list
#Tanks:
#MNK
MONK = Champions(1000, 100, 50, 'Feramon, the Monk', "Monk", "MNK", "Focus", ["Palm Strike", "Leg Sweep"], ["Harmonize", "Pressure Points"])
#BBR
BARBARIAN = Champions(1000, 100, 50, 'Baralor, the Barbarian', "Barbarian", "BBR", "Rage", ["Bloodthirst", "Pulverize"], ["Challenging Shout", "Impactful Boast"])
#VBG
VETERAN_BODYGUARD = Champions(1000, 0, 50, 'Hecutis, the Veteran Bodyguard', "Veteran Bodyguard", "VBG", "null", ["Shield Bash", "Trainwreck"], ["Fortification", "Block"])
#MTF
MASTER_FENCER = Champions(1000, 0, 50, 'Lorelai, the Master Fencer', "Fencer", "MTF", "null", ["Pierce", "Disruptive Slash"], ["Parry", "Elusive Measures"])

#DPS:

#Melee
#BKR
BERSERKER = Champions(500, 100, 100, 'Kelzarg, the Berserker', "Berserkser", "BKR", "Rage", ["Raging Blow", "Rampage"], ["Enrage", "Reckless Flurry"])
#RGE
ROGUE = Champions(500, 0, 100, 'Ryker, the Rogue', "Rogue", "RGE", "null", ["Gouge", "Eviscerate"], ["Garrote", "Exploit Weakness"])
#SRV
SURVIVALIST = Champions(500, 0, 100, 'Mally, the Survivalist', "Survivalist", "SRV", "null", ["Rustic Spear", "Scrap Bomb"], ["Modify Gear", "Rushed Rest"])
#BST
BRAWLIST = Champions(500, 0, 100, 'George, the Brawlist', "Brawlist", "BST", "null", ["Deterministic Punch", "Blackout Punch"], ["Defensive Stance", "Rushdown"])

#Magic
#ADM
ACADEMIC_MAGE = Champions(500, 200, 100, 'Tulip, the Academic Mage', "Academics Mage", "ADM", "Mana", ["Frost Bolt", "Fireball"], ["Arcane Brilliance", "Apply Magical Barrier"])
#DRD
DRUID = Champions(500, 200, 100, 'Fuds, the Druid', "Druid", "DRD", "Mana", ["Venus-fly Snap", "Vine-Swipe"], ["Thorns", "Prickle Arena"])
#WRK
WARLOCK = Champions(500, 200, 100, "Sol'ghar, the Warlock", "Warlock", "WRK", "Mana", ["Firey Bolt", "Void Infusion"], ["Wound Fissure", "Soul Tap"])
#BDM
BLOODMANCER = Champions(500, 0, 100, 'Flynn, the Bloodmancer', "Bloodmancer", "BDM", "null", ["Drain Life", "Blood Spike"], ["Blood Boil", "Nerve Harden"])

#Mixed
#PLD
PALADIN = Champions(500, 0, 100, 'Olig, the Paladin', "Paladin", "PLD", "null", ["Overhand Justice", "Righteous Blow"], ["Aura of Power", "Aura of Protection"])
#CLR
CASTLE_RANGER = Champions(500, 0, 100, 'Brad, the Castle Ranger', "Ranger", "CLR", "null", ["Steady Shot", "Power Opt"], ["Equip Iron-Tipped Arrows", "Equip Tracker-Infused Arrows"])
#THD
THUNDER_APPRENTICE = Champions(500, 0, 100, "Kel'ther, the Thunders Apprentice", "Thunderous Apprentice", "THD", "null", ["Lightning Bolt", "Chain Lighting"], ["Crashing Boom", "Thunderous Grasp"])
#PWC
POWER_CONDUIT = Champions(500, 0, 0, 'Power Conduit', "Power Conduit", "PWC", "null", [], ["Muscle Enlarger", "Cell Bloom", "Power Surge", "Full Potential"])

#Healers:
#ESP
EARTH_SPEAKER = Champions(500, 200, 50, "Delmanar, the Earth's Speaker", "Earth Speaker", "ESP", "Mana", ["Rock Barrage"], ["Healing Surge", "Rejuvenating Whirlpool", "Bedrock Cocoon"])
#PRS
PRIEST_OF_THE_DEVOTED = Champions(500, 200, 50, 'Sethuk, Priest of the Devoted', "Priest", "PRS", "Mana", ["Shimmering Bolt", "Divine Smite"], ["Healing Light", "Diffracting Nova"])
#TWK
TIME_WALKER = Champions(500, 200, 50, 'Zaqner, the Time Walker', "Time Walker", "TWK", "Mana", ["Cybernetic Blast"], ["Nanoheal Bots", "Reverse Wounds", "Alter Time"])
#FDM
CHILD_OF_MEDICINE = Champions(500, 0, 50, 'Curie, a Child of Medicine', "Field Medic", "FDM", "null", ["Throw Scissors"], ["Bandage Wound", "Perfected Herbal Tea", "G.3.T  J.A.X.D"])