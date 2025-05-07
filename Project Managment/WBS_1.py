from graphviz import Digraph

# Create the graph
dot = Digraph(comment='WBS1: Full Breakdown', format='png')
dot.attr(rankdir='TB', size='10,12')
dot.attr(dpi='600')

# Root node
dot.node('WBS1', 'Phase Oriented WBS', shape='box', style='filled', fillcolor='#003366', fontcolor='white')

# Top-level categories
main_sections = [
    'Engineering',
    'Procurement',
    'Construction',
    'Testing'
]

for section in main_sections:
    dot.node(section, section, shape='box', style='filled', fillcolor='#005580', fontcolor='white')
    dot.edge('WBS1', section)

# Sub-sections and items
wbs_data = {
    'Engineering': {
        'Process': [
            'Chemical Process',
            'Automation Logic',
            'Mechanical Process'
        ],
        'Mechanical': [
            'BOM',
            'Technical Drawing',
            '3D Model'
        ],
        'Automation': [
            'Flowcomputer Logic',
            'Electrical/Pneumatic'
        ]
    },
    'Procurement': {
        'Critical Components': [
            'Filter',
            'Sterilizer/Mineralizer',
            'Pump'
        ],
        'Accessories': [
            'Bulk Piping',
            'Valves',
            'Flow computer',
            'Instruments'
        ]
    },
    'Construction': {
        'Mechanical Prefabrication': [
            'Steelworks',
            'Structure Prefabrication',
            'Painting Structure',
            'Piping Prefabrication',
            'Painting Piping'
        ],
        'Mechanical Erection': [
            'Piping',
            'Equipment',
            'Valves'
        ],
        'Electrical & Instrument Installation': [
            'Instruments',
            'Cables & Cabling',
            'Actuated Valve Setup',
            'Tubing'
        ]
    },
    'Testing': {
        'FATs Procedure': [
            'Equipment FAT',
            'Outside Skid FAT',
            'Assembled Skid FAT'
        ],
        'Skid': [
            'Structure',
            'Piping',
            'Observer (Third Party)',
            'Assembled Skid'
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
dot.render('WBS1', view=True)