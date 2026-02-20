from typing import List


class Modifier:
    """
    Represents a modification to a stat.
    Example:
        Modifier("damage", 10)        -> +10 flat damage
        Modifier("damage", 0.2, True) -> +20% damage
    """

    def __init__(self, stat: str, value: float, is_percent: bool = False):
        self.stat = stat
        self.value = value
        self.is_percent = is_percent

    def apply(self, base_value: float) -> float:
        if self.is_percent:
            return base_value * (1 + self.value)
        return base_value + self.value


class Weapon:
    def __init__(
        self,
        name: str,
        base_damage: float,
        attack_speed: float,
        crit_chance: float = 0.1,
        crit_multiplier: float = 2.0,
        strength_scaling: float = 0.5,
    ):
        # Base stats
        self.name = name
        self.base_damage = base_damage
        self.attack_speed = attack_speed
        self.crit_chance = crit_chance
        self.crit_multiplier = crit_multiplier
        self.strength_scaling = strength_scaling

        # External stats (can be linked to character)
        self.strength = 0

        # Modifiers (buffs, enchantments, debuffs)
        self.modifiers: List[Modifier] = []

    # ------------------------
    # Core Stat Calculation
    # ------------------------

    def _apply_modifiers(self, stat_name: str, value: float) -> float:
        """Applies all relevant modifiers to a stat."""
        flat_mods = []
        percent_mods = []

        for mod in self.modifiers:
            if mod.stat == stat_name:
                if mod.is_percent:
                    percent_mods.append(mod.value)
                else:
                    flat_mods.append(mod.value)

        # Apply flat first
        for value_add in flat_mods:
            value += value_add

        # Apply percent second
        for percent in percent_mods:
            value *= (1 + percent)

        return value

    # ------------------------
    # Derived Properties
    # ------------------------

    @property
    def scaled_damage(self) -> float:
        base = self.base_damage + (self.strength * self.strength_scaling)
        return self._apply_modifiers("damage", base)

    @property
    def crit_damage(self) -> float:
        return self.scaled_damage * self.crit_multiplier

    @property
    def average_hit_damage(self) -> float:
        return (
            self.scaled_damage * (1 - self.crit_chance)
            + self.crit_damage * self.crit_chance
        )

    @property
    def effective_dps(self) -> float:
        dps = self.average_hit_damage * self.attack_speed
        return self._apply_modifiers("dps", dps)

    # ------------------------
    # Utility
    # ------------------------

    def add_modifier(self, modifier: Modifier):
        self.modifiers.append(modifier)

    def remove_modifier(self, modifier: Modifier):
        self.modifiers.remove(modifier)

    def __str__(self):
        return (
            f"{self.name}\n"
            f"Damage: {self.scaled_damage:.2f}\n"
            f"Crit Damage: {self.crit_damage:.2f}\n"
            f"Effective DPS: {self.effective_dps:.2f}\n"
        )