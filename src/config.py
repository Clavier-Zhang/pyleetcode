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
}