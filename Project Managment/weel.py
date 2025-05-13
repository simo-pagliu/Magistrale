from graphviz import Digraph
from collections import defaultdict, deque
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------
# 1) Define tasks with resources
# ------------------------
tasks = [
    # Engineering (chain)
    {'name': 'Chemical Process',      'duration': 10, 'section': 'Engineering', 'parents': [],                     'resources': {'A':10,'B':1,'C':1,'D':1}},
    {'name': 'Automation Logic',      'duration':  8, 'section': 'Engineering', 'parents': [],   'resources': {'A':1,'B':1,'C':1,'D':1}},
    {'name': 'Mechanical Process',    'duration': 12, 'section': 'Engineering', 'parents': ['Automation Logic'],   'resources': {'A':1,'B':1,'C':1,'D':1}},
    {'name': 'BOM',                   'duration':  5, 'section': 'Engineering', 'parents': ['Automation Logic', 'Mechanical Process'], 'resources': {'A':1,'B':1,'C':1,'D':1}},
    {'name': 'Technical Drawing',     'duration':  7, 'section': 'Engineering', 'parents': ['BOM'],                'resources': {'A':1,'B':1,'C':10,'D':1}},
    {'name': '3D Model',              'duration':  9, 'section': 'Engineering', 'parents': ['Technical Drawing'],   'resources': {'A':1,'B':1,'C':1,'D':1}},
    {'name': 'Flowcomputer Logic',    'duration':  6, 'section': 'Engineering', 'parents': ['3D Model'],            'resources': {'A':1,'B':1,'C':1,'D':1}},
    {'name': 'Electrical/Pneumatic',  'duration': 10, 'section': 'Engineering', 'parents': ['Flowcomputer Logic'],  'resources': {'A':1,'B':1,'C':1,'D':1}},

    # Procurement
    {'name': 'Filter',                'duration': 15, 'section': 'Procurement', 'parents': ['Electrical/Pneumatic'], 'resources': {'A':1,'B':1,'C':1,'D':1}},
    {'name': 'Sterilizer/Mineralizer','duration': 20, 'section': 'Procurement', 'parents': ['Filter'],               'resources': {'A':1,'B':1,'C':1,'D':1}},
    {'name': 'Pump',                  'duration': 12, 'section': 'Procurement', 'parents': ['Sterilizer/Mineralizer'], 'resources': {'A':1,'B':1,'C':1,'D':1}},
    {'name': 'Bulk Piping',           'duration':  8, 'section': 'Procurement', 'parents': ['Pump'],                 'resources': {'A':1,'B':1,'C':1,'D':1}},
    {'name': 'Valves',                'duration':  5, 'section': 'Procurement', 'parents': ['Bulk Piping'],          'resources': {'A':1,'B':10,'C':1,'D':1}},
    {'name': 'Flow computer',         'duration':  7, 'section': 'Procurement', 'parents': ['Valves'],               'resources': {'A':1,'B':1,'C':1,'D':1}},
    {'name': 'Instruments',           'duration': 10, 'section': 'Procurement', 'parents': ['Flow computer'],        'resources': {'A':1,'B':1,'C':1,'D':10}},

    # Construction
    {'name': 'Steelworks',            'duration': 10, 'section': 'Construction', 'parents': ['Instruments'],          'resources': {'A':1,'B':1,'C':1,'D':1}},
    {'name': 'Structure Prefabrication','duration':12,'section':'Construction','parents':['Steelworks'],        'resources': {'A':1,'B':1,'C':1,'D':1}},
    {'name': 'Painting Structure',    'duration':  8, 'section': 'Construction', 'parents': ['Structure Prefabrication'],'resources':{'A':1,'B':1,'C':1,'D':1}},
    {'name': 'Piping Prefabrication', 'duration': 15, 'section': 'Construction', 'parents': ['Painting Structure'],   'resources':{'A':1,'B':1,'C':1,'D':1}},
    {'name': 'Painting Piping',       'duration':  7, 'section': 'Construction', 'parents': ['Piping Prefabrication'],  'resources':{'A':1,'B':1,'C':1,'D':1}},
    {'name': 'Piping',                'duration': 10, 'section': 'Construction', 'parents': ['Painting Piping'],      'resources':{'A':1,'B':1,'C':1,'D':1}},
    {'name': 'Equipment',             'duration': 12, 'section': 'Construction', 'parents': ['Piping'],               'resources':{'A':1,'B':1,'C':1,'D':1}},
    {'name': 'Valves (Const)',        'duration':  8, 'section': 'Construction', 'parents': ['Equipment'],            'resources':{'A':1,'B':1,'C':1,'D':1}},
    {'name': 'Instruments (Const)',   'duration': 15, 'section': 'Construction', 'parents': ['Valves (Const)'],      'resources':{'A':1,'B':1,'C':1,'D':1}},
    {'name': 'Cables & Cabling',      'duration': 20, 'section': 'Construction', 'parents': ['Instruments (Const)'], 'resources':{'A':1,'B':1,'C':1,'D':1}},
    {'name': 'Actuated Valve Setup',  'duration': 12, 'section': 'Construction', 'parents': ['Cables & Cabling'],     'resources':{'A':1,'B':1,'C':1,'D':1}},
    {'name': 'Tubing',                'duration': 10, 'section': 'Construction', 'parents': ['Actuated Valve Setup'], 'resources':{'A':1,'B':1,'C':1,'D':1}},

    # Testing
    {'name': 'Equipment FAT',         'duration':  5, 'section': 'Testing', 'parents': ['Tubing'],              'resources':{'A':1,'B':1,'C':1,'D':1}},
    {'name': 'Outside Skid FAT',      'duration':  7, 'section': 'Testing', 'parents': ['Equipment FAT'],       'resources':{'A':1,'B':1,'C':1,'D':1}},
    {'name': 'Assembled Skid FAT',    'duration': 10, 'section': 'Testing', 'parents': ['Outside Skid FAT'],     'resources':{'A':1,'B':1,'C':1,'D':1}},
    {'name': 'Structure Test',        'duration':  8, 'section': 'Testing', 'parents': ['Assembled Skid FAT'],   'resources':{'A':1,'B':1,'C':1,'D':1}},
    {'name': 'Piping Test',           'duration': 10, 'section': 'Testing', 'parents': ['Structure Test'],      'resources':{'A':1,'B':1,'C':1,'D':1}},
    {'name': 'Observer (Third Party)','duration': 5, 'section': 'Testing', 'parents': ['Piping Test'],         'resources':{'A':1,'B':1,'C':1,'D':1}},
    {'name': 'Assembled Skid',        'duration': 12, 'section': 'Testing', 'parents': ['Observer (Third Party)'],'resources':{'A':1,'B':1,'C':1,'D':1}},
]

