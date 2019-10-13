#!/usr/bin/env python3

from netaddr import *
from pprint import pprint
import argparse
import yaml

def merge_dict(a, b):
    # merge two dicts with preference given to 'b'
    return {**a, **b}

def find_target(target):
    # hunt for a target Network
    ip_target = IPNetwork(target)
    index = 0
    while True:
        ip_output = IPNetwork(output[index]['net'])
        if ip_output == ip_target:
            output[index]['attributes'] = config['targets'][target]
            break
        elif ip_target in ip_output:
            split(index)
        else:
            index += 1
    
def split(index):
    # split an item into its two subnets and insert them back into the list
    to_split = IPNetwork(output[index]['net'])
    split = [x for x in to_split.subnet(to_split.prefixlen + 1)]
    output[index] = merge_dict({'net': split[0].ipv4(), 'prefix': to_split.prefixlen + 1}, default_dict)
    output.insert(index + 1, merge_dict({'net': split[1].ipv4(), 'prefix': to_split.prefixlen + 1}, default_dict))

def find_deepest():
    # find the deepest prefix in the list
    return max(x['net'].prefixlen for x in output)

def fill_depth():
    # determine the column span for an item in the graph
    deepest = find_deepest()
    for i in range(0, len(output)):
        output[i]['colspan'] = deepest - output[i]['net'].prefixlen + 1

def fill_borders():
    # figure out which prefixes this item is a border for
    for i in range(0, len(output)):
        supernets = output[i]['net'].supernet(root.prefixlen)
        borders = [x.prefixlen for x in supernets if x.ip == output[i]['net'].ip]
        output[i]['rowspan'] = {k:1 for k in borders }

def fill_columns():
    # do a lookahead for each border to figure out how many rows the cell should span in the graph
    for i in range(0, len(output)):
        for prefix in output[i]['rowspan'].keys():
            for check in range(i + 1, len(output)):
                if prefix < output[check]['net'].prefixlen and prefix not in output[check]['rowspan'].keys():
                    output[i]['rowspan'][prefix] += 1
                else:
                    break

def render_jinja():
    # render an html document using Jinja templates
    from jinja2 import Environment, FileSystemLoader
    j2_env = Environment(loader=FileSystemLoader('./'), trim_blocks=True)
    template = j2_env.get_template('index.j2')
    rendered_template = template.render(headers=config['display_attributes'], table_data=output, depth=find_deepest() - root.prefixlen + 1)
    return rendered_template


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('config')

    args = parser.parse_args()

    with open(args.config, 'r') as config_file:
        config = yaml.safe_load(config_file)

    root = IPNetwork(config['root'])
    targets = config['targets'].keys()
    default_dict = {'colspan': 0, 'rowspan': {}, 'attributes': {}}

    # Dict structure:
    # {net: IPNetwork, colspan: column_span_for_graph, rowspan: {prefix, row_span_for_graph, ...}, attributes: {attributes_taken_from_config}}
    output = [merge_dict({'net': root, 'prefix': root.prefixlen}, default_dict)]

    for target in targets:
        find_target(target)

    fill_depth()
    fill_borders()
    fill_columns()

    print(render_jinja())