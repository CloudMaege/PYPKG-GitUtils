# Run PyTest:
# `poetry run pytest tests -v`
# Run single test file instead of entire test suite:
# `poetry run pytest tests/test_github_reports.py -v`
# Run single test from a single test file
# `poetry run pytest tests/test_github_reports.py::{testname} -v`

# Run Coverage Report:
# poetry run coverage run -m --source=. pytest tests/test_github_reports.py
# poetry run coverage html --omit=tests/* -i

################
# Imports:     #
################

# Pip Installed Imports:
from cloudmage.gitutils import GithubReports

# Base Python Module Imports:
import pytest
import os
import shutil
import sys

TestPath = os.path.join(os.getcwd(), 'gitreport_testing')

######################################
# Define Set and Teardown Fixtures:  #
######################################
@pytest.fixture(scope='session', autouse=True)
def setup():
    """ GithubReports Class PyTest Environment Setup and Teardown Fixture

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


######################################
# Test Init Defaults:                #
######################################
def test_init():
    """ GithubReports Class Constructor Init Test

    This test will instantiate a new GithubReports object and test to ensure
    that the object attributes match the expected instantiation values that
    should be set by the class init constructor.

    Expected Result:
      Constructor values should be set to their default settings.
    """

    # Ensure TestPath exists...
    assert(os.path.exists(TestPath))

    # Instantiate a GithubReports object,
    # and test the returned object instance for default values.
    GitHubReportObj = GithubReports()
    assert(isinstance(GitHubReportObj, object))

    # Test passed args
    assert(not GitHubReportObj._verbose)
    assert(not GitHubReportObj.verbose)
    assert(GitHubReportObj._log is None)
    assert(GitHubReportObj._log_context == "CLS->GitHubReports")
    assert(GitHubReportObj._auth_token is None)
    assert(GitHubReportObj._now is not None)
    assert(GitHubReportObj._repo_namespace is None)
    assert(not GitHubReportObj._is_organization)
    assert(not GitHubReportObj._notify)
    assert(GitHubReportObj._open_pr_threshold == 5)
    assert(GitHubReportObj._search_results is None)
    assert(GitHubReportObj.template_path is not None)
    assert('templates' in GitHubReportObj.template_path)


######################################
# Test Verbose:                      #
######################################
def test_verbose_init_enabled():
    """ GithubReports Class 'verbose' Property Init Test

    This test will test the verbose getter and setter property methods.
    Default value tested during init test, test setting value to True
    during object instantiation, using the class constructor.

    Expected Result:
      'verbose' property should be set to True.
    """

    # Instantiate a GithubReports object, and test for expected test values.
    GitHubReportObj = GithubReports(verbose=True)
    assert(isinstance(GitHubReportObj, object))

    # Test verbose is set to True
    assert(GitHubReportObj._verbose)
    assert(GitHubReportObj.verbose)


def test_verbose_setter_enabled():
    """ GithubReports Class 'verbose' Property Setter Test

    This test will test the verbose getter and setter property methods.
    Default value tested during init test, test setting value to True
    using the class verbose setter method.

    Expected Result:
      'verbose' property should be set to True.
    """

    # Instantiate a GithubReports object, and test for expected test values.
    GitHubReportObj = GithubReports()
    assert(isinstance(GitHubReportObj, object))

    # Test verbose is set to default False
    assert(not GitHubReportObj._verbose)
    assert(not GitHubReportObj.verbose)

    # Call the Setter to enable verbose and test the property value is True
    GitHubReportObj.verbose = True
    assert(GitHubReportObj._verbose)
    assert(GitHubReportObj.verbose)


def test_verbose_init_invalid():
    """ GithubReports Class 'verbose' Property Init Invalid Value Test

    This test will test the verbose getter and setter property methods.
    Default value tested during init test, test setting value to invalid value
    during object instantiation, using the class constructor.

    Expected Result:
      'verbose' property should be set to False, ignoring the invalid value.
    """

    # Instantiate a GithubReports object, and test for expected test values.
    GitHubReportObj = GithubReports(verbose=42)
    assert(isinstance(GitHubReportObj, object))

    # Test verbose is False default value, ignoring invalid input value
    assert(not GitHubReportObj._verbose)
    assert(not GitHubReportObj.verbose)


def test_verbose_setter_invalid(capsys):
    """ GithubReports Class 'verbose' Property Setter Invalid Value Test

    This test will test the verbose getter and setter property methods.
    Default value tested during init test, test setting value to invalid value
    using the property setter method.

    Expected Result:
      'verbose' property should be set to False, ignoring the invalid value.
    """

    # Instantiate a GithubReports object, and test for expected test values.
    GitHubReportObj = GithubReports()
    assert(isinstance(GitHubReportObj, object))

    # Test verbose setting was defaulted to False
    assert(not GitHubReportObj._verbose)
    assert(not GitHubReportObj.verbose)

    # Set verbose to an invalid value using property settter and test the
    # value ensuring that the invalid value was ignored, and is set False.
    GitHubReportObj.verbose = 42
    assert(not GitHubReportObj._verbose)
    assert(not GitHubReportObj.verbose)

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->GitHubReports.verbose: \
-> verbose property argument expected type bool but received type:" in err


######################################
# Test Auth_Token Property:          #
######################################
def test_auth_token_init_enabled():
    """ GithubReports Class 'auth_token' Property Init Test

    This test will test the auth_token getter and setter property methods.
    Default value tested during init test, test setting value to string
    during object instantiation, using the class constructor.

    Expected Result:
      'auth_token' property should be set to provided string.
    """

    # Instantiate a GithubReports object, and test for expected test values.
    GitHubReportObj = GithubReports(auth_token="12345678910987654321")
    assert(isinstance(GitHubReportObj, object))

    # Test auth_token is set to provided string
    assert(GitHubReportObj._auth_token == "12345678910987654321")
    assert(GitHubReportObj.auth_token == "12345678910987654321")


def test_auth_token_setter_enabled():
    """ GithubReports Class 'auth_token' Property Setter Test

    This test will test the auth_token getter and setter property methods.
    Default value tested during init test, test setting value to provided
    string using the class auth_token setter method.

    Expected Result:
      'auth_token' property should be set to provided string value.
    """

    # Instantiate a GithubReports object, and test for expected test values.
    GitHubReportObj = GithubReports()
    assert(isinstance(GitHubReportObj, object))

    # Test auth_token is set to default False
    assert(GitHubReportObj._auth_token is None)
    assert(GitHubReportObj.auth_token is None)

    # Call the Setter to enable auth_token and test the property value is
    # set to the provided string value.
    GitHubReportObj.auth_token = "12345678910987654321"
    assert(GitHubReportObj._auth_token == "12345678910987654321")
    assert(GitHubReportObj.auth_token == "12345678910987654321")


def test_auth_token_init_invalid():
    """ GithubReports Class 'auth_token' Property Init Invalid Value Test

    This test will test the auth_token getter and setter property methods.
    Default value tested during init test, test setting value to invalid value
    during object instantiation, using the class constructor.

    Expected Result:
      'auth_token' property should be set to False, ignoring the invalid value.
    """

    # Instantiate a GithubReports object, and test for expected test values.
    GitHubReportObj = GithubReports(auth_token=42)
    assert(isinstance(GitHubReportObj, object))

    # Test verbose is False default value, ignoring invalid input value
    assert(GitHubReportObj._auth_token is None)
    assert(GitHubReportObj.auth_token is None)


def test__auth_token_setter_invalid(capsys):
    """ GithubReports Class 'auth_token' Property Setter Invalid Value Test

    This test will test the auth_token getter and setter property methods.
    Default value tested during init test, test setting value to invalid value
    using the property setter method.

    Expected Result:
      'auth_token' property should be set to False, ignoring the invalid value.
    """

    # Instantiate a GithubReports object, and test for expected test values.
    GitHubReportObj = GithubReports()
    assert(isinstance(GitHubReportObj, object))

    # Test auth_token setting was defaulted to None
    assert(GitHubReportObj._auth_token is None)
    assert(GitHubReportObj.auth_token is None)

    # Set auth_token to an invalid value using property settter and test the
    # value ensuring that the invalid value was ignored, and is set None.
    GitHubReportObj.auth_token = 42
    assert(GitHubReportObj._auth_token is None)
    assert(GitHubReportObj.auth_token is None)

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->GitHubReports.auth_token: \
-> auth_token property argument expected type str but received type:" in err


######################################
# Test Logging:                      #
######################################
def test_logs_verbose_disabled(capsys):
    """ GithubReports Class Verbose Disabled Log Test

    This test will test to ensure that when verbose mode is disabled
    that no logs other then errors are output.

    Expected Result:
      Logged events are silent, Error messages are output to the console.
    """

    # Instantiate a GithubReports object
    # Test the returned object verbose attribute for expected values.
    GitHubReportObj = GithubReports(verbose=False)
    assert(isinstance(GitHubReportObj, object))

    # Test verbose setting
    assert(not GitHubReportObj._verbose)

    # Write a test log entry
    GitHubReportObj.log("Pytest debug log write test", 'debug', 'test_log')
    GitHubReportObj.log("Pytest info log write test", 'info', 'test_log')
    GitHubReportObj.log("Pytest warning log write test", 'warning', 'test_log')
    GitHubReportObj.log("Pytest error log write test", 'error', 'test_log')

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "DEBUG   CLS->GitHubReports.test_log: \
-> Pytest debug log write test" not in out
    assert "INFO    CLS->GitHubReports.test_log: \
-> Pytest info log write test" not in out
    assert "WARNING CLS->GitHubReports.test_log: \
-> Pytest warning log write test" not in out
    assert "ERROR   CLS->GitHubReports.test_log: \
-> Pytest error log write test" in err


def test_logs_verbose_enabled(capsys):
    """ GithubReports Class Verbose Enabled Log Test

    This test will test to ensure that when verbose mode is enabled
    that all logs are written to stdout, stderr

    Expected Result:
      Logged events are written to stdout, stderr. Verbose enabled.
    """

    # Instantiate a GithubReports object, and test for expected test values.
    GitHubReportObj = GithubReports(verbose=True)
    assert(isinstance(GitHubReportObj, object))

    # Test verbose setting was correctly set to input True value
    assert(GitHubReportObj._verbose)
    assert(GitHubReportObj.verbose)

    # Write a test log entry to each log level
    GitHubReportObj.log("Pytest debug log write test", 'debug', 'test_log')
    GitHubReportObj.log("Pytest info log write test", 'info', 'test_log')
    GitHubReportObj.log("Pytest warning log write test", 'warning', 'test_log')
    GitHubReportObj.log("Pytest error log write test", 'error', 'test_log')

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "DEBUG   CLS->GitHubReports.test_log: \
-> Pytest debug log write test" in out
    assert "INFO    CLS->GitHubReports.test_log: \
-> Pytest info log write test" in out
    assert "WARNING CLS->GitHubReports.test_log: \
-> Pytest warning log write test" in out
    assert "ERROR   CLS->GitHubReports.test_log: \
-> Pytest error log write test" in err


def test_logs_logger_object(capsys):
    """ GithubReports Class Log Object Test

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

    # Instantiate a GithubReports object, and test for expected test values.
    GitHubReportObj = GithubReports(verbose=True, log=LogObj)
    assert(isinstance(GitHubReportObj, object))
    assert(isinstance(GitHubReportObj._log, object))
    assert(isinstance(GitHubReportObj.log, object))

    # Test verbose setting
    assert(GitHubReportObj._verbose)
    assert(GitHubReportObj.verbose)
    assert(GitHubReportObj._log is not None)

    # Test the Log object to make sure the expected object attributes exist
    assert(hasattr(GitHubReportObj._log, 'debug'))
    assert(hasattr(GitHubReportObj._log, 'info'))
    assert(hasattr(GitHubReportObj._log, 'warning'))
    assert(hasattr(GitHubReportObj._log, 'error'))
    assert(hasattr(GitHubReportObj._log, 'debug_logs'))
    assert(hasattr(GitHubReportObj._log, 'info_logs'))
    assert(hasattr(GitHubReportObj._log, 'warning_logs'))
    assert(hasattr(GitHubReportObj._log, 'error_logs'))

    # Write test log entries for each of the different types of logs
    GitHubReportObj.log("Pytest log debug test", 'debug', 'test_log_object')
    GitHubReportObj.log("Pytest log info test", 'info', 'test_log_object')
    GitHubReportObj.log(
        "Pytest log warning test", 'warning', 'test_log_object'
    )
    GitHubReportObj.log("Pytest log error test", 'error', 'test_log_object')

    # Test that the Log object debug_logs, info_logs, warning_logs and
    # error_logs properties are lists
    assert(isinstance(GitHubReportObj._log.debug_logs, list))
    assert(isinstance(GitHubReportObj._log.info_logs, list))
    assert(isinstance(GitHubReportObj._log.warning_logs, list))
    assert(isinstance(GitHubReportObj._log.error_logs, list))

    # Test that each of the log_lists have items written into them
    assert(len(LogObj.debug_logs) >= 1)
    assert(len(LogObj.info_logs) >= 1)
    assert(len(LogObj.warning_logs) >= 1)
    assert(len(LogObj.error_logs) >= 1)

    # Test the log messages to make sure they match the written logs
    assert(
        LogObj.debug_logs[-1] == "CLS->GitHubReports.test_log_object: \
-> Pytest log debug test"
    )
    assert(
        LogObj.info_logs[-1] == "CLS->GitHubReports.test_log_object: \
-> Pytest log info test"
    )
    assert(
        LogObj.warning_logs[-1] == "CLS->GitHubReports.test_log_object: \
-> Pytest log warning test"
    )
    assert(
        LogObj.error_logs[-1] == "CLS->GitHubReports.test_log_object: \
-> Pytest log error test"
    )


