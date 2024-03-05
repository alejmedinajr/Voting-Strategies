import utils
import math
from itertools import combinations

def stv(candidates, voters, k=1):
    'In the single transferable voting strategy, a the candidates are voted on similar to plurality, and the one with the least votes is eliminated.'
    'This process is repeated until there is one candidate left, aka the winning candidate. This method takes advantage of the already exisitng plurality function.'
    committee = []
    while len(committee) < k:
        #for c in candidates: c.reset_votes()

        round = plurality(candidates, voters)[0]
        plurality_score = round[0][1]
        #print(plurality_score)
        #print(round[len(round)-1])
        n = 0
        for _,score in round:
            n += score
        #print(n)
        if plurality_score >= math.floor(n/(k+1)) + 1:
            committee.append(plurality(candidates, voters))
            print("new committee member")
        else: # remove lowest vote
            loser, _ = round[len(round)-1]
            candidates = utils.remove_candidate(candidates,loser) # using helper function to remove the loser candidate
            for voter in voters: # go through every voter and remove the loser from their preferences
                preferences = voter.get_preferences()
                voter.update_preferences(preferences.remove(loser))
            print("loser removed")
        
    print(committee)
    #return committee

    for cand in candidates: cand.reset_votes()

    plurality_result = plurality(candidates, voters) # the plurality rule can be used to determine which candidate should be eliminated
    loser, min_votes = plurality_result.pop() # loser and min_votes store the candidate name and number of votes
    max_votes = plurality_result[0] # the max_votes is used to keep track and make sure we do not have multiple winners
    candidate_removed = False # a boolean flag used to keep track of if we removed any candidates (initially false)
    candidates = utils.remove_candidate(candidates,loser) # using helper function to remove the loser candidate
    if min_votes < max_votes[1]: # we only want to remove the loser from the voters if it is not the same as the max_votes
        for voter in voters: # go through every voter and remove the loser from their preferences
            preferences = voter.get_preferences()
            voter.update_preferences(preferences.remove(loser))
        candidate_removed = True # set boolean flag to true since a candidate was removed from all preferences
        
    if len(candidates) > 1 and candidate_removed: return stv(candidates, voters) # make recursive call if there are sill candidates to remove
    else: return utils.sort_candidates(candidates) # at this point we have a winner candidate, return the results
   
def copeland(candidates, voters, k=1):
    'This is the voting strategy that compares all candidates in a head to head matchup, and one vote is representative'
    'of the candidate winning a matchup.'

    candidate_names = list() # create a list for quick access to candidate names
    for c in candidates: candidate_names.append(c.get_name()) # populate the list of candidate names
    comparisons = list(combinations(candidate_names, 2)) # find all matchups that will take place between candidates

    for matchup in comparisons: # each matchup of candidates needs to be taken into consideration
        c1,c2 = 0,0 # c1 and c2 represent the scores of the current candidatest that are in the current matchup
        for voter in voters: # each vote needs to be iterated through
            preferences = voter.get_preferences() # store the individual voter's preferences in a variable
            i,j = preferences.index(matchup[0]),preferences.index(matchup[1]) # i and j represent the indices of the matchup in the current preference list
            if i < j: c1 += 1 # if i < j, then candidate 1 has a higher preference rank than candidate 2
            if j < i: c2 += 1 # if j < i, then candidate 2 has a higher preference rank than candidate 1
        if c1 > c2: candidates[candidate_names.index(matchup[0])].increase_votes() # increase the votes for candidate 1 if they have more votes on a head to head comparison to candidate 2
        if c2 > c1: candidates[candidate_names.index(matchup[1])].increase_votes() # increase the votes for candidate 2 if they have more votes on a head to head comparison to candidate 1
           
    #return utils.sort_candidates(candidates)[:k] # return a sorted list of candidates in descending order based on total head to head wins
    return utils.sort_candidates(candidates) # return a sorted list of candidates in descending order based on total head to head wins

