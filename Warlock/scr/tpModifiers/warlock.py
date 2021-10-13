from templeplus.pymod import PythonModifier
from toee import *
import tpdp
import char_class_utils
import tpactions

###################################################

def GetConditionName():
    return "Warlock"
    
print "Registering " + GetConditionName()

classEnum = stat_level_warlock
classSpecModule = __import__('class033_warlock')

###################################################

########## Python Action ID's ##########
selectInvocationsEnum = 3300
detectMagicEnum = 3302
paResetEldritchBlastId = 3300
paEldritchBlastId = 3301

paFiendishResilienceId = 3303
paChangeStanceId = 3304
########################################

#### Constants.py Entries ####
#### Can be removed when entered in constants.py ####
#spell_frightful_blast = 2301
#spell_sickening_blast = 2302
#spell_eldritch_spear = 2303
#spell_hideous_blow = 2304
#spell_beguiling_influence = 2305
#spell_breath_of_the_night = 2306
#spell_dark_ones_own_luck = 2307
#spell_earthen_grasp = 2308
#spell_entropic_warding = 2309
#spell_leaps_and_bounds = 2310
#spell_miasmic_cloud = 2311
#spell_see_the_unseen = 2312
#spell_spiderwalk = 2313
#spell_summon_swarm = 2314

###### Invocation List ######
leastInvocations = [spell_frightful_blast, spell_sickening_blast, spell_eldritch_spear, spell_hideous_blow, spell_beguiling_influence, spell_breath_of_the_night, spell_dark_ones_own_luck, spell_earthen_grasp,
spell_entropic_warding, spell_leaps_and_bounds, spell_miasmic_cloud, spell_see_the_unseen, spell_spiderwalk, spell_summon_swarm]


#### standard callbacks - BAB and Save values
def OnGetToHitBonusBase(attachee, args, evt_obj):
    classLvl = attachee.stat_level_get(classEnum)
    babvalue = game.get_bab_for_class(classEnum, classLvl)
    evt_obj.bonus_list.add(babvalue, 0, 137) # untyped, description: "Class"
    return 0

def OnGetSaveThrowFort(attachee, args, evt_obj):
    value = char_class_utils.SavingThrowLevel(classEnum, attachee, D20_Save_Fortitude)
    evt_obj.bonus_list.add(value, 0, 137)
    return 0

def OnGetSaveThrowReflex(attachee, args, evt_obj):
    value = char_class_utils.SavingThrowLevel(classEnum, attachee, D20_Save_Reflex)
    evt_obj.bonus_list.add(value, 0, 137)
    return 0

def OnGetSaveThrowWill(attachee, args, evt_obj):
    value = char_class_utils.SavingThrowLevel(classEnum, attachee, D20_Save_Will)
    evt_obj.bonus_list.add(value, 0, 137)
    return 0


classSpecObj = PythonModifier(GetConditionName(), 0)
classSpecObj.AddHook(ET_OnToHitBonusBase, EK_NONE, OnGetToHitBonusBase, ())
classSpecObj.AddHook(ET_OnSaveThrowLevel, EK_SAVE_FORTITUDE, OnGetSaveThrowFort, ())
classSpecObj.AddHook(ET_OnSaveThrowLevel, EK_SAVE_REFLEX, OnGetSaveThrowReflex, ())
classSpecObj.AddHook(ET_OnSaveThrowLevel, EK_SAVE_WILL, OnGetSaveThrowWill, ())

#### Warlock Feats ####

## General Invocation Cast Actions ##
def pythonActionTriggerSpellAction(attachee, args, evt_obj):
    print "Hook Invocation Cast"
    currentSequence = tpactions.get_cur_seq()
    spellPacket = currentSequence.spell_packet
    newSpellId = tpactions.get_new_spell_id()
    tpactions.register_spell_cast(spellPacket, newSpellId)
    tpactions.trigger_spell_effect(newSpellId)
    return 0

## Eldritch Blast ##

###Handle Invocation Selection
def initialInvocationSetup(attachee, args, evt_obj):
    x = 0
    while x in range(0,14):
        args.set_arg(x, 0)
        x +=1
    return 0

def selectInvocations(attachee, args, evt_obj):
    classLevel = attachee.stat_level_get(classEnum)
    if classLevel > 0 and not args.get_arg(0):
        radialSelectInvocation = tpdp.RadialMenuEntryParent("Select First Invocation")
        radialSelectInvocation = radialSelectHeritageParent.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Class)
        radialSelectLeastInvocation = tpdp.RadialMenuEntryParent("Least Invocations")
        radialSelectLeastInvocation.add_as_child(attachee, radialSelectInvocation)
        for invocation in leastInvocations:
            invocationName = game.get_spell_mesline(invocation)
            radialInvocationId = tpdp.RadialMenuEntryPythonAction("{}".format(invocationName), D20A_PYTHON_ACTION, selectInvocationsEnum, invocation, "TAG_CLASS_FEATURES_WARLOCK_INVOCATIONS")
            radialInvocationId.add_as_child(attachee, radialSelectInvocation)
    elif classLevel > 1 and not args.get_arg(1):
        radialSelectInvocation = tpdp.RadialMenuEntryParent("Select Second Invocation")
        radialSelectInvocation = radialSelectHeritageParent.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Class)
        radialSelectLeastInvocation = tpdp.RadialMenuEntryParent("Least Invocations")
        radialSelectLeastInvocation.add_as_child(attachee, radialSelectInvocation)
    elif classLevel > 3 and not args.get_arg(2):
        radialSelectInvocation = tpdp.RadialMenuEntryParent("Select Third Invocation")
        radialSelectInvocation = radialSelectHeritageParent.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Class)
        radialSelectLeastInvocation = tpdp.RadialMenuEntryParent("Least Invocations")
        radialSelectLeastInvocation.add_as_child(attachee, radialSelectInvocation)
    elif classLevel > 5 and not args.get_arg(3):
        radialSelectInvocation = tpdp.RadialMenuEntryParent("Select Fourth Invocation")
        radialSelectInvocation = radialSelectHeritageParent.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Class)
        radialSelectLeastInvocation = tpdp.RadialMenuEntryParent("Least Invocations")
        radialSelectLeastInvocation.add_as_child(attachee, radialSelectInvocation)
        radialSelectLesserInvocation = tpdp.RadialMenuEntryParent("Lesser Invocations")
        radialSelectLesserInvocation.add_as_child(attachee, radialSelectInvocation)
    elif classLevel > 7 and not args.get_arg(4):
        radialSelectInvocation = tpdp.RadialMenuEntryParent("Select Fifth Invocation")
        radialSelectInvocation = radialSelectHeritageParent.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Class)
        radialSelectLeastInvocation = tpdp.RadialMenuEntryParent("Least Invocations")
        radialSelectLeastInvocation.add_as_child(attachee, radialSelectInvocation)
        radialSelectLesserInvocation = tpdp.RadialMenuEntryParent("Lesser Invocations")
        radialSelectLesserInvocation.add_as_child(attachee, radialSelectInvocation)
    elif classLevel > 9 and not args.get_arg(5):
        radialSelectInvocation = tpdp.RadialMenuEntryParent("Select Sixth Invocation")
        radialSelectInvocation = radialSelectHeritageParent.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Class)
        radialSelectLeastInvocation = tpdp.RadialMenuEntryParent("Least Invocations")
        radialSelectLeastInvocation.add_as_child(attachee, radialSelectInvocation)
        radialSelectLesserInvocation = tpdp.RadialMenuEntryParent("Lesser Invocations")
        radialSelectLesserInvocation.add_as_child(attachee, radialSelectInvocation)
    elif classLevel > 10 and not args.get_arg(6):
        radialSelectInvocation = tpdp.RadialMenuEntryParent("Select Seventh Invocation")
        radialSelectInvocation = radialSelectHeritageParent.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Class)
        radialSelectLeastInvocation = tpdp.RadialMenuEntryParent("Least Invocations")
        radialSelectLeastInvocation.add_as_child(attachee, radialSelectInvocation)
        radialSelectLesserInvocation = tpdp.RadialMenuEntryParent("Lesser Invocations")
        radialSelectLesserInvocation.add_as_child(attachee, radialSelectInvocation)
        radialSelectGreaterInvocation = tpdp.RadialMenuEntryParent("Greater Invocations")
        radialSelectGreaterInvocation.add_as_child(attachee, radialSelectInvocation)
    elif classLevel > 12 and not args.get_arg(7):
        radialSelectInvocation = tpdp.RadialMenuEntryParent("Select Eighth Invocation")
        radialSelectInvocation = radialSelectHeritageParent.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Class)
        radialSelectLeastInvocation = tpdp.RadialMenuEntryParent("Least Invocations")
        radialSelectLeastInvocation.add_as_child(attachee, radialSelectInvocation)
        radialSelectLesserInvocation = tpdp.RadialMenuEntryParent("Lesser Invocations")
        radialSelectLesserInvocation.add_as_child(attachee, radialSelectInvocation)
        radialSelectGreaterInvocation = tpdp.RadialMenuEntryParent("Greater Invocations")
        radialSelectGreaterInvocation.add_as_child(attachee, radialSelectInvocation)
    elif classLevel > 14 and not args.get_arg(8):
        radialSelectInvocation = tpdp.RadialMenuEntryParent("Select Nineth Invocation")
        radialSelectInvocation = radialSelectHeritageParent.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Class)
        radialSelectLeastInvocation = tpdp.RadialMenuEntryParent("Least Invocations")
        radialSelectLeastInvocation.add_as_child(attachee, radialSelectInvocation)
        radialSelectLesserInvocation = tpdp.RadialMenuEntryParent("Lesser Invocations")
        radialSelectLesserInvocation.add_as_child(attachee, radialSelectInvocation)
        radialSelectGreaterInvocation = tpdp.RadialMenuEntryParent("Greater Invocations")
        radialSelectGreaterInvocation.add_as_child(attachee, radialSelectInvocation)
    elif classLevel > 15 and not args.get_arg(9):
        radialSelectInvocation = tpdp.RadialMenuEntryParent("Select Tenth Invocation")
        radialSelectInvocation = radialSelectHeritageParent.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Class)
        radialSelectLeastInvocation = tpdp.RadialMenuEntryParent("Least Invocations")
        radialSelectLeastInvocation.add_as_child(attachee, radialSelectInvocation)
        radialSelectLesserInvocation = tpdp.RadialMenuEntryParent("Lesser Invocations")
        radialSelectLesserInvocation.add_as_child(attachee, radialSelectInvocation)
        radialSelectGreaterInvocation = tpdp.RadialMenuEntryParent("Greater Invocations")
        radialSelectGreaterInvocation.add_as_child(attachee, radialSelectInvocation)
        radialSelectDarkInvocation = tpdp.RadialMenuEntryParent("Dark Invocations")
        radialSelectDarkInvocation.add_as_child(attachee, radialSelectInvocation)
    elif classLevel > 17 and not args.get_arg(10):
        radialSelectInvocation = tpdp.RadialMenuEntryParent("Select Eleventh Invocation")
        radialSelectInvocation = radialSelectHeritageParent.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Class)
        radialSelectLeastInvocation = tpdp.RadialMenuEntryParent("Least Invocations")
        radialSelectLeastInvocation.add_as_child(attachee, radialSelectInvocation)
        radialSelectLesserInvocation = tpdp.RadialMenuEntryParent("Lesser Invocations")
        radialSelectLesserInvocation.add_as_child(attachee, radialSelectInvocation)
        radialSelectGreaterInvocation = tpdp.RadialMenuEntryParent("Greater Invocations")
        radialSelectGreaterInvocation.add_as_child(attachee, radialSelectInvocation)
        radialSelectDarkInvocation = tpdp.RadialMenuEntryParent("Dark Invocations")
        radialSelectDarkInvocation.add_as_child(attachee, radialSelectInvocation)
    elif classLevel > 19 and not args.get_arg(11):
        radialSelectInvocation = tpdp.RadialMenuEntryParent("Select Twelveth Invocation")
        radialSelectInvocation = radialSelectHeritageParent.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Class)
        radialSelectLeastInvocation = tpdp.RadialMenuEntryParent("Least Invocations")
        radialSelectLeastInvocation.add_as_child(attachee, radialSelectInvocation)
        radialSelectLesserInvocation = tpdp.RadialMenuEntryParent("Lesser Invocations")
        radialSelectLesserInvocation.add_as_child(attachee, radialSelectInvocation)
        radialSelectGreaterInvocation = tpdp.RadialMenuEntryParent("Greater Invocations")
        radialSelectGreaterInvocation.add_as_child(attachee, radialSelectInvocation)
        radialSelectDarkInvocation = tpdp.RadialMenuEntryParent("Dark Invocations")
        radialSelectDarkInvocation.add_as_child(attachee, radialSelectInvocation)
    return 0

