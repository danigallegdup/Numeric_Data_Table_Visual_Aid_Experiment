# Installation of the EyeLink Plugin

This plugin should also work on Linux and Mac, but we have only tested it on the Windows platform. The installation instructions presented below are for the Windows platform.

* Download the latest version of the Plugin from the SR Support website, under the Getting Started with Experimental Programming section.
* Unzip the downloaded .zip file and copy all the folders contained in the .zip file to C:\Program Files (x86)\OpenSesame\share\opensesame_plugins\
* Download and install the latest version of the EyeLink Developer’s Kit from the SR Support website, from the Downloads->Eyelink Display Software section. https://www.sr-support.com/forum/downloads/eyelink-display-software/39-eyelink-developers-kit-for-windows-windows-display-software
* OpenSesame needs the Pylink library to communicate with the tracker. Pylink is a Python wrapper of the EyeLink API (part of the Developer’s Kit) and one can find this library from C:\Program Files (x86)\SR Research\EyeLink\SampleExperiments\Python. There are multiple versions, with the last two digits in the folder name corresponding to the Python version it was built against (i.e., pylink27 is for the Python 2.7 series). Please rename the correct version of pylink folder to “pylink” and copy it to C:\Program Files (x86)\OpenSesame\Lib\site-packages. 
* After the above steps, please be sure to set the IP address of the experimental PC to “100.1.1.2” (without quotes) and Subnet mask to “255.255.255.0” (without quotes) so the experimental PC is on the same network as the EyeLink Host PC. Open the example experiment that comes with the EyeLink plugin to test the link between the two machines.  

OpenSesame supports Pygame (legacy), Psychopy, and Expyriment as its backend. We have found the Expyriment backend is crash-prone and would encourage users to stick to the Psychopy backend, which is robust and supports frequently used visual stimuli for visual psychophysics (e.g., gratings).

# Usage Guidelines

After the Plugin has been installed, one should see eight items come up in the item toolbar of the OpenSesame interface. To use the plugin, simply drag one of these items to the required location in the experiment sequence. For general cognitive tasks, we recommend that users follow these integration steps.

## Experiment level
1. Connect to the tracker when the script initializes. Please use the el_Connect item for this task. The configuration options available for this item will be elaborated in the next section.
2. Calibrate the tracker at the beginning of each block. This will help the user to maintain optimal tracking accuracy. For fMRI or tasks in which interruption of the task should be avoided, users can calibrate the tracker once at the beginning of each run/session. The item for this function is el_CamSetup. This item will help users to transfer the camera image to the experimental PC, to adjust the pupil/CR threshold by using hot keys on the experimental PC keyboard, to calibrate the tracker and validate the calibration results. 
3. Run the experimental trials one-by-one and record eye movement data.
4. Disconnect from the Eyelink Host PC and transfer the data file to the experimental PC.

## Trial level
1. Drift-correction or drift-check. This procedure will check the tracking accuracy and give the user a chance to re-calibrate the tracker, if needed.
2. Send commands/messages to the tracker to draw reference landmarks on the Host PC screen (optional, use the el_Command or el_Message items).
3. Start recording. We start and stop recording at the beginning and end of each trial, so the inter-trial intervals won’t be recorded; this will reduce the size of the EDF data file. For EEG and tasks where  continuous recording is preferred, please start recording at the beginning of each run/session. The user also has the option to send a “recording status” message to the tracker; this message will be shown in the bottom-right corner of the Host PC screen.
4. Draw experimental graphics and send messages to the tracker to mark the onset of these stimuli, and maybe also the interest areas that will be used in data analysis. This is IMPORTANT, otherwise, there is no way to tell when and what stimuli was presented from the eye movement data file.
5. Collect subject responses and send messages to the tracker.
6. Stop recording and send all experimental variables to the tracker. These variables will be accessible from the Data Viewer software, a nifty data analysis and visualization tool developed by SR Research.

We have provided an example script with all the recommended usage of the tracker. The functions of each of the items in the plugin are briefly explained below. Depending on the hardware, some options may not be configrable through the EyeLink Plugin (and will be grayed out).

# Item: el_Connect

