##############################################################################
# CloudMage : Git Config Parser Class
#=============================================================================
# CloudMage Git Config Object Utility/Library
#   - Search a provided directory path location for a .git/config directory.
#   - If config found, extract the repository URL, and git provider and return 
# Author: Richard Nason rnason@cloudmage.io
# Project Start: 2/12/2020
# License: GNU GPLv3
##############################################################################

###############
# Imports:    #
###############

# Import Base Python Modules
import os, sys, inspect


#####################
# Class Definition: #
#####################
class GitConfigParser(object):
    """CloudMage Git Config Parser Class
    This class is designed to search a provided file path location for a .git/config directory/file. If found, 
    the config file will be parsed, and attempt to extract the repository URL, and the git provider.
    If those properties are properly extracted, then the respective class properties are set, and the object is returned.

        Methods:

            Publish properly formatted Exception to log method.
            __________________________________________________________________________
            self._exception_handler(
                caller_function  (str) required,
                exception_object (obj) required
            )


            Publish properly formatted log_msg to class log object or stdout, stderr.
            __________________________________________________________________________
            self.log(
                log_msg  (str) required,
                log_type (str) required,
                log_id   (str) required
            )


            Enable | Disable verbose mode.
            __________________________________________________________________________
            Getter (bool) : verbose_setting = Obj.verbose
            Setter (bool) : Obj.verbose = True
            
            self.verbose(
                verbose (bool) optional [default=False]
            )


            Parse git_config_path/.git/config file and return/update repo URL string.
            __________________________________________________________________________
            Getter (str) : git_url = Obj.url
            Setter (str) : Obj.url = "/path/to/project/directory"
            
            url(
                git_config_path (str) required=setter_only
            )


            Parse repository_url and return/update repo platform provider.
            __________________________________________________________________________
            Getter (str) : git_provider = Obj.provider
            Setter (str) : Obj.provider = "https://github.com/namespace/repository.git"

            provider(
                repository_url (str) required=setter_only
            )
    """


    def __init__(self, path, verbose=False, log=None):
        """GitConfigParser Class Constructor

        Parameters:
            path    (str):  required
            verbose (bool): optional [default=False]
            log     (obj):  optional [default=None]
        
        Attributes:
            _path        (str)  : private
            _verbose     (bool) : private
            _log         (obj)  : private
            _log_context (str)  : private
            _url         (str)  : private
            _provider    (str)  : private
        
            url          (str)  : public
            provider     (str)  : public
            user:        (str)  : public
        """

        ##### Class Private Attributes #####
        self._path = path
        self._verbose = verbose
        self._log = log
        self._log_context = "CLS->GitConfigParser"

        ##### Class Public Attributes #####
        self.user = None

        ##### Class Private Properties #####        
        self._url = None
        self._provider = None

        ##### Class Public Properties #####
        # Execute Property Setters
        self.url = self._path
        self.provider = self._url


    ############################################
    # Class Exception Handler:                 #
    ############################################
    def _exception_handler(self, caller_function, exception_object):
        """Class Exception Handler
        
        Handle any exceptions that arise in a universal format for easy debuging purposes
        
        Parameters:
            caller_function  (str):  required
            exception_object (obj):  required

        Returns:
            Publish properly formatted exception to log object or stdout, stderr
        """
        parse_exc_msg = "An EXCEPTION has occurred in '{}.{}', on line {}: -> {}".format(
                self._log_context,
                caller_function,
                sys.exc_info()[2].tb_lineno,
                str(exception_object)
            )
        self.log(parse_exc_msg, 'error', caller_function)


    ############################################
    # Class Logger:                            #
    ############################################
    def log(self, log_msg, log_type, log_id):
        """Class Log Handler

        Provides the logging for this class. If the class caller instantiates the object with the verbose setting set to true, then the class 
        will log to stdout/stderr or to a provided log object if one was passed during object instantiation.
        
        Parameters:
            log_msg  (str):  required
            log_type (str):  required
            log_id   (str):  required

        Returns:
            Log Stream
        """
        # Define this methods identity for functional logging:
        self.__id = inspect.stack()[0][3]
        try:
            # Internal method variable assignments:
            log_msg_caller = "{}.{}".format(self._log_context, log_id)
            # Set the log message offset based on the message type: [debug=3, info=4, warning=1, error=3]
            log_msg_offset = 3
            log_msg_offset = 4 if log_type.lower() == 'info' else log_msg_offset
            log_msg_offset = 1 if log_type.lower() == 'warning' else log_msg_offset

            # If a valid log object was passed into the class constructor, publish the log to the log object:
            if self._log is not None:
                # Set the log message prefix
                log_message = "{}:   {}".format(log_msg_caller, log_msg)
                if log_type.lower() == 'error':
                    self._log.error(log_message)
                elif log_type.lower() == 'warning':
                    self._log.warning(log_message)
                elif log_type.lower() == 'info':
                    self._log.info(log_message)
                else:
                    self._log.debug(log_message)
            # If no valid log object was passed into the class constructor, write the message to stdout, stderr:
            else:
                log_message = "{}{}{}:   {}".format(log_type.upper(), " " * log_msg_offset, log_msg_caller, log_msg)
                if log_type.lower() == 'error':
                    if self._verbose:
                        print(log_message, file=sys.stderr)
                else:
                    if self._verbose:
                        print(log_message, file=sys.stdout)
        except Exception as e:
            self._exception_handler(self.__id, e)


    ################################################
    # Verbose Setter / Getter Methods:             #
    ################################################
    @property
    def verbose(self):
        """Getter method for the verbose property. This method will return the verbose setting."""
        # Define this methods identity for functional logging:
        self.__id = inspect.stack()[0][3]
        self.log("{} property requested.".format(self.__id), 'info', self.__id)
        return self._verbose


    @verbose.setter
    def verbose(self, verbose):
        """Setter method for the verbose property. This method will set the verbose setting if a valid bool value is provided."""
        # Define this methods identity for functional logging:
        self.__id = inspect.stack()[0][3]
        self.log("{} property update requested.", 'info', self.__id)
        try:
            if verbose is not None and isinstance(verbose, bool):
                self._verbose = verbose
                self.log("Updated {} property with value: {}".format(self._url, self._verbose), 'info', self.__id)
            else:
                self.log("Property {} verbose argument expected bool but received type: {}. Aborting update!".format(self._url, type(verbose)), 'error', self.__id)
        except Exception as e:
            self._exception_handler(self.__id, e)


    ################################################
    # Search Directory Path and Search for Git URL #
    ################################################
    @property
    def url(self):
        """Getter method for the url property. This property will return the repository URL if a value was set by the property setter method."""
        # Define this methods identity for functional logging:
        self.__id = inspect.stack()[0][3]
        self.log("{} property requested.".format(self.__id), 'info', self.__id)
        try:
            if self._url is not None:
                self.log("Return: {}".format(self._url), 'debug', self.__id)
                return self._url
            else:
                self.log("Return: {} has no value assigned!".format(self.__id), 'warning', self.__id)
                return "{} property has no value assigned!".format(self.__id)
        except Exception as e:
            self._exception_handler(self.__id, e)


    @url.setter
    def url(self, config_path):
        """Setter method for the object url property. This property will search the provided path and attempt to extact the a git repository URL if a .git/config file can be found in the provided path."""
        # Define this methods identity for functional logging:
        self.__id = inspect.stack()[0][3]
        self.log("{} property update requested.", 'info', self.__id)
        try:
            # Ensure that a valid value was passed.
            if config_path is not None and isinstance(config_path, str):
                # Search for a .git directory in the provided search path, and if found parse to get the repository URL.
                git_config_path = os.path.join(config_path, '.git/config')
                self.log("Searching for git config in path: {}".format(git_config_path), 'debug', self.__id)
                # If the provided path exists, then attempt to extract the url from the .git/config file.
                if os.path.exists(git_config_path):
                    self.log(".git/config file found in search path. Searching for repository url...", 'debug', self.__id)
                    try:
                        with open(git_config_path) as f:
                            for count, line in enumerate(f):
                                # For each line in the config, if url is found in the line, then attempt to parse it.
                                if 'url' in line:
                                    self.log("'URL' string match found in .git/config line: {}".format(line), 'debug', self.__id)
                                    k, v = line.partition("=")[::2]
                                    git_config_url = v.strip()
                                    self.log("Parsing 'URL' string match: {}".format(git_config_url), 'debug', self.__id)
                                    # If the found URL string starts and ends with proper criteria, assign the value and break.
                                    if git_config_url.startswith(('http', 'https', 'git', 'ssh')) and git_config_url.endswith('.git'):
                                        self._url = git_config_url
                                        self.log("'URL' string match verified... Updating url property with value: {}".format(self._url), 'info', self.__id)
                                        break
                                    else:
                                        self.log("'URL' match failed format verification on match string: {}".format(git_config_url), 'warning', self.__id)
                                        continue
                                else:
                                    self.log("'URL' match not found in line: {}".format(line), 'debug', self.__id)
                    except Exception as e:
                        self._exception_handler(self.__id, e)
                else:
                    self.log("Provided directory path does not exist. Aborting property update!", 'error', self.__id)
            else:
                self.log("Valid {} path argument expected string but received type: {}".format(self.__id, type(config_path)), 'error', self.__id)
        except Exception as e:
            self._exception_handler(self.__id, e)


    ################################################
    # Search URL String for Git Provider:          #
    ################################################
    @property
    def provider(self):
        """Getter method for the provider property. This property will return the repository platform provider if a value can be determined and set by the property setter method."""
        # Define this methods identity for functional logging:
        self.__id = inspect.stack()[0][3]
        self.log("{} property requested.".format(self.__id), 'info', self.__id)
        try:
            if self._provider is not None:
                self.log("Return: {}".format(self._provider), 'debug', self.__id)
                return self._provider
            else:
                self.log("Return: {} has no value assigned!".format(self.__id), 'warning', self.__id)
                return "{} property has no value assigned!".format(self.__id)
        except Exception as e:
            self._exception_handler(self.__id, e)


    @provider.setter
    def provider(self, repository_url):
        """Setter method for the object provider property. This property will search the provided url and attempt to extact the a git repository provider, such as github, gitlab, or bitbucket."""
        # Define this methods identity for functional logging:
        self.__id = inspect.stack()[0][3]
        self.log("{} property update requested.", 'info', self.__id)
        try:
            if repository_url is not None and isinstance(repository_url, str):
                self.log("Searching for git provider in URL: {}".format(repository_url), 'debug', self.__id)
                # Parse the provided repository url and attempt to extract the provider.
                if repository_url.startswith(('http', 'https', 'git', 'ssh')) and repository_url.endswith('.git'):
                    provider_git_url = repository_url.strip().split("/")
                    self.log("URL format validated, splitting into search list: {}".format(provider_git_url), 'debug', self.__id)
                    if len(provider_git_url) == 2:
                        provider_string = provider_git_url[-2].split(":")[0].split("@")[1]
                    elif len(provider_git_url) > 3:
                        provider_string = provider_git_url[-3]
                    else:
                        provider_string = None

                    # Validate the provider string is an expected value if one was parsed.
                    if provider_string is not None and ('github' in provider_string or 'gitlab' in provider_string or 'bitbucket' in provider_string):
                        # If a user@provider.tld is set, then parse the user designation and set the class user attribute.
                        if '@' in provider_string:
                            self.user = provider_string.split('@')[0]
                            self.log("User detected in provider string, updating user attribute: {}".format(self.user), 'debug', self.__id)
                            provider_string = provider_string.split('@')[1]
                        else:
                            self.user = "No user found in URL string."
                            self.log("No User detected in provider string, updating user attribute: {}".format(self.user), 'debug', self.__id)
                        # Now the provider string should be the target provider, set the internal class attribute.
                        self._provider = provider_string
                        self.log("Provider match {} found!".format(self._provider), 'debug', self.__id)
                    else:
                        self.log("Parsed provider value: {} not found or invalid. Aborting provider search!".format(provider_string), 'error', self.__id)
                else:
                    self.log("URL {} not properly formatted, aborting provider search...".format(repository_url), 'error', self.__id)
            else:
                self.log("Valid {} repository url argument expected string but received type: {}".format(self.__id, type(repository_url)), 'error', self.__id)
        except Exception as e:
            self._exception_handler(self.__id, e)
