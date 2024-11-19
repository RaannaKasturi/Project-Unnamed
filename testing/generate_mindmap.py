from graphviz import Digraph
from cairosvg import svg2pdf
import re
import random

def parse_markdown_to_dict(md_text):
    lines = md_text.strip().splitlines()
    mindmap = {}
    stack = []
    for line in lines:
        heading_match = re.match(r'^(#{1,6})\s+(.*)', line)
        bullet_match = re.match(r'^\s*-\s+(.*)', line)
        if heading_match:
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()
            node = {'title': title, 'children': []}
            while len(stack) >= level:
                stack.pop()
            if stack:
                stack[-1]['children'].append(node)
            else:
                mindmap = node  
            stack.append(node)
        elif bullet_match and stack:
            stack[-1]['children'].append({'title': bullet_match.group(1), 'children': []})
    return mindmap

generated_colors = set()

def generate_random_color():
    """Generate a random color that hasn't been generated before."""
    while True:
        # Generate a random color in hex format
        color = "#{:02x}{:02x}{:02x}".format(random.randint(128, 255), random.randint(128, 255), random.randint(128, 255))
        # If the color is not in the set, it's unique
        if color not in generated_colors:
            generated_colors.add(color)  # Add the color to the set of generated colors
            return color  # Return the unique color
        else:
            continue  # Try again

def brighten_color(color, factor=0.15):
    """Brighten the color by a certain factor (default 10%)"""
    # Remove the '#' symbol
    color = color.lstrip('#')
    
    # Convert hex to RGB
    r, g, b = [int(color[i:i+2], 16) for i in (0, 2, 4)]
    
    # Increase each component by the factor, but clamp to 255
    r = min(255, int(r * (1 + factor)))
    g = min(255, int(g * (1 + factor)))
    b = min(255, int(b * (1 + factor)))
    
    # Convert back to hex
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def add_nodes_to_graph(graph, node, parent_id=None, font_size=9, parent_color=None):
    node_id = str(id(node))
    title = node['title']
    if parent_color is None:
        node_color = "#ADD8E6"  # Light Blue for the main heading
        border_color = "#000000"  # Dark Blue border for the main heading
        parent_color = "#ADD8E6"
    elif parent_color == "#ADD8E6":
        node_color = generate_random_color()
        border_color = "#808080"
        parent_color = node_color
    else:
        # Child node and its descendants with the same random color
        node_color = brighten_color(parent_color, factor=0.15)
        border_color = "#808080"
    # Check for markdown links
    url_match = re.search(r'\[(.*?)\]\((.*?)\)', title)
    if url_match:
        prefix_text = title[:url_match.start()].strip()
        display_text = url_match.group(1)
        url = url_match.group(2)
        
        label = f'{prefix_text} {display_text}'
        graph.node(node_id, label=label, shape="box", style="rounded,filled", color=border_color, fontcolor="black", fillcolor=node_color, href=url, tooltip=title, fontsize=str(font_size))
    else:
        graph.node(node_id, title, shape="box", style="rounded,filled", color=border_color, fontcolor="black", fillcolor=node_color, tooltip=title, fontsize=str(font_size))
    
    if parent_id:
        graph.edge(parent_id, node_id)

    # Recurse to children, passing down color for the child and its descendants
    for child in node.get('children', []):
        # Assign a random color to each child node (no inheritance from parent)
        add_nodes_to_graph(graph, child, node_id, font_size=max(8, font_size - 1), parent_color=parent_color)

def generate_mindmap_pdf(svg_file):
    pdf_file = svg_file.replace(".svg", ".pdf")
    svg2pdf(file_obj=open(svg_file, "rb"), write_to=pdf_file)
    return pdf_file

