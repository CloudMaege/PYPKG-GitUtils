# Run test suite with `poetry run pytest tests -v`
# Run this test with `poetry run pytest tests/test_github_api.py -v`
################
# Imports:     #
################
from cloudmage.gitutils import GitHubAPI
import pytest, sys

NonValidRepositoryURL = "https://github.com/TheCloudMage/Mock-Repository.git"
NonValidGITURL = "git@github.com:TheCloudMage/Mock-Repository.git"
ValidRepositoryURL = "https://github.com/TheCloudMage/UnitTest-GitUtils-Public.git"

######################################
# Test GitHubAPI Repository Object:  #
######################################
def test_init():
    """This test will instantiate a new GitHubAPI object with a mock repository URL to test the object instance for default values.
    Test each class property to ensure that the default instantiation values are correct.
    Test the _parse_url method to ensure that it parses the provided HTTP URL correctly.
    Test the _repository_url method to ensure that it sets the Github API Endpoint URL correctly.
    Test the .data property to ensure that a blank list comes back.
    Test the .state property to ensure its been set to fail from the _request_handler method.
    Test to ensure that the .owner property is set to None, instead of an object, Check that the .owner attributes do not exist.
    """

    # Instantiate a GitHubAPI object, and test the returned object instance for default values.
    GitHubInitDefaults = GitHubAPI(NonValidRepositoryURL)
    assert(isinstance(GitHubInitDefaults, object))

    # Test passed args
    assert(GitHubInitDefaults.verbose == False)
    assert(GitHubInitDefaults._target_repo_url == NonValidRepositoryURL)
    assert(GitHubInitDefaults._auth_token is None)
    assert(GitHubInitDefaults._log is None)

    # Test object attributes
    assert(GitHubInitDefaults._log_context == 'CLS->GitHubAPI')

    # Test object properties (_parse_url)
    assert(GitHubInitDefaults.namespace == 'TheCloudMage')
    assert(GitHubInitDefaults.name == 'Mock-Repository')

    # Test default properties
    assert(GitHubInitDefaults.id is None)
    assert(GitHubInitDefaults.access is None)
    assert(GitHubInitDefaults.http_url is None)
    assert(GitHubInitDefaults.git_url is None)
    assert(GitHubInitDefaults.description is None)
    assert(GitHubInitDefaults.created is None)
    assert(GitHubInitDefaults.updated is None)
    assert(GitHubInitDefaults.last_push is None)
    assert(GitHubInitDefaults.size is None)
    assert(GitHubInitDefaults.language is None)
    assert(GitHubInitDefaults.license is None)
    assert(GitHubInitDefaults.archived is None)
    assert(GitHubInitDefaults.disabled is None)
    assert(GitHubInitDefaults.default_branch is None)
    assert(GitHubInitDefaults.fork is None)
    assert(GitHubInitDefaults.forks is None)
    assert(GitHubInitDefaults.watchers is None)
    assert(GitHubInitDefaults.stars is None)
    assert(GitHubInitDefaults.issues is None)
    assert(GitHubInitDefaults.open_issues is None)
    assert(GitHubInitDefaults.homepage is None)
    assert(GitHubInitDefaults.wiki is None)
    assert(GitHubInitDefaults.pages is None)
    assert(GitHubInitDefaults.downloads is None)
    assert(GitHubInitDefaults.projects is None)

    # Test that owner is None, and was not assigned the RepoOwner object
    assert(GitHubInitDefaults.owner is None)
    assert(not hasattr(GitHubInitDefaults.owner, 'id'))
    assert(not hasattr(GitHubInitDefaults.owner, 'name'))
    assert(not hasattr(GitHubInitDefaults.owner, 'avatar'))
    assert(not hasattr(GitHubInitDefaults.owner, 'url'))

    # Test repository url and data
    assert(GitHubInitDefaults._repo_request_url == "https://api.github.com/repos/{}/{}".format(GitHubInitDefaults.namespace, GitHubInitDefaults.name))
    assert(GitHubInitDefaults._repo_data is None)
    assert(isinstance(GitHubInitDefaults.data, dict))
    assert(not bool(GitHubInitDefaults.data)) # Test that the set dictionary is empty.
    assert(GitHubInitDefaults.state == 'Fail')