def borda(candidates, voters, k=1):
    'In the borda voting strategy, a vote is achieved by adding different points based on the candidate preferences.'
    'This function goes through a list of votes (given in ranked preferences), and assigns points to the candidate based on their rank.'
    'This is done for each vote given as a parameter. The number of points added is the priority of the candidate minus the total number of candidates minus one.'
    candidate_names = list() # list of candidate names that will be used to find the index of a specific candidate by name
    for c in candidates: candidate_names.append(c.get_name()) # adding each candidate name to the list of candidate names

    for voter in voters: # every voter needs to be iterated through
        for i in range(len(voter.get_preferences())): # each individual preference of a single voter needs to be iterated since borda relies on preference to increase the vote count
            candidates[candidate_names.index(voter.get_preferences()[i])].increase_votes(len(candidates) - i - 1) # the current candidate will have its vote count inreased by its position in the voter's preference list
         
    results = utils.sort_candidates(candidates)
    k_results = results[:k]
    return results,k_results # return sorted list of candidates in descending order based on total votes

def plurality(candidates, voters, k=1):
    'In plurality voting, a vote is achieved by being the first preference. There are no points associated for second or third ranked choice.'
    'This function goes through a list of preferences and checks if the candidate ranked first already exists in our collection of candidates.'
    'If the candidate already exists, then this is the same as someone else voting for this candidate, so the tally increases by one.'
    'If the candidate does not already exist, then this means this is the candidates first vote. By the end, the dictionary will contain the results from the votes.'
    
    for vote in voters: # every voter needs to be accounted for
        top_candidate = vote.get_preferences()[0] # the top_candidate for an individual is at the 0th index of a voters preferences list
        for candidate in candidates: # every candidate needs to be iterated through in order to determine if the current candidate is the top_candidate that should receive a vote
            if top_candidate == candidate.get_name(): # current candidate is the top candidate
                candidate.increase_votes() # increase the candidates vote count by 1 (default value)

    results = utils.sort_candidates(candidates)
    k_results = results[:k]
    return results,k_results # return sorted list of candidates in descending order based on total votes

def main(): 
    zip_dictionary = utils.populate_zipcode_dictionary("datasets/us_zipcodes.csv") # make the zipcode dictionary 
    candidates = utils.create_candidates("datasets/stadiums.csv")
    scenarios = []
    tours = [line.strip() for line in open('tours.txt')] 

    for i in range(len(tours)):
        voters = utils.populate_voters("datasets/" + tours[i], zip_dictionary, candidates)
        name = tours[i]
        scenarios.append((candidates,voters,name)) 

    #utils.create_graph(candidates, voters)
    k = 5
    for c,v,n in scenarios:
        print(n)
        #plurality_result = plurality(c.copy(), v.copy(), k)
        #print("Plurality Voting Strategy: " + str(plurality_result[1])) # print the results using the plurality voting strategy
        #print("Plurality Voting Strategy total: " + str(plurality_result[0])) # print the results using the plurality voting strategy
        
        for cand in c: cand.reset_votes() # reset votes

        #borda_result = borda(c.copy(), v.copy(), k) # store the results of the borda voting strategy
        #print("\nBorda Voting Strategy: " + str(borda_result[1])) # print the results using the borda voting strategy
        
        #for cand in c: cand.reset_votes() # reset votes

        copeland_result = copeland(candidates.copy(), voters.copy(), k) # store the results of the copeland voting strategy
        print("\nCopeland Voting Strategy: " + str(copeland_result)) # print the results using the borda voting strategy

        for cand in c: cand.reset_votes() # reset votes

        #stv_result = stv(candidates.copy(), voters.copy(), k) # store the results of the stv voting strategy
        #print("\nSTV Voting Strategy: " + str(stv_result)[1]) # print the results using the borda voting strategy

        print("============================================================")
        

if __name__=="__main__": 
    main() 