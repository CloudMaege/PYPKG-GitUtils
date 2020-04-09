# Run PyTest:
# `poetry run pytest tests -v`
# Run single test file instead of entire test suite:
# `poetry run pytest tests/test_gitconfig_parser.py -v`
# Run single test from a single test file
# `poetry run pytest tests/test_gitconfig_parser.py::{testname} -v`

# Run Coverage Report:
# poetry run coverage run -m --source=. pytest tests/test_gitconfig_parser.py
# poetry run coverage html --omit=tests/* -i

################
# Imports:     #
################

# Pip Installed Imports:
from cloudmage.gitutils import GitConfigParser

# Base Python Module Imports:
import pytest
import os
import shutil
# import sys

# GitHub Style URLs
GithubHttpUrl = "https://github.com/TheCloudMage/Mock-Repository.git"
GithubGitUrl = "git@github.com:TheCloudMage/Mock-Repository.git"

# GitLab Style URLs
GitlabHttpUrl = "https://gitlab.com/TheCloudMage/Mock-Repository.git"
GitlabGitUrl = "git@gitlab.com:TheCloudMage/Mock-Repository.git"

# BitBucket Style URLs
BitBucketHttpUrl = "https://mocuser@bitbucket.org/TheCloudMage/Mock-Repo.git"
BitBucketGitUrl = "git@bitbucket.org:TheCloudMage/Mock-Repo.git"

TestPath = os.path.join(os.getcwd(), 'gitconfig_testing')
ConfigPath = os.path.join(TestPath, '.git')

######################################
# Define Set and Teardown Fixtures:  #
######################################
@pytest.fixture(scope='session', autouse=True)
def setup():
    """ GitUtilsParser Class PyTest Environment Setup and Teardown Fixture

    Setup any state specific to the execution of the given class (which
    usually contains tests).
    """

    # If the test directory doesn't exist then create it.
    if not os.path.exists(TestPath):
        os.mkdir(TestPath)

    # Setup, Yield the test, and when finished, tear down the test directory.
    yield
    if os.path.exists(TestPath):
        shutil.rmtree(TestPath)


@pytest.fixture
def create_git_config():
    def create_config(url):
        # Instantiate a GitConfigParser object, and test the returned object
        # instance for default values.
        mock_git_config = f"""
[core]
    repositoryformatversion = 0
    filemode = true
    bare = false
    logallrefupdates = true
    ignorecase = true
    precomposeunicode = true
[user]
    name = Rich Nason
    email = rnason@cloudmage.io
[remote "origin"]
    url = {url}
    fetch = +refs/heads/*:refs/remotes/origin/*
        """

        # Remove the ConfigPath if it already exists
        if os.path.exists(ConfigPath):
            shutil.rmtree(ConfigPath)

        # If the file path doesn't exist (Which it shouldn't) then create it
        # for the test, and write a mock git config file.
        os.mkdir(ConfigPath)
        git_config = open(os.path.join(ConfigPath, 'config'), "w")
        git_config.write(mock_git_config)
        git_config.close()

    return create_config


@pytest.fixture
def destroy_git_config():
    def create_config():
        shutil.rmtree(ConfigPath)

    return create_config


######################################
# Test Init Defaults:                #
######################################
def test_init():
    """ GitConfigParser Class Constructor Init Test

    This test will instantiate a new GitConfigParser object and test to ensure
    that the object attributes match the expected instantiation values that
    should be set by the class init constructor.

    Expected Result:
      Constructor values should be set to their default settings.
    """

    # Ensure TestPath exists...
    assert(os.path.exists(TestPath))

    # Instantiate a GitConfigParser object,
    # and test the returned object instance for default values.
    GitRepo = GitConfigParser(TestPath)
    assert(isinstance(GitRepo, object))

    # Test passed args
    assert(not GitRepo._verbose)
    assert(not GitRepo.verbose)
    assert(GitRepo._path == TestPath)
    assert(GitRepo._log is None)
    assert(GitRepo._log_context == "CLS->GitConfigParser")
    assert(GitRepo._url is None)
    assert(GitRepo.url == 'url property has no value assigned!')
    assert(GitRepo._provider is None)
    assert(GitRepo.provider == 'provider property has no value assigned!')
    assert(GitRepo._user is None)
    assert(GitRepo.user == "user property has no value assigned!")


######################################
# Test Path:                         #
######################################
def test_path_not_provided():
    """ GitConfigParser Class Path Property None Test

    This test will test the path instantiation variable requirement.
    It will attempt the instantiate a new object with an undefined path,
    causing the test to fail or pass with failure.

    Expected Result:
      Test should pass with instantiation exception requiring valid path.
    """

    GitRepo = False

    with pytest.raises(
        TypeError,
        match=r".* missing 1 required positional argument: .*"
    ):
        # Instantiate GitRepo object, and test for expected test values.
        GitRepo = GitConfigParser()

    assert(not GitRepo)


