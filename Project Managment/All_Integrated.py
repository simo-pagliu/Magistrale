from graphviz import Digraph
from collections import defaultdict, deque
import pandas as pd
from input import tasks, section_colors # Import data
import matplotlib.pyplot as plt
# ----------------------------------------------------------
# This creates:
# 1. A network diagram of the project
# 2. A Gantt chart with dependencies
# 3. A resource profile
# 4. An S-curve
# -----------------------------------------------------------

# Set working directory as current directory
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# ----------------------------------------------------------

def init():
    task_lookup = {t['name']: t for t in tasks}
    children = defaultdict(list)
    for t in tasks:
        for p in t['parents']:
            children[p].append(t['name'])

    for t in tasks:
        t['ES'] = t['EF'] = 0
        t['LS'] = t['LF'] = float('inf')

    return task_lookup, children

def forward_pass(task_lookup, children):
    # Compute how many parents each task has
    in_deg = {n: len(task_lookup[n]['parents']) for n in task_lookup}
    q = deque(n for n, d in in_deg.items() if d == 0)

    while q:
        n = q.popleft()
        t = task_lookup[n]
        t['EF'] = t['ES'] + t['duration']

        for c in children[n]:
            ct = task_lookup[c]
            # Update child's ES only after all parents are processed
            ct['ES'] = max(ct['ES'], t['EF'])
            in_deg[c] -= 1
            if in_deg[c] == 0:
                q.append(c)


def backward_pass(task_lookup, children):
    proj = max(t['EF'] for t in tasks)
    
    # initialize LF and LS for all tasks
    for t in tasks:
        t['LF'] = float('inf')
        t['LS'] = float('inf')
    
    out_deg = {n: len(children[n]) for n in task_lookup}
    q = deque(n for n, d in out_deg.items() if d == 0)

    # terminal tasks get project finish time
    for n in q:
        t = task_lookup[n]
        t['LF'] = proj
        t['LS'] = proj - t['duration']
    
    while q:
        n = q.popleft()
        t = task_lookup[n]
        for p in t['parents']:
            pt = task_lookup[p]
            pt['LF'] = min(pt['LF'], t['LS'])
            pt['LS'] = pt['LF'] - pt['duration']
            out_deg[p] -= 1
            if out_deg[p] == 0:
                q.append(p)
# ----------------------------------------------------------
def network_diagram():
    dot = Digraph(comment='WBS1: Full Breakdown', format='png')
    # Set up attributes for the graph
    dot.attr(rankdir='LR', dpi='600')

    for t in tasks:
        label_name = t['name'].replace('&', '&amp;')
        slack = t['LS'] - t['ES']
        label = f'''<<table border="1" cellborder="0" cellspacing="0">
        <tr><td>{t['ES']}</td><td></td><td></td><td>{t['EF']}</td></tr>
        <tr><td>{slack}</td><td colspan="2"><b>{label_name}</b></td><td>{t['duration']}</td></tr>
        <tr><td>{t['LS']}</td><td></td><td></td><td>{t['LF']}</td></tr>
        </table>>'''
        style = 'filled, bold' if slack==0 else 'filled'
        dot.node(t['name'], label, shape='plain', style=style, fillcolor=section_colors[t['section']])

    for t in tasks:
        for p in t['parents']:
            edge_color = 'red' if (task_lookup[p]['LS']-task_lookup[p]['ES']==0 and t['LS']-t['ES']==0) else 'black'
            dot.edge(p, t['name'], color=edge_color)

    dot.render('network_diagram', view=True, cleanup=True)

def gantt():
    ROW_HEIGHT = 0.5
    X_SCALE = 0.5
    Y_SCALE = 0.5
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
    # for t in tasks:
        # for p in t['parents']:
            # dot.edge(p, t['name'], arrowhead='normal', tailport='e', headport='w')

    dot.render('gantt_with_deps', view=True, cleanup=True)

def resource_profile():
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

def s_curve():
    # Compute cumulative resource for each type
    cumulative_profile = {r: [0]*len(time_range) for r in res_types}
    for r in res_types:
        cumulative_profile[r] = [sum(profile[r][:i+1]) for i in range(len(profile[r]))]
    # Plot S-Curve
    fig, ax = plt.subplots(figsize=(10,4))
    for r in res_types:
        ax.plot(time_range, cumulative_profile[r], label=r)
    ax.set_xlabel('Time')
    ax.set_ylabel('Cumulative Usage')
    ax.set_title('S-Curve')
    ax.legend()
    plt.tight_layout()
    plt.savefig('s_curve.png', dpi=300)

# ----------------------------------------------------------
task_lookup, children = init()
forward_pass(task_lookup, children)
backward_pass(task_lookup, children)
df = pd.DataFrame([{
    'Task': t['name'],
    'Start': t['ES'],
    'Finish': t['EF'],
    **t['resources']
} for t in tasks])

df['Finish'] = df['Finish'].astype(int)
time_range = list(range(0, max(df['Finish'])+1))
res_types = list(tasks[0]['resources'].keys())
profile = {r: [0]*len(time_range) for r in res_types}
# ----------------------------------------------------------
network_diagram()
gantt()
resource_profile()
s_curve()