import type { CartResponse } from "../types/api";
import { apiFetch } from "./client";

export function getCart(cartId?: string): Promise<CartResponse> {
  const headers: Record<string, string> = {};
  if (cartId) headers["X-Cart-Id"] = cartId;
  return apiFetch<CartResponse>("/api/v1/cart", { headers });
}

export function addCartItem(
  productId: string,
  quantity: number,
  cartId?: string
): Promise<{ id: string; product_id: string; quantity: number }> {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (cartId) headers["X-Cart-Id"] = cartId;
  return apiFetch("/api/v1/cart/items", {
    method: "POST",
    headers,
    body: JSON.stringify({ product_id: productId, quantity }),
  });
}
