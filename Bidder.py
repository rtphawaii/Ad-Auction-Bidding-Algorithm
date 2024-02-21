import numpy as np
class Bidder():
    """generates a bidder that bids on a user using
    an algorithm that tracks historical user win rate"""
    def __init__(self,num_users,num_rounds):
        """create a Bidder instance"""
        self.num_users=num_users
        self.num_rounds=num_rounds
        #stores remaining rounds
        self.remaining_rounds=self.num_rounds
        #stores a list of users in order of being put up for auction, multiple entries allowed
        self.listofusers=[]
        #stores the total times a user has been won in auction
        self.usertotalads={}
        #stores the win rate of users, only users that have been won are in here
        self.userwindict={}
        #stores the total spend on each user - even if the bidder did not win
        self.spendonuser={}
        #stores a list of bids in order of when they are placed
        self.bidhistory=[]
        #a list of lists containing user and price in chronological order
        self.userprice=[]
        #track steals
        self.steals={}
        #give the bidder a bidding ID - this is useful for keeping track in testing
        self.bidderid=np.random.randint(1,100)
    def __repr__(self):
        """show an ID"""
        #rather than showing location in memory we want to show a string
        return f'bidder {self.bidderid}'
    def bid(self, user_id):
        """bid on a user use a budget to explore and get info then adjust bid
        keeping a record of price increases, average pricing, round number, user click rate"""
        #add the user to list of users
        self.listofusers.append(user_id)
        #add the user and a $0 price to user price list to be updated by notify
        self.userprice.append([user_id,0])
        #count how many times the user has been auctioned
        usercount=self.listofusers.count(user_id)
        #set a standard bid size
        bidamount = 0.5
        #explorebudget is $330 across all users for the first 5% of rounds
        explorebudget=330/self.num_users
        #vary exploration by the ratio of users to the number of rounds
        #need a higher budget when users are more valuable
        exploreratio=self.num_users/self.num_rounds
        if exploreratio > .9:
            explorebudget*=0
        elif exploreratio < .9 and exploreratio>0.7:
            explorebudget*=0.5
        elif exploreratio < .7 and exploreratio>0.5:
            explorebudget*=0.7
        elif exploreratio <0.5 and exploreratio>0.3:
            explorebudget*=0.8
        #sum of personal bids for the auction so far
        totalspend=sum(self.bidhistory)
        #if in the first 5% of rounds spend the explore budget
        if totalspend<explorebudget*self.num_users and (self.num_rounds-self.remaining_rounds)<0.05*self.num_rounds:
            bidamount=explorebudget
        #if the user has been bid on more than once try to steal if bid size is increasing
        #calculate the average price paid for that user and set it as the bid amount
        if usercount>1:
            most_recent_value = None
            second_most_recent_value = None
            #Iterate through the list of user prices in chronological order
            #find the most recent price and second most recent
            for id, value in reversed(self.userprice):
                if id == user_id:
                    if most_recent_value is None:
                        most_recent_value = value
                    elif second_most_recent_value is None:
                        second_most_recent_value = value
                        break  # We've found the second most recent value, so we can exit the loop
            if second_most_recent_value is not None:
                #if the price is increasing then bid more,
                #increasing the typical bid size to the average price
                if self.userprice[-1][1]>second_most_recent_value:
                    averageprice=self.spendonuser[user_id]/usercount
                    bidamount=averageprice
                #if the price is decreasing then bid less
                elif self.userprice[-1][1]<second_most_recent_value:
                    bidamount*=0.8
        #check to see if the user has been won in auction by this bidder
        if user_id in self.userwindict.keys():
            #check the winrate of the user that is being auctioned,
            #if greater than 50% then bid more by a multiplier of up to 2
            if self.userwindict[user_id]<.5:
                #bid low on users that have a below average click rate
                bidamount*=0.2
            elif self.userwindict[user_id]==.5:
                bidamount=bidamount
            elif self.userwindict[user_id]>.5 and self.userwindict[user_id]<=.6:
                bidamount*=1.5
            elif self.userwindict[user_id]>.5 and self.userwindict[user_id]<=.6:
                bidamount*=1.7
            elif self.userwindict[user_id]>.6 and self.userwindict[user_id]<=.7:
                bidamount*=1.8
            elif self.userwindict[user_id]>.7 and self.userwindict[user_id]<=1:
                bidamount*=2
        #store the number of rounds that have passed
        rounds=self.num_rounds-self.remaining_rounds
        #how much of the auction has taken place
        completion=rounds/self.num_rounds
        #start bidding slightly higher early on in the first third to gain information on users
        #cap the max bid at $1 after the first third of the auction
        if self.remaining_rounds==self.num_rounds:
            bidamount*=1
        elif completion<=(1/3):
            bidamount*=1
        elif completion>=(1/3) and bidamount>1:
            bidamount=1
        #subtract from number of rounds
        self.remaining_rounds-=1
        #keep track of personal bid history
        self.bidhistory.append(bidamount)
        #round the bid amount
        bidamount=round(bidamount,3)
        return bidamount
    def notify(self,auction_winner,price,clicked=None):
        """At the end of the auction, notify the bidder of outcome"""
        #get the user_id - the latest one to be added to the list of users
        user_id=self.listofusers[-1]
        #update the user price for the round
        self.userprice[-1][1]=price
        #if the user exists in the price dict then add to the
        #total spend on the user and the count up for auction
        if user_id in self.spendonuser:
            self.spendonuser[user_id]+=price
        else:
            self.spendonuser[user_id]=price
        if auction_winner==True:
            #if the auction winner is in windict, add to the existing key and calculate the win rate
            #add the user to userwindict - first create a key and value if there is none, else
            if user_id in self.userwindict.keys():
                numerator=self.userwindict[user_id]*self.usertotalads[user_id]
                self.usertotalads[user_id]+=1
                self.userwindict[user_id]=(int(clicked)+numerator)/self.usertotalads[user_id]
            #if the user does not exist in windict, create a new key value then add to it
            else:
                self.usertotalads[user_id]=1
                self.userwindict[user_id]=0
                self.userwindict[user_id]=(int(clicked)/self.usertotalads[user_id])