import stackexchange
import re
import html
import itertools
import subprocess
import sys


max_requests_per_run = 20
api_key = 'R91Ul6Hz*Reptmjm52BPHQ(('
so = stackexchange.Site(stackexchange.StackOverflow, api_key)
so.include_body = True


languages = {
    'C#old': (['C#'], 'testcsharp.exe'),
    'C#' : (['C#'], 'roslyn_csharp.exe')
}


def fetch_code_blocks(lang, searchterms, max_requests=None):
    """
    loads stack overflow questions,
    and extracts all code blocks contained therein.
    yields [(source1, codeblock1), ..., (sourceM, codeblockM)]
    """
    tags, _ = languages[lang]
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


def test_code_block(lang, block, regex, tests):
    """
    Try to mangle the code block into something that compiles & runs then check
    the test cases against it. If it worked return the source code string that
    successfully passed the tests. Otherwise return None.
    """
    _, runstring = languages[lang]

    if sys.platform in ['linux', 'linux2', 'darwin']:
        runstring = './' + runstring
    else:
        runstring = runstring

    proc = subprocess.Popen([runstring, block, regex], stdout=subprocess.PIPE,
                                                       stderr=subprocess.PIPE)
    out, err = proc.communicate()
    if proc.returncode == 0:
        return out
    else:
        return None


def run():
    lang = input('language: ')
    if lang not in languages:
        print('error: not a known language')
        return

    keywords = input('keywords: ').split()

    regex = input('now enter a regex the console output must match: ')

    tests = []
    print('now enter test cases for the desired function f (e.g. f(3) == 42)')
    for i in itertools.count():
        expr = input('test case {}: '.format(i+1))
        if expr.strip() == 'q':
            break
        tests.append(expr)

    for src, block in fetch_code_blocks(lang, keywords, max_requests_per_run):
        result = test_code_block(lang, block, regex, tests)
        if result is not None:
            result = result.decode('utf-8')
            print('// url: {}'.format(src.url))
            print('// code:\n{}'.format(result))
            break


if __name__ == '__main__':
    run()
