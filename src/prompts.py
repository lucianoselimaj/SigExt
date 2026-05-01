ZS_NAIVE_PROMPT_STR_FOR_MISTRAL = {
    "cnn": "<s>[INST]Here is a news article:\n<text>\n\n"
    "Please write a short summary for the article in 1-2 sentences.[/INST]",
    "arxiv": "<s>[INST]Here is a research paper:\n<text>\n\n"
    "Please write a short abstract in about 3 sentences.[/INST]",
    "pubmed": "<s>[INST]Here is a research paper:\n<text>\n\n"
    "Please write a short abstract in about 3 sentences.[/INST]",
    "samsum": "<s>[INST]Here is a conversation:\n<text>\n\n" "Please write a short 1 sentence summary. [/INST]",
    "meetingbank": "<s>[INST]Here is a conversation:\n<text>\n\n" "Please write a 2-3 sentence summary. [/INST]",
}

ZS_NAIVE_PROMPT_STR_FOR_CLAUDE = {
    "cnn": "Here is a news article:\n<text>\n\nPlease write a summary for the article in 2-3 sentences.",
    "arxiv": "Here is a research paper:\n<text>\n\nPlease write a comprehensive paper abstract section.",
    "pubmed": "Here is a research paper:\n<text>\n\nPlease write a paper abstract in around 5 sentences.",
    "samsum": "Here is a conversation:\n<text>\n\nPlease write a very short 1 sentence summary.",
    "meetingbank": "Here is a conversation:\n<text>\n\nPlease write a summary in about 5 sentences.",
}

ZS_KEYWORD_PROMPT_STR_FOR_MISTRAL = {
    "cnn": "<s>[INST]Here is a news article:\n<text>\n\n"
    "Please write a short summary for the article in 1-2 sentences. "
    "Consider include the following information: <keywords>[/INST]",
    "arxiv": "<s>[INST]Here is a research paper:\n<text>\n\n"
    "Please write a short abstract in about 3 sentences. "
    "Consider include the following information: <keywords>[/INST]",
    "pubmed": "<s>[INST]Here is a research paper:\n<text>\n\n"
    "Please write a short abstract in about 3 sentences. "
    "Consider include the following information: <keywords>[/INST]",
    "samsum": "<s>[INST]Here is a conversation:\n<text>\n\n"
    "Please write a short 1 sentence summary. "
    "Consider include the following information: <keywords>[/INST]",
    "meetingbank": "<s>[INST]Here is a conversation:\n<text>\n\n"
    "Please write a 2-3 sentence summary. "
    "Consider include the following information: <keywords>[/INST]",
}


ZS_KEYWORD_PROMPT_STR_FOR_CLAUDE = {
    "cnn": "Here is a news article:\n<text>\n\n"
    "Please write a summary for the article in 2-3 sentences. "
    "Consider include the following information: <keywords>.",
    "arxiv": "Here is a research paper:\n<text>\n\n"
    "Please write a comprehensive paper abstract section."
    "Consider include the following information: <keywords>.",
    "pubmed": "Here is a research paper:\n<text>\n\n"
    "Please write a paper abstract in around 5 sentences. "
    "Consider include the following information: <keywords>.",
    "samsum": "Here is a conversation:\n<text>\n\n"
    "Please write a very short 1 sentence summary. "
    "Consider include the following information: <keywords>",
    "meetingbank": "Here is a conversation:\n<text>\n\n"
    "Please write a summary in about 5 sentences. "
    "Consider include the following information: <keywords>",
}


CRITIC_KEYWORD_PROMPT_STR_FOR_MISTRAL = {
    "cnn": "<s>[INST]You are a rigorous auditor. Here is the original news article:\n<text>\n\nHere is the drafted summary:\n<summary>\n\nPlease compare the draft against the source. Evaluate if the draft accurately captures the context and incorporates the following key phrases: <keywords>. Provide a Critique Report highlighting factual discrepancies, missing metadata, or omitted key phrases.[/INST]",
    "arxiv": "<s>[INST]You are a rigorous auditor. Here is the research paper:\n<text>\n\nHere is the drafted abstract:\n<summary>\n\nPlease compare the draft against the source. Evaluate if the draft accurately captures the context and incorporates the following key phrases: <keywords>. Provide a Critique Report highlighting factual discrepancies, missing metadata, or omitted key phrases.[/INST]",
    "pubmed": "<s>[INST]You are a rigorous auditor. Here is the research paper:\n<text>\n\nHere is the drafted abstract:\n<summary>\n\nPlease compare the draft against the source. Evaluate if the draft accurately captures the context and incorporates the following key phrases: <keywords>. Provide a Critique Report highlighting factual discrepancies, missing metadata, or omitted key phrases.[/INST]",
    "samsum": "<s>[INST]You are a rigorous auditor. Here is the conversation:\n<text>\n\nHere is the drafted summary:\n<summary>\n\nPlease compare the draft against the source. Evaluate if the draft accurately captures the context and incorporates the following key phrases: <keywords>. Provide a Critique Report highlighting factual discrepancies, missing metadata, or omitted key phrases.[/INST]",
    "meetingbank": "<s>[INST]You are a rigorous auditor. Here is the conversation:\n<text>\n\nHere is the drafted summary:\n<summary>\n\nPlease compare the draft against the source. Evaluate if the draft accurately captures the context and incorporates the following key phrases: <keywords>. Provide a Critique Report highlighting factual discrepancies, missing metadata, or omitted key phrases.[/INST]",
}

