import codecs
import sys

from cli import CLI
from config import FileConfig
from main import Main

SIMPLE_DB_MIGRATE_VERSION = '1.3.7'

# fixing print in non-utf8 terminals
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

def run():
    try:
        (options, args) = CLI().parse()

        if options.simple_db_migrate_version:
            msg = 'simple-db-migrate v%s' % SIMPLE_DB_MIGRATE_VERSION
            CLI().info_and_exit(msg)

        if options.show_colors:
            CLI.show_colors()

        # Create config
        config = FileConfig(options.config_file)
        config.put('schema_version', options.schema_version)
        config.put('show_sql', options.show_sql)
        config.put('show_sql_only', options.show_sql_only)
        config.put('new_migration', options.new_migration)
        config.put('drop_db_first', options.drop_db_first)
        config.put('interactive_mode', options.interactive_mode)
        
        log_level = int(options.log_level)
        if options.interactive_mode:
            log_level = 2
        
        config.put('log_level', log_level)

        # If CLI was correctly parsed, execute db-migrate.
        Main(config).execute()
    except Exception, e:
        CLI().error_and_exit(str(e))
        
if __name__ == '__main__':
    run()
