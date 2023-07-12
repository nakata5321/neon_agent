import json
import web3
import ipfs_api
import base58
from logging import getLogger
from eth_account.messages import encode_defunct
from utils.offer import Offer

from config import (
    NEON_WSS,
    MNEMONIC
)

logger = getLogger(__name__)


class NeonAgent:
    """
    Robonomics agent to listen Neon network.
    It can listen IPFS pubsub topics and create offer based on them.
    """
    def __init__(self):

        self.ipfs_subscriber = ipfs_api.pubsub_subscribe("test", self.sub_callback)
        self.offer = Offer
        self.data = ""
        self.w3 = web3.Web3(web3.Web3.HTTPProvider(NEON_WSS))
        self.account = web3.eth.account.from_mnemonic(MNEMONIC)

    def make_offer(self, data):
        try: #TODO delete unused parameters
            cur_offer = Offer
            cur_offer.model = data["model"]
            cur_offer.objective = data["objective"]
            cur_offer.token = data["token"]
            cur_offer.cost = data["cost"]
            cur_offer.validator = data["validator"]
            cur_offer.lighthouse = data["lighthouse"]
            cur_offer.lighthouseFee = 1
            cur_offer.deadline = web3.eth.get_block_number() + 100000
            cur_offer.nonce = web3.eth.get_transaction_count(self.account)
            cur_offer.sender = self.account
        except Exception as e:
            logger.warning("not enough arguments")

        # TODO разобраться как подписывать сообщение
        types = ['bytes',
                 'bytes',
                 'address',
                 'uint256',
                 'address',
                 'address',
                 'uint256',
                 'uint256',
                 'uint256',
                 'address']

        hash = web3.Web3.soliditySha3(types, [base58.b58decode(cur_offer.model),
                                         base58.b58decode(cur_offer.objective),
                                         cur_offer.token,
                                         int(cur_offer.cost),
                                         cur_offer.validator,
                                         cur_offer.lighthouse,
                                         int(cur_offer.lighthouseFee),
                                         int(cur_offer.deadline),
                                         int(cur_offer.noncecur_offer),
                                         cur_offer.sender])
        msg = encode_defunct(hash)

        cur_offer.signature = web3.eth.account.sign_message(msg, private_key=private_key)

        return cur_offer

    def sub_callback(self, data) -> None:
        try:
            self.data = json.loads(data)
        except ValueError:
            logger.warning("Invalid data")
        self.offer = self.make_offer(self.data)


if __name__ == '__main__':
    agent = NeonAgent()
# Press the green button in the gutter to run the script.