# ------------------------
# 2) Build relations & init
# ------------------------
task_lookup = {t['name']: t for t in tasks}
children = defaultdict(list)
for t in tasks:
    for p in t['parents']:
        children[p].append(t['name'])

for t in tasks:
    t['ES'] = t['EF'] = 0
    t['LS'] = t['LF'] = float('inf')

# ------------------------
# 3) CPM
# ------------------------
def forward_pass():
    in_deg = {n: len(task_lookup[n]['parents']) for n in task_lookup}
    q = deque(n for n,d in in_deg.items() if d==0)
    while q:
        n = q.popleft(); t = task_lookup[n]
        t['EF'] = t['ES'] + t['duration']
        for c in children[n]:
            ct = task_lookup[c]
            ct['ES'] = max(ct['ES'], t['EF'])
            in_deg[c] -= 1
            if in_deg[c]==0: q.append(c)

def backward_pass():
    proj = max(t['EF'] for t in tasks)
    outd = {n: len(children[n]) for n in task_lookup}
    q = deque(n for n,d in outd.items() if d==0)
    for n in q:
        t = task_lookup[n]
        t['LF'] = proj; t['LS'] = proj - t['duration']
    while q:
        n = q.popleft(); t = task_lookup[n]
        for p in t['parents']:
            pt = task_lookup[p]
            pt['LF'] = min(pt['LF'], t['LS'])
            pt['LS'] = pt['LF'] - pt['duration']
            outd[p] -= 1
            if outd[p]==0: q.append(p)

forward_pass(); backward_pass()

# ------------------------
# 4) Gantt-in-Graphviz
# ------------------------
# layout params
X_SCALE, Y_SCALE, ROW_HEIGHT = 0.5, 0.5, 0.4
section_colors = {
    'Engineering': '#005580',
    'Procurement': '#0073e6',
    'Construction': '#008000',
    'Testing': '#FFA500'
}

dot = Digraph('G', engine='neato', format='png')
dot.attr(overlap='true', splines='ortho', bgcolor='white')
dot.attr('node', shape='box', fixedsize='true', height=str(ROW_HEIGHT), margin='0', pin='true')

# bucket by ES and assign rows in ES order
by_start = defaultdict(list)
for t in tasks:
    by_start[t['ES']].append(t)
row = 0
for day in sorted(by_start):
    for t in by_start[day]:
        w        = (t['EF'] - t['ES']) * X_SCALE
        x_center = t['ES'] * X_SCALE + w/2
        y_center = -row * Y_SCALE
        dot.node(
            t['name'],
            label=t['name'],
            pos=f"{x_center},{y_center}!",
            width=str(w),
            fillcolor=section_colors[t['section']],
            style='filled'
        )
        row += 1

# draw arrows from parent EF to child ES
for t in tasks:
    for p in t['parents']:
        dot.edge(p, t['name'], arrowhead='normal', tailport='e', headport='w')

dot.render('gantt_with_deps', view=True)

# ------------------------
# 5) Resource profile
# ------------------------
# Build DataFrame
df = pd.DataFrame([{
    'Task': t['name'],
    'Start': t['ES'],
    'Finish': t['EF'],
    **t['resources']
} for t in tasks])

# Compute profile
time_range = list(range(0, max(df['Finish'])+1))
res_types = list(tasks[0]['resources'].keys())
profile = {r: [0]*len(time_range) for r in res_types}
for _, row in df.iterrows():
    for r in res_types:
        for ti in range(int(row['Start']), int(row['Finish'])):
            profile[r][ti] += row[r]

# Plot & save
fig, ax = plt.subplots(figsize=(10,4))
for r in res_types:
    ax.plot(time_range, profile[r], label=r)
ax.set_xlabel('Time')
ax.set_ylabel('Usage')
ax.set_title('Resource Profile')
ax.legend()
plt.tight_layout()
plt.savefig('resource_profile.png', dpi=300)
plt.show()

# ------------------------
# 6) S-Curve
# ------------------------
# Compute cumulative duration