######################################
# Test Verbose:                      #
######################################
def test_verbose_init_enabled():
    """ GitConfigParser Class Verbose Property Init Test

    This test will test the verbose getter and setter property methods.
    Default value tested during init test, test setting value to True
    during object instantiation, using the class constructor.

    Expected Result:
      Verbose property should be set to True.
    """

    # Instantiate a GitConfigParser object, and test for expected test values.
    GitRepo = GitConfigParser(TestPath, verbose=True)
    assert(isinstance(GitRepo, object))

    # Test verbose is set to True
    assert(GitRepo._verbose)
    assert(GitRepo.verbose)


def test_verbose_setter_enabled():
    """ GitConfigParser Class Verbose Property Setter Test

    This test will test the verbose getter and setter property methods.
    Default value tested during init test, test setting value to True
    using the class verbose setter method.

    Expected Result:
      Verbose property should be set to True.
    """

    # Instantiate a GitConfigParser object, and test for expected test values.
    GitRepo = GitConfigParser(TestPath)
    assert(isinstance(GitRepo, object))

    # Test verbose is set to default False
    assert(not GitRepo._verbose)
    assert(not GitRepo.verbose)

    # Call the Setter to enable verbose and test the property value is True
    GitRepo.verbose = True
    assert(GitRepo._verbose)
    assert(GitRepo.verbose)


def test_verbose_init_invalid():
    """ GitConfigParser Class Verbose Property Init Invalid Value Test

    This test will test the verbose getter and setter property methods.
    Default value tested during init test, test setting value to invalid value
    during object instantiation, using the class constructor.

    Expected Result:
      Verbose property should be set to False, ignoring the invalid value.
    """

    # Instantiate a GitConfigParser object, and test for expected test values.
    GitRepo = GitConfigParser(TestPath, verbose=42)
    assert(isinstance(GitRepo, object))

    # Test verbose is False default value, ignoring invalid input value
    assert(not GitRepo._verbose)
    assert(not GitRepo.verbose)


def test_verbose_setter_invalid(capsys):
    """ GitConfigParser Class Verbose Property Setter Invalid Value Test

    This test will test the verbose getter and setter property methods.
    Default value tested during init test, test setting value to invalid value
    using the property setter method.

    Expected Result:
      Verbose property should be set to False, ignoring the invalid value.
    """

    # Instantiate a GitConfigParser object, and test for expected test values.
    GitRepo = GitConfigParser(TestPath)
    assert(isinstance(GitRepo, object))

    # Test verbose setting was defaulted to False
    assert(not GitRepo._verbose)
    assert(not GitRepo.verbose)

    # Set verbose to an invalid value using property settter and test the
    # value ensuring that the invalid value was ignored, and is set False.
    GitRepo.verbose = 42
    assert(not GitRepo._verbose)
    assert(not GitRepo.verbose)

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->GitConfigParser.verbose: \
-> verbose property argument expected type bool but received type:" in err


######################################
# Test Logging:                      #
######################################
def test_logs_verbose_disabled(capsys):
    """ GitConfigParser Class Verbose Disabled Log Test

    This test will test to ensure that when verbose mode is disabled
    that no logs other then errors are output.

    Expected Result:
      Logged events are silent, Error messages are output to the console.
    """

    # Instantiate a GitConfigParser object
    # Test the returned object verbose attribute for expected values.
    GitRepo = GitConfigParser(TestPath, verbose=False)
    assert(isinstance(GitRepo, object))

    # Test verbose setting
    assert(not GitRepo._verbose)

    # Write a test log entry
    GitRepo.log("Pytest debug log write test", 'debug', 'test_log')
    GitRepo.log("Pytest info log write test", 'info', 'test_log')
    GitRepo.log("Pytest warning log write test", 'warning', 'test_log')
    GitRepo.log("Pytest error log write test", 'error', 'test_log')

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "DEBUG   CLS->GitConfigParser.test_log: \
-> Pytest debug log write test" not in out
    assert "INFO    CLS->GitConfigParser.test_log: \
-> Pytest info log write test" not in out
    assert "WARNING CLS->GitConfigParser.test_log: \
-> Pytest warning log write test" not in out
    assert "ERROR   CLS->GitConfigParser.test_log: \
-> Pytest error log write test" in err


