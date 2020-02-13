# Run test suite with `poetry run pytest tests -v`
# Run only this test with `poetry run pytest tests/test_gitconfig_parser.py -v`
################
# Imports:     #
################
from gitutils import GitConfigParser
import pytest, os, sys, shutil

# GitHub Style URLs
GithubHttpUrl = "https://github.com/TheCloudMage/Mock-Repository.git"
GithubGitUrl = "git@github.com:TheCloudMage/Mock-Repository.git"

# GitLab Style URLs
GitlabHttpUrl = "https://gitlab.com/TheCloudMage/Mock-Repository.git"
GitlabGitUrl = "git@gitlab.com:TheCloudMage/Mock-Repository.git"

# BitBucket Style URLs
BitBucketHttpUrl = "https://mocuser@bitbucket.org/TheCloudMage/Mock-Repository.git"
BitBucketGitUrl = "git@bitbucket.org:TheCloudMage/Mock-Repository.git"

TestPath = "./tests"
ConfigPath = os.path.join(TestPath, '.git')


######################################
# Test GitHubAPI Repository Object:  #
######################################
def test_init():
    """This test will instantiate a new GitConfigParser object with a mock directory path to test the object instance for default values.
    Test each class property to ensure that the default instantiation values are correct.
    Test the url method to ensure that failure with invalid path, directory doesn't exist.
    """

    # If a previous test failed to remove the test .git directory do it now
    if os.path.exists(ConfigPath):
        shutil.rmtree(ConfigPath)
    
    # Instantiate a GitConfigParser object, and test the returned object instance for default values.
    GitRepo = GitConfigParser(TestPath)
    assert(isinstance(GitRepo, object))

    # Test passed args
    assert(GitRepo.verbose == False)
    assert(GitRepo.path == TestPath)
    assert(GitRepo._log is None)
    assert(GitRepo._url is None)
    assert(GitRepo.url is None)
    assert(GitRepo._provider is None)
    assert(GitRepo.provider is None)
    assert(GitRepo.user is None)

    # Test object attributes
    assert(GitRepo._log_context == 'CLS->GitConfigParser')


def test_init_verbose(capsys):
    """This test will instantiate a new GitConfigParser object with a mock directory path and verbose=True to test the object instance for default values.
    Test each class property to ensure that the default instantiation values are correct.
    Test the url method to ensure that failure with invalid path, directory doesn't exist.
    Test the .verbose property to ensure that it has been enabled.
    Test the local logger by parsing the log messages sent and verify that the url setter method fails due to improper file path, .git/config not found.
    """

    # If a previous test failed to remove the test .git directory do it now
    if os.path.exists(ConfigPath):
        shutil.rmtree(ConfigPath)
    
    # Instantiate a GitConfigParser object, and test the returned object instance for default values.
    GitRepo = GitConfigParser(TestPath, verbose=True)
    assert(isinstance(GitRepo, object))

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)
    assert "ERROR   CLS->GitConfigParser.url:   Provided directory path does not exist. Exiting..." in err
    assert "ERROR   CLS->GitConfigParser.provider:   Required url property argument was not provided... Aborting search..." in err

    # Test passed args
    assert(GitRepo.verbose == True)
    assert(GitRepo.path == TestPath)
    assert(GitRepo._log is None)
    assert(GitRepo._url is None)
    assert(GitRepo.url is None)
    assert(GitRepo._provider is None)
    assert(GitRepo.provider is None)
    assert(GitRepo.user is None)

    # Test object attributes
    assert(GitRepo._log_context == 'CLS->GitConfigParser')


