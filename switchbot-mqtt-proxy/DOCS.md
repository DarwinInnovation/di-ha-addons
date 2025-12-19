# SwitchBot Cloud to MQTT Proxy add-on

## How to use

1. Populate the `switchbot.token` and `switchbot.secret` options with the
	credentials you obtain from the SwitchBot developer portal.
2. Configure or install an MQTT broker add-on so that Home Assistant exposes a
	managed MQTT service (the add-on already requests `mqtt: need`).
3. Start this add-on; it polls the SwitchBot Cloud API, publishes sensor data to
	MQTT, and automatically registers Home Assistant sensors for each device.

### Configuration options

| Section | Option | Purpose |
| --- | --- | --- |
| `switchbot` | `token` | SwitchBot API token (required) |
|  | `secret` | SwitchBot API secret (required) |
| `mqtt` | `host` | Optional broker host to override the MQTT service |
|  | `username` | Optional username when overriding the broker |
|  | `password` | Optional password when overriding the broker |

## MQTT host override

The add-on exports `MQTT_HOST`, `MQTT_USER`, and `MQTT_PASSWORD` before
starting `switchbot-mqtt-proxy.py`. When `mqtt.host` is empty, these values are
filled from Home Assistant’s MQTT service (`bashio::services mqtt`). If you need
to target a broker that is not managed by Home Assistant, set `mqtt.host`,
`mqtt.username`, and `mqtt.password` to the desired values. Once the add-on
receives the override, it will use those credentials instead of the service data.

The start script complains and exits if neither the MQTT service nor `mqtt.host`
provide a host, so make sure at least one of them is configured.