def test_logs_verbose_enabled(capsys):
    """ GitConfigParser Class Verbose Enabled Log Test

    This test will test to ensure that when verbose mode is enabled
    that all logs are written to stdout, stderr

    Expected Result:
      Logged events are written to stdout, stderr. Verbose enabled.
    """

    # Instantiate a GitConfigParser object, and test for expected test values.
    GitRepo = GitConfigParser(TestPath, verbose=True)
    assert(isinstance(GitRepo, object))

    # Test verbose setting was correctly set to input True value
    assert(GitRepo._verbose)
    assert(GitRepo.verbose)

    # Write a test log entry to each log level
    GitRepo.log("Pytest debug log write test", 'debug', 'test_log')
    GitRepo.log("Pytest info log write test", 'info', 'test_log')
    GitRepo.log("Pytest warning log write test", 'warning', 'test_log')
    GitRepo.log("Pytest error log write test", 'error', 'test_log')

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "DEBUG   CLS->GitConfigParser.test_log: \
-> Pytest debug log write test" in out
    assert "INFO    CLS->GitConfigParser.test_log: \
-> Pytest info log write test" in out
    assert "WARNING CLS->GitConfigParser.test_log: \
-> Pytest warning log write test" in out
    assert "ERROR   CLS->GitConfigParser.test_log: \
-> Pytest error log write test" in err


def test_logs_logger_object(capsys):
    """ GitConfigParser Class Log Object Test

    This test will test the log method to ensure that if the class constructor
    is passed a logger object object to write to that all class logs will be
    written to that provided object instead of stdout, stderr.

    Expected Result:
      Logged events are written to the provided log object. Verbose enabled.
    """

    # Create a test log object that will just collect logs and add them to a
    # list, which we can check for produced log messages
    class Log(object):
        """Test Log Object"""

        def __init__(self):
            """Class Constructor"""
            self.debug_logs = []
            self.info_logs = []
            self.warning_logs = []
            self.error_logs = []

        def debug(self, message):
            """Log Debug Messages"""
            self.debug_logs.append(message)

        def info(self, message):
            """Log Info Messages"""
            self.info_logs.append(message)

        def warning(self, message):
            """Log Warning Messages"""
            self.warning_logs.append(message)

        def error(self, message):
            """Log Error Messages"""
            self.error_logs.append(message)

    # Instantiate a new log object to collect test logs.
    LogObj = Log()

    # Instantiate a GitConfigParser object, and test for expected test values.
    GitRepo = GitConfigParser(TestPath, verbose=True, log=LogObj)
    assert(isinstance(GitRepo, object))
    assert(isinstance(GitRepo._log, object))
    assert(isinstance(GitRepo.log, object))

    # Test verbose setting
    assert(GitRepo._verbose)
    assert(GitRepo.verbose)
    assert(GitRepo._log is not None)

    # Test the Log object to make sure the expected object attributes exist
    assert(hasattr(GitRepo._log, 'debug'))
    assert(hasattr(GitRepo._log, 'info'))
    assert(hasattr(GitRepo._log, 'warning'))
    assert(hasattr(GitRepo._log, 'error'))
    assert(hasattr(GitRepo._log, 'debug_logs'))
    assert(hasattr(GitRepo._log, 'info_logs'))
    assert(hasattr(GitRepo._log, 'warning_logs'))
    assert(hasattr(GitRepo._log, 'error_logs'))

    # Write test log entries for each of the different types of logs
    GitRepo.log("Pytest log debug test", 'debug', 'test_log_object')
    GitRepo.log("Pytest log info test", 'info', 'test_log_object')
    GitRepo.log("Pytest log warning test", 'warning', 'test_log_object')
    GitRepo.log("Pytest log error test", 'error', 'test_log_object')

    # Test that the Log object debug_logs, info_logs, warning_logs and
    # error_logs properties are lists
    assert(isinstance(GitRepo._log.debug_logs, list))
    assert(isinstance(GitRepo._log.info_logs, list))
    assert(isinstance(GitRepo._log.warning_logs, list))
    assert(isinstance(GitRepo._log.error_logs, list))

    # Test that each of the log_lists have items written into them
    assert(len(LogObj.debug_logs) >= 1)
    assert(len(LogObj.info_logs) >= 1)
    assert(len(LogObj.warning_logs) >= 1)
    assert(len(LogObj.error_logs) >= 1)

    # Test the log messages to make sure they match the written logs
    assert(
        LogObj.debug_logs[-1] == "CLS->GitConfigParser.test_log_object: \
-> Pytest log debug test"
    )
    assert(
        LogObj.info_logs[-1] == "CLS->GitConfigParser.test_log_object: \
-> Pytest log info test"
    )
    assert(
        LogObj.warning_logs[-1] == "CLS->GitConfigParser.test_log_object: \
-> Pytest log warning test"
    )
    assert(
        LogObj.error_logs[-1] == "CLS->GitConfigParser.test_log_object: \
-> Pytest log error test"
    )


