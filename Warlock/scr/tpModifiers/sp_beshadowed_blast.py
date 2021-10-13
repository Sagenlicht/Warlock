from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Beshadowed Blast"

def beshadowedBlastSpellOnConditionAdd(attachee, args, evt_obj):
    attachee.condition_add_with_args('Blindness', args.get_arg(1), args.get_arg(1))
    return 0

def beshadowedBlastSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Beshadowed Blast ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Beshadowed Blast ({} rounds)".format(args.get_arg(1)))
    return 0

def beshadowedBlastSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("BESHADOWED_BLAST"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("BESHADOWED_BLAST"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def beshadowedBlastSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def beshadowedBlastSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def beshadowedBlastSpellSpellEnd(attachee, args, evt_obj):
    print "Beshadowed Blast SpellEnd"
    return 0

beshadowedBlastSpell = PythonModifier("sp-Beshadowed Blast", 2) # spell_id, duration
beshadowedBlastSpell.AddHook(ET_OnConditionAdd, EK_NONE, beshadowedBlastSpellOnConditionAdd, ())
beshadowedBlastSpell.AddHook(ET_OnGetTooltip, EK_NONE, beshadowedBlastSpellTooltip, ())
beshadowedBlastSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, beshadowedBlastSpellEffectTooltip, ())
beshadowedBlastSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, beshadowedBlastSpellSpellEnd, ())
beshadowedBlastSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, beshadowedBlastSpellHasSpellActive, ())
beshadowedBlastSpell.AddHook(ET_OnD20Signal, EK_S_Killed, beshadowedBlastSpellKilled, ())
beshadowedBlastSpell.AddSpellDispelCheckStandard()
beshadowedBlastSpell.AddSpellTeleportPrepareStandard()
beshadowedBlastSpell.AddSpellTeleportReconnectStandard()
beshadowedBlastSpell.AddSpellCountdownStandardHook()
