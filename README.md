# CFUCounter

An application that counts colony-forming units in images of petri dishes. CFU Counter uses Mask R-CNN which is a
state-of-the-art model for instance segmentation, developed on top of Faster R-CNN. The CNN was trained using the Agar dataset.


https://github.com/matterport/Mask_RCNN

https://agar.neurosys.com/
![cfucounterUI](https://github.com/dedovskaya/CFUCounter/assets/71874540/a0e5cb34-1a12-4c3a-b23a-d6e56c894257)

## Instructions:
<ol>
<li><b>Download .h5 file from this link</b>: https://drive.google.com/file/d/19-mxrjV_EeSQAb7SppIVG_vgjse_pP7u/view?usp=sharing</li>
  
<li>Put .h5 file to <b>"agar_cfg20221010T2320"</b> folder</li>

<li>Create an environment with <b>Python 3.6.3</b> and install dependencies with the following commands in terminal/powershell:</li>

<ol>
  <li>conda create -n agarrcnn python=3.6.3</li>

  <li>conda activate agarrcnn</li>

  <li>pip install -r requirements.txt</li>
</ol>
</ol>

## To run the application:

python cfucounter.py

</div>
<h2>Upload a file</h2>
<ul><li><p>To upload a single image use the "Upload File" button.</p></li>
    <li><p>To upload all images from a folder use the "Upload Folder" button.</p></li>
</ul>

<h2>Set configurations</h2>
<ol>
<li><p>Set <b>Number of Samples</b>, the maximum number of final detections. If you don't know the estimated number of colonies, leave this number high.</p></li>
<li><p>Set <b>Detection Confidence</b>, minimum probability value to accept a detected instance. ROIs below this threshold are skipped. For the best results raise its value to 0.99. If you have a vague picture and you think that the application underestimates the number of colonies you can leave the default number or decrease it.</p></li>
<p>Or just leave the default parameters.</p>
</ol>
<p>Hint: you can run the detection multiple times on the same image with different configuration parameters. All the input configuration parameters are saved in the output .csv table.</p>
<h2>Run Detection</h2>
<ul>
<li>
<p>Click <b>"Detect selected"</b> to detect colonies on the displayed image. The detection will be performed on the picture that is shown in the main window. To change the picture use arrow buttons near thumbnails of images.</p></li>
<li><p>Click <b>"Detect all"</b> to detect colonies in all the uploaded images.</p></li>
</ul>
<h2>Export results</h2>
<ul>
<li><p>Click <b>"Export csv table"</b> after the detection process to save a table containing information: img name, number of colonies, bounding boxes (rectangles that surround colonies, that specify their position).</p>
<p class="warning">Please always export the table before closing the application!</p>
</li>
<div class="table-wrapper">
<table class="fl-table">
    <thead>
      <tr>
        <th>Filename</th>
        <th>Number of colonies</th>
        <th>Bounding boxes</th>
        <th>conf_numsamples</th>
        <th>conf_det_confidence</th>
        <th>Colonies per sector</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Filename</td>
        <td>Number of detected colonies</td>
        <td>Coordinates of colonies as boxes</td>
        <td>Max. number of samples</td>
        <td>Min. detection confidence</td>
        <td>Number of colonies in each sector</td>
      </tr>
    </tbody>
    </table>
</div>
<div class="sectors">
<p>Sectors represent certain areas of the petri dish:</p>
<img src="sectors_scheme.png" width='200px' alt="">
</div>
<li><p>Click <b>"Export image"</b> to save displayed image.</p></li>
</ul>
<h2>Information</h2>
<p><b>Progress bar</b> shows percentage-wise progress of a current detection process. For a large number of images, it does not update itself consistently.</p>
<p>In the bottom part of the application there is <b>log window</b> capturing all the events.</p>
</body>

## Author
Ekaterina Baikova, TU Graz, 2022

