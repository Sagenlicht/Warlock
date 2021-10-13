from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Beguiling Influence"

beguilingInfluenceSpell = PythonModifier("sp-Beguiling Influence", 2) # spell_id, duration
beguilingInfluenceSpell.AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.spellTooltip, ())
beguilingInfluenceSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.spellEffectTooltip, ())
beguilingInfluenceSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
beguilingInfluenceSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
beguilingInfluenceSpell.AddSpellDispelCheckStandard()
beguilingInfluenceSpell.AddSpellTeleportPrepareStandard()
beguilingInfluenceSpell.AddSpellTeleportReconnectStandard()
beguilingInfluenceSpell.AddSpellCountdownStandardHook()
