import re, subprocess
from datetime import datetime

re_subject = '^Subject\s=\sCN=([^,]+).+?$'
re_status_type = '^Status\s=\s(\w+)\s{3}Kind\s=\s(\w+).+?$'
re_date = '^Not_Before.*Not_After:\s(.+?)$'

days_warning = 60
days_critical = 30
days_emergency = 7

class bcolors:
        HEADER = '\033[95m'
        BLUE = '\033[94m'
        CYAN = '\033[96m'
        GREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

def banner():
  logo = \
    """
    +-+-+-+-+-+-+-+-+-+-+-+-+-+
    |C|e|r|t|V|a|l|i|d|a|t|o|r|
    +-+-+-+-+-+-+-+-+-+-+-+-+-+

    By: The Machine
    """
  print(logo)
  print(f"Color Legend:\n{bcolors.GREEN}{days_warning} - Still good, but start on planning to reset certificate")
  print(f"{bcolors.WARNING}{days_critical} - Still ok, but put in the RFC for certificate renewal")
  print(f"{bcolors.FAIL}{days_emergency} - You risk outage, renew certificate NOW or already too late\n{bcolors.ENDC}")

def main():
  banner()
  certificates = []
  for kind in ['IKE', 'SIC']:
    process = subprocess.Popen(['cpca_client', 'lscert', '-kind', kind], stdout=subprocess.PIPE, universal_newlines=True)
    print(f"{bcolors.HEADER}Printing {kind} type of certificates:{bcolors.ENDC}")
    certificates += read_cert(process)
  print(certificates)

def read_cert(process: subprocess.Popen) -> list:
  gateways = []
  cert = {}
  date_diff = None

  for line in process.stdout.readlines():
    if re.match(re_subject, line):
      match = re.match(re_subject, line).group(1)
      cert['Cert'] = match.replace(" VPN Certificate", "") if " VPN Certificate" in match else match
    elif re.match(re_status_type, line):
      cert['Status'] = re.match(re_status_type, line).group(1)
      cert['Type'] = re.match(re_status_type, line).group(2)
    elif re.match(re_date, line):
      match = re.match(re_date, line).group(1)
      match = match.replace("  ", " 0") if "  " in match else match
      tmp_datetime = datetime.strptime(match, "%a %b %d %H:%M:%S %Y")
      date_diff = tmp_datetime - datetime.now()
      cert['Expiration'] = tmp_datetime.strftime("%m/%d/%Y")
    elif 'Expiration' in cert.keys():
      if cert['Status'] in ['Valid', 'Expired']:
        gateways.append(cert)
        if cert['Status'] == "Expired" or date_diff.days <= days_emergency:
          print(f"{bcolors.FAIL}{cert}")
        elif date_diff.days <= days_critical:
          print(f"{bcolors.WARNING}{cert}")
        elif date_diff.days <= days_warning:
          print(f"{bcolors.GREEN}{cert}")
        else:
          print(f"{bcolors.ENDC}{cert}")
      cert = {}
  return gateways

if __name__ == "__main__":
  main()