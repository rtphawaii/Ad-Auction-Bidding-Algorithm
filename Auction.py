import numpy as np
import random
class User():
    """generates a user with an ID and a probability of paying when shown an ad"""
    def __init__(self):
        """initialize"""
        #a user has a probability of paying when show ad of 0-1
        self.__probability=np.random.uniform()
        #for testing purposes we will add a random id to the user
        self.userid=np.random.randint(1,100)
    def __repr__(self):
        """return an ID instead of a location in memory"""
        #I want this to return a userid
        return f'user {self.userid}'
    def show_ad(self):
        """shows if a user clicks or not based on hidden probability"""
        result= np.random.choice([True,False],p=[self.__probability,1-self.__probability])
        return result
class Auction():
    """An auction that can have multiple rounds, 
    each with one user up for bidding among multiple bidders"""
    def __init__(self,users,bidders):
        self.users=users
        self.bidders=bidders
        #create a list of 0 balance for each bidder
        self.balances={bidder: 0 for bidder in self.bidders}
        self.round=0
        self.__bidderscore={}
    def execute_round(self):
        """choose a random user, accept a valid bid, find a second price and winner, 
        show ad to user, notify all bidders"""
        #create an empty list that will store list of bids from each bidder
        bidlist={}
        #choose a random user from the list of users
        choice=np.random.choice(np.arange(len(self.users)))
        user=self.users[choice]
        #accept a bid from the bidders, for each bidder what is their bid for the userID?
        for bidder in self.bidders:
            #disqualify the bidder if theyre equal to or below $1000
            if self.balances[bidder] <=(-1000):
                self.bidders.remove(bidder)
            #get the bid from the bidder and add it to 
            #the bidlist dictionary with the bidder as the key
            bidlist[bidder]=bidder.bid(user)
            #check what the balance will be of the bidder after bidding
            balanceafterbid=self.balances[bidder]-bidlist[bidder]
            #if the balance will be below or equal to -1000 then they can only
            #bid what is left in their balance
            if balanceafterbid<=(-1000):
                bidlist[bidder]=1000+self.balances[bidder]
        #from the list of bids select the bid values
        bids = list(bidlist.values())
        # Sort the list of bids in descending order
        sorted_bids = sorted(bids, reverse=True)
        # Get the second-highest bid, if index error then 
        #the auction is over, only one bidder left
        # also get the highest bid
        try:
            sellingprice = sorted_bids[1]
            highestbid=sorted_bids[0]
        except IndexError:
            return
        #now refer back to the bidlist and see who bid the highest bid, including ties
        bid_winners = [key for key, value in bidlist.items() if value == highestbid]
        #now select a random person from the bid_winners
        bid_winner = random.choice(bid_winners)
        #create a list of those that lost
        bid_losers = [key for key, value in bidlist.items() if key!=bid_winner]
        #run the user.show_ad and see if it is a winner or not
        adresult=self.users[choice].show_ad()
        #notify the bidder the results with the following arguements: auction_winner,price,clicked
        bid_winner.notify(True,sellingprice,adresult)
        #notify the losers that they lost, and the selling price, and default the adresult to none
        for bid_loser in bid_losers:
            bid_loser.notify(False,sellingprice,None)
        #add one to the balance of the winner if the user clicked
        if adresult:
            self.balances[bid_winner]+=1
        #subtract the second highest bid from the users balance that bid enough to win
        self.balances[bid_winner]-=sellingprice
        #add the bidder and the result to the bidder score
        if bid_winner in self.__bidderscore.keys():
            self.__bidderscore[bid_winner]+=int(adresult)
        else:
            self.__bidderscore[bid_winner]=int(adresult)
        #show everyone their balances
        self.__bidderscore = dict(sorted(self.__bidderscore.items(), key=lambda item: item[1],reverse=True))
        #add one to the round counter
        self.round+=1


# In[ ]:




