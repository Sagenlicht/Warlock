from toee import *
import eldritchBlastMod

def OnBeginSpellCast(spell):
    print "Eldritch Blast OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

############   Weapon Focus Ray Fix   ############
    spell.caster.condition_add('Wf Ray Fix', 0)
############ Weapon Focus Ray Fix End ############

def OnSpellEffect(spell):
    print "Eldritch Blast OnSpellEffect"

    spell.duration = 0 * spell.caster_level
    spellTarget = spell.target_list[0]
    essenceStanceEnum = spell.caster.d20_query("Q_Eldritch_Essence_Stance")
    damageType, saveType, saveDescriptor, specialFlag, secondaryEffect, secondaryEffectDuration = eldritchBlastMod.getModifications(essenceStanceEnum)
    if specialFlag == 1: #Requires living target for secondary effect
        if spellTarget.obj.is_category_type(mc_type_construct) or spellTarget.obj.is_category_type(mc_type_undead):
            ImmunityFlag = True
            secondaryEffect = False
        else:
            ImmunityFlag = False
    if essenceStanceEnum == spell_brimstone_blast:
        secondaryEffectDuration = (spell.caster_level/5)

    #game.particles_end(projectile.obj_get_int(obj_f_projectile_part_sys_id))
    game.particles( 'sp-Lightning Bolt', spell.target_loc )
    game.pfx_lightning_bolt( spell.caster, spell.target_loc, spell.target_loc_off_x, spell.target_loc_off_y, spell.target_loc_off_z )

    rangedTouchAttack = spell.caster.perform_touch_attack(spellTarget.obj)
    if  rangedTouchAttack & D20CAF_HIT:
        spellDamageDice = dice_new('1d6')
        if rangedTouchAttack & D20CAF_CRITICAL:
            spellDamageDice.number = min(spell.caster_level/2, 9)*2
        else:
            spellDamageDice.number = min(spell.caster_level/2, 9) #capped at CL 18
        if specialFlag == 2 and spellTarget.obj.is_category_type(mc_type_undead):
            spellTarget.spell_heal(spell.caster, spellDamageDice, D20A_CAST_SPELL, spell.id)
        else:
            spellTarget.obj.spell_damage(spell.caster, damageType, spellDamageDice, D20DAP_UNSPECIFIED, D20A_CAST_SPELL, spell.id)
        if secondaryEffect:
            if spellTarget.obj.saving_throw_spell(spell.dc, saveType, saveDescriptor, spell.caster, spell.id): #success
                spellTarget.obj.float_mesfile_line('mes\\spell.mes', 30001)
                spell.target_list.remove_target(spellTarget.obj)
            else:
                spellTarget.obj.float_mesfile_line('mes\\spell.mes', 30002)
                essenceStanceName = game.get_spell_mesline(essenceStanceEnum)
                spellTarget.obj.condition_add_with_args('sp-{}'.format(essenceStanceName), spell.id, secondaryEffectDuration)
        elif ImmunityFlag:
            spellTarget.obj.float_text_line("Unaffected due to Racial Immunity")
            spell.target_list.remove_target(spellTarget.obj)
        else:
            spell.target_list.remove_target(spellTarget.obj)
    else:
        spellTarget.obj.float_mesfile_line('mes\\spell.mes', 30007)
        game.particles('Fizzle', spellTarget.obj)
        spell.target_list.remove_target(spellTarget.obj)

    spell.spell_end(spell.id)


def OnBeginRound(spell):
    print "Eldritch Blast OnBeginRound"

#def OnBeginProjectile(spell, projectile, index_of_target):
#    print "Eldritch Blast OnBeginProjectile"
#    projectile.obj_set_int(obj_f_projectile_part_sys_id, game.particles('sp-Ray of Frost', projectile))

#def OnEndProjectile( spell, projectile, index_of_target ):
#    print "Eldritch Blast OnEndProjectile"


def OnEndSpellCast(spell):
    print "Eldritch Blast OnEndSpellCast"