CRITIC_KEYWORD_PROMPT_STR_FOR_CLAUDE = {
    "cnn": "You are a rigorous auditor. Here is the original news article:\n<text>\n\nHere is the drafted summary:\n<summary>\n\nPlease compare the draft against the source. Evaluate if the draft accurately captures the context and incorporates the following key phrases: <keywords>. Provide a Critique Report highlighting factual discrepancies, missing metadata, or omitted key phrases.",
    "arxiv": "You are a rigorous auditor. Here is the research paper:\n<text>\n\nHere is the drafted abstract:\n<summary>\n\nPlease compare the draft against the source. Evaluate if the draft accurately captures the context and incorporates the following key phrases: <keywords>. Provide a Critique Report highlighting factual discrepancies, missing metadata, or omitted key phrases.",
    "pubmed": "You are a rigorous auditor. Here is the research paper:\n<text>\n\nHere is the drafted abstract:\n<summary>\n\nPlease compare the draft against the source. Evaluate if the draft accurately captures the context and incorporates the following key phrases: <keywords>. Provide a Critique Report highlighting factual discrepancies, missing metadata, or omitted key phrases.",
    "samsum": "You are a rigorous auditor. Here is the conversation:\n<text>\n\nHere is the drafted summary:\n<summary>\n\nPlease compare the draft against the source. Evaluate if the draft accurately captures the context and incorporates the following key phrases: <keywords>. Provide a Critique Report highlighting factual discrepancies, missing metadata, or omitted key phrases.",
    "meetingbank": "You are a rigorous auditor. Here is the conversation:\n<text>\n\nHere is the drafted summary:\n<summary>\n\nPlease compare the draft against the source. Evaluate if the draft accurately captures the context and incorporates the following key phrases: <keywords>. Provide a Critique Report highlighting factual discrepancies, missing metadata, or omitted key phrases.",
}


ENHANCER_KEYWORD_PROMPT_STR_FOR_MISTRAL = {
    "cnn": "<s>[INST]Here is a news article:\n<text>\n\nHere is the initial 1-2 sentence summary draft:\n<summary>\n\nHere is the Critique Report of that draft:\n<critique>\n\nPlease re-write and adjust the summary. Address the flaws noted by the Critic and ensure the following key phrases are accurately integrated: <keywords>. Output the final, verified summary.[/INST]",
    "arxiv": "<s>[INST]Here is a research paper:\n<text>\n\nHere is the initial ~3 sentence abstract draft:\n<summary>\n\nHere is the Critique Report of that draft:\n<critique>\n\nPlease re-write and adjust the abstract. Address the flaws noted by the Critic and ensure the following key phrases are accurately integrated: <keywords>. Output the final, verified abstract.[/INST]",
    "pubmed": "<s>[INST]Here is a research paper:\n<text>\n\nHere is the initial ~3 sentence abstract draft:\n<summary>\n\nHere is the Critique Report of that draft:\n<critique>\n\nPlease re-write and adjust the abstract. Address the flaws noted by the Critic and ensure the following key phrases are accurately integrated: <keywords>. Output the final, verified abstract.[/INST]",
    "samsum": "<s>[INST]Here is a conversation:\n<text>\n\nHere is the initial 1 sentence summary draft:\n<summary>\n\nHere is the Critique Report of that draft:\n<critique>\n\nPlease re-write and adjust the summary. Address the flaws noted by the Critic and ensure the following key phrases are accurately integrated: <keywords>. Output the final, verified summary.[/INST]",
    "meetingbank": "<s>[INST]Here is a conversation:\n<text>\n\nHere is the initial 2-3 sentence summary draft:\n<summary>\n\nHere is the Critique Report of that draft:\n<critique>\n\nPlease re-write and adjust the summary. Address the flaws noted by the Critic and ensure the following key phrases are accurately integrated: <keywords>. Output the final, verified summary.[/INST]",
}

ENHANCER_KEYWORD_PROMPT_STR_FOR_CLAUDE = {
    "cnn": "Here is a news article:\n<text>\n\nHere is the initial 2-3 sentence summary draft:\n<summary>\n\nHere is the Critique Report of that draft:\n<critique>\n\nPlease re-write and adjust the summary. Address the flaws noted by the Critic and ensure the following key phrases are accurately integrated: <keywords>. Output the final, verified summary.",
    "arxiv": "Here is a research paper:\n<text>\n\nHere is the initial abstract draft:\n<summary>\n\nHere is the Critique Report of that draft:\n<critique>\n\nPlease re-write and adjust the abstract. Address the flaws noted by the Critic and ensure the following key phrases are accurately integrated: <keywords>. Output the final, verified abstract.",
    "pubmed": "Here is a research paper:\n<text>\n\nHere is the initial ~5 sentence abstract draft:\n<summary>\n\nHere is the Critique Report of that draft:\n<critique>\n\nPlease re-write and adjust the abstract. Address the flaws noted by the Critic and ensure the following key phrases are accurately integrated: <keywords>. Output the final, verified abstract.",
    "samsum": "Here is a conversation:\n<text>\n\nHere is the initial 1 sentence summary draft:\n<summary>\n\nHere is the Critique Report of that draft:\n<critique>\n\nPlease re-write and adjust the summary. Address the flaws noted by the Critic and ensure the following key phrases are accurately integrated: <keywords>. Output the final, verified summary.",
    "meetingbank": "Here is a conversation:\n<text>\n\nHere is the initial ~5 sentence summary draft:\n<summary>\n\nHere is the Critique Report of that draft:\n<critique>\n\nPlease re-write and adjust the summary. Address the flaws noted by the Critic and ensure the following key phrases are accurately integrated: <keywords>. Output the final, verified summary.",
}