warlockHandleInvocations = PythonModifier("Warlock Handle Invocations", 14) #0-11: InvocationEnum, empty, empty
warlockHandleInvocations.MapToFeat("Warlock Invocations")
warlockHandleInvocations.AddHook(ET_OnConditionAdd, EK_NONE, initialInvocationSetup, ())
warlockHandleInvocations.AddHook(ET_OnBuildRadialMenuEntry , EK_NONE, selectInvocations, ())

warlockEldritchBlast = PythonModifier("Warlock Eldritch Blast Feat", 4) #essenceStanceEnum, shapeStanceEnum, essenceStanceSpellLevel, shapeStanceSpellLevel
warlockEldritchBlast.MapToFeat("Warlock Eldritch Blast")
#warlockEldritchBlast.AddHook(ET_OnBuildRadialMenuEntry , EK_NONE, radialEldritchBlast, ())

## Detect Magic SLA ##
def radialDetectMagic(attachee, args, evt_obj):
#    detectMagicSpellStore = PySpellStore(spell_detect_magic, 161, 0) #stat_level_warlock is wrong, needs to be ClassCode (which seems to be 128 + stat_level_[class], but how do I properly set it?)
#    detectMagicSlaId = tpdp.RadialMenuEntryPythonAction(detectMagicSpellStore, D20A_PYTHON_ACTION, paDetectMagicId, spell_detect_magic, "TAG_CLASS_FEATURES_WARLOCK_DETECT_MAGIC")
#    detectMagicSlaId.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Class)

    spellEnum = spell_detect_magic
    casterLevel = attachee.stat_level_get(classEnum)

    detectMagicId = tpdp.RadialMenuEntryPythonAction("Detect Magic (at Will)", D20A_PYTHON_ACTION, detectMagicEnum, spellEnum, "TAG_CLASS_FEATURES_WARLOCK_DETECT_MAGIC")
    spellData = tpdp.D20SpellData(spellEnum)
    spellData.set_spell_class(classEnum)
    spellData.set_spell_level(casterLevel)
    detectMagicId.set_spell_data(spellData)
    detectMagicId.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Class)
    return 0

