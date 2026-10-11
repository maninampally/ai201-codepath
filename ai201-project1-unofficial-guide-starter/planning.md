# planning.md — The Unofficial Guide: FAU CS Professor Reviews

## Domain

This Unofficial Guide covers student-generated reviews of professors in the
Computer Science and Electrical Engineering departments at Florida Atlantic
University (FAU). The domain includes Rate My Professors reviews for 10 FAU
CS/EE faculty members spanning courses in data mining, machine learning,
software engineering, computer architecture, operating systems, and web
development.

This knowledge is valuable because official FAU channels (course catalogs,
department websites) tell you nothing about what a professor's class is
actually like — how hard the exams are, whether they respond to emails,
whether attendance matters, or whether the online section is worth taking.
Students share this knowledge informally, but it's scattered across review
sites and hard to query directly. This system makes it searchable and
answerable.

## Documents

10 plain-text files in the /data directory, one per professor:

- prof_agarwal_ankur.txt — 31 reviews, courses: CEN4010, CDA4210, CEN5035
- prof_ibrahim_ali.txt — 23 reviews, courses: CAP4770, COP2034
- prof_kalva_hari.txt — 13 reviews, courses: CEN5806, CNT6885, LOGIC3204
- prof_resnick_rhian.txt — 17 reviews, courses: ISM4403, ISM3230, ISM4324
- prof_assis_raquel.txt — 19 reviews, courses: CAP4773, CAP6546
- prof_kayikci_safak.txt — 26 reviews, courses: CEN3062C, CEN4010, CAP4773
- prof_koch_fernando.txt — 6 reviews, courses: CAP5768, CEN4010, CAP4773
- prof_alhalabi_bassem.txt — 56 reviews, courses: CDA3331, CDA4630, CDA3201
- prof_furht_borko.txt — 12 reviews, courses: COP4610
- prof_marques_oge.txt — 47 reviews, courses: COP3813, CAP4630, CAP6635

Total: ~251 reviews across 10 professors.
Sources: Rate My Professors (ratemyprofessors.com), manually collected.

## Chunking Strategy

Documents are review-based: short opinions ranging from 1 sentence to
roughly 10 sentences each. Each review is a standalone unit of student
opinion about a specific professor and course.

Strategy: chunk by individual review, not by fixed character count.
Each review becomes one chunk. This preserves the natural unit of meaning —
one student's complete opinion — and avoids splitting a review mid-thought.

Where reviews are very short (1-2 sentences), they will be grouped with
adjacent reviews from the same professor to reach a minimum meaningful size
of ~100 characters.

Chunk size: roughly 100–600 characters per chunk (one review each).
Overlap: none needed — reviews are already self-contained units.

Why this fits: unlike long-form guides or textbook chapters, these documents
are already segmented by review. Splitting by character count would cut
reviews mid-sentence and destroy meaning. Splitting by review keeps each
chunk answerable on its own.

Too-small risk: a 1-sentence review ("Good teacher.") carries almost no
semantic signal for embedding. Mitigation: merge very short reviews.
Too-large risk: combining many reviews into one chunk dilutes the specific
facts a student is asking about. Avoided by keeping reviews separate.

Expected chunk count: 200–260 chunks across 10 files.

## Retrieval Approach

Embedding model: all-MiniLM-L6-v2 via sentence-transformers.
Runs locally — no API key, no rate limits, no cost.

Vector store: ChromaDB, running locally.

Top-k: 5 chunks per query. Rationale: professor review questions often need
2–3 reviews to give a confident answer (one review might be an outlier).
Retrieving 5 gives the LLM enough context to synthesize without drowning it
in noise.

Production tradeoffs (if cost were no constraint):
- Context length: all-MiniLM-L6-v2 has a 256-token limit, fine for short
  reviews but would truncate long documents. text-embedding-3-small (OpenAI)
  or embed-english-v3.0 (Cohere) support longer contexts.
- Accuracy: larger models like text-embedding-3-large would produce better
  semantic matches at higher cost and latency.
- Multilingual: not needed here (all reviews in English), but
  paraphrase-multilingual-MiniLM-L12-v2 would handle multilingual corpora.
- Local vs API: local embedding (our choice) avoids cost and latency but
  can't be updated without redeployment. API embeddings are easier to swap.

## Evaluation Plan

5 test questions with expected answers:

Q1: "Does Professor Agarwal respond to emails?"
Expected: No. Multiple reviews across different years and courses consistently
report that Agarwal rarely or never responds to emails. This is one of the
most repeated complaints in his reviews.

Q2: "What is Alhalabi's class like?"
Expected: Hands-on, lab-focused, fun. Students describe engaging lectures,
challenging but rewarding labs, group projects, and a professor who genuinely
cares. He is frequently called the best professor in the department. Classes
like CDA3331 and CDA4630 involve wiring circuits and building microcontroller
projects.

Q3: "Is CAP4770 with Ibrahim hard?"
Expected: Moderately difficult (average 3/5 difficulty). The class involves
heavy mathematics in lectures and Python coding for assignments. Graded only
on 5 projects, no traditional exams. Students say he simplifies complex
material but his lectures can be hard to follow due to his accent and
handwriting.

Q4: "What do students say about Furht's exams in COP4610?"
Expected: Exams follow the lectures closely so attending and watching
recordings is essential. A cheat sheet is allowed. The CPU scheduler
programming assignment should be started early. Exams are moderately hard
but curved.

Q5: "Which professor gives the most useful feedback on assignments?"
Expected: Based on reviews, Ibrahim and Assis (in her CAP5768 class) are
most frequently praised for timely and valuable feedback. Alhalabi and
Marques also receive positive mentions. Agarwal and Furht are specifically
criticized for slow or absent feedback.
This question requires cross-document comparison and may surface a retrieval
weakness — the system may only return chunks from one professor rather than
synthesizing across all 10.

## Anticipated Challenges

1. Cross-document comparison queries: Questions like "which professor gives
     the best feedback" require the system to retrieve and synthesize chunks
     from multiple professors. The top-k retrieval may return 5 chunks all
     from one professor, missing the comparative picture entirely. This is the
     most likely failure case.

2. Review noise and contradictions: The same professor often has wildly
     contradictory reviews (5-star and 1-star for the same course). The LLM
     may over-weight the most recent or most-retrieved chunk rather than
     synthesizing the range of opinions. Source attribution helps here but
     doesn't fully solve it.

3. Short chunks with low semantic signal: Very short reviews ("Good teacher."
     "Really good professor.") embed poorly and may surface as false positives
     for unrelated queries.

4. Professor name variants: Reviews use "Dr. Alhalabi", "Baseem", "Bassem",
     "Alhalabi" interchangeably. The embedding model handles this reasonably
     but exact-name queries may miss some chunks.

## AI Tool Plan

1. Ingestion and chunking (ingest.py):
     Input to AI: the Documents section and Chunking Strategy section of this
     planning.md, plus the requirement to output chunks with source metadata.
     Expected output: a script that loads all .txt files from /data, splits
     them by review block (blank-line separated), filters out chunks under 50
     characters, and saves chunks with source filename attached.

2. Embedding and vector store (embed.py):
     Input to AI: the Retrieval Approach section of this planning.md and the
     pipeline diagram.
     Expected output: a script that loads chunks from ingest.py, embeds them
     with all-MiniLM-L6-v2, stores them in ChromaDB with metadata
     (source, chunk_index), and exposes a retrieve(query, k=5) function.

3. Generation (query.py):
     Input to AI: the grounding requirement (answer from retrieved context
     only), the output format (answer + source list), and example of a
     grounded vs non-grounded response from the spec.
     Expected output: a function ask(question) that calls retrieve(), builds
     a prompt with the chunks as context, calls Groq llama-3.3-70b-versatile,
     and returns {"answer": ..., "sources": [...] }.

4. Interface (app.py):
     Input to AI: the Gradio skeleton from the spec plus the ask() function
     signature.
     Expected output: a working Gradio app with a question input, answer
     output, and sources output.

## Architecture

Document Ingestion        Chunking              Embedding + Vector Store
(load .txt files)  -->   (split by review,  --> (all-MiniLM-L6-v2         
(10 professor files)      filter short chunks)    sentence-transformers)
                                                                                  (ChromaDB, local)
                                                                                            |
                                                                                            v
User Query  ----------------------------------------> Retrieval
(Gradio UI)                                      (semantic search, top-5)
                                                                                            |
                                                                                            v
                                                                                      Generation
                                                                                 (Groq API, llama-3.3-70b)
                                                                                 (grounded prompt + sources)
                                                                                            |
                                                                                            v
                                                                             Answer + Source Citations
                                                                                      (Gradio UI)

