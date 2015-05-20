# diamond collectors package builder

This script generates all configuration files needed to package diamond collectors.

Each diamond collector can be enabled by installing the corresponding package.

In settings.yml you define the collector name and the content of the collectors config file.
After running the create packages script, all config files are generated to build.

After building, you can easily enabled packages by running 

    apt-get install -y diamond-collector-<name>


## Building
    
    # Build all config files
    ./create-package.py

    # Commit all changes in git
    git add . --all ; git commit -am "commit message"

    # Build debian packages
    time git-buildpackage --git-pbuilder --git-dist=trusty --git-arch=amd64 --git-ignore-branch --git-ignore-new 


## Setup a ubuntu or debian build environment: 

See [here](https://gist.github.com/fliphess/c01298a307c5c23fcc56) (for debian)
and [here](https://gist.github.com/fliphess/9cffebbe8421189da931) (for ubuntu)


## Settings file

Each package has it's own section in settings.yml
```yml

diamond-collector-cpu:     # Package name 
  name:  CPUCollector      # Collector name
  dir: collectors/cpu      # Directory with your own custom collectors (optional)
  deps: 
    - procps               # List of dependent debian packages (optional)
  content:            
    - 'enabled = True'     # First line of the collector config file
    - 'percore = False'    # Second line of the collector config file
    ...

```
