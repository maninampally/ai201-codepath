# The Unofficial Guide: FAU CS/EE Professor Reviews

A RAG (Retrieval-Augmented Generation) system that makes student-generated
professor reviews searchable and answerable. Ask plain-language questions
about FAU CS/EE professors and get grounded, cited answers drawn from
real Rate My Professors reviews.

## Domain and Document Sources

**Domain:** Student reviews of professors in the Computer Science and
Electrical Engineering departments at Florida Atlantic University (FAU).

This knowledge is valuable because official FAU channels tell you nothing
about what a professor's class is actually like — how hard the exams are,
whether they respond to emails, whether the online section is worth taking.
Students share this informally, but it's scattered and hard to query.

**Sources:** Rate My Professors (ratemyprofessors.com), manually collected.

| File | Professor | Reviews |
|------|-----------|---------|
| prof_agarwal_ankur.txt | Ankur Agarwal | 31 |
| prof_ibrahim_ali.txt | Ali Ibrahim | 23 |
| prof_kalva_hari.txt | Hari Kalva | 13 |
| prof_resnick_rhian.txt | Rhian Resnick | 17 |
| prof_assis_raquel.txt | Raquel Assis | 19 |
| prof_kayikci_safak.txt | Safak Kayikci | 26 |
| prof_koch_fernando.txt | Fernando Koch | 6 |
| prof_alhalabi_bassem.txt | Bassem Alhalabi | 56 |
| prof_furht_borko.txt | Borko Furht | 12 |
| prof_marques_oge.txt | Oge Marques | 47 |

Total: 251 reviews, 246 chunks after processing.

## Chunking Strategy and Reasoning

**Strategy:** Split documents by individual review (blank-line separated
blocks), not by fixed character count.

**Chunk size:** ~100–600 characters per chunk (one review per chunk).
**Overlap:** None. Reviews are self-contained units and don't benefit from
overlap.

**Why this fits the documents:** Each review is already a standalone unit
of student opinion. Splitting by character count would cut reviews
mid-sentence and destroy meaning. Splitting by review keeps each chunk
self-contained and directly answerable.

**Filtering:** Chunks under 50 characters and header blocks (professor
name/rating lines) are excluded. Final count: 246 chunks.

## Sample Chunks

**Chunk 1** (source: prof_alhalabi_bassem.txt)
```

Quality: 5.0 | Difficulty: 1.0 | Course: CDA4630 | Dec 2024
Alhalabi is the GOAT. This is also the most practical course in the CE
curriculum. First half of the semester, you learn about sensors and
actuators and wire up a circuit. Then you get into teams and come up with
a project that uses a microcontroller (we were given an ESP32) and present
it at the end. Just manage your time well.

```
**Chunk 2** (source: prof_ibrahim_ali.txt)
```

Quality: 5.0 | Difficulty: 2.0 | Course: CAP4770 | May 2025
Somehow he has everything memorized, he's not even looking at notes when
he's lecturing. He will just write out big formulas from his head. This
class is important if you want to understand transformers in large language
models. Cosine similarity is the most important concept in this class.

```
**Chunk 3** (source: prof_agarwal_ankur.txt)
```

Quality: 1.0 | Difficulty: 4.0 | Course: CDA4210 | Aug 2023
If you're taking this online, it is awful. Prepare to pull yourself up.
And pray. The professor checks emails on class days if at all. He claims
he won't accept lates but will give you an extension if you ask (which is
a lie). His lectures have mistakes which you must catch.

```
**Chunk 4** (source: prof_furht_borko.txt)
```

Quality: 4.0 | Difficulty: 3.0 | Course: COP4610 | Nov 2015
Furht has a slight accent but you can understand him very well. His
lectures are very informative. The class consisted of 1 programming
assignment on CPU schedulers, 1 research group project on OS, and 2 exams.
No final. Textbook free online. Nice guy. I learned a lot.

```
**Chunk 5** (source: prof_assis_raquel.txt)
```

Quality: 1.0 | Difficulty: 3.0 | Course: CAP4773 | Feb 2022
She gives abstract instructions for homework assignments and states that
it doesn't matter if your code is different as long as it produces the
correct answer, then takes points off for having different code than hers.
She doesn't give partial credit either.

```
## Embedding Model

**Model used:** `all-MiniLM-L6-v2` via sentence-transformers.
Runs fully locally — no API key, no rate limits, no cost.

**Production tradeoffs:**
- **Context length:** all-MiniLM-L6-v2 has a 256-token limit, fine for
     short reviews but would truncate longer documents. For production,
     text-embedding-3-small (OpenAI) or embed-english-v3.0 (Cohere) support
     longer contexts.
- **Accuracy:** Larger models like text-embedding-3-large produce better
     semantic matches at higher cost and latency.
- **Multilingual:** Not needed here (all English), but
     paraphrase-multilingual-MiniLM-L12-v2 would handle multilingual corpora.
