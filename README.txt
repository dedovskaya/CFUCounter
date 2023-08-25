######################################################################################################
CFU Counter

An application that counts colony forming units in images of petri dishes. CFU Counter uses Mask R-CNN which is a
state of the art model for instance segmentation, developed on top of Faster R-CNN. The CNN was trained using Agar dataset.

https://github.com/matterport/Mask_RCNN
https://agar.neurosys.com/

######################################################################################################
# cfu_counter_windows.zip is the achive containing .exe file of CFUCounter application for Windows OS.

To run the application run cfucounter.exe file.

# cfu_counter_linux.zip is the achive containing files for installation using Linux terminal/Windows powershell.
# Instructions:
# Create environment with Python 3.6.3 and install dependences with the following commands in terminal/powershell:

conda create -n agarrcnn python=3.6.3
conda activate agarrcnn
pip install -r requirements.txt

# To run the application:

python cfucounter.py