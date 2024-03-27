# Item: el_SendCommand

Send commands to the tracker. If you need to send multiple commands, put each command in a line, for instance,

>sampling_rate 500
>draw_cross 512 384

The various 'draw' commands can be very useful and one can use them to draw simple landmarks on the Host display during recording. These commands (e.g., clear_screen, draw_line, draw_box, draw_text) can be found in the COMMANDS.INI file on the Host PC, under /elcl/exe. One can also send various commands to configure the tracker options, for instance, setting the sampling rate to 500 Hz (see the example above). 