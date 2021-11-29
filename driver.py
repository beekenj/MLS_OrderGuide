from modules.Shamrock import get_shamrock
from modules.Shamrock import rename_shamrock
from modules.Sysco import get_sysco
from modules.Sysco import rename_sysco
from modules.PriceFormat import price_sheet_create
from modules.Upload import drive_upload
from modules.Email import send_report

import time

MAXATTEMPTS = 5
attempts = 0


# Error reports
shamrock_report = '''
MLS Price Guide: SHAMROCK DOWNLOAD FAILURE

Shamrock price list download failed after %i attempts.
''' % (MAXATTEMPTS)

sysco_report = '''
MLS Price Guide: SYSCO DOWNLOAD FAILURE

Sysco price list download failed after %i attempts.
''' % (MAXATTEMPTS)


# Attempt to download shamrock price list csv
while not get_shamrock() and attempts < MAXATTEMPTS:
	time.sleep(30)
	attempts+=1
	if attempts == MAXATTEMPTS:
		print("Shamrock MAXATTEMPTS reached")
		# report failure via email
		send_report(shamrock_report)


# Rename shamrock price list for price_sheet_create()
rename_shamrock()

attempts = 0

# Attempt to download sysco price list csv
while not get_sysco() and attempts < MAXATTEMPTS:
	time.sleep(30)
	attempts+=1
	if attempts == MAXATTEMPTS:
		print("Sysco MAXATTEMPTS reached")
		# report failure via email
		send_report(sysco_report)

# Rename sysco price list for price_sheet_create()
rename_sysco()

# Import, join, format, and export
price_sheet_create()

# Send result to google drive
drive_upload()