from pydantic_ai import Agent, RunContext
from deps import Deps
from opcua import Client, ua

def set_oven_temperature(ctx: RunContext[Deps], temperature: float) -> bool:
    """
    :param temperature: Einstellung der Backofentemperatur in Grad Celsius.
    Die Temperatur muss zwischen 100 und 250 Grad liegen.
    Die Rückgabe ist True, falls der Backofen die gewünschte Temperatur einstellen kann.
    """
    print(f'=> tool_set_oven_temperature {temperature}')
    set_oven_temperature_opcua(temperature=temperature)
    return True if temperature >= 100 and temperature <= 250 else False

def set_oven_temperature_opcua(temperature: float):
    ip_plc = '192.168.1.151'
    port_plc = 4840
    opcua_client = Client(f'opc.tcp://{ip_plc}:{port_plc}')
    try:
        opcua_client.connect()
        root = opcua_client.get_root_node()
        plc_name = "4:CODESYS Control for Raspberry Pi 64 SL"
        node_root_base = ['0:Objects', '2:DeviceSet', plc_name,
                          '3:Resources', '4:app', '3:Programs', '4:MAIN']
        fOvenTemperatureSetpointNode = root.get_child(node_root_base + ['4:fOvenTemperatureSetpoint'])
        fOvenTemperatureNode = root.get_child(node_root_base + ['4:fOvenTemperature'])
        bOvenNode = root.get_child(node_root_base + ['4:bOven'])

        fOvenTemperatureSetpointNode.set_value(ua.DataValue(ua.Variant((temperature), ua.VariantType.Double)))

        # print(fOvenTemperatureNode.get_value())
        # print(bOvenNode.get_value())
        # bOvenNode.set_value(ua.DataValue(ua.Variant((True), ua.VariantType.Boolean)))

    except Exception as exc:
        print(f'Error: {exc}')
    finally:
        opcua_client.disconnect()

if __name__ == '__main__':
    from pydantic_ai import Agent
    from pydantic_ai.models.test import TestModel
    from rich import print

    model = TestModel()
    deps: Deps = Deps()
    agent = Agent(
        model=model,
        deps_type=str,
        tools=[set_oven_temperature],
    )
    # result = agent.run_sync(user_prompt='hallo', model=model, deps=deps)
    # for function_tool in model.last_model_request_parameters.function_tools:
    #     print(f'===> {function_tool.name}')
    #     print(function_tool.parameters_json_schema)

    set_oven_temperature_opcua(temperature=315)
