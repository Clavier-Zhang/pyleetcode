
from .cache import cache
from .leetcode import leetcode
from .system import system
from .config import lang_dict
from .screen import screen
from .lru_cache import lru
import click

class Client:

    def check_login(self):
        if (not cache.check_user_account_statue()):
            self.login()
        if (not cache.check_user_token_statue()):
            if not self.update_token():
                self.login()

    def login(self):
        while True:
            username = click.prompt('Please enter your username')
            password = click.prompt('Please enter your password', hide_input=True)
            cache.save_username_and_password(username, password)
            if leetcode.login(username, password):
                screen.print_login_success_message()
                break
            else:
                screen.print_login_fail_message()

    def logout(self):
        cache.clear_user()
        screen.print_logout_success_message()

    def update_token(self):
        username = cache.get_user_username()
        password = cache.get_user_password()
        return leetcode.login(username, password)

    def set_coding_language(self, lang):
        cache.save_user_lang(lang)
        screen.print_update_lang_message(lang)

    # question methods
    def submit(self, filename):
        lang = system.get_lang_from_filename(filename)
        question_id = system.get_question_id_from_filename(filename)
        typed_code = system.get_solution(filename)
        result = leetcode.submit(lang, question_id, typed_code)
        screen.print_submit_result(result)

    def show(self, start, end):
        screen.print_question_summarys(cache.get_question_summarys_by_range(start, end))

    def detail(self, question_id):
        question_detail = self.get_question_detail(question_id)
        screen.print_question_detail(question_detail)

    def check_lang(self):
        while not cache.check_user_lang_status():
            lang = click.prompt('Please enter your preferred language')
            if lang not in lang_dict:
                print('does not support this language')
            else:
                cache.save_user_lang(lang)

    def check_question_list(self):
        if not cache.check_question_index_status():
            leetcode.fetch_all_questions()

    def get_question_detail(self, question_id):
        question_slug = cache.question_id_to_question_slug(question_id)
        question_detail = lru.get(str(question_id)+'_detail')
        if question_detail == None:
            question_detail = leetcode.fetch_question_detail(question_slug)
            lru.put(str(question_id)+'_detail', question_detail)
        return question_detail

    def create_template(self, question_id):
        question_slug = cache.question_id_to_question_slug(question_id)
        question_detail = self.get_question_detail(question_id)
        code_templates = question_detail['codeSnippets']
        sample_test_case = question_detail['sampleTestCase']
        for code_template in code_templates:
            if code_template['langSlug'] == cache.get_user_lang():
                filename = str(question_id)+'-'+question_slug
                lang = cache.get_user_lang()
                system.generate_code_file(filename, lang, code_template['code'], sample_test_case)
                screen.print_generate_code_template_message(filename, lang)

    def test(self, filename):
        data_input = system.get_test_case(filename)
        lang = system.get_lang_from_filename(filename)
        question_id = system.get_question_id_from_filename(filename)
        typed_code = system.get_solution(filename)
        test_result, expected_test_result = leetcode.test(data_input, lang, question_id, typed_code)
        screen.print_compare_test_result(test_result, expected_test_result)

    def clean(self):
        cache.clean()
        screen.print_clean_message()

    def disscussion_list(self, question_id):
        discussion_list = leetcode.fetch_discussion_by_question_id(question_id)
        screen.print_discussion_list(discussion_list)

    def disscussion_post(self, question_id, rank):
        discussion_list = leetcode.fetch_discussion_by_question_id(question_id)
        post_ids = []
        for discussion in discussion_list:
            post_ids.append(discussion['node']['id'])
        discussion_post = leetcode.fetch_discussion_post(post_ids[rank-1])
        screen.print_discussion_post(discussion_post)

    def create_company_list(self, company, start, end):
        company_questions = cache.get_company_questions(company)
        if end > len(company_questions):
            print('The range exceeds the length of '+company+' questions')
            print(company+' questions length: '+str(len(company_questions)))
            return
        question_ids = company_questions[start-1:end]
        leetcode.add_all_question_to_list(question_ids, company+'-top-'+str(start)+'-'+str(end))

    def contribute(self):
        company_tags = leetcode.fetch_all_company_tags(1, 1200)
        company_frequency_ranking = {}
        for company_slug in cache.get_company_slugs():
            targets = list(filter(lambda elem : company_slug in elem, company_tags))
            targets.sort(key=lambda elem : elem[company_slug], reverse=True)
            ranking = []
            for target in targets:
                ranking.append(target['question_id'])
            company_frequency_ranking[company_slug] = ranking
        company_frequency_ranking['frequency'] = leetcode.fetch_frequency_list()
        cache.save_company_frequency_ranking(company_frequency_ranking)

client = Client()