def test_logs_invalid_object(capsys):
    """ GithubReports Class Invalid Log Object Test

    This test will test the log method to ensure that
    if the logs constructor object is provided an invalid log object
    to write to that the invalid object will be ignored, resulting in
    all class logs being written to stdout, stderr.

    Expected Result:
      Invalid object ignored. Logged events are written to stdout, stderr.
    """

    # Test to ensure that passing a non valid log object is properly caught.
    GitHubReportObj = GithubReports(verbose=True, log=42)
    assert(isinstance(GitHubReportObj, object))
    assert(GitHubReportObj._log is None)

    # Write a test log entry to each log level
    GitHubReportObj.log("Pytest debug log write test", 'debug', 'test_log')
    GitHubReportObj.log("Pytest info log write test", 'info', 'test_log')
    GitHubReportObj.log("Pytest warning log write test", 'warning', 'test_log')
    GitHubReportObj.log("Pytest error log write test", 'error', 'test_log')

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "DEBUG   CLS->GitHubReports.test_log: \
-> Pytest debug log write test" in out
    assert "INFO    CLS->GitHubReports.test_log: \
-> Pytest info log write test" in out
    assert "WARNING CLS->GitHubReports.test_log: \
-> Pytest warning log write test" in out
    assert "ERROR   CLS->GitHubReports.test_log: \
-> Pytest error log write test" in err


