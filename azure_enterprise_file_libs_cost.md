## 💰 Enterprise File Library Cost Summary (OwlONE)

| Cost Type | Continuous? | When It Applies | Associated Fee Amount* |
|---------|------------|----------------|------------------------|
| **File Upload / Ingestion (Overall)** | ❌ No | Each time a file is uploaded or re-uploaded | **~$0.02 per page (one-time)** |
| Document processing (OCR & structure) | ❌ No | On upload / re-upload | Included in ~$0.02 per page (Azure AI Document Intelligence) |
| Embedding generation | ❌ No | On upload / re-upload | Charged per token (Azure OpenAI embeddings; varies by model) |
| Processing orchestration | ❌ No | On upload | Per job execution (minimal, bundled into ingestion estimate) |
| **Azure Blob Storage** | ✅ Yes | As long as files exist | ~$0.018–$0.023 per GB/month (region & tier dependent) |
| **Azure AI Search (Enterprise index)** | ✅ Yes | As long as the Enterprise library exists | **~$981 per Search Unit (SU) per month** |
| Semantic ranker | ❌ No | Only when semantic search is used | First 1,000 requests/month free, then **$1 per 1,000 requests** |

\*Fee amounts are approximate and region-dependent; exact charges appear in Azure Cost Management.