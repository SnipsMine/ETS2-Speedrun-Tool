# ETS2-Speedrun-Tool

This tool uses the telemetry data send by Euro Truck Simulator 2 to create an user interface. This interface contains
sections that allow speedrunners to analyze there runs in Real time. These sections are: A section by section breakdown 
of the run showing the average speed, entrance speed, exit speed and time, a map view showing the current run and the
location of te Truck, when the run contains a ferry the map view is split in sections. All the sections can be executed
as there own screen for import into OBS.

## Installation
In order to run this program you will need to install the sdk-plugin from RenCloud.
[Download Link V1.9.0](https://github.com/RenCloud/scs-sdk-plugin/releases/tag/v.1.9.0), this program currently only 
supports V1.9.0.

To install the sdk-plugin inside Euro Truck Simulator 2. Place the acquired DLL inside bin/win_x64/plugins/ of your 
ETS2/ATS installation. It is possible the plugins directory doesn't exists yet (as with every default installation). 
In that case you need to create the plugins folder. Place the DLL inside the plugins folder.

You will now notice that each time ETS2/ATS now starts it prompts the SDK has been activated. Unfortunately you have to 
press OK to this message every time, but it's a small price to pay for the added features that are possible via the SDK.

Currently this tool only supports version 1.9.0.