def test_url_github_http(capsys):
    """This test will instantiate a new GitConfigParser object with a mock directory path and verbose=True to test the object instance.
    Test each class property to ensure that the default instantiation values are correct.
    Test the .verbose property to ensure that it has been enabled.
    Test the local logger by parsing the log messages sent and verify that the url setter method fails due to improper file path, .git/config not found.
    Create .git/config directory/file in the set path to test the url property setter method.
    Test url getter method to ensure that a valid url is provided back.
    Test provider setter passing the parsed URL string from the url getter/setter method
    Test provider getter method to ensure that the provider is properly parsed from the provided URL string.
    Test to ensure that the returned provider matchs 'github.com'
    """

    # Instantiate a GitConfigParser object, and test the returned object instance for default values.

    mock_git_config = """
    [core]
        repositoryformatversion = 0
        filemode = true
        bare = false
        logallrefupdates = true
        ignorecase = true
        precomposeunicode = true
    [user]
        name = Rich Nason
        email = rnason@2ndwatch.com
    [remote "origin"]
        url = {}
        fetch = +refs/heads/*:refs/remotes/origin/*
    """.format(GithubHttpUrl)

    # If the file path doesn't exist (Which it shouldn't) then create it for the test, and write a mock git config file.
    if not os.path.exists(ConfigPath):
        os.mkdir(ConfigPath)
    git_config = open(os.path.join(ConfigPath, 'config'), "w")
    git_config.write(mock_git_config)
    git_config.close()

    GitRepo = GitConfigParser(TestPath, verbose=True)
    assert(isinstance(GitRepo, object))

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)
    assert "DEBUG   CLS->GitConfigParser.url:   URL match verified... setting url to value: {}".format(GithubHttpUrl) in out
    assert "DEBUG   CLS->GitConfigParser.provider:   Provider match {} found!".format('github.com') in out

    # Test passed args
    assert(GitRepo.verbose == True)
    assert(GitRepo.path == TestPath)
    assert(GitRepo._log is None)
    assert(GitRepo._url == GithubHttpUrl)
    assert(GitRepo.url == GithubHttpUrl)
    assert(GitRepo._provider == 'github.com')
    assert(GitRepo.provider == 'github.com')
    assert(GitRepo.user is None)

    # Test object attributes
    assert(GitRepo._log_context == 'CLS->GitConfigParser')

    # Cleanup
    shutil.rmtree(ConfigPath)


def test_url_github_git(capsys):
    """This test will instantiate a new GitConfigParser object with a mock directory path and verbose=True to test the object instance.
    Test each class property to ensure that the default instantiation values are correct.
    Test the .verbose property to ensure that it has been enabled.
    Test the local logger by parsing the log messages sent and verify that the url setter method fails due to improper file path, .git/config not found.
    Create .git/config directory/file in the set path to test the url property setter method.
    Test url getter method to ensure that a valid url is provided back.
    Test provider setter passing the parsed URL string from the url getter/setter method
    Test provider getter method to ensure that the provider is properly parsed from the provided URL string.
    Test to ensure that the returned provider matchs 'github.com'
    """

    # Instantiate a GitConfigParser object, and test the returned object instance for default values.

    mock_git_config = """
    [core]
        repositoryformatversion = 0
        filemode = true
        bare = false
        logallrefupdates = true
        ignorecase = true
        precomposeunicode = true
    [user]
        name = Rich Nason
        email = rnason@2ndwatch.com
    [remote "origin"]
        url = {}
        fetch = +refs/heads/*:refs/remotes/origin/*
    """.format(GithubGitUrl)

    # If the file path doesn't exist (Which it shouldn't) then create it for the test, and write a mock git config file.
    if not os.path.exists(ConfigPath):
        os.mkdir(ConfigPath)
    git_config = open(os.path.join(ConfigPath, 'config'), "w")
    git_config.write(mock_git_config)
    git_config.close()

    GitRepo = GitConfigParser(TestPath, verbose=True)
    assert(isinstance(GitRepo, object))

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)
    assert "DEBUG   CLS->GitConfigParser.url:   URL match verified... setting url to value: {}".format(GithubGitUrl) in out
    assert "DEBUG   CLS->GitConfigParser.provider:   Provider match {} found!".format('github.com') in out

    # Test passed args
    assert(GitRepo.verbose == True)
    assert(GitRepo.path == TestPath)
    assert(GitRepo._log is None)
    assert(GitRepo._url == GithubGitUrl)
    assert(GitRepo.url == GithubGitUrl)
    assert(GitRepo._provider == 'github.com')
    assert(GitRepo.provider == 'github.com')
    assert(GitRepo.user is None)

    # Test object attributes
    assert(GitRepo._log_context == 'CLS->GitConfigParser')

    # Cleanup
    shutil.rmtree(ConfigPath)


