from django.db import models
from taggit.managers import TaggableManager
from PIL import Image

def crop_center(pil_img, crop_width: int, crop_height: int) -> Image:
    """
    Функция для обрезки изображения по центру.
    """
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


class Disease(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(unique=True, max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    symptoms = TaggableManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open('media/' + str(self.image))
            x = crop_center(img, min(img.size), min(img.size))
            x.save('media/' + str(self.image))

