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
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
        st.session_state.answers = {}
        st.session_state.result = None

    def handle_answer(answer):
        st.session_state.answers[questions[st.session_state.current_question]['id']] = answer
        next_question = get_next_question(st.session_state.answers)
        if next_question:
            st.session_state.current_question = next((index for (index, q) in enumerate(questions) if q['id'] == next_question), None)
        else:
            st.session_state.result = get_recommended_test(st.session_state.answers)

    st.title("Statistical Test Selector")
    st.write("Answer the questions to find the right statistical test")

    if st.session_state.result:
        st.success(f"The recommended test is: {st.session_state.result}")
        if st.button('Start Over'):
            st.session_state.current_question = 0
            st.session_state.answers = {}
            st.session_state.result = None
    else:
        question = questions[st.session_state.current_question]
        st.write(question['text'])
        for option in question['options']:
            if st.button(option['label']):
                handle_answer(option['value'])
                st.experimental_rerun()

if __name__ == "__main__":
    main()


# Footer
st.markdown("""
    <div style="text-align: center; margin-top: 50px; padding: 10px; background-color: #0E1117; color: white;">
        Web app made by Bashar Hasan, MD
    </div>
""", unsafe_allow_html=True)
