import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def score(self, user: UserProfile, song: Song) -> float:
        """Return a numeric score for how well a song matches a user profile."""
        score = 0.0
        if song.genre == user.favorite_genre:
            score += 2.0
        if song.mood == user.favorite_mood:
            score += 1.0
        score += 1.0 - abs(song.energy - user.target_energy)
        return score

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs ranked by score for the given user."""
        ranked = sorted(self.songs, key=lambda s: self.score(user, s), reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was recommended."""
        reasons = []
        if song.genre == user.favorite_genre:
            reasons.append(f"genre match ({song.genre}, +2.0)")
        if song.mood == user.favorite_mood:
            reasons.append(f"mood match ({song.mood}, +1.0)")
        energy_sim = round(1.0 - abs(song.energy - user.target_energy), 2)
        reasons.append(f"energy similarity ({energy_sim:.2f})")
        return "Recommended because: " + ", ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return a list of dicts with numeric fields cast to int/float."""
    int_fields = {"id", "tempo_bpm"}
    float_fields = {"energy", "valence", "danceability", "acousticness", "instrumentalness", "speechiness"}
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in int_fields:
                if field in row:
                    row[field] = int(row[field])
            for field in float_fields:
                if field in row:
                    row[field] = float(row[field])
            songs.append(dict(row))
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """Score a song against user preferences; returns (score, explanation string)."""
    score = 0.0
    reasons = []

    # Genre match: +2.0 points
    if song.get("genre") == user_prefs.get("genre"):
        score += 2.0
        reasons.append(f"genre match ({song['genre']}, +2.0)")

    # Mood match: +1.0 point
    if song.get("mood") == user_prefs.get("mood"):
        score += 1.0
        reasons.append(f"mood match ({song['mood']}, +1.0)")

    # Energy similarity: up to +1.0
    energy_sim = round(1.0 - abs(song.get("energy", 0.0) - user_prefs.get("target_energy", 0.0)), 2)
    score += energy_sim
    reasons.append(f"energy similarity ({energy_sim:.2f})")

    # Tempo similarity: up to +0.5 (scaled so 60 BPM apart = 0 bonus)
    if user_prefs.get("target_tempo_bpm") and song.get("tempo_bpm"):
        tempo_sim = round(max(0.0, 1.0 - abs(song["tempo_bpm"] - user_prefs["target_tempo_bpm"]) / 60.0) * 0.5, 2)
        score += tempo_sim
        reasons.append(f"tempo similarity ({tempo_sim:.2f})")

    explanation = "Recommended because: " + " | ".join(reasons)
    return score, explanation

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs against user_prefs and return the top k as (song, score, explanation) tuples."""
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
