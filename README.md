# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This simulation builds a content-based music recommender called **VibeFinder 1.0**. Given a user's preferred genre, mood, energy level, and acoustic taste, it scores every song in a small catalog and returns the top matches with a plain-English explanation of why each song was chosen.

---

## How The System Works

Real-world recommenders like Spotify combine two strategies: collaborative filtering, which finds patterns across millions of users ("people like you also liked this"), and content-based filtering, which analyzes the song itself ("this track has similar energy and mood to ones you played on repeat"). Our simulation focuses entirely on content-based filtering — the simpler of the two — because it only needs the song's own attributes and a single user's stated preferences, no crowd data required. The system prioritizes **genre and energy** as primary signals, with mood as a strong secondary signal. Every song in the catalog gets an independent score before any ranking happens, so the scoring logic stays clean and testable, and the ranking step can be changed without touching the score math.

### `Song` Features

| Feature | Type | Role in scoring |
|---|---|---|
| `genre` | categorical | +2.0 pts — primary style match |
| `mood` | categorical | +1.0 pts — emotional feel match |
| `energy` | float (0–1) | +0.0–1.0 pts — intensity proximity |
| `acousticness` | float (0–1) | available for future experiments |
| `tempo_bpm` | float | available for future experiments |
| `valence` | float (0–1) | available for future experiments |
| `danceability` | float (0–1) | available for future experiments |
| `title`, `artist`, `id` | string/int | display and identification only |

### `UserProfile` Fields

| Field | Type | How it's used |
|---|---|---|
| `favorite_genre` | string | matched against `song.genre` |
| `favorite_mood` | string | matched against `song.mood` |
| `target_energy` | float (0–1) | compared to `song.energy` via absolute difference |
| `likes_acoustic` | bool | reserved for future scoring weight |

### Algorithm Recipe

The finalized scoring recipe applied to every song in `data/songs.csv`:

```
score = 0.0

if song.genre == user.favorite_genre:
    score += 2.0          # Genre match — strongest signal (+2.0 max)

if song.mood == user.favorite_mood:
    score += 1.0          # Mood match — secondary signal (+1.0 max)

score += 1.0 - abs(song.energy - user.target_energy)
                          # Energy similarity — continuous 0.0–1.0

# Maximum possible score: 4.0
```

**Why these weights?**
- Genre (+2.0) is the heaviest because it defines the broadest sound category a user expects — recommending metal to a lofi listener breaks trust immediately.
- Mood (+1.0) is important but secondary — a "chill" jazz song and a "chill" lofi song both satisfy a chill mood, so mood alone is not enough.
- Energy (0.0–1.0) is continuous and always contributes, acting as a tiebreaker between songs that share genre or mood.

### Data Flow

```
Input                          Process                        Output
─────────────────────          ────────────────────────────   ─────────────────────
songs.csv                      for song in all_songs:         scored[:k]
  id, title, artist    ──▶     score = 0.0                    [(song, score, why),
  genre, mood, energy          genre match? +2.0               (song, score, why),
                               mood match?  +1.0               ...]
UserProfile            ──▶     energy sim   +0–1.0            Top-K Recommendations
  favorite_genre               ─────────────────
  favorite_mood                append (song, score, explanation)
  target_energy                sort descending
                               return top k
```

### Known Biases and Limitations

- **Genre over-prioritization:** A genre match alone adds +2.0 pts — the same as a perfect mood match plus a perfect energy match combined (1.0 + 1.0). This means a same-genre song with the wrong mood and mismatched energy can still outscore a cross-genre song with a perfect mood and perfect energy. Great songs from outside the user's favorite genre will be systematically ranked lower even if they match every other preference.
- **Mood is binary:** A "chill" vs "relaxed" distinction scores 0 — there is no partial credit for adjacent moods. This makes the system fragile when mood vocabulary in the catalog does not exactly match user input.
- **Cold-start limitation:** The system has no memory. It cannot learn from what the user actually skips or replays, so its recommendations never improve over time.
- **Small and culturally narrow catalog:** The 20 songs in `songs.csv` skew toward Western pop-adjacent genres. Users whose tastes fall outside that range will receive poor recommendations regardless of scoring weights.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

