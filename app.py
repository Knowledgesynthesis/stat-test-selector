import streamlit as st

questions = [
    {
        'id': 'purpose',
        'text': 'What is the purpose of your analysis?',
        'options': [
            {'value': 'compare', 'label': 'Compare a difference'},
            {'value': 'relationship', 'label': 'Check a relationship/association'},
            {'value': 'predict', 'label': 'Predict one variable from another (regression)'}
        ]
    },
    {
        'id': 'datatype',
        'text': 'What type of data are you working with?',
        'options': [
            {'value': 'continuous', 'label': 'Continuous'},
            {'value': 'ordinal', 'label': 'Ordinal'},
            {'value': 'nominal', 'label': 'Nominal'}
        ]
    },
    {
        'id': 'parametric',
        'text': 'Is your data parametric or nonparametric?',
        'options': [
            {'value': 'parametric', 'label': 'Parametric'},
            {'value': 'nonparametric', 'label': 'Nonparametric'}
        ]
    },
    {
        'id': 'groups',
        'text': 'How many groups are you comparing?',
        'options': [
            {'value': 'one', 'label': 'One group'},
            {'value': 'two', 'label': 'Two groups'},
            {'value': 'more', 'label': 'More than two groups'}
        ]
    },
    {
        'id': 'paired',
        'text': 'Are the data paired or unpaired?',
        'options': [
            {'value': 'paired', 'label': 'Paired'},
            {'value': 'unpaired', 'label': 'Unpaired'}
        ]
    }
]

decision_tree = {
    'compare': {
        'continuous': {
            'parametric': {
                'one': 'One sample t-test',
                'two': {
                    'paired': 'Paired t-test',
                    'unpaired': 'Unpaired t-test'
                },
                'more': {
                    'paired': 'Repeated-measures ANOVA',
                    'unpaired': 'One-way ANOVA'
                }
            },
            'nonparametric': {
                'one': 'Wilcoxon signed-rank',
                'two': {
                    'paired': 'Wilcoxon signed-rank',
                    'unpaired': 'Wilcoxon-Mann-Whitney'
                },
                'more': {
                    'paired': 'Friedman',
                    'unpaired': 'Kruskal-Wallis'
                }
            }
        },
        'ordinal': {
            'one': 'Sign test',
            'two': {
                'paired': 'Sign test',
                'unpaired': 'Wilcoxon-Mann-Whitney'
            },
            'more': {
                'paired': 'Friedman',
                'unpaired': 'Kruskal-Wallis'
            }
        },
        'nominal': {
            'one': 'Chi-square goodness-of-fit',
            'two': {
                'paired': 'McNemar',
                'unpaired': 'Chi-square test of homogeneity'
            },
            'more': {
                'paired': "Cochran's Q test",
                'unpaired': 'Chi-square test'
            }
        }
    },
    'relationship': {
        'continuous': {
            'parametric': 'Pearson correlation',
            'nonparametric': 'Spearman correlation'
        },
        'ordinal': 'Spearman correlation',
        'nominal': {
            'one': 'Chi-square goodness-of-fit',
            'two': {
                'paired': 'McNemar',
                'unpaired': 'Chi-square test of independence'
            },
            'more': {
                'paired': "Cochran's Q test",
                'unpaired': 'Chi-square test'
            }
        }
    },
    'predict': {
        'continuous': {
            'parametric': 'Linear regression',
            'nonparametric': 'Nonparametric regression'
        },
        'ordinal': 'Nonparametric regression',
        'nominal': 'Logistic regression'
    }
}

def get_next_question(answers):
    if not answers.get('datatype'):
        return 'datatype'
    if answers['purpose'] == 'compare':
        if answers['datatype'] == 'continuous' and not answers.get('parametric'):
            return 'parametric'
        if not answers.get('groups'):
            return 'groups'
        if answers['groups'] != 'one' and not answers.get('paired'):
            return 'paired'
    if answers['purpose'] == 'relationship':
        if answers['datatype'] == 'continuous' and not answers.get('parametric'):
            return 'parametric'
        if answers['datatype'] == 'nominal':
            if not answers.get('groups'):
                return 'groups'
            if answers['groups'] != 'one' and not answers.get('paired'):
                return 'paired'
    if answers['purpose'] == 'predict':
        if answers['datatype'] == 'continuous' and not answers.get('parametric'):
            return 'parametric'
    return None

def get_recommended_test(answers):
    result = decision_tree[answers['purpose']]
    result = result[answers['datatype']]
    if isinstance(result, dict):
        result = result.get(answers.get('parametric', ''), result)
    if isinstance(result, dict):
        result = result.get(answers.get('groups', ''), result)
    if isinstance(result, dict):
        result = result.get(answers.get('paired', ''), result)
    return result if isinstance(result, str) else 'No specific test found for this combination'

def main():
    st.title("Statistical Test Selector")
    st.write("Answer the questions to find the right statistical test")

    answers = {}
    for question in questions:
        options = [opt['label'] for opt in question['options']]
        answer = st.radio(question['text'], options, key=question['id'])
        value = next(opt['value'] for opt in question['options'] if opt['label'] == answer)
        answers[question['id']] = value

        next_question = get_next_question(answers)
        if next_question and next_question != question['id']:
            st.stop()

    test = get_recommended_test(answers)
    st.success(f"The recommended test is: {test}")

if __name__ == "__main__":
    main()
