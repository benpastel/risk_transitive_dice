
import numpy as np

faces = np.array([
  [9, 4, 4, 4, 4, 4],
  [0, 5, 5, 5, 5, 5],
  [2, 2, 2, 7, 7, 7],
  [6, 6, 6, 6, 1, 1],
  [3, 3, 3, 3, 8, 8]])

colors = np.array([
  "red",
  "green",
  "blue",
  "magenta",
  "yellow"
])
colors_list = list(colors)

def to_indices(names):
  return np.array([colors_list.index(n) for n in names], dtype=int)

def three_vs_two(attack_dice, defense_dice, verbose=False):
  a1_faces, a2_faces, a3_faces = faces[attack_dice]
  d1_faces, d2_faces = faces[defense_dice]

  attack_kills = 0
  for a1 in a1_faces:
    for a2 in a2_faces:
      for a3 in a3_faces:
        lo_a, mid_a, hi_a = sorted([a1, a2, a3])

        for d1 in d1_faces:
          for d2 in d2_faces:
            lo_d = min(d1, d2)
            hi_d = max(d1, d2)

            attack_kills += (hi_a > hi_d)
            attack_kills += (mid_a > lo_d)

  defense_kills = 2 * (6**5) - attack_kills
  ratio = attack_kills / defense_kills
  if verbose:
    print("""
      Attack colors: {}
      Defense colors: {}

      Attack kills: {}
      Defense kills: {}
      Ratio: {:.2f}
    """.format(
      colors[attack_dice], colors[defense_dice],
      attack_kills, defense_kills))
  return ratio

def three_vs_one(attack_dice, defense_die, verbose=False):
  a1_faces, a2_faces, a3_faces = faces[attack_dice]
  d_faces = faces[defense_die]

  attack_kills = 0
  for a1 in a1_faces:
    for a2 in a2_faces:
      for a3 in a3_faces:
        hi_a = max(a1, a2, a3)

        for d in d_faces:
          attack_kills += (hi_a > d)

  defense_kills = (6**4) - attack_kills
  ratio = attack_kills / defense_kills
  if verbose:
    print("{} vs {}: {:.2f}".format(
      colors[attack_dice], colors[defense_die], ratio))
  return ratio

def valid(attack_dice, defense_dice):
  attack_dice = np.array(attack_dice)
  defense_dice = np.array(defense_dice)
  for c in range(5):
    if np.sum(attack_dice == c) + np.sum(defense_dice == c) > 2:
      return False
  return True

def best_defense_three_vs_one(attack_dice, verbose=False):
  ratios = []
  for c in range(5):
    if valid(attack_dice, c):
      ratios.append(three_vs_one(attack_dice, c))
    else:
      if verbose:
        print("{} vs {}: invalid".format(colors[attack_dice], colors[c]))
      ratios.append(99)

  ok = np.count_nonzero(attack_dice == c) < 2

  best = np.argmin(ratios)
  print("Best defense is {} with {:.2f}".format(colors[best], ratios[best]))
  return ratios[best]

def best_defense_three_vs_two(attack_dice):
  best_ratio = 99
  best_dice = None
  for c1 in range(5):
    for c2 in range(5):
      defense_dice = [c1, c2]
      if valid(attack_dice, defense_dice):
        ratio = three_vs_two(attack_dice, defense_dice)
        if ratio < best_ratio:
          best_ratio = ratio
          best_dice = defense_dice
  print("defend {} with {:.2f}".format(colors[best_dice], best_ratio))
  return best_ratio

def all(single_defender):
  if single_defender:
    defense_fn = best_defense_three_vs_one
  else:
    defense_fn = best_defense_three_vs_two

  best_ratio = -99
  best_dice = set()
  for c1 in range(5):
    for c2 in range(5):
      for c3 in range(5):
        dice = [c1, c2, c3]
        if not (c1 == c2 == c3):
          print("{}:".format(colors[dice]), end=' ')
          ratio = defense_fn(dice)
          if ratio > best_ratio:
            best_dice = {tuple(sorted(dice))}
            best_ratio = ratio
          elif ratio == best_ratio:
            best_dice.add(tuple(sorted(dice)))

  print("Best attacks force ratio {:.2f}:".format( best_ratio))
  for dice in best_dice:
    print("  {}".format(colors[list(dice)]))
  return best_ratio

all(False)


