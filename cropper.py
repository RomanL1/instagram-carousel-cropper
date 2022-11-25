#Goal is to crop images into segments into the format 1080x1350 (ratio 1.25)

from PIL import Image

imgToCrop = Image.open("./input/_0IM9922.jpg")

exportResize = "./output/resized.jpg"
exportSegmentsPath = "./output/segment$$x$$.jpg"
exportBanner = "./output/banner.jpg"

segmentHeight = 1350
segmentWidth = 1080

def make_banner(image, min_size=256, fill_color=(0, 0, 0, 0)):
    x, y = segmentWidth, segmentHeight
    size = max(min_size, x, y)
    new_im = Image.new('RGBA', (x, y), fill_color)
    new_im.paste(image, (0, int((y -image.size[1]) / 2)))
    return new_im

imagesExported = 1

width, height = imgToCrop.size
print(width)
print(height)

newWidth = int(width/(height/segmentHeight))
newSize = newWidth, segmentHeight

segments = newWidth/segmentWidth
print(segments)
print("Segments there will be")

if newWidth%segmentWidth > 0:
    print("Cant resize image into good segments, please try another format")
    print(newWidth%segmentWidth)
    print(" pixels left")
    optimalWidth = (newWidth - newWidth%segmentWidth)*(height/segmentHeight)
    print("Optimal width would be:")
    print(optimalWidth)
    optimalRatio = optimalWidth/height
    print("Optimal ratio (width/height) would be:")
    print(optimalRatio)
    print("Or version with one more image:")
    optimalWidth2 = ((newWidth - newWidth%segmentWidth) + segmentWidth)*(height/segmentHeight)
    print("Optimal width2 would be:")
    print(optimalWidth2)
    optimalRatio2 = optimalWidth2/height
    print("Optimal ratio (width/height) would be:")
    print(optimalRatio2)
    exit()

resizedImage = imgToCrop.resize(newSize, Image.Resampling.LANCZOS)
resizedImage.save(exportResize)

segments = int(segments)
for x in range(segments):
    top = segmentHeight
    left = segmentWidth*x
    bottom = 0
    right = segmentWidth*(x+1)
    crop = "top: " + str(top) + " left: " + str(left) + " bottom: " + str(bottom) + " right: " + str(right)
    print(crop)
    croppedImage = resizedImage.crop((left, bottom, right, top))
    exportImagePath = exportSegmentsPath.replace("$$x$$", str(imagesExported))
    print(exportImagePath)
    imagesExported = imagesExported+1
    croppedImage.save(exportImagePath, "JPEG")
    print(imagesExported)
    
bannerSize = segmentWidth, int(segmentHeight/(newWidth/segmentWidth))
bannerImage = imgToCrop.resize(bannerSize, Image.Resampling.LANCZOS)

bannerImage = make_banner(bannerImage)
bannerImage = bannerImage.convert('RGB')
bannerImage.save(exportBanner)