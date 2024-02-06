class Candidate:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.total_votes = 0

    def __str__(self):
        return f'Name: {self.name}\t\tXY: {(self.x,self.y)}\tTotal Votes:{self.total_votes}'
    
    def get_name(self): return self.name    
    
    def get_position(self): return (self.x,self.y)

    def get_votes(self): return self.total_votes

    def increase_votes(self, factor=1): self.total_votes += factor

    def update_position(self, new_position): self.x, self.y = new_position

    def display(self): print(str(self))

    def reset_votes(self): self.total_votes = 0
    
class Voter:
    def __init__(self, id, x, y, preferences):
        self.id = id
        self.x = x
        self.y = y
        self.preferences = preferences
    
    def __str__(self):
        return f'ID: {self.id}\t\tXY: {(self.x,self.y)}\tPreferences:{self.preferences}'
    
    def get_id(self): return self.id

    def get_position(self): return (self.x,self.y)

    def get_preferences(self): return self.preferences

    def update_preferences(self, new_preferences): self.total_votes = new_preferences

    def update_position(self, new_position): self.x, self.y = new_position

    def display(self): print(str(self))

def read_votes_from_file(filename):
    file = open(filename,"r")
    votes = [x.strip().split(',') for x in file] 
    return votes

def create_candidates(possible_candidates):
    candidates = []
    for candidate in possible_candidates:
        candidates.append(Candidate(candidate, 0,0))

    return candidates

def create_voters(votes):
    voters = []
    index = 0
    for v in votes:
        voters.append(Voter(index, 0,0, v))
        index += 1

    return voters

def sort_candidates(candidates):
    result = []
    for candidate in candidates:
        result.append((candidate.get_name(), candidate.get_votes()))
    return sorted(result, key=lambda x:x[1], reverse=True)

def filter_losers(candidates):
    result = []
    max_score = candidates[0][1]
    for candidate in candidates:
        if candidate[1] == max_score:
            result.append(candidate)
    return result

def remove_candidate(candidates, removed):
    for c in candidates:
        if c.get_name() == removed:
            candidates.remove(c)
    return candidates
