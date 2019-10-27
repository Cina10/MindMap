def knit(template_path, store_path, replacement_map):
    with open(template_path) as f:
        html = f.read()
    
    for key in replacement_map:
        html = html.replace(key, replacement_map[key])
    
    with open(store_path, 'w') as f:
        f.write(html)
