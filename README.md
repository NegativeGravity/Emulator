# Emulator
Simple Python script to automate Caldera, Which would:
* Add atomic techniques to your caldera's abilities.
* Emulate Mitter Attack APT groups.

## Usage
You can easily run Emulator by just defining your Caldera server's IP and the API session, By which you could authenticate in Caldera, like the `config.yaml`.

`python3 Emulator.py <APT ID>`

Example:

`python3 Emulator.py G0006`

You can find APT ID from Mitter Attack, which is the ID that Mitter assigns to APT groups.

Example:

`APT1 -> G0006`
