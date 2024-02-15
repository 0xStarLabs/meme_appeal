from loguru import logger
import tls_client


class Form:
    def __init__(self, index: int, proxy: str, twitter_username: str, discord: str, wallet_address: str, answer: str):
        self.index = index
        self.proxy = proxy
        self.discord = discord
        self.wallet_address = wallet_address
        self.twitter_username = twitter_username
        self.client: tls_client.Session | None = None
        self.answer = answer

        self.__init_data()

    def __init_data(self):
        for x in range(5):
            try:
                self.client = self.create_client(self.proxy)
                break
            except Exception as err:
                if x + 1 != 5:
                    logger.error(f"{self.index} | Failed to init data: {err}")
                else:
                    raise Exception(f"Failed to init data 5 times. Exit...")

    def login(self):
        try:
            headers = {
                'authority': 'dyno.gg',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'cache-control': 'no-cache',
                'pragma': 'no-cache',
                'referer': 'https://dyno.gg/',
                'sec-ch-ua-arch': '"x86"',
                'sec-ch-ua-bitness': '"64"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"15.0.0"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
            }

            response = self.client.get('https://dyno.gg/auth', headers=headers)

            state = response.text.split("state=")[1].split("'")[0]

            headers = {
                'authority': 'discord.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'cache-control': 'no-cache',
                'pragma': 'no-cache',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'cross-site',
                'upgrade-insecure-requests': '1',
            }

            self.client.get(
                f'https://discord.com/oauth2/authorize?redirect_uri=https://dyno.gg%2Freturn&scope=identify%20guilds%20email%20applications.commands.permissions.update&response_type=code&prompt=none&client_id=161660517914509312&state={state}',
                headers=headers,
            )

            headers = {
                'authority': 'discord.com',
                'accept': '*/*',
                'accept-language': 'ru',
                'authorization': self.discord,
                'content-type': 'application/json',
                'origin': 'https://discord.com',
                'referer': f'https://discord.com/oauth2/authorize?redirect_uri=https://dyno.gg%2Freturn&scope=identify%20guilds%20email%20applications.commands.permissions.update&response_type=code&prompt=none&client_id=161660517914509312&state={state}',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                'x-debug-options': 'bugReporterEnabled',
                'x-discord-locale': 'en-US',
                'x-discord-timezone': 'Europe/Kiev',
                'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6InJ1IiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExOS4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTE5LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjI2NDkxMywiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0=',
            }

            params = {
                'client_id': '161660517914509312',
                'response_type': 'code',
                'redirect_uri': 'https://dyno.gg/return',
                'scope': 'identify guilds email applications.commands.permissions.update',
                'state': state,
            }

            json_data = {
                'permissions': '0',
                'authorize': True,
                'integration_type': 0,
            }

            response = self.client.post(
                'https://discord.com/api/v9/oauth2/authorize',
                params=params,
                headers=headers,
                json=json_data,
            )

            location = response.json()['location']

            headers = {
                'authority': 'dyno.gg',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'referer': 'https://discord.com/',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'cross-site',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
            }

            params = {
                'code': location.split('code=')[1].split('&')[0],
                'state': location.split('state=')[1].strip(),
            }

            response = self.client.get('https://dyno.gg/return', params=params, headers=headers, allow_redirects=True)

            headers = {
                'authority': 'dyno.gg',
                'accept': 'application/json, text/plain, */*',
                'cache-control': 'no-cache',
                'content-type': 'application/json;charset=UTF-8',
                'origin': 'https://dyno.gg',
                'pragma': 'no-cache',
                'referer': 'https://dyno.gg/form/ecfaebc1',
                'sec-ch-ua-arch': '"x86"',
                'sec-ch-ua-bitness': '"64"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"15.0.0"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
            }

            json_data = {
                'formData': [
                    {
                        'question': 'What is your X handle?',
                        'type': 'shortAnswer',
                        'id': '572a',
                        'required': False,
                        'answer': self.twitter_username,
                    },
                    {
                        'question': 'What is the wallet address linked to the X handle above?',
                        'type': 'shortAnswer',
                        'id': '63f9',
                        'required': False,
                        'description': '',
                        'answer': self.wallet_address,
                    },
                    {
                        'question': 'Please describe your issue',
                        'type': 'paragraph',
                        'id': 'b370',
                        'required': True,
                        'answer': self.answer,
                    },
                ],
            }
            logger.info(f"{self.index} | Trying to send a form...")
            response = self.client.post('https://dyno.gg/api/forms/ecfaebc1/submit', headers=headers, json=json_data)

            if "notMember" in response.text:
                logger.error(f"{self.index} | Discord account is not MemeLand server member.")
                return True, False

            if response.status_code == 200:
                logger.success(f"{self.index} | Form sent successfully.")
                return True, True
            else:
                logger.error(f"{self.index} | Unknown error: {response.text}")
                return True, False

        except Exception as err:
            logger.error(f"{self.index} | Failed to send a form: {err}")
            return False, False

    @staticmethod
    def create_client(proxy: str) -> tls_client.Session:
        session = tls_client.Session(
            client_identifier="chrome_120",
            random_tls_extension_order=True,
        )

        if proxy:
            session.proxies.update({
                "http": "http://" + proxy,
                "https": "http://" + proxy,
            })

        return session
