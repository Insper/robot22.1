# Como gerar um arquivo de calibração de câmera

Para calibrar a câmera você vai precisar de um padrão xadrez (*checkerboard pattern*) que acompanha o ROS. 

	rosrun camera_calibration cameracalibrator.py --size 8x6 --square 0.108 image:=/usb_cam/image_raw camera:=/usb_cam


Depois da calibração, será salvo um arquivo em **/tmp/calibrator.tar.gz** que descompactado gera um arquivo **ost.yaml**

Mova este arquivo para onde será necessário (o lugar adequado é indicado no launch file que vai usar a imagem)


Por exemplo, para rastrear via webcam com o alvar, o lugar desejado é: ~/.ros/camera_info/head_camera.yaml


Se você estiver com muita pressa e não se importar muito com erros de medida, use [este arquivo](head_camera.yaml)