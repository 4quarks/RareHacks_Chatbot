from google_images_download import google_images_download


def getImageFromGoogle(image_to_search,num_images=1):

    response = google_images_download.googleimagesdownload()
    absolute_image_paths = response.download({"keywords":image_to_search,"limit":5})

    return absolute_image_paths[0][image_to_search]