Establish a link to the EyeLink Host PC, configure the tracker, and automatically open a data file on the Host to record the eye movement data. The options can be set with this item are explained in the table below.

* <b>Tracker Address</b>
	
	The IP address of the Eyelink Host PC. The default IP address of the Host PC is 100.1.1.1; the IP address of the experimental PC should be in the same network of the Host PC, i.e., in the range of 100.1.1.2-255.

* <b>Tracker Version</b>

	The model of EyeLink tracker being used for data collection, could be Eyelink I, EyeLink II, EyeLink 1000, EyeLink 1000 Plus, or EyeLink Portable DUO. Some configuration options may not be available for certain models, e.g., sampling rate cannot be set from the EyeLink Plugin for EyeLink I and II, and the Pupil-only tracking method is not available in EyeLink 1000, 1000 Plus and Portable DUO.

* <b>Camera Mount</b>

	The mounting solution of the EyeLink camera, i.e., Desktop, Tower, Arm, Long-range. 

* <b>Mount Usage</b>
	
	Tracking in either Head Stabilized or Remote (head free to move) mode. The remote mode is unavailable for Tower and Long-range mounts. Tracking in remote mode requires the use of a target sticker on the subject’s forehead.

* <b>Dummy Mode</b>
	
	Run the tracker in “simulation” mode, i.e., no physical connection to the tracker is established. In Dummy Mode, the user should press F1 to skip Camera setup/calibration, and the drift-correction/check target will briefly flashes and then disappear (as not tracker is physically connected to the experimental PC).

* <b>Link Filter Level</b>
	
	The EyeLink trackers utilizes a heuristic filtering algorithm for denoise purposes (see Stampe, 1993). Each increase in filter level reduces noise by a factor of 2 to 3 but introduces a 1-sample delay to the data available over the link. The default option is set to STANDARD, but user can turn off Link Filter if real time online access of gaze data is critical.

* <b>File Filter Level</b>
	
	Same as above, but applies to the data recorded in file.

* <b>Eye Event Data</b>

	Set how velocity information for saccade detection is to be computed. This option is almost always set to GAZE. Please see the EyeLink user manual (section 4) for details of various eye events (e.g., fixation, saccade). 

* <b>Saccade Sensitivity</b>

	Sensitivity of the Eyelink online parse, see Section 4.3.9 of the user manual. For Eyelink II and newer models, HIGH-velocity=22 deg/sec, acceleration=3200 deg/sec^2; NORMAL-velocity=30 deg/sec, acceleration=8000 deg/sec^2."

* <b>Eye Tracking Mode</b>

	Select the tracking algorithm. EyeLink I operates in Pupil-only mode, while EyeLink II operates in either Pupil-only or Pupil-CR mode. EyeLink 1000 and newer models all operate in Pupil-CR mode. The Pupil-CR tracking algorithm is resilient to small head movements (i.e., drift-free to certain extent). This is why force drift-correcting the tracker is not recommended for EyeLInk 1000 and newer models.

* <b>Pupil Detection</b>

	Set the algorithm used to detect the pupil center. This option only applies to EyeLink 1000 and newer models.

* <b>Sampling rate</b>

	The sampling rate of the tracker.

* <b>Eye(s) to Track</b>

	Set the eyes to track; can be changed on the Host PC manually.

* <b>Pupil Size</b>

	Record the pupil size in arbitrary units, AREA and DIAMETER measures are equivalent: DIAMETER = 256*SQRT(AREA/PI). The pupil size recorded in the data files is in arbitrary units; calibration during testing is required if one needs to report pupil size in real world units (i.e., mm). Please see this SR Support forum post for details, https://www.sr-support.com/showthread.php?5021-Answers-to-EyeLink-Host-PC-and-Hardware-FAQ&p=20283#post20283.

* <b>EDF Folder</b>

	The EyeLink data file will be saved on the Host PC and retrieved to the current <b>'EDF Folder'</b> at the end of a session. By default, the subject number the user specified at the beginning of a session will be used to name the EDF data file. Please bear in mind that the length of the EDF data file name and hence the subject number you specified CANNOT exceed 8 characters.
