# Item: el_DriftCheck

This item helps to drift-correct the tracker. The EyeLink II and EyeLink I trackers mount the eye camera on the headband and are susceptible to gaze-drifts as the headband may slip during recording. Drift-correction helps to maintain the tracking accuracy. For EyeLink 1000 and newer models, the tracker uses the Pupil-CR tracking method by default. This method is relatively drift-free and there is no need to drift-correct the tracker; by default the drift-correction routine only checks the gaze error without linearly correct the gaze data. The various configuration options of this item are listed in the table below.

* <b>Target X/Y</b>

	The X, Y coordinates of the drift-correction/check target in OpenSesame’s default screen coordinates (i.e., 0,0 correspond to the center of the screen). The drift-correction/check target does not necessarily need to be presented at the center of the screen.

* <b>Allow Re-calibrate if Drift-correction/check Fails</b>

	Allow the user to press ESCAPE to setup the tracker and to re-calibrate.

* <b>Apply Drift-correction</b>

	Force the tracker to drift-correct only when using EyeLInk II/I.

* <b>Drift-correction Target</b>
	
	Use the same target as the calibration routine or use an image instead.
	
* <b>Custom Target Image</b>

	Select an image file to use as the drift-correction target.
