import type { ProductItem, ProductListResponse } from "../types/api";
import { apiFetch } from "./client";

export function getProductList(params: {
  page?: number;
  page_size?: number;
}): Promise<ProductListResponse> {
  const q = new URLSearchParams();
  if (params.page != null) q.set("page", String(params.page));
  if (params.page_size != null) q.set("page_size", String(params.page_size));
  return apiFetch<ProductListResponse>(`/api/v1/products?${q}`);
}

export function getProductById(id: string): Promise<ProductItem> {
  return apiFetch<ProductItem>(`/api/v1/products/${id}`);
}
