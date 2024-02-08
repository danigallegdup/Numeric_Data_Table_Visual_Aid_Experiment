# Item: el_SendMessage

Messages are very IMPORTANT and we need messages in the DATA FILE to tell what events happened during a trial and at what time. Messages should be sent to the tracker everytime a stimulus screen is on or a response has been issued. One can send multiple messages, please put one message in a line.

One can also send “Data Viewer Integration Messages” to the tracker. These messages will be used by the Data Viewer software, a data analysis and visualization tool provided by SR Research to load the interest areas, background images, etc. Please see the Data Viewer user manual for a full list of Data Viewer integration messages. A few frequently used ones are listed below.

* <b>Image Loading Messages</b>

	!V IMGLOAD FILL relative_image_path
	
	!V IMGLOAD TOP_LEFT relative_image_path x_position y_position width height
	
	!V IMGLOAD CENTER relative_image_path x_position y_position width height
	
* <b>Interest Area Messages</b>

	!V IAREA RECTANGLE id left top right bottom label
	
	!V IAREA ELLIPSE id left top right bottom label 
	
	!V IAREA FREEHAND id x1, y1 x2, y2  ... xn, yn label
	
	!V IAREA FILE relative_file_path (load interest area template file)