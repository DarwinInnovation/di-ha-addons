# SwitchBot Cloud to MQTT Proxy Add-on

Publishes SwitchBot sensor readings into MQTT and auto-discovers them inside
Home Assistant. The add-on requires your SwitchBot API `token` and `secret`, plus
an MQTT broker that Home Assistant registers for you.

If you want to target a broker that Home Assistant does not manage, fill the
optional `mqtt.host`, `mqtt.username`, and `mqtt.password` options instead of
depending on the service. The start script prioritizes those overrides and will
exit with an error if it cannot find any MQTT host from either source.
