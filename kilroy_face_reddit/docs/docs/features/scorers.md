# Scorers

Scorers are a way to evaluate posts.
You give them a post, and they return a single number representing the score.
All implemented scorers are described below.

## `RelativeScoreScorer`

This is probably the simplest scorer imaginable and the only one implemented.
It simply retrieves the score of the post
and divides it by the number of subscribers of the subreddit it was posted in.
So if a post has 10 upvotes and 2 downvotes in a subreddit with 1000 members,
it will get a score of 0.008.
