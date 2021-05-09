#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from smtplib import SMTP, SMTPException
from subprocess import PIPE, run
from time import sleep
from config import (SEND_FREQ, SEND_FROM, SEND_SCAN_REPORTS, SEND_TO,
                    SMTP_HOST, SMTP_PORT)

try:
    with open('/root/.cobpwd', 'r') as f:
        SEND_PWD = f.read()


except FileNotFoundError:
    print('No password file found. Exiting.')
    exit()


def main() -> None:
    try:
        server = SMTP(SMTP_HOST, SMTP_PORT)
        server.ehlo()
        server.starttls()
        server.login(SEND_FROM, SEND_PWD)

    except SMTPException:
        print(f'Could not connect to mail server. Retry in {SEND_FREQ.pprint()}', flush=True)
        return

    date = datetime.now()
    delta = (date - timedelta(seconds=int(SEND_FREQ))).isoformat(' ', 'seconds')
    report = run(['journalctl', '-u', 'cobra-sentinel.service', '--no-pager', '--since', delta],
                 check=True, stdout=PIPE).stdout
    report = '<br></br>'.join(i for i in str(report)[2:-3].split('\\n'))
    for user in SEND_TO:
        msg = f'''From: {SEND_FROM}
To: {user}
Subject: CobraAV report on {date.date()}
Content-Type: text/html; charset=UTF-8

<html>
  <body>
    {report}
  </body>
</html>
'''
        server.sendmail(SEND_FROM, user, msg)


if __name__ == '__main__':
    if SEND_SCAN_REPORTS:
        main()
    else:
        print('Scan reports disabled. Exiting.')
        exit()
    print(f'Sleeping {SEND_FREQ.pprint()}', flush=True)
    try:
        sleep(int(SEND_FREQ))
    except KeyboardInterrupt:
        print('Shutting down')
