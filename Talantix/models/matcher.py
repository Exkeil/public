import faiss
import numpy as np

def match_resumes_to_vacancies(resumes, vacancies, resume_embeddings, vacancy_embeddings, top_k=3):
    dim = resume_embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vacancy_embeddings.cpu().numpy())
    dists, indices = index.search(resume_embeddings.cpu().numpy(), top_k)

    for i, res in enumerate(resumes):
        print(f"\n📄 Резюме: {res[:80]}...")
        print("🔍 Лучшие вакансии:")
        for rank, idx in enumerate(indices[i]):
            print(f"  {rank+1}. {vacancies[idx][:80]}... (dist = {dists[i][rank]:.4f})")