"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # -------------------------------------------------------
    # PROFILE 1: Late-night focus session (PRIMARY)
    # Low energy + chill lofi = calm, sustained attention
    # -------------------------------------------------------
    profile_lofi_focus = {
        "genre":             "lofi",
        "mood":              "chill",
        "target_energy":     0.38,
        "target_valence":    0.58,
        "target_tempo_bpm":  76,
        "likes_acoustic":    True,
        "wants_vocals":      False,
        "target_instrumentalness": 0.85,
        "target_speechiness":      0.04,
    }

    # -------------------------------------------------------
    # PROFILE 2: High-energy pop workout
    # Max energy + euphoric pop = pump-up gym session
    # -------------------------------------------------------
    profile_pop_workout = {
        "genre":             "pop",
        "mood":              "euphoric",
        "target_energy":     0.92,
        "target_valence":    0.88,
        "target_tempo_bpm":  130,
        "likes_acoustic":    False,
        "wants_vocals":      True,
        "target_instrumentalness": 0.05,
        "target_speechiness":      0.08,
    }

    # -------------------------------------------------------
    # PROFILE 3: Deep intense rock
    # High energy + angry rock = driving or venting session
    # -------------------------------------------------------
    profile_intense_rock = {
        "genre":             "rock",
        "mood":              "intense",
        "target_energy":     0.88,
        "target_valence":    0.35,
        "target_tempo_bpm":  148,
        "likes_acoustic":    False,
        "wants_vocals":      True,
        "target_instrumentalness": 0.10,
        "target_speechiness":      0.07,
    }

    # -------------------------------------------------------
    # EDGE CASE A: Conflicting energy vs mood
    # energy=0.9 (intense) but mood=sad — does a sad metal
    # song beat a cheerful pop song? Score won't penalise the
    # mood conflict, so high-energy sad songs float to the top.
    # -------------------------------------------------------
    profile_conflict_energy_mood = {
        "genre":             "metal",
        "mood":              "sad",
        "target_energy":     0.90,
        "target_valence":    0.20,
        "target_tempo_bpm":  160,
        "likes_acoustic":    False,
        "wants_vocals":      True,
        "target_instrumentalness": 0.15,
        "target_speechiness":      0.06,
    }

    # -------------------------------------------------------
    # EDGE CASE B: Genre that doesn't exist in the dataset
    # No song will ever earn the +2.0 genre bonus, so the
    # entire ranking collapses to mood + energy similarity only.
    # -------------------------------------------------------
    profile_unknown_genre = {
        "genre":             "bossa nova",
        "mood":              "relaxed",
        "target_energy":     0.45,
        "target_valence":    0.70,
        "target_tempo_bpm":  90,
        "likes_acoustic":    True,
        "wants_vocals":      True,
        "target_instrumentalness": 0.20,
        "target_speechiness":      0.06,
    }

    # -------------------------------------------------------
    # EDGE CASE C: Perfectly neutral energy (0.5)
    # Every song gets a moderate energy similarity score,
    # so genre/mood matches dominate the ranking completely.
    # -------------------------------------------------------
    profile_neutral_energy = {
        "genre":             "jazz",
        "mood":              "moody",
        "target_energy":     0.50,
        "target_valence":    0.50,
        "target_tempo_bpm":  100,
        "likes_acoustic":    True,
        "wants_vocals":      False,
        "target_instrumentalness": 0.50,
        "target_speechiness":      0.05,
    }

    # --- Switch the active profile here to test each one ---
    user_prefs = profile_lofi_focus

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 40)
    print("   TOP MUSIC RECOMMENDATIONS")
    print("=" * 40)
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        reasons = explanation.replace("Recommended because: ", "").split(" | ")
        print(f"\n#{i}  {song['title']} by {song['artist']}")
        print(f"    Score : {score:.2f}")
        print(f"    Genre : {song['genre']}  |  Mood: {song['mood']}")
        print("    Why   :")
        for reason in reasons:
            print(f"            • {reason}")
    print("\n" + "=" * 40)


if __name__ == "__main__":
    main()
