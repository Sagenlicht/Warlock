from toee import *
import char_class_utils
import char_editor
###################################################

def GetConditionName(): # used by API
    return "Warlock"
    
# def GetSpellCasterConditionName():
    # return "Wizard Spellcasting"

def GetCategory():
    return "Complete Arcane"

def GetClassDefinitionFlags():
    return CDF_BaseClass

def GetClassHelpTopic():
    return "TAG_WARLOCKS"

classEnum = stat_level_warlock

###################################################

class_feats = {
1: (feat_armor_proficiency_light, feat_simple_weapon_proficiency, "Warlock Eldritch Blast", "Warlock Spell Failure", "Warlock Invocations",),
2: ("Warlock Detect Magic",),
3: ("Warlock Damage Reduction",),
8: ("Warlock Fiendish Resilience",),
}

class_skills = (skill_bluff, skill_concentration, skill_craft, skill_disguise, skill_intimidate, skill_jump, skill_knowledge_arcana, skill_knowledge_religion,
skill_profession, skill_sense_motive, skill_spellcraft, skill_use_magic_device) #skill_knowledge_planes is not in the game

#Spell Level 1+2 = Least Invocations
#Spell Level 3+4 = Lesser Invocations
#Spell Level 5+6 = Greater Invocations
#Spell Level 7-9 = Dark Invocations
### Note Some Dark Invocations actually would be spell level 6 by raw but I need a filter option for learning so I move these to spell level 7

spell_list = {
#    2: (spell_frightful_blast, spell_sickening_blast, spell_eldritch_spear, spell_beguiling_influence,),
#    3: (spell_brimstone_blast,),
#    4: (spell_beshadowed_blast, spell_hellrime_blast, spell_eldritch_chain,)
    }

    #spell_breath_of_the_night, spell_dark_ones_own_luck, spell_darkness, spell_earthen_grasp, spell_miasmic_cloud, spell_see_the_unseen, spell_spiderwalk),
    #1: (spell_charm, spell_curse_of_despair, spell_the_dead_walk, spell_stony_grasp, spell_voidsense, spell_voracious_dispelling, spell_walk_unseen, spell_wall_of_gloom),
    #2: (spell_bewitching_blast, spell_noxious_blast, spell_repelling_blast, spell_vitriolic_blast, spell_eldritch_cone, spell_chilling_tentacles, spell_devour_magic, spell_enervating_shadow, spell_tenacious_plague, spell_wall_of_perilous_flame),
    #3: (spell_utterdark_blast, spell_eldritch_doom, spell_retributive_invisibility, spell_word_of_changing)

bonus_feats =["Warlock Energy Resistance"]

spells_per_day = {
1:  (-1, 5, 5),
2:  (-1, 5, 5),
3:  (-1, 5, 5),
4:  (-1, 5, 5),
5:  (-1, 5, 5),
6:  (-1, 5, 5, 5, 5),
7:  (-1, 5, 5, 5, 5),
8:  (-1, 5, 5, 5, 5),
9:  (-1, 5, 5, 5, 5),
10: (-1, 5, 5, 5, 5),
11: (-1, 5, 5, 5, 5, 5, 5),
12: (-1, 5, 5, 5, 5, 5, 5),
13: (-1, 5, 5, 5, 5, 5, 5),
14: (-1, 5, 5, 5, 5, 5, 5),
15: (-1, 5, 5, 5, 5, 5, 5),
16: (-1, 5, 5, 5, 5, 5, 5, 5, 5, 5),
17: (-1, 5, 5, 5, 5, 5, 5, 5, 5, 5),
18: (-1, 5, 5, 5, 5, 5, 5, 5, 5, 5),
15: (-1, 5, 5, 5, 5, 5, 5, 5, 5, 5),
20: (-1, 5, 5, 5, 5, 5, 5, 5, 5, 5)
#lvl  0  1  2  3  4  5  6  7  8  9
}

def IsEnabled():
    return 1

def GetHitDieType():
    return 6
    
def GetSkillPtsPerLevel():
    return 2
    
def GetBabProgression():
    return base_attack_bonus_type_semi_martial
    
def IsFortSaveFavored():
    return 0
    
def IsRefSaveFavored():
    return 0
    
