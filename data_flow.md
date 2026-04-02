# Music Recommender — Data Flow Diagram

```mermaid
flowchart TD
    A[(songs.csv\nid, title, artist\ngenre, mood, energy\ntempo_bpm, valence\ndanceability, acousticness)] -->|load_songs csv_path| B[List of Song Dicts\nList of Dict]

    C([UserProfile\nfavorite_genre\nfavorite_mood\ntarget_energy\nlikes_acoustic]) --> D

    B --> D{The Loop\nfor song in songs\n20 iterations}

    D -->|each song dict| E[score_song\nuser_prefs, song]

    E --> E1{genre match?\nsong.genre == user.favorite_genre}
    E1 -->|yes| E1Y[+2.0 pts]
    E1 -->|no| E1N[+0.0 pts]

    E --> E2{mood match?\nsong.mood == user.favorite_mood}
    E2 -->|yes| E2Y[+1.0 pts]
    E2 -->|no| E2N[+0.0 pts]

    E --> E3[energy similarity\n1.0 - abs song.energy - user.target_energy\nrange: 0.0 to 1.0]

    E1Y & E1N & E2Y & E2N & E3 --> F[total score\nmax possible = 4.0]

    F --> G[append to scored list\ntuple: song, score, explanation]

    G --> H{all 20 songs scored?}
    H -->|no, next song| D
    H -->|yes| I[scored.sort\nkey=score, reverse=True\nhighest first]

    I --> J[scored k\nslice top K results]

    J --> K([Output\nList of Tuple\nsong dict, float score, explanation str\nTop K Recommendations])

    style A fill:#f0f4ff,stroke:#4a6cf7
    style C fill:#fff4e6,stroke:#f7a24a
    style K fill:#e6fff0,stroke:#4af77a
    style D fill:#ffeef0,stroke:#f74a6c
    style E fill:#ffeef0,stroke:#f74a6c
    style H fill:#ffeef0,stroke:#f74a6c
```

## Single Song Journey (Example: Library Rain — song #4)

```mermaid
sequenceDiagram
    participant CSV as songs.csv
    participant LS as load_songs()
    participant LOOP as recommend_songs() loop
    participant SS as score_song()
    participant OUT as Output

    CSV->>LS: row: Library Rain, lofi, chill, energy=0.35
    LS->>LOOP: Dict {genre:lofi, mood:chill, energy:0.35}
    LOOP->>SS: score_song(user_prefs, song)
    SS->>SS: genre lofi == lofi → +2.0
    SS->>SS: mood chill == chill → +1.0
    SS->>SS: 1.0 - abs(0.35 - 0.40) = 0.95 → +0.95
    SS-->>LOOP: (score=3.95, explanation)
    LOOP->>LOOP: append (song, 3.95, explanation) to scored[]
    LOOP->>LOOP: sort all 20 scores descending
    LOOP-->>OUT: scored[:k] → Library Rain is Rank #1
```

## Score Breakdown Reference

| Points | Condition | Max |
|--------|-----------|-----|
| +2.0 | `song.genre == user.favorite_genre` | 2.0 |
| +1.0 | `song.mood == user.favorite_mood` | 1.0 |
| +0.0–1.0 | `1.0 - abs(song.energy - user.target_energy)` | 1.0 |
| | **Total possible** | **4.0** |
