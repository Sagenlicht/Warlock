from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Beguiling Influence"

def beguilingInfluenceSpellSkillBonus(attachee, args, evt_obj):
    evt_obj.bonus_list.add(6, 0, "~Beguiling Influence~[TAG_SPELLS_BEGUILING_INFLUENCE]") #In Complete Arcane no bonus type is specified.
    return 0

def beguilingInfluenceSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Beguiling Influence ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Beguiling Influence ({} rounds)".format(args.get_arg(1)))
    return 0

def beguilingInfluenceSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("BEGUILING_INFLUENCE"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("BEGUILING_INFLUENCE"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def beguilingInfluenceSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def beguilingInfluenceSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def beguilingInfluenceSpellSpellEnd(attachee, args, evt_obj):
    print "Beguiling Influence SpellEnd"
    return 0

beguilingInfluenceSpell = PythonModifier("sp-Beguiling Influence", 2) # spell_id, duration
beguilingInfluenceSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_BLUFF, beguilingInfluenceSpellSkillBonus, ())
beguilingInfluenceSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_DIPLOMACY, beguilingInfluenceSpellSkillBonus, ())
beguilingInfluenceSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_INTIMIDATE, beguilingInfluenceSpellSkillBonus, ())
beguilingInfluenceSpell.AddHook(ET_OnGetTooltip, EK_NONE, beguilingInfluenceSpellTooltip, ())
beguilingInfluenceSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, beguilingInfluenceSpellEffectTooltip, ())
beguilingInfluenceSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, beguilingInfluenceSpellSpellEnd, ())
beguilingInfluenceSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, beguilingInfluenceSpellHasSpellActive, ())
beguilingInfluenceSpell.AddHook(ET_OnD20Signal, EK_S_Killed, beguilingInfluenceSpellKilled, ())
beguilingInfluenceSpell.AddSpellDispelCheckStandard()
beguilingInfluenceSpell.AddSpellTeleportPrepareStandard()
beguilingInfluenceSpell.AddSpellTeleportReconnectStandard()
beguilingInfluenceSpell.AddSpellCountdownStandardHook()
