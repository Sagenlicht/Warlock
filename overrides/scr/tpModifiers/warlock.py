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
paResetEldritchBlastId = 3300
paEldritchBlastId = 3301
paDetectMagicId = 3302
paFiendishResilienceId = 3303
paChangeStanceId = 3304
########################################


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
def radialEldritchBlast(attachee, args, evt_obj):
    #Find actual spell level of Eldritch Blast
    classLevel = attachee.stat_level_get(classEnum)
    if not args.get_arg(0) in range(spell_frightful_blast, 3331) or args.get_arg(0) == spell_eldritch_blast:
        args.set_arg(0, spell_eldritch_blast)
    if not args.get_arg(1) in range(spell_eldritch_blast, spell_frightful_blast):
        args.set_arg(1, spell_eldritch_blast)
    essenceStanceSpellLevel = args.get_arg(2) if args.get_arg(2) else 1
    shapeStanceSpellLevel = args.get_arg(3) if args.get_arg(3) else 1
    eldritchBlastSpellLevel = max(1, min(classLevel/2, 9)) #Eldritch Blast has a spell Level equal to one half warlock level (min 1, max 9), can be overwritten by a modification
    spellLevel = max(essenceStanceSpellLevel, shapeStanceSpellLevel, eldritchBlastSpellLevel)

    #Create Eldritch Blast Radial
    eldritchBlastType = args.get_arg(1)
    eldritchBlastSpellStore = PySpellStore(eldritchBlastType, 161, spellLevel) #stat_level_warlock is wrong, needs to be ClassCode (which seems to be 128 + stat_level_[class], but how do I properly set it?)
    radialEldritchBlastId = tpdp.RadialMenuEntryPythonAction(eldritchBlastSpellStore, D20A_PYTHON_ACTION, paEldritchBlastId, spell_eldritch_blast, "TAG_CLASS_FEATURES_WARLOCK_ELDRITCH_BLAST")
    radialEldritchBlastId.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Class)

    #Create Set Stance Options Radial
    radialStanceOptions = tpdp.RadialMenuEntryParent("Set Eldritch Blast Stance")
    radialStanceOptionsId = radialStanceOptions.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Class)
    knownInvocations = attachee.spells_known
    # I have no idea how I do properly access the enum in a PySpellStore, so I am gonna slice it if for now
    for invocation in knownInvocations:
        spellStoreString = str(invocation)
        startSlice = spellStoreString.find("=") + 1
        stopSlice = spellStoreString.find(",", startSlice)
        slicedEnum = int(spellStoreString[startSlice:stopSlice])
        if slicedEnum in range(spell_eldritch_blast, 3331):
            invocationRadialId = tpdp.RadialMenuEntryPythonAction(invocation, D20A_PYTHON_ACTION, paChangeStanceId, 0, "TAG_CLASS_FEATURES_WARLOCK_ELDRITCH_BLAST")
            invocationRadialId.add_as_child(attachee, radialStanceOptionsId)

    #Add Reset Option
    radialResetBlastId = tpdp.RadialMenuEntryPythonAction("Reset Eldritch Blast", D20A_PYTHON_ACTION, paResetEldritchBlastId, 0, "TAG_CLASS_FEATURES_WARLOCK_ELDRITCH_BLAST")
    radialResetBlastId.add_as_child(attachee, radialStanceOptionsId)
    return 0

def resetEldritchBlast(attachee, args, evt_obj):
    attachee.float_text_line("Eldritch Blast reset")
    args.set_arg(0, spell_eldritch_blast)
    args.set_arg(1, spell_eldritch_blast)
    args.set_arg(2, 1)
    args.set_arg(3, 1)
    return 0

def eldritchBlastTooltip(attachee, args, evt_obj):
    if args.get_arg(0) in range(spell_frightful_blast, 3331):
        essenceStanceEnum = args.get_arg(0)
    else:
        essenceStanceEnum = spell_eldritch_blast
    if args.get_arg(1) in range(spell_eldritch_blast, spell_frightful_blast):
        shapeStanceEnum = args.get_arg(1)
    else:
        shapeStanceEnum = spell_eldritch_blast
    essenceStance = game.get_spell_mesline(essenceStanceEnum)
    essenceStance = essenceStance.split(" ")
    essenceStance = str(essenceStance[0])
    shapeStance = game.get_spell_mesline(shapeStanceEnum)
    shapeStance = shapeStance.split(" ")
    shapeStance = str(shapeStance[1])
    evt_obj.append("Eldritch Blast Stance: {} {}".format(essenceStance, shapeStance))
    return 0

def queryAnswerEssense(attachee, args, evt_obj):
    activeEssenceStance = args.get_arg(0)
    if activeEssenceStance < spell_eldritch_blast:
        activeEssenceStance = spell_eldritch_blast
        args.set_arg(0, activeEssenceStance)
    evt_obj.return_val = activeEssenceStance
    return 0

def setEldritchBlastStance(attachee, args, evt_obj):
    stanceEnum = evt_obj.d20a.spell_data.spell_enum
    stanceSpellLevel = evt_obj.d20a.spell_data.get_spell_level()
    stanceName = game.get_spell_mesline(stanceEnum)
    attachee.float_text_line("{} activated".format(stanceName))
    if stanceEnum in range(spell_eldritch_blast, spell_frightful_blast):
        args.set_arg(1, stanceEnum)
        args.set_arg(3, stanceSpellLevel)
    elif stanceEnum in range(spell_frightful_blast, 3331):
        args.set_arg(0, stanceEnum)
        args.set_arg(2, stanceSpellLevel)
    else:
        args.set_arg(0, spell_eldritch_blast)
        args.set_arg(1, spell_eldritch_blast)
        args.set_arg(2, 1)
        args.set_arg(3, 1)
    print "Stance set"
    return 0