def test_logs_invalid_object(capsys):
    """ GitConfigParser Class Invalid Log Object Test

    This test will test the log method to ensure that
    if the logs constructor object is provided an invalid log object
    to write to that the invalid object will be ignored, resulting in
    all class logs being written to stdout, stderr.

    Expected Result:
      Invalid object ignored. Logged events are written to stdout, stderr.
    """

    # Test to ensure that passing a non valid log object is properly caught.
    GitRepo = GitConfigParser(TestPath, verbose=True, log=42)
    assert(isinstance(GitRepo, object))
    assert(GitRepo._log is None)

    # Write a test log entry to each log level
    GitRepo.log("Pytest debug log write test", 'debug', 'test_log')
    GitRepo.log("Pytest info log write test", 'info', 'test_log')
    GitRepo.log("Pytest warning log write test", 'warning', 'test_log')
    GitRepo.log("Pytest error log write test", 'error', 'test_log')

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "DEBUG   CLS->GitConfigParser.test_log: \
-> Pytest debug log write test" in out
    assert "INFO    CLS->GitConfigParser.test_log: \
-> Pytest info log write test" in out
    assert "WARNING CLS->GitConfigParser.test_log: \
-> Pytest warning log write test" in out
    assert "ERROR   CLS->GitConfigParser.test_log: \
-> Pytest error log write test" in err


####################################
# Test Exception handler method:   #
####################################
def test_exception_handler(capsys):
    """ GitConfigParser Class Exception Handler Test

    This test will test the class wide exception handler.

    Expected Result:
      When an exception condition is encountered,
      exceptions will output in correct format to stderr.
    """

    # Instantiate a GitConfigParser object, and test for expected test values.
    GitRepo = GitConfigParser(TestPath, verbose=True)
    assert(isinstance(GitRepo, object))

    # Write a log with a bad value to trigger an exception.
    GitRepo.log('Message', 42, 2)

    # Capture stdout, stderr to check the log messages
    # for the expected outputs.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->GitConfigParser.log: \
-> EXCEPTION occurred in: CLS->GitConfigParser.log" in err


######################################
# Test url property methods: #
######################################
def test_url_property_getter(capsys, create_git_config, destroy_git_config):
    """ GitConfigParser Class 'url' Property Value Test

    This test will test the url getter property method.
    The Test will create a test directory, and write
    a test .git/config file to the directory. When the object is
    instantiated, it will automatically call the url setter.
    The test will try to validate and parse the file,
    extracting the proper git URL from the written config file.
    This test will run 6 times, once for each test URL provided.

    Expected Result:
      Objects url property will have the correct test URL value set.
    """

    # Test to ensure the test path was created.
    assert(os.path.exists(TestPath))

    # For each example Git Provider, create a test file with a cooresponding
    # test object to test for the expected URL string.
    for providerUrl in [
        GithubHttpUrl,
        GithubGitUrl,
        GitlabHttpUrl,
        GitlabGitUrl,
        BitBucketHttpUrl,
        BitBucketGitUrl
    ]:

        # Create the test config file
        create_git_config(providerUrl)

        # Instantiate a GitConfigParser object to test the provider url.
        GitRepo = GitConfigParser(TestPath, verbose=True)
        assert(isinstance(GitRepo, object))
        assert(GitRepo.verbose)
        assert(GitRepo._log is None)

        # Test url property value.
        assert(GitRepo._url == providerUrl)
        assert(GitRepo.url == providerUrl)

        # Capture stdout, stderr to test log messages
        out, err = capsys.readouterr()
        # sys.stdout.write(out)
        # sys.stderr.write(err)

        assert "DEBUG   CLS->GitConfigParser.url: \
-> URL string match found in .git/config" in out
        assert "INFO    CLS->GitConfigParser.url: \
-> URL string match verified... Updating url property with value: {}".format(
            providerUrl
            ) in out

        # Tear down the test config
        destroy_git_config()


def test_url_property_getter_no_config(capsys):
    """ GitConfigParser Class 'url' Property No Config Getter Test

    This test will test the url getter property method.
    The test will be passed a path value that will not contain a config file.
    The same test directory will be used, but the .git/config test fixture
    will not be called, which means that no test file will be created.
    When the call to the URL getter is made, the value should be returned
    indicating that no config was discovered, and that the directory path
    provided is invalid (no .git directory in set path)

    Expected Result:
      Objects url property will return not found message.
    """

    # Test to ensure the test path was created.
    assert(os.path.exists(TestPath))

    # Instantiate a GitConfigParser object to test the provider url.
    GitRepo = GitConfigParser(TestPath, verbose=True)
    assert(isinstance(GitRepo, object))
    assert(GitRepo.verbose)
    assert(GitRepo._log is None)

    # Test url property value.
    assert(GitRepo._url is None)
    assert "url property has no value assigned!" in GitRepo.url


