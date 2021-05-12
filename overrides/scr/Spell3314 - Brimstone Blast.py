from toee import *

def OnBeginSpellCast(spell):
    print "Brimstone Blast OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Brimstone Blast OnSpellEffect"

    spell.duration = 0 * spell.caster_level
    spellTarget = spell.target_list[0]

    spell.caster.d20_send_signal("S_Essence_Stance_Change", 3314)
    spell.caster.float_text_line("Eldritch Blast changed to Brimstone Blast")

    spell.target_list.remove_target(spellTarget.obj)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Brimstone Blast OnBeginRound"

def OnEndSpellCast(spell):
    print "Brimstone Blast OnEndSpellCast"

