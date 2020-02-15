# Run test suite with `poetry run pytest tests -v`
# Run only this test with `poetry run pytest tests/test_gitconfig_parser.py -v`
################
# Imports:     #
################
from gitutils import GitConfigParser
import pytest, os, sys, shutil, inspect

class BadLog(object):
    """Something other than a logger"""
    def __init__(self):
        self.answer = 42
    
    def divide_answer(self):
        return self.answer / 2


class Log(object):
    """Test Log Object"""

    def __init__(self):
      self.msg = None

    def debug(self, message):
        """Log Debug Messages"""
        print('DEBUG   ' + message, file=sys.stdout)

    def info(self, message):
        """Log Debug Messages"""
        print('INFO    ' + message, file=sys.stdout)

    def warning(self, message):
        """Log Warning Messages"""
        print('WARNING ' + message, file=sys.stdout)

    def error(self, message):
        """Log Debug Messages"""
        print('ERROR  ' + message, file=sys.stderr)

# GitHub Style URLs
GithubHttpUrl = "https://github.com/TheCloudMage/Mock-Repository.git"
GithubGitUrl = "git@github.com:TheCloudMage/Mock-Repository.git"

# GitLab Style URLs
GitlabHttpUrl = "https://gitlab.com/TheCloudMage/Mock-Repository.git"
GitlabGitUrl = "git@gitlab.com:TheCloudMage/Mock-Repository.git"

# BitBucket Style URLs
BitBucketHttpUrl = "https://mocuser@bitbucket.org/TheCloudMage/Mock-Repository.git"
BitBucketGitUrl = "git@bitbucket.org:TheCloudMage/Mock-Repository.git"

TestPath = os.path.join(os.getcwd(), 'gitconfig_testing')
ConfigPath = os.path.join(TestPath, '.git')

######################################
# Setup for class tests
######################################
@pytest.fixture(scope='session', autouse=True)
def setup():
    """ setup any state specific to the execution of the given class (which
    usually contains tests).
    """
    # if os.path.exists(TestPath):
    #   shutil.rmtree(TestPath)

    os.mkdir(TestPath)
    yield
    shutil.rmtree(TestPath)

