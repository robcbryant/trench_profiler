# trench_profiler

================================================
HELP FILE FOR POINT_CONVERTER.PY
written and copyrighted by Robert c. Bryant 2009
================================================

Written for Python 2.*

This program emulates a 3d perspective to acturately stretch profiles photographed with control points to their metric reality and outputs the points in a horizontal/elevation format to use the georeferencing plugin in arcGIS to stretch the TIF images to accurate proportions without distortion.s


Requires a text file using the following delimited format:

Pt#,Northing,Easting,Elevation,


*Note: make sure there is a comma following the elevation as it signals the end of a line in the code

-----------------------------------------------------------------------------
To change the path of where the files are read from and written to, open the point_converter.py file in notepad or a similar editing program and change the directory paths on the following lines:

Line 65: Set the path to where the original point file will be read from

hzpointsfile = open("C:\\Users\\Lauren\\Desktop\\" + self.contents4.get(), 'w')


Line 137: Set the path to where converted point files will be written to

path = "C:\\Users\\Lauren\\Desktop\\" + input_fileName


*These are set to a windows 7 desktop. Make the necessary changes for which directory you will be using. ie, if you want to use the Parent C:\ directory then the line should read:
	hzpointsfile = open("C:\\" + self.contents4.get(), 'w')
	path = "C:\\" + input_fileName

*Notice the backslashes are doubled--this is a signal to the compiler necessary to capture one backslash symbol. Do not forget the backslashes at the end  ie, Desktop\\

-------------------------------------------------------------------------

The GUI consists of:

First Point -- End Point -- Input File name -- Output File name -- Profile Orientation

First Point: if file contains more points than profile, then it may not be '1' but rather '35' or '45.' This point should be an side point of one of the two sides of the profile

End Point: This point should also be a side point to the profile. Since the points are read consecutively it is important to take the points at one side of the profile and end with taking points on the opposite side of the profile ie.,

East <==========--------=========>West
________________________________________
I 1		  5		    9  I
I 2		  6		    10 I
I 3		  7		    11 I
I 4		  8		    12 I
I---------------------------------------


*not taking the points consecutively in this fashion can cause faulty planar distortion.

Input File name: Type any name here and its extension. The default is shown as .txt but any file extension will work as long as it follows the delimited pattern shown at the beginning of this file

Output File name: Type any name here and desired extension. The resulting delimited format will be:

Pt#, Horizontal, Elevation

*Note: Horizontal means the 'x coordinate' which is what is converted from the available x,y pts and the elevation takes the place of the vertical y coordinate. This means that these profiles aren't actuallly georeferenced. They are simply in a format that allows the georeferencing software in ArcGIS to stretch the photograph(s) to proper proportion and then exported with a scale bar and elevation meter that is true to their metric proportions, ie., if the section is 10 meters wide, then the finished image will also be 10 meters wide to scale. and the elevations should match to scale as well with their intended values. If the bottom of the profile is at 1000m asl then the finished photograph's base in arcGIS should also be at 1000m for the y coordinate.


Profile Orientation: N/w or S/E simply means that depending on the cardinal orientation of the section, it needs to be mirrored. Looking at a northern profile head on requires no changes where as looking at a southern profile without mirroring will have you seeing the pts as if you were seeing through the northern balk of the trench below it. Mirroring it is necessary to have it properly oriented to the human viewers perspective orientation when looking at it head on. Make sure to type  N/w regardless of whether or not its north or west. The same applies to S/E.


