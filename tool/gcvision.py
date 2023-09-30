def detect_text_uri(uri) -> str:
    from google.cloud import vision
    from tool.settings import COUNTER_URL
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