####################################
# Test Exception handler method:   #
####################################
def test_exception_handler(capsys):
    """ GithubReports Class Exception Handler Test

    This test will test the class wide exception handler.

    Expected Result:
      When an exception condition is encountered,
      exceptions will output in correct format to stderr.
    """

    # Instantiate a GithubReports object, and test for expected test values.
    GitHubReportObj = GithubReports(verbose=True)
    assert(isinstance(GitHubReportObj, object))

    # Write a log with a bad value to trigger an exception.
    GitHubReportObj.log('Message', 42, 2)

    # Capture stdout, stderr to check the log messages
    # for the expected outputs.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->GitHubReports.log: \
-> EXCEPTION occurred in: CLS->GitHubReports.log" in err


######################################
# Test Repo_Namespace Property:      #
######################################
def test_repo_namespace_setter_enabled():
    """ GithubReports Class 'repo_namespace' Property Setter Test

    This test will test the 'repo_namespace' getter and setter property
    methods. Default value tested during init test, test setting value to
    provided string using the class 'repo_namespace' setter method.

    Expected Result:
      'repo_namespace' property should be set to provided string value.
    """

    # Instantiate a GithubReports object, and test for expected test values.
    GitHubReportObj = GithubReports()
    assert(isinstance(GitHubReportObj, object))

    # Test repo_namespace is set to default False
    assert(GitHubReportObj._repo_namespace is None)
    assert(GitHubReportObj.repo_namespace is None)

    # Call the Setter to enable repo_namespace and test the property value is
    # set to the provided string value.
    GitHubReportObj.repo_namespace = "TheCloudMage"
    assert(GitHubReportObj._repo_namespace == "TheCloudMage")
    assert(GitHubReportObj.repo_namespace == "TheCloudMage")


