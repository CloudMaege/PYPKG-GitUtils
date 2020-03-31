# CloudMage GitUtils Python3 Utility Package

<br>

![CloudMage](https://github.com/TheCloudMage/Common-Images/raw/master/cloudmage/cloudmage-glow-banner.png)

<br><br>

## Table of Contents

* [Description](#description)
* [Road Map](#road-map)
* [Python Version Support](#python-version-support)
* [Package Installation](#package-installation)
* [Package Dependencies](#package-dependencies)
* [GitConfigParser Class](#gitconfigparser-class)
  * [GitConfigParser Constructor Arguments](#gitconfigparser-constructor-arguments)
  * [GitConfigParser Attributes and Properties](#gitconfigparser-attributes-and-properties)
  * [GitConfigParser Available Methods](#gitconfigparser-available-methods)
  * [GitConfigParser Class Usage](#gitconfigparser-class-usage)
* [GitHubAPI Class](#githubapi-class)
  * [GitHubAPI Object Arguments](#githubapi-object-arguments)
  * [GitHubAPI Object Properties](#githubapi-object-properties)
  * [GitHubAPI Class Usage](#githubapi-class-usage)
* [ChangeLog](#changelog)
* [Contacts and Contributions](#contacts-and-contributions)

<br><br>

## Description

This utility package was created to allow quick and easy access to Git repository data for a provided repository. The purpose of this library is to be able to either automatically detect a projects configured Git repository by searching for and parsing a .git/config file in a given file path, or to take an input consisting simply of the repositories URL (HTTP | Git formatted) along with an optional access token. Once the repository has been determined by either means, the library will create and return an object instance consisting of the repository data received from the determined providers API parsed into the respective object properties.

<br><br>

## Road Map

Currently this library gathers data from the Githubs main repository API, however, future development will include Gitlab and Bitbucket repository APIs as well. Once all of the main core providers repository API development has been completed commit, issue, release, and other datapoint development is planned.

<br><br>

## Python Version Support

This library is compatible with Python 3.6 and higher. It may work with earlier versions of Python3 but was not tested against anything earlier then 3.6. As Python 2.x is soon to be end of life, backward compatibility was not taken into consideration.

<br><br>

## Package Installation

This library has been published to [PyPi](https://pypi.org/project/cloudmage-gitutils/) and can be installed via normal python package manager conventions such as [pip](https://pip.pypa.io/en/stable/) or [poetry](https://pypi.org/project/poetry/).

<br>

```python
pip3 install cloudmage-gitutils
```

<br><br>

## Package Dependencies

This package installs and imports the following python modules during installation:

* requests

<br>

Additionally the package takes advantage of the following built in python modules:

* os
* sys
* json
* inspect

<br><br>

## GitConfigParser Class

This class takes a directory path argument, which it uses as a target directory to search for a .git/config file. If a file is found, then the class will parse the URL from the config, and determines the git platform provider from the parsed URL path. This data is then used to return back an object instance with properties set to the parsed values.

<br>

### GitConfigParser Constructor Arguments

-----

The following arguments can be used to instantiate a new object instance:

<br>

| __[path]('')__ |  *A valid directory path where a `.git/config` file can be found. <br> Must be valid directory path, checked with `os.path.exists()`* |
|:---------------|:-------------------------------------------------------|
| *required*     | [true]('')                                             |
| *type*         | [str](https://docs.python.org/3/library/stdtypes.html) |

<br>

| __[verbose]('')__ |  *Enables verbose mode. &nbsp; [[true]('')=enable &nbsp; [false]('')=disable]* |
|:------------------|:--------------------------------------------------------|
| *required*        | [false]('')                                             |
| *type*            | [bool](https://docs.python.org/3/library/stdtypes.html) |
| *default*         | [false]('') *(disabled)*                                |

<br>

| __[log]('')__ |  *Redirects object standard log messaging to provided log object.* |
|:--------------|:-----------------------------------------------------------|
| *required*    | [false]('')                                                |
| *type*        | [obj](https://docs.python.org/3/library/stdtypes.html)     |
| *default*     | [None]('') *(log to stdout, stderr if verbose=[true](''))* |

<br><br>

### GitConfigParser Attributes and Properties

-----

The following attributes/properties are available to an instantiated object instance. Any of the attributes or properties can be accessed with standard object dot notation as in the example: `verbose_mode = GitConfigParserObj.verbose`

<br>

| __[verbose]('')__ |  *Verbose setting that controls logging level within the object. &nbsp; [[true]('')=enabled, [false]('')=disabled]* |
|:---------------------|:--------------------------------------------------------|
| *returns*            | [true](true) or [false](false) *(enabled or disabled)*  |
| *type*               | [bool](https://docs.python.org/3/library/stdtypes.html) |
| *instantiated value* | [false](false)                                          |

<br>

| __[url]('')__ |  *Verbose setting that controls logging level within the object. &nbsp; [[true]('')=enabled, [false]('')=disabled]* |
|:---------------------|:---------------------------------------------------------------------------------------------|
| *returns*            | *url string* [->](->) `https://github.com/namespace/repository`                              |
| *type*               | [str](https://docs.python.org/3/library/stdtypes.html)                                       |
| *instantiated value* | *URL string parsed from .git/config in directory path specified during object instantiation* |

<br>

| __[provider]('')__   |  *The parsed provider (*github.com*, *gitlab.com*, or *bitbucket.org*) from a given URL string* |
|:---------------------|:-------------------------------------------------------------------------------|
| *returns*            | Provider string [->](->) `github.com`                                          |
| *type*               | [str](https://docs.python.org/3/library/stdtypes.html)                         |
| *instantiated value* | *Provider string parsed from object url property during object instantiation*  |

<br>

| __[user]('')__       |  *If a user was used in the config url, then the value of the user will be assigned to this property* |
|:---------------------|:-------------------------------------------------------------------------------|
| *returns*            | User string [->](->) `username`                                                |
| *type*               | [str](https://docs.python.org/3/library/stdtypes.html)                         |
| *instantiated value* | *User string parsed from object url property during object instantiation*      |

<br>

| __[log]('')__        |  *The class logger. Will either write directly to stdout, stderr, or to a lob object if passed into the object constructor during object instantiation* |
|:---------------------|:-------------------------------------------------------------------------------|
| *returns*            | Log Event Stream                                                               |
| *type*               | [str](https://docs.python.org/3/library/stdtypes.html)                         |
| *instantiated value* | *Logs written to stdout, stderr*                                               |

<br><br>

### GitConfigParser Available Methods

-----

The following methods are available to an instantiated object instance. Some of the methods are simply setter methods that run the logic required to discover and then set one of the above instance properties.

<br>

__[verbose]('')__

Setter method for `verbose` property that enables or disables verbose mode

<br>

| parameter   | type       | required     | arg info                                                   |
|:-----------:|:----------:|:------------:|:-----------------------------------------------------------|
| verbose | [bool]('')  | [true](true) | *[True]('') enables verbose logging, [False]('') disables it* |

<br>

__Example method call:__

```python
GitConfigParserObj.verbose = True
```

<br><br>

__[log]('')__

Method to enable logging throughout the class. Log messages are sent to the log method providing the log message, the message type being one of `[debug, info, warning, error]`, and finally the function or method id that is automatically derived within the function or method using the python inspect module. If a log object such as a logger or an already instantiated log object instance was passed to the class constructor during the objects instantiation, then all logs will be written to the provided log object. If no log object was provided during instantiation then all `debug`, `info`, and `warning` logs will be written to stdout, while any encountered `error` log entries will be written to stderr. Note that debug or verbose mode needs to be enabled to receive the event log stream.

<br>

| arg     | type       | required     | arg info                                          |
|:-------:|:----------:|:------------:|:--------------------------------------------------|
| log_msg | [str]('')  | [true](true) | *The actual message being sent to the log method* |
| log_type | [str]('')  | [true](true) | *The type of message that is being sent to the log method, one of `[debug, info, warning, error]`* |
| log_id | [str]('')  | [true](true) | *A string value identifying the sender method or function, consisting of the method or function name* |

<br>

__Example method call:__

```python
def my_function():
  __function_id = inspect.stack()[0][3]
  GitConfigParserObj.log("{} called.".format(__function_id), 'info', __function_id)
```

<br><br>

__[url]('')__

Setter method for `url` property that will search the object instances set directory path and look for a .git/config directory in that path. If found, then the setter method will parse the .git/config file and look for a URL line to parse and extract the URL. It will then update the object property with the parsed value. If this method is called post instantiation, then a valid directory path must be provided as an argument.

<br>

| parameter   | type       | required     | arg info                                          |
|:-----------:|:----------:|:------------:|:--------------------------------------------------|
| config_path | [str]('')  | [true](true) | *Must be a valid directory path. This value is checked by `os.path.exists()` and will write an error to the log if the provided argument directory path does not exist* |

<br>

__Example method call:__

```python
GitConfigParserObj.url = /home/projects/my_project_directory
```

<br><br>

__[provider]('')__

Setter method for `provider` property that will search the object instances updated url property for a valid git provider string. Currently the provider setter will look specifically for a value that matches one of `[github.com, gitlab.com, bitbucket.org]`. If this method is called post instantiation, then a valid git repository url must be provided as an argument. The provider property setter will parse either an http, https, git or ssh formatted URL string. During the parse operation, if a user is identified in the provider string such as user@bitbucket.org, then the username will also be parsed and used to update the `user` object property.

<br>

| parameter      | type       | required     | arg info                                          |
|:--------------:|:----------:|:------------:|:--------------------------------------------------|
| repository_url | [str]('')  | [true](true) | *Must be a properly formatted URL string starting with one of `[http, https, git, ssh]` and must end in `.git`* |

<br>

__Example method call:__

```python
GitConfigParserObj.provider = "git@github.com:namespace/repository.git"
```

<br><br>

### GitConfigParser Class Usage

-----

<br>

#### Default Instantiation

```python
from cloudmage-gitutils import GitConfigParser

ProjectPath = '/Projects/MyCoolProject'
# Contains .git/config with
# url = https://github.com/GithubNamespace/MyCoolProject-Repo.git

Repo = GitConfigParser(ProjectPath)

repo_url = Repo.url
print(repo_url) # https://github.com/GithubNamespace/MyCoolProject-Repo

repo_provider = Repo.provider
print(repo_provider) # github.com

repo_user = Repo.user
print(repo_user) # None
```

<br><br>

> ![CloudMage](https://github.com/TheCloudMage/Common-Images/raw/master/icons/note.png) &nbsp;&nbsp; [__Optional Verbose Class Constructor Argument:__](Note) <br> When instantiating the class an optional `verbose` argument can be provided. The argument expects a bool value of either `True` or `False`. By default verbose is set to False. If `verbose=True` is passed during object instantiation, then debug mode is turned on allowing the class to output DEBUG, INFO, and WARNING messages to stdout, and ERROR messages to stderr.

<br><br>

#### Verbose Instantiation

```python
from cloudmage-gitutils import GitConfigParser

ProjectPath = '/Projects/MyCoolProject'
# Contains .git/config with
# url = https://github.com/GithubNamespace/MyCoolProject-Repo.git

Repo = GitConfigParser(ProjectPath, verbose=True)

repo_url = Repo.url
print(repo_url) # https://github.com/GithubNamespace/MyCoolProject-Repo

repo_provider = Repo.provider
print(repo_provider) # github.com

repo_user = Repo.user
print(repo_user) # None

# Class DEBUG, INFO, and WARNING messages will be printed to stdout, and ERROR messages will be printed to stderr
```

<br><br>

> ![CloudMage](https://github.com/TheCloudMage/Common-Images/raw/master/icons/note.png) &nbsp;&nbsp; [__Optional Log Object:__](Note) <br> When instantiating the class an optional `log` argument can also be provided. The argument expects an Logger object to be passed as an input. If passed then all DEBUG, INFO, WARNING, and ERROR messages will be printed to the standard log levels [`log.debug()`, `log.info()`, `log.warning()`, `log.error()`] and printed to the passed respective logger object method.

<br><br>

#### Log Instantiation

```python
from cloudmage-gitutils import GitConfigParser

# Define test log class
# This is an example log object that simply appends any DEBUG, INFO and ERROR received class messages
# to the respective log level list. Normally this would be a logger or custom log object.
class Log(object):
        """Test Log Object"""

        def __init__(self):
            """Class Constructor"""
            self.debug_logs = []
            self.info_logs = []
            self.error_logs = []

        def debug(self, message):
            """Log Debug Messages"""
            self.debug_logs.append(message)

        def info(self, message):
            """Log Debug Messages"""
            self.info_logs.append(message)

        def error(self, message):
            """Log Debug Messages"""
            self.error_logs.append(message)

# Instantiate test log class
GitLog = Log()

ProjectPath = '/Projects/MyCoolProject'
# Contains .git/config with
# url = https://github.com/GithubNamespace/MyCoolProject-Repo.git

Repo = GitConfigParser(ProjectPath, verbose=True, log=GitLog)

repo_url = Repo.url
print(repo_url) # https://github.com/GithubNamespace/MyCoolProject-Repo

repo_provider = Repo.provider
print(repo_provider) # github.com

repo_user = Repo.user
print(repo_user) # None

for items in GitLog.debug_logs:
    print(item) # Prints stored debug logs
```

<br><br>

## GitHubAPI Class

This class takes a git repository URL as input, and then uses that input to construct and send a request to the github api for the targeted repository /repos endpoint. When a response is received and tested for validity, the JSON formatted response object is stored in the .data property, and used to populate the other class object properties listed below.

<br>

### GitHubAPI Object Arguments

-----

* `repo_url`: The https or git formatted URL string of the target git repository
  * `type`: str
  * `required`
* `auth_token`: Optional git provider authentication token to be set in the API request headers to authenticate the API request.
  * `type`: str
  * `required`
* `verbose`: Enables verbose mode
  * `type`: bool
  * `default`: False
  * `optional`
* `log`: Redirects standard class log messages to a provided log object.
  * `type`: object
  * `default`: None
  * `optional`

<br>

### GitHubAPI Object Properties

-----

* `verbose`: Verbose bool value that can be optionally passed to the class constructor

<br>

__Github Response Properties:__

* `name`: The name of the targeted Git Repository (derived from provided URL string)
* `namespace`: The namespace under which the repository is owned (derived from provided URL string)
* `id`: The repositories Github id
* `access`: Set to either `public` or `private` based on the github repository type
* `http_url`: The HTTPS url of the repository
* `git_url`: The GIT url of the repository
* `mirror`: Repository configured mirror (If configured)
* `description`: The repository description
* `created`: The repository creation date
* `updated`: The date the repository was last updated
* `last_push`: The the date of the last push to the repository
* `size`: The repository size
* `language`: The repository language
* `license`: The repository license
* `archived`: True or False depending on if the repository has been archived
* `disabled`: True or False depending on if the repository has been disabled
* `default_branch`: The repositories default branch, typically `master`
* `fork`: Indicator as to if the repository is a fork of another repository
* `forks`: Number of forks from the repository
* `watchers`: Number of repository watchers
* `stars`: Number of stars on the repository
* `issues`: Indicates if the repository has an issues section
* `open_issues`: Number of open issues in the repositories
* `homepage`: Value of repository homepage if configured
* `wiki`: Indicates if the repository has a wiki
* `pages`: Indicates if the repository has pages enabled
* `downloads`: Indicates if the repository has downloads enabled
* `projects`: Indicates if the repository has projects enabled.
* `owner`: Object containing owner attributes
  * `owner.id`: The github id of the repository owner
  * `owner.name`: The name of the repository owner (github username)
  * `owner.avatar`: The url of the repository owners avatar
  * `owner.url`: The github url for the repository user profile
* `state`: The state of the API request. Either `Success` or `Fail`
* `data`: A dictionary containing the original github JSON response object
* `log`: The class logger. It will either write directly to stdout, stderr, or to a lob object if one was passed into the object constructor.

<br><br>

### GitHubAPI Class Usage

-----

```python
from cloudmage-gitutils import GitHubAPI

RepositoryURL = 'https://github.com/TheCloudMage/Mock-Repository.git'

Repo = GitHubAPI(RepositoryURL)

repo_name = Repo.name
print(repo_name) # Mock-Repository

repo.url = Repo.http_url
print(repo_provider) # https://github.com/TheCloudMage/Mock-Repository

response_name = Repo.data.get('name')
print(response_name) # Mock-Repository

print(json.dumps, indent=4, sort_keys=True)
# Original github API response object.
{
    'name': 'Mock-Repository',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc'
}
```

<br><br>

> ![CloudMage](https://github.com/TheCloudMage/Common-Images/raw/master/icons/note.png) &nbsp;&nbsp; [__Passing an Authentication Token:__](Note) <br> When instantiating the class, an option `auth_token` argument can be provided. The argument is a valid auth token issued from the platform provider. If provided, the auth_token will be passed to the request handler method, where the method will construct request headers including the authentication token for authenticated requests to private repositories.

<br>

```python
from cloudmage-gitutils import GitHubAPI

RepositoryURL = 'https://github.com/TheCloudMage/Mock-Repository.git'

Repo = GitHubAPI(RepositoryURL)

repo_name = Repo.name
print(repo_name) # Mock-Repository

repo.url = Repo.http_url
print(repo_provider) # https://github.com/TheCloudMage/Mock-Repository

response_name = Repo.data.get('name')
print(response_name) # Mock-Repository

print(json.dumps, indent=4, sort_keys=True)
# Original github API response object.
{
    'name': 'Mock-Repository',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc'
}
```

<br><br>

> ![CloudMage](https://github.com/TheCloudMage/Common-Images/raw/master/icons/note.png) &nbsp;&nbsp; [__Optional Verbose Class Constructor Argument:__](Note) <br> When instantiating the class an optional `verbose` argument can be provided. The argument expects a bool value of either `True` or `False`. By default verbose is set to False. If `verbose=True` is passed during object instantiation, then debug mode is turned on allowing the class to output DEBUG, INFO, and WARNING messages to stdout, and ERROR messages to stderr.repositories.

<br>

```python
from cloudmage-gitutils import GitHubAPI

RepositoryURL = 'https://github.com/TheCloudMage/Mock-Repository.git'

Repo = GitHubAPI(RepositoryURL, verbose=True)

repo_name = Repo.name
print(repo_name) # Mock-Repository

repo.url = Repo.http_url
print(repo_provider) # https://github.com/TheCloudMage/Mock-Repository

response_name = Repo.data.get('name')
print(response_name) # Mock-Repository

print(json.dumps, indent=4, sort_keys=True)
# Original github API response object.
{
    'name': 'Mock-Repository',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc'
}

# Class DEBUG, INFO, and WARNING messages will be printed to stdout, and ERROR messages will be printed to stderr
```

<br><br>

> ![CloudMage](https://github.com/TheCloudMage/Common-Images/raw/master/icons/note.png) &nbsp;&nbsp; [__Optional Log Object:__](Note) <br> When instantiating the class an optional `log` argument can also be provided. The argument expects an Logger object to be passed as an input. If passed then all DEBUG, INFO, WARNING, and ERROR messages will be printed to the standard log levels (`log.debug()`, `log.info()`, `log.warning()`, `log.error()`) and printed to the passed respective logger object method.

<br>

```python
from cloudmage-gitutils import GitHubAPI

# Define test log class
# This is an example log object that simply appends any DEBUG, INFO and ERROR received class messages
# to the respective log level list. Normally this would be a logger or custom log object.
class Log(object):
        """Test Log Object"""

        def __init__(self):
            """Class Constructor"""
            self.debug_logs = []
            self.info_logs = []
            self.error_logs = []

        def debug(self, message):
            """Log Debug Messages"""
            self.debug_logs.append(message)

        def info(self, message):
            """Log Debug Messages"""
            self.info_logs.append(message)

        def error(self, message):
            """Log Debug Messages"""
            self.error_logs.append(message)

# Instantiate test log class
GitLog = Log()

RepositoryURL = 'https://github.com/TheCloudMage/Mock-Repository.git'

Repo = GitHubAPI(RepositoryURL, verbose=True, log=GitLog)

repo_name = Repo.name
print(repo_name) # Mock-Repository

repo.url = Repo.http_url
print(repo_provider) # https://github.com/TheCloudMage/Mock-Repository

response_name = Repo.data.get('name')
print(response_name) # Mock-Repository

print(json.dumps, indent=4, sort_keys=True)
# Original github API response object.
{
    'name': 'Mock-Repository',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc'
}

for items in GitLog.debug_logs:
    print(item) # Prints stored debug logs
```

<br><br>

## Changelog

To view the project changelog see: [ChangeLog:](CHANGELOG.md)

<br><br>

## ![TheCloudMage](https://github.com/TheCloudMage/Common-Images/raw/master/cloudmage/cloudmage-profile.png) &nbsp;&nbsp;Contacts and Contributions

This project is owned and maintained by: [@rnason](https://github.com/rnason)

<br>

To contribute, please:

* Fork the project
* Create a local branch
* Submit Changes
* Create A Pull Request
