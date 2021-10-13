from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *

def getModifications(enum):
    # damageType, saveType, saveDescriptor, specialFlag (0 = None, 1 = Living Target, 2 = Heals Undead), secondaryEffect, secondaryEffectDuration
    modificationDict = {
    3300: ("Eldritch Blast", D20DT_UNSPECIFIED, -1, D20STD_F_NONE, 0, False, 0),
    3311: ("Frightful Blast", D20DT_UNSPECIFIED, D20_Save_Will, D20STD_F_SPELL_DESCRIPTOR_MIND_AFFECTING | D20STD_F_SPELL_DESCRIPTOR_FEAR, 0, True, 10),
    3312: ("Sickening Blast", D20DT_UNSPECIFIED, D20_Save_Fortitude, D20STD_F_SPELL_SCHOOL_NECROMANCY, 1, True, 10),
    3313: ("Beshadowed Blast", D20DT_UNSPECIFIED, D20_Save_Fortitude, D20STD_F_SPELL_SCHOOL_NECROMANCY, 1, True, 1),
    3314: ("Brimstone Blast", D20DT_FIRE, D20_Save_Reflex, D20STD_F_SPELL_DESCRIPTOR_FIRE, 0, True, 1),
    3315: ("Hellrime Blast", D20DT_COLD, D20_Save_Fortitude, D20STD_F_SPELL_DESCRIPTOR_COLD, 0, True, 100)
    }

    damageType = modificationDict.get(enum)[1]
    saveType = modificationDict.get(enum)[2]
    saveDescriptor = modificationDict.get(enum)[3]
    specialFlag = modificationDict.get(enum)[4]
    secondaryEffect = modificationDict.get(enum)[5]
    secondaryEffectDuration = modificationDict.get(enum)[6]
    return damageType, saveType, saveDescriptor, specialFlag, secondaryEffect, secondaryEffectDuration
