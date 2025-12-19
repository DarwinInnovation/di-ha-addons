# Darwin Innovation Home Assistant Add-ons

A curated collection of Home Assistant Supervisor add-ons published and maintained by
Darwin Innovation. Each add-on contains Supervisor metadata, documentation, and
docker build recipes so you can install them directly from this repository.

[![Add repository to Home Assistant](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FDarwinInnovation%2Fdi-ha-addons)

## Add-ons

### SwitchBot MQTT Proxy

- **Path:** `switchbot-mqtt-proxy`
- **Description:** Polls the SwitchBot Cloud API, publishes all sensor readings to MQTT,
  and auto-discovers those sensors inside Home Assistant.
- **Requirements:** your SwitchBot API `token` and `secret`, plus a broker exposed to
  the Supervisor MQTT service or overridden via the optional `mqtt` configuration block.
- **Documentation:** see [`switchbot-mqtt-proxy/DOCS.md`](switchbot-mqtt-proxy/DOCS.md) for usage, options,
  and MQTT override instructions.

## Installing from this repository

1. In Home Assistant Supervisor, go to **Add-on Store** > **Repositories** and add
   `https://github.com/DarwinInnovation/di-ha-addons`.
2. Install the desired add-on (for example, the SwitchBot MQTT Proxy) and configure
   the provided options.
3. Start the add-on; the log output and MQTT telemetry are visible inside the Supervisor UI.

## Development notes

- Each add-on publishes a `build.yaml` so GitHub Actions can build container images
  for the architectures listed in `config.yaml`.
- Keep the `version` key in sync with releases and update the corresponding `CHANGELOG.md` entry
  before merging to the `main` branch.
- Document any configuration overrides (like MQTT host) so edge-case deployments know how to target
  alternative services.

## Support

Report issues or feature requests via [the GitHub issues page](https://github.com/DarwinInnovation/di-ha-addons/issues).# Example Home Assistant add-on repository

This repository can be used as a "blueprint" for add-on development to help you get started.

Add-on documentation: <https://developers.home-assistant.io/docs/add-ons>

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fhome-assistant%2Faddons-example)

## Add-ons

This repository contains the following add-ons

### [Example add-on](./example)

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]
![Supports armhf Architecture][armhf-shield]
![Supports armv7 Architecture][armv7-shield]
![Supports i386 Architecture][i386-shield]

_Example add-on to use as a blueprint for new add-ons._

<!--

Notes to developers after forking or using the github template feature:
- While developing comment out the 'image' key from 'example/config.yaml' to make the supervisor build the addon
  - Remember to put this back when pushing up your changes.
- When you merge to the 'main' branch of your repository a new build will be triggered.
  - Make sure you adjust the 'version' key in 'example/config.yaml' when you do that.
  - Make sure you update 'example/CHANGELOG.md' when you do that.
  - The first time this runs you might need to adjust the image configuration on github container registry to make it public
  - You may also need to adjust the github Actions configuration (Settings > Actions > General > Workflow > Read & Write)
- Adjust the 'image' key in 'example/config.yaml' so it points to your username instead of 'home-assistant'.
  - This is where the build images will be published to.
- Rename the example directory.
  - The 'slug' key in 'example/config.yaml' should match the directory name.
- Adjust all keys/url's that points to 'home-assistant' to now point to your user/fork.
- Share your repository on the forums https://community.home-assistant.io/c/projects/9
- Do awesome stuff!
 -->

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg
