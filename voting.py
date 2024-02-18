import utils
from itertools import combinations

def stv(candidates, voters):
    'In the single transferable voting strategy, a the candidates are voted on similar to plurality, and the one with the least votes is eliminated.'
    'This process is repeated until there is one candidate left, aka the winning candidate. This method takes advantage of the already exisitng plurality function.'
    
    for cand in candidates: cand.reset_votes()

    plurality_result = plurality(candidates, voters) # the plurality rule can be used to determine which candidate should be eliminated
    loser, min_votes = plurality_result.pop()
    max_votes = plurality_result[0]
    candidate_removed = False
    candidates = utils.remove_candidate(candidates,loser)
    if min_votes < max_votes[1]:
        for voter in voters:
            preferences = voter.get_preferences()
            voter.update_preferences(preferences.remove(loser))
        candidate_removed = True
        
    if len(candidates) > 1 and candidate_removed: return stv(candidates, voters)
    else: return utils.sort_candidates(candidates)
   
def copeland(candidates, voters):
    ''
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
           
    return utils.sort_candidates(candidates) # return a sorted list of candidates in descending order based on total head to head wins
    
def borda(candidates, voters):
    'In the borda voting strategy, a vote is achieved by adding different points based on the candidate preferences.'
    'This function goes through a list of votes (given in ranked preferences), and assigns points to the candidate based on their rank.'
    'This is done for each vote given as a parameter. The number of points added is the priority of the candidate minus the total number of candidates minus one.'
    candidate_names = list() # list of candidate names that will be used to find the index of a specific candidate by name
    for c in candidates: candidate_names.append(c.get_name()) # adding each candidate name to the list of candidate names

    for voter in voters: # every voter needs to be iterated through
        for i in range(len(voter.get_preferences())): # each individual preference of a single voter needs to be iterated since borda relies on preference to increase the vote count
            candidates[candidate_names.index(voter.get_preferences()[i])].increase_votes(len(candidates) - i - 1) # the current candidate will have its vote count inreased by its position in the voter's preference list
         
    return utils.sort_candidates(candidates) # return the sorted list of candidates in descending order based on their total votes

def plurality(candidates, voters):
    'In plurality voting, a vote is achieved by being the first preference. There are no points associated for second or third ranked choice.'
    'This function goes through a list of preferences and checks if the candidate ranked first already exists in our collection of candidates.'
    'If the candidate already exists, then this is the same as someone else voting for this candidate, so the tally increases by one.'
    'If the candidate does not already exist, then this means this is the candidates first vote. By the end, the dictionary will contain the results from the votes.'
    
    for vote in voters: # every voter needs to be accounted for
        top_candidate = vote.get_preferences()[0] # the top_candidate for an individual is at the 0th index of a voters preferences list
        for candidate in candidates: # every candidate needs to be iterated through in order to determine if the current candidate is the top_candidate that should receive a vote
            if top_candidate == candidate.get_name(): # current candidate is the top candidate
                candidate.increase_votes() # increase the candidates vote count by 1 (default value)

    return utils.sort_candidates(candidates) # return sorted list of candidates in descending order based on total votes

def main(): 
    candidates = utils.create_candidates("stadiums.csv")
    print(str(candidates))

    utils.create_graph(candidates, None) # currently no data for voters
    print("++++")
    #voters = utils.create_voters(votes)
    #for voter in voters: voter.display()

    #utils.create_graph(candidates, voters)

    print("============================================================")
    #plurality_result = plurality(votes) # store the results of the plurality voting strategy
    #plurality_result = plurality(candidates.copy(), voters.copy())
    #print("Plurality Voting Strategy: " + str(plurality_result)) # print the results using the plurality voting strategy
    #print("Plurality Winner(s): " + str(utils.filter_losers(plurality_result))) # announce the winner since the results are not sorted
    
    #for cand in candidates: cand.reset_votes()

    #borda_result = borda(candidates.copy(), voters.copy()) # store the results of the borda voting strategy
    #print("\nBorda Voting Strategy: " + str(borda_result)) # print the results using the borda voting strategy
    #print("Borda Winner(s): " + str(utils.filter_losers(borda_result))) # announce the winner since the results are not sorted
    
    #for cand in candidates: cand.reset_votes()

    #copeland_result = copeland(candidates.copy(), voters.copy()) # store the results of the copeland voting strategy
    #print("\nCopeland Voting Strategy: " + str(copeland_result)) # print the results using the copeland voting strategy
    #print("Copeland Winner(s): " + str(utils.filter_losers(copeland_result))) # announce the winner since the results are not sorted
    
    #for cand in candidates: cand.reset_votes()

    #stv_result = stv(candidates.copy(), voters.copy()) # store the results of the stv voting strategy
    #print("\nSTV Voting Strategy: " + str(stv_result)) # print the results using the stv voting strategy
    #print("STV Winner(s): " + str(utils.filter_losers(stv_result))) # announce the winner since the results are not sorted
    
    print("============================================================")
    

if __name__=="__main__": 
    main() 