from graphviz import Digraph
from collections import defaultdict, deque

##########################################################################################
# USER INPUT
# modify the following variables to customize the graph
#
#
# Create the graph
dot = Digraph(comment='WBS1: Full Breakdown', format='png')
# Set up attributes for the graph
dot.attr(rankdir='LR', dpi='600')
# Colors for the sections
colors = {
    'Engineering': '#005580',
    'Procurement': '#0073e6',
    'Construction': '#008000',
    'Testing': '#FFA500'
}
# Do you want to print the summary of tasks?
PRINT = False
# Define tasks, specify their duration, section (for coloring), and dependencies
tasks = [
    # Engineering
    {'name': 'Chemical Process',      'duration': 10, 'section': 'Engineering', 'parents': []},
    {'name': 'Automation Logic',      'duration':  8, 'section': 'Engineering', 'parents': []},
    {'name': 'Mechanical Process',    'duration': 12, 'section': 'Engineering', 'parents': []},
    {'name': 'BOM',                   'duration':  5, 'section': 'Engineering', 'parents': ['Mechanical Process', 'Automation Logic', 'Chemical Process']},
    {'name': 'Technical Drawing',     'duration':  7, 'section': 'Engineering', 'parents': ['BOM']},
    {'name': '3D Model',              'duration':  9, 'section': 'Engineering', 'parents': ['Technical Drawing']},
    {'name': 'Flowcomputer Logic',    'duration':  6, 'section': 'Engineering', 'parents': ['3D Model']},
    {'name': 'Electrical/Pneumatic',  'duration': 10, 'section': 'Engineering', 'parents': ['Flowcomputer Logic']},

    # Procurement
    {'name': 'Filter',                'duration': 15, 'section': 'Procurement', 'parents': ['Electrical/Pneumatic']},
    {'name': 'Sterilizer/Mineralizer','duration': 20, 'section': 'Procurement', 'parents': ['Filter']},
    {'name': 'Pump',                  'duration': 12, 'section': 'Procurement', 'parents': ['Sterilizer/Mineralizer']},
    {'name': 'Bulk Piping',           'duration':  8, 'section': 'Procurement', 'parents': ['Pump']},
    {'name': 'Valves',                'duration':  5, 'section': 'Procurement', 'parents': ['Bulk Piping']},
    {'name': 'Flow computer',         'duration':  7, 'section': 'Procurement', 'parents': ['Valves']},
    {'name': 'Instruments',           'duration': 10, 'section': 'Procurement', 'parents': ['Flow computer']},

    # Construction
    {'name': 'Steelworks',           'duration': 10, 'section': 'Construction', 'parents': ['Instruments']},
    {'name': 'Structure Prefabrication','duration': 12, 'section': 'Construction', 'parents': ['Steelworks']},
    {'name': 'Painting Structure',   'duration':  8, 'section': 'Construction', 'parents': ['Structure Prefabrication']},
    {'name': 'Piping Prefabrication','duration': 15, 'section': 'Construction', 'parents': ['Painting Structure']},
    {'name': 'Painting Piping',      'duration':  7, 'section': 'Construction', 'parents': ['Piping Prefabrication']},
    {'name': 'Piping',               'duration': 10, 'section': 'Construction', 'parents': ['Painting Piping']},
    {'name': 'Equipment',            'duration': 12, 'section': 'Construction', 'parents': ['Piping']},
    {'name': 'Valves (Const)',       'duration':  8, 'section': 'Construction', 'parents': ['Equipment']},
    {'name': 'Instruments (Const)',  'duration': 15, 'section': 'Construction', 'parents': ['Valves (Const)']},
    {'name': 'Cables & Cabling',     'duration': 20, 'section': 'Construction', 'parents': ['Instruments (Const)']},
    {'name': 'Actuated Valve Setup', 'duration': 12, 'section': 'Construction', 'parents': ['Cables & Cabling']},
    {'name': 'Tubing',               'duration': 10, 'section': 'Construction', 'parents': ['Actuated Valve Setup']},

    # Testing
    {'name': 'Equipment FAT',        'duration':  5, 'section': 'Testing', 'parents': ['Tubing']},
    {'name': 'Outside Skid FAT',     'duration':  7, 'section': 'Testing', 'parents': ['Equipment FAT']},
    {'name': 'Assembled Skid FAT',   'duration': 10, 'section': 'Testing', 'parents': ['Outside Skid FAT']},
    {'name': 'Structure Test',       'duration':  8, 'section': 'Testing', 'parents': ['Assembled Skid FAT']},
    {'name': 'Piping Test',          'duration': 10, 'section': 'Testing', 'parents': ['Structure Test']},
    {'name': 'Observer (Third Party)','duration':  5, 'section': 'Testing', 'parents': ['Piping Test']},
    {'name': 'Assembled Skid',       'duration': 12, 'section': 'Testing', 'parents': ['Observer (Third Party)']},
]
#
# End of USER INPUT
##########################################################################################

