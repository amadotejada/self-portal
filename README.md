# Self Portal
Self Portal is a cross-platform desktop application used to deploy software via [Chef](https://github.com/chef/chef) while providing the same user experience across multiple platforms

Self Portal is in beta. Test throughly before using in production.

<!-- [Supports](#supports)
[User Interface](#user-interface)
[Chef Requirements](#chef-requirements)
[Self Portal Requirements](#self-portal-requirements)
[JSON schema](#apps-json-schema)
[Build executables](#build-executables)
[Disclaimers](#disclaimer) -->

#### Supports

| macOS               | Windows             | Linux               |
|---------------------|---------------------|---------------------|
|✅ Monterey|✅ Win 11|✅ Ubuntu|


## User Interface

### macOS - Monterey
<img src="/screenshots/mac_dark.png">

### Windows 11
<img src="/screenshots/win_dark.png">

### Linux - Ubuntu
<img src="/screenshots/linux_dark.png">

## Chef Requirements:
1. [Chef](https://github.com/chef/chef) server and cookbooks needs to be pre-configured before using Self Portal.
2. [pyinstaller](https://pypi.org/project/pyinstaller/) to build executables
 
## Self Portal Requirements: 
1. [PyQt5](https://pypi.org/project/PyQt5/) - Runtime files are bundled in executable for simple deployment.
2. Endpoints need to be enrolled to the Chef instance.
3. Create JSON file for each cookbook/app to deploy - see below.

##### Apps JSON schema
```json
{
  "name": "Chrome",
  "id": "chrome",
  "description": "Chrome is a fast, secure, free web browser. The browser built by Google.",
  "category": ["browser"],
  "icon": "resources/icons/chrome.png",
  "bashcmd": "chef client -o recipe[app-chrome] -L /var/log/chef/self_portal.log"
}
```

## Build executables
- It's best to build on the targeted OS
```cmd
pyinstaller build.spec
```
Executables output to ```/self-portal/dist/```

#
#### Disclaimer

This software {Self Portal} has not been endorsed or supported by [Chef](https://github.com/chef) (Progress Software Corporation) and is in no way associated with Progress Software Corporation and/or its subsidiaries or affiliate. 

#### Licence

Self Portal is released under the [Apache 2.0 Licence](https://github.com/amadotejada/self-portal/blob/main/LICENSE).
####
