import stackexchange
api_key = 'R91Ul6Hz*Reptmjm52BPHQ(('
so = stackexchange.Site(stackexchange.StackOverflow, api_key)


def fetch_code_blocks(searchterms):
    """returns [(url, codeblock1), ..., (url, codeblockN)]"""
    print(so.search(intitle=searchterms))


def run():
    fetch_code_blocks('fibonacci')


if __name__ == '__main__':
    run()
