# Feedback Categories

# When adding a new one, add the category to the available marksheet tuple
# to make sure it appears in the Module form.

AVAILABLE_MARKSHEETS = (
    ('PRESENTATION', 'Oral Presentation'),
    ('ESSAY', 'Essay'),
    ('LEGAL_PROBLEM', 'Legal Problem'),
)

CATEGORIES = {
    'PRESENTATION': {
        'title': 'Oral Presentation',
        'i_1': 'Understanding, Analysis and Content',
        'i_1_helptext': """<strong>80+</strong> Very full and perceptive awareness of socio-legal issues, with original, critical and analytic assessment of the issues and an excellent grasp of their wider significance. Balanced argument. Exceptionally well-argued. Excellent response to questions. In-depth analysis.<br><strong>70-79</strong>Comprehensive awareness of socio-legal issues and a clear grasp of their wider significance. Balanced argument. Well argued. Very good response to questions. Good critical analysis of issues<br><strong>60-69</strong>Very good awareness of socio-legal issues and a serious understanding of their wider significance. Balanced argument with evidence of some critical discussion. Good response to questions<br><strong>50-59</strong>Some awareness of issues and their wider significance. Clear argument. Limited critical discussion. Reasonable responses to questions<br><strong>40-49</strong>Limited awareness of issues and their wider significance. Argument not always clearly advanced. No critical discussion. Lack of understanding of key concepts, principles etc. Some difficulty in answering questions/response to questions limited<br><strong>30-39</strong>Very poor awareness of issues and of their wider significance, with incoherent argument and structure. Some major inaccuracies of information<br><strong>Below 30</strong>Unable to provide an adequate response to question posed with no evidence of an attempted argument & Incoherent argument lacking in structure, academic sources and application of material"""
    },
}
