from bs4 import BeautifulSoup
import click

class Screen:

    # helper methods
    def space(self, s, size):
        return ('{:'+str(size)+'}').format(str(s))
    
    def new_line(self):
        click.secho('')

    def print_success(self, text):
        click.secho(str(text), fg='bright_green')

    def print_fail(self, text):
        click.secho(str(text), fg='bright_red')

    def dash(self, s, size):
        return ('{:-<'+str(size)+'}').format(str(s))

    def print_difficulty(self, difficulty):
        if difficulty == 1 or difficulty == 'Easy':
            click.secho(self.space('Easy', 8), fg='bright_green', nl=False)
        if difficulty == 2 or difficulty == 'Medium':
            click.secho(self.space('Medium', 8), fg='bright_yellow', nl=False)
        if difficulty == 3 or difficulty == 'Hard':
            click.secho(self.space('Hard', 8), fg='bright_red', nl=False)
    
    def print_need_pay(self, need_pay):
        if need_pay:
            click.secho(self.space('$', 2), fg='bright_yellow', nl=False)
        else:
            click.secho(self.space('', 2), nl=False)

    def print_is_favor(self, is_favor):
        if is_favor:
            click.secho(self.space('❤', 2), fg='bright_magenta', nl=False)
        else:
            click.secho(self.space('', 2), nl=False)

    def print_status(self, status):
        if status == 'ac':
            click.secho(self.space('AC', 3), fg='bright_cyan', nl=False)
        else:
            click.secho(self.space('', 3), fg='bright_cyan', nl=False)
    
    def print_content(self, content):
        click.secho('', fg='bright_white')
        content =  BeautifulSoup(content, "html.parser")
        content = content.get_text().replace('Example:\n', '\nExample:')
        content = content.replace('Example 1:\n', '\nExample 1:')
        content = content.replace('Example 2:\n', '\nExample 2:')
        content = content.replace('Note:\n', '\nNote:')
        click.secho('Description:', fg='bright_blue')
        for line in content.splitlines():
            if line == 'Example:' or line == 'Note:' or line == 'Example 1:' or line == 'Example 2:':
                click.secho(line, fg='bright_blue')
            else:
                click.secho(line, fg='bright_white')
        click.secho('', fg='bright_white')

    def print_discussion_post_content(self, content):
        content = content.split('\\n')
        for line in content:
            click.secho(line, fg='bright_white')
            
    def print_likes_and_dislikes(self, likes, dislikes):
        click.secho(str(likes)+' ', fg='bright_green', nl=False)
        click.secho(self.space('likes', 6), fg='bright_green', nl=False)
        click.secho(str(dislikes)+' ', fg='bright_red', nl=False)
        click.secho(self.space('dislikes', 9), fg='bright_red', nl=False)

    def print_topic_tages(self, topic_tags):
        click.secho('Topic: ', nl=False, fg='blue')
        for topic_tag in topic_tags:
            click.secho('['+topic_tag['name']+'] ', nl=False, fg='bright_cyan')
        click.secho('')  

    def print_sample_testcase(self, testcase):
        click.secho('Sample Test Case:', fg='bright_blue')
        click.secho(testcase)

    def print_runtime(self, runtime, percentile):
        click.secho('Runtime: ', fg='bright_white', nl=False)
        click.secho(str(runtime)+', ', fg='bright_cyan', nl=False)
        click.secho('faster than ', fg='bright_white', nl=False)
        click.secho(str(int(percentile))+'%', fg='bright_cyan', nl=False)
        click.secho(' submissions', fg='bright_white')
    
    def print_memory(self, memory, percentile):
        click.secho('Memory Usage: ', fg='bright_white', nl=False)
        click.secho(str(memory)+', ', fg='bright_cyan', nl=False)
        click.secho('less than ', fg='bright_white', nl=False)
        click.secho(str(int(percentile))+'%', fg='bright_cyan', nl=False)
        click.secho(' submissions', fg='bright_white')

    def print_input(self, code_input):
        click.secho(self.space('Input:', 10)+str(code_input), fg='bright_white')

    def print_output(self, output):
        click.secho(self.space('Ouput:', 10)+str(output), fg='bright_white')
    
    def print_std_output(self, output):
        if output != None and output != '':
            click.secho(self.space('Stdout:', 10)+str(output), fg='bright_white')

    def print_expected(self, expected):
        click.secho(self.space('Expected:', 10)+str(expected), fg='bright_white')

    def print_discussion_title(self, title):
        title = title.split()
        key_words = ['java', 'c++', 'cpp', 'python', 'o(n)', 'o(nlogn)', 'o(logn)']
        for word in title:
            if word.lower() in key_words:
                click.secho(word+' ', fg='bright_green', nl=False)
            else:
                click.secho(word+' ', fg='bright_white', nl=False)

    # question methods
    def print_question_summarys(self, question_summarys):
        for question_summary in question_summarys:
            stat = question_summary['stat']
            
            question_id = self.space(str(stat['question_id']), 5)
            question_title = self.dash(stat['question__title'], 55)

            difficulty = question_summary['difficulty']['level']
            paid_only = question_summary['paid_only']
            is_favor = question_summary['is_favor']
            status = question_summary['status']
            
            click.secho(question_id, fg='bright_white', nl=False)
            click.secho(question_title, fg='bright_white', nl=False)
            self.print_difficulty(difficulty)
            self.print_need_pay(paid_only)
            self.print_is_favor(is_favor)
            self.print_status(status)
            click.secho('', fg='bright_white')

    def print_question_detail(self, question_detail):

        question_id = self.space(question_detail['questionId'] ,5)
        title = question_detail['title']+' '
        difficulty = question_detail['difficulty']

        likes = question_detail['likes']
        dislikes = question_detail['dislikes']

        status = question_detail['status']

        topicTags = question_detail['topicTags']

        content = question_detail['content']

        sampleTestCase = question_detail['sampleTestCase']

        click.secho('Question '+str(question_id), fg='bright_yellow')
        click.secho(title, fg='bright_cyan')

        self.print_difficulty(difficulty)
        self.print_likes_and_dislikes(likes, dislikes)
        self.print_status(status)
        click.secho('', fg='bright_white')

        self.print_topic_tages(topicTags)

        self.print_content(content)
        self.print_sample_testcase(sampleTestCase)

    # message
    def print_login_request_message(self):
        click.secho('Login:', fg='bright_white')

    def print_login_success_message(self):
        click.secho('Login success', fg='bright_white')

    def print_login_fail_message(self):
        click.secho('Login fail, try agin', fg='bright_white')

    def print_logout_success_message(self):
        click.secho('Logout success', fg='bright_white')

    def print_update_lang_message(self, lang):
        click.secho('Update language to '+lang, fg='bright_white')

    def print_generate_code_template_message(self, filename, lang):
        click.secho('Generate '+lang+' code template '+filename, fg='bright_white')

    def print_clean_message(self):
        click.secho('Clean cache success', fg='bright_white')
        
    # test results
    def print_compare_test_result(self, test_result, expected_test_result):
        status_code = test_result['status_code']
        

        if status_code == 10:
            code_answer = test_result['code_answer'][0]
            correct_answer = expected_test_result['code_answer'][0]
            if code_answer == correct_answer:
                self.print_success('Pass the test')
            else:
                self.print_fail('Fail the test')
            click.secho(self.space('Output:', 10), fg='bright_white', nl=False)
            click.secho(code_answer, fg='bright_white')
            click.secho(self.space('Expected:', 10), fg='bright_white', nl=False)
            click.secho(correct_answer, fg='bright_white')


        elif status_code == 20:
            self.print_fail('Compile Error')
            print(test_result['full_compile_error'])

        elif status_code == 14:
            self.print_fail('Runtime Error')
            print(test_result['runtime_error'])

        else:
            print('Unknown error')

    def print_submit_result(self, submit_result):
        status_code = submit_result['status_code']
        status_msg = submit_result['status_msg']

        if status_code == 10:
            status_runtime = submit_result['status_runtime']
            status_memory = submit_result['status_memory']
            runtime_percentile = submit_result['runtime_percentile']
            memory_percentile = submit_result['memory_percentile']
            self.print_success(status_msg)
            self.print_runtime(status_runtime, runtime_percentile)
            self.print_memory(status_memory, memory_percentile)

        elif status_code == 11:
            self.print_fail(status_msg)
            code_input = submit_result['input_formatted']
            std_output = submit_result['std_output']
            code_output = submit_result['code_output']
            expected_output = submit_result['expected_output']
            self.print_input(code_input)
            self.print_output(code_output)
            self.print_expected(expected_output)
            self.print_std_output(std_output)

        elif status_code == 14:
            self.print_fail(status_msg)
            last_testcase = submit_result['last_testcase'].replace('\n', ', ')
            std_output = submit_result['std_output']
            self.print_input(last_testcase)
            self.print_std_output(std_output)
            
        elif status_code == 20:
            self.print_fail(status_msg)
            full_compile_error = submit_result['full_compile_error']
            click.secho(full_compile_error, fg='bright_white')

        else:
            print('Unknown error')
            print(submit_result)

    def print_discussion_list(self, discussion_list):
        count = 1
        for discussion in discussion_list:
            title = discussion['node']['title']
            click.secho(self.space(count, 4), fg='bright_white', nl=False)
            self.print_discussion_title(title)
            self.new_line()
            count += 1

    def print_discussion_post(self, discussion_post):
        title = discussion_post['title']
        content = discussion_post['post']['content']
        click.secho(title, fg='bright_yellow')
        self.print_discussion_post_content(content)

    # create list
    def print_add_question_to_list_result(self, result, question_id):
        question_id = str(question_id)
        if 'errors' not in result:
            click.secho('Add question '+question_id+' success', fg='bright_green')
        else:
            click.secho('question '+question_id+' already exists ', fg='bright_red')

screen = Screen()