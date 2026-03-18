def level_from_xp(total_xp: int) -> int:
    return max(1, total_xp // 100 + 1)