def test_repo_namespace_setter_invalid(capsys):
    """ GithubReports Class 'repo_namespace' Property Setter Invalid Val Test

    This test will test the 'repo_namespace' getter and setter property
    methods. Default value tested during init test, test setting value to
    invalid value using the property setter method.

    Expected Result:
      'repo_namespace' property should be set to None,
      ignoring the invalid value.
    """

    # Instantiate a GithubReports object, and test for expected test values.
    GitHubReportObj = GithubReports()
    assert(isinstance(GitHubReportObj, object))

    # Test repo_namespace setting was defaulted to None
    assert(GitHubReportObj._repo_namespace is None)
    assert(GitHubReportObj.repo_namespace is None)

    # Set repo_namespace to an invalid value using property settter and
    # test the value ensuring that the invalid value was ignored,
    # and is set None.
    GitHubReportObj.repo_namespace = 42
    assert(GitHubReportObj._repo_namespace is None)
    assert(GitHubReportObj.repo_namespace is None)

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->GitHubReports.repo_namespace: \
-> repo_namespace property argument expected type str but received " in err


######################################
# Test Is_Organization Property:     #
######################################
def test_is_organization_setter_enabled():
    """ GithubReports Class 'is_organization' Property Setter Test

    This test will test the 'is_organization' getter and setter property
    methods. Default value tested during init test, test setting value to
    true using the class 'is_organization' setter method.

    Expected Result:
      'is_organization' property should be set to True.
    """

    # Instantiate a GithubReports object, and test for expected test values.
    GitHubReportObj = GithubReports()
    assert(isinstance(GitHubReportObj, object))

    # Test is_organization is set to default False
    assert(not GitHubReportObj._is_organization)
    assert(not GitHubReportObj.is_organization)

    # Call the Setter to enable is_organization and test the property value is
    # set to True value.
    GitHubReportObj.is_organization = True
    assert(GitHubReportObj._is_organization)
    assert(GitHubReportObj.is_organization)


