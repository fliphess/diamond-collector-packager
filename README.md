# diamond collectors package builder

This script generates all configuration files needed to package diamond collectors.

In settings.yml you define the diamond collector name and the content of the collectors config file.
After running the create packages script, all config files needed to build are generated.

This script generates several files:
* A collector config file: /etc/diamond/collectors/<collector_name>.conf for each collector defined in settings.yml
* A debian/<package name>.install file that moves this collector config file and optionally custom collectors to the default location when installing on a debian or ubuntu server.
* A debian/control file containing all collector package definitions.

After running this script, building and uploading your package to a ppa or repository server, you can easily enable diamond collectors by running:

    apt-get install -y diamond-collector-<name>

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

