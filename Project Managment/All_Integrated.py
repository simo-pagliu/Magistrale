from graphviz import Digraph
from collections import defaultdict, deque
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd

section_colors = {
    'Engineering': '#005580',
    'Procurement': '#0073e6',
    'Construction': '#008000',
    'Testing': '#FFA500'
}
late = False
# ----------------------------------------------------------
import pandas as pd

# Load the Excel file
df = pd.read_excel("./Project Managment/CBS.xlsx")

start_row = 4
end_row = 74

# --- Define column mappings (update these based on the actual header names) ---
column_map = {
    "name": "Unnamed: 8",
    "duration": "Unnamed: 9",
    "section": "Unnamed: 1",
    "parents": "Unnamed: 11", 
    "Materials": "Unnamed: 13",
    "External Engineering": "Unnamed: 14",
    "Regulatory Body": "Unnamed: 15",
    "Supplier": "Unnamed: 16",
    "Internal Manpower": "Unnamed: 17",
    "Internal Engineering": "Unnamed: 18"
}

# Filter the dataframe to the target rows
df = df.iloc[start_row:end_row].copy()

# Fill NaNs with appropriate defaults
df.fillna({column_map["parents"]: ''}, inplace=True)
df.fillna(0, inplace=True)

# Build the tasks list
tasks = []
for _, row in df.iterrows():
    task = {
        "name": str(row[column_map["name"]]).strip(),
        "duration": max(1, round(float(row[column_map["duration"]]))),
        "section": str(row[column_map["section"]]).strip(),
        "parents": [p.strip() for p in str(row[column_map["parents"]]).split(",") if p.strip()],
        "resources": {
            "Materials": float(row.get(column_map["Materials"], 0)),
            "External Engineering": float(row.get(column_map["External Engineering"], 0)),
            "Regulatory Body": float(row.get(column_map["Regulatory Body"], 0)),
            "Supplier": float(row.get(column_map["Supplier"], 0)),
            "Internal Manpower": float(row.get(column_map["Internal Manpower"], 0)),
            "Internal Engineering": float(row.get(column_map["Internal Engineering"], 0)),
        }
    }
    tasks.append(task)

# Output result
print(f"Loaded {len(tasks)} tasks from Excel.")

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
            ct['ES'] = max(ct['ES'], t['EF']+1)
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
            pt['LF'] = min(pt['LF'], t['LS']-1)
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
    import math
    ROW_HEIGHT = 0.5
    X_SCALE = 0.5
    Y_SCALE = 0.5
    GRID_INTERVAL = 7  # every X units
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
            w        = (t['EF'] - t['ES'] + 1) * X_SCALE
            if late == True:
                x_center = (t['LS']) * X_SCALE + w / 2
            else:
                x_center = (t['ES']) * X_SCALE + w / 2
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

    # Add background vertical dashed lines (tall thin nodes)
    max_day = max(t['EF'] for t in tasks)
    num_rows = row
    total_height = num_rows * Y_SCALE
    for x in range(0, max_day + GRID_INTERVAL, GRID_INTERVAL):
        x_center = x * X_SCALE
        grid_id = f'grid_{x}'
        dot.node(
            grid_id,
            label='',
            pos=f"{x_center},{-total_height / 2}!",
            width='0.01',
            height=str(total_height),
            style='dashed',
            color='gray',
            shape='box',
            fillcolor='white'  # prevent coloring
        )

    dot.render('gantt_with_deps', view=True, cleanup=True)

def resource_profile():
    for _, row in df.iterrows():
        for r in res_types:
            if r == 'Internal Engineering' or r == 'Internal Manpower':
                # Get task duration and distribute resources over time
                duration = int(row['Finish']) - int(row['Start'])
                for ti in range(int(row['Start']), int(row['Finish'])):
                    profile[r][ti] += row[r] / duration
            else:
                # In this case you pay at the end if the cost is low, otherwise you pay half at the beginning and half at the end
                if row[r] > 10000:
                    profile[r][int(row['Start'])] += row[r] / 2
                    profile[r][int(row['Finish'])] += row[r] / 2
                else:
                    profile[r][int(row['Finish'])] += row[r]

            # "Materials": float(row.get(column_map["Materials"], 0)),
            # "External Engineering": float(row.get(column_map["External Engineering"], 0)),
            # "Regulatory Body": float(row.get(column_map["Regulatory Body"], 0)),
            # "Supplier": float(row.get(column_map["Supplier"], 0)),
            # "Internal Manpower": float(row.get(column_map["Internal Manpower"], 0)),
            # "Internal Engineering": float(row.get(column_map["Internal Engineering"], 0)),

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
    import numpy as np
    # Compute cumulative resource for each type
    cumulative_profile = {r: [0]*len(time_range) for r in res_types}
    for r in res_types:
        cumulative_profile[r] = [sum(profile[r][:i+1]) for i in range(len(profile[r]))]
    tot = sum(np.array(cumulative_profile[r]) for r in res_types)
    # Plot S-Curve
    fig, ax = plt.subplots(figsize=(10,4))
    for r in res_types:
        ax.plot(time_range, cumulative_profile[r], label=r)
    ax.plot(time_range, tot, label='Total', color='black', linestyle='--')
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
if late: # Late start and finish
    df = pd.DataFrame([{
    'Task': t['name'],
    'Start': t['LS'],
    'Finish': t['LF'],
    **t['resources']
} for t in tasks])
else: # Early start and finish
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