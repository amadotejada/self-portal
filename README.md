# Self Portal
##### Written by [Amado Tejada](https://www.linkedin.com/in/amadotejada/)
Self Portal is a cross-platform desktop application used to deploy software across your endpoints fleet via [Chef](https://github.com/chef/chef) while providing the same user experience across multiple platforms.

Self Portal is in beta. Test throughly before using in production.

<!-- To discuss Self Portal join the `#self-portal` channel on the [MacAdmins Slack](https://www.macadmins.org) -->

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

## How does Self Portal work?
Self Portal does not connect to Chef directly. After you meet the [requirements](#chef-requirements) and create the JSON file per app like [below](#apps-json-schema) for each app, Self Portal runs `chef-client` with the override parameter to only install that app ad hoc. 

Self Portal behaves as a front-end to users that want to install apps hosted by Chef across multiple Opering Systems.

## User Interface

### macOS - Monterey
<img src="/screenshots/mac_dark.png">

### Windows 11
<img src="/screenshots/win_dark.png">

### Linux - Ubuntu
<img src="/screenshots/linux_dark.png">

## Chef Requirements:
* [Chef](https://github.com/chef/chef) server and cookbooks needs to be pre-configured before using Self Portal.
* Cookbooks need to exists on Chef and scoped to the endpoints
* [pyinstaller](https://pypi.org/project/pyinstaller/) to build executables
 
## Self Portal Requirements: 
* [PyQt5](https://pypi.org/project/PyQt5/) - Runtime files are bundled in executable for simple deployment.
* Endpoints need to be enrolled to the Chef instance.
* Create JSON file for each cookbook/app to deploy - see below.
* Self Portal needs to run with an admin account and the ability to run `chef-client` with elevated permissions.
  - Depending on your security posture and requirements.
  - There are several ways of doing this per OS. e.g. sudoers, [polkit](https://linux.die.net/man/8/polkit), [pkexec](https://linux.die.net/man/1/pkexec), [gsudo](https://github.com/gerardog/gsudo)

##### Apps JSON schema
```json
{
  "name": "Chrome",
  "id": "chrome",
  "description": "Chrome is a fast, secure, free web browser. The browser built by Google.",
  "category": ["browser"],
  "icon": "resources/icons/chrome.png",
  "bashcmd": "pkexec chef-client -o recipe[app-chrome] -L /var/log/chef/self_portal.log"
  \\ Self Portal calls the bashcmd to install the software via Chef.
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
