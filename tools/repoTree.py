import json
import requests

# GitHub API token
TOKEN = ''
# User and repository
USER = 'GalacticBobster'
REPO = 'GITM'
# Default branch
BRANCH = 'master'

# Get the commit SHA of the default branch
branch_url = f'https://api.github.com/repos/{USER}/{REPO}/branches/{BRANCH}'
headers = {'Authorization': f'token {TOKEN}'}
response = requests.get(branch_url, headers=headers)
response.raise_for_status()
sha = response.json()['commit']['sha']

# Fetch the repository tree
tree_url = f'https://api.github.com/repos/{USER}/{REPO}/git/trees/{sha}?recursive=1'
response = requests.get(tree_url, headers=headers)
response.raise_for_status()
tree = response.json()['tree']

# Convert the tree to a nested JSON structure
# Convert the tree to a nested JSON structure
def build_tree(entries):
    tree = {}
    for entry in entries:
        parts = entry['path'].split('/')
        node = tree
        for part in parts[:-1]:
            if part not in node:
                node[part] = {}
            node = node[part]
        node[parts[-1]] = {} if entry['type'] == 'tree' else None
    return tree

# Assuming 'tree' is the input data
tree_structure = build_tree(tree)

# Print or save the JSON tree
json_tree = json.dumps(tree_structure, indent=4)
print(json_tree)

# Optionally, save to a file
with open('repo_tree.json', 'w') as f:
    f.write(json_tree)

# Load the nested JSON tree structure
with open('repo_tree.json', 'r') as f:
    repo_tree = json.load(f)

nodes = []
links = []

def process_node(name, tree, parent=None,path=""):
    url = f"https://github.com/{USER}/{REPO}/tree/{BRANCH}/{path}/{name}"  # Adjust the base URL accordingly
    node_info = {
        "id": name,
        "user": "example_user",  # Replace with actual user information
        "description": "example_description",  # Replace with actual description
        "url": url  # Add the hyperlink
    }
    nodes.append(node_info)
    if parent:
        links.append({"source": parent, "target": name})
    if isinstance(tree, dict):
        for child_name, child_tree in tree.items():
            process_node(child_name, child_tree, name, f"{path}/{name}".strip("/"))

# Start processing from the root
process_node('',repo_tree)

# Save the transformed JSON structure
transformed_tree = {"nodes": nodes, "links": links}
with open('transformed_repo_tree.json', 'w') as f:
    json.dump(transformed_tree, f, indent=4)

print(json.dumps(transformed_tree, indent=4))
