from graphviz import Digraph

# Create the graph
dot = Digraph(comment='OBS: Organization Breakdown Structure', format='png')
dot.attr(rankdir='TB', size='10,12')
dot.attr(dpi='600')

# Root nodes
dot.node('Program Manager', 'Program Manager', shape='box', style='filled', fillcolor='#003366', fontcolor='white')
dot.node('Project Manager', 'Project Manager', shape='box', style='filled', fillcolor='#003366', fontcolor='white')
dot.edge('Program Manager', 'Project Manager')

# Top-level categories
main_sections = [
    'Technical Manager',
    'Package Manager',
    'Workshop Manager',
    'QC Manager'
]

for section in main_sections:
    dot.node(section, section, shape='box', style='filled', fillcolor='#005580', fontcolor='white')
    dot.edge('Project Manager', section)

# Sub-sections and items
wbs_data = {
    'Technical Manager': {
            'Process Engineers',
            'Mechanical Engineers',
            'Automation Engineers'
    },
    'Package Manager': {
            'Procurement Team'       
    },
    'Workshop Manager': {
            'Mechanical Team',
            'Electrical Team',
            'Pneumatic Team'
    },
    'QC Manager': {
            'Quality Control',
            'Inspection',
            'Testing'
    }
}

# Populate all nodes with unique IDs to allow repeated labels
for parent, children in wbs_data.items():
    for i, child in enumerate(children):
        child_id = f"{parent}_{i}_{child}".replace(" ", "_")
        dot.node(child_id, child, shape='box', style='filled', fillcolor='#0073e6', fontcolor='white')
        dot.edge(parent, child_id)

# Save and render
dot.render('./Project Managment/OBS', view=True, cleanup=True)