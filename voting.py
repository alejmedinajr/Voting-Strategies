import utils

def borda(votes):
    'In the borda voting strategy, a vote is achieved by adding different points based on the candidate preferences.'
    'This function goes through a list of votes (given in ranked preferences), and assigns points to the candidate based on their rank.'
    'This is done for each vote given as a parameter. The number of points added is the priority of the candidate minus the total number of candidates minus one.'

    candidates = {} # this dictionary will be used to keep track of the voting results.
    for vote in votes: # for each vote, the candidates priority will be used to keep track of scores
        for i in range(len(vote)): # for every vote entry, all candidates need to be iterated through
            candidate = vote[i] # candidate will contain the current candidate
            if candidate in candidates: # if the current candidate already exists, simply add a tally (or point) for them based on borda voting rules
                candidates[candidate] += len(vote) - i - 1 # update the candidates score by adding the candidates preference minus the total number of candidates minus one 
            else: # at this point the first candidate does not exist, a new element in the collection of candidates needs to be made
                candidates[candidate] = len(vote) - i - 1 # update the candidates score by adding the candidates preference minus the total number of candidates minus one 
      
    return sorted(candidates.items(), key=lambda x:x[1], reverse=True) # return the sorted results of candidates and their scores


def plurality(votes):
    'In plurality voting, a vote is achieved by being the first preference. There are no points associated for second or third ranked choice.'
    'This function goes through a list of preferences and checks if the candidate ranked first already exists in our collection of candidates.'
    'If the candidate already exists, then this is the same as someone else voting for this candidate, so the tally increases by one.'
    'If the candidate does not already exist, then this means this is the candidates first vote. By the end, the dictionary will contain the results from the votes.'
    
    candidates = {} # this dictionary will be used to keep track of the voting results.
    for vote in votes: # for each vote, the priority candidate (first choice) needs to be recorded
        first_candidate = vote[0] # votes is a list of lists, and the very first index of every list is the first choice candidate
        if first_candidate in candidates: # if the first candidate already exists, simply add a tally (or point) for them
            candidates[first_candidate] += 1 # update the candidates score by 1
        else: # at this point the first candidate does not exist, a new element in the collection of candidates needs to be made
            candidates[first_candidate] = 1 # update the candidates dictionary so this new candidate is there (with a score of one since the candiate was a first choice)
      
    return sorted(candidates.items(), key=lambda x:x[1], reverse=True) # return the sorted results of candidates and their scores

def main(): 
    votes = utils.read_votes_from_file("votes.txt") # use a helper function in order to read from the file (contains lines of voting preferences)
    print("============================================================")
    plurality_result = plurality(votes) # store the results of the plurality voting strategy
    print("Plurality Voting Strategy: " + str(plurality_result)) # print the results using the plurality voting strategy
    print("Winner: " + str(plurality_result[0])) # announce the winner since the results are not sorted
    
    borda_result = borda(votes) # store the results of the borda voting strategy
    print("\nBorda Voting Strategy: " + str(borda_result)) # print the results using the borda voting strategy
    print("Winner: " + str(borda_result[0])) # announce the winner since the results are not sorted
    
    print("============================================================")



if __name__=="__main__": 
    main() 