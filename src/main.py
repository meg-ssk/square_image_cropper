import sys
import glob
import numpy as np
import cv2
import tqdm
import yaml

def load_config_yaml():
    # load config yaml
    print("load cfg yaml")
    with open('cfg.yaml') as file:
        cfg = yaml.safe_load(file)
    return cfg

def fetch_image_list(cfg):
    target_extension, path_to_image_directory = cfg['target_extension'], cfg['path_to_image_directory']
    image_list = sorted(glob.glob( path_to_image_directory + '*.' + target_extension))
    
    return image_list

def check_is_power_of_two(image_size):
    image_size = int(image_size)
    is_power_of_two = np.abs(np.log2(image_size) - int(np.log2(image_size))) < 10**(-6)    
    if not is_power_of_two:
        print("output image size is NOT power of two. Modify output_image_size `./cfg.yaml`. ")
        sys.exit()
    else:
        return
    
def down_size_output_image_less_than_cropped_image(output_image_size, image_shape):
    while output_image_size > np.min(image_shape[0:2]):
            output_image_size = int(output_image_size/2)
    return output_image_size

def generate_square_image(image, output_image_size):
    image_height, image_width = image.shape[0], image.shape[1]
    
    left = np.random.randint(0, image_width  - output_image_size + 1)
    top  = np.random.randint(0, image_height - output_image_size + 1)
    right, bottom = left + output_image_size, top + output_image_size
    
    return image[top:bottom, left:right, :]

def resize_image(output_image, output_image_size_org):
    if output_image.shape[0] != output_image_size_org:
            output_image = cv2.resize(output_image,
                                      (output_image_size_org, output_image_size_org),
                                      interpolation=cv2.INTER_CUBIC)
    
    return output_image

def write_square_image(output_image, image_name, cfg):
    output_directory, output_extension = cfg['output_directory'], cfg['output_extension']
    output_image_path = output_directory + image_name + '.' +output_extension
    cv2.imwrite(output_image_path, output_image)
    return

def main():
    cfg = load_config_yaml()
    output_image_size_org, output_directory, output_extension = \
        cfg['output_image_size'], cfg['output_directory'], cfg['output_extension']
    
    check_is_power_of_two(output_image_size_org)
    
    image_list = fetch_image_list(cfg)
    
    for image_path in tqdm.tqdm(image_list):
        
        image = cv2.imread(image_path)
        image_name = image_path.split('/')[-1].split('.')[0]
        
        output_image_size = cfg['output_image_size']
        
        output_image_size = down_size_output_image_less_than_cropped_image(output_image_size, image.shape)
        output_image = generate_square_image(image, output_image_size)
        output_image = resize_image(output_image, cfg['output_image_size'])
        
        write_square_image(output_image, image_name, cfg)
                
    return

if __name__ == "__main__":
    main()