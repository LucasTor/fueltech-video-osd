# fueltech-video-osd

⚠️⚠️⚠️ **Highly experimental project** ⚠️⚠️⚠️ 

The goal of this project is to be able to generate OSD (On screen display) for FuelTech EFI, which saves logs internally, to overlay on videos from the cameras to create a new way to show data on the screen 

To run it, install the frontend dependencies with ```npm i```, and then start it using ```npm start```
Install the backend dependencies with ```pip install -r requirements.txt```, and then run it using ```flask --app api run```

TODO:
- Upload log file via frontend
- Download the video from the browser once it's done generating
- Generate more gauges (boost pressure, oil/gas pressure, tps...) (ideas are welcome)
- Download or save the layout of the gauges from the frontend (just a JSON, which could be saved in localstorage or downloaded as a file), if downloadable, allow users to upload the file to set the layout
- Make resolution selectable, currently, it's fixed on 1080x1920 (I made it with Instagram reels in mind)
- Optimize generation? Really slow as is
