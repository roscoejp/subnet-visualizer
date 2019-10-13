# Subnet Visualizer
##### Heavily inspired by [David C.'s Visual Subnet Calculator](http://www.davidc.net/sites/default/subnets/subnets.html)

This is an offline tool that should help non network-savy folks to get an appreciation for how their network may be laid out. This tool can also help with network planning since it'll give you an easy way to identify network boundries and extra space in your current network.

## Installation
Clone the git repo or source code and make sure you have the required modules installed:
```bash
pip3 install -r ./subnet_visualizer/requirements.txt
```

## Configuration
All configuration options will be read from a YAML configuration file:
```yaml
root: 10.0.0.0/8    # Required: The root of the graph.
display_attributes: # The target attributes that will be shown in the table.
    - name
    - use
    - tag
targets:            # Required: One or more target networks to display.
    10.0.0.0/9:
        name: Some Name     # The network can contain any attributes, but only
        use: Some Use       # those in the 'display_attributes' section will be
        tag: Some Tag       # rendered in the graph.
        foo: bar            # Example of an unrendered attribute.
        color: "#FFA500"    # Optional: Color of the target's row in the graph.
```

## Using the Tool
The only option the tool has at the moment is the path to the configuration file. The default behavior of the tool _at the moment_ is to render an HTML document of the graph.

The following example shows how to generate an HTML version of the graph:
```bash
./subnet_visualizer/subnet-generator.py config.yaml > index.html
```

## Planned Features
- ~~HTML Rendering of the network graph~~
- Add switches for various output types.
- MD Rendering of the network graph
- Javascript so you can actively split the graph. Should allow for manual planning.
- Recommendation Engine
    - Ability to specify several groups of prefixes that the tool will try to place in the same supernet
    - Automatically recommend networks at sane network boundries
- Rendering the graph as a series of Terraform resource blocks
- Rendering the graph as a series of Gcloud commands
