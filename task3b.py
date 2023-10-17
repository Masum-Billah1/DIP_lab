import numpy as np
import cv2
import matplotlib.pyplot as plt
image= cv2.imread('imgg/cameraman.jpg', cv2.IMREAD_GRAYSCALE)
image=cv2.resize(image,(512,512))
height=512
width=512
def addNoise(image):
    noise_image=image.copy()
    noise=0.02
    height,width=512,512

    for h in range(height):
        for w in range(width):
            random_val=np.random.rand()
            if random_val<noise/2:
                noise_image[h,w]=0
            elif random_val<noise:
                noise_image[h,w]=255
    return noise_image
noise_image=addNoise(image)
plt.subplot(3,3,4)
plt.imshow(image,cmap='gray')
plt.subplot(3,3,5)
plt.imshow(noise_image,cmap='gray')
def padding_add(n,noise_image):
    mask = np.ones((n,n), dtype=np.float32) / (n*n*1.0)
    pad_height=n//2
    pad_width=n//2
    new_height=height+2*pad_height # 0 value added left and right
    new_width=width+2*pad_width  # 0 value added top and bottom
    pad_image=np.zeros((new_height,new_width),dtype=np.uint8)
    pad_image[pad_height:pad_height + height, pad_width:pad_width + width] = noise_image

    return pad_image,mask

def masking2(noise_image,height,width,n):
    spatial_image=np.zeros((height,width),dtype=np.uint8)

    pad_image,mask=padding_add(n,noise_image)

    # mask = np.ones((n,n), dtype=np.float32) / (n*n*1.0)
    # pad_height=n//2
    # pad_width=n//2    
    # pad_image=np.pad(noise_image,((pad_height,pad_height),(pad_width,pad_width)),mode='constant')

    for h in range(height):
        for w in range(width):
            tmp_window=pad_image[h:h+n,w:w+n]
            weight=np.sum(tmp_window*mask)
            spatial_image[h,w]=weight

    return spatial_image

def PSNR(original,noisy):
   mse = np.mean((original.astype(np.float32) - noisy.astype(np.float32)) ** 2)
   max_pixel_value = 255.0
   psnr = 20 * np.log10(max_pixel_value / np.sqrt(mse))
   return psnr
c=0
for i in range(1,4):
    n=(i+1)*2-1
    spatial_image=masking2(noise_image,height,width,n)
    med_original=PSNR(image,spatial_image)
    plt.subplot(3,3,i)
    plt.imshow(spatial_image,cmap='gray')
    plt.title(f'{n}X{n} psnr {med_original:.2f} dB')

plt.tight_layout()
plt.show()



