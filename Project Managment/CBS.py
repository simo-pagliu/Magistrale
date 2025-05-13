from graphviz import Digraph

# Create the graph
dot = Digraph(comment='Cost Breakdown Structure', format='png')
dot.attr(rankdir='TB', size='10,12')
dot.attr(dpi='600')

# Define the data
data = {
    'External Costs': {
        'Materials': '21,500.00 €',
        'External Engineering': '106,000.00 €',
        'Supplier': '135,600.00 €',
        'Total': '263,100.00 €'
    },
    'Internal Costs': {
        'Manpower': '26,800.00 €',
        'Internal Engineering': '7,280.00 €',
        'Total': '34,080.00 €'
    },
    'Grand Total': '297,180.00 €'
}

# Define colors
colors = {
    'External Costs': '#FFD700',  # Gold
    'Internal Costs': '#87CEEB',  # Sky Blue
    'Grand Total': '#90EE90'      # Light Green
}

# Create node for Grand Total
dot.node('Grand Total', f'Grand Total: {data["Grand Total"]}', shape='box', style='filled', fillcolor=colors['Grand Total'])

# Create nodes for External Costs
dot.node('External Costs', 'External Costs: 263,100.00 €', shape='box', style='filled', fillcolor=colors['External Costs'])
dot.edge('Grand Total', 'External Costs')
for item, cost in data['External Costs'].items():
    if item != 'Total':
        dot.node(item, f'{item}: {cost}', shape='box', style='filled', fillcolor=colors['External Costs'])
        dot.edge('External Costs', item)

# Create nodes for Internal Costs
dot.node('Internal Costs', 'Internal Costs: 34,080.00 €', shape='box', style='filled', fillcolor=colors['Internal Costs'])
dot.edge('Grand Total', 'Internal Costs')
for item, cost in data['Internal Costs'].items():
    if item != 'Total':
        dot.node(item, f'{item}: {cost}', shape='box', style='filled', fillcolor=colors['Internal Costs'])
        dot.edge('Internal Costs', item)

# Save and render
dot.render('./Project Managment/cost_breakdown_structure', view=True, cleanup=True)
