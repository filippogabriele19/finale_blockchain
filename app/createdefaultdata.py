from zoneinfo import available_timezones
from .models import Article


def PopulateDb():
    pr1 = Article(
        name="Bicolor",
        image_url="https://d1fufvy4xao6k9.cloudfront.net/images/landings/353/two-tone-wingtip-shoes.png",
        description="top quality",
    )
    pr1.save()
    pr2 = Article(
        name="Brogue",
        image_url="https://d1fufvy4xao6k9.cloudfront.net/feed/img/man_shoe/186385/side.png",
        description="top quality",
    )
    pr2.save()
    pr3 = Article(
        name="Wingtip",
        image_url="https://d1fufvy4xao6k9.cloudfront.net/images/landings/356/brown-brogues_5.png",
        description="top quality",
    )
    pr3.save()
    pr4 = Article(
        name="Brogue brown leather and tweed",
        image_url="https://d1fufvy4xao6k9.cloudfront.net/feed/img/man_shoe/260379/side.png",
        description="top quality",
    )
    pr4.save()
    pr5 = Article(
        name="Cap toe Monk shoes",
        image_url="https://d1fufvy4xao6k9.cloudfront.net/feed/img/man_shoe/155379/side.png",
        description="top quality",
    )
    pr5.save()
