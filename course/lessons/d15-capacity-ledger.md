# What a GPU cloud actually sells

**15. GPU cloud economics**

Separate capacity billing, hardware access and software responsibility.

**Driving question:** What is the customer buying, and who operates it?

## Capacity, not a successful training run

A neocloud supplies computing capacity on graphics processing units (GPUs), with associated services. Its customer may buy a dedicated cluster for a term or consume resources by the hour. The bill need not depend on a successful training run. CoreWeave’s 2025 annual report describes committed capacity access and usage-based access; over 98 percent of that year’s revenue came from committed contracts.

A model application programming interface (API) is a different product layer. CoreWeave’s product comparison includes GPU-hour billing for dedicated inference and token billing for serverless inference. A lab can calculate its internal cost per token or training run even while paying its infrastructure supplier for GPU-hours. Keeping those perspectives separate avoids pretending every facility sells completed AI tasks.

## Bare metal does not settle software responsibility

Bare metal describes hardware access without a virtualization hypervisor. It does not mean that the supplier simply hands over a Secure Shell (SSH) key and stops operating anything. A supplier still supports the contracted hardware, network and facility; software responsibility varies by service. CoreWeave describes Kubernetes on bare metal and a managed Slurm-on-Kubernetes product, SUNK.

For an inference customer, compare running a serving stack on CoreWeave Kubernetes Service (CKS), which CoreWeave calls Inference on CKS, with Dedicated Inference: the latter moves routing, scaling and serving lifecycle work to the provider. Both can retain GPU-hour billing. Containers, Kubernetes and Slurm are not alternatives to bare metal: they can run on it. A purchase decision therefore needs both the hardware access model and the operating responsibility boundary.

## Case: Anthropic buys capacity; Fireworks serves Cursor’s model

CoreWeave’s April 10, 2026 announcement of a multi-year agreement with Anthropic describes capacity for developing and deploying Claude, with Anthropic running production workloads on CoreWeave’s platform. The announcement leaves the hardware access model and the division of serving work unstated, so it documents a capacity purchase.

Fireworks’ June 2024 account of Cursor’s Fast Apply feature documents the provider-run end of the choice above. Cursor trained a specialized model, and Fireworks deployed it on its own inference engine and served it through a completion API. The account covers Fast Apply only. Placing a contract at either end takes a description of who runs the serving, which Fireworks gives for Fast Apply and the Anthropic announcement leaves out.

## Three offers that must not be conflated

On-demand means pay-as-used access with no term or capacity commitment, billed as the provider specifies. Because nothing is reserved, a launch can fail when the provider has no free capacity. An explicitly interruptible Spot product can be reclaimed; Amazon Web Services documents that behavior for its Elastic Compute Cloud (EC2) Spot Instances. A short-term bilateral market rental is not automatically interruptible merely because someone calls its price spot. A reservation adds a capacity and payment commitment for a term set in its contract, so even a one-year reservation is a committed tenor rather than on-demand access.

Compare the same accelerator, memory, interconnect, region, start date and service scope before interpreting an hourly price difference. Storage, data transfer, support, prepayment and interruption terms can move the effective cost. An index combines market observations; it is not necessarily an offer a buyer can execute for the required cluster.

## Worked example: Two GPU-hour offers with different operating scope

- A customer needs dedicated GPUs for its own inference model.
- Compare customer-operated serving on CKS and CoreWeave Dedicated Inference.

1. Hardware — Dedicated GPU capacity — Both paths can use bare-metal servers.
2. Operations — Customer-operated versus provider-operated serving — Routing, autoscaling and lifecycle responsibilities differ.

**Result:** The hardware and billing unit can be similar while the operating burden differs.

**Model boundary:** Use the documented product scope; private support and commercial terms remain contract-specific.

## The tradeoff

Choice: Use provider-managed serving.

Benefit: Reduce the customer’s serving operations burden.

Cost: Accept the supported runtime and management interfaces.

## When the situation changes

Trigger: A price comparison treats bare metal as synonymous with unmanaged software.

Mechanism: Customer-operated serving on CKS and CoreWeave Dedicated Inference can both bill GPU-hours on bare metal, but only the second includes routing, scaling and serving lifecycle work.

Response: Compare the responsibility boundary and the invoice unit separately.

## Apply the idea

A provider offers managed serving on bare-metal GPUs and bills GPU-hours. Is that contradictory?

<details>
<summary>Reveal the worked answer</summary>

No. Hardware access, operating responsibility and billing unit are separate choices.

The provider can operate software directly on dedicated hardware and bill the reserved or consumed capacity.

</details>

**The idea to keep:** Separate capacity billing, hardware access and software responsibility.

## Sources

- [CoreWeave 2025 annual report](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000104/crwv-20251231.htm) — CoreWeave · Reviewed 2026-09-17. Capacity contracts, revenue mix and asset-level financing.
- [CoreWeave bare metal](https://www.coreweave.com/products/bare-metal) — CoreWeave · Reviewed 2026-09-17. Kubernetes runs directly on bare-metal servers.
- [CoreWeave inference service options](https://www.coreweave.com/products/dedicated-inference) — CoreWeave · Reviewed 2026-09-17. Customer-operated and managed serving differ; dedicated GPU-hour billing and serverless token billing coexist.
- [Create a CoreWeave SUNK cluster](https://docs.coreweave.com/products/sunk/deploy_sunk/create-sunk-cluster) — CoreWeave · Reviewed 2026-09-17. Managed Slurm on Kubernetes.
- [EC2 Spot Instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-spot-instances.html) — AWS · Reviewed 2026-09-17. Spot instances can be reclaimed, unlike an ordinary on-demand commitment.
- [CoreWeave — CoreWeave Announces Multi-Year Agreement With Anthropic, April 10, 2026](https://www.coreweave.com/news/coreweave-announces-multi-year-agreement-with-anthropic) — CoreWeave · Published 2026-04-10 · Reviewed 2026-09-26. Anthropic will use CoreWeave's cloud platform to run workloads at production scale, supporting development and deployment of Claude models.
- [Fireworks AI — How Cursor built Fast Apply using the Speculative Decoding API](https://fireworks.ai/blog/cursor) — Fireworks AI · Published 2024-06-23 · Reviewed 2026-09-26. Cursor trained a specialized Fast Apply model, and Fireworks deployed and served it on its inference engine through its Completion API.