def generate_mindmap_svg(md_text):
    mindmap_dict = parse_markdown_to_dict(md_text)
    root_title = mindmap_dict.get('title', 'Mindmap')
    sanitized_title = re.sub(r'[^a-zA-Z0-9_\-]', '', root_title.replace(" ", ""))
    output_filename = f"{sanitized_title}_mindmap.svg"
    graph = Digraph(format='svg')
    graph.attr(rankdir='LR', size='10,10!', pad="0.5", margin="0.2", ratio="auto")
    graph.attr('node', fontname="Arial", fontsize="9")
    add_nodes_to_graph(graph, mindmap_dict)
    svg_content = graph.pipe(format='svg').decode('utf-8')
    # Replace %3 with the sanitized filename in the SVG content
    svg_content = svg_content.replace("%3", root_title)
    # Save the modified SVG content to a file
    with open(output_filename, 'w') as f:
        f.write(svg_content)
    return output_filename

def generate_mindmap(md_text):
    mindmap_svg = generate_mindmap_svg(md_text)
    mindmap_pdf = generate_mindmap_pdf(mindmap_svg)
    return mindmap_svg, mindmap_pdf

# md = '''
# # Nucleic Acids Research: Updates to SAbDab and SAbDab-nano

# ## Introduction

# - **Antibodies in the Age of Biotherapeutics**
#   - Antibodies are fundamental components of the immune system
#   - Represent the largest class of biotherapeutics
#   - Ability to bind to antigen targets with high affinity and specificity makes them promising candidates for development of therapeutic antibodies against various targets, including cancer, virus, and other diseases.

# ## Updates to Data Annotation

# - **Search Interface**
#   - SAbDab can now be searched via a Flask app served by a fast SQL backend
#   - Structures can be searched based on experimental method, resolution, species, type of antigen, presence of affinity values, and presence of amino acid residues at specific sequence positions defined using the Chothia numbering scheme.
# - **Auxiliary Databases**
#   - Thera-SAbDab and CoV-AbDab databases contain antibody sequence information linking to relevant entries in SAbDab
#   - These databases contain antibody sequence information, linking to relevant entries in SAbDab where structures of the antibody in question (CoV-AbDab) or structures with at least 95% sequence identity (Thera-SAbDab) exist.

# ## Updates to Data Access

# - **Search Features**
#   - New search features were added to improve the ability to create task-specific nanobody and antibody datasets
#   - Free-text keyword query can be performed over certain annotation fields (antigen, species, publication, and structure title)
# - **Download Options**
#   - Structures matching search queries can be downloaded in bulk as a zipped archive and a summary .csv file containing annotation data
#   - Individual structures can be accessed via the structure viewer interface

# ## Updates to SAbDab-nano

# - **Development of SAbDab-nano**
#   - SAbDab-nano is a subset of SAbDab containing nanobody structures
#   - Entries for which at least one antibody has a heavy chain variable domain, but no light chain variable domain are added to SAbDab-nano
# - **Composition and Growth**
#   - SAbDab-nano contains 823 structures (492 nanobodies) with non-redundant CDR sequences
#   - Average 3.8 structures per week are added to SAbDab-nano over the first 36 weeks of 2021

# ## Comparison to Other Nanobody Resources

# - **Other Databases**
#   - There are other databases compiling nanobody data, but no other resource provides nanobody structures in a continuously updated and comprehensively annotated format
#   - Several databases compiling nanobody sequences (but not structures) from a variety of data sources

# ## Conclusion

# - **SAbDab and SAbDab-nano**
#   - SAbDab continues to be updated weekly and represents the most thoroughly annotated antibody structure database from which researchers can quickly create custom datasets
#   - Searching SAbDab is now more powerful and faster, with new connections to auxiliary databases that catalogue therapeutic and antigen-specific antibodies
#   - SAbDab and SAbDab-nano can be accessed freely online under a CC-BY 4.0 license at opig.stats.ox.ac.uk/webapps/newsabdab/ or at opig.stats.ox.ac.uk/webapps/newsabdab/nano respectfully'''
# generate_mindmap_svg(md)