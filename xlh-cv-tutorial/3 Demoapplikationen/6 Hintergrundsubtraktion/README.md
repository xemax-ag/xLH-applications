# Hintergrundsubtraktion

# Aufgabe
In einem Video mit unregelmässigen Hintergrund ist der braune Labrador (Max) zu extrahieren. 
Der Massepunkt soll mit einem roten Punkt in das Video eingeblendet werden.

## Lösungsvorgehen
1. Einlesen des Originalvideos
2. Hintergrundsubtraktion (`cv2.createBackgroundSubtractorMOG2()`)
3. Morphologische Operationen
4. Maskierung
5. Konturenoperationen
6. Ausgabe des bearbeiteten Videobildes

<img src="img/background_subtraction.png" width="100%">

## Weiterführende Links
* https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_video/py_bg_subtraction/py_bg_subtraction.html
* https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_video/py_bg_subtraction/py_bg_subtraction.html
* https://docs.opencv.org/4.2.0/d1/dc5/tutorial_background_subtraction.html
* https://docs.opencv.org/4.2.0/d7/d7b/classcv_1_1BackgroundSubtractorMOG2.html