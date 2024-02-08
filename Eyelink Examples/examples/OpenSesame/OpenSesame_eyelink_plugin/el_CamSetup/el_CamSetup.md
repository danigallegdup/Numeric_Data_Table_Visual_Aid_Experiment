# Item: el_CamSetup

This item wraps all the functions a user may need to calibrate the tracker. Using animation calibration target (video) has not yet been implemented. One should put this item at the beginning of each block of trials. The configuration options are explained in the table below.

* <b>Calibration Type</b>

	Select the calibration type, i.e, HV9 for a 9-point calibration. When tracking in remote mode, it is recommended to use HV13, whereas in head-stabilized mode, HV9 gives the best calibration results.
	
* <b>Pacing Interval</b>

	Set the pacing interval for the calibration/validation targets, i.e., after how much time will the next calibration target be presented after the current calibration target has been accepted.

* <b>Randomize Order</b>

	Randomize the order of the calibration/validation targets

* <b>Repeat First Point</b>

	Repeat the first point. This option is enabled by default, helps to improve calibration results.

* <b>Force Manual Accept</b>

	Manually accept fixation duration calibration/validation by pressing SPACEBAR or ENTER. One can switch to automatic mode at any time during calibration/validation by pressing “A” key on the Host or experimental PC keyboard.

* <b>Horiztonal Screen Proportion to Calibrate</b>

	The horizontal proportion of screen to calibrate. This option is useful when the subject display is large and the top corners may be outside the tracking range of the tracker. One can manually specify the calibration/validation target positions, but this is the recommended way of controlling the size of the calibrated screen region.

* <b>Vertical Screen Proportion to Calibrate</b>

	The horizontal proportion of screen to calibrate.

* <b>Calibration Target</b>

	Select which type of calibration target to use. The default is a bull’s eye shaped dot, but one can also use an image or a video as the calibration target.

* <b>Custom Target Image/Video</b>
	Select an image or a video file from the File Pool to use as the calibration target.
