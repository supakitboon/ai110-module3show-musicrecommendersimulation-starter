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

    # --- Primary taste profile: late-night focus session ---
    # High instrumentalness + low speechiness = no distracting vocals
    # Low energy + chill mood = calm, sustained attention
    # High acousticness = warm, organic sound over harsh electronic
    user_prefs = {
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

    # --- Alternate profile A: high-energy workout ---
    # Uncomment to test against primary profile results
    # user_prefs = {
    #     "genre":             "edm",
    #     "mood":              "intense",
    #     "target_energy":     0.95,
    #     "target_valence":    0.80,
    #     "target_tempo_bpm":  138,
    #     "likes_acoustic":    False,
    #     "wants_vocals":      False,
    #     "target_instrumentalness": 0.60,
    #     "target_speechiness":      0.04,
    # }

    # --- Alternate profile B: rainy afternoon with vocals ---
    # Uncomment to test against primary profile results
    # user_prefs = {
    #     "genre":             "r&b",
    #     "mood":              "romantic",
    #     "target_energy":     0.55,
    #     "target_valence":    0.65,
    #     "target_tempo_bpm":  88,
    #     "likes_acoustic":    True,
    #     "wants_vocals":      True,
    #     "target_instrumentalness": 0.05,
    #     "target_speechiness":      0.12,
    # }

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