def test_url_property_setter_no_config(capsys):
    """ GitConfigParser Class 'url' Property No Config Setter Test

    This test will test the url setter property method.
    The test will be passed a path value that will not contain a config file.
    The same test directory will be used, but the .git/config test fixture
    will not be called, which means that no test file will be created.
    When the call to the URL getter is made, the value should be returned
    indicating that no config was discovered, and that the directory path
    provided is invalid (no .git directory in set path)

    Expected Result:
      Objects url property will return not found message.
    """

    # Test to ensure the test path was created.
    assert(os.path.exists(TestPath))

    # Instantiate a GitConfigParser object to test the provider url.
    GitRepo = GitConfigParser(TestPath, verbose=True)
    assert(isinstance(GitRepo, object))
    assert(GitRepo.verbose)
    assert(GitRepo._log is None)

    # Test url property value.
    assert(GitRepo._url is None)
    assert "url property has no value assigned!" in GitRepo.url

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)

    assert "ERROR   CLS->GitConfigParser.url: \
-> Provided directory path doesn't exist. Aborting update!" in err


def test_url_property_setter_path_none():
    """ GitConfigParser Class 'url' Property Path None Setter Test

    This test will test the url setter property method.
    The test will be passed a path value of None.
    Init should set the path to the current working directory

    Expected Result:
      Objects url property will return not found message.
      Directory Path should be set to the current working directory.
    """

    # Grab the current directory location.
    current_directory = os.getcwd()

    # Instantiate a GitConfigParser object to test the provider url.
    GitRepo = GitConfigParser(None, verbose=True)
    assert(isinstance(GitRepo, object))
    assert(GitRepo.verbose)
    assert(GitRepo._log is None)

    # Test url property value.
    assert(GitRepo._path == current_directory)


def test_url_property_setter_path_type_invalid():
    """ GitConfigParser Class 'url' Property Path Invalid Type Setter Test

    This test will test the url setter property method.
    The test will be passed a path value of of a non string.
    Init should set the path to the current working directory

    Expected Result:
      Objects url property will return not found message.
      Directory Path should be set to the current working directory.
    """

    # Grab the current directory location.
    current_directory = os.getcwd()

    # Instantiate a GitConfigParser object to test the provider url.
    GitRepo = GitConfigParser(42, verbose=True)
    assert(isinstance(GitRepo, object))
    assert(GitRepo.verbose)
    assert(GitRepo._log is None)

    # Test url property value.
    assert(GitRepo._path == current_directory)


def test_url_property_setter_force_path_type_invalid(capsys):
    """ GitConfigParser Class 'url' Property Path Invalid Type Setter Test

    This test will test the url setter property method.
    The test will be passed a path value of of a non string.
    Init should set the path to the current working directory

    Expected Result:
      Objects url property will return not found message.
      Directory Path should be set to the current working directory.
    """

    # Instantiate a GitConfigParser object to test the provider url.
    GitRepo = GitConfigParser(42, verbose=True)
    assert(isinstance(GitRepo, object))
    assert(GitRepo.verbose)
    assert(GitRepo._log is None)

    GitRepo.url = 42

    # Test to ensure proper error message is logged.
    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)

    assert "ERROR   CLS->GitConfigParser.url: \
-> url path argument expected string but received type:" in err


def test_url_property_setter_invalid_url(
    capsys,
    create_git_config,
    destroy_git_config
):
    """ GitConfigParser Class 'url' Property Path Invalid URL Setter Test

    This test will test the url setter property method.
    The test will be passed a path value set to the test directory.
    A non valid URL will then be passed to the method to ensure that
    the URL is parsed correctly and not set or returned if the URL
    string structure is incorrect.

    Expected Result:
      Objects url property will return not found message.
      Validation error should be logged.
    """
    # Test to ensure the test path was created.
    assert(os.path.exists(TestPath))

    # Create the test config file with an invalid protocol
    create_git_config("ftp://github.com/TheCloudMage/Mock-Repository.git")

    # Instantiate a GitConfigParser object to test the provider url.
    GitRepo = GitConfigParser(TestPath, verbose=True)
    assert(isinstance(GitRepo, object))
    assert(GitRepo.verbose)
    assert(GitRepo._log is None)
    assert(GitRepo._url is None)

    # Test to ensure proper error message is logged.
    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)

    assert "WARNING CLS->GitConfigParser.url: \
-> URL match failed format verification" in out

    # Tear down the test config
    destroy_git_config()

    # Create the test config file without the .git url extention
    create_git_config("https://github.com/TheCloudMage/Mock-Repository")

    # Instantiate a GitConfigParser object to test the provider url.
    GitRepo2 = GitConfigParser(TestPath, verbose=True)
    assert(isinstance(GitRepo2, object))
    assert(GitRepo2.verbose)
    assert(GitRepo2._log is None)
    assert(GitRepo2._url is None)

    # Test to ensure proper error message is logged.
    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)

    assert "WARNING CLS->GitConfigParser.url: \
-> URL match failed format verification" in out

    # Tear down the test config
    destroy_git_config()


