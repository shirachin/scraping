def detect_text_uri(uri) -> str:
    """Detects text in the file located in Google Cloud Storage or on the Web."""
    from google.cloud import vision
    from settings.settings import COUNTER_URL
    import requests

    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri

    response = client.text_detection(image=image)
    requests.get(COUNTER_URL)
    texts = response.text_annotations

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

    return texts[0].description
    
if __name__ == '__main__':
    detect_text_uri('https://d280xyghme9e5g.cloudfront.net/txt2img?f=2&…2&m=mbkn&d=16a555544e776b6a4e31637a4d3541544d040e')