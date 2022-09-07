from plant_detection.PlantDetection import PlantDetection
PD = PlantDetection(image='../Data/Images/041238_0.png')
PD.detect_plants()
PD = PlantDetection(image='../Data/Images/041238_0.png', morph=15, iterations=2, debug=True)
PD.detect_plants()