def test_init_verbose(capsys):
    """This test will instantiate a new GitHubAPI object with a mock repository URL with verbose=True to test the object instance for default values.
    Test each class property to ensure that the default instantiation values are correct.
    Test the _parse_url method to ensure that it parses the provided HTTP URL correctly.
    Test the _repository_url method to ensure that it sets the Github API Endpoint URL correctly.
    Test the .data property to ensure that a blank list comes back.
    Test the .state property to ensure its been set to fail from the _request_handler method.
    Test to ensure that the .owner property is set to None, instead of an object, Check that the .owner attributes do not exist.
    Test the .verbose property to ensure that it has been enabled.
    Test the local logger by parsing the log messages sent and verify that the _request_handler failed due to the proper 404 not found response.
    """

    # Instantiate a GitHubAPI object, and test the returned object instance for default values.
    GitHubInitDefaults = GitHubAPI(NonValidRepositoryURL, verbose=True)
    assert(isinstance(GitHubInitDefaults, object))

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)
    assert "ERROR   CLS->GitHubAPI._request_handler:   Request unsuccessful. Received response status code: 404" in err
    assert "ERROR   CLS->GitHubAPI.data:   Updating object properties failed. Bad data source received" in err

    # Test passed args
    assert(GitHubInitDefaults.verbose == True)
    assert(GitHubInitDefaults._target_repo_url == NonValidRepositoryURL)
    assert(GitHubInitDefaults._auth_token is None)
    assert(GitHubInitDefaults._log is None)

    # Test object attributes
    assert(GitHubInitDefaults._log_context == 'CLS->GitHubAPI')
    
    # Test object properties (_parse_url)
    assert(GitHubInitDefaults.namespace == 'TheCloudMage')
    assert(GitHubInitDefaults.name == 'Mock-Repository')

    # Test default properties
    assert(GitHubInitDefaults.id is None)
    assert(GitHubInitDefaults.access is None)
    assert(GitHubInitDefaults.http_url is None)
    assert(GitHubInitDefaults.git_url is None)
    assert(GitHubInitDefaults.description is None)
    assert(GitHubInitDefaults.created is None)
    assert(GitHubInitDefaults.updated is None)
    assert(GitHubInitDefaults.last_push is None)
    assert(GitHubInitDefaults.size is None)
    assert(GitHubInitDefaults.language is None)
    assert(GitHubInitDefaults.license is None)
    assert(GitHubInitDefaults.archived is None)
    assert(GitHubInitDefaults.disabled is None)
    assert(GitHubInitDefaults.default_branch is None)
    assert(GitHubInitDefaults.fork is None)
    assert(GitHubInitDefaults.forks is None)
    assert(GitHubInitDefaults.watchers is None)
    assert(GitHubInitDefaults.stars is None)
    assert(GitHubInitDefaults.issues is None)
    assert(GitHubInitDefaults.open_issues is None)
    assert(GitHubInitDefaults.homepage is None)
    assert(GitHubInitDefaults.wiki is None)
    assert(GitHubInitDefaults.pages is None)
    assert(GitHubInitDefaults.downloads is None)
    assert(GitHubInitDefaults.projects is None)

    # Test that owner is None, and was not assigned the RepoOwner object
    assert(GitHubInitDefaults.owner is None)
    assert(not hasattr(GitHubInitDefaults.owner, 'id'))
    assert(not hasattr(GitHubInitDefaults.owner, 'name'))
    assert(not hasattr(GitHubInitDefaults.owner, 'avatar'))
    assert(not hasattr(GitHubInitDefaults.owner, 'url'))

    # Test repository url and data
    assert(GitHubInitDefaults._repo_request_url == "https://api.github.com/repos/{}/{}".format(GitHubInitDefaults.namespace, GitHubInitDefaults.name))
    assert(GitHubInitDefaults._repo_data is None)
    assert(isinstance(GitHubInitDefaults.data, dict))
    assert(not bool(GitHubInitDefaults.data)) # Test that the set dictionary is empty.
    assert(GitHubInitDefaults.state == 'Fail')