def test_is_organization_setter_invalid(capsys):
    """ GithubReports Class 'is_organization' Property Setter Invalid Val Test

    This test will test the 'is_organization' getter and setter property
    methods. Default value tested during init test, test setting value to
    invalid value using the property setter method.

    Expected Result:
      'is_organization' property should be set to False,
      ignoring the invalid value.
    """

    # Instantiate a GithubReports object, and test for expected test values.
    GitHubReportObj = GithubReports()
    assert(isinstance(GitHubReportObj, object))

    # Test is_organization setting was defaulted to False
    assert(not GitHubReportObj._is_organization)
    assert(not GitHubReportObj.is_organization)

    # Set is_organization to an invalid value using property settter and
    # test the value ensuring that the invalid value was ignored, and is
    # set False.
    GitHubReportObj.is_organization = 42
    assert(not GitHubReportObj._is_organization)
    assert(not GitHubReportObj.is_organization)

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->GitHubReports.is_organization: \
-> is_organization property argument expected type bool but received " in err


######################################
# Test Notify Property:              #
######################################
def test_notify_setter_enabled():
    """ GithubReports Class 'notify' Property Setter Test

    This test will test the 'notify' getter and setter property
    methods. Default value tested during init test, test setting value to
    True using the class 'notify' setter method.

    Expected Result:
      'notify' property should be set to True.
    """

    # Instantiate a GithubReports object, and test for expected test values.
    GitHubReportObj = GithubReports()
    assert(isinstance(GitHubReportObj, object))

    # Test notify is set to default False
    assert(not GitHubReportObj._notify)
    assert(not GitHubReportObj.notify)

    # Call the Setter to enable notify and test the property value is
    # set to True value.
    GitHubReportObj.notify = True
    assert(GitHubReportObj._notify)
    assert(GitHubReportObj.notify)


def test_notify_setter_invalid(capsys):
    """ GithubReports Class 'notify' Property Setter Invalid Val Test

    This test will test the 'notify' getter and setter property
    methods. Default value tested during init test, test setting value to
    invalid value using the property setter method.

    Expected Result:
      'notify' property should be set to False,
      ignoring the invalid value.
    """

    # Instantiate a GithubReports object, and test for expected test values.
    GitHubReportObj = GithubReports()
    assert(isinstance(GitHubReportObj, object))

    # Test notify setting was defaulted to False
    assert(not GitHubReportObj._notify)
    assert(not GitHubReportObj.notify)

    # Set notify to an invalid value using property settter and test the
    # value ensuring that the invalid value was ignored, and is set False.
    GitHubReportObj.notify = 42
    assert(not GitHubReportObj._notify)
    assert(not GitHubReportObj.notify)

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->GitHubReports.notify: \
-> notify property argument expected type bool but received type:" in err