def test_url_gitlab_http(capsys):
    """This test will instantiate a new GitConfigParser object with a mock directory path and verbose=True to test the object instance.
    Test each class property to ensure that the default instantiation values are correct.
    Test the .verbose property to ensure that it has been enabled.
    Test the local logger by parsing the log messages sent and verify that the url setter method fails due to improper file path, .git/config not found.
    Create .git/config directory/file in the set path to test the url property setter method.
    Test url getter method to ensure that a valid url is provided back.
    Test provider setter passing the parsed URL string from the url getter/setter method
    Test provider getter method to ensure that the provider is properly parsed from the provided URL string.
    Test to ensure that the returned provider matchs 'gitlab.com'
    """

    # Instantiate a GitConfigParser object, and test the returned object instance for default values.

    mock_git_config = """
    [core]
        repositoryformatversion = 0
        filemode = true
        bare = false
        logallrefupdates = true
        ignorecase = true
        precomposeunicode = true
    [user]
        name = Rich Nason
        email = rnason@2ndwatch.com
    [remote "origin"]
        url = {}
        fetch = +refs/heads/*:refs/remotes/origin/*
    """.format(GitlabHttpUrl)

    # If the file path doesn't exist (Which it shouldn't) then create it for the test, and write a mock git config file.
    if not os.path.exists(ConfigPath):
        os.mkdir(ConfigPath)
    git_config = open(os.path.join(ConfigPath, 'config'), "w")
    git_config.write(mock_git_config)
    git_config.close()

    GitRepo = GitConfigParser(TestPath, verbose=True)
    assert(isinstance(GitRepo, object))

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)
    assert "DEBUG   CLS->GitConfigParser.url:   URL match verified... setting url to value: {}".format(GitlabHttpUrl) in out
    assert "DEBUG   CLS->GitConfigParser.provider:   Provider match {} found!".format('gitlab.com') in out

    # Test passed args
    assert(GitRepo.verbose == True)
    assert(GitRepo.path == TestPath)
    assert(GitRepo._log is None)
    assert(GitRepo._url == GitlabHttpUrl)
    assert(GitRepo.url == GitlabHttpUrl)
    assert(GitRepo._provider == 'gitlab.com')
    assert(GitRepo.provider == 'gitlab.com')
    assert(GitRepo.user is None)

    # Test object attributes
    assert(GitRepo._log_context == 'CLS->GitConfigParser')

    # Cleanup
    shutil.rmtree(ConfigPath)


def test_url_gitlab_git(capsys):
    """This test will instantiate a new GitConfigParser object with a mock directory path and verbose=True to test the object instance.
    Test each class property to ensure that the default instantiation values are correct.
    Test the .verbose property to ensure that it has been enabled.
    Test the local logger by parsing the log messages sent and verify that the url setter method fails due to improper file path, .git/config not found.
    Create .git/config directory/file in the set path to test the url property setter method.
    Test url getter method to ensure that a valid url is provided back.
    Test provider setter passing the parsed URL string from the url getter/setter method
    Test provider getter method to ensure that the provider is properly parsed from the provided URL string.
    Test to ensure that the returned provider matchs 'gitlab.com'
    """

    # Instantiate a GitConfigParser object, and test the returned object instance for default values.

    mock_git_config = """
    [core]
        repositoryformatversion = 0
        filemode = true
        bare = false
        logallrefupdates = true
        ignorecase = true
        precomposeunicode = true
    [user]
        name = Rich Nason
        email = rnason@2ndwatch.com
    [remote "origin"]
        url = {}
        fetch = +refs/heads/*:refs/remotes/origin/*
    """.format(GitlabGitUrl)

    # If the file path doesn't exist (Which it shouldn't) then create it for the test, and write a mock git config file.
    if not os.path.exists(ConfigPath):
        os.mkdir(ConfigPath)
    git_config = open(os.path.join(ConfigPath, 'config'), "w")
    git_config.write(mock_git_config)
    git_config.close()

    GitRepo = GitConfigParser(TestPath, verbose=True)
    assert(isinstance(GitRepo, object))

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)
    assert "DEBUG   CLS->GitConfigParser.url:   URL match verified... setting url to value: {}".format(GitlabGitUrl) in out
    assert "DEBUG   CLS->GitConfigParser.provider:   Provider match {} found!".format('gitlab.com') in out

    # Test passed args
    assert(GitRepo.verbose == True)
    assert(GitRepo.path == TestPath)
    assert(GitRepo._log is None)
    assert(GitRepo._url == GitlabGitUrl)
    assert(GitRepo.url == GitlabGitUrl)
    assert(GitRepo._provider == 'gitlab.com')
    assert(GitRepo.provider == 'gitlab.com')
    assert(GitRepo.user is None)

    # Test object attributes
    assert(GitRepo._log_context == 'CLS->GitConfigParser')

    # Cleanup
    shutil.rmtree(ConfigPath)


