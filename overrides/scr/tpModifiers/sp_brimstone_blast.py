from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Brimstone Blast"

def brimstoneBlastSpellOnBeginRound(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellDamageDice = dice_new('1d6')
    spellDamageDice.number = 2
    damageType = D20DT_FIRE
    spell_damage(spellPacket.caster, damageType, spellDamageDice, D20DAP_UNSPECIFIED, D20A_CAST_SPELL, args.get_arg(0))
    return

def brimstoneBlastSpellExtinguishFlames(attachee, args, evt_obj):
    attachee.float_text_line("Flames extinguished")
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def radialExtinguishFlames(attachee, args, evt_obj):
    fiendishResilienceId = tpdp.RadialMenuEntryPythonAction("Extinguish Flames", D20A_PYTHON_ACTION, brimstoneBlastExtinguishFlamesId, 0, "TAG_SPELLS_BRIMSTONE_BLAST")
    fiendishResilienceId.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Class)
    return 0

def brimstoneBlastSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Brimstone Blast ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Brimstone Blast ({} rounds)".format(args.get_arg(1)))
    return 0

def brimstoneBlastSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("BRIMSTONE_BLAST"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("BRIMSTONE_BLAST"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def brimstoneBlastSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def brimstoneBlastSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def brimstoneBlastSpellSpellEnd(attachee, args, evt_obj):
    print "Brimstone Blast SpellEnd"
    return 0

brimstoneBlastExtinguishFlamesId = 3315

brimstoneBlastSpell = PythonModifier("sp-Brimstone Blast", 2) # spell_id, duration
brimstoneBlastSpell.AddHook(ET_OnBeginRound, EK_NONE, brimstoneBlastSpellOnBeginRound, ())
brimstoneBlastSpell.AddHook(ET_OnBuildRadialMenuEntry , EK_NONE, radialExtinguishFlames, ())
brimstoneBlastSpell.AddHook(ET_OnD20PythonActionPerform, brimstoneBlastExtinguishFlamesId, brimstoneBlastSpellExtinguishFlames, ())
brimstoneBlastSpell.AddHook(ET_OnGetTooltip, EK_NONE, brimstoneBlastSpellTooltip, ())
brimstoneBlastSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, brimstoneBlastSpellEffectTooltip, ())
brimstoneBlastSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, brimstoneBlastSpellSpellEnd, ())
brimstoneBlastSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, brimstoneBlastSpellHasSpellActive, ())
brimstoneBlastSpell.AddHook(ET_OnD20Signal, EK_S_Killed, brimstoneBlastSpellKilled, ())
brimstoneBlastSpell.AddSpellDispelCheckStandard()
brimstoneBlastSpell.AddSpellTeleportPrepareStandard()
brimstoneBlastSpell.AddSpellTeleportReconnectStandard()
brimstoneBlastSpell.AddSpellCountdownStandardHook()
