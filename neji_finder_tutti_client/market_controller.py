from typing import Optional
import hashlib

class TuttiMarketController:
    '''Tutti.marketに関連する操作を行うオブジェクトです。

    現状、必要最低限のメソッド群のみを定義しています。JavaScriptにおいて既に `こちら`_ に定義された
    操作のうち、このクラスに実装が必要なものは別途問い合わせてください。

    .. _こちら:
        https://github.com/iflb/tutti-market/blob/a4b6b9054183f761a1692ff9633a84e80d93ea3c/frontend/src/scripts/ducts.js#L142
    '''
    def __init__(self, duct):
        self._duct = duct

    async def open(self, wsd_url: str):
        '''Tutti.marketサーバーへ接続します。

        Args:
            wsd_url: DUCTSサーバーへ接続するエンドポイント
        '''
        await self._duct.open(wsd_url)

    async def register_job(
        self,
        job_class_id: str,
        job_parameter: Optional[dict] = None,
        description: Optional[str] = None,
        num_job_assignments_max: Optional[int] = None,
        priority_score: Optional[int] = None
    ) -> dict:
        '''ジョブを発注します。

        Args:
            job_class_id: ジョブクラスID
            job_parameter: 発注するジョブへ与えるパラメータ群
            description: ジョブの説明文（リクエスタから見えるメモ用）
            num_job_assignments_max: 収集する回答数上限
            priority_score: 優先度。値が小さいほど優先度が高く、優先的にワーカーへ割り当てられます。
        '''
        data = await self._duct.call(self._duct.EVENT['REGISTER_JOB'], {
                'access_token': self.access_token,
                'job_class_id': job_class_id,
                'job_parameter': job_parameter,
                'description': description,
                'num_job_assignments_max': num_job_assignments_max,
                'priority_score': priority_score
            })
        return data

    async def sign_in(self, user_id: str, password: str, access_token_lifetime: int):
        '''Tutti.marketにサインインします。
        '''
        data = await self._duct.call(self._duct.EVENT['SIGN_IN'], {
            'user_id': user_id,
            'password_hash': hashlib.sha512(password.encode('ascii')).digest(),
            'access_token_lifetime': access_token_lifetime
        })
        self.access_token = data['body']['access_token']

    async def sign_out(self):
        '''Tutti.marketからサインアウトします。
        '''
        data = await self._duct.call(self._duct.EVENT['SIGN_OUT'], {
            'access_token': self.access_token
        })
