from distutils.command.upload import upload
from pickletools import optimize

from backend.e_commerce.config.settings import BASE_DIR
from django.conf import settings
from django.db import models

from PIL import Image


class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    imagem = models.ImageField(
        upload_to="produto_imagens/%Y/%m/", blank=True, null=True
    )
    slug = models.SlugField(unique=True)
    preco_marketing = models.FloatField()
    preco_marketing_promocional = models.FloatField(default=0)
    tipo = models.CharField(
        default="V", max_length=1, choices=(("V", "Variação"), ("S", "Simples"))
    )

    @staticmethod
    def resize_image(img, new_width=800):
        img_full_path = BASE_DIR / settings.MEDIA_ROOT, img.name
        img_pil = Image.open(img_full_path)
        original_width, original_heigth = img_pil.size
        if original_width <= new_width:
            img_pil.close()
            return
        new_height = round((new_width * original_heigth / original_width))
        new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)
        new_img.save(img_full_path, optimize=True, quality=50)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        max_image_size = 800

        if self.imagem:
            self.resize_image(self.imagem, max_image_size)

    def __str__(self):
        return f"{self.nome}"


class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, blank=True, null=True)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.nome}" or f"{self.produto.nome}"

    class Meta:
        verbose_name = "Variação"
        verbose_name_plural = "Variações"
