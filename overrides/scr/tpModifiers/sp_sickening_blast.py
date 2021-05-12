from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Sickening Blast"

def sickeningBlastSpellOnConditionAdd(attachee, args, evt_obj):
    attachee.float_text_line("I should be sickend")
    return 0

def sickeningBlastSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Sickening Blast ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Sickening Blast ({} rounds)".format(args.get_arg(1)))
    return 0

def sickeningBlastSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("SICKENING_BLAST"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("SICKENING_BLAST"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def sickeningBlastSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def sickeningBlastSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def sickeningBlastSpellSpellEnd(attachee, args, evt_obj):
    print "Sickening Blast SpellEnd"
    return 0

sickeningBlastSpell = PythonModifier("sp-Sickening Blast", 2) # spell_id, duration
sickeningBlastSpell.AddHook(ET_OnConditionAdd, EK_NONE, sickeningBlastSpellOnConditionAdd, ())
sickeningBlastSpell.AddHook(ET_OnGetTooltip, EK_NONE, sickeningBlastSpellTooltip, ())
sickeningBlastSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, sickeningBlastSpellEffectTooltip, ())
sickeningBlastSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, sickeningBlastSpellSpellEnd, ())
sickeningBlastSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, sickeningBlastSpellHasSpellActive, ())
sickeningBlastSpell.AddHook(ET_OnD20Signal, EK_S_Killed, sickeningBlastSpellKilled, ())
sickeningBlastSpell.AddSpellDispelCheckStandard()
sickeningBlastSpell.AddSpellTeleportPrepareStandard()
sickeningBlastSpell.AddSpellTeleportReconnectStandard()
sickeningBlastSpell.AddSpellCountdownStandardHook()
