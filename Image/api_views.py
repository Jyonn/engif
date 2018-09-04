from django.utils.crypto import get_random_string
from django.views import View

from Base.common import deprint
from Base.error import Error
from Base.policy import get_avatar_policy
from Base.qn import QN_PUBLIC_MANAGER
from Base.response import response, error_response
from Base.validator import require_get, require_json, require_post
from Image.models import Image


class ImageView(View):
    @staticmethod
    @require_get()
    # @require_login
    # @require_scope(deny_all_auth_token=True)
    def get(request):
        """ GET /api/image

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
        """ POST /api/image

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
