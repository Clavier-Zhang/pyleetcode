from src.system import system
import os
path = os.path.dirname(os.path.abspath(__file__))+'/'

def test_get_lang_from_filename():
    assert system.get_lang_from_filename('1-two-sum.java') == 'java'
    assert system.get_lang_from_filename('./templates/1-two-sum.java') == 'java'
    assert system.get_lang_from_filename('../templates/1-two-sum.cpp') == 'cpp'
    assert system.get_lang_from_filename('1112-two-sum.java') == 'java'
    assert system.get_lang_from_filename('../templates/1111-two-sum.cpp') == 'cpp'

def test_get_question_id_from_filename():
    assert system.get_question_id_from_filename('1-two-sum.java') == '1'
    assert system.get_question_id_from_filename('1123-two-sum.java') == '1123'
    assert system.get_question_id_from_filename('./1-two-sum.java') == '1'
    assert system.get_question_id_from_filename('./12312-two-sum.java') == '12312'
    assert system.get_question_id_from_filename('../asd/test/1-two-sum.java') == '1'
    assert system.get_question_id_from_filename('../../test/1-two-sum.java') == '1'
    assert system.get_question_id_from_filename('../templates/1111-two-sum.cpp') == '1111'

def test_get_test_case():
    assert system.get_test_case(path+'templates/1-two-sum.java') == '[2,7,11,15]\n9\n'
    assert system.get_test_case(path+'templates/2-add-two-numbers.cpp') == '[2,4,3]\n[5,6,4]\n'
    assert system.get_test_case(path+'templates/3-longest-substring-without-repeating-characters.cpp') == '"abcabcbb"\n'
    assert system.get_test_case(path+'templates/4-median-of-two-sorted-arrays.cpp') == '[1,3]\n[2]\n'
    assert system.get_test_case(path+'templates/5-longest-palindromic-substring.java') == '"babad"\n'

def test_get_solution():
    assert system.get_solution(path+'templates/1-two-sum.java') == 'class Solution {\n    public int[] twoSum(int[] nums, int target) {\n        int[] result = new int[2];\n        if (nums == null || nums.length < 2) return result;\n        Map<Integer,Integer> m = new HashMap();\n        for (int i = 0; i < nums.length; i++) {\n            if (m.containsKey(target-nums[i])) {\n                result[0] = m.get(target-nums[i]);\n                result[1] = i;\n                return result;\n            }\n            m.put(nums[i], i);\n        }\n        return result;\n    }\n}\n'
    assert system.get_solution(path+'templates/2-add-two-numbers.cpp') == '/**\n * Definition for singly-linked list.\n * struct ListNode {\n *     int val;\n *     ListNode *next;\n *     ListNode(int x) : val(x), next(NULL) {}\n * };\n */\nclass Solution {\npublic:\n    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {\n        \n    }\n};\n'