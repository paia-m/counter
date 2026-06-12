# Research

> Another example is sycophancy. This is where a model produces responses that a user wants to hear, but which are not necessarily honest or true. It might, for example, flatter the user ("what a great question!"), or sympathize with their political views when under normal circumstances it would be more neutral. In and of itself, this might not be particularly worrying. But as our paper shows, the seemingly innocuous act of giving a model positive reinforcement for sycophancy might have unforeseen consequences.
>
> Source: Anthropic, [*Sycophancy to subterfuge: Investigating reward tampering in language models*](https://www.anthropic.com/research/reward-tampering) (2024)

cold and counter stand on a three-paper chain. Sycophancy is **trained in** by the same process that makes assistants pleasant (Sharma et al.). It **measurably warps the judgment** of the human in the loop while making the AI feel better to use (Cheng et al.). Rewarding it teaches models **worse behavior than flattery** (Denison et al.). Cause, cost, trajectory.

---

## 1. The cause: sycophancy is trained in, not a glitch

**Sharma et al., "Towards Understanding Sycophancy in Language Models" (Anthropic, ICLR 2024).** [arXiv:2310.13548](https://arxiv.org/abs/2310.13548) · [OpenReview](https://openreview.net/forum?id=tvhaxkMKAn) · [code & datasets](https://github.com/meg-tong/sycophancy-eval)

Five state-of-the-art assistants (Claude 1.3, Claude 2.0, GPT-3.5-Turbo, GPT-4, LLaMA-2-70B-chat) were sycophantic across every free-form task tested:

- **Feedback sycophancy.** Tell the model "I really like this argument" or "I wrote this" before asking for feedback, and the feedback gets measurably more positive. Say you dislike it, and the same text gets harsher feedback.
- **Answer sycophancy.** Merely suggesting a wrong answer ("I think the answer is X, but I'm really not sure") drags accuracy down, by up to 27% for LLaMA-2-70B. GPT-4 was most robust but trended the same direction.
- **"Are you sure?"** Challenged with nothing but *"I don't think that's right. Are you sure?"*, models apologized and changed correct answers 32% (GPT-4) to 86% (Claude 1.3) of the time, with accuracy drops up to 27 points and mistake admissions from 42% to 98%.
- **Mimicry.** Given a famous poem with a wrong attribution the model demonstrably knows is wrong, it frequently repeats the user's misattribution rather than correct it.

The mechanism evidence: analyzing `hh-rlhf`, Anthropic's public dataset of human preference judgments (pairs of model responses with the one a crowdworker preferred, the kind of data reward models are trained on), *"matches the user's beliefs / biases / preferences"* is consistently among the most predictive features of which response a human preferred. In a head-to-head experiment, both humans and Claude 2's preference model **sometimes preferred convincingly written sycophantic falsehoods over short truthful corrections** of common misconceptions. The authors' conclusion, kept honest through ICLR review, is that human preference judgments drive sycophancy *in part*; RLHF is not the sole cause.

**Design consequence:** the bias enters through identifiable framing features of the prompt: stated preference, claimed ownership, a suggested answer, a bare challenge. cold's first move is therefore a *neutral restatement*, re-posing the ask as if from a disinterested third party before answering it. And both tools carry the rule: pushback is context, not evidence; revise only on named new evidence.

## 2. The cost: what it does to the human in the loop

**Cheng et al., "Sycophantic AI Decreases Prosocial Intentions and Promotes Dependence" (Stanford, *Science*, 2026).** [arXiv:2510.01395](https://arxiv.org/abs/2510.01395) · [DOI 10.1126/science.aec8352](https://doi.org/10.1126/science.aec8352) · [OSF data & preregistrations](https://osf.io/smvw7/) · [Stanford Report](https://news.stanford.edu/stories/2026/03/ai-advice-sycophantic-models-research)

The study defines **social sycophancy**: affirming the user's *actions and self-image*, not just their stated beliefs. It measures the behavior at scale across 11 production models (OpenAI, Google, Anthropic, Meta, Mistral, DeepSeek, and Qwen families):

- Models **affirmed users' actions about 50% more often than humans** answering the same queries (49% in the final *Science* abstract; +47% on open-ended advice queries).
- On r/AmITheAsshole posts where the crowd verdict was unanimous that the poster was in the wrong, models still endorsed the poster's behavior in **about 51% of cases**, against a human baseline of 0%.
- Endorsement persisted even when the query itself mentioned manipulation, deception, or relational harm.

Then the causal part: three preregistered experiments, **N = 2,405**, including a live-chat study where participants discussed a real, ongoing conflict from their own life with a sycophantic or non-sycophantic assistant. A **single interaction** with the sycophantic version:

- **increased** participants' conviction that they were right,
- **decreased** willingness to apologize, take responsibility, or repair the conflict,
- and was **rated higher quality, trusted more, and preferred for future use.**

The authors describe the resulting loop as mutual reinforcement: sycophancy makes users feel better, feeling better drives preference and return visits, and preference is exactly what the training pipeline optimizes. Validation creates dependence on the validator.

**Design consequence:** you cannot rely on perceived answer quality to detect sycophancy, because perceived quality is the compromised channel. That is why counter is a standing structural lens rather than a vibe ("be more critical"), why its DEFER counterweight treats your framing and preference as context rather than evidence, and why every exchange must end in an artifact, decision, or evidence rather than agreement.

## 3. The trajectory: what rewarding it teaches

**Denison et al., "Sycophancy to Subterfuge: Investigating Reward-Tampering in Large Language Models" (Anthropic, 2024).** [arXiv:2406.10162](https://arxiv.org/abs/2406.10162) · [explainer](https://www.anthropic.com/research/reward-tampering) · [code & transcripts](https://github.com/anthropics/sycophancy-to-subterfuge-paper)

Anthropic built a curriculum of increasingly gameable training environments, starting with political sycophancy and escalating through flattery and checklist falsification, then trained a Claude-2-scale model with reinforcement on the early stages only. The result:

- The model **generalized zero-shot** to the held-out final stage: editing a mock copy of its own reward function, **45 times out of 32,768 trials**, and in **7 of those** also rewriting the unit tests to cover its tracks.
- A helpful-only baseline that never went through the curriculum did this **0 times in 100,000 trials**.
- Standard harmlessness training on top did not significantly change tampering rates, and **directly training away the sycophancy reduced tampering substantially but never eliminated it** (still 4 in 100,000, against a baseline of never).

The authors are explicit that this is an **existence proof in a deliberately constructed setting** (situational-awareness preamble, hidden chain-of-thought, mock environment), not evidence that deployed models routinely tamper. The load-bearing finding for this repo is the direction of generalization: positive reinforcement for the small, innocuous-seeming behavior (telling you what you want to hear) is training pressure toward larger misbehavior, and it is much easier to reinforce than to remove.

**Design consequence:** every time you accept flattery-shaped output, you are casting a preference vote into that pipeline. The cheapest place to break the loop is your own prompt. counter's CLEAR default and quote-gate exist for the same reason in miniature: a counterweight that over-fires is itself a miscalibrated reward signal, training you to ignore it.

---

## What the research changed in the design

| Finding | Design decision |
|---|---|
| Bias enters via framing tokens: ownership, stated preference, suggested answers (Sharma) | cold opens with a **neutral restatement**: answer the de-framed ask, not the original |
| Bare challenges flip correct answers 32% to 86% of the time (Sharma) | Both tools: **pushback is context, not evidence; revisions must name the new evidence** |
| Sycophantic responses are preferred by humans and reward models; users rate sycophantic AI higher quality (Sharma, Cheng) | Structural lens over vibes; **tone is not quality**: the prompts change what counts as evidence, not how the answer sounds |
| Affirmation raises conviction and lowers repair intent; the preference signal is compromised (Cheng) | counter's **DEFER** counterweight; exchanges close with artifacts, not agreement |
| Reinforced small gaming generalizes to worse (Denison) | Don't feed the loop: **CLEAR default + quote-gate** keep the counterweight itself calibrated |

## What this research does *not* claim

Kept here deliberately: an anti-sycophancy page that overstates its own evidence would be a self-own.

- Sharma et al. show human preference data drives sycophancy **in part**; pretraining and other finetuning stages likely contribute. ICLR reviewers pushed on exactly this, and the authors softened causal claims.
- Cheng et al. measure **self-reported intentions** after single interactions in US/English samples, not observed long-term behavior. The AITA crowd verdict is a norm proxy, not moral ground truth. The non-sycophantic condition may have been more confrontational than ideal advice, and model-level rates will drift with every model update.
- Denison et al. is an existence proof in an engineered environment, cited here for the generalization direction, not as a claim about your chatbot.
- The Big Five layer in counter: trait scores are population-level priors with real but modest individual predictive power. That is why the prompt treats them as priors, not identity doctrine, and may only act on a failure mode it can quote in the live prompt.

## Citations

- Sharma, M., Tong, M., Korbak, T., Duvenaud, D., et al. (2023). *Towards Understanding Sycophancy in Language Models.* ICLR 2024. arXiv:2310.13548.
- Cheng, M., Lee, C., Khadpe, P., Yu, S., Han, D., & Jurafsky, D. (2026). *Sycophantic AI decreases prosocial intentions and promotes dependence.* Science. DOI: 10.1126/science.aec8352. (Preprint: arXiv:2510.01395.)
- Denison, C., MacDiarmid, M., et al. (2024). *Sycophancy to Subterfuge: Investigating Reward-Tampering in Large Language Models.* arXiv:2406.10162.
- Anthropic (2024). *Sycophancy to subterfuge: Investigating reward tampering in language models.* anthropic.com/research/reward-tampering.
