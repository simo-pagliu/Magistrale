from graphviz import Digraph

# Create the graph
dot = Digraph(comment='WBS2: Full Breakdown', format='png')
dot.attr(rankdir='TB', size='10,12')
dot.attr(dpi='600')

# Root node
dot.node('WBS2', 'System Oriented WBS', shape='box', style='filled', fillcolor='#003366', fontcolor='white')

# Top-level categories
main_sections = [
    'Process System',
    'Piping System',
    'Structural System',
    'Electrical & Control System',
]

for section in main_sections:
    dot.node(section, section, shape='box', style='filled', fillcolor='#005580', fontcolor='white')
    dot.edge('WBS2', section)

# Sub-sections and items
wbs_data = {
    'Process System': {
        'Engineering': [
            'Chemical Process',
            'Automation Logic',
            'Mechanical Process',
            'Flowcomputer Logic'
        ],
        'Procurement': [
            'Filter',
            'Sterilizer/Mineralizer',
            'Pump'
        ],
        'Installation': [
            'Equipment',
            'Actuated Valve Setup',
            'Tubing'
        ],
        'Testing': [
            'Equipment FAT'
        ]
    },
    'Piping System': {
        'Engineering': [
            'Technical Drawing',
            '3D Model'
        ],
        'Procurement': [
            'Bulk Piping',
            'Valves'
        ],
        'Fabrication': [
            'Piping Prefabrication',
            'Painting Piping'
        ],
        'Installation': [
            'Piping'
        ],
        'Testing': [
            'Outside Skid FAT'
        ]
    },
    'Structural System': {
        'Engineering': [
            'BOM'
        ],
        'Fabrication': [
            'Steelworks',
            'Structure Prefabrication',
            'Painting Structure'
        ],
        'Installation': [
            'Structure',
            'Assembled Skid'
        ],
        'Testing': [
            'Observer (Third Party)'
        ]
    },
    'Electrical & Control System': {
        'Engineering': [
            'Electrical/Pneumatic'
        ],
        'Procurement': [
            'Instruments',
            'Flow computer',
            'Cables & Cabling'
        ],
        'Installation': [
            'Instruments',
            'Electrical'
        ],
        'Testing': [
            'Assembled Skid FAT'
        ]
    }
}



# Populate all nodes with unique IDs to allow repeated labels
for parent, sub_sections in wbs_data.items():
    for sub_sec, children in sub_sections.items():
        sub_sec_id = f"{parent}_{sub_sec}".replace(" ", "_")
        dot.node(sub_sec_id, sub_sec, shape='box', style='filled', fillcolor='#0073e6', fontcolor='white')
        dot.edge(parent, sub_sec_id)
        
        for i, item in enumerate(children):
            # Unique ID per item (in case of duplicate labels)
            item_id = f"{sub_sec_id}_{i}_{item}".replace(" ", "_")
            dot.node(item_id, item, shape='box', style='filled', fillcolor='#e6f2ff')
            dot.edge(sub_sec_id, item_id)

# Save and render
dot.render('./Project Managment/WBS2', view=True, cleanup=True)