# GPS track analyzer
This codes analyses gps tracks in .gpx format. Computes relevant information and plots them

The code can be used by simply running

```
python gps_analyzer.py
```

The code will load the information in the provided .gpx track, which is referred to a 80 km bike run. 
The file ```gps_parse.py``` takes care of parsing the position, elevation and time information in the .gpx track file, while ```haversine.py``` computes the distance between two points defined by their respective latitude and longitude.

Running the code will print at video various information on the gps track and also provides some plots.