######################################
# Test Open_PR_Threshold Property:   #
######################################
def test_open_pr_threshold_setter_enabled():
    """ GithubReports Class 'open_pr_threshold' Property Setter Test

    This test will test the 'open_pr_threshold' getter and setter property
    methods. Default value tested during init test, test setting value to
    valid int value using the class 'open_pr_threshold' setter method.

    Expected Result:
      'open_pr_threshold' property should be set to provided int value.
    """

    # Instantiate a GithubReports object, and test for expected test values.
    GitHubReportObj = GithubReports()
    assert(isinstance(GitHubReportObj, object))

    # Test open_pr_threshold is set to default 5
    assert(GitHubReportObj._open_pr_threshold == 5)
    assert(GitHubReportObj.open_pr_threshold == 5)

    # Call the Setter to enable open_pr_threshold and test the property
    # value is set to provided int value value.
    GitHubReportObj.open_pr_threshold = 3
    assert(GitHubReportObj._open_pr_threshold == 3)
    assert(GitHubReportObj.open_pr_threshold == 3)


def test_open_pr_threshold_setter_invalid(capsys):
    """ GithubReports 'open_pr_threshold' Property Setter Invalid Val Test

    This test will test the 'open_pr_threshold' getter and setter property
    methods. Default value tested during init test, test setting value to
    invalid value using the property setter method.

    Expected Result:
      'open_pr_threshold' property should be set to 5 (default value),
      ignoring the invalid value.
    """

    # Instantiate a GithubReports object, and test for expected test values.
    GitHubReportObj = GithubReports()
    assert(isinstance(GitHubReportObj, object))

    # Test open_pr_threshold setting was defaulted to 5
    assert(GitHubReportObj._open_pr_threshold == 5)
    assert(GitHubReportObj.open_pr_threshold == 5)

    # Set open_pr_threshold to an invalid value using property settter
    # and test the value ensuring that the invalid value was ignored,
    # and is set to default value of 5.
    GitHubReportObj.open_pr_threshold = True
    assert(GitHubReportObj._open_pr_threshold == 5)
    assert(GitHubReportObj.open_pr_threshold == 5)

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->GitHubReports.open_pr_threshold: \
-> open_pr_threshold property argument expected type int but received " in err


######################################
# Test Open_PR_Threshold Property:   #
######################################
def test_search_open_pulls_no_token_or_namespace(capsys):
    """ GithubReports Class 'test_search_open_pulls' Method Test

    This test will test the 'test_search_open_pulls' method. The method
    is designed to run a search against Github for number of open PRs
    across a given organization or user account.

    This test will attempt to call the search_open_pulls() method
    without a set auth_token or repo_namespace configured.

    Expected Result:
        return object should be None.
        Log Error no auth_token
    """

    # Instantiate a GithubReports object, and test for expected test values.
    GitHubReportObj = GithubReports(verbose=True)
    assert(isinstance(GitHubReportObj, object))

    assert(GitHubReportObj.auth_token is None)
    assert(GitHubReportObj.repo_namespace is None)
    search_results = GitHubReportObj.search_open_pulls()
    assert(search_results is None)

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->GitHubReports.search_open_pulls: \
-> Github auth_token required to call this method" in err


def test_search_open_pulls_no_namespace(capsys):
    """ GithubReports Class 'test_search_open_pulls' Method Test

    This test will test the 'test_search_open_pulls' method. The method
    is designed to run a search against Github for number of open PRs
    across a given organization or user account.

    This test will attempt to call the search_open_pulls() method
    without repo_namespace configured. auth_token will be tested
    by using the auth_token property setter.

    Expected Result:
        return object should be None.
        Log Error no repo_namespace
    """
    # Instantiate a GithubReports object, and test for expected test values.
    GitHubReportObj = GithubReports(verbose=True)
    assert(isinstance(GitHubReportObj, object))

    assert(GitHubReportObj.auth_token is None)
    assert(GitHubReportObj.repo_namespace is None)

    # Set the Auth Token
    GitHubReportObj.auth_token = "12345678910987654321"
    assert(GitHubReportObj.auth_token == "12345678910987654321")
    assert(GitHubReportObj.repo_namespace is None)

    # Call the method
    search_results = GitHubReportObj.search_open_pulls()
    assert(search_results is None)

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->GitHubReports.search_open_pulls: \
-> Github repo_namespace required to call this method" in err


