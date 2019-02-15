from src.leetcode import leetcode
from src.config import SUCCESS, FAIL
from src.cache import cache
import os
path = os.path.dirname(os.path.abspath(__file__))+'/'

def test_login():
    leetcode.logout()
    assert leetcode.login('pyleetcodetest1', 'test1234') == SUCCESS
    leetcode.logout()
    assert leetcode.login('pyleetcodetest1', 'aaaa1234') == FAIL
    leetcode.logout()
    assert leetcode.login('adsgsdgasdfasdf', 'aaaa1234') == FAIL
    leetcode.logout()
    assert leetcode.login('adsgsdgasdfasdf', 'aaasdf34') == FAIL
    leetcode.logout()
    assert leetcode.login('pyleetcodetest2', 'test1234') == SUCCESS
    leetcode.logout()

def test_fetch_all_questions():
    leetcode.logout()
    assert leetcode.fetch_all_questions() == SUCCESS
    leetcode.logout()
    assert leetcode.login('pyleetcodetest1', 'test1234') == SUCCESS
    assert leetcode.fetch_all_questions() == SUCCESS
    leetcode.logout()

def test_fetch_question_detail():
    leetcode.logout()
    assert leetcode.fetch_question_detail('two-sum') == FAIL
    leetcode.logout()
    assert leetcode.login('pyleetcodetest1', 'test1234') == SUCCESS
    assert leetcode.fetch_question_detail('longest-substring-without-repeating-characters') == SUCCESS
    assert leetcode.fetch_question_detail('zigzag-conversion') == SUCCESS
    assert leetcode.fetch_question_detail('regular-expression-matching') == SUCCESS
    assert leetcode.fetch_question_detail('longest-common-prefix') == SUCCESS
    leetcode.logout()
    assert leetcode.fetch_question_detail('longest-substring-without-repeating-characters') == FAIL
    assert leetcode.fetch_question_detail('zigzag-conversion') == FAIL
    assert leetcode.fetch_question_detail('regular-expression-matching') == FAIL
    assert leetcode.fetch_question_detail('longest-common-prefix') == FAIL
    leetcode.logout()

def test_test():
    leetcode.logout()
    assert leetcode.test(path+'templates/1-two-sum.java') == FAIL
    assert leetcode.test(path+'templates/2-add-two-numbers.cpp') == FAIL
    assert leetcode.login('pyleetcodetest1', 'test1234') == SUCCESS
    assert leetcode.test(path+'templates/1-two-sum.java') == SUCCESS
    # assert leetcode.test(path+'templates/2-add-two-numbers.cpp') == SUCCESS
    leetcode.logout()