import stackexchange
import re
import html
import itertools

max_requests_per_run = 20
api_key = 'R91Ul6Hz*Reptmjm52BPHQ(('
so = stackexchange.Site(stackexchange.StackOverflow, api_key)
so.include_body = True


def fetch_code_blocks(searchterms, max_requests=None):
    """
    loads stack overflow questions,
    and extracts all code blocks contained therein.
    yields [(source1, codeblock1), ..., (sourceM, codeblockM)]
    """
    tags = ["C#"]
    questions = so.search(intitle=searchterms, tagged=';'.join(tags))
    if max_requests:
        # we only want to load max_requests - 1 questions since we already used
        # one for the search.
        questions = questions[:max_requests-1]
    for q in questions:
        q.fetch()
        for source in q.answers + [q]:
            found = re.findall(r'<code>(.*?)</code>', source.body, re.DOTALL)
            found = map(html.unescape, found)
            yield from [(source, c) for c in found]


def test_code_block(block, tests):
    """
    Try to mangle the code block into something that compiles & runs then check
    the test cases against it. If it worked return the source code string that
    successfully passed the tests. Otherwise return None.
    """
    return "just kidding"


def run():
    keywords = input('keywords: ').split()
    tests = []
    print('now enter test cases for the desired function f (e.g. f(3) == 42)')
    for i in itertools.count():
        expr = input('test case {}: '.format(i+1))
        if expr.strip() == 'q':
            break
        tests.append(expr)

    for block in fetch_code_blocks(keywords, max_requests_per_run):
        result = test_code_block(block, tests)
        if result is not None:
            print('=== We did it! ===')
            print(result)
            break


if __name__ == '__main__':
    run()
