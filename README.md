# cp_certs_query
Check Point - Query IKE and SIC type certificates for expiration date

## Idea
The idea was to define three levels of days to be ahead and run against all certificates to see which ones will expire.
Color coded output helps with quit determination which ones the operator needs to take care of.

## Requirements
None

## Usage
Clone repo or copy the `certs_query.py` to the SMS/MDS.

```
git clone https://github.com/Senas23/cp_cert_query.git
```
Set read/write/exec flags:
```
chmod 0770 certs_query.py
```
On SMS run:
```
$FWDIR/Python/bin/python3 certs_query.py
```
On MDS run:
```
$MDS_FWDIR/Python/bin/python3 certs_query.py
```
Or
```
./certs_query.py
```

## Developement Environment
Python 3.6.9