def test_url_property_setter_invalid_file(
    capsys,
    create_git_config,
    destroy_git_config
):
    """ GitConfigParser Class 'url' Property Path Invalid File Setter Test

    This test will test the url setter property method.
    The test will be passed a path value set to the test directory.
    A test file will be created, and then made un-readable.
    The test should gracefully handle the open failure.

    Expected Result:
      Error should be returned indicating that the file was not accessable.
    """
    # Test to ensure the test path was created.
    assert(os.path.exists(TestPath))

    # Create the test config file with an invalid protocol
    create_git_config("https://github.com/TheCloudMage/Mock-Repository.git")

    # Set the file permssions to limit file accessability
    os.chmod(os.path.join(ConfigPath, "config"), 000)

    # Instantiate a GitConfigParser object to test the provider url.
    GitRepo = GitConfigParser(TestPath, verbose=True)
    assert(isinstance(GitRepo, object))
    assert(GitRepo.verbose)
    assert(GitRepo._log is None)
    assert(GitRepo._url is None)

    # Test to ensure proper error message is logged.
    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)

    assert "ERROR   CLS->GitConfigParser.url: \
-> Provided directory path doesn't exist. Aborting update!" in err

    # Re-Set the file permssions to limit file accessability
    os.chmod(os.path.join(ConfigPath, "config"), 777)

    # Tear down the test config
    destroy_git_config()


######################################
# Test provider property methods: #
######################################
def test_provider_property_getter(
    capsys,
    create_git_config,
    destroy_git_config
):
    """ GitConfigParser Class 'provider' Property Value Test

    This test will test the provider getter property method.
    The Test will create a test directory, and write
    a test .git/config file to the directory. When the object is
    instantiated, it will automatically call the provider setter.
    The test will attempt to validate and parse the file,
    extracting the proper git provider from the written config file.
    This test will run 6 times, once for each test URLs provided.

    Expected Result:
      Objects provider property will have the correct test URL value set.
    """

    # Test to ensure the test path was created.
    assert(os.path.exists(TestPath))

    # For each example Git Provider, create a test file with a cooresponding
    # test object to test for the expected URL string.
    for providerUrl in [
        GithubHttpUrl,
        GithubGitUrl,
    ]:

        # Create the test config file
        create_git_config(providerUrl)

        # Instantiate a GitConfigParser object to test the git provider.
        GitHubRepo = GitConfigParser(TestPath, verbose=True)
        assert(isinstance(GitHubRepo, object))
        assert(GitHubRepo.verbose)

        # Validate the provider and the user properties.
        assert(GitHubRepo._provider == 'github.com')
        assert(GitHubRepo.provider == 'github.com')
        assert(GitHubRepo._user is None)
        assert("has no value assigned" in GitHubRepo.user)

        # Capture stdout, stderr to test log messages
        out, err = capsys.readouterr()
        # sys.stdout.write(out)
        # sys.stderr.write(err)

        assert "DEBUG   CLS->GitConfigParser.provider: \
-> Searching for git provider in URL:" in out
        assert "DEBUG   CLS->GitConfigParser.provider: \
-> No User detected in provider string" in out
        assert "DEBUG   CLS->GitConfigParser.provider: \
-> Provider match github.com found!" in out

        # Tear down the test config
        destroy_git_config()

    # GITLAB URL Tests
    # -----------------
    for providerUrl in [
        GitlabHttpUrl,
        GitlabGitUrl,
    ]:

        # Create the test config file
        create_git_config(providerUrl)

        # Instantiate a GitConfigParser object to test the git provider.
        GitLabRepo = GitConfigParser(TestPath, verbose=True)
        assert(isinstance(GitLabRepo, object))
        assert(GitLabRepo.verbose)

        # Validate the provider and the user properties.
        assert(GitLabRepo._provider == 'gitlab.com')
        assert(GitLabRepo.provider == 'gitlab.com')
        assert(GitLabRepo._user is None)
        assert("has no value assigned" in GitLabRepo.user)

        # Capture stdout, stderr to test log messages
        out, err = capsys.readouterr()
        # sys.stdout.write(out)
        # sys.stderr.write(err)

        assert "DEBUG   CLS->GitConfigParser.provider: \
-> Searching for git provider in URL:" in out
        assert "DEBUG   CLS->GitConfigParser.provider: \
-> No User detected in provider string" in out
        assert "DEBUG   CLS->GitConfigParser.provider: \
-> Provider match gitlab.com found!" in out

        # Tear down the test config
        destroy_git_config()

    # BitBucket URL Tests
    # -----------------
    for providerUrl in [
        BitBucketHttpUrl,
        BitBucketGitUrl
    ]:

        # Create the test config file
        create_git_config(providerUrl)

        # Instantiate a GitConfigParser object to test the git provider.
        BitBucketRepo = GitConfigParser(TestPath, verbose=True)
        assert(isinstance(BitBucketRepo, object))
        assert(BitBucketRepo.verbose)

        # Capture stdout, stderr to test log messages
        out, err = capsys.readouterr()
        # sys.stdout.write(out)
        # sys.stderr.write(err)

        # Validate the provider and the user properties.
        assert(BitBucketRepo._provider == 'bitbucket.org')
        assert(BitBucketRepo.provider == 'bitbucket.org')

        # Check logs for common output
        assert "DEBUG   CLS->GitConfigParser.provider: \
-> Searching for git provider in URL:" in out
        assert "DEBUG   CLS->GitConfigParser.provider: \
-> Provider match bitbucket.org found!" in out

        # Check for correct user settings if the bitbucket http url is parsed
        if BitBucketRepo._url.startswith(('http', 'https')):
            assert(BitBucketRepo._user == 'mocuser')
            assert(BitBucketRepo.user == 'mocuser')

            # Capture stdout, stderr to test log messages
            out, err = capsys.readouterr()
            # sys.stdout.write(out)
            # sys.stderr.write(err)

            assert "DEBUG   CLS->GitConfigParser.user: \
-> Return: mocuser" in out
        else:
            assert(BitBucketRepo._user is None)
            assert("has no value assigned" in BitBucketRepo.user)

            # Capture stdout, stderr to test log messages
            out, err = capsys.readouterr()
            # sys.stdout.write(out)
            # sys.stderr.write(err)

            assert "WARNING CLS->GitConfigParser.user: \
-> Return: user has no value assigned!" in out

        # Tear down the test config
        destroy_git_config()


