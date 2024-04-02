import utils
import math
from itertools import combinations

def stv(candidates, voters, committee, k=1):
    candidates_copy = candidates[:])
    voters_copy = voters[:]
    while len(committee) < k and candidates_copy:
        for cand in candidates_copy: cand.reset_votes()

        plurality_round, _ = plurality(candidates_copy, voters_copy, k) # contains information of the plurality round
        potential_candidate, plurality_score = plurality_round[0] # get the top performing candidates and plurality score
        #print(plurality_round)
        #print(potential_candidate)
        total_votes = sum(score for _, score in plurality_round)
        #print(total_votes)
        threshold = math.floor(total_votes / (k + 1)) + 1 # formula to determine addition of candidate

        if plurality_score >= threshold:
            committee.append(potential_candidate) # potential candidate meets threshold to be added to committe
            candidates_copy = utils.remove_candidate(candidates_copy, potential_candidate) # remove the candidate from the list since they are now in committee 

        else: # the candidate with the fewest votes (worst-performing candidate) should be removed
            worst_candidate, _ = plurality_round[-1] # the round is sorted, so this has the results of the worst performing candidate
            #print(worst_candidate)
            candidates_copy = utils.remove_candidate(candidates_copy, worst_candidate) # Remove worst-performing candidate from the candidate list

        remaining_candidates = candidates_copy[:]  # copy (may be redundant)
        for voter in voters_copy: # update voter preferences based on the remaining candidates
            x, y = voter.get_position() # position needs to be used to update the preferences of each voter
            voter.update_preferences(utils.populate_preferences(x, y, remaining_candidates)) 

    return committee

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
           
    return utils.sort_candidates(candidates)[:k] # return a sorted list of candidates in descending order based on total head to head wins

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
    #k = 5
    for k in range(10,20):
        print(f"========= k: {k} ==========")
        for c,v,n in scenarios:
            print(n)
            #plurality_result = plurality(c.copy(), v.copy(), k)
            #print("Plurality Voting Strategy: " + str(plurality_result[1])) # print the results using the plurality voting strategy
            #for cand in c: cand.reset_votes() # reset votes

            #borda_result = borda(c.copy(), v.copy(), k) # store the results of the borda voting strategy
            #print("\nBorda Voting Strategy: " + str(borda_result[1])) # print the results using the borda voting strategy
            
            #for cand in c: cand.reset_votes() # reset votes

            #copeland_result = copeland(c.copy(), v.copy(), k) # store the results of the copeland voting strategy
            #print("\nCopeland Voting Strategy: " + str(copeland_result)) # print the results using the borda voting strategy

            for cand in c: cand.reset_votes() # reset votes

            stv_result = stv(c.copy(), v.copy(), [], k) # store the results of the stv voting strategy
            print("\nSTV Voting Strategy: " + str(stv_result)) # print the results using the stv voting strategy

            print("============================================================")
            #f = open(f"test_results_{n}_k{k}.txt", "a")
            #f.write(f"Plurality Results: {plurality_result[1]}\nBorda Results: {borda_result[1]}\nCopeland Results: {copeland_result}\nSTV Results: {stv_result}")
            #f.close()
if __name__=="__main__": 
    main() 