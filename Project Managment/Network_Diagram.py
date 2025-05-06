### This automatically connects nodes if something is repeated, could be useful for network diagram
# # Populate all nodes
# for parent, sub_sections in wbs_data.items():
#     for sub_sec, children in sub_sections.items():
#         dot.node(sub_sec, sub_sec, shape='box', style='filled', fillcolor='#0073e6', fontcolor='white')
#         dot.edge(parent, sub_sec)
#         for item in children:
#             dot.node(item, item, shape='box', style='filled', fillcolor='#e6f2ff')
#             dot.edge(sub_sec, item)

# # Save and render
# dot.render('wbs1_full', view=True)