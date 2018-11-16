from django.utils.crypto import get_random_string
from django.views import View

from Base.common import deprint
from Base.error import Error
from Base.policy import get_avatar_policy
from Base.qn import QN_PUBLIC_MANAGER
from Base.response import response, error_response
from Base.validator import require_get, require_json, require_post
from Image.models import Image


MLC_KEYS = ['mao', 'lu', 'chan', '11', '18', 'sheng', 'ri', 'kuai', 'le']
TEMPLATE = 'engif/mlc/%s.png'
MLC_IMG_LIST = []
for k in MLC_KEYS:
    MLC_IMG_LIST.append(dict(key=TEMPLATE % k))
MLC_IMG_COUNT = len(MLC_KEYS)

MLC_IMG_DICT = dict(
    image_list=MLC_IMG_LIST,
    count=MLC_IMG_COUNT,
    next=0,
)


class ImageHistoryView(View):
    @staticmethod
    @require_get([{
        'value': 'end',
        'default': True,
        'default_value': -1,
        'process': int,
    }, {
        'value': 'count',
        'default': True,
        'default_value': 10,
        'process': int,
    }])
    def get(request):
        """ GET /api/image/history

        获取历史图片
        """

        # end = request.d.end
        # count = request.d.count
        # image_list = Image.get_old_images(end, count)

        return response(body=MLC_IMG_DICT)


class ImageView(View):
    @staticmethod
    @require_get()
    # @require_login
    # @require_scope(deny_all_auth_token=True)
    def get(request):
        """ GET /api/image/

        获取七牛上传token
        """
        # o_user = request.user
        # filename = request.d.filename

        # if not isinstance(o_user, User):
        #     return error_response(Error.STRANGE)
        deprint('ImageView-get')

        import datetime
        crt_time = datetime.datetime.now().timestamp()
        key = '%s_%s' % (crt_time, get_random_string(length=4))
        qn_token, key = QN_PUBLIC_MANAGER.get_upload_token(key, get_avatar_policy())
        return response(body=dict(upload_token=qn_token, key=key))

    @staticmethod
    @require_json
    @require_post(['key'])
    def post(request):
        """ POST /api/image/

        七牛上传用户头像回调函数
        """
        deprint('ImageView-post')
        ret = QN_PUBLIC_MANAGER.qiniu_auth_callback(request)
        if ret.error is not Error.OK:
            return error_response(ret)

        key = request.d.key
        ret = Image.create(key)
        if ret.error is not Error.OK:
            return error_response(ret)
        o_image = ret.body
        if not isinstance(o_image, Image):
            return error_response(Error.STRANGE)

        return response(body=o_image.to_dict())
