# INTERNATIONAL STANDARDS ON COMBATING MONEY LAUNDERING AND THE FINANCING OF TERRORISM
## The FATF 40 Recommendations (Core Forensic Extract)

### FATF Recommendation 10: Customer Due Diligence (CDD)
Financial institutions must undertake CDD measures when:
1. Establishing business relations.
2. Carrying out occasional transactions above the applicable designated threshold (USD/EUR 15,000 or regional equivalents such as INR 10 Lakhs).
3. There is a suspicion of money laundering or terrorist financing, regardless of any exemptions or thresholds.
4. The financial institution has doubts about the veracity or adequacy of previously obtained customer identification data.

*Forensic Marker - Structuring / Smurfing:* 
Where transactions are deliberately fragmented into smaller amounts below statutory reporting ceilings to evade threshold triggers, institutions must identify connected multi-party transactions conducted in brief time windows and treat them as a single consolidated operation.

---

### FATF Recommendation 16: Wire Transfers (The Travel Rule)
1. Countries must ensure that financial institutions include required and accurate originator information, and required beneficiary information, on cross-border wire transfers and real-time domestic rails (including instant settlements, UPI, FAST, IMPS, RTGS).
2. Intermediary financial institutions must detect lack of required originator or beneficiary information and monitor high-velocity pass-through transfers.

*Forensic Marker - Rapid Movement Layering:*
An intermediate node exhibiting near-zero balance dwell time (funds drained >95% within 60 minutes of credit), especially when converting domestic instant rails to cross-border outbound wires (e.g., IMPS to SWIFT), constitutes high-risk layering under Recommendation 16.

---

### FATF Recommendation 20: Reporting of Suspicious Transactions (STR)
If a financial institution suspects or has reasonable grounds to suspect that funds are the proceeds of a criminal activity, or are related to terrorist financing, it must be required, by law, to report its suspicions promptly to the national Financial Intelligence Unit (FIU).

*Forensic Standard:*
The Suspicious Transaction Report (STR) must cite specific transactional facts, counterparties, velocity patterns, and statutory thresholds violated. Vague or ungrounded accusations are non-compliant.

---

### FATF Recommendation 24 & 25: Transparency and Beneficial Ownership of Legal Persons
1. Competent authorities must be able to obtain, or have access in a timely manner to, adequate, accurate and current information on the beneficial ownership and control of companies and other legal persons.
2. The use of shell companies—entities with no physical operations, minimal corporate age (<30 days), and rapid high-value transactions—must trigger immediate enhanced due diligence (EDD) and beneficial ownership look-through.