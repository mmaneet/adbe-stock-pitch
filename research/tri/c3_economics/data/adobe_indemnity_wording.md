# Adobe Firefly IP indemnification - exact wording (R1 resolution, accessed 2026-10-02)

Quotes are <25 words each. "verified" = document fetched and parsed by R1 (Y) or wording from search snippet only (N).
Raw PDFs are in the R1 scratchpad, not in the repo.

## 1. PSLT - Adobe Firefly Supplemental Coverage (2024v1)  [verified: Y]
URL: https://www.adobe.com/content/dam/cc/en/legal/terms/enterprise/pdfs/PSLT-AdobeFireflySupplementalCoverage_2024v1.pdf (1 page; fetched with WebFetch; curl to www.adobe.com stalled at TLS)

- Scope: "The terms in this PSLT apply only to SKUs that explicitly reference this PSLT."
- Eligible features: "'Eligible Firefly Features' means the Firefly features listed at helpx.adobe.com/legal/product-descriptions/adobe-firefly.html" (that helpx page returns 403 to us).
- Trigger: coverage attaches to a Firefly Output "(following an Export Event)".
- Covered claims (s.3): a Claim that a Firefly Output "directly infringes the third party's patent, copyright, trademark, publicity, or privacy rights."
- Exceptions (s.4), Adobe has no liability where the claim arises from:
  (A) "any modification of a Firefly Output, including with any Adobe Products and Services";
  (B) "any combination of a Firefly Output with any other material, content or information";
  (C) "use of a Firefly Output in violation of the Agreement";
  (D) "the context in which any Firefly Output is used";
  (E) output "based on a non-text Firefly Input, where the Firefly Input on its own would have given rise to the Claim";
  (F) "any use of a Firefly Output after Adobe has instructed Customer to stop using it";
  (G) "anything that is not the audio and/or visual content displayed or played by the Eligible Firefly Feature" (e.g. metadata).
- No cap stated in the PSLT (see FAQ Q15 below). Partner / third-party models are not mentioned in this PSLT.
- s.5: customer may not use outputs "to directly or indirectly create, train, test, or otherwise improve any machine learning algorithms".

## 2. PSLT - Creative Partner Model Supplemental Coverage (2026v1)  [verified: Y]
URL: https://www.adobe.com/go/partner-model-supplemental-coverage (resolves to a 1-page PSLT PDF; fetched with WebFetch)

- Partner-model outputs ARE indemnifiable, but under this separate, narrower PSLT that the SKU must reference.
- "'Covered IP Rights' means patent, copyright, moral rights or similar rights." (trademark, publicity and privacy are NOT in the definition)
- "'Eligible Generative AI Feature' means features powered by any of the partner models listed at https://helpx.adobe.com/legal/product-descriptions/partner-model.html" (page 403 to us).
- Covered claims (s.3): a "Legal Proceeding" alleging that "unmodified Indemnified Output directly misappropriates a trade secret or infringes a third party's Covered IP Rights."
- "'Legal Proceeding' means a formal legal proceeding filed by an unaffiliated third party before a court or government tribunal." (demand letters alone do not qualify)
- Exceptions (s.4), in addition to General Terms exceptions:
  (A) "any combination of Indemnified Output with any other material, content or information";
  (B) use "in violation of the Agreement";
  (C) "use of an Indemnified Output in commerce or the course of trade that violates a third party's trademark or related rights";
  (D) "Customer's Input or other data or models provided by or on behalf of Customer (including in connection with any customization or fine-tuning)";
  (E) use "after Adobe has instructed Customer to stop using it";
  (F) "Customer's disabling, modification, or circumvention of Adobe's or its licensors' filters or other safety systems";
  (G) use "that Customer knows or reasonably should have known was likely to infringe any Covered IP Rights."

## 3. Firefly Legal FAQs - Enterprise Customers (Adobe, May 10, 2024)  [verified: Y]
URL: https://adobe.com/cc-shared/assets/pdf/enterprise/firefly-legal-faqs-enterprise-customers-2024-06-11.pdf (5 pages)

- Q10: models "were trained on licensed content, such as Adobe Stock, and public domain content where the copyright has expired."
- Q12: "Yes, if you have purchased the appropriate entitlement (which will require a new contracting event), subject to the applicable terms, conditions, and exclusions."
- Q13: covers claims that the output "directly infringes or violates any third party's patent, copyright, trademark, publicity rights or privacy rights."
- Q13 exclusions: "your modification of the Firefly output using any product or service, including edits made with Creative Cloud products/services"; "any content that you provide for custom training".
- Q14: "Adobe's Firefly IP indemnity for eligible offers covers Firefly GA features that generate imagery. Terms apply."
- Q15 (cap): "The same limitation of liability that applies to technology-based IP claims under your existing contract with Adobe will apply".

## 4. Adobe Firefly for enterprise overview (Adobe collateral dated 2025-03-27, hosted by reseller SHI)  [verified: Y]
URL: https://www.content.shi.com/cms-content/accelerator/media/pdfs/adobe/adobe-032725-adobe-firefly-for-enterprise-overview.pdf

- "Firefly is designed to be commercially safe, and enterprises may obtain an IP indemnity from Adobe for content generated by select Firefly-powered workflows.*"
- "*Opportunity to obtain an IP indemnity from Adobe for content generated by select Firefly-powered workflows under certain Adobe offers. Terms will apply."
- "IP indemnification is also available through certain Creative Cloud plans.*"

## 5. Pages that could not be fetched (wording from search snippets only)  [verified: N]
- https://business.adobe.com/products/firefly-business/firefly-ai-approach.html (HTTP 503 to curl and WebFetch): snippet "enterprise customers may be eligible for IP indemnification for outputs from Adobe Firefly, Google, and OpenAI".
- https://helpx.adobe.com/firefly/web/work-with-enterprise-features/creative-production/partner-models-in-firefly-creative-production-for-enterprise.html (403): snippet "for eligible generally available Google and OpenAI media generation models ... Adobe provides indemnification for certain copyright infringement claims"; "does not cover trademark, publicity rights, or privacy rights claims" (consistent with PSLT 2026v1 s.2.1 and s.4(C)).
- https://www.adobe.com/legal/licenses-terms/adobe-gen-ai-user-guidelines.html (fetched, last updated 2026-05-15): contains no indemnification language (verified Y that it is absent).

## 6. Third-party reads (for context only)
- Redress Compliance, 2026-09-24 (fetched): "Features the interface marks as powered by models Adobe did not train fall outside the Firefly indemnity." and "Beta and trial features. These are excluded".
- CMO Tech, 2023-10-10 (fetched): "the indemnification will not cover any modifications or additions to the Firefly output that infringe on existing copyrights."

## What this means for C3 (economics / "commercially safe" moat)
1. Indemnity is an enterprise entitlement (new contracting event, SKU must reference the PSLT); it is not a feature of individual or teams plans.
2. Firefly-model outputs: broad (patent, copyright, trademark, publicity, privacy) but only for GA imagery features, unmodified output, after export.
3. Partner-model outputs (Google, OpenAI, etc. on Adobe's eligible list): covered since the 2026v1 PSLT, but only for patent/copyright/moral rights, only unmodified output, only once a formal legal proceeding is filed, and with a knew-or-should-have-known carve-out.
4. Cap = the customer's existing technology-IP limitation of liability (not a stated dollar figure).