def test_provider_property_getter_no_config(capsys):
    """ GitConfigParser Class 'provider' Property No Config Getter Test

    This test will test the provider getter property method.
    The test will be passed a path value that will not contain a config file.
    The same test directory will be used, but the .git/config test fixture
    will not be called, which means that no test file will be created.
    When the call to the provider getter is made, the value should be returned
    indicating that no config was discovered, and that the repository url
    provided is invalid (no .git directory in set path)

    Expected Result:
      Objects provider property will return invalid message.
    """

    # Test to ensure the test path was created.
    assert(os.path.exists(TestPath))

    # Instantiate a GitConfigParser object to test the provider url.
    GitRepo = GitConfigParser(TestPath, verbose=True)
    assert(isinstance(GitRepo, object))
    assert(GitRepo.verbose)
    assert(GitRepo._log is None)

    # Test url property value.
    assert(GitRepo._provider is None)
    assert(GitRepo._user is None)
    assert "provider property has no value assigned!" in GitRepo.provider


def test_provider_property_setter_no_config(capsys):
    """ GitConfigParser Class 'provider' Property No Config Setter Test

    This test will test the provider setter property method.
    The test will be passed a path value that will not contain a config file.
    The same test directory will be used, but the .git/config test fixture
    will not be called, which means that no test file will be created.
    When the call to the URL getter is made, the value should be returned
    indicating that no config was discovered, and that the directory path
    provided is invalid (no .git directory in set path)

    Expected Result:
      Objects provider property will return type error message.
    """

    # Test to ensure the test path was created.
    assert(os.path.exists(TestPath))

    # Instantiate a GitConfigParser object to test the provider url.
    GitRepo = GitConfigParser(TestPath, verbose=True)
    assert(isinstance(GitRepo, object))
    assert(GitRepo.verbose)
    assert(GitRepo._log is None)

    # Test provider property value.
    assert(GitRepo._provider is None)
    assert "provider property has no value assigned!" in GitRepo.provider

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)

    assert "ERROR   CLS->GitConfigParser.provider: \
-> provider repository url argument expected string but received type:" in err


def test_provider_property_setter_path_type_invalid(capsys):
    """ GitConfigParser Class 'provider' Property Invalid Type Setter Test

    This test will test the provider setter property method.
    The test will be passed a repository url value of of a non string type
    to ensure it fails gracefully.

    Expected Result:
      Objects provider property will return type error message.
    """

    # Test to ensure the test path was created.
    assert(os.path.exists(TestPath))

    # Instantiate a GitConfigParser object to test the provider url.
    GitRepo = GitConfigParser(TestPath, verbose=True)
    assert(isinstance(GitRepo, object))
    assert(GitRepo.verbose)
    assert(GitRepo._log is None)

    # Call the setter and attempt to set a bool value
    GitRepo.provider = False

    # Test provider property value.
    assert(GitRepo._provider is None)
    assert "provider property has no value assigned!" in GitRepo.provider

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)

    assert "ERROR   CLS->GitConfigParser.provider: \
-> provider repository url argument expected string but received type:" in err