warlockDetectMagic = PythonModifier("Warlock Detect Magic Feat", 2) #empty, empty
warlockDetectMagic.MapToFeat("Warlock Detect Magic")
warlockDetectMagic.AddHook(ET_OnBuildRadialMenuEntry , EK_NONE, radialDetectMagic, ())
warlockDetectMagic.AddHook(ET_OnD20PythonActionPerform, detectMagicEnum, pythonActionTriggerSpellAction, ())

## Damage Reduction Cold Iron ##
def addColdIronDr(attachee, args, evt_obj):
    classLevel = attachee.stat_level_get(classEnum)
    drValue = min((classLevel+1)/4, 5) #bonus capped at level 19
    evt_obj.damage_packet.add_physical_damage_res(drValue, D20DAP_COLD, 126) #ID 126 in damage.mes is DR; D20DAP_COLD = Cold Iron!!
    return 0

warlockDamageReduction = PythonModifier("Warlock Damage Reduction Feat", 2) #empty, empty
warlockDamageReduction.MapToFeat("Warlock Damage Reduction")
warlockDamageReduction.AddHook(ET_OnTakingDamage, EK_NONE, addColdIronDr, ())

## Fiendish Resilience ##
def radialFiendishResilience(attachee, args, evt_obj):
    chargesLeft = args.get_arg(0)
    fiendishResilienceId = tpdp.RadialMenuEntryPythonAction("Fiendish Resilience ({}/1)".format(chargesLeft), D20A_PYTHON_ACTION, paFiendishResilienceId, 114, "TAG_CLASS_FEATURES_WARLOCK_FIENDISH_RESILIENCE")
    fiendishResilienceId.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Class)
    return 0

def checkFiendishResilienceCharges(attachee, args, evt_obj):
    if args.get_arg(0) < 1:
        evt_obj.return_val = AEC_OUT_OF_CHARGES
    return 0

def activateFiendishResilience(attachee, args, evt_obj):
    chargesLeft = args.get_arg(0)
    resilienceDuration = 20 #2 min
    attachee.float_text_line("Fiendish Resilience activated")
    classLevel = attachee.stat_level_get(classEnum)
    if classLevel < 13:
        fastHealingAmount = 1
    elif classLevel < 18:
        fastHealingAmount = 2
    else:
        fastHealingAmount = 5
    attachee.condition_add_with_args('Warlock Fiendish Resilience Effect', resilienceDuration, fastHealingAmount)
    chargesLeft -= 1
    args.set_arg(0, chargesLeft)
    return 0

