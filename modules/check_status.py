from eth_account.messages import encode_defunct
from loguru import logger
from eth_account import Account
from utilities.common import create_client

class CheckStatus():
    def __init__(self, index, private_key, proxy) -> None:
        self.index = index
        self.private_key = private_key
        self.wallet = Account.from_key(private_key)
        self.proxy = proxy
        self.client = create_client(proxy)


    def login(self):
        try:
            message = f'The wallet will be used for MEME allocation. If you referred friends, family, lovers or strangers, ensure this wallet has the NFT you referred.\n\nBut also...\n\nNever gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you\n\nWallet: {self.wallet.address[:5]}...{self.wallet.address[-4:]}'
            message_encode = encode_defunct(text=message)
            signed_message = self.wallet.sign_message(message_encode)
            signature = signed_message["signature"].hex()
            json_data = {
                'address': self.wallet.address,
                'delegate': self.wallet.address,
                'message': message,
                'signature': signature,
            }
            
            response = self.client.post('https://memefarm-api.memecoin.org/user/wallet-auth', json=json_data, timeout=60)
            response_data = response.json()
            if 'error' in response_data:
                logger.info(f"| {self.index} | {self.wallet.address} has no points")
                return None
            
            access_token = response_data['accessToken']
            return access_token
        except Exception as e:
            logger.error(f"Error in login: {e}")
            return None
        

    def check_win(self):
        try:
            response = self.client.get('https://memefarm-api.memecoin.org/user/results')
            response_data = response.json()
            won_status = response_data['results'][0]['won']

            if not won_status:
                logger.warning(f'| {self.index} | {self.wallet.address} | Is robot')
                response = self.client.get('https://memefarm-api.memecoin.org/user/info')
                response_data = response.json()
                username = response_data['twitter']['username']
                return f"@{username}"
            else:
                logger.success(f'| {self.index} | {self.wallet.address} | Is not robot')
                return None

        except Exception as e:
            logger.error(f"Error in login: {e}")
            return None


    def execute(self):
        try:
            access_token = self.login()
            if access_token:
                self.client.headers["authorization"] = f"Bearer {access_token}"
            return self.check_win()

        except Exception as e:
            logger.error(f"Error in login: {e}")
            return None