warlockEldritchBlast = PythonModifier("Warlock Eldritch Blast Feat", 4) #essenceStanceEnum, shapeStanceEnum, essenceStanceSpellLevel, shapeStanceSpellLevel
warlockEldritchBlast.MapToFeat("Warlock Eldritch Blast")
warlockEldritchBlast.AddHook(ET_OnBuildRadialMenuEntry , EK_NONE, radialEldritchBlast, ())
warlockEldritchBlast.AddHook(ET_OnD20PythonActionPerform, paEldritchBlastId, pythonActionTriggerSpellAction, ())
warlockEldritchBlast.AddHook(ET_OnD20PythonActionPerform, paChangeStanceId, setEldritchBlastStance, ())
warlockEldritchBlast.AddHook(ET_OnD20PythonActionPerform, paResetEldritchBlastId, resetEldritchBlast, ())
warlockEldritchBlast.AddHook(ET_OnGetTooltip, EK_NONE, eldritchBlastTooltip, ())
warlockEldritchBlast.AddHook(ET_OnD20PythonQuery, "Q_Eldritch_Essence_Stance", queryAnswerEssense, ())

## Detect Magic SLA ##
def radialDetectMagic(attachee, args, evt_obj):
    detectMagicSpellStore = PySpellStore(spell_detect_magic, 161, 0) #stat_level_warlock is wrong, needs to be ClassCode (which seems to be 128 + stat_level_[class], but how do I properly set it?)
    detectMagicSlaId = tpdp.RadialMenuEntryPythonAction(detectMagicSpellStore, D20A_PYTHON_ACTION, paDetectMagicId, spell_detect_magic, "TAG_CLASS_FEATURES_WARLOCK_DETECT_MAGIC")
    detectMagicSlaId.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Class)
    return 0

warlockDetectMagic = PythonModifier("Warlock Detect Magic Feat", 0)
warlockDetectMagic.MapToFeat("Warlock Detect Magic")
warlockDetectMagic.AddHook(ET_OnBuildRadialMenuEntry , EK_NONE, radialDetectMagic, ())
warlockDetectMagic.AddHook(ET_OnD20PythonActionPerform, paDetectMagicId, pythonActionTriggerSpellAction, ())

## Damage Reduction Cold Iron ##
def addColdIronDr(attachee, args, evt_obj):
    classLevel = attachee.stat_level_get(classEnum)
    drValue = min((classLevel+1)/4, 5) #bonus capped at level 19
    evt_obj.damage_packet.add_physical_damage_res(drValue, D20DAP_COLD, 126) #ID 126 in damage.mes is DR; D20DAP_COLD = Cold Iron!!
    return 0

warlockDamageReduction = PythonModifier("Warlock Damage Reduction Feat", 0)
warlockDamageReduction.MapToFeat("Warlock Damage Reduction")
warlockDamageReduction.AddHook(ET_OnTakingDamage, EK_NONE, addColdIronDr, ())

## Fiendish Resilience ##
def radialFiendishResilience(attachee, args, evt_obj):
    chargesLeft = args.get_arg(0)
    fiendishResilienceId = tpdp.RadialMenuEntryPythonAction("Fiendish Resilience ({}/1)".format(chargesLeft), D20A_PYTHON_ACTION, paFiendishResilienceId, 114, "TAG_CLASS_FEATURES_WARLOCK_FIENDISH_RESILIENCE")
    fiendishResilienceId.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Class)
    return 0

def activateFiendishResilience(attachee, args, evt_obj):
    chargesLeft = args.get_arg(0)
    if chargesLeft:
        attachee.float_text_line("Fiendish Resilience activated")
        classLevel = attachee.stat_level_get(classEnum)
        if classLevel < 13:
            fastHealingAmount = 1
        elif classLevel < 18:
            fastHealingAmount = 2
        else:
            fastHealingAmount = 5
        attachee.condition_add_with_args('Warlock Fiendish Resilience Effect', 20, fastHealingAmount) #duration (2min); healAmount
        chargesLeft -= 1
        args.set_arg(0, chargesLeft)
    else:
        attachee.float_text_line("Out of charges", tf_red)
    return 0

def resetFiendishResilienceCharges(attachee, args, evt_obj):
    args.set_arg(0, 1)
    return 0

warlockFiendishResilience = PythonModifier("Warlock Fiendish Resilience Feat", 1) #chargesLeft
warlockFiendishResilience.MapToFeat("Warlock Fiendish Resilience")
warlockFiendishResilience.AddHook(ET_OnBuildRadialMenuEntry , EK_NONE, radialFiendishResilience, ())
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
    return 0

def fiendishResilienceTickdown(attachee, args, evt_obj):
    args.set_arg(0, args.get_arg(0)-evt_obj.data1) # Ticking down duration
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

warlockFiendishResilienceEffect = PythonModifier("Warlock Fiendish Resilience Effect", 2) #duration, healAmount
warlockFiendishResilienceEffect.AddHook(ET_OnConditionAdd, EK_NONE, fiendishResilienceHealTick, ())
warlockFiendishResilienceEffect.AddHook(ET_OnBeginRound, EK_NONE, fiendishResilienceHealTick, ())
warlockFiendishResilienceEffect.AddHook(ET_OnBeginRound, EK_NONE, fiendishResilienceTickdown, ())
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
