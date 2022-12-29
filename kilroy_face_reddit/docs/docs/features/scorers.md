# Scorers

Scorers are a way to evaluate posts.
You give them a post, and they return a single number representing the score.
All implemented scorers are described below.

## `ScoreScorer`

This is probably the simplest scorer imaginable and the only one implemented.
It simply retrieves the score of the post.
So if a post has 10 upvotes and 2 downvotes, it will return 8.
