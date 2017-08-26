import json
k = {}
k['initial_state'] = 0
k['final_states'] = [4]
k['accepting_states'] = [0,1,2,3,4]
func  =[
    [0,' ',1,'0','R'],
    [1,' ',2,'0','R'],
    [2,' ',3,'1','R'],
    [3,' ',4,'1','R']
    ]
k['transition_function']=func
print json.dumps(k)
