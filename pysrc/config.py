from libunits import *

CHECK_FOR_UPDATES = 0  # Check for updates
UPDATE_FREQ = Days(1)  # Check interval
MAX_FILE_SIZE = MBytes(8)  # Max file size

# Antivirus database sources
AV_SOURCES = [r'http://database.clamav.net/main.cvd']

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

# Sender email password
SEND_PASSWD = r'12345'

# Send to these emails
SEND_TO = [r'example@yahoo.com']
