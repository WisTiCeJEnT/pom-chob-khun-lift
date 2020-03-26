lift = [None, None, None]
lift[1] = {
    'queue': [],
    'status': 'OPEN',
    'going': None,
    'floor': 1}
lift[2] = {
    'queue': [],
    'status': None,
    'going': None,
    'floor': 1}

def pop_lift(lift_no):
    if lift[lift_no]:
        lift[lift_no]['queue'] = lift[lift_no]['queue'][1:]

def dist(lift_no, floor, going):
    sim = dict(lift[lift_no])
    if sim['going'] == None:
        if sim['floor'] < floor:
            sim['going'] = 'UP'
        elif sim['floor'] > floor:
            sim['going'] = 'DOWN'
        else:
            sim['going'] = going
    ans = 0
    while(sim['floor'] != floor or sim['going'] != going):
        if sim['going'] == 'DOWN':
            sim['floor'] -= 1
        else:
            sim['floor'] += 1
        if sim['floor'] == 1:
            sim['going'] = 'UP'
        if sim['floor'] == 4:
            sim['going'] = 'DOWN'
        ans += 1
    return ans

def add_queue(lift_no, floor):
    None

def new_user(floor, going):
    l1_dist = dist(lift_no=1, floor=floor, going=going)
    l2_dist = dist(lift_no=2, floor=floor, going=going)
    if(l1_dist < l2_dist):
        add_queue(1, floor)
    else:
        add_queue(2, floor)
    #print(dist(floor, going))
