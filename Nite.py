import subprocess
from os import path, getenv, chdir
from ast import literal_eval
from configparser import ConfigParser
from urllib import request
from glob import glob
from sys import argv

chdir(path.dirname(__file__))
USERPROFILE = getenv('USERPROFILE')
APPDATA = getenv('APPDATA')

Repository = 'https://raw.githubusercontent.com/Aetopia/Nite'
if path.exists('Options.ini') is False:
	request.urlretrieve(f'{Repository}/main/Options.ini', 'Options.ini')
Options = ConfigParser()
Options.read('Options.ini')

if len(argv) >= 3:
	Version = argv[1]
	Server = f'--server {argv[2]}'
elif len(argv) >= 2:
	Version = argv[1]	
	Server = ''
elif len(argv) == 1:
	exit(1)	

Directory = Options['Directories'][Version]
Arguments = Options['Java']['Arguments']
JRE = Options['Java']['JRE']
Cosmetics = literal_eval(Options['Lunar Client']['Cosmetics'])
Assets = literal_eval(Options['Nite']['Assets'])
Verbose = literal_eval(Options['Nite']['Verbose'])

if Version == "1.7":
    AssetIndex="1.7.10"
else:
    AssetIndex=Version

if Directory.lower() == 'default':
	Directory = f'{APPDATA}/.minecraft'

if JRE.lower() == 'lunar':
	JRE = glob(f'{USERPROFILE}/.lunarclient/jre\{Version}/*zulu*/bin/javaw.exe')[0]

if Cosmetics is True:
    Cosmetics = f'{USERPROFILE}/lunarclient/textures'
else:
    Cosmetics = ""

if Assets is True:
	Assets = f'{APPDATA}/.minecraft/assets'
else:
	Assets = f'{Directory}/assets'		

Libraries = ' '.join((
	'--add-modules jdk.naming.dns --add-exports',
	'jdk.naming.dns/com.sun.jndi.dns=java.naming',
	f'-Djna.boot.library.path="{USERPROFILE}/.lunarclient/offline/{Version}/natives"',
	'-Dlog4j2.formatMsgNoLookups=true',
	'--add-opens java.base/java.io=ALL-UNNAMED'
	))

Jars = ''
for Jar in ('lunar-assets-prod-1-optifine.jar',
			'lunar-assets-prod-2-optifine.jar',
			'lunar-assets-prod-3-optifine.jar',
			'lunar-libs.jar',
			'lunar-prod-optifine.jar',
			path.split(glob(f'{USERPROFILE}/.lunarclient/offline/{Version}/*OptiFine_*')[0])[1], 
			'vpatcher-prod.jar'
			):
	Jars += f'"{USERPROFILE}/.lunarclient/offline/{Version}/{Jar}";'
Jars = Jars[:len(Jars)-1]

Game = ' '.join((
	f'-Djava.library.path="{USERPROFILE}/.lunarclient/offline/{Version}/natives"', 
	"-XX:+DisableAttachMechanism",
	f'-cp {Jars}',
	'com.moonsworth.lunar.patcher.LunarMain',
	f'--version {Version}',
	'--accessToken 0', 
	f'--assetIndex {AssetIndex}',
	'--userProperties {}',
	f'--gameDir "{Directory}"',
	'--width 854 --height 480',
	f'--texturesDir "{Cosmetics}"',
	f'--assetsDir "{Assets}"'
	))

Command = f'{JRE} {Libraries} {Arguments} {Game} {Server}'
if Verbose is True:
	print(f"""---Verbose---
Version: {Version}
Directory: {path.abspath(Directory)}
JRE: {path.abspath(JRE)}
Arguments: {Arguments}
Cosmetics: {Cosmetics == f'{USERPROFILE}/lunarclient/textures'}
Assets Directory: {path.abspath(Assets)}
""")
subprocess.Popen(Command)
exit(0)