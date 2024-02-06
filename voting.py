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
    'In the borda voting strategy, a vote is achieved by adding different points based on the candidate preferences.'
    'This function goes through a list of votes (given in ranked preferences), and assigns points to the candidate based on their rank.'
    'This is done for each vote given as a parameter. The number of points added is the priority of the candidate minus the total number of candidates minus one.'
    candidate_names = list()
    for c in candidates: candidate_names.append(c.get_name())
    comparisons = list(combinations(candidate_names, 2))

    for matchup in comparisons: 
        c1,c2 = 0,0
        for voter in voters:
            preferences = voter.get_preferences()
            i,j = preferences.index(matchup[0]),preferences.index(matchup[1])
            if i < j: c1 += 1
            if j < i: c2 += 1
        if c1 > c2: candidates[candidate_names.index(matchup[0])].increase_votes()
        if c2 > c1: candidates[candidate_names.index(matchup[1])].increase_votes()
           
    return utils.sort_candidates(candidates)
    
def borda(candidates, voters):
    'In the borda voting strategy, a vote is achieved by adding different points based on the candidate preferences.'
    'This function goes through a list of votes (given in ranked preferences), and assigns points to the candidate based on their rank.'
    'This is done for each vote given as a parameter. The number of points added is the priority of the candidate minus the total number of candidates minus one.'
    candidate_names = list()
    for c in candidates: candidate_names.append(c.get_name())

    for voter in voters:
        for i in range(len(voter.get_preferences())):
            candidates[candidate_names.index(voter.get_preferences()[i])].increase_votes(len(candidates) - i - 1)
         
    result = utils.sort_candidates(candidates)
    return result

def plurality(candidates, voters):
    'In plurality voting, a vote is achieved by being the first preference. There are no points associated for second or third ranked choice.'
    'This function goes through a list of preferences and checks if the candidate ranked first already exists in our collection of candidates.'
    'If the candidate already exists, then this is the same as someone else voting for this candidate, so the tally increases by one.'
    'If the candidate does not already exist, then this means this is the candidates first vote. By the end, the dictionary will contain the results from the votes.'
    
    for vote in voters:
        top_candidate = vote.get_preferences()[0]
        for candidate in candidates:
            if top_candidate == candidate.get_name():
                candidate.increase_votes()

    result = utils.sort_candidates(candidates)
    return result

def main(): 
    votes = utils.read_votes_from_file("votes.txt") # use a helper function in order to read from the file (contains lines of voting preferences)
    candidates = utils.create_candidates(votes[0])
    for candidate in candidates: candidate.display()
    
    print("++++")
    voters = utils.create_voters(votes)
    for voter in voters: voter.display()
    print("============================================================")
    #plurality_result = plurality(votes) # store the results of the plurality voting strategy
    plurality_result = plurality(candidates.copy(), voters.copy())
    print("Plurality Voting Strategy: " + str(plurality_result)) # print the results using the plurality voting strategy
    print("Plurality Winner(s): " + str(utils.filter_losers(plurality_result))) # announce the winner since the results are not sorted
    
    for cand in candidates: cand.reset_votes()

    borda_result = borda(candidates.copy(), voters.copy()) # store the results of the borda voting strategy
    print("\nBorda Voting Strategy: " + str(borda_result)) # print the results using the borda voting strategy
    print("Borda Winner(s): " + str(utils.filter_losers(borda_result))) # announce the winner since the results are not sorted
    
    for cand in candidates: cand.reset_votes()

    copeland_result = copeland(candidates.copy(), voters.copy()) # store the results of the copeland voting strategy
    print("\nCopeland Voting Strategy: " + str(copeland_result)) # print the results using the copeland voting strategy
    print("Copeland Winner(s): " + str(utils.filter_losers(copeland_result))) # announce the winner since the results are not sorted
    
    for cand in candidates: cand.reset_votes()

    stv_result = stv(candidates.copy(), voters.copy()) # store the results of the stv voting strategy
    print("\nSTV Voting Strategy: " + str(stv_result)) # print the results using the stv voting strategy
    print("STV Winner(s): " + str(utils.filter_losers(stv_result))) # announce the winner since the results are not sorted
    
    print("============================================================")

if __name__=="__main__": 
    main() 