# Reflection: Profile Comparisons

---

## Pair 1: Lofi Focus vs Pop Workout

The lofi focus profile (energy 0.38, chill mood) surfaced quiet, instrumental tracks — Library Rain and Midnight Coding topped the list because they matched genre, mood, and energy all at once. The pop workout profile (energy 0.92, euphoric mood) shifted the entire list toward loud, fast songs. "Gym Hero" kept appearing here because it is the only pop song in the catalog with energy above 0.90, so it earns the genre bonus (+2.0) and lands near a perfect energy match. A non-programmer way to think about it: the system is essentially asking "does this song feel like what you described?" — and Gym Hero is the closest thing in the catalog to someone who said they want to feel pumped up and energetic.

The difference makes sense because energy is a continuous signal. Going from 0.38 to 0.92 is not a small shift — it flips the entire ranking. Songs that were near the bottom for the focus profile (high-energy rock, EDM) jumped to the top, and the calm lofi tracks fell away completely.

---

## Pair 2: Intense Rock vs Conflict Edge Case (metal/sad, energy 0.90)

Both profiles want high energy (0.88 vs 0.90), but the conflict profile pairs that with a "sad" mood and metal genre — a deliberately contradictory combination. For the rock profile, Storm Runner (rock/intense) scored well because genre and mood both matched. For the conflict profile, no song in the catalog is both metal and sad, so the mood bonus was never triggered for the top result. The rankings still looked reasonable on the surface, but for the wrong reason: high-energy songs floated up on energy alone, regardless of mood. This shows that the system cannot detect when a user's preferences contradict each other — it just quietly ignores the conflict and scores whatever it can.

---

## Pair 3: Unknown Genre (bossa nova) vs Neutral Energy (jazz/moody, 0.50)

These two edge cases reveal different failure modes. The unknown genre profile got zero genre bonuses for every single song, so the entire ranking collapsed to mood + energy + tempo. The results were not terrible — relaxed, medium-energy songs surfaced — but the system had no way to reward what the user actually asked for. It is like going to a restaurant and ordering a dish that is not on the menu: the waiter brings you the closest thing they have without telling you it is not what you ordered.

The neutral energy profile (0.50) had the opposite problem. Because 0.50 sits in the middle of the catalog's energy range, almost every song scored a moderate energy similarity. This flattened the differences between songs, making genre and mood the only real tiebreakers. Jazz and moody songs rose to the top, but the gap between #1 and #5 was very small — meaning a tiny change in the catalog could reshuffle the whole list unpredictably.

---

## Pair 4: Lofi Focus (original weights) vs Lofi Focus (weight shift experiment)

Running the same lofi focus profile with halved genre weight (1.0 instead of 2.0) and doubled energy weight (×2 instead of ×1) showed that the top 3 results did not change. Library Rain and Midnight Coding still dominated because they matched on every dimension — the weights barely mattered when all signals agreed. The real difference appeared at #4 and #5: cross-genre songs with close energy moved up, and the sad country song's score doubled purely on energy. This taught an important lesson: weight changes only matter at the boundary — when the catalog has no strong all-around match and the system has to choose between a weak genre match and a strong energy match. For users whose favorite genre is well-represented, the weights are almost irrelevant.
