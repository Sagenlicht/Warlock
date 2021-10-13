from toee import *

def OnBeginSpellCast(spell):
    print "Eldritch Chain OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Eldritch Chain OnSpellEffect"

    spell.duration = 0 * spell.caster_level
    spellTarget = spell.target_list[0]

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Eldritch Chain OnBeginRound"

def OnEndSpellCast(spell):
    print "Eldritch Chain OnEndSpellCast"

