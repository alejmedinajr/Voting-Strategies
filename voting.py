import utils

def plurality(votes):
    'In plurality voting, a vote is achieved by being the first preference. There are no points associated for second or third ranked choice.'
    'This method goes through a list of preferences and checks if the candidate ranked first already exists in our collection of candidates.'
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
    print("Winner: " + str(max(plurality_result))) # announce the winner since the results are not sorted
    print("============================================================")



if __name__=="__main__": 
    main() 