- **Local vs API:** Local embedding avoids cost and latency but requires
     redeployment to update. API embeddings are easier to swap and scale.

## Retrieval Test Results

**Query 1: "Does Professor Agarwal respond to emails?"**
Top chunks returned:
- [1.065] prof_agarwal_ankur.txt: "Dr. Agarwal is a great lecturer. He takes a long time to grade anything..."
- [1.104] prof_marques_oge.txt: "He is slow to reply to emails, but other than that he is a very good professor..."
- [1.148] prof_agarwal_ankur.txt: "Agarwal demonstrated many qualities you look for in a great professor..."

The top result is relevant (Agarwal, slow grading). The second result
(Marques) is a false positive — it matched on "emails" semantically but
is from the wrong professor. The system retrieved the correct professor's
file in positions 1, 3, and 5. Relevance: partially accurate.

**Query 2: "What is Alhalabi's class like?"**
Top chunks returned:
- [0.572] prof_alhalabi_bassem.txt: "Alhalabi genuinely cares that his students understand the material..."
- [0.679] prof_alhalabi_bassem.txt: "Dr. Alhalabi is very good at teaching. He is lenient..."
- [0.765] prof_agarwal_ankur.txt: "If you can avoid taking him please do so..." (false positive)
- [0.778] prof_alhalabi_bassem.txt: "Dr. Baseem Alhalabi is the best professor I ever had..."

Strong retrieval. Top 2 results are highly relevant with low distance
scores (0.57, 0.68). One false positive from Agarwal snuck in at position
3 but did not affect the final answer. Relevance: accurate.

**Query 3: "Is CAP4770 with Ibrahim hard?"**
Top chunks returned (all from prof_ibrahim_ali.txt):
- [1.013] CAP4770 review mentioning extensions
- [1.060] CAP4770 review mentioning math and Python
- [1.170] CAP4770 review praising his teaching

All 5 results from the correct professor and correct course.
Relevance: accurate.

## Grounded Generation

Grounding is enforced through the system prompt in `query.py`:
```

You are a helpful assistant for FAU students looking up professor reviews.
Answer the user's question using ONLY the information provided in the
retrieved review chunks below. Do not use any outside knowledge. If the
retrieved chunks do not contain enough information to answer the question,
say "I don't have enough information in my documents to answer that."
Always cite which professor and source file the information came from.

```
The user prompt also explicitly instructs: "Answer using only the reviews
above. Cite the source files in your answer."

Source attribution is included in every response — the LLM is instructed
to cite source files inline, and the UI displays a separate Sources panel
showing all retrieved filenames.

## Example Responses

**Example 1 — grounded response with citation:**

Query: "What is Alhalabi's class like?"

Answer: According to the reviews, Alhalabi's class is one where he
genuinely cares that his students understand the material and expects them
to study outside of the classroom, keep up with weekly textbook readings,
and attend lectures (Source 1: prof_alhalabi_bassem.txt). He is very good
at teaching, lenient, and makes his class pretty easy to get an A in,
although he may be late sometimes (Source 2: prof_alhalabi_bassem.txt).
Students who pay attention in lectures, read ahead, and do their labs can
expect to get an A (Source 5: prof_alhalabi_bassem.txt).

Sources: prof_alhalabi_bassem.txt, prof_agarwal_ankur.txt

**Example 2 — grounded response with citation:**

Query: "What do students say about Furht's exams in COP4610?"

Answer: According to the reviews, Furht's exams in COP4610 are challenging
but manageable if you follow the lectures. One student mentions that you
can use a cheat sheet for each exam (Source 1: prof_furht_borko.txt).
Another describes the tests as "moderately hard" (Source 3). A student
states that the tests are "exactly what's in the lectures" (Source 4).
Overall, the consensus is that Furht's exams require preparation and
attention to lectures, but are not impossible to pass.

Sources: prof_furht_borko.txt, prof_kayikci_safak.txt

**Example 3 — out-of-scope refusal:**

Query: "Who is the best professor in the physics department?"

Answer: I don't have enough information in my documents to answer that.
The reviews I have access to only cover CS/EE professors at FAU.

## Query Interface

The interface is a Gradio web app (`app.py`). Run with `python app.py`
and open `http://localhost:7860`.

**Input:** A plain-language question about FAU CS/EE professors.
**Output:**
- Answer panel: grounded response with inline source citations
- Sources panel: list of source files the answer drew from

**Sample interaction:**

Input: "Is CAP4770 with Ibrahim hard?"

Answer: The difficulty of CAP4770 with Professor Ibrahim is rated as 3.0
by most students. However, one student rated it as 1.0, suggesting that
the course may not be hard for everyone. It's also noted that while the
lectures can be difficult to follow, especially due to the mathematical
content, the assignments are purely coding. Overall, CAP4770 with Professor
Ibrahim can be challenging, but manageable, especially with the professor's
generous extensions and grading.