def test_init_token(capsys):
    """This test will instantiate a new GitHubAPI object with a mock repository URL with verbose=True and AuthToken='12345678919' to test the object instance for default values.
    Test each class property to ensure that the default instantiation values are correct.
    Test the _parse_url method to ensure that it parses the provided HTTP URL correctly.
    Test the _repository_url method to ensure that it sets the Github API Endpoint URL correctly.
    Test the .data property to ensure that a blank list comes back.
    Test the .state property to ensure its been set to fail from the _request_handler method.
    Test to ensure that the .owner property is set to None, instead of an object, Check that the .owner attributes do not exist.
    Test the .verbose property to ensure that it has been enabled.
    Test the ._auth_token property to ensure that it has been set to the provided bogus auth_token value.
    Test the logging output from the _request_handler to verify that it attempted to set a header value using the provided bogus auth_token.
    Test the local logger by parsing the log messages sent and verify that the _request_handler failed due to the proper 401 Unauthorized response.
    """

    # Instantiate a GitHubAPI object, and test the returned object instance for default values.
    GitHubInitDefaults = GitHubAPI(NonValidRepositoryURL, auth_token="12345678910", verbose=True)
    assert(isinstance(GitHubInitDefaults, object))

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)
    assert "DEBUG   CLS->GitHubAPI._request_handler:   Auth token found! Adding to request headers." in out
    assert "ERROR   CLS->GitHubAPI._request_handler:   Request unsuccessful. Received response status code: 401" in err
    assert "ERROR   CLS->GitHubAPI.data:   Updating object properties failed. Bad data source received" in err

    # Test passed args
    assert(GitHubInitDefaults.verbose == True)
    assert(GitHubInitDefaults._target_repo_url == NonValidRepositoryURL)
    assert(GitHubInitDefaults._auth_token == '12345678910')
    assert(GitHubInitDefaults._log is None)

    # Test object attributes
    assert(GitHubInitDefaults._log_context == 'CLS->GitHubAPI')
    
    # Test object properties (_parse_url)
    assert(GitHubInitDefaults.namespace == 'TheCloudMage')
    assert(GitHubInitDefaults.name == 'Mock-Repository')

    # Test default properties
    assert(GitHubInitDefaults.id is None)
    assert(GitHubInitDefaults.access is None)
    assert(GitHubInitDefaults.http_url is None)
    assert(GitHubInitDefaults.git_url is None)
    assert(GitHubInitDefaults.description is None)
    assert(GitHubInitDefaults.created is None)
    assert(GitHubInitDefaults.updated is None)
    assert(GitHubInitDefaults.last_push is None)
    assert(GitHubInitDefaults.size is None)
    assert(GitHubInitDefaults.language is None)
    assert(GitHubInitDefaults.license is None)
    assert(GitHubInitDefaults.archived is None)
    assert(GitHubInitDefaults.disabled is None)
    assert(GitHubInitDefaults.default_branch is None)
    assert(GitHubInitDefaults.fork is None)
    assert(GitHubInitDefaults.forks is None)
    assert(GitHubInitDefaults.watchers is None)
    assert(GitHubInitDefaults.stars is None)
    assert(GitHubInitDefaults.issues is None)
    assert(GitHubInitDefaults.open_issues is None)
    assert(GitHubInitDefaults.homepage is None)
    assert(GitHubInitDefaults.wiki is None)
    assert(GitHubInitDefaults.pages is None)
    assert(GitHubInitDefaults.downloads is None)
    assert(GitHubInitDefaults.projects is None)

    # Test that owner is None, and was not assigned the RepoOwner object
    assert(GitHubInitDefaults.owner is None)
    assert(not hasattr(GitHubInitDefaults.owner, 'id'))
    assert(not hasattr(GitHubInitDefaults.owner, 'name'))
    assert(not hasattr(GitHubInitDefaults.owner, 'avatar'))
    assert(not hasattr(GitHubInitDefaults.owner, 'url'))

    # Test repository url and data
    assert(GitHubInitDefaults._repo_request_url == "https://api.github.com/repos/{}/{}".format(GitHubInitDefaults.namespace, GitHubInitDefaults.name))
    assert(GitHubInitDefaults._repo_data is None)
    assert(isinstance(GitHubInitDefaults.data, dict))
    assert(not bool(GitHubInitDefaults.data)) # Test that the set dictionary is empty.
    assert(GitHubInitDefaults.state == 'Fail')


