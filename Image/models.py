from django.db import models

from Base.common import deprint
from Base.error import Error
from Base.response import Ret
from Base.validator import field_validator


class Image(models.Model):
    """图片类"""
    L = {
        'key': 255,
    }
    key = models.CharField(
        max_length=L['key'],
        unique=True,
    )
    FIELD_LIST = ['key']

    class __ConfigNone:
        pass

    @classmethod
    def _validate(cls, dict_):
        """验证传入参数是否合法"""
        return field_validator(dict_, Image)

    @classmethod
    def create(cls, key):
        ret = cls._validate(locals())
        if ret.error is not Error.OK:
            return ret

        try:
            o_image = cls(
                key=key,
            )
            o_image.save()
        except Exception as err:
            deprint('Image-create', str(err))
            return Ret(Error.ERROR_CREATE_IMAGE, append_msg=str(err))
        return Ret(o_image)

    @classmethod
    def get_old_images(cls, end, count=10):
        if count > 10 or count <= 0:
            count = 10
        last = cls.objects.count()

        print('end', end)
        print('count', count)
        print('last', last)

        if end > last or end == -1:
            end = last
        if end - count < 0:
            count = end
        start = end - count

        print('start', start)

        image_list = []
        for o_image in cls.objects.all()[start:end]:
            image_list.append(o_image.to_dict())

        return dict(
            image_list=image_list,
            count=count,
            next=start,
        )

    def to_dict(self):
        return dict(
            key=self.key,
            id=self.pk,
        )