Sources: prof_ibrahim_ali.txt

## Evaluation Report

**Q1: Does Professor Agarwal respond to emails?**
- Expected: No, multiple reviews say he rarely or never responds
- System response: "Professor Agarwal may not respond to emails promptly
     or regularly, as suggested in Source 6 (checks emails on class days if
     at all)" — hedged but directionally correct
- Retrieved chunks: Mixed — some Agarwal chunks, one Marques false positive
- Accuracy: **Partially accurate** — correct conclusion but hedged, and
     the most explicit email complaints were not in the top retrieved chunks

**Q2: What is Alhalabi's class like?**
- Expected: Hands-on, lab-focused, fun, highly recommended
- System response: Correctly described as caring, high quality, expects
     attendance and readings, easy to get an A, labs, sometimes late
- Retrieved chunks: 4 of 5 from correct professor, low distance scores
- Accuracy: **Accurate**

**Q3: Is CAP4770 with Ibrahim hard?**
- Expected: Moderately difficult (3/5), heavy math in lectures, Python
     coding assignments, no traditional exams, generous grading
- System response: Difficulty rated 3.0 by most students, lectures hard
     to follow due to math, assignments are coding, manageable with extensions
- Retrieved chunks: All 5 from correct professor and course
- Accuracy: **Accurate**

**Q4: What do students say about Furht's exams in COP4610?**
- Expected: Follow lectures, cheat sheet allowed, CPU scheduler starts
     early, moderately hard but curved
- System response: Challenging but manageable, cheat sheet allowed, tests
     follow lectures exactly, one Kayikci false positive in sources
- Retrieved chunks: Mostly correct, one unrelated source (Kayikci) in
     the sources panel but not used in the answer
- Accuracy: **Accurate**

**Q5: Which professor gives the most useful feedback on assignments?**
- Expected: Ibrahim and Assis most praised; Agarwal and Furht criticized
- System response: Named only Marques (clear rubric, marks assignments),
     did not mention Ibrahim or Assis, did not compare across professors
- Retrieved chunks: Pulled from 5 different professors but only surfaced
     Marques feedback mentions prominently
- Accuracy: **Partially accurate** — identified one valid answer but
     missed the fuller comparative picture

## Failure Case Analysis

**Q5 is the key failure case.**

The query "Which professor gives the most useful feedback?" requires
comparing feedback quality across all 10 professors. The retrieval
returned chunks from 5 different professors (Agarwal, Alhalabi, Ibrahim,
Marques, Kayikci), but the chunks retrieved were not the ones that most
explicitly discussed feedback quality. The system surfaced Marques because
his reviews mention "clear rubric" and "marks assignments" — which
semantically match "feedback on assignments" — but missed the explicit
"gives good feedback" tags on Ibrahim and Assis reviews.

**Why it happened:** The embedding model matched on surface-level semantic
similarity ("feedback on assignments") rather than the underlying intent
(which professor is best at giving feedback). Reviews tagged "Gives good
feedback" don't always use that exact phrase in the review body, so they
don't embed strongly for this query. This is a retrieval failure, not a
generation failure — the LLM answered correctly from what it was given,
but what it was given was incomplete.

**Fix:** Metadata filtering (storing the RMP tag labels as metadata and
filtering by "Gives good feedback" tag) would solve this. This is one of
the listed stretch features.

## Spec Reflection

**One way the spec helped:** Writing the evaluation plan in planning.md
before coding forced me to think about what "correct" looks like for each
query before building anything. When Q1 (Agarwal emails) initially failed
with k=5, I had a clear expected answer to compare against, which told me
immediately that retrieval was the problem — not generation. Without the
spec, I might have tuned the prompt instead of increasing k.

**One way implementation diverged:** The spec suggested chunk overlap for
cases where key facts span chunk boundaries. I ended up using zero overlap
because the documents are review-based (each review is already a complete
unit). Overlap would have created duplicate chunks without adding useful
context. I updated planning.md to reflect this decision.

## AI Usage

**Instance 1 — ingest.py generation:**
I prompted Claude with the Documents and Chunking Strategy sections of
planning.md and asked it to implement a script that loads .txt files,
splits by blank-line-separated blocks, filters short chunks, and returns
chunks with source metadata. Claude generated a working script. I changed
the filtering logic — the original filtered only on `block.startswith
("Professor:")` but missed other header lines like "Overall Quality".
I added a second condition `or block.startswith("Overall")` after
inspecting the actual output.

**Instance 2 — query.py system prompt:**
I asked Claude to write the grounding system prompt for the Groq API call.
The initial version said "try to use only the provided documents" — too
weak. I revised it to "Answer using ONLY the information provided" and
added the explicit fallback instruction ("say I don't have enough
information") to prevent the model from drawing on general knowledge when
retrieval is weak.
