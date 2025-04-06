from jproperties import Properties

configs = Properties()
with open('server-client.properties', 'rb') as config_file:
    configs.load(config_file)