# 🎧 Model Card: VibeFinder 1.0

---

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Goal / Task

VibeFinder picks songs that match your vibe. You tell it your favorite genre, your mood, and how energetic you want the music. It scores every song and shows you the top 5 matches with a reason for each one.

---

## 3. Data Used

- 20 songs in `data/songs.csv`
- Each song has: genre, mood, energy, tempo, and a few other audio features
- 17 genres are in the catalog (lofi, pop, rock, jazz, metal, EDM, folk, and more)
- 15 moods are in the catalog (chill, happy, intense, sad, groovy, romantic, and more)
- Most genres only have 1 song — that is a big limit
- Features like danceability and acousticness are loaded but not used in scoring yet

---

## 4. Algorithm Summary

Each song gets a score based on 4 rules:

- **Genre match → +2.0 points.** Biggest bonus. If the genre matches, the song jumps to the top.
- **Mood match → +1.0 point.** Smaller bonus for matching the feeling.
- **Energy similarity → 0 to 1.0 points.** The closer the energy, the higher the score.
- **Tempo similarity → 0 to 0.5 points.** Songs with a similar BPM get a small extra boost.

All songs get scored, then sorted from highest to lowest. The top 5 are shown with a plain-English explanation.

---

## 5. Strengths

- Lofi users get great results because lofi has 3 songs — enough to actually compare and rank
- Every result shows exactly why it was picked (genre match, mood match, energy score)
- Adding tempo as a 4th signal changed the #1 result — shows the system responds to new signals
- Unknown genres and weird inputs don't crash the app — they just score lower

---

## 6. Limitations and Bias

**The genre bonus is too powerful.**

Genre gives +2.0 points. Mood and energy together max out at 2.0. So a song that matches your genre will almost always beat every other song — even if the mood and energy are wrong.

Most genres only have 1 song. That means one song wins every time for that genre. No competition.

**A sad country song kept showing up in a chill study playlist.** "Broken Porch" had no genre match and no mood match. It floated up because its energy (0.38) was close to the target. The system can't penalize a bad match — it can only reward good ones.

**Other limits:**
- Mood must match exactly. "Chill" and "relaxed" score zero against each other even though they feel similar.
- Very calm users (energy below 0.25) can never get a perfect energy score — the quietest song in the catalog has energy 0.22.
- Five features (valence, danceability, acousticness, instrumentalness, speechiness) are collected but never used.

---

## 7. Evaluation Process

Six profiles were tested:

| Profile | Genre | Mood | Energy | Why |
|---|---|---|---|---|
| Lofi Focus | lofi | chill | 0.38 | Normal study session |
| Pop Workout | pop | euphoric | 0.92 | High-energy gym session |
| Intense Rock | rock | intense | 0.88 | Driving or venting |
| Conflict | metal | sad | 0.90 | Edge case — mood and energy fight each other |
| Unknown Genre | bossa nova | relaxed | 0.45 | Edge case — genre not in catalog |
| Neutral Energy | jazz | moody | 0.50 | Edge case — energy right in the middle |

Two weight experiments were also run. Genre was halved (2.0 → 1.0) and energy was doubled. The top 3 results didn't change. Only the bottom of the list shifted. Tempo was added as a permanent 4th signal after it changed the #1 result in the lofi profile.

**Biggest surprise:** Broken Porch (sad country) kept appearing in a chill lofi playlist. Only energy matched. Everything else was wrong. The system had no way to filter it out.

---

## 8. Intended Use and Non-Intended Use

**Use it for:**
- Learning how content-based recommenders work
- Experimenting with scoring weights and seeing what changes
- A classroom project — not a real product

**Do not use it for:**
- Real music discovery — the catalog is too small
- Replacing Spotify or Apple Music — those use millions of songs and real listening history
- Users outside Western pop-adjacent music — the catalog doesn't represent them fairly

---

## 9. Personal Reflection

**Biggest learning moment:**
I expected the scoring logic to feel "smart." It doesn't. It just adds up numbers. The moment that clicked was when Broken Porch — a sad country song — kept appearing in a chill lofi study playlist. Nothing about it matched except the energy number. That showed me that the algorithm has no concept of "wrong." It only knows how to reward, never how to penalize. Real recommenders feel smart because they have millions of songs to choose from, not because the math is smarter.

**How AI tools helped — and when I had to double-check:**
AI helped write and fix code quickly. But twice it got things wrong in ways that were hard to spot. The first was a key name mismatch — `score_song` was looking up `"favorite_genre"` but the profile used `"genre"`, so genre and mood never matched and all recommendations were energy-only. The output looked plausible, which made the bug easy to miss. The second was the reason string splitting bug — using `", "` as a separator broke inside strings like `"genre match (lofi, +2.0)"`. Both bugs only showed up when I actually ran the code and read the output carefully.

**What surprised me about simple algorithms:**
Even with just four rules and 20 songs, the results feel personal. When the lofi profile returned Library Rain and Midnight Coding at the top, it genuinely felt like a good playlist for studying. The "why" explanation next to each song made it feel even more intentional — like something thought about it. That was surprising. The algorithm didn't think at all. It just found the closest numbers.

**What I'd try next:**
I'd add genre similarity so that "ambient" and "lofi" aren't treated as completely unrelated. I'd also use the acousticness feature — it's already in the data and would let acoustic fans get meaningfully different results. Most of all, I'd grow the catalog. With only 1 song per genre for most genres, the system isn't really recommending — it's just looking things up.

---

## 10. Ideas for Improvement

1. **Genre similarity.** Right now "ambient" and "lofi" score zero against each other. A simple map of related genres would help users get better results even when their exact genre isn't in the catalog.

2. **Use acousticness and valence.** They are already loaded. Adding even a small weight for acousticness would let acoustic fans get different results than electronic fans.

3. **More songs per genre.** With 1 song per genre, the genre bonus is basically a lookup table. Adding 5–10 songs per genre would make the ranking actually meaningful.
