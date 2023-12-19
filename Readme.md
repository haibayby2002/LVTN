# Recommended environment
- Python 3

# Setup
Use PyCharm to install all the import library in quyhai_ui.py

# Using
1. In terminal: `python3 quyhai_ui.py`
2. If you want to crop image in polygon mode,click on the Polygon checkbox button. If not, it will automatically understand that it is in rectangle mode.
3. Reference to video source (.mp4 file has been tested)
4. Cut the image. 
   1. When using rectangle mode, click and hold the mouse from the top left to the bottom right of the button, hit `Space` button to finish.  
   2. When using Polygon mode, click at 3 or more points to make polygon. Note: Polygon must be in covex
5. In both cases, if finish cutting image, the location of the video will appear in Program. Press `Analyze` button to see the video.

# Still in develop
1. Export to CSV. Configure interval frame
2. Compress CSV using Huffman algorithm before sending to data to the server
3. Apply Semantic Segmentation Model