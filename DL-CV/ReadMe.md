testing camera: gst-launch-1.0 nvarguscamerasrc sensor_id=0 !    'video/x-raw(memory:NVMM),width=1920, height=1080, framerate=30/1' !    nvvidconv flip-method=6 ! 'video/x-raw,width=960, height=540' !    nvvidconv ! nvegltransform ! nveglglessink -e^C

