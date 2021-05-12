from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Frightful Blast"

def frightfulBlastSpellOnConditionAdd(attachee, args, evt_obj):
    attachee.float_text_line("I should be shaken")
    return 0

def frightfulBlastSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Frightful Blast ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Frightful Blast ({} rounds)".format(args.get_arg(1)))
    return 0

def frightfulBlastSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("FRIGHTFUL_BLAST"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("FRIGHTFUL_BLAST"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def frightfulBlastSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def frightfulBlastSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def frightfulBlastSpellSpellEnd(attachee, args, evt_obj):
    print "Frightful Blast SpellEnd"
    return 0

frightfulBlastSpell = PythonModifier("sp-Frightful Blast", 2) # spell_id, duration
frightfulBlastSpell.AddHook(ET_OnConditionAdd, EK_NONE, frightfulBlastSpellOnConditionAdd, ())
frightfulBlastSpell.AddHook(ET_OnGetTooltip, EK_NONE, frightfulBlastSpellTooltip, ())
frightfulBlastSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, frightfulBlastSpellEffectTooltip, ())
frightfulBlastSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, frightfulBlastSpellSpellEnd, ())
frightfulBlastSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, frightfulBlastSpellHasSpellActive, ())
frightfulBlastSpell.AddHook(ET_OnD20Signal, EK_S_Killed, frightfulBlastSpellKilled, ())
frightfulBlastSpell.AddSpellDispelCheckStandard()
frightfulBlastSpell.AddSpellTeleportPrepareStandard()
frightfulBlastSpell.AddSpellTeleportReconnectStandard()
frightfulBlastSpell.AddSpellCountdownStandardHook()