def resetFiendishResilienceCharges(attachee, args, evt_obj):
    args.set_arg(0, 1)
    return 0

warlockFiendishResilience = PythonModifier("Warlock Fiendish Resilience Feat", 3) #chargesLeft, empty, empty
warlockFiendishResilience.MapToFeat("Warlock Fiendish Resilience")
warlockFiendishResilience.AddHook(ET_OnBuildRadialMenuEntry , EK_NONE, radialFiendishResilience, ())
warlockFiendishResilience.AddHook(ET_OnD20PythonActionCheck, paFiendishResilienceId, checkFiendishResilienceCharges, ())
warlockFiendishResilience.AddHook(ET_OnD20PythonActionPerform, paFiendishResilienceId, activateFiendishResilience, ())
warlockFiendishResilience.AddHook(ET_OnNewDay, EK_NEWDAY_REST, resetFiendishResilienceCharges, ())

def fiendishResilienceHealTick(attachee, args, evt_obj):
    healAmount = args.get_arg(1)
    ### workaround for heal ###
    #heal requires a dice
    healDice = dice_new('1d1')
    healDice.bonus = healAmount -1
    ### workaround end ###
    game.particles ('sp-Cure Minor Wounds', attachee)
    attachee.heal(attachee, healDice, D20A_HEAL, 0)
    attachee.healsubdual(attachee, healDice, D20A_HEAL, 0)
    # Ticking down duration
    args.set_arg(0, args.get_arg(0)-evt_obj.data1)
    if args.get_arg(0) < 0:
        args.condition_remove()
    return 0

def fiendishResilienceOnConditionRemove(attachee, args, evt_obj):
    attachee.float_text_line("Fiendish Resilience end")
    return 0

def fiendishResilienceTooltip(attachee, args, evt_obj):
    if args.get_arg(0) == 1:
        evt_obj.append("Fast Healing {} ({} round)".format(args.get_arg(1), args.get_arg(0)))
    else:
        evt_obj.append("Fast Healing {} ({} rounds)".format(args.get_arg(1), args.get_arg(0)))
    return 0

def fiendishResilienceEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("WARLOCK_FIENDISH_RESILIENCE"), -2, " {} ({} round)".format(args.get_arg(1), args.get_arg(0)))
    else:
        evt_obj.append(tpdp.hash("WARLOCK_FIENDISH_RESILIENCE"), -2, " {} ({} rounds)".format(args.get_arg(1), args.get_arg(0)))
    return 0

warlockFiendishResilienceEffect = PythonModifier("Warlock Fiendish Resilience Effect", 4) #duration, healAmount, empty, empty
warlockFiendishResilienceEffect.AddHook(ET_OnConditionAdd, EK_NONE, fiendishResilienceHealTick, ())
warlockFiendishResilienceEffect.AddHook(ET_OnBeginRound, EK_NONE, fiendishResilienceHealTick, ())
warlockFiendishResilienceEffect.AddHook(ET_OnConditionRemove, EK_NONE, fiendishResilienceOnConditionRemove, ())
warlockFiendishResilienceEffect.AddHook(ET_OnGetTooltip, EK_NONE, fiendishResilienceTooltip, ())
warlockFiendishResilienceEffect.AddHook(ET_OnGetEffectTooltip, EK_NONE, fiendishResilienceEffectTooltip, ())

## Energy Resistance ##
def addEnergyResistance(attachee, args, evt_obj):
    classLevel = attachee.stat_level_get(classEnum)
    resistanceAmount = 5 if classLevel in range(10, 20) else 10
    energyType = args.get_param(0)
    evt_obj.damage_packet.add_damage_resistance(resistanceAmount, energyType, 124)
    return 0

warlockEnergyResistanceAcid = PythonModifier('Warlock Acid Resistance Feat', 0)
warlockEnergyResistanceAcid .MapToFeat('Warlock Energy Resistance - Acid')
warlockEnergyResistanceAcid .AddHook(ET_OnTakingDamage, EK_NONE, addEnergyResistance, (D20DT_ACID,))

