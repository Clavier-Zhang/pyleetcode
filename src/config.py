SUCCESS = True
FAIL = False

lang_dict = {
    'java': 'java',
    'cpp': 'cpp',
    'python': 'py',
    'python3': 'py',
    'c': 'c',
    'csharp': 'cs',
    'javascript': 'js',
    'ruby': 'rb',
    'swift': 'swift',
    'golang': 'go',
    'scala': 'scala',
    'kotlin': 'kt',
    'rust': 'rs',
    'php': 'php'
}

urls = {
    'base': 'https://leetcode.com',
    'login': 'https://leetcode.com/accounts/login/',
    'graphql': 'https://leetcode.com/graphql',
    'submit': 'https://leetcode.com/problems/add-two-numbers/submit/',
    'all_questions': 'https://leetcode.com/api/problems/algorithms/',
    'test': 'https://leetcode.com/problems/add-two-numbers/interpret_solution/',
    'check': 'https://leetcode.com/submissions/detail/$ID/check/',
    'company_tags': 'https://leetcode.com/problems/api/tags/'
}

querys = {
    'question_detail': '''
        query questionData($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionId
                title
                content
                difficulty
                likes
                dislikes
                status
                similarQuestions
                topicTags {
                    name
                    slug
                }
                codeSnippets {
                    lang
                    langSlug
                    code
                }
                sampleTestCase
            }
        }
    ''',
    'discussion_list': '''
        query questionTopicsList($questionId: String!, $orderBy: TopicSortingOption, $skip: Int, $query: String, $first: Int!, $tags: [String!]) {
            questionTopicsList(questionId: $questionId, orderBy: $orderBy, skip: $skip, query: $query, first: $first, tags: $tags) {
                ...TopicsList
            }
        }
        fragment TopicsList on TopicConnection {
            totalNum
            edges {
                node {
                    id
                    title
                    viewCount
                    post {
                        id
                        voteCount
                    }
                }
            }
        }
    ''',
    'discussion_post': '''
        query DiscussTopic($topicId: Int!) {
            topic(id: $topicId) {
                id
                viewCount
                topLevelCommentCount
                title
                post {
                    ...DiscussPost
                }
            }
        }
        fragment DiscussPost on PostNode {
            id
            voteCount
            voteStatus
            content
        }
    ''',
    'create_list': '''
        mutation addQuestionToNewFavorite($name: String!, $isPublicFavorite: Boolean!, $questionId: String!) {
            addQuestionToNewFavorite(name: $name, isPublicFavorite: $isPublicFavorite, questionId: $questionId) {
                ok
                error
                name
                isPublicFavorite
                favoriteIdHash
                questionId
                __typename
            }
        }
    ''',
    'fetch_lists': '''
        query allFavorites {
            favoritesLists {
                allFavorites {
                idHash
                name
                isPublicFavorite
                questions {
                    questionId
                    __typename
                }
                __typename
                }
                officialFavorites {
                idHash
                name
                questions {
                    questionId
                    __typename
                }
                __typename
                }
                __typename
            }
        }
    ''',
    'remove_from_list': '''
        mutation removeQuestionFromFavorite($favoriteIdHash: String!, $questionId: String!) {
            removeQuestionFromFavorite(favoriteIdHash: $favoriteIdHash, questionId: $questionId) {
                ok
                error
                favoriteIdHash
                questionId
            }
        }
    ''',
    'add_to_list': '''
        mutation addQuestionToFavorite($favoriteIdHash: String!, $questionId: String!) {
            addQuestionToFavorite(favoriteIdHash: $favoriteIdHash, questionId: $questionId) {
                ok
                error
                favoriteIdHash
                questionId
            }
        }
    ''',
    'fetch_company_encounter_count': '''
        query questionData($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionId
                titleSlug
                companyTagStats
            }
        }
    '''
}

leet_clean_help_msg      = """\b leet clean                          leet clean
"""
leet_login_help_msg      = """\b leet login                          leet login
"""
leet_logout_help_msg     = """\b leet logout                         leet logout
"""
leet_lang_help_msg       = """\b leet lang <language>                leet lang java
"""
leet_start_help_msg      = """\b leet start <question_id>            leet start 1
"""
leet_detail_help_msg     = """\b leet detail <question_id>           leet detail 1
"""
leet_submit_help_msg     = """\b leet submit <filename>              leet submit 1-two-sum.java
"""
leet_test_help_msg       = """\b leet test <filename>                leet test 1-two-sum.java
"""
leet_show_help_msg       = """\b leet show <start> <end>             leet show 1 50
"""
leet_diss_help_msg       = """\b leet diss <question_id> <ranking>   leet diss 1
"""
leet_create_help_msg     = """\b leet create <company> <start> <end> leet create google 1 50
"""
leet_contribute_help_msg = """\b leet contribute                     leet contribute\b
"""