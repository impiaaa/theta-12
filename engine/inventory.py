import pygame, t12, entities

currentWeaponIndex = 0
weapons = []

def changeWeapon(index):
	global currentWeaponIndex
	if index < 0 or index >= len(weapons): return
	currentWeaponIndex = index
	t12.player.weapon = weapons[index]
	t12.spam("Equip " + weapons[index].name)

def addWeapon(w):
	weapons.append(w)

def nextWeapon():
	global currentWeaponIndex
	i = currentWeaponIndex + 1
	if i >= len(weapons): i = 0
	changeWeapon(i)

def previousWeapon():
	global currentWeaponIndex
	i = currentWeaponIndex - 1
	if i < 0:
		i = max(0, len(weapons)-1)
	changeWeapon(i)
