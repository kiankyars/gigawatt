# What a GPU cloud actually sells

Generated reading view. Edit [`course/expansion/heat-delivery-operations.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/heat-delivery-operations.json), lesson `d15-capacity-ledger`, then run `uv run gigawatt-expand`.

**15. GPU cloud economics · Authored draft**

Separate capacity billing, hardware access and software responsibility.

**Driving question:** What is the customer buying, and who operates it?

## Capacity, not a successful training run

A neocloud supplies GPU computing capacity and associated services. Its customer may buy a dedicated cluster for a term or consume resources by the hour. The bill need not depend on a successful training run. CoreWeave’s 2025 annual report describes committed capacity access and usage-based access; over 98 percent of that year’s revenue came from committed contracts.

A model API is a different product layer. CoreWeave’s product comparison includes GPU-hour billing for dedicated inference and token billing for serverless inference. A lab can calculate its internal cost per token or training run even while paying its infrastructure supplier for GPU-hours. Keeping those perspectives separate avoids pretending every facility sells completed AI tasks.

## Bare metal does not settle software responsibility

Bare metal describes hardware access without a virtualization hypervisor. It does not mean that the supplier simply hands over an SSH key and stops operating anything. A supplier still supports the contracted hardware, network and facility; software responsibility varies by service. CoreWeave describes Kubernetes on bare metal and a managed Slurm-on-Kubernetes product, SUNK.

For an inference customer, compare running a serving stack on CKS with Dedicated Inference: the latter moves routing, scaling and serving lifecycle work to the provider. Both can retain GPU-hour billing. Containers, Kubernetes and Slurm are not alternatives to bare metal: they can run on it. A purchase decision therefore needs both the hardware access model and the operating responsibility boundary.

## Three offers that must not be conflated

On-demand means access without a multi-year capacity commitment, billed as specified by the provider. An explicitly interruptible Spot product can be reclaimed; AWS EC2 documents that behavior. A short-term bilateral market rental is not automatically interruptible merely because someone calls its price spot. A reservation adds a capacity and payment commitment defined in its contract.

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

Mechanism: The offers contain different services.

Response: Compare the responsibility boundary and the invoice unit separately.

## Apply the idea

A provider offers managed serving on bare-metal GPUs and bills GPU-hours. Is that contradictory?

<details>
<summary>Reveal the worked answer</summary>

No. Hardware access, operating responsibility and billing unit are separate choices.

The provider can operate software directly on dedicated hardware and bill the reserved or consumed capacity.

</details>

**The idea to keep:** Separate capacity billing, hardware access and software responsibility.

## Sources and reading boundaries

- [CoreWeave 2025 annual report](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000104/crwv-20251231.htm) — Capacity contracts, revenue mix and asset-level financing. Read 2026-09-17. Fiscal 2025 observations; these are not claims about every provider or every private contract.
- [CoreWeave bare metal](https://www.coreweave.com/products/bare-metal) — Kubernetes runs directly on bare-metal servers. Read 2026-09-17. Product architecture, not a claim of customer ownership or a benchmark.
- [CoreWeave inference service options](https://www.coreweave.com/products/dedicated-inference) — Customer-operated and managed serving differ; dedicated GPU-hour billing and serverless token billing coexist. Read 2026-09-17. Current product descriptions reviewed; actual contract inclusions govern.
- [Create a CoreWeave SUNK cluster](https://docs.coreweave.com/products/sunk/deploy_sunk/create-sunk-cluster) — Managed Slurm on Kubernetes. Read 2026-09-17. Documentation describes this product, not all Slurm deployments.
- [EC2 Spot Instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-spot-instances.html) — Spot instances can be reclaimed, unlike an ordinary on-demand commitment. Read 2026-09-17. AWS interruption policy; not a definition of every market use of spot.
