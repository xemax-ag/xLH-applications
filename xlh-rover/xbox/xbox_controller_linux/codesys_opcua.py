import time
from xbox import Xbox
from opcua import Client, ua
import time


class CodesysOpcUa:
    def __init__(self, ip_plc='192.168.1.41', port=4840, xbox: Xbox = None):
        self.ip_plc = ip_plc
        self.port_plc = port
        self.xbox = xbox

        self._abDataToCodesys = [False for i in range(14)]
        self._abDataFromCodesys = [False for i in range(2)]
        self._arDataToCodesys = [0.0 for i in range(10)]
        self._arDataFromCodesys = [0.0 for i in range(10)]

        self._opcua_client = None
        self._abDataToCodesys_node = None
        self._abDataFromCodesys_node = None
        self._arDataToCodesys_node = None
        # self._arDataFromCodesys_node = None

        self._node_root_base = None
        self._counter = 0.0
        self._start_time = time.perf_counter()

    def connect(self):
        self._opcua_client = Client(f'opc.tcp://{self.ip_plc}:{self.port_plc}')
        self._opcua_client.connect()
        root = self._opcua_client.get_root_node()
        plc_name = "4:CODESYS Control for Raspberry Pi 64 SL"
        node_root_base = ['0:Objects', '2:DeviceSet', plc_name,
                          '3:Resources', '4:app', '3:Programs', '4:io', '4:xbox']

        self._abDataToCodesys_node = root.get_child(node_root_base + ['4:abDataFromXbox'])
        self._abDataFromCodesys_node = root.get_child(node_root_base + ['4:abDataToXbox'])
        self._arDataToCodesys_node = root.get_child(node_root_base + ['4:arDataFromXbox'])

    def disconnect(self):
        self._opcua_client.disconnect()

    def reconnect(self):
        try:
            self.disconnect()
        except Exception as e:
            print(e)
            print('error disconnect')
            pass

        time.sleep(1.0)

        try:
            self.connect()
        except Exception as e:
            # print(e)
            # print('error reconnect')
            pass

    def read_write(self):
        try:
            if self._opcua_client is None:
                self.connect()

            self._abDataToCodesys[0] = bool(self.xbox.bBtnA)
            self._abDataToCodesys[1] = bool(self.xbox.bBtnB)
            self._abDataToCodesys[2] = bool(self.xbox.bBtnX)
            self._abDataToCodesys[3] = bool(self.xbox.bBtnY)
            self._abDataToCodesys[4] = bool(self.xbox.bBtnBack)
            self._abDataToCodesys[5] = bool(self.xbox.bBtnStart)
            self._abDataToCodesys[6] = bool(self.xbox.bBtnThumbLeft)
            self._abDataToCodesys[7] = bool(self.xbox.bBtnThumbRight)
            self._abDataToCodesys[8] = bool(self.xbox.bBtnTriggerLeft)
            self._abDataToCodesys[9] = bool(self.xbox.bBtnTriggerRight)
            self._abDataToCodesys[10] = bool(self.xbox.bBtnDpadLeft)
            self._abDataToCodesys[11] = bool(self.xbox.bBtnDpadRight)
            self._abDataToCodesys[12] = bool(self.xbox.bBtnDpadUp)
            self._abDataToCodesys[13] = bool(self.xbox.bBtnDpadDown)

            self._arDataToCodesys[0] = float(self.xbox.rAxLeftX)
            self._arDataToCodesys[1] = float(self.xbox.rAxLeftY) * (-1.0)
            self._arDataToCodesys[2] = float(self.xbox.rAxRightX)
            self._arDataToCodesys[3] = float(self.xbox.rAxRightY) * (-1.0)
            self._arDataToCodesys[4] = float(self.xbox.rTriggerLeft)
            self._arDataToCodesys[5] = float(self.xbox.rTriggerRight)
            perf_counter = time.perf_counter()
            cycle_time = perf_counter - self._start_time
            self._start_time = perf_counter
            self._counter += 0.1
            self._arDataToCodesys[8] = float(cycle_time * 1000.0)
            self._arDataToCodesys[9] = float(self._counter)
            self._start_time = time.perf_counter()

            self._abDataToCodesys_node.set_value(ua.Variant(self._abDataToCodesys, ua.VariantType.Boolean))
            self._arDataToCodesys_node.set_value(ua.Variant(self._arDataToCodesys, ua.VariantType.Double))
            self._abDataFromCodesys = self._abDataFromCodesys_node.get_value()

            if self._abDataFromCodesys[0]:
                self.xbox.rumble()
            # print(self._abDataFromCodesys)
        except Exception as e:
            print(e)
            print('exception read_write')
            self.reconnect()

    def update(self, print_cli=False):
        self.read_write()


if __name__ == '__main__':
    _xbox = Xbox()
    _plc_opcua = CodesysOpcUa(ip_plc='127.0.0.1', port=4840, xbox=_xbox)
    # _plc_opcua = CodesysOpcUa(ip_plc='192.168.1.41', port=4840, xbox=_xbox)

    ctr = 0
    while ctr < 5 or False:
        ctr += 1
        _plc_opcua.update()

    _plc_opcua.disconnect()

