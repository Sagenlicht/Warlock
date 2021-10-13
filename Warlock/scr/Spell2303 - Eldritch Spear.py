from toee import *

def OnBeginSpellCast(spell):
    print "Eldritch Spear OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Eldritch Spear OnSpellEffect"

    spell.duration = 0 * spell.caster_level
    spellTarget = spell.target_list[0]

    spellTarget.obj.condition_add_with_args('sp-Eldritch Spear', spell.id, spell.duration)
    spellTarget.partsys_id = game.particles('sp-Heroism', spellTarget.obj)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Eldritch Spear OnBeginRound"

def OnEndSpellCast(spell):
    print "Eldritch Spear OnEndSpellCast"

