from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Hellrime Blast"

def hellrimeBlastSpellPenaltyToDexterity(attachee, args, evt_obj):
    evt_obj.bonus_list.add(-4, 0, "Penalty: ~Hellrime Blast~[TAG_SPELLS_HELLRIME_BLAST]")
    return 0

def hellrimeBlastSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Hellrime Blast ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Hellrime Blast ({} rounds)".format(args.get_arg(1)))
    return 0

def hellrimeBlastSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("HELLRIME_BLAST"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("HELLRIME_BLAST"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def hellrimeBlastSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def hellrimeBlastSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def hellrimeBlastSpellSpellEnd(attachee, args, evt_obj):
    print "Hellrime Blast SpellEnd"
    return 0

hellrimeBlastSpell = PythonModifier("sp-Hellrime Blast", 2) # spell_id, duration
hellrimeBlastSpell.AddHook(ET_OnAbilityScoreLevel, EK_STAT_DEXTERITY, hellrimeBlastSpellPenaltyToDexterity, ())
hellrimeBlastSpell.AddHook(ET_OnGetTooltip, EK_NONE, hellrimeBlastSpellTooltip, ())
hellrimeBlastSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, hellrimeBlastSpellEffectTooltip, ())
hellrimeBlastSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, hellrimeBlastSpellSpellEnd, ())
hellrimeBlastSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, hellrimeBlastSpellHasSpellActive, ())
hellrimeBlastSpell.AddHook(ET_OnD20Signal, EK_S_Killed, hellrimeBlastSpellKilled, ())
hellrimeBlastSpell.AddSpellDispelCheckStandard()
hellrimeBlastSpell.AddSpellTeleportPrepareStandard()
hellrimeBlastSpell.AddSpellTeleportReconnectStandard()
hellrimeBlastSpell.AddSpellCountdownStandardHook()
