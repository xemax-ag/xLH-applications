import time

from codesys_opcua import CodesysOpcUa
from xbox import Xbox

while True:
    try:
        xbox = Xbox()
        plc_opcua = CodesysOpcUa(ip_plc='127.0.0.1', port=4840, xbox=xbox)
        while True:
            xbox.update()
            plc_opcua.update()
            time.sleep(0.010)
    except Exception as e:
        print('CRITICAL ERROR')
        time.sleep(1.0)
