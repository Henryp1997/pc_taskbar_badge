# pc_taskbar_badge
Small application to show a widget on top of the Windows 11 taskbar. Currently only designed to work with taskbar position set to centre.

<img src=./assets/screenshot.png>

## Setup
Open `config.yml` in a text editor:
- Set `text` to the desired display text. Set to 'null' to use the PC's hostname
- Set `bg_colour` to the desired background colour of the widget
- Set `fg_colour` to the desired foreground (text) colour of the widget
- Set `border_radius` to the desired border radius of the widget

## Running the widget
The widget is currently only executable via Python. An .exe version will be included in future

## Closing the widget
Close the widget by either:
- Holding `CTRL` and `SHIFT` and left-clicking the widget
- Right clicking the widget and pressing the `Close` option that pops up