def test_search_open_pulls_no_namespace_2(capsys):
    """ GithubReports Class 'test_search_open_pulls' Method Test

    This test will test the 'test_search_open_pulls' method. The method
    is designed to run a search against Github for number of open PRs
    across a given organization or user account.

    This test will attempt to call the search_open_pulls() method
    without repo_namespace configured. auth_token will be tested
    being passed into the instance init and set by the constructor.

    Expected Result:
        return object should be None.
        Log Error no repo_namespace
    """
    # Instantiate a GithubReports object, and test for expected test values.
    GitHubReportObj = GithubReports(
        verbose=True,
        auth_token="12345678910987654321"
    )
    assert(isinstance(GitHubReportObj, object))

    assert(GitHubReportObj.auth_token == "12345678910987654321")
    assert(GitHubReportObj.repo_namespace is None)

    # Call the method
    search_results = GitHubReportObj.search_open_pulls()
    assert(search_results is None)

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->GitHubReports.search_open_pulls: \
-> Github repo_namespace required to call this method" in err


def test_search_open_pulls_no_namespace_3(capsys):
    """ GithubReports Class 'test_search_open_pulls' Method Test

    This test will test the 'test_search_open_pulls' method. The method
    is designed to run a search against Github for number of open PRs
    across a given organization or user account.

    This test will attempt to call the search_open_pulls() method
    without a or repo_namespace configured. auth_token will be tested
    by being passed as a method argument.

    Expected Result:
        return object should be None.
        Log Error no repo_namespace
    """
    # Instantiate a GithubReports object, and test for expected test values.
    GitHubReportObj = GithubReports(verbose=True)
    assert(isinstance(GitHubReportObj, object))

    assert(GitHubReportObj.auth_token is None)
    assert(GitHubReportObj.repo_namespace is None)

    # Call the method
    search_results = GitHubReportObj.search_open_pulls(
        auth_token="12345678910987654321"
    )
    assert(GitHubReportObj.auth_token == "12345678910987654321")
    assert(GitHubReportObj.repo_namespace is None)
    assert(search_results is None)

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->GitHubReports.search_open_pulls: \
-> Github repo_namespace required to call this method" in err


def test_search_open_pulls_invalid_token(capsys):
    """ GithubReports Class 'test_search_open_pulls' Method Test

    This test will test the 'test_search_open_pulls' method. The method
    is designed to run a search against Github for number of open PRs
    across a given organization or user account.

    This test will attempt to call the search_open_pulls() method
    with an invalid auth token. Auth Token will be set at
    init, and repo_namespace will be tested using the repo_namespace
    property setter. As the auth_token will be invalid, a Github object
    instantiation exception should be triggered and Error logged.

    Expected Result:
        return object should be None.
        Log Error Bad Credentials Exception
    """
    # Instantiate a GithubReports object, and test for expected test values.
    GitHubReportObj = GithubReports(
        verbose=True,
        auth_token="12345678910987654321"
    )
    assert(isinstance(GitHubReportObj, object))

    assert(GitHubReportObj.auth_token == "12345678910987654321")
    assert(GitHubReportObj.repo_namespace is None)

    # Set the namespace
    GitHubReportObj.repo_namespace = "TheCloudMage"
    assert(GitHubReportObj.repo_namespace == "TheCloudMage")

    # Call the Search method, and expect Bad Credentials exception
    # with pytest.raises(
    #     Exception,
    #     match=r'401 {"message": "Bad credentials"'
    # ):
    #     # Call Search, expect BadCredentials Exception
    #     search_results = GitHubReportObj.search_open_pulls()
    #     assert(search_results is None)
    search_results = GitHubReportObj.search_open_pulls()
    assert(search_results is None)

    # Call the method
    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "EXCEPTION occurred in" in err
    assert "401 {\"message\": \"Bad credentials\"" in err


def test_search_open_pulls_invalid_token_2(capsys):
    """ GithubReports Class 'test_search_open_pulls' Method Test

    This test will test the 'test_search_open_pulls' method. The method
    is designed to run a search against Github for number of open PRs
    across a given organization or user account.

    This test will attempt to call the search_open_pulls() method
    with an invalid auth token. Auth Token will be set at
    init, and repo_namespace will be tested by passing the value
    as a method argument. As the auth_token will be invalid, a Github object
    instantiation exception should be triggered and Error logged.

    Expected Result:
        return object should be None.
        Log Error Bad Credentials Exception
    """
    # Instantiate a GithubReports object, and test for expected test values.
    GitHubReportObj = GithubReports(
        verbose=True,
        auth_token="12345678910987654321"
    )
    assert(isinstance(GitHubReportObj, object))

    assert(GitHubReportObj.auth_token == "12345678910987654321")
    assert(GitHubReportObj.repo_namespace is None)

    # search_results = None
    # Call the Search method, and expect Bad Credentials exception
    # with pytest.raises(
    #     Exception,
    #     match=r'401 {"message": "Bad credentials"'
    # ):
    #     # Call Search, expect BadCredentials Exception
    #     search_results = GitHubReportObj.search_open_pulls(
    #         repo_namespace="TheCloudMage"
    #     )

    # Call the Search method, and expect Bad Credentials exception
    search_results = GitHubReportObj.search_open_pulls(
        repo_namespace="TheCloudMage"
    )

    assert(GitHubReportObj.repo_namespace == "TheCloudMage")
    assert(search_results is None)

    # Call the method
    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "EXCEPTION occurred in" in err
    assert "401 {\"message\": \"Bad credentials\"" in err


