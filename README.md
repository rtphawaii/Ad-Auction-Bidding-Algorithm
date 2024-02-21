# Ad-Auction-Bidding-Algorithm

Please read this article: 
https://medium.com/@rpang167/multi-armed-bandit-problem-and-ad-auction-78abf577579c

The following excerpt is from the article above that documents my process as a whole:

"The multi-armed bandit problem is one concerned with exploration and exploitation.

The one armed bandit was the first slot machine that could pay players automatically. Each bandit has a hidden probability of paying the user when they pull its arm.

The multi-armed bandit problem presents a solver with a given number of bandits to choose from and a budget that they are able to spend across all the bandits in a manner of their choice.

The multi-armed bandit problem is one that is top of mind for many companies as they advertise to users. Each user is akin to a bandit in that they have a certain probability of clicking an ad when it is shown to them. The advertising companies will auction off users to a number of bidders that would like to advertise to the user. How does the bidder know how much to bid?

An algorithm can choose to prioritize exploration — spreading your resources out and “exploring” when there are a lot of “bandits” or “users”. Or an algorithm can choose to prioritize exploitation — finding one “bandit” that pays well and bidding high every time it is up for auction. Every new bandit has a 50% chance of being an above average performer. A good algorithm should choose to explore when there are a lot of bandits and exploit when there are less bandits.

Here is my program that I wrote simulating an auction with multiple rounds, each round offering up a user that has an undisclosed probability of clicking an ad when shown an ad. Bidders compete with a budget of $1000 to show the user an Ad. If a User clicks the ad, add a $1 to the balance of the bidder that won. The goal of the auction is to have the highest balance possible."
