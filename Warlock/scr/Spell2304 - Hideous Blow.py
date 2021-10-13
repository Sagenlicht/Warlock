from toee import *

def OnBeginSpellCast(spell):
    print "Hideous Blow OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Hideous Blow OnSpellEffect"

    spell.duration = 0 * spell.caster_level
    spellTarget = spell.target_list[0]

    spellTarget.obj.condition_add_with_args('sp-Hideous Blow', spell.id, spell.duration)
    spellTarget.partsys_id = game.particles('sp-Heroism', spellTarget.obj)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Hideous Blow OnBeginRound"

def OnEndSpellCast(spell):
    print "Hideous Blow OnEndSpellCast"

