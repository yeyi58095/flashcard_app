# Avionics Flashcards

A Streamlit flashcard app for reviewing digital avionics and flight-system terms. Choose one of the ten topic units, recall a term's meaning, reveal the answer, then mark whether you knew it.

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run avionics_flashcard_app.py
```

The app reads its cards from `alias.txt`. Each bracketed heading is a selectable study unit. Entries use either `abbreviation: full name: explanation` or `term: explanation` format.

Cards marked **還不熟** are listed at the end of the session and appended to `wrongs.txt` for later review. The original `flashcard_app.py` and `flashcards.txt` files are kept as they were.