def IsWillSaveFavored():
    return 1

# Spell casting
def GetSpellListType():
    return spell_list_type_special

def GetSpellList():
    return spell_list

def GetSpellSourceType():
    return spell_source_type_arcane

def GetSpellReadyingType():
    return spell_readying_innate

def GetSpellsPerDay():
    return spells_per_day

caster_levels = range(1, 21)
def GetCasterLevels():
    return caster_levels

def GetSpellDeterminingStat():
    return stat_charisma

def IsClassSkill(skillEnum):
    return char_class_utils.IsClassSkill(class_skills, skillEnum)

def IsClassFeat(featEnum):
    return char_class_utils.IsClassFeat(class_feats, featEnum)

def GetClassFeats():
    return class_feats


def IsAlignmentCompatible(alignment):
    if (alignment & ALIGNMENT_EVIL):
        return 1
    elif (alignment & ALIGNMENT_CHAOTIC):
        return 1
    return 0

def ObjMeetsPrereqs( obj ):
    return 1

def GetDeityClass():
    return stat_level_sorcerer

## Levelup callbacks

def IsSelectingFeatsOnLevelup(obj):
    newLevel = obj.stat_level_get(classEnum) + 1
    if newLevel == 10:
        return 1
    return 0

def LevelupGetBonusFeats( obj ):
    bonFeatInfo = []
    for ft in bonus_feats:
        bonFeatInfo.append(char_editor.FeatInfo(ft))
    char_editor.set_bonus_feats(bonFeatInfo)
    return 0

#def IsSelectingSpellsOnLevelup( obj ):
#    newLevel = obj.stat_level_get(classEnum) + 1
#    if newLevel % 2 == 0:
#        return 1
#    elif newLevel == 1:
#        return 1
#    elif newLevel == 15:
#        return 1
#    return 0

#def InitSpellSelection( obj, classLvlNew = -1, classLvlIncrement = 1):
#    classLvl = obj.stat_level_get(classEnum)
#    if classLvlNew <= 0:
#        classLvlNew = classLvl + 1
#    maxSpellLvl = char_editor.get_max_spell_level(obj, classEnum, classLvlNew ) # this regards spell list extension by stuff like Mystic Theurge
#    
    # Available Spells
#    spAvail = char_editor.get_learnable_spells(obj, classEnum, maxSpellLvl)

    # add spell level labels
#    for p in range(1,maxSpellLvl+1):
#        spAvail.append(char_editor.KnownSpellInfo(spell_label_level_0 + p, 0, classEnum))
#    spAvail.sort()
#    char_editor.append_available_spells(spAvail)
    
    # Spell slots
#    spEnums = []
#    vacant_slot = char_editor.KnownSpellInfo(spell_vacant, 3, classEnum) # sets it to spell level -1
#    spEnums.append(vacant_slot)
#    char_editor.append_spell_enums(spEnums)
#    return 0

#def LevelupCheckSpells( obj):
#    spell_enums = char_editor.get_spell_enums()
#    classLvl = obj.stat_level_get(classEnum)
#    classLvlNew = classLvl + 1
#    if classLvlNew == 2:
#        sp_lvl_1_count = 0
#        spKnown = char_editor.get_known_class_spells(obj, classEnum)
#        for spInfo in spKnown:
#            if spInfo.spell_level == 1:
#                sp_lvl_1_count += 1
#        if sp_lvl_1_count > 20: # for scroll puffing maniacs
#            return 1
#    
#    for spInfo in spell_enums:
#        if spInfo.spell_enum == spell_vacant:
#            return 0
#    return 1

#def LevelupSpellsFinalize( obj, classLvlNew = -1 ):
#    spEnums = char_editor.get_spell_enums()
#    char_editor.spell_known_add(spEnums) # internally takes care of duplicates and the labels/vacant slots

#    classLvl = obj.stat_level_get(classEnum)
#    if classLvlNew <= 0:
#        classLvlNew = classLvl + 1
#    if classLvlNew > 1:
#        return 0
#    # for new wizards, add all cantrips
#    cantrips = char_editor.get_learnable_spells(obj, classEnum, 0)
#    char_editor.spell_known_add(cantrips)
#    return 0