from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Hideous Blow"

hideousBlowSpell = PythonModifier("sp-Hideous Blow", 2) # spell_id, duration
hideousBlowSpell.AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.spellTooltip, ())
hideousBlowSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.spellEffectTooltip, ())
hideousBlowSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
hideousBlowSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
hideousBlowSpell.AddSpellDispelCheckStandard()
hideousBlowSpell.AddSpellTeleportPrepareStandard()
hideousBlowSpell.AddSpellTeleportReconnectStandard()
hideousBlowSpell.AddSpellCountdownStandardHook()
