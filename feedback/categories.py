# Feedback Categories

# When adding a new one, add the category to the available marksheet tuple
# to make sure it appears in the Module form.

AVAILABLE_MARKSHEETS = (
    ('PRESENTATION', 'Oral Presentation'),
    ('ESSAY', 'Essay'),
    ('LEGAL_PROBLEM', 'Legal Problem'),
    ('MEDIATION_ROLE_PLAY', 'Mediation Role Play'),
    ('GROUP_PRESENTATION', 'Group Presentation'),
)

CATEGORIES = {
    'PRESENTATION': {
        'title': 'Oral Presentation',
        'number_of_categories': 3,
        'i-1': 'Understanding, Analysis and Content',
        'i-1-free': False,
        'i-1-helptext': "<strong>80+</strong> Very full and perceptive awareness of socio-legal issues, with original, critical and analytic assessment of the issues and an excellent grasp of their wider significance. Balanced argument. Exceptionally well-argued. Excellent response to questions. In-depth analysis.<br><strong>70-79</strong> Comprehensive awareness of socio-legal issues and a clear grasp of their wider significance. Balanced argument. Well argued. Very good response to questions. Good critical analysis of issues<br><strong>60-69</strong> Very good awareness of socio-legal issues and a serious understanding of their wider significance. Balanced argument with evidence of some critical discussion. Good response to questions<br><strong>50-59</strong> Some awareness of issues and their wider significance. Clear argument. Limited critical discussion. Reasonable responses to questions<br><strong>40-49</strong> Limited awareness of issues and their wider significance. Argument not always clearly advanced. No critical discussion. Lack of understanding of key concepts, principles etc. Some difficulty in answering questions/response to questions limited<br><strong>30-39</strong> Very poor awareness of issues and of their wider significance, with incoherent argument and structure. Some major inaccuracies of information<br><strong>Below 30</strong> Unable to provide an adequate response to question posed with no evidence of an attempted argument & Incoherent argument lacking in structure, academic sources and application of material",
        'i-2': 'Organisation and Application',
        'i-2-free': False,
        'i-2-helptext': "<strong>80+</strong> Exceptionally well-structured and well-planned presentation. Clear, coherent progression between points. Extensive range of academic sources used. Material applied to offer critical and persuasive analysis of issues<br><strong>70-79</strong> Very well structured and well-planned presentation. Clear progression between points. Wide range of academic sources used. Material applied to offer critical and persuasive analysis of issues<br><strong>60-69</strong> Well-structured and well organised presentation. Clear progression between points. Range of relevant academic sources used. Material applied to offer some critical analysis of issues<br><strong>50-59</strong> Generally well-structured and organised presentation. Progression between points. Some relevant academic sources used to offer analysis of issues<br><strong>40-49</strong> Poorly organised presentation. Little progression between points. Very few academic sources used. Limited application of material<br><strong>30-39</strong> A very poorly organised presentation lacking reference to relevant academic sources<br><strong>Below 30</strong> Incoherent argument lacking in structure, academic sources and application of material",
        'i-3': 'Delivery (including visual aid), Timing and Planning',
        'i-3-free': False,
        'i-3-helptext': "<strong>80+</strong> Excellent delivery of material, excellent eye contact. Confident. Engaging presentation delivered without the use of prompts. Well-paced, well-timed. Excellent use and range of visual aids<br><strong>70-79</strong> Very confident delivery of material, very good eye contact. Engaging presentation delivered without the use of prompts. Well-paced, well-timed. Very good use and range of visual aide. Visual aids clear, accurate and concise<br><strong>60-69</strong> Confident delivery of material, good eye contact. Engaging presentation delivered with limited use of prompts. Well-paced, well-timed. Good use and range of clear and reasonably concise visual aids<br><strong>50-59</strong> Good delivery of material, good eye contact. Over-reliance of prompts. Fair pace. Some engagement with audience. Visual aids too detailed or lacking in clarity with some errors<br><strong>40-49</strong> Limited eye contact. Presentation mainly delivered by reading from script. Very little engagement with audience. Limited use of visual aids. Visual aids unclear/poorly presented with a number of errors<br><strong>30-39</strong> No eye contact. Direct reading from script. Extremely limited attempt, or no attempt, to engage with the audience. Exceptionally poorly paced. Very limited use of visual aids. Visual aids very unclear/poorly presented with significant errors<br><strong>Below 30</strong> No eye contact with only direct reading from script. No engagement with audience. No structured pacing, no use of visual aids",
    },
    'ESSAY': {
        'title': 'Essay',
        'number_of_categories': 4,
        'i-1': 'Knowledge and Understanding',
        'i-1-free': False,
        'i-1-helptext': "<strong>80+</strong> Extensive reading and exceptional comprehensive knowledge<br><strong>70-79</strong> Wide reading and comprehensive knowledge<br><strong>60-69</strong> Good range of reading and adequate knowledge<br><strong>50-59</strong> Fair range of reading and reasonable knowledge<br><strong>40-49</strong> Limited reading and incomplete knowledge<br><strong>30-39</strong> Very limited reading and knowledge<br><strong>Below 30</strong> Very poor level of reading and failure to demonstrate competent knowledge",
        'i-2': 'Analysis',
        'i-2-free': False,
        'i-2-helptext': "<strong>80+</strong> Extremely full and perceptive awareness of issues, with original critical and analytic assessment of the issues and an excellent grasp of their wider significance<br><strong>70-79</strong> Full and perceptive awareness of issues and a clear grasp of their wider significance<br><strong>60-69</strong> Adequate awareness  of issues and a serious understanding of their wider significance<br><strong>50-59</strong> Some awareness of issues and their wider significance<br><strong>40-49</strong> Limited awareness of issues and of their wider significance<br><strong>30-39</strong> Very limited awareness of issues and of their wider significance<br><strong>Below 30</strong> Very poor awareness of issues and of their wider significance, and fails to demonstrate competent understanding",
        'i-3': 'Argument',
        'i-3-free': False,
        'i-3-helptext': "<strong>80+</strong> Clear evidence of independent and original thought and the ability to defend a position logically and convincingly, with arguments presented that are sophisticated and highly challenging<br><strong>70-79</strong> Clear evidence of independent thought and the ability to defend a position logically and convincingly<br><strong>60-69</strong> A well-developed argument<br><strong>50-59</strong> Some evidence of thought with a serious attempt at an argument<br><strong>40-49</strong> Limited thought and very meagre argument<br><strong>30-39</strong> Very limited thought and very meagre argument<br><strong>Below 30</strong> Lack of thought, and a lack of or irrelevant argumentation",
        'i-4': 'Presentation and Organisation',
        'i-4-free': False,
        'i-4-helptext': "<strong>80+</strong> Excellent arrangement and development of material and argument, where the material has been handled with great dexterity.<br>The work will be in excellent English and the presentation meticulous, with immaculate footnotes and extensive bibliography<br><strong>70-79</strong> Careful thought has been given to the arrangement and development of material and argument. The work will be in excellent English with appropriate footnotes and comprehensive bibliography<br><strong>60-69</strong> Adequate arrangement and development of material and argument. The work will be in good English with appropriate footnotes and bibliography<br><strong>50-59</strong> Effort to organise the material and argument. The work will be in adequate English with reasonable footnoting and a bibliography<br><strong>40-49</strong> Limited effort to organise material and argument. The work generally will be in satisfactory English but with limited footnoting and bibliography<br><strong>30-39</strong> Very little effort at organising the material. The work will show significant errors in English and have poor footnoting and bibliography<br><strong>Below 30</strong> A lack of organisation of the material. The work will show substantial errors in English and have very poor or a lack of footnoting and bibliography",
    },
    'LEGAL_PROBLEM': {
        'title': 'Legal Problem',
        'number_of_categories': 4,
        'i-1': 'Issue Identification',
        'i-1-free': False,
        'i-1-helptext': "<strong>80+</strong> Identification of all core issues and almost all peripheral issues<br><strong>70-79</strong> Identification of all core issues and most peripheral issues<br><strong>60-69</strong> Identification of all (or nearly all) core issues<br><strong>50-59</strong> Identification of at least half the core issues<br><strong>40-49</strong> Identification of some core issues<br><strong>30-39</strong> Identification of very few issues<br><strong>Below 30</strong> No issues are correctly identified",
        'i-2': 'Rule Identification',
        'i-2-free': False,
        'i-2-helptext': "<strong>80+</strong> Identification of all applicable rules<br><strong>70-79</strong> Identification of nearly all applicable legal rules<br><strong>60-69</strong> Identification of most applicable primary and some legal rules<br><strong>50-59</strong> Identification of a substantial number of applicable legal rules<br><strong>40-49</strong> Identification of some applicable legal rules<br><strong>30-39</strong> Identification of very few applicable legal rules<br><strong>Below 30</strong> No identification of applicable legal rules",
        'i-3': 'Analysis and Application of Law',
        'i-3-free': False,
        'i-3-helptext': "<strong>80+</strong> Excellent issue analysis: an in-depth understanding and application of legal principles, cases and legislation, going beyond the main authorities and legislation<br><strong>70-79</strong> Very good issue analysis and understanding with an application of legal principles, cases and legislation, going beyond the main authorities and legislation<br><strong>60-69</strong> Good issue analysis and understanding of legal principles and effective use of main authorities and legislation<br><strong>50-59</strong> Fair issue analysis which goes beyond a descriptive account, with some understanding of relevant legal principles and some use of main authorities and legislation<br><strong>40-49</strong> Issue analysis mainly descriptive with very little application of legal principles, cases or legislation<br><strong>30-39</strong> Unclear application of the law to the facts, lacking in issue analysis<br><strong>Below 30</strong> Failure to demonstrate the ability to apply the law and no issue analysis",
        'i-4': 'Structure and Presentation',
        'i-4-free': False,
        'i-4-helptext': "<strong>80+</strong> Excellent, clear and coherent structure for the analysis of the legal problem which facilitates an in-depth analysis of the issues<br><strong>70-79</strong> Very clear structure for the analysis of legal problem which facilitates analysis of the issues<br><strong>60-69</strong> Clear and concise structure for the analysis of legal problem allowing analysis of issues identified<br><strong>50-59</strong> Clear structure with somewhat less clear style for the analysis of legal problem; or clear style with slightly less clear structure for the analysis of legal problem<br><strong>40-49</strong> Confused structure for analysis of legal problem, but an argument does come across; or the structure is adequate, but the style is such that meaning is not adequately conveyed<br><strong>30-39</strong> Structure is virtually non-existent and so obscures meaning and/or presentation is unclear<br><strong>Below 30</strong> Lack of structure and/or a style which leads to a lack of coherent meaning and to a lack of coherency in the presentation of the law", 
    },
    'MEDIATION_ROLE_PLAY': {
        'title': 'Mediation Role-Play',
        'number_of_categories': 3,
        'i-1': 'Relationship Skills',
        'i-1-free': True,
        'i-1-helptext': "Show skills to create an environment conducive to mediation (i.e. setting of scene, tone, etc.). Build confidence and trust with parties. Develop communication and interaction with the parties",
        'i-2': 'Process Knowledge',
        'i-2-free': True,
        'i-2-helptext': "Knowledge of the process. Understanding of the process/phases of mediation. Establishment and maintenance of a working structure.",
        'i-3': 'Teamwork',
        'i-3-free': True,
        'i-3-helptext': "The preparation undertaken for the mediation. The relationship developed between the co-mediators. Effectiveness in working as a team; sharing responsibility and providing mutual support.",
    },
    'GROUP_PRESENTATION': {
        'title': 'Group Presentation',
        'number_of_categories': 5,  # Only individual categories
        'number_of_individual_categories': 3,
        'number_of_group_categories': 2,
        'split': (10, 90),  # (Group mark weighting, individual mark weighting)
        'i-1': 'Understanding, Analysis and Content',
        'i-1-free': False,
        'i-1-helptext': "<strong>80+</strong> Very full and perceptive awareness of socio-legal issues, with original, critical and analytic assessment of the issues and an excellent grasp of their wider significance. Balanced argument. Exceptionally well-argued. Excellent response to questions. In-depth analysis.<br><strong>70-79</strong> Comprehensive awareness of socio-legal issues and a clear grasp of their wider significance. Balanced argument. Well argued. Very good response to questions. Good critical analysis of issues<br><strong>60-69</strong> Very good awareness of socio-legal issues and a serious understanding of their wider significance. Balanced argument with evidence of some critical discussion. Good response to questions<br><strong>50-59</strong> Some awareness of issues and their wider significance. Clear argument. Limited critical discussion. Reasonable responses to questions<br><strong>40-49</strong> Limited awareness of issues and their wider significance. Argument not always clearly advanced. No critical discussion. Lack of understanding of key concepts, principles etc. Some difficulty in answering questions/response to questions limited<br><strong>30-39</strong> Very poor awareness of issues and of their wider significance, with incoherent argument and structure. Some major inaccuracies of information<br><strong>Below 30</strong> Unable to provide an adequate response to question posed with no evidence of an attempted argument & Incoherent argument lacking in structure, academic sources and application of material",
        'i-2': 'Organisation and Application',
        'i-2-free': False,
        'i-2-helptext': "<strong>80+</strong> Exceptionally well-structured and well-planned presentation. Clear, coherent progression between points. Extensive range of academic sources used. Material applied to offer critical and persuasive analysis of issues<br><strong>70-79</strong> Very well structured and well-planned presentation. Clear progression between points. Wide range of academic sources used. Material applied to offer critical and persuasive analysis of issues<br><strong>60-69</strong> Well-structured and well organised presentation. Clear progression between points. Range of relevant academic sources used. Material applied to offer some critical analysis of issues<br><strong>50-59</strong> Generally well-structured and organised presentation. Progression between points. Some relevant academic sources used to offer analysis of issues<br><strong>40-49</strong> Poorly organised presentation. Little progression between points. Very few academic sources used. Limited application of material<br><strong>30-39</strong> A very poorly organised presentation lacking reference to relevant academic sources<br><strong>Below 30</strong> Incoherent argument lacking in structure, academic sources and application of material",
        'i-3': 'Delivery (including visual aid), Timing and Planning',
        'i-3-free': False,
        'i-3-helptext': "<strong>80+</strong> Excellent delivery of material, excellent eye contact. Confident. Engaging presentation delivered without the use of prompts. Well-paced, well-timed. Excellent use and range of visual aids<br><strong>70-79</strong> Very confident delivery of material, very good eye contact. Engaging presentation delivered without the use of prompts. Well-paced, well-timed. Very good use and range of visual aide. Visual aids clear, accurate and concise<br><strong>60-69</strong> Confident delivery of material, good eye contact. Engaging presentation delivered with limited use of prompts. Well-paced, well-timed. Good use and range of clear and reasonably concise visual aids<br><strong>50-59</strong> Good delivery of material, good eye contact. Over-reliance of prompts. Fair pace. Some engagement with audience. Visual aids too detailed or lacking in clarity with some errors<br><strong>40-49</strong> Limited eye contact. Presentation mainly delivered by reading from script. Very little engagement with audience. Limited use of visual aids. Visual aids unclear/poorly presented with a number of errors<br><strong>30-39</strong> No eye contact. Direct reading from script. Extremely limited attempt, or no attempt, to engage with the audience. Exceptionally poorly paced. Very limited use of visual aids. Visual aids very unclear/poorly presented with significant errors<br><strong>Below 30</strong> No eye contact with only direct reading from script. No engagement with audience. No structured pacing, no use of visual aids",
        'g-1': 'Structure and Organisation',
        'g-1-free': False,
        'g-1-helptext': '',
        'g-2': 'Delivery and Supporting Material',
        'g-2-free': False,
        'g-2-helptext': '',
    },
}

# "<strong>80+</strong> <br><strong>70-79</strong> <br><strong>60-69</strong> <br><strong>50-59</strong> <br><strong>40-49</strong> <br><strong>30-39</strong> <br><strong>Below 30</strong> ",
