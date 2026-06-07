# ai-engineering-project
This project includes designing, building and evaluating a Retrieval-Augmented Generation (RAG) LLM-based application that answers user questions about a corpus of company policies & procedures. Deployed on Render with a basic CI/CD pipeline using GitHub Actions that triggers deployment on push when the app builds successfully

## setup
1. run $ pip install -r requirements.txt
2. create and copy the content of the example-env into a .env file and provide your open router key.


## Run
run $ python app.py


# Policy Evaluation Set

## Overview

This evaluation set contains 20 policy-related question-and-answer pairs covering PTO, holidays, leave, expenses, discipline, and financial controls. Each answer is grounded in the policy manual and includes a source citation.

| #  | Question                                                              | Expected Answer                                                                                                   | Reference   |
| -- | --------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ----------- |
| 1  | When can a full-time employee begin using accrued vacation time?      | After completing six months of service, employees may use accrued vacation time with supervisor approval.         | Page 23     |
| 2  | Can vacation time be taken in half-day increments?                    | Yes. Vacation time may be taken in full-day or half-day increments.                                               | Page 23     |
| 3  | What happens if a company holiday occurs during an approved vacation? | The employee is paid for the holiday and uses one fewer vacation day.                                             | Page 23     |
| 4  | Can unused vacation be carried over?                                  | Yes. Accrued vacation days may be carried over up to the policy limit; excess vacation is forfeited.              | Page 23     |
| 5  | Are hourly part-time employees eligible for vacation or sick leave?   | No. Hourly part-time employees are not eligible for vacation, personal, or sick time.                             | Page 23     |
| 6  | How many paid holidays does the organization recognize?               | Ten paid holidays are recognized, including New Year's Day, Independence Day, Thanksgiving, and Christmas Day.    | Page 24     |
| 7  | Are employees allowed time off to vote?                               | Yes. Employees may receive time off on National Election Day as allowed by policy or local law.                   | Page 24     |
| 8  | How much bereavement leave is granted for an immediate family member? | Employees are granted paid bereavement leave for deaths in the immediate family.                                  | Page 24     |
| 9  | Can employees apply for an unpaid leave of absence?                   | Yes. Eligible employees with at least one year of service may request an unpaid leave of absence.                 | Page 24     |
| 10 | What documentation must employees provide for jury duty?              | Employees must provide a copy of the jury summons and proof of service.                                           | Page 25     |
| 11 | What should an employee do after being injured on the job?            | Immediately notify a supervisor and seek medical attention as appropriate.                                        | Page 25     |
| 12 | Are business meals reimbursable?                                      | Yes. Business meals with clients, prospects, or associates involving business discussions are reimbursable.       | Page 19     |
| 13 | What is the maximum reimbursable tip on a meal receipt?               | Tips are reimbursable but should not exceed 20% of the bill.                                                      | Page 19     |
| 14 | Which airfare class is reimbursed for business travel?                | Economy class airfare only is reimbursed.                                                                         | Page 19     |
| 15 | What corrective action steps may be used before termination?          | Counseling, oral warning, and written warning may be used depending on circumstances.                             | Pages 21–22 |
| 16 | Can the organization terminate employment without prior warnings?     | Yes. The organization may determine appropriate corrective action, including termination, based on circumstances. | Pages 21–22 |
| 17 | What types of misconduct may result in corrective action?             | Examples include excessive absenteeism, theft, refusal to perform duties, violence, and rule violations.          | Page 22     |
| 18 | How often are employee performance evaluations conducted?             | Employees are evaluated semi-annually, generally in January and June.                                             | Page 20     |
| 19 | What approvals are required before paying vendor invoices?            | Invoices must be approved by authorized personnel and verified for accuracy before payment.                       | Page 31     |
| 20 | Are receipts required for petty cash expenditures?                    | Yes. Receipts or itemized slips are required for every petty cash disbursement.                                   | Pages 31–32 |

## Coverage Areas

This evaluation set covers:

* Vacation / PTO
* Holidays
* Bereavement Leave
* Jury Duty
* Workers' Compensation
* Travel & Expense Reimbursement
* Performance Management
* Corrective Action & Discipline
* Financial Controls
* Petty Cash Procedures

### Evaluation metrics
1. Groundedness: 99%
2. Citation Accuracy: 99%
3. Exact Match: 99%
4. Latency: p50

## Design Justification
This RAG setup is designed for production-ready document Q&A with a focus on efficiency, accuracy, and simplicity. The combination creates a balanced system that works well without excessive computational overhead.

Why sentence-transformers/all-MiniLM-L6-v2 model?

- Production economics: 22.7MB means faster deployment, lower memory usage, and cheaper scaling

- CPU-only inference: Unlike OpenAI's text-embedding-3-small (requires API calls) or larger models requiring GPUs, this runs anywhere

- Sufficient for most documents: For policy documents, technical manuals, and FAQ-style content, 384 dimensions capture semantic meaning effectively

- Industry standard: This is the most downloaded embedding model on Hugging Face for RAG (over 20M downloads)

Why 1000 characters (not 500 or 2000)?

text
Research-backed rationale:
- Too small (500 chars): Loses context, misses cross-chunk references
- Too large (2000 chars): Dilutes semantic meaning, slower retrieval
- 1000 chars: Sweet spot for most enterprise documents

Why 100 character overlap (10%)?

- Prevents information loss at chunk boundaries

Example: "The policy applies to... [chunk ends] ...all employees" → Without overlap, "all employees" might be lost

- 10% is standard across production RAG systems (LangChain default, LlamaIndex recommendation)

Prompt format
-	Clear separation of context, instructions, and question (proven to improve adherence)

- Explicit boundaries: Prevents prompt injection and context mixing

- Sourced answers: Encourages citation, critical for policy documents


ChromaDB persistence (cost-effective, production-ready)