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

# Save and render
dot.render('./Project Managment/OBS', view=True, cleanup=True)