def test_url_bitbucket_http(capsys):
    """This test will instantiate a new GitConfigParser object with a mock directory path and verbose=True to test the object instance.
    Test each class property to ensure that the default instantiation values are correct.
    Test the .verbose property to ensure that it has been enabled.
    Test the local logger by parsing the log messages sent and verify that the url setter method fails due to improper file path, .git/config not found.
    Create .git/config directory/file in the set path to test the url property setter method.
    Test url getter method to ensure that a valid url is provided back.
    Test provider setter passing the parsed URL string from the url getter/setter method
    Test provider getter method to ensure that the provider is properly parsed from the provided URL string.
    Test to ensure that the returned provider matchs 'bitbucket.org'
    """

    # Instantiate a GitConfigParser object, and test the returned object instance for default values.

    mock_git_config = """
    [core]
        repositoryformatversion = 0
        filemode = true
        bare = false
        logallrefupdates = true
        ignorecase = true
        precomposeunicode = true
    [user]
        name = Rich Nason
        email = rnason@2ndwatch.com
    [remote "origin"]
        url = {}
        fetch = +refs/heads/*:refs/remotes/origin/*
    """.format(BitBucketHttpUrl)

    # If the file path doesn't exist (Which it shouldn't) then create it for the test, and write a mock git config file.
    if not os.path.exists(ConfigPath):
        os.mkdir(ConfigPath)
    git_config = open(os.path.join(ConfigPath, 'config'), "w")
    git_config.write(mock_git_config)
    git_config.close()

    GitRepo = GitConfigParser(TestPath, verbose=True)
    assert(isinstance(GitRepo, object))

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)
    assert "DEBUG   CLS->GitConfigParser.url:   URL match verified... setting url to value: {}".format(BitBucketHttpUrl) in out
    assert "DEBUG   CLS->GitConfigParser.provider:   Provider match {} found!".format('bitbucket.org') in out

    # Test passed args
    assert(GitRepo.verbose == True)
    assert(GitRepo.path == TestPath)
    assert(GitRepo._log is None)
    assert(GitRepo._url == BitBucketHttpUrl)
    assert(GitRepo.url == BitBucketHttpUrl)
    assert(GitRepo._provider == 'bitbucket.org')
    assert(GitRepo.provider == 'bitbucket.org')
    assert(GitRepo.user == 'mocuser')

    # Test object attributes
    assert(GitRepo._log_context == 'CLS->GitConfigParser')

    # Cleanup
    shutil.rmtree(ConfigPath)


def test_url_bitbucket_git(capsys):
    """This test will instantiate a new GitConfigParser object with a mock directory path and verbose=True to test the object instance.
    Test each class property to ensure that the default instantiation values are correct.
    Test the .verbose property to ensure that it has been enabled.
    Test the local logger by parsing the log messages sent and verify that the url setter method fails due to improper file path, .git/config not found.
    Create .git/config directory/file in the set path to test the url property setter method.
    Test url getter method to ensure that a valid url is provided back.
    Test provider setter passing the parsed URL string from the url getter/setter method
    Test provider getter method to ensure that the provider is properly parsed from the provided URL string.
    Test to ensure that the returned provider matchs 'bitbucket.org'
    """

    # Instantiate a GitConfigParser object, and test the returned object instance for default values.

    mock_git_config = """
    [core]
        repositoryformatversion = 0
        filemode = true
        bare = false
        logallrefupdates = true
        ignorecase = true
        precomposeunicode = true
    [user]
        name = Rich Nason
        email = rnason@2ndwatch.com
    [remote "origin"]
        url = {}
        fetch = +refs/heads/*:refs/remotes/origin/*
    """.format(BitBucketGitUrl)

    # If the file path doesn't exist (Which it shouldn't) then create it for the test, and write a mock git config file.
    if not os.path.exists(ConfigPath):
        os.mkdir(ConfigPath)
    git_config = open(os.path.join(ConfigPath, 'config'), "w")
    git_config.write(mock_git_config)
    git_config.close()

    GitRepo = GitConfigParser(TestPath, verbose=True)
    assert(isinstance(GitRepo, object))

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)
    assert "DEBUG   CLS->GitConfigParser.url:   URL match verified... setting url to value: {}".format(BitBucketGitUrl) in out
    assert "DEBUG   CLS->GitConfigParser.provider:   Provider match {} found!".format('bitbucket.org') in out

    # Test passed args
    assert(GitRepo.verbose == True)
    assert(GitRepo.path == TestPath)
    assert(GitRepo._log is None)
    assert(GitRepo._url == BitBucketGitUrl)
    assert(GitRepo.url == BitBucketGitUrl)
    assert(GitRepo._provider == 'bitbucket.org')
    assert(GitRepo.provider == 'bitbucket.org')
    assert(GitRepo.user is None)

    # Test object attributes
    assert(GitRepo._log_context == 'CLS->GitConfigParser')

    # Cleanup
    shutil.rmtree(ConfigPath)