def test_provider_property_setter_invalid_url(capsys):
    """ GitConfigParser Class 'provider' Property Invalid URL Setter Test

    This test will test the provider setter property method.
    A non valid URL will be passed to the method to ensure that
    the URL is parsed correctly and not set or returned if the URL
    string structure is incorrect.

    Expected Result:
      Objects provider property will return validation error.
    """
    # Test to ensure the test path was created.
    assert(os.path.exists(TestPath))

    # Set the invalid Test URLs
    invalid_url_protocol = "ftp://github.com/TheCloudMage/Mock-Repository.git"
    invalid_url_suffix = "https://github.com/TheCloudMage/Mock-Repository"
    invalid_url_format = "https://github.git"

    # Test Invalid URL Protocol
    # --------------------------
    # Instantiate a GitConfigParser object to test the provider url.
    GitRepo = GitConfigParser(TestPath, verbose=True)
    assert(isinstance(GitRepo, object))
    assert(GitRepo.verbose)
    assert(GitRepo._log is None)
    assert(GitRepo._url is None)
    assert(GitRepo._provider is None)
    assert "provider property has no value assigned!" in GitRepo.provider

    # Pass invalid URL string
    GitRepo.provider = invalid_url_protocol

    # Re-Test provider property value.
    assert(GitRepo._provider is None)
    assert "provider property has no value assigned!" in GitRepo.provider

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)

    assert f"ERROR   CLS->GitConfigParser.provider: \
-> URL {invalid_url_protocol} not properly formatted, \
aborting provider search" in err

    # Test non .git URL suffix
    # --------------------------
    # Instantiate a GitConfigParser object to test the provider url.
    GitRepo2 = GitConfigParser(TestPath, verbose=True)
    assert(isinstance(GitRepo2, object))
    assert(GitRepo2.verbose)
    assert(GitRepo2._log is None)
    assert(GitRepo2._url is None)
    assert(GitRepo2._provider is None)
    assert "provider property has no value assigned!" in GitRepo2.provider

    # Attempt to use setter to set second invalid URL
    GitRepo2.provider = invalid_url_suffix

    # Re-Test provider property value.
    assert(GitRepo2._provider is None)
    assert "provider property has no value assigned!" in GitRepo2.provider

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)

    assert f"ERROR   CLS->GitConfigParser.provider: \
-> URL {invalid_url_suffix} not properly formatted, \
aborting provider search" in err

    # Test Invalid URL Format
    # --------------------------
    # Instantiate a GitConfigParser object to test the provider url.
    GitRepo3 = GitConfigParser(TestPath, verbose=True)
    assert(isinstance(GitRepo3, object))
    assert(GitRepo3.verbose)
    assert(GitRepo3._log is None)
    assert(GitRepo3._url is None)
    assert(GitRepo3._provider is None)
    assert "provider property has no value assigned!" in GitRepo3.provider

    # Attempt to use setter to set second invalid URL
    GitRepo3.provider = invalid_url_format

    # Re-Test provider property value.
    assert(GitRepo3._provider is None)
    assert "provider property has no value assigned!" in GitRepo3.provider

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)

    assert "ERROR   CLS->GitConfigParser.provider: \
-> Parsed provider value: None not found or invalid. \
Aborting provider search!" in err


def test_provider_property_setter_invalid_provider(capsys):
    """ GitConfigParser Class 'provider' Property Invalid provider Setter Test

    This test will test the provider setter property method.
    The test will call the provider method passing a non standard
    git provider, which does NOT contain github, bitbucket, or gitlab
    in the URL string. The test should gracefully handle the open failure.

    Expected Result:
      Error should be returned indicating an invalid provider has been passed.
    """
    # Test to ensure the test path was created.
    assert(os.path.exists(TestPath))

    # Set the invalid Test URLs
    invalid_provider = "https://gethuub.com/TheCloudMage/Mock-Repository.git"

    # Instantiate a GitConfigParser object to test the provider url.
    GitRepo = GitConfigParser(TestPath, verbose=True)
    assert(isinstance(GitRepo, object))
    assert(GitRepo.verbose)
    assert(GitRepo._log is None)
    assert(GitRepo._url is None)
    assert(GitRepo._provider is None)
    assert "provider property has no value assigned!" in GitRepo.provider

    # Pass invalid URL string
    GitRepo.provider = invalid_provider

    # Re-Test provider property value.
    assert(GitRepo._provider is None)
    assert "provider property has no value assigned!" in GitRepo.provider

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)

    assert "ERROR   CLS->GitConfigParser.provider: \
-> Parsed provider value: gethuub.com not found \
or invalid. Aborting provider search!" in err
