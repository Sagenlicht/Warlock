from toee import *

def OnBeginSpellCast(spell):
    print "Frightful Blast OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Frightful Blast OnSpellEffect"

    spell.duration = 0
    spellTarget = spell.target_list[0]

    spell.caster.d20_send_signal("S_Essence_Stance_Change", 3311)
    spell.caster.float_text_line("Eldritch Blast changed to Frightful Blast")

    spell.target_list.remove_target(spellTarget.obj)
    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Frightful Blast OnBeginRound"

def OnEndSpellCast(spell):
    print "Frightful Blast OnEndSpellCast"