# Creation of the Graph
task_lookup = {t['name']: t for t in tasks}
children = defaultdict(list)
for t in tasks:
    for p in t['parents']:
        children[p].append(t['name'])

# Initialize CPM fields
for t in tasks:
    t['ES'] = 0
    t['EF'] = 0
    t['LS'] = float('inf')
    t['LF'] = float('inf')

# Forward pass
def forward_pass():
    in_deg = {name: len(task_lookup[name]['parents']) for name in task_lookup}
    queue = deque([n for n,d in in_deg.items() if d==0])
    while queue:
        n = queue.popleft()
        t = task_lookup[n]
        t['EF'] = t['ES'] + t['duration']
        for c in children[n]:
            ct = task_lookup[c]
            ct['ES'] = max(ct['ES'], t['EF'])
            in_deg[c] -= 1
            if in_deg[c] == 0:
                queue.append(c)

# Backward pass
def backward_pass():
    proj_dur = max(t['EF'] for t in tasks)
    out_deg = {name: len(children[name]) for name in task_lookup}
    queue = deque([n for n,d in out_deg.items() if d==0])
    for n in queue:
        t = task_lookup[n]
        t['LF'] = proj_dur
        t['LS'] = t['LF'] - t['duration']
    while queue:
        n = queue.popleft()
        t = task_lookup[n]
        for p in t['parents']:
            pt = task_lookup[p]
            pt['LF'] = min(pt['LF'], t['LS'])
            pt['LS'] = pt['LF'] - pt['duration']
            out_deg[p] -= 1
            if out_deg[p] == 0:
                queue.append(p)

forward_pass()
backward_pass()

for t in tasks:
    label_name = t['name'].replace('&', '&amp;')
    slack = t['LS'] - t['ES']
    label = f'''<<table border="1" cellborder="0" cellspacing="0">
      <tr><td>{t['ES']}</td><td></td><td></td><td>{t['EF']}</td></tr>
      <tr><td>{slack}</td><td colspan="2"><b>{label_name}</b></td><td>{t['duration']}</td></tr>
      <tr><td>{t['LS']}</td><td></td><td></td><td>{t['LF']}</td></tr>
    </table>>'''
    style = 'filled, bold' if slack==0 else 'filled'
    dot.node(t['name'], label, shape='plain', style=style, fillcolor=colors[t['section']])

for t in tasks:
    for p in t['parents']:
        edge_color = 'red' if (task_lookup[p]['LS']-task_lookup[p]['ES']==0 and t['LS']-t['ES']==0) else 'black'
        dot.edge(p, t['name'], color=edge_color)

dot.render('network_diagram', view=True)

# Summary printout
if PRINT:
    for t in tasks:
        print(f"{t['name']}: ES={t['ES']}, EF={t['EF']}, LS={t['LS']}, LF={t['LF']}, Slack={t['LS']-t['ES']}")
