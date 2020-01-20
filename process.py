import base64
def convert(image_path):
    with open(image_path, "rb") as img_file:
        my_string = base64.b64encode(img_file.read()).decode('utf-8')
    return my_string    