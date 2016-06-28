import ConfigParser
import newt.gstate

config = ConfigParser.RawConfigParser()
config.read('.newt')

newt.gstate.filename = [config.get('input', 'file')]
newt.gstate.outdir = config.get('input', 'outdir')