def test_log():
    """This test will instantiate a new GitHubAPI object with a mock repository URL, verbose=True, and with log=<LobObject>.
    Test Creation of test Log object, and the passing of that log object to the GitHubAPI object for logging.
    Test that class logging events get pushed to the provided log object instead of the local stdout, stderr logger.
    The Log object will push each Class log event to a Log object list property. Check the DEBUG, INFO, and ERROR lists to ensure they are not empty
    Test the last element of each of the DEBUG, INFO, and ERROR log object list properties for the expected log messages from the GitHubAPI object instantiation.
    """

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


    # Instantiate a log object
    GitHubLog = Log()

    # Instantiate a GitHubAPI object, and test the returned object instance for default values.
    GitHubInitLog = GitHubAPI(NonValidRepositoryURL, verbose=True, log=GitHubLog)
    assert(isinstance(GitHubInitLog, object))

    # Test passed args
    assert(GitHubInitLog.verbose == True)
    assert(GitHubInitLog._target_repo_url == NonValidRepositoryURL)
    assert(GitHubInitLog._auth_token is None)

    # Test the Log object passed to the GitHubAPI init method
    assert(GitHubInitLog._log is not None)
    assert(isinstance(GitHubInitLog._log, object))
    assert(hasattr(GitHubInitLog._log, 'debug'))
    assert(hasattr(GitHubInitLog._log, 'info'))
    assert(hasattr(GitHubInitLog._log, 'error'))
    assert(hasattr(GitHubInitLog._log, 'debug_logs'))
    assert(hasattr(GitHubInitLog._log, 'info_logs'))
    assert(hasattr(GitHubInitLog._log, 'error_logs'))

    # Test the Log object debug_logs, info_logs, and error_logs properties are lists
    assert(isinstance(GitHubInitLog._log.debug_logs, list))
    assert(isinstance(GitHubInitLog._log.info_logs, list))
    assert(isinstance(GitHubInitLog._log.error_logs, list))

    # Test the GitHubLog object to ensure that the lists are not empty (The GitHubAPI flow should add records to each one.)
    assert(len(GitHubLog.debug_logs) > 0)
    assert(len(GitHubLog.info_logs) > 0)
    assert(len(GitHubLog.error_logs) > 0)

    # Test the Log object for the expected output messages from the GitHubAPI instance instantiation by testing the expected value of the last item in each of the lists.
    assert(GitHubLog.debug_logs[-1] == "CLS->GitHubAPI._request_handler:   Request successfully sent to: https://api.github.com/repos/TheCloudMage/Mock-Repository.")
    assert(GitHubLog.info_logs[-1] == "CLS->GitHubAPI.data:   Initializing object properties.")
    assert(GitHubLog.error_logs[-1] == "CLS->GitHubAPI.data:   Updating object properties failed. Bad data source received")


def test_parse_url():
    """This test will instantiate a GitHubAPI object and pass it a git structured URL.
    Test that the _parse_url function can decode a git styled URL string.
    """

    # Instantiate a GitHubAPI object, and test the returned object instance for default values.
    GitHubInit = GitHubAPI(NonValidGITURL)
    assert(isinstance(GitHubInit, object))

    # Test passed args
    assert(GitHubInit._target_repo_url == NonValidGITURL)
    assert(GitHubInit.namespace == "TheCloudMage")
    assert(GitHubInit.name == "Mock-Repository")
    assert(GitHubInit._repo_request_url == "https://api.github.com/repos/{}/{}".format(GitHubInit.namespace, GitHubInit.name))