warlockEnergyResistanceCold = PythonModifier('Warlock Cold Resistance Feat', 0)
warlockEnergyResistanceCold.MapToFeat('Warlock Energy Resistance - Cold')
warlockEnergyResistanceCold.AddHook(ET_OnTakingDamage, EK_NONE, addEnergyResistance, (D20DT_COLD,))

warlockEnergyResistanceElectricity = PythonModifier('Warlock Electricity Resistance Feat', 0)
warlockEnergyResistanceElectricity.MapToFeat('Warlock Energy Resistance - Electricity')
warlockEnergyResistanceElectricity.AddHook(ET_OnTakingDamage, EK_NONE, addEnergyResistance, (D20DT_ELECTRICITY,))

warlockEnergyResistanceFire = PythonModifier('Warlock Fire Resistance Feat', 0)
warlockEnergyResistanceFire.MapToFeat('Warlock Energy Resistance - Fire')
warlockEnergyResistanceFire.AddHook(ET_OnTakingDamage, EK_NONE, addEnergyResistance, (D20DT_FIRE,))

warlockEnergyResistanceSonic = PythonModifier('Warlock Sonic Resistance Feat', 0)
warlockEnergyResistanceSonic.MapToFeat('Warlock Energy Resistance - Sonic')
warlockEnergyResistanceSonic.AddHook(ET_OnTakingDamage, EK_NONE, addEnergyResistance, (D20DT_SONIC,))

#No spell failure in Light Armor for Warlock spells
def WarlockSpellFailure(attachee, args, evt_obj):
    #Only effects spells cast as a warlock
    if evt_obj.data1 != classEnum:
        return 0

    equip_slot = evt_obj.data2
    item = attachee.item_worn_at(equip_slot)

    if item == OBJ_HANDLE_NULL:
        return 0
        
    if equip_slot == item_wear_armor:
        armor_flags = item.obj_get_int(obj_f_armor_flags)
        if attachee.d20_query("Improved Armored Casting"):
            if (armor_flags & ARMOR_TYPE_NONE) or (armor_flags == ARMOR_TYPE_LIGHT) or (armor_flags == ARMOR_TYPE_MEDIUM):
                return 0
        else:
            if (armor_flags & ARMOR_TYPE_NONE) or (armor_flags == ARMOR_TYPE_LIGHT):
                return 0
    evt_obj.return_val += item.obj_get_int(obj_f_armor_arcane_spell_failure)
    return 0

warlockSpellFailure = PythonModifier("Warlock Spell Failure", 0)
warlockSpellFailure.MapToFeat("Warlock Spell Failure")
warlockSpellFailure.AddHook(ET_OnD20Query, EK_Q_Get_Arcane_Spell_Failure, WarlockSpellFailure, ())

### Spell casting
def OnGetBaseCasterLevel(attachee, args, evt_obj):
    if evt_obj.arg0 != classEnum:
        return 0
    classLvl = attachee.stat_level_get(classEnum)
    evt_obj.bonus_list.add(classLvl, 0, 137)
    return 0

def OnLevelupSpellsFinalize(attachee, args, evt_obj):
    if evt_obj.arg0 != classEnum:
        return 0
    classSpecModule.LevelupSpellsFinalize(attachee)
    return 0
    
def OnInitLevelupSpellSelection(attachee, args, evt_obj):
    if evt_obj.arg0 != classEnum:
        return 0
    classSpecModule.InitSpellSelection(attachee)
    return 0
    
def OnLevelupSpellsCheckComplete(attachee, args, evt_obj):
    if evt_obj.arg0 != classEnum:
        return 0
    if not classSpecModule.LevelupCheckSpells(attachee):
        evt_obj.bonus_list.add(-1, 0, 137) # denotes incomplete spell selection
    return 1    

classSpecObj.AddHook(ET_OnGetBaseCasterLevel, EK_NONE, OnGetBaseCasterLevel, ())
classSpecObj.AddHook(ET_OnLevelupSystemEvent, EK_LVL_Spells_Finalize, OnLevelupSpellsFinalize, ())
classSpecObj.AddHook(ET_OnLevelupSystemEvent, EK_LVL_Spells_Activate, OnInitLevelupSpellSelection, ())
classSpecObj.AddHook(ET_OnLevelupSystemEvent, EK_LVL_Spells_Check_Complete, OnLevelupSpellsCheckComplete, ())
