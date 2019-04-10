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