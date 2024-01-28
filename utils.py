def read_votes_from_file(filename):
    file = open(filename,"r")
    votes = [x.strip().split(',') for x in file] 
    return votes