def test_log():
    """This test will instantiate a new GitConfigParser object with a mock directory path and verbose=True and with log=<LogObject> to test the object instance.
    Test each class property to ensure that the default instantiation values are correct.
    Test the .verbose property to ensure that it has been enabled.
    Test Creation of test Log object, and the passing of that log object to the GitConfigParser object for logging.
    Test that class logging events get pushed to the provided log object instead of the local stdout, stderr logger.
    The Log object will push each Class log event to a Log object list property. Check the DEBUG, INFO, and ERROR lists to ensure they are not empty
    Test the last element of each of the DEBUG, INFO, and ERROR log object list properties for the expected log messages from the GitConfigParser object instantiation.
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
    GitLog = Log()

    # Instantiate a GitConfigParser object, and test the returned object instance for default values.

    mock_git_config = """
    [core]
        repositoryformatversion = 0
        filemode = true
        bare = false
        logallrefupdates = true
        ignorecase = true
        precomposeunicode = true
    [user]
        name = Rich Nason
        email = rnason@2ndwatch.com
    [remote "origin"]
        url = {}
        fetch = +refs/heads/*:refs/remotes/origin/*
    """.format(BitBucketHttpUrl)

    # If the file path doesn't exist (Which it shouldn't) then create it for the test, and write a mock git config file.
    if not os.path.exists(ConfigPath):
        os.mkdir(ConfigPath)
    git_config = open(os.path.join(ConfigPath, 'config'), "w")
    git_config.write(mock_git_config)
    git_config.close()

    GitRepo = GitConfigParser(TestPath, verbose=True, log=GitLog)
    assert(isinstance(GitRepo, object))

    # Test passed args
    assert(GitRepo.verbose == True)
    assert(GitRepo.path == TestPath)
    assert(GitRepo._url == BitBucketHttpUrl)
    assert(GitRepo.url == BitBucketHttpUrl)
    assert(GitRepo._provider == 'bitbucket.org')
    assert(GitRepo.provider == 'bitbucket.org')
    assert(GitRepo.user == 'mocuser')

    # Test the Log object passed to the GitHubAPI init method
    assert(GitRepo._log is not None)
    assert(isinstance(GitRepo._log, object))
    assert(hasattr(GitRepo._log, 'debug'))
    assert(hasattr(GitRepo._log, 'info'))
    assert(hasattr(GitRepo._log, 'error'))
    assert(hasattr(GitRepo._log, 'debug_logs'))
    assert(hasattr(GitRepo._log, 'info_logs'))
    assert(hasattr(GitRepo._log, 'error_logs'))

    # Test the Log object debug_logs, info_logs, and error_logs properties are lists
    assert(isinstance(GitRepo._log.debug_logs, list))
    assert(isinstance(GitRepo._log.info_logs, list))
    assert(isinstance(GitRepo._log.error_logs, list))

    # Test the GitHubLog object to ensure that the lists are not empty (The GitHubAPI flow should add records to each one.)
    assert(len(GitLog.debug_logs) > 0)
    assert(len(GitLog.info_logs) > 0)
    assert(len(GitLog.error_logs) == 0)

    # Test the Log object for the expected output messages from the GitHubAPI instance instantiation by testing the expected value of the last item in each of the lists.
    assert(GitLog.debug_logs[-1] == "CLS->GitConfigParser.provider:   Provider match bitbucket.org found!")
    assert(GitLog.info_logs[-1] == "CLS->GitConfigParser.provider:   Request for provider property received.")

    # Test object attributes
    assert(GitRepo._log_context == 'CLS->GitConfigParser')

    # Cleanup
    shutil.rmtree(ConfigPath)


def cleanup():
    """Test to ensure that if the tests/.git/config file was written that it is properly removed."""
    if os.path.exists(ConfigPath):
        shutil.rmtree(ConfigPath)


