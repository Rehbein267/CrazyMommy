#!/usr/bin/python
# -*- coding: utf-8 -*-

from Player import Player
from Enemy import Enemy
from Background import Background


class EntityFactory(Player, Enemy, Background):
    def __init__(self):
        pass

    def get_entity(self, entity_type):
        pass
