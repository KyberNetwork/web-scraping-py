from typing import *
from logzero import logger as log
import etherscan as esc


tokens = esc.read_top_tokens(100)
holders = {t[1]: esc.read_top_holders(t[2], 100) for t in tokens}
