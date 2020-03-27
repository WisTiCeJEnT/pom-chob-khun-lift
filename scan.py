lift = [None, None, None]
lift[1] = {
    'queue': [],
    'status': None,
    'going': None,
    'floor': 1}
lift[2] = {
    'queue': [],
    'status': None,
    'going': None,
    'floor': 1}

floor_light = {
    '4_DOWN': 0,
    '3_UP': 0,
    '3_DOWN': 0,
    '2_UP': 0,
    '2_DOWN': 0,
    '1_UP': 0
}

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

def add_queue(lift_no, dest): #Review again soon
    lift[lift_no]['queue'].append(dest)
    """
    if lift[lift_no]['floor'] < dest:
        if lift[lift_no]['going'] == 'UP':
            for i in range(len(lift[lift_no]['queue'])):
                if lift[lift_no]['queue'][i] > dest:
                    lift[lift_no]['queue'].insert(i, dest)
                    break
        elif lift[lift_no]['going'] == 'DOWN':
            for i in range(len(lift[lift_no]['queue'])):
                if lift[lift_no]['queue'][len(lift[lift_no]['queue'])-i-1] < dest:
                    lift[lift_no]['queue'].insert(i+1, dest)
                    break
        else:
            lift[lift_no]['queue'].append(dest)
    elif lift[lift_no]['floor'] > dest:
        if lift[lift_no]['going'] == 'UP':
            for i in range(len(lift[lift_no]['queue'])):
                if lift[lift_no]['queue'][i] > dest:
                    lift[lift_no]['queue'].insert(i, dest)
                    break
        elif lift[lift_no]['going'] == 'DOWN':
            for i in range(len(lift[lift_no]['queue'])):
                if lift[lift_no]['queue'][len(lift[lift_no]['queue'])-i-1] < dest:
                    lift[lift_no]['queue'].insert(i+1, dest)
                    break
        else:
            lift[lift_no]['queue'].append(dest)
    """

def update_lift_status(lift_no, floor):
    if floor == None:
        if lift[lift_no]['going'] == 'DOWN':
            return -1 #going down
        elif lift[lift_no]['going'] == 'UP':
            return 1 #going up
        else:
            return 0 #stop
    print("update_lift_status", lift_no)
    lift[lift_no]['floor'] = floor
    # fast dev
    floor_light[str(f"{lift[lift_no]['floor']}_UP")] = 0
    floor_light[str(f"{lift[lift_no]['floor']}_DOWN")] = 0
    queue = lift[lift_no]['queue']
    if queue:
        if queue[0] == floor:
            pop_lift(lift_no)
            lift[lift_no]['status'] = 'OPEN'
            lift[lift_no]['going'] = None
            return 0
        else:
            lift[lift_no]['status'] = 'MOVING'
            if queue[0] < floor:
                lift[lift_no]['going'] = 'DOWN'
                return -1 #going down
            elif queue[0] > floor:
                lift[lift_no]['going'] = 'UP'
                return 1 #going up
            else:
                lift[lift_no]['going'] = None
                return 0 #stop
    else:
        lift[lift_no]['status'] = None
        lift[lift_no]['going'] = None
        return 0

def new_user(floor, going):
    l1_dist = dist(lift_no=1, floor=floor, going=going)
    l2_dist = dist(lift_no=2, floor=floor, going=going)
    if(l1_dist < l2_dist):
        add_queue(1, floor)
    else:
        add_queue(2, floor)
    #print(dist(floor, going))
