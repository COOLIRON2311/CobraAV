from libunits import *

CHECK_FOR_UPDATES = 0  # Check for updates
UPDATE_FREQ = Days(1)  # Check interval
MAX_FILE_SIZE = MBytes(8)  # Max file size

# Antivirus database sources
AV_SOURCES = [
    r'https://bitbucket.org/Urdeney/cobraav-signatures/raw/60470e54b1a44d94fda4726538cae18b1a3a7bed/main.crb',
    r'https://bitbucket.org/Urdeney/cobraav-signatures/raw/60470e54b1a44d94fda4726538cae18b1a3a7bed/main.fp',
    r'https://bitbucket.org/Urdeney/cobraav-signatures/raw/60470e54b1a44d94fda4726538cae18b1a3a7bed/main.hdb',
    r'https://bitbucket.org/Urdeney/cobraav-signatures/raw/60470e54b1a44d94fda4726538cae18b1a3a7bed/main.hsb',
    r'https://bitbucket.org/Urdeney/cobraav-signatures/raw/60470e54b1a44d94fda4726538cae18b1a3a7bed/main.info',
    r'https://bitbucket.org/Urdeney/cobraav-signatures/raw/60470e54b1a44d94fda4726538cae18b1a3a7bed/main.msb',
    r'https://bitbucket.org/Urdeney/cobraav-signatures/raw/60470e54b1a44d94fda4726538cae18b1a3a7bed/main.ndb',
    r'https://bitbucket.org/Urdeney/cobraav-signatures/raw/60470e54b1a44d94fda4726538cae18b1a3a7bed/main.sfp'
    ]

# Antivirus database path
DB_PATH = r'/opt/cobraav/signatures'

# On threat:
# 0 - quarantine
# 1 - remove
REMOVE_THREATS = 1

# Directories to scan
SCAN_TARGETS = [r'/home']

# Exclude from scanning
SCAN_EXCLUDE = []

# quarantine location
QUARANTINE_PATH = r'/opt/cobraav/quarantine'

# Send scan reports
SEND_SCAN_REPORTS = 0

# Scan reports frequency
SEND_FREQ = Weeks(1)

# Send from this email
SEND_FROM = r'example@yahoo.com'

# Send to these emails
SEND_TO = [r'example@yahoo.com']

# SMTP settings (preset for gmail)
SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 587

# GUI Language
LANG = 'en'
