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

def main():
    cfg = load_config_yaml()
    output_image_size, output_directory = cfg['output_image_size'], cfg['output_directory']
    image_list = fetch_image_list(cfg)
    
    for image_path in tqdm.tqdm(image_list):
        
        image = cv2.imread(image_path)
        image_name = image_path.split('/')[-1].split('.')[0]
        image_height, image_width = image.shape[0], image.shape[1]
        
        
        if np.min(image.shape[0:2]) >= output_image_size:
            left = np.random.randint(0, image_width  - output_image_size)
            top  = np.random.randint(0, image_height - output_image_size)
            right, bottom = left + output_image_size, top + output_image_size
            output_image = image[left:right, top:bottom, :]
            try:
                cv2.imwrite(output_directory + image_name + ".png", output_image)
            except:
                print([right, bottom], [image_height, image_width])
        else:
            pass
        
    return

if __name__ == "__main__":
    main()