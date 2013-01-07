"""
(C) Copyright 2011, 10gen

Unless instructed by 10gen, do not modify default settings.

When upgrading your agent, you must also upgrade your settings.py file.
"""

#
# Seconds between Mongo status checks. Please do not change this.
#
collection_interval = 56

#
# Seconds between cloud configuration checks. Please do not change this.
#
conf_interval = 120

#
# Seconds between log data collection (if enabled in UI). Please do not change this.
#
log_interval = 5

#
# The mms server
#
mms_server = "https://mms.10gen.com"

#
# The mms ping url
#
ping_url = mms_server + "/ping/v1/%s"

#
# The mms config url
#
config_url = mms_server + "/conf/v3/%(key)s?am=true&ah=%(hostname)s&sk=%(sessionKey)s&av=%(agentVersion)s&sv=%(srcVersion)s"

#
# The mms agent version url
#
version_url = mms_server + "/agent/v2/version/%(key)s"

#
# The mms agent upgrade url
#
upgrade_url = mms_server + "/agent/v2/upgrade/%(key)s"

#
# The mms agent log path.
#
logging_url = mms_server + "/agentlog/v2/catch/%(key)s"

#
# The operation failure log path.
#
operationFailureUrl = mms_server + "/agentlog/v2/qcmdf/%s"

#
# Enter your API key  - See: https://mms.10gen.com/settings
#
mms_key = "4fc4b0e42f64555cbd333a8b3043ea55"

secret_key = "471991721b7302bf8f6270e1571cf10d"

src_version = "9c667c1155e3fda1e91dbf354b7a040f9f2e40ae"

#
# Enabled by default
#
autoUpdateEnabled = True

#
# The global authentication credentials to be used by the agent.
#
# The user must be created on the "admin" database.
#
# If the global username/password is set then all hosts monitored by the
# agent *must* use the same username password.
#
# Example usage:
#
# globalAuthUsername="""yourAdminUser"""
# globalAuthPassword="""yourAdminPassword"""
#
#
# If you do not use this, the values must be set to None.
#
# Please use """ quotes to ensure everything is escaped properly.
#
# E.g.,
#
# globalAuthPassword="""yourAdminPasswordWith"DoubleQuotes"""
#
# globalAuthPassword="""yourAdminPasswordWith'SingleQuote"""
#
# For more information about MongoDB authentication, see:
#
# http://www.mongodb.org/display/DOCS/Security+and+Authentication
#
#

globalAuthUsername = None

globalAuthPassword = None

#
# Some config db collection properties
#
configCollectionsEnabled = True
configDatabasesEnabled = True

#
# Ability to disable getLogs and profile data collection in the agent. This overrides
# the server configuration. Set these fields to True if you can NEVER allow profile or log data
# to be relayed to the central MMS servers.
#
disableProfileDataCollection = False
disableGetLogsDataCollection = False

#
# Set to a specific bind address or 0.0.0.0 for all interfaces. Set to None to disable.
#
shutdownAgentBindAddr = None

#
# You must change the shutdown port if you run multiple agents on a machine.
#
shutdownAgentBindPort = 23017

#
# The shutdown agent bind challenge. You can change this to whatever you like. When
# you send a shutdown message to the agent, this must be the message sent.
#
shutdownAgentBindChallenge = '23237NYouCanChangeThis'

settingsAgentVersion = "1.5.2"

#
# You must be running a mongod process with built in SSL support.
#
useSslForAllConnections = False

# Set to False if you have no plans to use munin (saves one thread per server)
enableMunin = True

# Misc - Please do not change this.
socket_timeout = 40