######################################
# Test Github Object Exception:      #
######################################
def test_search_open_pulls_github_except(capsys):
    """ GithubReports Class 'test_search_open_pulls' Method Test

    This test will test the 'test_search_open_pulls' method. The method
    is designed to run a search against Github for number of open PRs
    across a given organization or user account.

    This test will attempt to call the search_open_pulls() method
    with the AuthToken set to a forced bad value. Instantiation of
    the PyGithub Object should result in an Exception Condition.

    Expected Result:
        Github Object Instantiation should cause Exception.
    """
    # Instantiate a GithubReports object, and test for expected test values.
    GitHubReportObj = GithubReports(
        verbose=True,
        auth_token="12345678910987654321"
    )

    # Force set a bad Auth Token Value
    GitHubReportObj._auth_token = 42
    GitHubReportObj._repo_namespace = "TheCloudMage"
    # Ensure auth_token is set to a bad value
    assert(GitHubReportObj.auth_token == 42)
    assert(GitHubReportObj.repo_namespace == "TheCloudMage")

    # Attempt to call the search method
    search_results = None
    search_results = GitHubReportObj.search_open_pulls()

    # Call the method
    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    # Call the Search method, and expect Bad Credentials exception
    assert "An un-expected error occurred when attempting" in err
    assert "EXCEPTION occurred in" in err
    assert(search_results is None)


########################################
# Test Github Pull Request Valid Test: #
########################################
def test_search_open_pulls(capsys):
    """ GithubReports Class 'test_search_open_pulls' Method Test

    This test will test the 'test_search_open_pulls' method. The method
    is designed to run a search against Github for number of open PRs
    across a given organization or user account.

    This test will grab a valid token from an env export
    (export GITHUB_TOKEN=<Token>) and use the token to make
    a valid open pull request query from Github.

    Expected Result:
        Github Object should be properly returned.
    """
    # Instantiate a GithubReports object, and test for expected test values.
    GitHubReportObj = GithubReports(
        verbose=True,
        auth_token=os.environ['GITHUB_TOKEN']
    )

    # Attempt to call the search method
    assert(not GitHubReportObj.is_organization)
    assert(GitHubReportObj._search_results is None)
    assert(GitHubReportObj._repo_namespace is None)
    assert(GitHubReportObj.auth_token == os.environ['GITHUB_TOKEN'])

    GitHubReportObj.notify = True
    search_results = GitHubReportObj.search_open_pulls(
        repo_namespace="rnason"
    )
    assert(GitHubReportObj._notify)
    GitHubReportObj.notify = False
    assert(not GitHubReportObj._notify)

    GitHubReportObj.is_organization = True
    search_results = GitHubReportObj.search_open_pulls(
        repo_namespace="CFWiP"
    )
    assert(GitHubReportObj._is_organization)
    assert(GitHubReportObj._repo_namespace == "CFWiP")
    assert(not bool(GitHubReportObj._search_results))
    assert(search_results is None)

    # Call the method
    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    # Call the Search method, and expect Bad Credentials exception
    assert "0 results returned, exiting search function..." in out

    # Now that 0 results have been tested, poll an organization with
    # an Open PR
    search_results = GitHubReportObj.search_open_pulls(
        repo_namespace="CloudMages"
    )
    assert(GitHubReportObj._is_organization)
    assert(GitHubReportObj._repo_namespace == "CloudMages")
    assert(bool(GitHubReportObj._search_results))
    assert(search_results is not None)

    # Call the method
    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    # Call the Search method, and expect Bad Credentials exception
    assert(
        "of the returned search results were verified "
        "as open pull requests" in out
    )
