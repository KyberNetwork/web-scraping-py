import etherscan as esc


def get_token_holders_top_100():
     tokens = esc.read_top_tokens(100)
     holders = {token[1]: esc.read_top_holders(token[2], 100) for token in tokens}
     result = {
         "tokens": tokens,
         "holders": holders
     }
     return result


get_token_holders_top_100()