def test_valid_verbose(capsys):
    """This test will instantiate a new GitHubAPI object with a valid repository URL with verbose=True to test the object instance for properly set values based on the GitHub API response.
    Test each class property to ensure that the set values are set from the Github API response.
    Test the _parse_url method to ensure that it parses the provided HTTP URL correctly.
    Test the _repository_url method to ensure that it sets the Github API Endpoint URL correctly.
    Test the .data property to ensure that the value reflects a proper json formatted Github API response object.
    Test the .state property to ensure its been set to success from the _request_handler method.
    Test to ensure that the .owner property is set to an object, and has the expected owner object attributes, and that their values are based on the Github API response.
    Test the .verbose property to ensure that it has been enabled.
    Test the local logger by parsing the log messages sent and verify that the _request_handler succeeded due to the proper 200 OK response.
    """

    # Instantiate a GitHubAPI object, and test the returned object instance for default values.
    GitHubRepo = GitHubAPI(ValidRepositoryURL, verbose=True)
    assert(isinstance(GitHubRepo, object))

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)
    assert "DEBUG   CLS->GitHubAPI._request_handler:   Response contains return code: 200" in out
    assert "DEBUG   CLS->GitHubAPI._request_handler:   Verified response object contains valid formatting." in out
    assert "INFO    CLS->GitHubAPI.data:   Object property update state: Success!" in out

    # Test passed args
    assert(GitHubRepo.verbose == True)
    assert(GitHubRepo._target_repo_url == ValidRepositoryURL)
    assert(GitHubRepo._auth_token is None)
    assert(GitHubRepo._log is None)

    # Test object attributes
    assert(GitHubRepo._log_context == 'CLS->GitHubAPI')
    
    # Test object properties (_parse_url)
    assert(GitHubRepo.namespace == 'TheCloudMage')
    assert(GitHubRepo.name == 'UnitTest-GitUtils-Public')

    # Test default properties
    assert(GitHubRepo.id == 240092439)
    assert(GitHubRepo.access == 'public')
    assert(GitHubRepo.http_url == 'https://github.com/TheCloudMage/UnitTest-GitUtils-Public')
    assert(GitHubRepo.git_url == 'git://github.com/TheCloudMage/UnitTest-GitUtils-Public.git')
    assert(GitHubRepo.description == 'Test Repository used only for PyPkgs-GitUtils package unit tests against a public repository')
    assert(GitHubRepo.created == '2020-02-12T19:05:43Z')
    assert(GitHubRepo.updated == '2020-02-12T19:06:07Z')
    assert(GitHubRepo.last_push == '2020-02-12T19:05:44Z')
    assert(GitHubRepo.size == 0)
    assert(GitHubRepo.language is None)
    assert(GitHubRepo.license is None)
    assert(GitHubRepo.archived == False)
    assert(GitHubRepo.disabled == False)
    assert(GitHubRepo.default_branch == 'master')
    assert(GitHubRepo.fork == False)
    assert(GitHubRepo.forks is None)
    assert(GitHubRepo.watchers == 1)
    assert(GitHubRepo.stars == 0)
    assert(GitHubRepo.issues is None)
    assert(GitHubRepo.open_issues == 0)
    assert(GitHubRepo.homepage is None)
    assert(GitHubRepo.wiki == True)
    assert(GitHubRepo.pages == False)
    assert(GitHubRepo.downloads == True)
    assert(GitHubRepo.projects == True)

    # Test that owner is None, and was not assigned the RepoOwner object
    assert(GitHubRepo.owner is not None)
    assert(hasattr(GitHubRepo.owner, 'id'))
    assert(hasattr(GitHubRepo.owner, 'name'))
    assert(hasattr(GitHubRepo.owner, 'avatar'))
    assert(hasattr(GitHubRepo.owner, 'url'))
    assert(GitHubRepo.owner.id == 59182333)
    assert(GitHubRepo.owner.name == 'TheCloudMage')
    assert(GitHubRepo.owner.avatar == 'https://avatars1.githubusercontent.com/u/59182333?v=4')
    assert(GitHubRepo.owner.url == 'https://github.com/TheCloudMage')

    # Test repository url and data
    assert(GitHubRepo._repo_request_url == "https://api.github.com/repos/{}/{}".format(GitHubRepo.namespace, GitHubRepo.name))
    assert(GitHubRepo._repo_data is not None)
    assert(isinstance(GitHubRepo._repo_data, dict))
    assert(bool(GitHubRepo._repo_data))
    assert(isinstance(GitHubRepo.data, dict))
    assert(bool(GitHubRepo.data)) # Test that the set dictionary is not empty.
    assert(GitHubRepo.data.get('full_name') == 'TheCloudMage/UnitTest-GitUtils-Public')
    assert(GitHubRepo.state == 'Success')