@pytest.fixture
def create_git_config():
    def _meh(url):
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
        """.format(url)
        
        if os.path.exists(ConfigPath):
              shutil.rmtree(ConfigPath)

        # If the file path doesn't exist (Which it shouldn't) then create it for the test, and write a mock git config file.
        os.mkdir(ConfigPath)
        git_config = open(os.path.join(ConfigPath, 'config'), "w")
        git_config.write(mock_git_config)
        git_config.close()

    return _meh

@pytest.fixture
def destroy_git_config():
    def _meh():
      shutil.rmtree(ConfigPath)
    
    return _meh


######################################
# Test GitHubAPI Repository Object:  #
######################################
def test_init():
    """This test will instantiate a new GitConfigParser object with a mock directory path to test the object instance for default values.
    Test each class property to ensure that the default instantiation values are correct.
    Test the url method to ensure that failure with invalid path, directory doesn't exist.
    """

    # Ensure TestPath exists...
    assert(os.path.exists(TestPath))
    
    # Instantiate a GitConfigParser object, and test the returned object instance for default values.
    GitRepo = GitConfigParser(TestPath)
    assert(isinstance(GitRepo, object))
    # print('ROCK!!! ' + GitRepo.url + '::' + GitRepo._path + '::' + GitRepo._log_context)

    # Test passed args
    assert(GitRepo.verbose == False)
    assert(GitRepo._path == TestPath)
    assert(GitRepo._log is None)
    assert(GitRepo._log_context == "CLS->GitConfigParser")
    assert(GitRepo._url is None)
    assert(GitRepo._provider is None)
    assert(GitRepo.url == 'url property has no value assigned!')
    assert(GitRepo.provider == 'provider property has no value assigned!')
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

    # Instantiate a GitConfigParser object, and test the returned object instance for default values.
    GitRepo = GitConfigParser(TestPath, verbose=True)
    assert(isinstance(GitRepo, object))
    assert(GitRepo._log_context == "CLS->GitConfigParser")

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)
    assert "ERROR   CLS->GitConfigParser.provider:   Valid provider repository url argument expected string but received type: <class 'NoneType'>" in err
    assert "ERROR   CLS->GitConfigParser.url:   Valid url path argument expected string but received type: <class 'NoneType'>" in err

    # Test passed args
    assert(GitRepo.verbose == True)

def test_url_from_gitters(capsys, create_git_config, destroy_git_config):
    for providerUrl in [GithubHttpUrl, GithubGitUrl, GitlabHttpUrl, GitlabGitUrl, BitBucketHttpUrl, BitBucketGitUrl]:
        create_git_config(providerUrl)
    
        GitRepo = GitConfigParser(TestPath, verbose=True)
        assert(isinstance(GitRepo, object))

        # Test passed args
        assert(GitRepo.verbose == True)
        assert(GitRepo._url == providerUrl)
        assert(GitRepo.url == providerUrl)
        assert(GitRepo._provider is not None)
        assert(GitRepo.provider is not None)

        # Capture stdout, stderr to test log messages
        out, err = capsys.readouterr()
        sys.stdout.write(out)
        sys.stderr.write(err)

        assert "INFO    CLS->GitConfigParser.url:   'URL' string match verified... Updating url property with value: {}".format(providerUrl) in out
        assert "DEBUG   CLS->GitConfigParser.provider:   Provider match {} found!".format(GitRepo.provider) in out
        
        if GitRepo._provider == 'github.com' and GitRepo.provider == 'github.com':
            assert(GitRepo.user == 'No user found in URL string.')
        
        if GitRepo._provider == 'gitlab.com' and GitRepo.provider == 'gitlab.com':
            assert(GitRepo.user == 'No user found in URL string.')
        
        if GitRepo._provider == 'bitbucket.org' and GitRepo.provider == 'bitbucket.org':
            if GitRepo.url.startswith('http'):
                assert(GitRepo.user == 'mocuser')
            else:
                assert(GitRepo.user == 'No user found in URL string.')

        destroy_git_config()


def test_log():
    """This test will instantiate a new GitConfigParser object with a mock directory path and verbose=True and with log=<LogObject> to test the object instance.
    Test each class property to ensure that the default instantiation values are correct.
    Test the .verbose property to ensure that it has been enabled.
    Test Creation of test Log object, and the passing of that log object to the GitConfigParser object for logging.
    Test that class logging events get pushed to the provided log object instead of the local stdout, stderr logger.
    The Log object will push each Class log event to a Log object list property. Check the DEBUG, INFO, and ERROR lists to ensure they are not empty
    Test the last element of each of the DEBUG, INFO, and ERROR log object list properties for the expected log messages from the GitConfigParser object instantiation.
    """
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
    assert(GitRepo._path == TestPath)
    assert(GitRepo._url == BitBucketHttpUrl)
    assert(GitRepo.url == BitBucketHttpUrl)
    assert(GitRepo._provider == 'bitbucket.org')
    assert(GitRepo.provider == 'bitbucket.org')
    assert(GitRepo.user == 'mocuser')

    # Test the Log object passed to the GitHubAPI init method
    assert(GitRepo._log is not None)
    assert(GitRepo._log_context == 'CLS->GitConfigParser')
    assert(isinstance(GitRepo._log, object))
    assert(hasattr(GitRepo._log, 'debug'))
    assert(hasattr(GitRepo._log, 'info'))
    assert(hasattr(GitRepo._log, 'warning'))
    assert(hasattr(GitRepo._log, 'error'))

# Negative Tests (expected failuers).
def test_fails_and_coverage(capsys, create_git_config, destroy_git_config):
    GitRepo = GitConfigParser(TestPath)
    GitRepo.verbose = True

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)
    
    assert 'INFO    CLS->GitConfigParser.verbose:   Updated verbose property with value: True' in out
    
    with pytest.raises(TypeError):
      GitRepo.log('This is a message', 'info')
    
    with pytest.raises(TypeError):
      GitRepo.log('This is a message')
    
    with pytest.raises(TypeError):
      GitRepo.log()

    GitRepo.log('This is a message for warning purposes.', 'warning', 'TESTS')

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)

    assert 'WARNING CLS->GitConfigParser.TESTS:   This is a message for warning purposes.' in out

    GitRepo.log('Message', 42, 2)
    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)

    assert "ERROR   CLS->GitConfigParser.log:   An EXCEPTION has occurred in 'CLS->GitConfigParser.log', on line 182: -> 'int' object has no attribute 'lower'" in err

    GitRepo.verbose = 42
    
    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)
    
    assert "ERROR   CLS->GitConfigParser.verbose:   Property verbose argument expected bool but received type: <class 'int'>. Aborting update!" in err

    BadProtocolBitbucket = "meh://mocuser@bitbucket.org/TheCloudMage/Mock-Repository.git"

    create_git_config(BadProtocolBitbucket)

    GitRepo = GitConfigParser(TestPath, verbose=True)

    GitRepo.url = ConfigPath

    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)

    destroy_git_config()
    
    assert "WARNING CLS->GitConfigParser.url:   'URL' match failed format verification on match string: meh://mocuser@bitbucket.org/TheCloudMage/Mock-Repository.git" in out

    GitRepo = GitConfigParser(TestPath, verbose=True)
    GitRepo.url = './meheheheh'

    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)

    assert "ERROR   CLS->GitConfigParser.url:   Provided directory path does not exist. Aborting property update!" in err

    GitRepo.url = 42

    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)

    assert "ERROR   CLS->GitConfigParser.url:   Valid url path argument expected string but received type: <class 'int'>" in err

    GitRepo.provider = BadProtocolBitbucket

    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)

    assert "ERROR   CLS->GitConfigParser.provider:   URL meh://mocuser@bitbucket.org/TheCloudMage/Mock-Repository.git not properly formatted, aborting provider searc" in err

    GitRepo.provider = 'https:github.com/42.lower()/Mock-Repository.git'

    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)

    assert "ERROR   CLS->GitConfigParser.provider:   Parsed provider value: None not found or invalid. Aborting provider search!" in err

    GitLog = Log()
    GitRepo = GitConfigParser(TestPath, True, GitLog)

    assert(GitRepo.verbose is True)
    assert(GitRepo._log is not None)
    
    GitRepo.log('WARNING WARNING WARNING', 'warning', 'rich-was-here')
    
    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)

    assert "WARNING CLS->GitConfigParser.rich-was-here:   WARNING WARNING WARNING" in out

    GitLog = BadLog()
    GitRepo = GitConfigParser(TestPath, True, GitLog)

    assert(GitRepo.verbose is True)
    assert(GitRepo._log is None)

