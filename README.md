# GPS track analyzer
This codes analyses gps tracks in .gpx format. Computes relevant information and plots them

The code can be used by simply running

```
python gps_analyzer.py
```

The code will load the information in the provided .gpx track, which is referred to a 80 km bike run. The auxiliary files ```gps_parse.py``` and ```haversine.py``` take care of parsing the position, elevation and time information in the .gpx track file and of computing the distance between two points. 

Running the code will print at video various information on the gps track and also provides some plots.



